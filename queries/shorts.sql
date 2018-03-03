SELECT
  TIMESTAMP_TRUNC(published_at, DAY) AS date,
  count(percent.float) AS sum
FROM
  `insikt-e1887.forecast.short_positions`
WHERE comment = 'Fallit under 0,5%'
GROUP BY
  date
ORDER BY
  date ASC
