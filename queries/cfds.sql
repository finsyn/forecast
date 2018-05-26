SELECT
  TIMESTAMP_TRUNC(openQuotes.date, DAY) AS date,
  openQuotes.service_id as id,
  closeQuotes.newestClose as c,
  openQuotes.newestOpen as o
FROM
(
  SELECT
    # we might have duplicates, if so  want the latest added value
    first_value(open) over (partition by service_id, date order by created_at desc) as newestOpen,
    *
    FROM `notifications.quotes`
    WHERE format_timestamp("%H:%M", date, "Europe/Stockholm") = '09:00'
    AND service_id = 'cfd_OMX30-20SEK-HOUR'
) openQuotes
INNER JOIN (
  SELECT
    # we might have duplicates, if so  want the latest added value
    first_value(close) over (partition by service_id, date order by created_at desc) as newestClose,
    *
    FROM `notifications.quotes`
    WHERE format_timestamp("%H:%M", date, "Europe/Stockholm") = '17:00'
    AND service_id = 'cfd_OMX30-20SEK-HOUR'
) closeQuotes
on format_timestamp("%F", closeQuotes.date) = format_timestamp("%F", openQuotes.date)
GROUP BY
  date,
  id,
  o,
  c
ORDER BY
  date asc
