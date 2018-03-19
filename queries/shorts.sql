SELECT
  TIMESTAMP_TRUNC(published_at, DAY) AS date,
  sum(positionDiff) as totalDiff,
  'all' as id 
FROM
  (
  SELECT 
    newestPercent - lag(newestPercent, 1, 0.0) over (partition by service_id, position_holder_name order by published_at asc) as positionDiff,
    published_at,
    service_id
    FROM 
      (
        # only get latest percent entry since there might be duplicates in the DB
        SELECT
        service_id,
        position_holder_name,
        published_at,
        first_value(percent) over (partition by service_id, TIMESTAMP_TRUNC(published_at, DAY) order by published_at desc) as newestPercent
        FROM `insikt-e1887.notifications.short_positions`
      ) 
    ) shorts
    LEFT JOIN `notifications.shares` as shares on shares.service_id = shorts.service_id
GROUP BY
  date,
  id 
ORDER BY
  date ASC
