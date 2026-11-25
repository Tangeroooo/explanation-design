# 재생성과 검증

최종 자산은 structure.html/svg/png, keys.html/svg/png. 문서는 document/index.html, document/explanation.md. 편집 원본은 make_sources.py와 document.json, 명세는 brief.md다. 모든 전달 파일은 이 디렉터리에 있다.

설치된 diagram-design 2.6의 template.html을 복사해 사용했다. 재생성은 이 폴더에서 다음 순서다. `DIAGRAM_SKILL`과 `EXPLANATION_SKILL`은 해당 스킬의 실제 경로로 지정한다.

```sh
python3 make_sources.py
python3 "$DIAGRAM_SKILL/scripts/export_svg.py" structure.html structure.svg --system-fonts
python3 "$DIAGRAM_SKILL/scripts/export_svg.py" keys.html keys.svg --system-fonts
python3 "$DIAGRAM_SKILL/scripts/export_png.py" structure.html structure.png 2
python3 "$DIAGRAM_SKILL/scripts/export_png.py" keys.html keys.png 2
python3 "$EXPLANATION_SKILL/scripts/assemble.py" document.json --out document
python3 finalize_document.py
python3 inspect_render.py
python3 "$DIAGRAM_SKILL/scripts/verify_geometry.py" structure.html keys.html
python3 "$DIAGRAM_SKILL/scripts/self_check.py" structure.html keys.html
python3 "$EXPLANATION_SKILL/scripts/assemble.py" document.json --check
```

`self_check`는 폰트 data URL 두 건을 금지하므로 두 파일에 실패한다. 이 제한을 바꾸지 않았다. 기하 검사와 문서 구조 검사는 통과했다. font-face는 SVG 내부 defs에 두었으므로 `--system-fonts`로 외부 Google Fonts import만 제거해도 원본의 내장 폰트가 유지된다. 외부 요청을 차단하고 standalone SVG 폰트 렌더링을 관측했다.

Playwright와 호환 Chromium이 필요하다. 설치 경로나 추가 라이브러리가 필요한 환경에서는 해당 환경의 `PLAYWRIGHT_BROWSERS_PATH`와 라이브러리 설정을 사용한다. 생성기·자산에는 특정 사용자의 홈 경로를 고정하지 않았다. `inspect_render.py`는 Playwright·Pillow, 폰트 재부분집합 생성에는 fontTools가 필요하다. 저장소의 선택 개발 의존성 설치로 제공되는 도구를 사용한다.

Noto Sans KR 폰트는 variable `wght` 100–900, default100이며 face 선언도 100 900이다. CDP는 기본 face의 metadata 이름 `Noto Sans KR Thin`을 보고한다. 실제 custom font 로딩과 제목 CSS 30px/700을 확인했으며, 그림에서도 굵은 제목을 확인했다. 모든 glyph의 내부 축 적용까지 독립적으로 검증하지는 않았다. 코드 글자는 DejaVu Sans Mono 실제 사용을 확인했다.

폰트는 subset되어 fonts/에 있으며 OFL과 DejaVu 라이선스를 동봉했다. 수정 시 기존 subset에 없는 새 글자는 원본 폰트에서 다시 subset해야 한다. subset_fonts.py는 그림 원본용이며 문서용 폰트는 document/index.html의 모든 글자를 대상으로 만들었다. 원본 폰트 전체를 전달물에 넣지 않았다.

make_sources.py 재실행 전후 HTML SHA-256이 동일함을 확인했다. 반영 전 일본어 표기 후처리도 제거했고 한국어/영문을 원본에 직접 적었다.

관측은 render-observations.json, 전체 체크 요약·해시는 verification.json, 최초 독립 해석은 review-phase1.md, 결과는 review.md다. PNG 1× 최초본은 preview/, 최종 2× PNG는 루트에 있다. 최초본은 F01 수정 전이며 최종 산출물이 아니다.
