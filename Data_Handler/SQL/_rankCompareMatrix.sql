-- Page: Model Tracking - Rank Comparison Matrix 

select
count(GOLD.CLIENT_NUMBER) as QUOTE_COUNT,
GOLD.RATE_EFFECTIVE_DATE as DATE,
GOLD.GOLD_RANKING,
case when GOLD.VEHICLE_kms in ("K","L","M","N") then 'LowKM'
                                                else 'Otherwise' end as AnnualKM_Banding
,OCEA.OCEA_RANKING
,OCEA.SALE_STATUS
from ( 
    -- BUDGET DIRECT GOLD
    SELECT
    journeyid,
    RATE_EFFECTIVE_DATE,
    PC_CORVEH_FIN_PREM,
    CLIENT_NUMBER,
    VEHICLE_kms,
    partnerrankposition as GOLD_RANKING
    FROM
      `pricing-nonprod-687b.ML.AL_ARCHIVE_COMP`
    WHERE UNDERWRITER_PRODUCT =504 and AFNTY_BRAND="BUDD"
    ) GOLD

inner join (
    -- OCEANIA
    SELECT
    L.journeyid,
    L.RATE_EFFECTIVE_DATE,
    L.PC_CORVEH_FIN_PREM,
    L.CLIENT_NUMBER,
    L.NVI_Code,
    L.GNAF_PID,
    L.partnerrankposition as OCEA_RANKING
    ,case when S.XLEAD is not null then 'SOLD'
                                    else "QUOTE" end as  SALE_STATUS
    FROM
      `pricing-nonprod-687b.ML.AL_ARCHIVE_COMP` L
    
    LEFT JOIN `pricing-nonprod-687b.ML.SALES_OCEA` S
    ON S.XLEAD=L.CLIENT_NUMBER 
    WHERE L.UNDERWRITER_PRODUCT =518 and L.AFNTY_BRAND="IHAF" -- change this to 518, IHAF    
    ) OCEA
on GOLD.journeyid = OCEA.journeyid
--due to Oceania CORVEH inclusive of lowkm discount, we are not able to match with GOLD
-- and round(GOLD.PC_CORVEH_FIN_PREM,0)=round(OCEA.PC_CORVEH_FIN_PREM,0) 
and GOLD.RATE_EFFECTIVE_DATE=OCEA.RATE_EFFECTIVE_DATE

group by
GOLD.RATE_EFFECTIVE_DATE,
GOLD.GOLD_RANKING,
case when GOLD.VEHICLE_kms in ("K","L","M","N") then 'LowKM'
                                                else 'Otherwise' end,
OCEA.OCEA_RANKING,
OCEA.SALE_STATUS                                
