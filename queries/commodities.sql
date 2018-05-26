SELECT
  TIMESTAMP_TRUNC(date, DAY) AS date,
  quotes.service_id as id,
  quotes.newestClose as c
FROM
(
  SELECT
    # we might have duplicates, then we want the latest added value
    first_value(close) over (partition by service_id, TIMESTAMP_TRUNC(date, DAY) order by created_at desc) as newestClose,
    *
    FROM `notifications.quotes`
) quotes
WHERE
  close > 0.0
AND
(
  quotes.service_id IN (
    # global commodities
    'commodity_butane',
    'commodity_oil-brent',
    'commodity_wld-itimber',
    'commodity_copper',
    'commodity_fe-tjn',
    'commodity_al-lme'
  )
)
AND
  date > TIMESTAMP "2010-01-01"
GROUP BY
  date,
  id,
  c
ORDER BY
  date asc,
  id
