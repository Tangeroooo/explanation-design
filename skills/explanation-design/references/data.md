# 수치 계산과 해석

원본과 재현 코드를 함께 보존한다. 먼저 데이터 사전 확인: 한 row의 의미, 단위, 표본 수, 기간, 필터, 결측, 집계, 비교 조건. 합성 데이터면 그렇게 표시한다.

## 계산 기준

```text
absolute_change = new - old
relative_change_pct = (new - old) / old * 100  # old == 0이면 정의 불가
ratio = new / old                            # 기준 방향 명시
rate = numerator / denominator              # denominator == 0이면 결측
percentage_point_change = (new_rate - old_rate) * 100
```

- 2% → 3%는 +1 percentage point, 상대 +50%, 1.5배다. 서로 바꾸지 않는다.
- 여러 집단의 비율은 단순 평균하지 말고 numerator·denominator를 합산한다. 집단 비중이 바뀌면 전체와 집단별 방향이 다를 수 있다.
- 평균과 p95는 다른 양이다. 평균들의 평균·p95들의 평균으로 전체 통계를 복원하지 않는다. 분위수 계산법을 밝힌다.
- 결측·0·중복 row를 조용히 제거하거나 0으로 채우지 않는다. 처리 규칙과 영향 표시.
- 관측 차이는 원인 증명이 아니다. 무작위 배정·교란 통제·표본 조건이 없으면 causal wording을 제한한다. 표본이 작으면 그 사실과 불확실성을 보인다.

## 정확한 차트

정확한 수치는 Matplotlib 등 표준 plotting 도구로 원본에서 계산한다. 생성 코드·환경·축·단위·scale·필터·uncertainty를 남긴다. 그림 스타일에 맞추려고 data point·막대 길이·축 범위를 바꾸지 않는다. 기본 bar는 0 기준; 다른 축이면 이유와 범위를 눈에 보이게 표시한다.

표가 더 정확하고 짧으면 표만 쓴다. 평균 두 개를 비교하면서 분포 차이를 설명했다고 하지 않는다. uncertainty를 계산하지 않았으면 error bar를 꾸미지 않는다. 이미지 생성 모델은 정확한 차트 제작에 사용하지 않는다.

검증: 작은 입력으로 계산을 독립 재산출하고, chart data와 표 값·본문을 대조한다. 원본 hash와 계산 명령을 기록한다. 숫자·코드가 맞아도 인과 해석은 별도 검토다.
