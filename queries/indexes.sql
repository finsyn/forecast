SELECT
  TIMESTAMP_TRUNC(date, DAY) AS date,
  quotes.service_id as id,
  quotes.newestClose as c,
  quotes.newestOpen as o,
  quotes.newestHigh as h,
  quotes.newestLow as l,
  quotes.newestVolume as v
FROM
(
  SELECT
    # we might have duplicates, then we want the latest added value
    first_value(open) over (partition by service_id, TIMESTAMP_TRUNC(date, DAY) order by created_at desc) as newestOpen,
    first_value(close) over (partition by service_id, TIMESTAMP_TRUNC(date, DAY) order by created_at desc) as newestClose,
    first_value(volume) over (partition by service_id, TIMESTAMP_TRUNC(date, DAY) order by created_at desc) as newestVolume,
    first_value(high) over (partition by service_id, TIMESTAMP_TRUNC(date, DAY) order by created_at desc) as newestHigh,
    first_value(low) over (partition by service_id, TIMESTAMP_TRUNC(date, DAY) order by created_at desc) as newestLow,
    *
    FROM `notifications.quotes`
) quotes
LEFT JOIN `notifications.shares` as shares on shares.service_id = quotes.service_id
WHERE
  close > 0.0 AND open > 0.0
AND
(
  quotes.service_id IN (
    # global markets
    /* 'market-index_AEX', */
    /* 'market-index_CBOE', */
    /* 'market-index_DJI', */
    /* 'market-index_EURONEXT', */
    'market-index_FTSE',
    /* 'market-index_GDAXI', */
    /* issues to get opening prices on these from the daily job */     
    /* 'market-index_HANGSENG', */
    /* 'market-index_NIKKEI', */
    /* 'market-index_NYSE', */
    /* 'market-index_OMX30', */
    'market-index_SP500',

    # commodities index
    'market-index_USCI',
    # volatility index
    'market-index_VIX',
    # some branch indexes
    'market-index_XLB',
    'market-index_XLE',
    'market-index_XLF',
    'market-index_XLI',
    'market-index_XLK',
    'market-index_XLU',
    'market-index_XLV',
    'market-index_XLP'
    # not enough historical real estate data available
    # 'market-index_XLRE',

    # 'security_SE0000869646'
    # 'security_SE0000106270',
    # 'security_CH0012221716',
    # 'security_SE0000695876',
    # 'security_SE0007100581',
    # 'security_GB0009895292',
    # 'security_SE0000108656',
    # 'security_SE0008374250',
    # 'security_SE0000667891',
    # 'security_SE0001785197',
    # 'security_SE0000115446',
    # 'security_SE0000310336',
    # 'security_SE0007100599',
    # 'security_SE0000242455',
    # 'security_SE0000171100',
    # 'security_SE0000108227',
    # 'security_SE0000113250',
    # 'security_SE0000148884',

    # currencies */
    /* 'market-index_SEKUSD', */
    /* 'market-index_CNYUSD', */
    /* 'market-index_JPYUSD' */
    /* 'market-index_GBPUSD' */
  )
)
AND
  date > TIMESTAMP "2010-01-01"
GROUP BY
  date,
  id,
  o,
  c,
  l,
  h,
  v
ORDER BY
  date asc,
  id
