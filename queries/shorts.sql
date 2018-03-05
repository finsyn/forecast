SELECT
  TIMESTAMP_TRUNC(published_at, DAY) AS date,
# we do stupid aggregate over all companies per day now
#  isin,
  sum(positionDiff) as totalDiff
FROM
  (
  SELECT 
    percent.float - lag(percent.float, 1, 0.0) over (partition by isin, position_holder_name order by published_at asc) as positionDiff,
    *
    FROM `insikt-e1887.forecast.short_positions`
    )
GROUP BY
#  isin,
  published_at
ORDER BY
  date ASC
