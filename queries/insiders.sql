SELECT
  DISTINCT TIMESTAMP_TRUNC(TIMESTAMP(created_at), DAY) AS date,
  SUM(CAST(REPLACE(REPLACE(transaction_type, 'Avyttring', '1'), 'Förvärv', '0') AS INT64) * CAST(volume AS FLOAT64) * CAST(price AS FLOAT64)) AS sell,
  SUM(CAST(REPLACE(REPLACE(transaction_type, 'Förvärv', '1'), 'Avyttring', '0') AS INT64) * CAST(volume AS FLOAT64) * CAST(price AS FLOAT64)) AS buy
FROM
  `insikt-e1887.notifications.transactions_ds`
WHERE transaction_type IN ('Avyttring', 'Förvärv')
GROUP BY
  date
ORDER BY
  date asc
