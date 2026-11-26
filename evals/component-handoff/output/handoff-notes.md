# 제작 전 인수인계 점검

기준: `../brief.md`만 시스템 사실로 사용했다. 원본 input.md, 예제/eval, 다른 그림 및 에이전트 대화는 읽지 않았다. S1 표시는 brief가 전달한 근거 번호이며 원본을 독립 검증했다는 뜻이 아니다.

## 렌더 전 판단

- 중요한 의미 모호성: 제작을 막는 모호성은 없다. S와 P/Q의 관점 차이, mailbox 소유권, pool 공유 범위, 접점 귀속, 추가 worker의 범위가 모두 명시되어 있다.
- 남은 시스템 사실: 선택 규칙, mailbox 소비 방법·용량·순서, pool 종류·용량·API, Catalog 배포·내구성은 미상이다. 그림으로 보충하지 않는다. coordinator 송신 API와 Catalog 호출 구현 주체도 정하지 않는다.
- 배치 결정: 상단 논리 서비스 S → Catalog, 하단 P 상세 / Q 요약으로 관점을 분리한다. S→P,Q 배포 대응은 문장으로 명시한다. 실행 순서 화살표를 추가하지 않는다.
- 배치 결정: P worker 네 개를 가로로 놓고 기존 세 개는 실선, 추가 한 개와 그 mailbox만 3px 점선으로 표시한다. 기존 pool은 하나의 중립 자원 바이며 변경 표시를 하지 않는다.
- 배치 결정: mailbox는 worker 내부 구획이다. coordinator의 대표 전달선은 세 번째 mailbox의 경계 포트로 연결하며, 특정 worker 고정이 아니라는 설명을 인접 배치한다. submit(job)은 coordinator의 외부 입력 포트로 별도 표시한다.
- 배치 결정: worker의 아래 책임 구획에서 공용 pool로 각각 무방향 선을 연결한다. mailbox 자체가 pool을 공유하는 것처럼 보이지 않도록 mailbox 구획 아래에 worker 책임 구획을 둔다.
- 결과 크기: fit, 폭 1280 CSS px, 높이 1088 CSS px 예정. 2× PNG는 2560×2176 px, 1× preview는 1280×1088 px. 작은 화면에서는 local horizontal scroll.
- 스타일: 제공된 고정 역할 팔레트, Noto Sans KR 설명체, DejaVu Sans Mono 식별자. 제목 30px/700, 경계 2px, 주요 선 2.5px, 제안 경계 3px. 테마/프로필 질문 없음.
- 도구: 설치된 diagram-design의 assets/template.html을 작업 사본으로 수정하고 scripts/export_svg.py와 export_png.py 사용. 별도 renderer는 만들지 않는다.

## 검증 예정 및 한계

패키지 self_check.py, verify_geometry.py, 1× 실제 PNG 확인, font loading 및 실제 사용 glyph font 확인, PNG 크기 확인을 수행할 예정이다. 독립 시각 검토 및 사람 검토는 이 제작 작업에 포함하지 않는다. 구조적 자동 검사와 의미 적합성/시각 판단은 별도로 보고한다.

## 실제 제작과 작성자 관찰

- 첫 렌더: `preview/component-handoff-initial.png`. 원본 상태를 보존했다. 최종본은 `preview/component-handoff-1x.png`이다.
- 첫 렌더에서 coordinator 전달선의 수직 구간 x=480이 worker[2]의 오른쪽 경계와 겹쳤다. worker 너비를 196→184px로 줄여 36px 간격을 확보하고 경로를 x=484로 옮겼다. mailbox 포트는 `enqueue(job)` 줄 높이 y=700에 맞췄다. 부모 작성자도 같은 문제를 관찰했다. 독립 평가 성과로 계산하지 않는다.
- 첫 렌더에서 공유선 옆 설명문이 첫 수직 공유선 위를 지났다. 이 문장은 아래 범례와 중복이어서 삭제했다.
- 최종 1× 렌더를 직접 열어 확인했다. 제목, worker 이름, mailbox 구획, 접점, pool을 읽을 수 있다. 글자 잘림과 겹침은 관찰되지 않았다. 전달선이 worker[2] 경계에서 분리됐고 arrow 끝은 worker[3]의 mailbox 포트에 닿는다. 각 공유선은 서로 분리되어 worker 하단에서 P.pool 윗면까지 이어진다. 중간 다른 노드를 통과하지 않는다. P의 worker 간격은 일정하며 Q는 비교 범위를 수량으로 요약했다. 상단과 하단의 여백은 논리/프로세스 관점 구분에 쓰인다. 1280 CSS px 폭에서 과도한 축소는 없다.
- 서브셋 폰트를 HTML과 SVG에 data URL로 포함했다. 전체 폰트 포함 초기 HTML 약 14MB를 최종 약 57KB로 줄였다. CSS 가족 이름은 Noto Sans KR이며 variable font의 내부 family 이름은 `Noto Sans KR Thin`으로 CDP에 나온다. 제목은 실제 computed 30px/700이다. 코드 식별자는 DejaVu Sans Mono이다.
- fontTools는 기본 Python과 `/home/juhyeon/.venv/bin/python`에 없었다. 이미 설치된 `/tmp/pr515-fonttools`를 `PYTHONPATH`로 사용했다. 설치 작업은 하지 않았다. 라이선스는 `font-licenses/`에 보존했다.
- 기존 `export_svg.py`가 embedded font가 있어도 기본 Google Fonts `@import`를 넣었다. export 후 그 불필요한 import 1개만 제거했다. 원본 helper나 전역 설정은 바꾸지 않았다. 최종 HTML과 SVG에는 외부 font 요청이 없다.

