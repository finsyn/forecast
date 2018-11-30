SELECT
  date,
  service_id as id,
  open,
  high,
  low
FROM `notifications.quotes`
WHERE service_id = 'cfd_OMX30-20SEK-MINUTE_15'
AND format_timestamp("%H:%M", date, "{timezone}") >= '{time_from}'
AND format_timestamp("%H:%M", date, "{timezone}") <= '{time_to}'


GROUP BY
  date,
  id,
  open,
  high,
  low
ORDER BY
  date asc
