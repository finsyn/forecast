SELECT
  DISTINCT TIMESTAMP_TRUNC(date, DAY) AS date,
  service_id as id,
  open,
  close,
  volume
FROM `notifications.quotes_training`
GROUP BY
  date,
  id,
  open,
  close,
  volume
ORDER BY
  date asc,
  id
