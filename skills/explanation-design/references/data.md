# Calculate and interpret numerical evidence

Keep original data and reproducible code together. Establish the data dictionary first: row meaning, units, sample size, period, filters, missing values, aggregation, and comparison conditions. Label synthetic data explicitly.

## Calculation rules

```text
absolute_change = new - old
relative_change_pct = (new - old) / old * 100  # undefined when old == 0
ratio = new / old                            # state the reference direction
rate = numerator / denominator              # missing when denominator == 0
percentage_point_change = (new_rate - old_rate) * 100
```

- A change from 2% to 3% is +1 percentage point, +50% relative, and 1.5 times the original. Keep these quantities distinct.
- For an overall rate, sum numerators and denominators rather than averaging group rates. Changes in group composition can reverse the overall direction relative to within-group changes.
- Means and p95 describe different quantities. Do not reconstruct an overall statistic by naively averaging group means or p95s. State the quantile method used.
- Do not silently remove missing, zero, or duplicate rows or fill them with zero. State handling rules and their impact.
- An observed difference does not prove its cause. Limit causal wording without randomization, confounder control, and suitable samples. Expose small samples and uncertainty.

## Exact charts

Calculate from original data with standard plotting tools such as Matplotlib. Preserve generation code, environment, axes, units, scale, filters, and uncertainty. Do not alter data points, bar lengths, or axis ranges to fit a visual style. Bars normally start at zero; visibly explain any different baseline.

Use a table alone when it is shorter and more precise. Comparing two means does not explain their distributions. Do not invent error bars when uncertainty was not calculated. Do not use image-generation models to produce exact charts.

Verify by independently recalculating a small input and comparing plotted data with table values and prose. Record the source hash and calculation command. Correct numbers and code do not by themselves establish a causal interpretation.
