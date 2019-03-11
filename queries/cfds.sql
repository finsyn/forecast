SELECT
  TIMESTAMP_TRUNC(openQuotes.date, DAY) AS date,
  openQuotes.service_id as id,
  closeQuotes.newestClose as c,
  openQuotes.newestOpen as o
  /* max(extremeQuotes.newestHighest) as h, */
  /* min(extremeQuotes.newestLowest) as l */
FROM
(
  SELECT
    # we might have duplicates, if so  want the latest added value
    first_value(open) over (partition by service_id, date order by created_at desc) as newestOpen,
    *
    FROM `notifications.quotes`
    WHERE format_timestamp("%H:%M", date, "{timezone}") = '{time_from}'
    AND service_id = '{service_id}'
) openQuotes

INNER JOIN (
  SELECT
    # we might have duplicates, if so  want the latest added value
    first_value(open) over (partition by service_id, date order by created_at desc) as newestClose,
    *
    FROM `notifications.quotes`
    WHERE format_timestamp("%H:%M", date, "{timezone}") = '{time_to}'
    AND service_id = '{service_id}'
) closeQuotes
on format_timestamp("%F", closeQuotes.date) = format_timestamp("%F", openQuotes.date)

/* INNER JOIN ( */
/*   SELECT */
/*   first_value(high) over (partition by service_id, date order by created_at desc) as newestHighest, */
/*   first_value(low) over (partition by service_id, date order by created_at desc) as newestLowest, */
/*   * */
/*   FROM `notifications.quotes` */
/*   WHERE format_timestamp("%H:%M", date, "{timezone}") >= '{time_from}' */
/*   AND   format_timestamp("%H:%M", date, "{timezone}") <= '{time_to}' */
/*   AND service_id = '{service_id}' */
/* ) extremeQuotes */
/* on format_timestamp("%F", closeQuotes.date) = format_timestamp("%F", extremeQuotes.date) */

/* WHERE */
/*  /1* missing this for some NIKKEI days *1/ */
/*  extremeQuotes.newestLowest > 0.0 */
GROUP BY
  date,
  id,
  o,
  c
ORDER BY
  date asc