## 실제 실행한 검사

- `verify_geometry.py`: `Summary: 1 file(s) checked, 0 finding(s).`
- `self_check.py`: FAIL, `non-fragment CSS url() is not allowed` 두 건. 이는 self-contained를 위한 embedded font data URL 두 개이다. 이 validator의 전체 통과를 주장하지 않는다. 검사기를 바꾸거나 URL을 숨기지 않았다.
- `verify-render.py`: Chromium에서 HTML과 standalone SVG를 각각 열고 외부 HTTP 요청을 차단한 상태로 검사했다. CDP가 실제 glyph에 사용한 font는 Noto Sans KR variable과 DejaVu Sans Mono 두 custom font다. 두 파일 모두 font loaded, SVG text의 viewBox 밖 이탈 0, text끼리 bbox 겹침 0이다. 상세 원본은 `render-checks.json`.
- HTML/SVG 실제 표시 크기 1280×1088 CSS px. PNG 2×는 2560×2176 px, 1× preview는 1280×1088 px이다. 해상도 2×를 표시 크기와 혼동하지 않는다.
- 390px viewport: document 폭 390px, local wrapper 폭 390px, 내부 scrollWidth/SVG 폭 1280px. 페이지 전체가 옆으로 늘어나지 않고 다이어그램만 local scroll한다.
- 접근성: SVG role=img, 첫 자식 title, 고유 prefix title/desc ID와 aria-labelledby를 포함한다. 구조 검사의 data URL 정책 실패와 별개로 이를 실제 소스에서 확인했다.

## 재현 명령과 환경

`DIAGRAM_SKILL`은 설치된 diagram-design 경로로 지정한다. 아래 명령은 이 output 디렉터리에서 실행한다. Playwright·Pillow와 호환 Chromium이 필요하며 브라우저·라이브러리 환경 변수는 각 환경에 맞춘다.

```bash
python3 "$DIAGRAM_SKILL/scripts/export_svg.py" component-handoff.html component-handoff.svg
python3 - <<'PY_SVG'
from pathlib import Path
import re
p = Path("component-handoff.svg")
s, count = re.subn(r"@import\s+url\([^)]*\);\s*", "", p.read_text())
assert count == 1 and s.count("@font-face") == 2
p.write_text(s)
PY_SVG
python3 "$DIAGRAM_SKILL/scripts/verify_geometry.py" component-handoff.html
python3 "$DIAGRAM_SKILL/scripts/self_check.py" component-handoff.html
python3 "$DIAGRAM_SKILL/scripts/export_png.py" component-handoff.html preview/component-handoff-1x.png 1
python3 "$DIAGRAM_SKILL/scripts/export_png.py" component-handoff.html component-handoff.png 2
python3 verify-render.py
```

SVG export 뒤 기본 Google Fonts import만 제거하는 과정을 명시적으로 재현한다. `--system-fonts`는 이 원본에서는 필요한 font-face도 제거하므로 사용하지 않는다. 위 export와 후처리로 검토된 SVG와 바이트가 동일함을 저장소 복사 후 확인했다. self_check의 예상 실패는 위에 설명한 두 data URL이며 다른 검사의 성공과 구분한다.

이 환경에서는 `PLAYWRIGHT_BROWSERS_PATH=/tmp/component-brief-trial/output/browser-runtime`, `LD_LIBRARY_PATH=/tmp/pr926-render/libs/usr/lib/x86_64-linux-gnu`를 사용했다. 기본 안내 경로 `/tmp/sddb-096-browsers`는 없었다. 임시 browser-runtime의 `chromium_headless_shell-1248/chrome-headless-shell-linux64` symlink는 기존 `/tmp/pr926-render/chrome-headless-shell-linux64`를 가리킨다. 이 symlink는 배포용 산출물이 아니다. Chromium 실행은 sandbox 제약 때문에 exec_command의 require_escalated 승인을 사용했다. 전역 설정은 수정하지 않았다.

## 미실행과 한계

- 원본 input.md를 재분석하지 않았다. brief 내 S1 항목과 일치 여부만 판단했다.
- 이 작성자는 독립 시각 검토 또는 사람 검토를 수행하지 않았다. 부모가 별도로 진행한다.
- Illustrator/Figma/다른 SVG 뷰어, 실제 문서 플랫폼 embed는 시험하지 않았다. SVG의 embedded font 지원이 없는 도구에서는 PNG를 사용한다.
- bbox 검사는 텍스트끼리 겹침과 viewBox 이탈을 다루며 모든 의미 오류를 검출하지 않는다. 포트 귀속과 경계 의미는 실제 렌더와 brief로 따로 확인했다.

저장소 보존 시 HTML과 라이선스의 줄 끝 공백만 정리했다. 라이선스 문구는 유지했으며 HTML에서 다시 export한 SVG가 검토본과 바이트 단위로 같음을 확인했다.
