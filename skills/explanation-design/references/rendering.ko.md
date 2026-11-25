# 제작 연계와 문서 조립

## diagram-design 호출 경계

1. 현재 session의 skill catalog에서 `diagram-design` 위치를 찾는다. 경로가 사라졌으면 알려진 skill/plugin roots에서 `rg --files --hidden … -g SKILL.md`로 발견한다. 버전·홈 디렉터리를 스킬에 고정하지 않는다. 여러 설치가 있으면 활성 catalog와 일치하는 것을 우선하고 모호함을 기록한다.
2. 실제 `SKILL.md`, 선택한 type reference, 필요한 style·export·검증 지침을 읽는다. 제작자의 기본 스타일과 온보딩 대신 선택된 [다이어그램 테마](diagram-theme.ko.md)와 확인 대기 생략 지침을 적용한다. 사용자가 명시한 변경·크기·출력 결정을 전달한다. 제작 도구의 지침을 기억으로 대체하지 않는다.
3. [그림 명세](../assets/figure-brief.ko.md)를 전달한다. 질문·메시지·대상·출처·claim·node/edge·상태·정확한 라벨·생략·size·고정 팔레트와 Noto Sans KR 요건·format·수용 기준을 포함한다. 사실/추론/제안/미확인의 시각 표현은 명세에서 합의한다.
4. 해당 환경에서 skill을 적용해 제작하고 제작본과 검증 결과를 회수한다. skill은 agent 지침일 수 있으며 별도 rendering API가 있다고 가정하지 않는다. 실제 제작·검증·export가 없으면 “연계 완료”라고 쓰지 않는다.
5. 결과를 의미적으로 대조한다. 특히 화살표 방향·guard·수치·순서·실패 후 상태를 확인한다. 누락이 해석을 바꾸면 그림 또는 명세를 수정하고 다시 검증한다.
6. SVG/PNG가 요청되면 설치된 skill의 export helper를 사용하고 테마 reference에 따라 실제 출력의 폰트와 팔레트를 검증한다. 파일 이름·출력 형식·미검증 범위를 보고한다.

diagram-design이 없거나 도구가 작동하지 않으면 가능한 설명·표·명세를 완료한다. 요청한 그림의 미제작 상태를 표시하고 필요한 설치·실행을 안내한다. 제작기를 복제하거나 성공으로 가장하지 않는다. 정확한 수치 차트는 [data](data.ko.md)의 plotting 경로를 쓴다.

## 선택형 산출물

짧은 답변에는 파일 불필요. 공유 문서가 필요하면 Markdown/HTML과 요청된 assets, 재확인할 source·figure brief를 함께 둔다. diagram-design의 self-contained diagram HTML과 이 스킬의 **자산 폴더를 동반한 설명 HTML**은 다른 산출물이다.

## `assemble.py` 입력 계약

[document.json](../assets/document.ko.json)은 실행 가능한 최소 예시다. JSON은 agent가 근거를 분석한 뒤 작성한다. 내용은 plain text이며 HTML/Markdown 구문을 평가하지 않는다.

- top-level: `title`, `language`, `summary`, `sources`, `claims`, `sections`.
- source: 고유 `id`, `label`, 재확인 위치 `location`, 버전/내용 식별 `version`, optional `href`.
- claim: 고유 `id`, `text`, `kind` (`fact`, `inference`, `proposal`, `unknown`), `source_ids`, `basis`. fact/inference는 source 필수; proposal/unknown은 빈 배열 가능. basis에는 적용 조건·추론·미확인 사유를 쓴다.
- section: 고유 `id`, `heading`, `blocks`.
- block: `type` = `paragraph` (`text`), `list` (`items`), `code` (`text`, `language`), `table` (`headers`, `rows`), `figure` (`path`, `alt`, `caption`, `brief`). optional `claim_ids`로 인접 주장 연결.
- figure: 실제 local SVG/PNG만 허용. path·brief는 JSON 폴더 안의 상대 경로. 명세는 Markdown 파일. 의미 있는 `alt`, `caption` 필수. optional `display_width`는 검토한 CSS pixel 폭(64~16384)이다. 기본은 이미지 고유 폭이다. 예: 글자 12px인 diagram은 원래 폭 유지, 큰 PNG chart는 축·라벨이 읽히는 폭을 지정. SVG의 표시 폭도 명시할 수 있다. 조립기는 의미나 적절한 글자 크기를 판단하지 않는다.
- source `href`는 HTTP(S) 또는 **입력 JSON 기준** 상대 파일 링크. 로컬 출처 링크는 존재를 확인하고 output 위치에 맞춰 재계산한다. source 링크는 상위 폴더의 근거 파일을 가리킬 수 있지만 자산 복사는 입력 폴더 안으로 제한한다. 위험한 URL scheme·missing asset·중복 ID·미해결 claim/source·불완전 table은 실패 처리.
- 입력 `language`가 `en`/`en-*`이면 조립기의 제목·라벨은 영어, `ko`/`ko-*`이면 한국어이며 그 외에는 영어를 사용한다. 작성한 block은 번역하지 않는다. 기본 템플릿은 영어, 한국어 참고 템플릿은 별도의 `.ko` 파일에 있다. 독자가 요청한 언어에 맞춰 작성한다.

```bash
python3 <skill-dir>/scripts/assemble.py document.json --out dist
python3 <skill-dir>/scripts/assemble.py document.json --check
```

결과: `dist/index.html`, `dist/explanation.md`, `dist/assets/…`, `dist/briefs/…`. 원본 JSON은 그대로 보존한다. HTML은 script 없이 CSP와 escaping을 적용한다. 같은 입력을 같은 output 폴더에 다시 조립할 수 있지만 index.html/explanation.md는 교체되므로 전용 생성 폴더를 쓴다. 자산은 내용 hash로 이름 붙여 충돌을 피한다. HTML의 그림은 원래 크기를 유지하고 해당 영역 안에서 가로로 스크롤한다. print에서는 페이지 폭에 맞춘다. 로컬 출처 파일을 동반하지 않고 공유하면 source 링크는 접근할 수 없으므로 공유 범위를 확인한다.
