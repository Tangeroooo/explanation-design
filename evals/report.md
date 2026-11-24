# 실제 적용·개선·검증 기록

검증일: **2026-11-24 (Asia/Seoul)**. 모든 사례는 repository에 포함된 합성 입력이다. 구조 검사, 근거·의미 평가, 실제 render 검토를 별도로 수행했다. 전체 점수로 한계를 숨기지 않고 관측한 판단과 미검증 범위를 기록한다.

## 환경과 초기 상태

- 현재 작업 폴더는 비어 있었고 이전 폴더에는 `agents/openai.yaml`만 있었다. 완성된 스킬을 전제로 재사용하지 않았다.
- GitHub `Tangeroooo/explanation-design`은 public으로 존재했고 `git ls-remote`에 refs가 없었다. 기존 원격 커밋은 없었으며 이력을 덮어쓰지 않았다.
- 기본 sandbox에서는 Git 초기화와 DNS가 차단됐으나 승인된 실행에서 Git 초기화·GitHub 계정 조회·저장소 조회가 성공했다. 기본 sandbox의 token 오류 메시지를 실제 인증 실패로 단정하지 않았다.
- Python 3.14, Node.js 22.22.1, skills CLI 1.9.0. 선택 개발 도구: PyYAML 6.0.4, Matplotlib 3.11.2, Playwright 1.65.2 / Chromium 1255. 스킬 기본 조립·검증 도구는 Python 3.10+ 표준 라이브러리만 사용한다.

## 1. 구조·도구 검증

| 실행 | 관측 결과 | 보장 범위 |
|---|---|---|
| `python3 scripts/check.py` | package/JSON 구조, shell syntax, **13 unittest** 통과 | 구조와 도구의 검증 대상 동작 |
| skill-creator `quick_validate.py skills/explanation-design` | `Skill is valid!` | 공식 frontmatter·이름·scaffold 검사 |
| 세 `document.json`의 `assemble.py --check` 및 실제 조립 | HTML/Markdown/assets/briefs 생성 | 필수 값·reference 연결·파일·table 구조 |
| 다른 깊이의 output 폴더로 조립 | source href 재계산 확인 | input 기준 상대 링크를 output에 맞게 유지 |
| diagram-design `self_check.py`, `verify_geometry.py` | OK, 0 findings | accessible SVG·단일 파일·geometry 검사 범위 |
| diagram-design `export_svg.py`, `export_png.py … 1` | 실제 SVG, 1280×720 PNG 생성 | 설치본 helper를 실제 사용한 export |
| `npx skills@1.9.0 add <local-repo> --skill explanation-design --agent codex claude-code --yes --copy` | 임시 프로젝트 양쪽 경로 설치 성공 | CLI discovery·파일 설치. host별 자동 선택 품질까지 뜻하지 않음 |

13개 unittest는 누락 근거·잘못된 상태·위험한 URL·깨진 table·asset 탈출·escaping·자산 이름 충돌·source 링크 재계산·가중 비율/0 기준·전달 실패/retry·게시 실패 분류를 검사한다. 게시 테스트는 외부 mutation 없이 fake git/gh로 인증·DNS·소유 목록 실패·잘못된 origin·원격 divergence에서 create/push가 실행되지 않는지 확인한다. 실제 GitHub 게시 결과는 원격 저장소에서 별도로 확인한다.

## 2. 근거·의미 실제 적용

skill-creator의 Independent Forward-Testing에 따라 독립 agent에는 스킬·관련 raw input·실제 요청만 전달했다. 의도한 답안, `cases.json`의 criteria, 기존 `document.json`과 output은 제공하지 않았다. 결과를 받은 뒤 주 agent가 원본·계산·실행 결과와 대조하고 최종 예제를 작성했다. 이 평가는 다른 모델/환경 전체의 성능 보장이 아니다.

