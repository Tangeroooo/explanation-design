# F2 — 전체와 집단별 오류율

- 질문: B의 오류율은 개선됐는가?
- 메시지: 집단별 오류율은 낮지만 heavy 요청 비중이 커져 전체 오류율은 높다.
- 독자/선행: 비율을 읽는 엔지니어·의사결정자. 단위는 요청 오류율 %.
- 출처/주장: input/cohorts.csv, input/context.md, analyze.py, output/results.json. document.json의 S1–S3 / C1–C4.
- 유형/이유: grouped bar chart, 전체와 각 집단의 A/B를 같은 축으로 비교. 데이터가 적어 표도 함께 제공.
- 요소/관계: Overall/Light/Heavy 각각 A/B 값. 시간·인과·실행 순서 edge 없음.
- 상태 표현: 합성 관측값만 plotting. 원인·통계 유의성·제안은 chart에 넣지 않음.
- 데이터/단위: 1000 요청씩. 전체 A 19/1000=1.9%, B 72/1000=7.2%; light 1%→0%, heavy 10%→8%.
- 정확한 라벨: Request error rate (%), Overall, Light, Heavy, A, B. 원본 count는 표에 보존.
- 캡션: 전체 +5.3 percentage points. 집단 비중이 달라 causal 개선을 판정할 수 없다.
- 생략: error bar·시간 변화·유의성. 표본의 사용자 독립성과 무작위 배정이 없어 임의 불확실성 구간을 만들지 않음.
- 크기: 9.6×5.4 inch, PNG 150dpi. style은 zero-baseline Matplotlib, 색+해칭+직접 값·범례.
- 형식: SVG, PNG, 원본 CSV, 재현 plotting 코드, results.json.
- 의미 수용: 가중 전체율, pp/상대 변화 구분, 각 bar 원본과 일치, 0에서 시작하는 축.
- 시각 수용: label·주석 잘림 없음, 흑백에서도 A/B 해칭 식별, 문서에서 확대·읽기 가능.
- 재현: python examples/data/analyze.py --plot (Matplotlib 필요).
- 실제 결과/검증/수정: evals/report.md.
