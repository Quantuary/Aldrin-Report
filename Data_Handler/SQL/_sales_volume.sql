-- Page: Overview  - Premium Sold
-- The following script extract sales volume and premium

SELECT 
SALE_DATE as DATE
,case when UNDERWRITER_PRODUCT="0504" then "GOLD"
      when UNDERWRITER_PRODUCT="0518" then "OCEA" 
                          else "Error" end as AFNTY_BRAND
,case when MEDIA_TYPE='CM' then 'CTM'
                           else 'Others' end as CHANNEL
,sum( SALES_COUNT ) as SALES_COUNT
,sum( RISK_CLASS_1_ANNUAL_PREMIUM ) as VEHICLE_PREMIUM
FROM `pricing-nonprod-687b.ML.SALES`
where 1=1
and COVER_TYPE ="COMPREHENSIVE"
and SALE_DATE >="2022-03-01"
group by
SALE_DATE 
,case when UNDERWRITER_PRODUCT="0504" then "GOLD"
      when UNDERWRITER_PRODUCT="0518" then "OCEA" 
                          else "Error" end
,case when MEDIA_TYPE='CM' then 'CTM'
                           else 'Others' end 
                           ;