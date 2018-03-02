SELECT
  FORMAT_TIMESTAMP('%Y-%V', TIMESTAMP_TRUNC(date, WEEK(MONDAY)), 'Europe/Stockholm') AS date,
  service_id as id,
  (weekClose - weekOpen)/weekOpen * 100 as weekChange,
  sum(volume) as weekVolume
FROM
(
  SELECT
    first_value(open) over (partition by service_id, TIMESTAMP_TRUNC(date, WEEK(MONDAY)) order by date asc) as weekOpen,
    first_value(close) over (partition by service_id, TIMESTAMP_TRUNC(date, WEEK(MONDAY)) order by date desc) as weekClose,
    *
    FROM `notifications.quotes_training`
)
GROUP BY
  id,
  week,
  weekOpen,
  weekClose
ORDER BY
  week asc,
  id
