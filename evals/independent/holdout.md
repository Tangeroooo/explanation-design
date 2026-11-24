# `refresh()` 실패·취소와 같은 key 동시 실행

**`record_seen()`에서 실패하거나 취소되어도 앞서 갱신한 cache는 되돌리지 않습니다.** permit을 정상 획득한 뒤에는 `finally`에서 `release()`를 호출하지만, 획득 중 실패·취소와 `release()` 자체의 실패는 별도로 봐야 합니다. 같은 key 요청의 실행 순서나 최신값 보존을 이 코드만으로 보장할 수는 없습니다.

근거는 [cache.py](../../evals/holdout/input/cache.py#L5) 전체 13줄입니다. `store`와 `pool`의 실제 구현은 제공되지 않았습니다. docstring은 “Request-scoped refresh”라고 하지만 `cache = {}`는 함수 밖의 module 전역입니다. 이 코드에서 cache는 요청별 객체가 아니라 같은 module instance를 사용하는 호출들이 공유하는 메모리 상태입니다. process 간 공유·영속성·TTL은 구현되어 있지 않습니다.

## 한 호출에서 실제 순서

```text
await acquire
→ try 진입
→ await read
→ cache[key] 대입
→ await record_seen
→ return 준비
→ finally에서 release 호출
→ release가 정상 완료하면 값 반환
```

이 흐름은 한 호출 안의 순서입니다. `record_seen()` 완료 전에 cache가 바뀌므로, 함수 전체 성공과 cache 갱신은 같은 atomic operation이 아닙니다.

| 실패·취소 지점 | cache | permit 처리와 종료 |
|---|---|---|
| `acquire()` 중 | 이 호출이 cache를 바꾸지 않음 | 아직 `try` 밖이므로 이 함수의 `release()` 호출 없음. 내부에서 선점한 자원의 복구는 pool 계약에 달림 |
| `read()` 중 | 이 호출의 대입은 실행되지 않음 | `finally`에서 release 호출 후 예외·취소 전파 |
| cache 대입 후 `record_seen()` 중 | 새 값이 이미 들어 있으며 rollback 없음 | release 호출 후 예외·취소 전파. seen 기록도 적용 전 실패인지 적용 후 응답 실패인지 미확인 |
| 두 await 정상 완료 | 새 값 유지 | release가 정상 완료해야 caller가 값을 받음 |
| `release()` 자체 실패 | 이미 한 cache 갱신은 유지 | release 예외가 정상 return 또는 원래 예외·취소를 가릴 수 있음 |

표에서 “이 호출이 바꾸지 않음”은 다른 동시 호출도 cache를 바꾸지 않는다는 뜻이 아닙니다. `finally`의 보장 역시 정상적인 Python stack unwinding 범위입니다. process 강제 종료 후 실행을 보장하지 않습니다. 또한 코드는 `release()`를 동기 함수로 호출합니다. 실제 API가 동기 release인지, 호출이 성공하면 permit이 실제로 반환되는지는 계약 확인이 필요합니다.

## 같은 key의 동시 요청

코드에 key별 lock, version 비교, request coalescing은 없습니다. `pool.acquire()`가 동시 실행 수를 제한할 가능성은 있지만, 구현이 없어 전역 제한인지 key별 제한인지·직렬화·fairness를 알 수 없습니다.

여러 permit을 허용하는 pool이라면 다음 실행이 가능합니다.

```text
요청 A 먼저 시작 → 오래된 값 read가 지연됨
요청 B 나중에 시작 → 새 값 read 완료 → cache[k] = 새 값 → 완료
요청 A read 완료 → cache[k] = 오래된 값 → 완료
```

따라서 마지막 **cache 대입**이 현재 값을 결정할 수 있으며, 먼저 시작한 요청이나 더 최신 데이터가 이긴다고 말할 수 없습니다. cache 대입 뒤 `record_seen()`에서 다시 대기하므로, 함수 반환 순서와 cache 대입 순서도 같을 필요가 없습니다. 여러 process에서는 각 process의 module cache가 따로 생길 수 있고, 이 파일에 이를 조정하는 장치는 없습니다.

## 실제로 실행한 범위

원본 `refresh()`를 import해 isolated fake store·pool·permit으로 9개 시나리오를 실행했습니다. [재현 코드](run_holdout.py)와 [관측 결과](holdout-observations.json)에 source SHA-256과 trace가 있습니다.

- read 실패: 기존 cache 유지, release 1회 호출.
- seen 기록 실패 및 기록 대기 중 취소: 새 cache 값 유지, release 1회 호출. 각각 `ValueError`, `CancelledError` 전파.
- release 실패: 정상 return 대신 `RuntimeError` 관측. seen 기록 실패와 겹치면 release 예외가 전파되고 원래 예외는 `__context__`에 남음.
- acquire 실패·획득 대기 중 취소: 이 함수의 release 0회. 내부에서 선점 후 대기하는 fake에서는 선점 상태가 그대로 남음. 실제 pool이 같은 문제를 가진다고 검증한 것은 아님.
- concurrent same-key: 뒤 요청의 `version-2`가 cache에 들어간 뒤 앞 요청의 `version-1`로 덮이는 실행 재현.

모든 assertion은 통과했습니다. 이는 코드가 허용하는 흐름을 재현한 것이며 실제 store의 일관성·seen 기록 내구성, pool의 취소 안전성·공정성·permit 회수는 미검증입니다. 표와 짧은 trace로 충분해 그림은 만들지 않았습니다.

## 대처와 남은 확인

- **단기**: `acquire/release`의 취소 안전성과 동기 API 계약, `read/record_seen`의 부수 효과·실패 의미를 확인합니다. cache 갱신과 seen 기록 중 무엇을 성공 조건으로 삼는지 정합니다.
- **중기**: 필요한 계약에 따라 갱신 시점, key별 직렬화·동일 요청 병합, version 비교, cleanup 오류 처리 중 최소 변경을 선택합니다. `record_seen` 뒤로 대입을 옮기는 것만으로 두 외부 상태의 atomicity가 생기지는 않습니다.
- **장기**: 여러 process가 동일 freshness를 공유해야 한다면 process-local cache 경계를 다시 설계합니다. 실제 요구가 없다면 분산 조정을 미리 추가할 이유는 없습니다.

위험의 실제 영향과 빈도는 cache가 무엇을 결정하는지와 pool 구현에 달려 있습니다. 현재 근거로는 stale 값·실패 후 남는 cache·cleanup 오류의 **가능 조건**까지만 설명할 수 있습니다.
