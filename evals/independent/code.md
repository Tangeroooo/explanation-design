# `deliver()`가 보장하는 것과 실패 뒤 남는 것

`deliver()`는 `send()`가 정상 완료한 뒤에만 `ack()`를 호출하며, 둘 다 정상 완료하면 `"acked"`를 반환합니다. 그러나 반환값만으로 실제 데이터의 영속성이나 무중복 전달을 보장할 수는 없습니다. 제공된 파일에는 외부 구현 대신 `Protocol`만 있고, `send`와 `ack`를 묶는 transaction·보상·retry·deduplication 코드가 없습니다.

## 용어와 확인 범위

- **정상 완료**: coroutine이 예외 없이 반환했다는 뜻입니다. 외부 서비스에서 어떤 효과가 확정되는지는 해당 구현의 계약이 필요합니다.
- **부수 효과**: sink의 기록·전송 또는 broker의 ack 상태 변경처럼 호출 밖에 남는 변화입니다.
- **retry**: `deliver()` 전체를 다시 호출하는 경우를 뜻합니다. 현재 함수는 스스로 retry하지 않습니다.

읽은 범위는 [worker.py](../../examples/code/input/worker.py#L20)의 23줄 전체입니다. `Sink.send`와 `Broker.ack`의 구체 구현·호출자·broker 재배달 정책은 제공되지 않았습니다. 코드의 목적을 확정할 상세 spec도 없습니다. 함수명에서 전달 의도는 추측할 수 있지만, 아래 동작은 실제 statement 순서에 근거합니다.

## 실제 구조와 시나리오

`Message`는 frozen dataclass이며 ID와 payload를 담습니다. `deliver()`가 소유하는 저장 상태는 없고, 상태 변화는 전달받은 sink와 broker의 구현에 달려 있습니다. `await`가 있으므로 두 호출 사이 또는 호출 도중 caller가 취소될 수 있지만, 동시성 제어와 취소 보상은 이 함수에 없습니다.

| 시나리오 | 이 함수에서 확인되는 흐름 | 함수 종료 뒤 외부 상태 |
|---|---|---|
| 두 호출 정상 완료 | `send` 완료 → `ack` 완료 → `"acked"` 반환 | 각 구현이 정상 반환에 약속한 효과. 영속성 수준은 미확인 |
| `send`가 예외 | 예외가 caller로 전파, `ack` 미호출 | 효과가 전혀 없거나, 효과는 생겼는데 응답만 실패했을 수 있음 |
| `send` 정상 완료, `ack` 예외 | `send` 완료 → `ack` 호출 → 예외 전파 | sink 효과가 이미 생겼을 수 있음. ack도 적용 전 실패인지 적용 후 응답 실패인지 이 함수는 구분 못 함 |
| 첫 호출 후 전체 retry | 처음부터 `send` 다시 호출 | sink가 ID로 중복을 제거하지 않으면 효과가 반복될 수 있음 |
| 호출 중 취소·process 종료 | 완료된 앞 단계는 rollback하지 않음 | 어떤 외부 단계까지 적용됐는지 별도 조회·계약 필요 |

핵심은 **예외가 났다는 사실과 부수 효과가 없다는 사실이 같지 않다**는 점입니다. `send()`가 성공했고 `ack()`가 실패한 경우 caller가 전체 작업을 다시 호출하면 `send()`도 반복합니다. broker가 실제로 재배달하는지는 정책을 확인해야 하며, 이 코드만으로 자동 재배달을 단정할 수 없습니다.

## 실제 실행 관측

별도 fake sink·broker로 원본 `deliver()`를 호출했습니다. production 서비스 대신 fake가 메모리 list에 기록하는 효과를 관측했습니다.

- 정상: `send:called → send:effect → send:returned → ack:called → ack:effect → ack:returned`, 반환 `"acked"`.
- send 효과 전 실패: sink 기록 0개, ack 호출 0회.
- send 효과 후 실패: sink 기록 1개, ack 호출 0회. **send 예외가 효과 부재를 뜻하지 않는 반례**입니다.
- ack 효과 전 실패: sink 기록 1개, ack 기록 0개.
- ack 효과 후 응답 실패: sink 기록 1개, ack 기록 1개지만 함수는 예외로 종료.
- ack 효과 전 실패 후 전체 retry: 동일 message ID의 sink 기록이 2개로 증가하고 두 번째 호출은 `"acked"` 반환.

실행 코드와 전체 결과: [run_observations.py](run_observations.py), [observations.json](observations.json). 이는 원본 함수가 허용하는 제어 흐름을 보이는 테스트입니다. 실제 sink·broker의 정책, 내구성, 장애 빈도를 검증한 결과는 아닙니다.

## 위험도와 대처

중복 효과가 결제·메일 발송처럼 비용을 만들면 결과가 중요합니다. 하지만 현재 자료로 실제 발생 빈도나 서비스 위험 등급을 추정할 수 없습니다. sink의 idempotency 지원과 broker의 재배달 설정에 따라 위험이 크게 달라집니다.

- **단기**: concrete `send`/`ack` 구현과 호출자의 retry 정책을 확인하고, message ID별 시도·sink 결과·ack 결과를 관측합니다. 예외를 모두 무효 처리로 분류하지 않습니다.
- **중기**: sink가 message ID로 원자적 중복 제거를 지원하는지 확인하고, 재시도 범위·timeout 후 상태 조회·취소 경계를 계약으로 만듭니다. 동일 ID 동시 호출과 응답 유실도 테스트합니다.
- **장기**: 실제 무중복 요구와 저장소 특성에 따라 inbox/outbox 또는 단일 transaction 경계를 비교합니다. 설계 이름만으로 exactly-once를 주장하지 않습니다.

미확인: 정상 `send` 반환의 내구성, ack 적용 여부 조회 가능성, broker 재배달·보존 정책, sink deduplication 범위·기간, caller의 retry·취소 정책. 이 정보가 있어야 전달 보장을 더 강하게 설명할 수 있습니다.

표와 실행 trace가 질문에 충분하므로 그림은 만들지 않았습니다. 구조 검토와 6개 fake 실행은 완료했고, production integration과 시각 render 검증은 수행하지 않았습니다.
