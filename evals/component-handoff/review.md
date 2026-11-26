# 2단계: 근거와 현재 렌더 대조

## 판정

현재 렌더에서 수정이 필요한 의미 오류나 판독 장애를 발견하지 않았다. 1단계에서 그림만 보고 읽은 소유 범위·수량·접점·변경 범위가 S1 및 제작 명세와 일치한다. 추가로 받은 CDP/브라우저 관측은 HTML/SVG에서 두 내장 폰트가 실제 사용되며, 390px 화면에서 그림이 1280px 폭을 유지하고 컨테이너가 가로 스크롤 범위를 갖는다는 점을 뒷받침한다. 다만 텍스트 용도별 폰트 배정과 glyph별 굵기 축까지 전수 검증한 자료는 아니다.

## 확인 범위와 독립성

- 1단계 기록 `review-phase1.md`는 수정하지 않았다. 당시에는 초기 이미지 한 장만 봤다.
- 이번에는 현재 `output/preview/component-handoff-1x.png`를 직접 열어 1280×1088 표시 이미지에서 판독했다.
- 대조 근거는 `input.md`의 S1.1–4, `brief.md`, 지정된 `diagram-theme.ko.md`다.
- 이미지 열람 후 현재 HTML/SVG를 읽어 좌표·색상·선 두께·폰트 선언·viewBox를 보조 확인했다. PNG 세 파일의 실제 픽셀 크기도 확인했다.
- 이후 `output/render-checks.json`과 측정 코드 `output/verify-render.py`를 받아 대조했다. 아래 도구 관측은 전달받은 실행 결과와 코드의 확인 범위이며, 검토자가 별도로 다시 실행한 결과는 아니다.
- 제작자 자기평가, handoff-notes, evals/cases, 다른 검토자의 결과는 읽지 않았다. 제작 산출물은 수정하지 않았다.

## 1단계 해석과 근거의 일치

| 확인 항목 | 그림에서 읽은 의미 | 대조 결과 |
|---|---|---|
| 논리/배포 관점 | S는 논리 서비스이며 P/Q는 S의 배포 프로세스 | S1.1 및 명세의 관점 전환과 일치. S를 세 번째 프로세스로 오해하지 않았음 |
| P의 현재 구성 | coordinator 1개, worker 3개, worker별 mailbox 1개, 공유 pool 1개 | S1.2와 일치. worker 번호는 반복 인스턴스를 구별하며 순서를 나타내지 않음 |
| pool 귀속 | pool은 worker 밖, 해당 프로세스 안에 존재 | S1.2 및 명세 C7과 일치. worker 내부의 `P.pool 공유`는 소유된 추가 pool이 아니라 바깥 자원 사용 설명으로 읽힘 |
| Q 요약 | coordinator 1개, worker 3개, 각자의 mailbox, Q.pool 1개 | S1.2와 일치. Q.pool은 P.pool과 별개임을 명시 |
| coordinator 접점 | 외부 입력 `submit(job)`과 job 전달 책임 | S1.3 및 명세 C4/R1과 일치. 전달선이 submit 입력 접점에서 출발하지 않음 |
| mailbox 접점 | 선택된 mailbox의 `enqueue(job)`로 전달 | S1.3 및 명세 C6/R1과 일치. 화살표 끝은 worker 이름 구획이 아니라 mailbox 경계의 작은 접점에 닿음 |
| 선택/공유 관계 | 대표 mailbox 하나로 전달, pool 공유선은 무방향 | S1.2–3과 일치. worker[3] 고정·broadcast·worker 실행 순서가 아님을 그림 안에서 확인 가능 |
| 논리 갱신 관계 | S에서 Catalog로 record 갱신 | S1.1/R3와 일치. 실제 호출 주체를 worker나 coordinator로 좁히지 않음 |
| 변경 범위 | P.worker[4]와 mailbox[4]만 추가, 기존 P.pool 공유, Q 불변 | S1.4와 일치. 변경 경계는 추가 worker와 mailbox에만 표시 |

## 사실과 미상의 분리

1단계에서 미확정으로 남긴 mailbox 소비 방식, 선택 규칙, 용량·순서, pool 종류·계약, Catalog 배포·내구성과 실제 갱신 컴포넌트는 근거에서도 미상이다. 그림이 빠뜨린 확정 사실로 취급하지 않는다.

새 worker를 선택 대상에 등록하는 별도 절차가 필요한지 역시 근거가 없다. 이 부분을 추가 설명하거나 coordinator 변경을 그리면 오히려 명세에 없는 계약을 만들게 된다. 처리량 보장과 병렬 실행도 주장하지 않으므로 증거 범위를 넘지 않는다.

Q의 개별 worker 연결선과 API 상세는 명세가 명시적으로 허용한 생략이다. 요약의 수량·mailbox 귀속·pool 분리는 보존되어 있어 수정 대상으로 보지 않는다.

## 현재 렌더의 가독성과 시각 명세

