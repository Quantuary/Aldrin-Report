-- Page: Model Tracking - Confusion Matrix

/* 1.
 -- Preprocess the data to get lowkm discount
 -- Define what is discount/loaded
*/

Create or replace temp table OceaniaPreprocess as
select
*
,case when OC_Discount >0 then "1.Loaded"
      when OC_Discount <=0   then "2.Discounted" 
       else "Error" end as PREDICTED
from(
    select
    *
    ,VEHICLE_PREMIUM3*(1- 0.85/(ADJUSTMENT_FACTOR*lowkm_loading)
                           ) as OC_Discount
    from (
      select
      journeyid
      ,RATE_EFFECTIVE_DATE
      ,PC_CORVEH_FIN_PREM
      ,CLIENT_NUMBER
      ,ADJUSTMENT_FACTOR
      ,case when VEHICLE_KMS="K" then 0.88
        when VEHICLE_KMS="L" then 0.9 
        when VEHICLE_KMS="M" then 0.94
        when VEHICLE_KMS="N" then 0.98
                              else 1 end as lowkm_loading
      ,VEHICLE_PREMIUM3
      ,partnerrankposition
       FROM
            `pricing-nonprod-687b.ML.AL_ARCHIVE_COMP`
         WHERE UNDERWRITER_PRODUCT=518 and AFNTY_BRAND="IHAF" -- change this to 518, IHAF
    )
)
;
/* 2.
 -- Join the predicted from Oceania to the actual ranking from Budget Gold
*/
select
GOLD.RATE_EFFECTIVE_DATE as DATE,
GOLD.AnnualKM_Banding,
case when GOLD.partnerrankposition=2 
        and OCEA.partnerrankposition=1 then "1. Rank Top"  --this is the false positive case
        else GOLD.RANKING end as RANKING,
        
OCEA.PREDICTED,
count(GOLD.CLIENT_NUMBER)  as QUOTE_COUNT
from(
   -- BUDGET DIRECT GOLD
   SELECT
    journeyid,
    RATE_EFFECTIVE_DATE,
    PC_CORVEH_FIN_PREM,
    CLIENT_NUMBER,
    partnerrankposition,
    case when VEHICLE_kms in ("K","L","M","N") then 'LowKM'
                                               else 'Otherwise' end as AnnualKM_Banding,
    case when partnerrankposition=1 then "1. Rank Top"
          when partnerrankposition>1 then '2. Rank Bottom'
                                 else "Error" end as RANKING

    FROM
      `pricing-nonprod-687b.ML.AL_ARCHIVE_COMP`
    WHERE UNDERWRITER_PRODUCT =504 and AFNTY_BRAND="BUDD"
    ) GOLD
inner join OceaniaPreprocess OCEA
on GOLD.journeyid = OCEA.journeyid
--due to Oceania CORVEH inclusive of lowkm discount, we are not able to match with GOLD
-- and round(GOLD.PC_CORVEH_FIN_PREM,0)=round(OCEA.PC_CORVEH_FIN_PREM,0) 
and GOLD.RATE_EFFECTIVE_DATE=OCEA.RATE_EFFECTIVE_DATE
group by 
GOLD.RATE_EFFECTIVE_DATE,
GOLD.AnnualKM_Banding,
case when GOLD.partnerrankposition=2 
        and OCEA.partnerrankposition=1 then "1. Rank Top"  --this is the false positive case
        else GOLD.RANKING end,
        
OCEA.PREDICTED
;
