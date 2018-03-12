SELECT
  TIMESTAMP_TRUNC(published_at, DAY) AS date,
# we do stupid aggregate over all companies per day now
  sum(positionDiff) as totalDiff,
  sector as id 
FROM
  (
  SELECT 
    percent - lag(percent, 1, 0.0) over (partition by service_id, position_holder_name order by published_at asc) as positionDiff,
    published_at,
    service_id
    FROM 
      (
        # only get distinct entries since there might be duplicates in the DB
        SELECT service_id, position_holder_name, published_at, percent
        FROM `insikt-e1887.notifications.short_positions`
        GROUP BY
        published_at,
        service_id,
        position_holder_name,
        percent
      ) 
    ) shorts
    LEFT JOIN `notifications.shares` as shares on shares.service_id = shorts.service_id
WHERE listing_nasdaq = 'nordic-large-cap'
GROUP BY
  date,
  id 
ORDER BY
  date ASC
