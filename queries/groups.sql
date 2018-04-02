SELECT
  TIMESTAMP_TRUNC(date, DAY) AS date,
  /* 'all' as id, */
  shares.listing_nasdaq as id,
  /* sum(cast(quotes.newestClose > quotes.newestOpen as INT64)) as numUp, */
  sum(cast(quotes.newestClose < quotes.newestOpen as INT64)) as numDown,
  sum(quotes.newestVolume) as volume
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
    FROM `notifications.quotes`
) quotes
LEFT JOIN `notifications.shares` as shares on shares.service_id = quotes.service_id
WHERE
  close > 0.0
AND
  date > TIMESTAMP "2014-01-01"
AND
  shares.market IN ('stockholm', 'first-north')
AND
  shares.listing_nasdaq IN ('nordic-large-cap', 'nordic-mid-cap') 
GROUP BY
  date,
  id
ORDER BY
  date asc
  /* id */ 
