# 독립 적용 작업 기록

## 입력과 독립성

부모가 지정한 스킬과 raw input만 읽었습니다. `evals/`, 기존 output, document 파일이나 정답은 읽지 않았습니다. 작업 산출물은 ``에만 기록했습니다. repository 변경·Git·외부 전송·패키지 설치는 수행하지 않았습니다. 원본 worker import 시 bytecode 쓰기를 비활성화했습니다.

## 사용한 지침

- `skills/explanation-design/SKILL.md`
- `references/code-reading.md`
- `references/mechanisms.md`
- `references/evidence.md`
- `references/design-derivation.md`
- `references/comparison.md`
- `references/data.md`
- `references/verification.md`

복잡한 세 요청에 관련 reference만 골랐고, 별도 그림은 세 요청 모두 표·짧은 flow로 충분하다고 판단했습니다. 짧은 percentage point 질문은 한 문단으로 답했습니다. 이 평가가 요청한 보존용 Markdown 외 추가 문서 묶음은 만들지 않았습니다.

## 실제 실행

`PYTHONDONTWRITEBYTECODE=1 python3 run_observations.py`

결과: exit 0. 원본 `deliver()`를 fake sink/broker로 실행한 6개 시나리오와 수치 계산 assertion 통과. JSON에 source SHA-256·trace·계산 저장.

원본 input:

- `examples/code/input/worker.py`
- `examples/design/input/requirements.md`
- `examples/data/input/cohorts.csv`
- `examples/data/input/context.md`

## 검증 범위

구조: 원본 파일을 읽고 Markdown 산출물·JSON 결과를 작성. package validator 또는 assembler는 실행하지 않음.

근거·의미: 코드 23줄 전체와 Protocol 경계를 정적 추적, fake 효과 전/후 실패·retry를 실행. 데이터는 원본에서 Decimal 재계산. 설계는 요구사항의 보장과 미확인 기능을 기준으로 비교.

시각: 그림·HTML을 제작하지 않아 render 시각 검증은 미수행. production DB/broker/sink의 보장·성능·내구성·장애 빈도는 미검증.

## 사용 중 발견한 스킬 문제

치명적 실행 장애는 없었습니다. 다음 두 점은 개선 후보입니다.

1. `code-reading.md`의 예시가 이번 입력의 `send → ack`와 거의 동일합니다. 실제 적용에 도움이 되지만 이 case를 학습된 예시와 독립인 일반화 검증으로 보기는 어렵습니다. 다른 형태의 상태 갱신·취소·resource lifetime 입력을 별도 holdout으로 추가하면 범용성을 더 잘 평가할 수 있습니다. 이번 실행에서는 예시보다 넓은 `send/ack 효과 적용 후 응답 실패`를 포함했습니다.
2. 설계 reference의 “명백히 부적합한 대안을 들러리로 쓰지 않는다”는 사용자 지정 후보가 필수 조건을 어기는 경우의 처리 문구가 없습니다. 이번처럼 local queue가 명시 후보이면 삭제하는 대신 불충족 이유를 보여주는 것이 적절합니다. “사용자가 지정한 후보는 유지하고 탈락 조건을 설명한다” 정도의 구분을 보완하면 오해가 줄어듭니다.

코드·설계·데이터의 내용을 바꾸도록 만드는 지침 충돌은 없었습니다. 짧은 질문에서 과잉 제작을 피하는 분기는 명확했습니다.
