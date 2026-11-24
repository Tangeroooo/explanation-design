# 집계 endpoint 설계 조건 — 합성 사례 v1

작은 팀의 기존 서비스에 보고서 집계 endpoint를 추가한다. 운영자가 관리하는 외부 DB와 기존 broker가 있으며 새 상시 service 운영은 피하고 싶다. 특정 제품·언어에 의존하지 않는다.

- 기존 public contract: 접수 응답은 작업 완료가 아니다. 응답에 job ID를 주고 이후 상태를 조회할 수 있다.
- 필수: `accepted`로 응답한 작업은 API process 재시작 후에도 조회·복구할 수 있어야 한다.
- 계산은 하나의 외부 DB 읽기와 결과 저장으로 구성한다. 결과 key는 job ID로 고정할 수 있다.
- 중복 계산은 허용하지만 같은 job ID의 최종 결과가 여러 개 생기면 안 된다.
- 요청 수·실행 시간·처리량 수치는 아직 측정하지 않았다. 임의 SLA나 성능 점수를 만들지 않는다.
- DB는 transaction과 unique constraint를 지원한다. row lease·조건부 update의 정확한 지원은 아직 확인하지 않았다.
- broker의 재배달·ack·보존 설정과 DB/broker 간 atomicity는 확인하지 않았다.
- 상태 응답의 field 이름과 job ID 형식은 유지해야 한다. 내부 scheduling과 storage table은 변경할 수 있다.

요청: process-local queue, DB job table + 같은 배포 단위의 worker, broker worker를 비교하고 현재 조건의 추천안과 추천이 바뀌는 조건을 설명한다. 구현 코드는 제공되지 않았다.