| 사례 | 실제 수행과 판단 | 확인한 한계 |
|---|---|---|
| 코드 동작·실패 | send→ack 순서, send 실패 시 ack 미호출, ack 실패 시 send 반환 상태를 구분. 원본 함수에 fake를 연결해 효과 전/후 실패·전체 retry **6개 시나리오** 실행. 효과 후 응답 실패와 중복 기록 반례 확인 | sink 내구성·broker 재배달·caller retry와 실제 발생 빈도는 미확인 |
| 제약 있는 설계 | 세 후보를 동일 축으로 비교. accepted 이후 복구·public field 유지 고정. DB commit 후 응답·unique 결과 저장을 조건부 추천. claim/lease·rolling update·stale worker·dual-write gap과 추천 전환 조건 포함 | 요구사항에서 도출한 제안. 실제 DB primitive·코드·통합·성능은 검증하지 않음 |
| 수치 해석 | 원본 count로 전체 A 1.9%, B 7.2%, 차이 +5.3pp, 상대 +278.95% 계산. light 1→0%, heavy 10→8%, heavy 비중 10→90% 구분. 독립 Decimal 계산과 plotting 입력 대조 | 무작위 배정·독립성·통계 유의성·인과 효과는 확인되지 않음. 0/100을 미래 오류율 0으로 해석하지 않음 |
| 짧은 질문 | 3%→4%를 +1pp, 상대 약 +33.3%로 한 문단 답변. 별도 그림·문서 묶음 제작 안 함 | 평가 결과 보존용 short.md만 저장한 것과 사용자에게 파일 제작하는 결정을 구분 |
| 추가 코드 holdout | send/ack 예시와 다른 cache·permit 코드 적용. 주석과 전역 cache 소유권 차이, try 밖 acquire, 갱신 뒤 실패/취소, release 오류의 원래 예외 가림, 오래된 read의 뒤늦은 overwrite를 설명. **9개 fake 시나리오** 실행 | pool의 취소 안전성·직렬화·fairness, store 일관성과 실제 서비스 장애는 미검증 |

