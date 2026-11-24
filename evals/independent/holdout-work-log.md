# 수정 후 독립 holdout 평가 기록

## 읽은 자료와 독립성

요청된 raw input `evals/holdout/input/cache.py`, `evals/holdout/request.md`만 추가 평가 입력으로 읽었습니다. 다른 evals 파일·정답·기존 holdout 결과는 읽지 않았습니다. 스킬 `SKILL.md`와 필요한 `code-reading`, `mechanisms`, `evidence`, 수정된 `design-derivation` reference를 읽었습니다.

원본 repository를 수정하지 않았고, 외부 전송·Git·패키지 설치를 수행하지 않았습니다. Python 원본 import는 `PYTHONDONTWRITEBYTECODE=1`로 실행했습니다. 생성물은 평가용 임시 폴더에만 저장했습니다.

## 수행과 결과

명령:

```text
PYTHONDONTWRITEBYTECODE=1 python3 run_holdout.py
```

exit 0, 원본 refresh + isolated fake로 9개 시나리오의 assertion 통과. 정상, read 실패, seen 실패, seen 대기 중 취소, 정상 후 release 실패, release가 원래 오류를 가리는 경우, acquire 실패, 내부 선점 후 acquire 취소, same-key read 완료 순서 역전을 실행했습니다. 모든 trace와 원본 SHA-256은 `holdout-observations.json`에 저장했습니다.

`holdout.md`는 구조 → 한 호출 흐름 → 지점별 실패·취소 → 동시 실행 → 실제 관측 → 대처 순서로 작성했습니다. 부수 효과와 함수 성공을 분리하고, finally가 release 호출을 보장하는 범위와 release 성공의 차이, acquire가 try 밖인 경계, module 전역 cache와 request-scoped 주석의 차이를 설명했습니다.

## 수정된 설계 후보 문구 재평가

수정된 문구:

> 현실적 대안 2~3개를 같은 평가 축으로 비교한다. 명백히 부적합한 대안을 들러리로 추가하지 않는다. 사용자가 지정한 후보가 필수 조건을 어기면 후보를 유지하고 탈락 이유와 가능해지는 조건을 설명한다.

이 문구를 이전 raw requirements에 적용하면 process-local queue, DB job table + 같은 배포 단위 worker, broker worker를 모두 유지하는 것이 맞습니다. local queue는 순수 메모리만으로는 accepted 이후 재시작 복구를 충족하지 못한다고 설명하고, 유실 허용으로 계약이 바뀌거나 별도 durable source가 있을 때 가능해지는 조건을 덧붙입니다. broker는 계약 미확인이므로 부적합으로 확정하지 않습니다. DB table은 현 조건의 조건부 추천을 유지합니다.

따라서 이전 `design.md`의 세 후보 유지·탈락 이유·전환 조건은 수정된 reference와 일치합니다. 문구 수정은 사용자 지정 후보를 삭제할 수 있는 모호함을 해소했고, 설명 결론 자체를 바꿀 필요는 없습니다.

## 검증 층과 한계

- 구조: raw input 읽기, Markdown·실행 코드·JSON 산출물 작성. package/assembler validator는 이번 평가에서 실행하지 않음.
- 근거·의미: 예시 send/ack와 다른 cache·resource lifetime·취소·동시성 사례에 적용. 9개 fake 시나리오로 가능한 실행을 확인. 특정 생산 환경 보장으로 확대하지 않음.
- 시각: 표·짧은 trace를 사용했고 그림/HTML render는 하지 않았음.

새롭게 드러난 치명적 스킬 결함은 없었습니다. 기존 code-reading의 `finally`, 자원 수명, await 앞뒤 취소, 상태 소유권, 미확인 외부 계약 지침으로 이번 입력을 처리할 수 있었습니다. holdout은 독립성 범위를 raw input과 미제공 외부 구현으로 제한한 행동 평가이며 production 검증은 아닙니다.
