SELECT
  TIMESTAMP_TRUNC(date, DAY) AS date,
  quotes.service_id as id,
  quotes.newestClose as close,
  quotes.newestOpen as open,
  quotes.newestHigh as high,
  quotes.newestLow as low,
  quotes.newestVolume as volume
FROM
(
  SELECT
    # we might have duplicates, then we want the latest added value
    first_value(open) over (partition by service_id, TIMESTAMP_TRUNC(date, DAY) order by created_at desc) as newestOpen,
    first_value(close) over (partition by service_id, TIMESTAMP_TRUNC(date, DAY) order by created_at desc) as newestClose,
    first_value(volume) over (partition by service_id, TIMESTAMP_TRUNC(date, DAY) order by created_at desc) as newestVolume,
    first_value(high) over (partition by service_id, TIMESTAMP_TRUNC(date, DAY) order by created_at desc) as newestHigh,
    first_value(low) over (partition by service_id, TIMESTAMP_TRUNC(date, DAY) order by created_at desc) as newestLow,
    *
    FROM `notifications.quotes_training`
) quotes
LEFT JOIN `notifications.shares` as shares on shares.service_id = quotes.service_id
WHERE
  close > 0.0
AND
(
  quotes.service_id LIKE 'market-index_%'
)
GROUP BY
  date,
  id,
  open,
  close,
  low,
  high,
  volume
ORDER BY
  date asc,
  id 