독립 산출물·trace·원본 hash: [independent/](independent/). 최초 임시 평가 후 공개 저장소에서 재현할 수 있도록 링크와 실행 코드 경로만 상대 경로로 변경했고, 두 실행 코드를 다시 실행해 같은 assertion 통과를 확인했다.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 evals/independent/run_observations.py
PYTHONDONTWRITEBYTECODE=1 python3 evals/independent/run_holdout.py
python3 examples/data/analyze.py
python3 examples/data/analyze.py --plot
```

원본 hash는 각 document.json과 독립 observations에 기록했다. hash는 출처 식별이며 내용의 진실성을 증명하지 않는다. 추가 평가 입력인 근거 충돌·자료 속 지시문 처리 사례는 `cases.json`에 마련했으나 **이번 세션에서 독립 행동 실행하지 않았다.** 지침 존재를 실행 성공으로 표시하지 않는다.

## 3. diagram-design 실제 연계

catalog 경로가 실제 설치 위치와 달라 파일 검색으로 활성 설치본을 발견하고 **현재 2.6.174**의 SKILL.md와 type-flowchart, semantic-patterns, style-guide, output-spec, export를 실제로 읽었다. 재사용 스킬에는 이 버전이나 설치 절대 경로를 고정하지 않았다. 사용자는 기본 스타일 사용을 명시적으로 선택했다.

[그림 명세](../examples/code/figures/brief.md)를 먼저 작성하고 flowchart / doc-wide / 6 nodes·5 edges로 제작했다. 현재 호출·예외 순서만 그리고 외부 재배달·내구성을 추가하지 않았다. [HTML](../examples/code/figures/delivery-flow.html)을 설치본 template에서 제작하고 설치본 self-check·geometry·SVG/PNG export helper를 실행한 뒤 [설명 문서](../examples/code/output/index.html)에 조립했다. 이름만 연계한 평가가 아니다.

수치 [차트](../examples/data/output/rates.png)는 별도의 [Matplotlib 코드](../examples/data/analyze.py)로 원본에서 생성했다. diagram renderer·이미지 생성 모델로 수치 그래프를 제작하지 않았다.

## 4. 실제 시각 검토

`review_visuals.py`로 diagram HTML + 세 설명 HTML을 1440×1000, 390×1000 viewport에서 렌더했다. [자동 관측 JSON](visual/observations.json)을 보존했다. 실제로 생성된 diagram 1280×720 PNG, chart PNG, desktop/mobile 설명 screenshot도 열어 확인했다. 인쇄는 CSS media의 overflow를 계산했으며 실제 종이·인쇄 페이지의 시각 검토는 수행하지 않았다.

최종 관측:

- page overflow, 깨진 이미지, 누락 local source link, SVG text viewBox 이탈: **8개 render 모두 0**.
- diagram의 mobile SVG는 폭 1280을 유지하고 local wrapper에서 scroll. 문서 그림도 지정 표시 폭을 유지한다. 전체 페이지가 가로로 밀리지 않는다.
- diagram의 computed family는 제목 Instrument Serif/Noto Serif KR, node Geist/Noto Sans KR이며 webfont 확인이 true. SVG를 offline import하면 폰트 대체 가능성이 있다. PNG에는 export 당시 표시가 보존된다.
- diagram: node label 잘림·겹침 없음, connector는 직선이며 다른 node를 통과하지 않음, 각 label은 해당 선 가까이 위치, edge 수가 적어 겹침·수렴 없음. 여백은 정상 경로와 양쪽 예외 분기를 분리하는 데 사용. 중요한 한국어 label은 12px. 아주 작은 legend는 보조 출처 정보이며 핵심 보장은 본문·caption에도 설명.
- chart: 0 기준 축, 범례·6개 값·하단 조건 주석이 보임. B는 색과 hatch로 구분. error bar는 생성하지 않았다. 문서 표시 폭 920px에서도 축·숫자를 읽을 수 있고 desktop에는 전체가 들어간다.
- 표는 좁은 화면에서 local scroll. 짧은 첫 열이 한 글자씩 세로로 줄바꿈되던 문제는 cell 최소 폭으로 수정했다. 모바일의 큰 표·diagram은 scroll이 필요하며 caption에 안내한다.

스크린샷 생성 자체를 시각 통과로 처리하지 않았다. 그림의 방향·분기·수치가 출처와 같다는 근거·의미 검토도 별도로 수행했다.

## 5. 발견한 문제 → 수정 → 재확인

| 문제 | 일반화한 수정 | 재확인 |
|---|---|---|
| 설계 reference가 필수 조건을 어기는 사용자 지정 후보를 지울 여지 | 부적합 후보를 들러리로 추가하지 않되 사용자 후보는 유지하고 탈락·가능 조건 설명 | 독립 agent가 기존 3후보 유지와 조건부 추천 재평가 |
| 첫 코드 fixture가 reference의 예시와 같은 구조 | cache·resource lifetime·취소·concurrency raw holdout 추가 | 독립 설명과 9개 실제 fake 실행 |
| 중첩 output의 상대 출처 링크가 깨짐 | source href를 input JSON 기준으로 정의하고 output에 맞게 재계산, missing local source 거부 | 서로 다른 깊이 output 테스트와 8개 browser render |
| 모바일에서 이미지가 축소되어 diagram label이 지나치게 작음 | 지정 표시 폭 보존 + local scroll, chart에는 읽을 수 있는 별도 폭 지정 | diagram 1280 / chart 920px 유지, page overflow 0 |
| 표의 짧은 첫 열이 한 글자씩 줄바꿈 | cell 최소 폭, print에서 최소 폭 해제 | desktop screenshot과 mobile/print overflow 재확인 |
| floating-point 표현이 결과 JSON에 7.199999…로 노출, CSV file 미종료 경고 | Decimal 기반 비율 계산 후 JSON 숫자 변환, with 문으로 파일 수명 관리 | 결과 7.2·5.3, 독립 Decimal 대조·테스트·차트 재생성 |
| 게시 성공 fake가 생성 후에도 404를 반환하여 테스트 실패 | 실제 repo 생성처럼 fake 상태를 전환 | 정상·명시 부재 경로 모두 non-force push, 실패 경로는 mutation 없음 |
| export된 SVG의 trailing whitespace가 게시 전 diff 검사를 차단 | SVG의 줄 끝 공백만 정규화하고 plotting 재현 코드에도 반영 | XML/수치 구조 유지 확인, diff 검사 재실행 |

## 남은 검증 범위

- Claude Code/Codex에 설치 파일을 복사하고 도구를 실행했으나 별도의 실제 Claude Code 대화 session에서 자동 선택·장기 사용은 평가하지 않았다.
- 실제 production DB/broker/sink/pool, 배포·성능·내구성·장애 빈도는 검증 대상이 아니다.
- 전체 언어·runtime·plotting 도구·브라우저 조합을 검증하지 않았다. 기본 도구의 Python 최소 버전은 문법·API 기준이며 실제 실행 환경은 3.14였다.
- SVG offline 폰트 대체, 실제 인쇄 페이지 배치, 의미 보존이 필요한 외부 편집 도구 import는 미검증이다.
- future `cases.json`의 근거 충돌·자료 속 지시문 case는 미실행이며 후속 평가 입력으로 남긴다.

## GitHub 게시와 원격 설치 확인

구현 커밋 [ba484cf](https://github.com/Tangeroooo/explanation-design/commit/ba484cf5cc1714536e1c56d33ae35f34ccb99d41)를 `main`에 non-force push했다. API로 public 설정과 default branch를 다시 확인했다. 해당 커밋의 [GitHub Actions check](https://github.com/Tangeroooo/explanation-design/actions/runs/45359260602)는 **success**였다.

게시 후 새 임시 프로젝트에서 `npx skills@1.9.0 add Tangeroooo/explanation-design --skill explanation-design --agent codex claude-code --yes --copy`를 실행했다. 원격 clone·단일 스킬 발견·양쪽 agent 설치 성공. 각 agent에 설치된 **20개 파일**의 SHA-256이 로컬 게시 원본과 모두 일치했다. 두 설치본의 package validator와 설치본 template을 이용한 assembler도 실제 실행해 통과했다. 사용자 global 설치·설정은 변경하지 않았다.

## English defaults and Korean reference editions — 2026-11-24

Default skill instructions, all 13 references, templates, sample JSON, Codex UI metadata, and README are now in English. The original Korean editions are preserved in 19 separate `.ko` files, including [README.ko.md](../README.ko.md) and [SKILL.ko.md](../skills/explanation-design/SKILL.ko.md). Links in the Korean skill resolve to Korean references and templates. Default entry points remain `SKILL.md` and `agents/openai.yaml`; explanations continue to follow the user's requested language. Existing Korean fixtures and evaluation artifacts remain in their original language.

The assembler previously emitted Korean document labels even for English input. Generated labels now follow `language`: English for `en`/`en-*`, Korean for `ko`/`ko-*`, and English fallback for other tags. Authored content is preserved without translation. Both language editions of the assembly contract document this behavior.

Validation performed:

- `python3 scripts/check.py`: **14 unittest cases passed**, including five language-tag cases for generated headings, claim statuses, figure/accessibility labels, fallback, and preservation of authored content.
- Official skill-creator `quick_validate.py`: passed. All 19 English/Korean file pairs exist; English default documentation contains no Korean prose. All local documentation links resolve. The package validator now covers both language editions and sample inputs.
- The three existing Korean examples regenerated **byte-for-byte unchanged**, including HTML and Markdown.
- Actual English and Korean sample HTML renders at desktop 1440px and mobile 390px had no page overflow. English headings were English; Korean headings remained Korean. Generated screenshots were opened and inspected for legibility and clipping. [Browser observations](visual/language-observations.json) are preserved.
- `npx skills@1.9.0` discovered **one skill** with the reference editions included. Local installation for Codex and Claude Code succeeded; all **38 package files per agent** matched source SHA-256 values. Both installed package validators passed. Global user configuration was not changed.

This translation update does not establish new production-system guarantees or cross-agent behavioral evaluation. Earlier independent behavioral evaluations above remain historical results; the new checks cover translated resources, assembly language handling, preservation of Korean outputs, and packaging.
