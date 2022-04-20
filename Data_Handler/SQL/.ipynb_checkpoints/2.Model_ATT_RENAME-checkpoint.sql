  -- The following script download data from AL_ARCHIVE for Aldrin ML model version 2
  -- This version include alignment of variables name and rerun the model for the latest data
  -- updated 09 NOV 2021 by Marcus Leong

SELECT
 L.policy_quoteno,
 quotecompleted,
 policy_sold,
 partnerrankposition,
 cast(VEHICLE_PREMIUM3/0.85 as float64)  as CORGPR,          --removing online discount
 
 -- Aligning MODEL attributes' NAME
 cast(ACCESSORIES_VALUE as float64)      as ACCVAL,
 cast(RD_CLAIM_COUNT_5YR as int)         as CLMTOT,
 cast(NCD as int64)                      as CORNCD,
 cast(POSTCODE as STRING)                as CORPCD,  --required Enx setup as NOM
 cast(PC_CORVEH_FIN_PREM as float64)     as CORVEH,
 DRIVER_OPTION                     as DRVOPT,
 cast(HC_FIN_PREM as float64)      as HCCOST,
 cast(HC_FREQ as float64)          as HCFREQ,
 cast(OD_FIN_PREM as float64)  as ODCOST,
 STATE_CODE   as STACDE,
 cast(TH_FREQ as float64)      as THFREQ,
 cast(TP_FIN_PREM as float64)  as TPCOST,  
 cast(TP_FREQ as float64)      as TPFREQ,
 cast(VEHICLE_AGE as int64)   as VEHAGE,
 VEHICLE_COLOUR               as VEHCLR,
 VEHICLE_KMS                  as VEHKMS,
 VEHICLE_MODEL                as VEHMDL,
 cast(WE_FREQ  as float64)     as WEFREQ,
 cast(WE_FIN_PREM  as float64) as WECOST, 
 cast(YD_LICENCE_TYPE as STRING) as YGDLIC,    --required Enx setup as int64

 R.coverdetail_previousinsurer     as INSNAM,  --Required Enx setup as NOM
 
    FROM
      `pricing-nonprod-687b.ML.AL_ARCHIVE` L
    left join (
        select
        distinct policy_quoteno,
        coverdetail_previousinsurer
        from `data-lake-prod-31d7.ctm_gi_risk_file.gi_risk_motor`
        where policy_quoteno is not null    
            ) R
      on  L.policy_quoteno=R.policy_quoteno    
    WHERE
      1=1
      AND AFNTY_BRAND='BUDD' 
      and quotecompleted>'2021-10-09' -- Date range to model on
      and quotecompleted<'2021-11-01'
      and COVER_TYPE ='A'