# 컴포넌트 명세 전달 시험

2026-11-26. 범용 제작 폼에 요소 이름만 적어도 넘어갈 수 있던 공백을 보완했다. 구조·설계 그림에만 [컴포넌트 명세](../../skills/explanation-design/assets/component-brief.ko.md)를 붙이고, 구성별 소유권·수량·내부 구획·근거 있는 접점·관계 의미·상세/요약 결정을 제작 전에 기록한다. 좌표와 선 경로는 제작자가 정한다. 미상·해당 없음·의도적 생략은 구분한다.

## 입력과 독립성

- [원문 S1](input.md)은 가상 시스템이다. 기존 P/Q 소유권 예제에 명시적인 `submit(job)` / `enqueue(job)` 계약을 추가한 별도 입력이며 실제 SeahorseDB나 원래 예제의 구현 사실이 아니다.
- 주 agent가 새 양식에 따라 [완성된 제작 명세](brief.md)를 작성하고 S1과 대조했다.
- 새 문맥 제작자에게는 완성된 명세와 관련 스킬 지침만 제공했다. 원문 S1, 기존 그림, 작성자 대화, 평가 기준은 읽지 않도록 했다. 파일시스템 접근 자체를 격리한 것은 아니다.
- 제작 전 모호함과 남은 결정을 [handoff-notes.md](output/handoff-notes.md)에 먼저 기록하게 했다. 제작자는 시스템 사실을 추가할 필요 없이 좌표·높이·접점 배치 등을 정할 수 있다고 보고했다.
- 또 다른 새 문맥 평가자는 초기 1× PNG와 독자 질문만 받아 [첫 해석](review-phase1.md)을 보존했다. 이후 S1·명세·테마·현재 이미지와 실제 도구 관측을 받아 [근거 대조](review.md)를 수행했다. 작성자 자기평가와 채점 기준은 제공하지 않았다.

## 관찰한 결과

| 명세의 정보 | 그림만 본 평가자의 해석 |
|---|---|
| 논리 S와 배포 P/Q | S를 세 번째 프로세스로 보지 않고 관점 전환으로 읽음 |
| worker별 mailbox, 프로세스별 pool | mailbox를 각 worker의 내부 상태로, pool을 해당 프로세스의 공유 자원 하나로 읽음 |
| 입력 접점과 전달 대상 접점 | coordinator의 `submit(job)` 입력과 선택된 mailbox의 `enqueue(job)` 전달을 구분 |
| 대표 연결과 미상 선택 규칙 | worker[3] 고정·broadcast·실행 순서를 추론하지 않음 |
| P worker 추가와 Q 요약 | P의 worker와 mailbox만 하나 늘고 기존 pool을 공유하며 Q는 그대로임을 읽음 |
| 근거 부족과 생략 | 소비 방식·선택 규칙·pool 계약·Catalog 배포를 미상으로 유지하고, Q의 상세 생략과 구별 |

초기 이미지에서는 전달선 수직 구간이 다른 worker의 경계와 겹쳤다. 주 agent와 제작자가 발견해 worker 사이 여백으로 경로를 옮기고 끝점을 `enqueue(job)` 행에 맞췄다. 겹치던 보조 문구도 정리했다. 명세의 시스템 사실은 바꾸지 않았다. 초기본은 `output/preview/component-handoff-initial.png`, 최종본은 `output/preview/component-handoff-1x.png`다. 첫 해석 당시 파일 이름은 후자였으며 초기본으로 복사해 보존했다.

독립 평가자는 수정 후 렌더와 근거가 일치하고 의미 오류·판독 장애가 없다고 보고했다. 이 경로 수정은 독립 평가자가 처음 발견한 결함으로 세지 않는다. 한 차례의 렌더 수정이며, 독립 평가가 요구한 추가 수정은 없었다.

## 도구 검증과 산출물

- 편집 원본 [HTML](output/component-handoff.html), [SVG](output/component-handoff.svg), [2배 PNG](output/component-handoff.png)를 보존했다. 표시 크기 1280×1088, PNG 2560×2176이다.
- [브라우저 관측](output/render-checks.json): HTML/SVG 모두 실제 사용 폰트 목록에 Noto Sans KR와 DejaVu Sans Mono가 나타났다. 제목 computed 30px/700, 텍스트 겹침·viewBox 이탈 없음. 390px 화면에서 문서 폭은 390px, 그림 영역은 1280px 내부 스크롤이다.
- 설치된 diagram-design의 기하 검사는 0 findings다. `self_check.py`는 내장 폰트 data URL 두 건을 금지해 실패한다. 검사기를 약화하거나 전체 검사 통과로 표시하지 않았다. 재현 명령과 제한은 [제작 기록](output/handoff-notes.md)을 참고한다.
- 저장소 `scripts/check.py`의 패키지·예제 구조 검사 및 기존 테스트 14개, 공식 skill validator를 통과했다. diff 검사도 통과했다. 이 검사는 위 의미·시각 평가와 별개다.

## 검증하지 않은 것

이 시험은 **완성된 명세를 전달했을 때의 제작 결과**를 확인한다. 독립 agent가 원문에서 명세를 작성하는 단계, 이전 폼과의 통제 비교, 실제 사람의 이해도 개선이나 여러 분야에서의 일반적 품질 향상은 측정하지 않았다. 기존 P/Q 모델을 확장한 단일 사례이므로 새 분야의 holdout도 아니다.

실제 운영 동작·성능·동시성, 다른 브라우저/편집기, 최종 게시 화면은 확인하지 않았다. CDP의 `Noto Sans KR Thin`은 variable font 기본 메타데이터 이름이며, computed 700과 육안 굵기는 확인했지만 모든 글리프의 내부 weight 축 적용이나 모든 텍스트 역할별 폰트 배정을 독립 검증한 것은 아니다. 순서만 답하는 기존 회귀 입력에는 부록을 요구하지 않는 지침을 검토했으나, 그 사례를 이번에 새로 렌더링하지 않았다.
