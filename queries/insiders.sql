SELECT
  DISTINCT TIMESTAMP_TRUNC(published_at, DAY) AS date,
  SUM(CAST(REPLACE(REPLACE(transaction_type, 'Avyttring', '1'), 'Förvärv', '0') AS INT64)) AS sell,
  SUM(CAST(REPLACE(REPLACE(transaction_type, 'Förvärv', '1'), 'Avyttring', '0') AS INT64)) AS buy,
  'all' as id
FROM
  `insikt-e1887.notifications.transactions` transactions
INNER JOIN
  (
    SELECT service_id, sector FROM `insikt-e1887.notifications.shares`
  ) shares 
  ON shares.service_id = transactions.service_id
WHERE transaction_type IN ('Avyttring', 'Förvärv')
AND status = 'Aktuell'
AND finsyn_type IN ('single', 'bundle-part')
AND volume_unit = 'Antal'
GROUP BY
  date,
  id
ORDER BY
  date asc
