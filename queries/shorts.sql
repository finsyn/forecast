SELECT
  TIMESTAMP_TRUNC(published_at, DAY) AS date,
  SUM(percent.float) AS sum
FROM
  `insikt-e1887.forecast.short_positions`
GROUP BY
  date
ORDER BY
  date ASC
