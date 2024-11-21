-- The following script download data from AL_ARCHIVE for Oceania scoring purpose
-- This SQL take the latest 365 days of data
-- 1. COVER_TYPE='A'  (Comprehensive)
-- 2. AFNTY_BRAND='BUDD'

-- updated 01 DEC 2021 by Marcus Leong

-- DECLARE max_date DATE;
-- SET max_date = (select MAX(quotecompleted) FROM `pricing-nonprod-687b.ML.AL_ARCHIVE`);


 SELECT
    quotecompleted as QUOTE_DATE,
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
    STATE_CODE
  FROM
    `pricing-nonprod-687b.ML.AL_ARCHIVE`
  WHERE
    1=1
    AND AFNTY_BRAND='BUDD' --Use quotes from Budget Direct Comprehensive only
    AND COVER_TYPE='A'
--     AND quotecompleted >= DATE_ADD(max_date, INTERVAL -365 DAY) 
    and quotecompleted >='2021-12-01'