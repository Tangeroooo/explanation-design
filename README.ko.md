# explanation-design

[English](README.md) | 한국어

기본 문서와 스킬 지침은 영어입니다. 한국어 참고본은 `.ko` 파일로 보존합니다.

한국어 스킬은 [SKILL.ko.md](skills/explanation-design/SKILL.ko.md), reference와 템플릿은 각 `.ko` 파일에 있습니다. 기본 진입점은 `SKILL.md`와 `agents/openai.yaml`입니다. 스킬 지침의 언어와 사용자에게 전달하는 설명의 언어는 별개이며, 설명은 계속 사용자가 요청한 언어를 따릅니다.

코드·문서·설계·데이터를 근거로, 독자가 동작과 조건을 이해하고 선택할 수 있는 설명을 만드는 agent skill입니다. Claude Code와 Codex에서 사용합니다.

핵심은 독자의 질문 → 근거와 주장 → 인과·실행 흐름 → 적절한 표현 → 의미·시각 검증입니다. 짧은 질문은 채팅에서 답하고, 필요할 때 Markdown·HTML·출처·그림 제작 명세를 만듭니다. 특정 언어·DB·제품을 전제하지 않습니다.

## 설치

### npx skills

2026-11-24에 `skills` CLI **1.9.0**의 실제 help와 Codex/Claude Code 설치를 검증했습니다. [공식 CLI](https://github.com/vercel-labs/skills)에서 현재 요구하는 Node.js 버전과 지원 옵션을 확인할 수 있습니다. 검증 환경은 Node.js 22.22.1입니다.

프로젝트 폴더에서 두 agent에 설치:

```bash
npx skills add Tangeroooo/explanation-design --skill explanation-design --agent codex claude-code
```

모든 프로젝트에서 사용하려면 `--global`을 추가합니다. 재현 가능한 CLI 버전을 원하면 `npx skills@1.9.0 …`을 사용합니다. 설치 명령이 기존 설치를 갱신할 수 있으므로 수정한 로컬 스킬은 먼저 보존하세요.

```bash
# 로컬 checkout에서 설치
npx skills add ./explanation-design --skill explanation-design --agent codex claude-code

# 설치 확인 / 업데이트
npx skills list --agent codex claude-code
npx skills update explanation-design
```

검증한 CLI의 project 설치 위치는 Codex `.agents/skills/`, Claude Code `.claude/skills/`입니다. global 설치 위치는 [공식 agent 목록](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)을 확인하세요. agent가 새 설치를 인식하지 않으면 새 session에서 확인합니다.

### CLI 없이 복사

저장소를 clone한 후 **대상 프로젝트 폴더에서** 실행합니다. 아래 `/path/to/explanation-design`은 실제 clone 경로로 바꿉니다. 기존 폴더가 있으면 명령이 멈추므로 먼저 변경 내용을 비교하세요.

```bash
mkdir -p .agents/skills .claude/skills
test ! -e .agents/skills/explanation-design && cp -R /path/to/explanation-design/skills/explanation-design .agents/skills/
test ! -e .claude/skills/explanation-design && cp -R /path/to/explanation-design/skills/explanation-design .claude/skills/
```

## 사용

Codex에서는 `$explanation-design`, Claude Code에서는 `/explanation-design`과 요청을 함께 사용하거나 자연어로 설명 작업을 요청합니다.

```text
$explanation-design 이 함수가 실패하거나 취소된 뒤 어떤 상태가 남는지
실제 코드를 읽고 설명해줘. 추론과 미확인을 구분해줘.

$explanation-design 이 제약에서 현실적인 대안을 비교하고 추천해줘.
유지할 계약, data/control flow, 변경 지점, 선택이 바뀌는 조건을 알려줘.

$explanation-design 이 데이터의 전체·집단별 차이를 계산해줘.
단위와 표본을 확인하고, 차트가 도움이 되면 원본과 재현 코드를 남겨줘.
```

기본 응답은 사용자 언어입니다. 고정된 섹션 수·그림 수·파일 묶음을 강제하지 않습니다.

## diagram-design과의 역할

explanation-design은 근거 조사·주장·설명 순서·표현 선택·그림 명세·의미 검증·문서 조립을 담당합니다. 실제 다이어그램의 레이아웃·style·시각 검증·SVG/PNG export는 **별도 설치된 diagram-design** 지침을 읽고 수행합니다. 경로·버전을 하드코딩하거나 renderer를 복제하지 않습니다.

diagram-design이 없으면 설명·표·제작 명세까지 완료하고 미제작 범위를 표시합니다. 그림이 없는 짧은 설명에는 필요하지 않습니다. 정확한 수치 차트는 Matplotlib 등 표준 plotting 도구와 원본 데이터로 만들며 이미지 생성 모델을 사용하지 않습니다.

실제 연계 예제: [제작 명세](examples/code/figures/brief.md) → [diagram HTML](examples/code/figures/delivery-flow.html) → [SVG](examples/code/figures/delivery-flow.svg) / [PNG](examples/code/figures/delivery-flow.png) → [조립한 설명 HTML](examples/code/output/index.html).

## 실제 적용 예제

모두 설명용 합성 fixture입니다. 실제 production 시스템을 검증한 결과가 아닙니다.

| 사례 | 질문·핵심 판단 | 산출물 |
|---|---|---|
| 코드 | send 실패와 ack 실패 뒤 상태, 외부 효과와 호출 성공의 차이 | [Markdown](examples/code/output/explanation.md), [HTML](examples/code/output/index.html), [입력](examples/code/input/worker.py) |
| 설계 | accepted 이후 복구 조건에서 local queue·DB job table·broker 비교 | [Markdown](examples/design/output/explanation.md), [HTML](examples/design/output/index.html), [요구사항](examples/design/input/requirements.md) |
| 데이터 | 집단별 오류율 감소와 전체 오류율 증가, workload 비중의 영향 | [Markdown](examples/data/output/document/explanation.md), [HTML](examples/data/output/document/index.html), [원본](examples/data/input/cohorts.csv), [plotting 코드](examples/data/analyze.py) |
| 추가 코드 평가 | cache 갱신 후 취소·cleanup 실패·동시 요청의 오래된 값 덮어쓰기 | [입력](evals/holdout/input/cache.py), [독립 설명](evals/independent/holdout.md) |

[평가 보고서](evals/report.md)에 구조 / 근거·의미 / 시각 검증, 발견한 문제와 수정·재확인, 미검증 범위를 구분했습니다. [평가 입력](evals/cases.json)과 [평가 기준](evals/rubric.md)도 포함합니다.

[표현 선택 검토](evals/representation-review.md)는 범위·자원 한도·실패·소유권에 관한 합성 사례에 그림 선택 규칙을 적용합니다. 명세 수준의 의미 검토와 산출물 최신성 판단을 기록했으며, 독립 평가나 렌더링된 그림의 품질 검증을 뜻하지 않습니다.

## 문서 조립과 검증

기본 도구는 **Python 3.10+ 표준 라이브러리**만 필요합니다. 조립기는 사람이/agent가 작성한 plain-text block과 assets를 묶으며 근거·설명 품질을 판단하지 않습니다.

```bash
python3 skills/explanation-design/scripts/assemble.py examples/code/document.json --out build/code
python3 skills/explanation-design/scripts/assemble.py examples/design/document.json --out build/design
python3 skills/explanation-design/scripts/assemble.py examples/data/document.json --out build/data
python3 scripts/check.py
```

HTML은 `index.html`과 동반 `assets/`, `briefs/` 폴더를 함께 공유합니다. [입력 예시](skills/explanation-design/assets/document.ko.json)와 [계약](skills/explanation-design/references/rendering.ko.md)을 참고하세요. diagram-design의 개별 self-contained HTML과 설명 HTML의 packaging은 다릅니다.

기본 JSON 예시는 영어이고 한국어 예시는 `document.ko.json`에 보존합니다. 입력 `language`가 `en`/`en-*`이면 조립기의 제목·라벨은 영어, `ko`/`ko-*`이면 한국어이며 그 외에는 영어를 사용합니다. 작성한 본문은 번역하지 않고 그대로 유지합니다.

차트 재생성·공식 skill validator·browser 검토가 필요할 때만 개발 의존성을 설치합니다.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python examples/data/analyze.py --plot
.venv/bin/python -m playwright install chromium
.venv/bin/python scripts/review_visuals.py --out build/visual-review
```

browser 검사는 페이지 overflow·깨진 이미지·링크·SVG text bounds 등을 확인하고 screenshot을 남깁니다. screenshot을 사람이/agent가 실제로 열어보는 검토는 별도로 수행해야 합니다. `scripts/check.py`와 CI는 의미·시각 품질 통과를 대신하지 않습니다.

## 구조와 변경

```text
skills/explanation-design/
  SKILL.md                 # 공유 흐름·분기
  references/              # 질문 유형별 선택 읽기
  assets/                  # 설명·그림 명세·JSON 예시
  scripts/                 # 구조 검증·기계적 문서 조립
  agents/openai.yaml       # Codex UI metadata
examples/                  # raw 근거·설명·실제 그림·재현 계산
evals/                     # 평가 입력·독립 실행·검증 보고
tests/                     # 조립·계산·실패 경로·게시 보호 테스트
```

지침 변경 시 해당 요청을 실제로 다시 풀고 품질을 확인하며 영어판과 한국어 참고본도 함께 갱신합니다. source 변경 시 document.json의 버전/hash·주장을 재검토하고 조립본도 갱신합니다. 문법·파일 존재만으로 완료하지 않습니다.

## GitHub 게시

대상은 public 저장소 `Tangeroooo/explanation-design`입니다.

```bash
gh auth status
bash scripts/publish-github.sh
```

스크립트는 계정·origin·branch·기존 이력·검증 결과를 확인하고 commit/push합니다. 인증·연결 실패를 저장소 부재로 처리하지 않습니다. 명시적 404와 소유 저장소 조회 성공을 확인했을 때만 생성하며, 기존 저장소는 public 설정을 확인합니다. force-push·reset·자동 merge는 하지 않습니다. 원격이 앞서거나 분기되었으면 변경을 보존한 채 중단하므로 직접 fetch·통합 후 다시 실행하세요. 기존 staged 변경도 검토를 위해 중단합니다.