- 1280 CSS px 폭에서 제목, P/Q 경계, worker 이름, mailbox 구획, `submit(job)`/`enqueue(job)`, 접점과 화살촉, 공유선, 변경 점선을 모두 구별할 수 있다. 육안으로 텍스트 겹침이나 잘림을 발견하지 않았다.
- 초기 이미지보다 P의 worker 상자가 조금 좁아지고 전달선이 상자 사이 공간으로 분리되었다. 전달 화살표 끝도 mailbox의 `enqueue(job)` 행 높이에 놓여 대상 접점을 더 직접적으로 읽을 수 있다. 초기의 핵심 의미는 유지된다.
- 현재 전달선의 세로 구간은 worker[2] 오른쪽 경계와 떨어져 있어 worker[2]를 경유하는 선처럼 보이지 않는다. source 좌표도 worker[2] 오른쪽 468, 전달선 x=484로 이를 뒷받침한다.
- 모든 worker의 pool 연결은 직선으로 해당 worker 하단과 P.pool 상단을 잇는다. 제안 worker의 연결도 같은 pool로 추적할 수 있다. 범례에서 실선 경계·점선 경계·무방향 선·화살표의 뜻을 분리한다.
- 밝은 배경, 조정 역할 보라, worker 주황, mailbox slate, Catalog 빨강, 중립 pool의 팔레트는 지정 테마와 일치한다. 역할 구분은 색뿐 아니라 이름·포함 경계·연결·문구로도 전달된다.
- source에서 제목 30px/700, 주요 관계선 2.5px, 주요 소유 경계 2px, 추가 경계 3px를 확인했다. viewBox는 1280×1088이고 HTML은 최소 표시 폭 1280px 및 가로 스크롤을 선언한다.
- 최종 PNG 크기는 2560×2176, 현재 및 초기 preview는 각각 1280×1088이다. 의도한 표시 크기 대비 2배 PNG라는 픽셀 규격을 충족한다. 별도의 최종 문서에 삽입된 상태는 이번 확인 범위가 아니다.

## 추가 CDP/브라우저 관측

- 측정 코드는 외부 HTTP(S) 요청을 차단하고 로컬 HTML과 SVG를 각각 연 뒤 `document.fonts.ready`를 기다린다. 각 `svg text`에 CDP `CSS.getPlatformFontsForNode`를 적용한다. 양쪽 결과 모두 실제 사용 폰트 집합에 `DejaVu Sans Mono`와 `Noto Sans KR Thin`이 나오고, 두 항목의 `isCustomFont`가 true다. 폰트 로딩 상태도 두 family 모두 loaded다. 단순 CSS 선언 확인을 넘어 실제 custom font 사용을 확인한 근거다.
- 보고된 glyphCount 합계는 HTML/SVG 각각 976이다. 결과가 node별 관측을 집계하면서 라벨별 대응과 glyph별 정보를 보존하지 않으므로, 이 숫자만으로 모든 설명·코드 구간에 의도한 family가 적용되었는지 단정하지 않는다.
- `Noto Sans KR Thin`은 도구가 보고한 family 이름이다. variable font 메타데이터 이름일 수 있으므로 이 문자열만으로 본문이나 제목이 weight 100으로 그려졌다고 판단하지 않는다. 제목의 computed font size는 30px, computed weight는 700이다. 다만 실제 glyph별 variation axis 적용을 직접 보고한 자료는 아니다.
- HTML/SVG 모두 SVG 표시 영역이 1280×1088이고, 측정한 text bounding box의 SVG 바깥 이탈과 text끼리의 겹침 목록은 비어 있다. 이는 육안 결과를 뒷받침한다. 이 측정은 text와 도형·선 사이 충돌이나 각 컴포넌트 내부 여백을 전수 검사하지 않는다.
- 390px viewport에서 document scrollWidth=390, 컨테이너 clientWidth=390, 컨테이너 scrollWidth=1280, SVG 표시 폭=1280으로 측정됐다. 그림 전체를 축소하지 않고 컨테이너에 가로 스크롤 범위를 두며 문서 자체는 가로로 넘치지 않는다는 구조를 확인했다. 실제 터치/키보드 스크롤 조작이나 모바일에서의 읽기 경험을 관측한 것은 아니다.

## 지적과 미검증 항목

요청된 `ID | 위치 | 분류 | 독자가 읽게 되는 의미 | 근거 | 영향 | 최소 수정` 형식으로 기록할 실제 수정 지적은 없다. 아래는 결함을 추정한 항목이 아니라 확인하지 못한 범위다.

- **폰트 검증의 남은 범위:** Chromium에서 HTML/SVG의 실제 custom font 사용 및 제목 computed weight는 도구 근거가 생겼다. 용도별 모든 라벨의 family 대응, 한글/라틴 glyph별 fallback 여부 및 variation axis 적용은 집계 결과만으로 전수 확정할 수 없다. 테마의 폰트 요건 전체를 검증 완료했다고 주장하지 않는다.
- **다른 렌더 환경:** 현재 preview와 source 및 PNG 크기, Chromium의 HTML/SVG 로딩 및 390px 화면 배치 측정을 확인했다. Chromium 외 SVG 뷰어, 인쇄, 최종 게시 화면, 실제 모바일 조작은 검증하지 않았다.
- **실제 시스템:** S1은 가상 명세다. 이 그림을 실제 운영 구조나 성능의 증거로 확인한 것이 아니다.

현재 증거에서 의미·가독성 수정은 요구하지 않는다. 추가 측정으로 실제 폰트 사용과 좁은 화면 배치에 대한 미검증 범위는 줄었다. 모든 용도·glyph별 폰트 요건과 최종 삽입 환경까지 확인한 것으로 확대 해석하지 않는다.
