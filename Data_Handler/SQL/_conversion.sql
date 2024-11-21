-- The following script get the aggregate result from ML.conversion table,
-- which collect sales count, quote count and vehicle_premium from EDW.Sales and PCXMLLOG

SELECT 
RATE_EFFECTIVE_DATE as DATE --Reporting date in the time-series
,case when UNDERWRITER_PRODUCT=504 then "GOLD"
      when UNDERWRITER_PRODUCT=518 then "OCEA" 
                                    else "Error" end as AFNTY_BRAND
,CANC_STATUS
,SALE_STATUS
,cast(sum(MARGIN) as FLOAT64)          as MARGIN
,cast(sum(VEHICLE_PREMIUM) as FLOAT64) as VEHICLE_PREMIUM
,cast(sum(SALES_COUNT) as FLOAT64)     as SALES_COUNT 
,cast(sum(QUOTE_COUNT) as FLOAT64)     as QUOTE_COUNT
FROM `pricing-nonprod-687b.ML.conversion`
where 1=1
  and( (RATE_EFFECTIVE_DATE>'2022-02-28' and underwriter_product=518)
        or underwriter_product<>518
      )
group by 
RATE_EFFECTIVE_DATE
,AFNTY_BRAND
,CANC_STATUS
,SALE_STATUS
order by RATE_EFFECTIVE_DATE asc
;