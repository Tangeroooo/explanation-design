# 보고서 집계 job: 현재는 DB job table을 우선

현재 조건에서는 **DB에 job을 먼저 commit하고, 같은 배포 단위의 worker가 미완료 job을 복구·처리하는 방식**을 추천합니다. API 재시작 후 복구할 기록이 필요하고 기존 DB의 transaction·unique constraint는 확인되어 있기 때문입니다. 단, DB의 atomic claim·lease 지원과 worker의 운영 방식은 아직 확인되지 않았으므로 이 추천은 구현 방향이며 production 동시성 보장이 검증된 상태는 아닙니다.

근거는 합성 요구사항 [requirements.md](../../examples/design/input/requirements.md#L3) 전체입니다. 실제 구현 코드는 제공되지 않았습니다. 아래 module·function·table 이름은 모두 제안입니다.

## 설계 목표와 현재 제약

유지할 계약:

- 접수 응답은 완료 응답이 아닙니다. 기존 job ID 형식과 상태 응답 field 이름을 유지합니다.
- `accepted` 응답한 job은 API process 재시작 후 조회·복구할 수 있어야 합니다.
- 같은 job ID의 최종 결과는 하나여야 합니다. 계산 자체의 중복은 허용합니다.

변경 가능한 내부는 scheduling과 storage table입니다. DB는 transaction·unique constraint를 지원하지만 lease·조건부 update의 정확한 지원은 미확인입니다. 기존 broker가 있더라도 ack·보존·재배달 설정과 DB/broker 간 atomicity는 확인되지 않았습니다. 요청량·실행시간·처리량이 없으므로 성능 SLA와 수치 순위는 정하지 않습니다. 새 상시 service 운영을 피하려는 작은 팀의 운영 제약도 반영합니다.

## 세 대안 비교

| 같은 평가 축 | Process-local queue | DB job table + 같은 배포 단위 worker | 기존 broker worker |
|---|---|---|---|
| `accepted` 후 재시작 복구 | 메모리만 사용하면 불충족. 별도 영속 기록을 넣으면 순수 local queue 대안이 달라짐 | commit된 job 기록을 기준으로 복구 가능하도록 설계 가능 | broker의 실제 보존·publisher 확인 계약을 검증해야 판단 가능 |
| 최종 결과 한 개 | queue 자체는 보장하지 않음. 저장소 unique job ID 필요 | 결과 table의 unique job ID로 강제 가능 | broker 사용과 별개로 결과 저장소 unique job ID 필요 |
| 기존 자원과 운영 | scheduling은 가장 작지만 필수 복구 계약을 충족 못 함 | 기존 DB 사용. polling·복구·worker lifecycle 운영 필요 | 기존 broker 활용 가능. worker·ack·dead-letter·적체 감시 등 실제 운영 절차 확인 필요 |
| 경계와 atomicity | memory enqueue와 영속 결과 사이에 crash gap | job 생성·상태·결과를 같은 DB transaction 범위로 묶을 수 있는지 설계·확인 | DB 기록과 broker publish 사이 dual-write gap. 필요하면 outbox 등 추가 설계 |
| 주요 실패·edge case | API 종료 시 대기 job 유실 | claim 경쟁·lease 만료·stale worker·DB 장애·복구 지연 | publish 응답 유실·재배달·ack 실패·중복·보존 만료 |
| 적합 조건 | 재시작 유실 허용 또는 다른 durable source 존재 | 현재 복구 요구, 기존 DB 활용, 규모 검증 전 | broker 계약·운영이 확인되고 burst 분리·독립 확장이 실제 필요 |

local queue는 사용자가 비교를 요청한 후보이며, 현재 필수 계약에 어긋나는 이유를 명시했습니다. broker는 부적합하다고 확정하지 않았습니다. 미확인 계약을 검증하면 현실적인 선택이 될 수 있습니다.

## 추천 설계의 data flow와 control flow

**접수**

```text
request → 기존 job ID 형식으로 ID 결정
        → DB transaction: job 기록 생성
        → commit 성공 확인
        → accepted + job ID 응답
```

commit을 확인하기 전에 `accepted`를 반환하면 필수 복구 계약을 지키지 못합니다. commit은 성공했는데 응답이 유실되는 경우에는 caller가 접수 여부를 모를 수 있습니다. 요청 재시도에서 같은 작업으로 묶을 안정적인 key가 현재 계약에 있는지 확인해야 합니다. 임의로 새 public field를 추가하지 않습니다.

**실행·복구**

```text
worker 시작·주기적 scan → 미완료 job 선택
                      → 안전한 claim (구체 DB 기능 확인 필요)
                      → 외부 DB 읽기·집계
                      → 결과 저장 + 완료 상태 확정
                      → 기존 상태 endpoint가 조회
```

job table은 복구 기준입니다. process-local notification을 추가하더라도 worker가 놓친 알림만을 이유로 job을 잃지 않도록 scan 경로가 필요합니다. “같은 배포 단위”는 별도 service 운영 부담을 줄이지만, 계산이 API와 CPU·connection pool을 경쟁할 수 있으므로 실행 수 제한·graceful stop·재시작 스캔을 정해야 합니다.

같은 DB에 결과를 두는 제안에서는 `results.job_id`의 unique constraint와 결과 기록·완료 상태의 transaction을 사용합니다. 두 worker가 계산하더라도 결과 삽입은 하나만 허용하고, 충돌한 worker는 이미 저장된 결과를 확인합니다. 결과가 다른 저장소에 있어 같은 transaction을 쓸 수 없다면 성공 상태와 결과가 어긋나는 복구 프로토콜을 별도로 설계해야 합니다.

claim·lease는 현재 DB 기능이 미확인입니다. 구현 전에 조건부 update·lock·fencing 등 가능한 primitive를 확인해야 합니다. 단순히 같은 deployment라는 이유로 단일 실행을 가정하면 rolling update 중 구·신 worker가 겹칠 수 있습니다. 초기 운영을 worker 하나로 제한하더라도 결과 unique constraint를 유지하고, 중복 실행과 상태 경쟁을 검증해야 합니다.

## 변경 위치 제안

실제 파일·함수로 확인된 이름은 없습니다. 예상 책임 경계는 다음과 같습니다.

| 제안 module / function | 책임 | 유지할 경계 |
|---|---|---|
| `api/jobs.create_job()` | 요청 검증, durable job commit 후 접수 응답 | 기존 job ID·응답 field |
| `api/jobs.get_job()` | 저장된 상태·결과 조회 | 기존 상태 API |
| `storage/jobs.insert_job()` / `claim_job()` | 접수 기록·동시 claim·복구 기준 | DB의 실제 지원 계약 확인 |
| `worker/run_job()` / `recover_jobs()` | 제한된 실행·scan·실패 및 재시작 복구 | API process와 자원 경쟁 관리 |
| `storage/results.store_once(job_id, result)` | 최종 결과 unique 제약·완료 확정 | 계산 중복과 저장 중복을 분리 |
| DB migration | jobs·results 및 unique key·필요 index | 구버전 reader/writer 공존·rollback |

## Trade-off와 위험 조건

- **DB commit 응답 유실**: job은 존재하지만 API는 실패 응답할 수 있습니다. 확인·조회·재시도 의미를 계약으로 정해야 합니다. `accepted` 응답한 작업의 복구 보장과 모든 요청의 정확히 한 번 접수는 별개입니다.
- **lease 만료 후 구 worker 계속 실행**: 새 worker와 중복 계산할 수 있습니다. unique 결과 key는 행 중복을 막지만 어떤 계산 결과를 채택할지는 별도 정책입니다. stale worker의 상태 덮어쓰기도 방어해야 합니다.
- **입력 데이터 변화**: 중복 계산이 다른 시점의 DB를 읽으면 결과가 달라질 수 있습니다. 하나만 저장하는 보장과 재현 가능한 동일 결과 보장은 다릅니다. snapshot/version 기준이 필요한지 확인합니다.
- **DB 장애**: 접수를 성공 처리할 수 없으므로 실패·재시도 의미가 필요합니다. 처리 중 장애는 미완료 job이 복구 대상에 남도록 설계해야 합니다.
- **처리 backlog**: polling과 같은 배포 단위 실행이 목표에 맞는지 측정해야 합니다. 현재 수치로 병목이나 충분한 성능을 단정할 수 없습니다.
- **migration·rollback**: schema와 상태 의미는 먼저 호환 가능하게 추가하고, 구버전 worker가 새 상태를 잘못 해석하지 않도록 배포 순서를 정합니다.

## 추천이 바뀌는 조건

broker의 publish 확인·보존·재배달·ack·운영 절차가 확인되고, burst 흡수나 API와 worker의 독립 확장이 필요한 것으로 측정되면 broker worker를 다시 비교합니다. 반대로 재시작 유실을 허용하도록 필수 계약을 바꾸거나 이미 다른 durable source가 있다면 local queue도 고려할 수 있습니다. 현재 계약은 그 조건이 아닙니다.

## 적용 순서

- **단기**: public contract와 복구 수용 기준 고정. DB 기능·broker 설정·worker lifecycle·결과 transaction 경계 조사. 요청량·실행시간·자원 사용 관측. commit 전후 종료 시 접수 상태가 어떻게 보이는지 재현.
- **중기**: DB job·unique result 최소 구현과 호환 migration. 접수 commit 직후 process 종료, 계산 중 종료, 완료 저장 중 실패, 동일 ID 병렬 실행, rolling update 겹침, 상태 조회를 integration 검증.
- **장기**: backlog·지연·API 자원 경쟁·운영 부담을 측정하고 분리 배포·broker·outbox 필요성을 재평가. 현재 정보로 미리 복잡성을 확정하지 않음.

남은 확인: atomic claim primitive, lease 만료·fencing 정책, 결과와 job 상태의 transaction 범위, 입력 snapshot 기준, 요청 재시도 key, 실제 broker 계약, workload와 지연 요구. 문서 기반 설계 평가만 수행했으며 실제 DB·worker integration과 성능·장애 검증은 수행하지 않았습니다. 세 대안의 동일 축 표와 짧은 flow로 판단이 가능해 다이어그램은 생략했습니다.
