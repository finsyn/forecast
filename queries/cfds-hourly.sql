SELECT
  TIMESTAMP_TRUNC(openQuotes.date, HOUR) AS date,
  openQuotes.service_id as id,
  openQuotes.newestOpen as o
FROM
(
  SELECT
    # we might have duplicates, if so  want the latest added value
    first_value(open) over (partition by service_id, TIMESTAMP_TRUNC(date, HOUR) order by created_at desc) as newestOpen,
    *
    FROM `notifications.quotes`
    /* WHERE format_timestamp("%H:%M", date, "Europe/Stockholm") = '10:00' */
    WHERE service_id = 'cfd_OMX30-20SEK-HOUR'
) openQuotes

GROUP BY
  date,
  id,
  o
ORDER BY
  date asc
