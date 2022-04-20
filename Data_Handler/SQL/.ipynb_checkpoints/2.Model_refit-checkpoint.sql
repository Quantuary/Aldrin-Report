-- The following script download data from AL_ARCHIVE for Oceania ML model update only
-- This SQL take only latest unique price point with condition:
-- 1. COVER_TYPE='A'  (Comprehensive)
-- 2. AFNTY_BRAND='BUDD'
-- 3. 90 days rolling data.

-- updated 26 NOV 2021 by Marcus Leong

DECLARE max_date DATE;
-- SET max_date = (select MAX(quotecompleted) FROM `pricing-nonprod-687b.ML.AL_ARCHIVE`);

select
* except(rank)
from (
  SELECT
    cast(partnerrankposition as int64) partnerrankposition,  --target
  -- list of all variables for existing model
    VEHICLE_MODEL,
    VEHICLE_KMS,
    cast(WE_COST as float64) WE_COST,
    DRIVER_OPTION,
    VEHICLE_COLOUR,
    cast(PC_CORVEH_FIN_PREM as float64) PC_CORVEH_FIN_PREM ,
    cast(TH_FREQ as float64) TH_FREQ,
    cast(HC_FREQ as float64) HC_FREQ,
    cast(NCD as INT64) NCD,
    YD_LICENCE_TYPE,
    cast(POSTCODE as int64) POSTCODE,
    cast(OD_COST as float64) OD_COST,
    cast(WE_FREQ as float64) WE_FREQ,
    cast(HC_COST as float64) HC_COST,
    cast(TP_FREQ as float64) TP_FREQ,
    cast(VEHICLE_AGE as int64) VEHICLE_AGE,
    cast(RD_CLAIM_COUNT_5YR as int64) RD_CLAIM_COUNT_5YR,
    cast(ACCESSORIES_VALUE as int64) ACCESSORIES_VALUE,
    cast(TP_COST as float64) TP_COST,
    STATE_CODE,
  -- End of list of all variables for existing model
    row_number() over(partition by 
        partnerrankposition, VEHICLE_MODEL, VEHICLE_KMS, WE_COST,
        DRIVER_OPTION, VEHICLE_COLOUR, PC_CORVEH_FIN_PREM, TH_FREQ,
        HC_FREQ, NCD, YD_LICENCE_TYPE, POSTCODE, OD_COST, WE_FREQ,
        HC_COST, TP_FREQ,VEHICLE_AGE, RD_CLAIM_COUNT_5YR,
        ACCESSORIES_VALUE, TP_COST, STATE_CODE
    order by RATING_TIMESTAMP desc) as rank, 
  FROM
    `pricing-nonprod-687b.ML.AL_ARCHIVE`
  WHERE
    1=1
    AND AFNTY_BRAND='BUDD' --Use quotes from Budget Direct Comprehensive only
    AND COVER_TYPE='A'
    and quotecompleted < '2021-12-01'
--     AND quotecompleted >= DATE_ADD(max_date, INTERVAL -90 DAY) 
  ) 
where rank=1 -- Take latest unique price point