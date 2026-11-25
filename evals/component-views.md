# 컴포넌트 표현·표시 굵기 실제 적용

2026-11-25. 사용 중 순서 중심 그림이 반복되고 제목·선이 얇아 보인다는 피드백에 따라 지침과 실제 제작을 함께 확인했다. 사용자가 보았던 원본 이미지는 제공되지 않았으므로 그 이미지의 원인을 해상도로 단정하지 않는다.

## 수정한 판단 경로

- 설계·아키텍처 요청은 컴포넌트·인터페이스·소유권·공유 자원을 먼저 표현한다. 순서가 질문일 때의 sequence는 유지한다.
- 새 설계 경로도 architecture reference를 읽게 연결했다. 메커니즘의 인과 추적을 모든 설계 그림의 단계 나열로 일반화하지 않는다.
- 제목 28–32px/700, 주요 선 2–2.5px, 의미 있는 경계 1.5–2px, 국소 강조 3px를 실제 표시 기준으로 적용한다.
- 벡터를 보존하고 PNG는 표시 치수의 2배로 만든다. 큰 비트맵과 실제 표시 굵기는 별개로 확인한다.

## 독립 제작과 평가

새 문맥의 제작 agent에게 수정된 스킬, [합성 원본](../examples/architecture/system.md), 구조·공유 범위·helper 의미·worker 증가를 설명하고 SVG/PNG를 달라는 요청을 전달했다. 이전 예제·평가 기록·정답은 읽지 않도록 했다. 원본은 기존 transfer 입력의 Ownership 절을 분리한 것으로, 완전히 새로운 분야의 holdout은 아니다.

제작자는 다음 두 그림을 선택했다.

1. [컴포넌트 구조](../examples/architecture/structure.svg): P 상세와 Q 요약, 중첩 소유 경계, worker별 mailbox, 프로세스당 하나의 pool, 네 번째 worker 제안.
2. [인자와 기록 대응](../examples/architecture/keys.svg): 같은 소스 정의를 공유해도 인자가 다르면 기록 대상이 다름. 좌우 조건 비교는 실행 순서가 아니다.

별도 새 문맥 평가자가 먼저 1× PNG만 읽고 [첫 해석](../examples/architecture/review-phase1.md)을 보존한 다음 원본·명세·관측과 대조했다. [평가 기록](../examples/architecture/review.md)에서 “규칙이 없다”가 미명시를 기능 부재로 표현하는 문제를 발견했다. 생성기·설명·그림을 “규칙은 주어지지 않았다”로 고쳐 재생성하고 한 차례 재검토해 해결했다. blocking 0건이며 실제 사람의 이해도 향상 측정은 아니다.

## 실제 렌더 관측

| 항목 | 관측 |
|---|---|
| 표시/viewBox | structure 1280×840, keys 1280×788 |
| PNG | 2560×1680, 2560×1576; 각각 2배 |
| 제목 | 실제 CSS 30px / weight 700, 렌더에서 굵기 확인 |
| 연결선·경계 | 주요 화살표 2.5px, 의미 있는 경계 1.5–2px, 제안 강조 3px; CSS 표시 폭과 viewBox 폭 동일 |
| 실제 폰트 | CDP에서 Noto Sans KR variable font 및 DejaVu Sans Mono 사용 확인 |
| 좁은 화면 | 390px 페이지 폭 유지, 그림 영역만 1280px 내부 스크롤 |
| SVG 이식 | 외부 요청 차단 상태에서도 내장 폰트 사용 관측 |
| 기하 | 설치된 검사기에서 두 그림 모두 0 findings; 실제 이미지의 잘림·겹침 미관측 |

[관측 JSON](../examples/architecture/render-observations.json), [검사 결과·해시](../examples/architecture/verification.json), [재생성 방법](../examples/architecture/REPRODUCE.md)을 보존했다. 저장소 경로로 옮긴 후에도 HTML·문서 재생성이 byte-for-byte 동일했고 브라우저 관측을 다시 실행했다. 제목 굵기와 실제 computed stroke 확인도 추가했다. 주 agent도 두 그림을 열어 확인했다.

## 구분해야 할 제한

- diagram-design의 `self_check.py`는 font data URL을 금지하여 두 그림에서 실패한다. 검사기를 바꾸거나 통과로 기록하지 않았다. 실제 폰트·기하·의미 검증과 별개인 호환성 제한이다.
- CDP의 `Noto Sans KR Thin`은 variable font의 기본 metadata 이름이다. `wght` 100–900과 face 선언, computed 700, 실제 굵은 렌더를 확인했지만 모든 glyph의 내부 축 적용을 독립 검증하지는 않았다.
- 현재 예제는 경계·공유·매핑을 검증한다. 저장소·로그·파일 등 모든 도형 유형, 다른 브라우저·편집 도구, 실제 production 성능·동시성은 검증하지 않았다.
- `sequence-still-valid` 사례는 순서가 질문일 때 sequence를 유지하는 회귀 입력으로 추가했으나 독립 실행하지 않았다. 지침상 조건 분기는 검토했다.
- 문서 전체의 한국어 폰트와 폭은 이 예제의 `finalize_document.py`가 적용한다. 공용 assembler의 기본 CSS를 변경한 것은 아니다.

저장소 package/example 검사·기존 테스트 14개·공식 skill validator·diff 검사를 통과했다. 이 결과와 실제 제작·평가의 범위는 구분한다.
