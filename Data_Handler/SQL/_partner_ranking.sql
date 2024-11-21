-- Page: Overview  - Quote Ranking Proportion 

select
RATE_EFFECTIVE_DATE as DATE,
cast(partnerrankposition as INT64) as RANKING,
case when UNDERWRITER_PRODUCT=504 then "GOLD"
      when UNDERWRITER_PRODUCT=518 then "OCEA" 
                                    else "Error" end as AFNTY_BRAND,
count(*) as QUOTE_COUNT
FROM `pricing-nonprod-687b.ML.AL_ARCHIVE_COMP`
where UNDERWRITER_PRODUCT in (504,518)
and AFNTY_BRAND in ("BUDD", "IHAF")
AND  RATE_EFFECTIVE_DATE>= '2022-02-01' 
group by 
RATE_EFFECTIVE_DATE,
partnerrankposition,
AFNTY_BRAND
order by
RATE_EFFECTIVE_DATE asc,
partnerrankposition desc