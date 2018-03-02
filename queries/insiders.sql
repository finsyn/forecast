SELECT
  DISTINCT TIMESTAMP_TRUNC(TIMESTAMP(created_at), DAY) AS date,
  SUM(CAST(REPLACE(REPLACE(transaction_type, 'Avyttring', '-1'), 'Förvärv', '1') AS INT64) * CAST(volume AS FLOAT64) * CAST(price AS FLOAT64)) AS netSum
FROM
  `insikt-e1887.notifications.transactions_ds`
WHERE transaction_type IN ('Avyttring', 'Förvärv')
GROUP BY
  date
ORDER BY
  date asc
