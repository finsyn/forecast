SELECT
  distinct omx.date,
  sum(shares.volume) as totVolume,
  stddev(shares.percentChange) as totChangeVariance,
  omx.intraDayDiff as omxIntraDayDiff,
  omx.percentChange,
  CASE
    WHEN omx.percentChange < -0.5 THEN 'decreased'
    WHEN omx.percentChange > 0.5  THEN 'increased'
    ELSE 'neutral'
    END 
  AS omxState
FROM
  (select distinct date, volume, (open - close)/open * 100 as percentChange, abs(low - high) as intraDayDiff
  from `insikt-e1887.notifications.quotes_training` where service_id = 'market-index_OMX30' group by date, volume, percentChange, intraDayDiff) omx
inner join
  (select distinct date, volume, (open - close)/open * 100 as percentChange
  from `insikt-e1887.notifications.quotes_training` where service_id != 'market-index_OMX30' group by date, volume, percentChange) shares
ON
  omx.date = shares.date
GROUP BY
  omx.date,
  omx.intraDayDiff,
  omx.percentChange
ORDER BY
  date asc
