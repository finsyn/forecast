SELECT
  DISTINCT TIMESTAMP_TRUNC(published_at, WEEK(MONDAY)) AS date,
  SUM(CAST(REPLACE(REPLACE(transaction_type, 'Avyttring', '1'), 'Förvärv', '0') AS INT64) * price * volume) AS sell,
  SUM(CAST(REPLACE(REPLACE(transaction_type, 'Förvärv', '1'), 'Avyttring', '0') AS INT64) * price* volume) AS buy,
  'all' as id
FROM
  `insikt-e1887.notifications.transactions` transactions
INNER JOIN
  (
    SELECT service_id, sector, listing_nasdaq, fiftyTwoWeekLow.float as low, fiftyTwoWeekHigh.float as high
    FROM `insikt-e1887.notifications.shares`
  ) shares 
  ON shares.service_id = transactions.service_id
WHERE transaction_type IN ('Avyttring', 'Förvärv')
AND status = 'Aktuell'
AND finsyn_type IN ('single', 'bundle-part')
AND volume_unit = 'Antal'
AND shares.listing_nasdaq = 'nordic-large-cap'
AND price < shares.high
AND price > shares.low 
GROUP BY
  date,
  id
ORDER BY
  date asc
