-- Get the Percentage Discount --

/* 1.
 -- Only extract unique lead from Earnix sales log
 -- This may includes same quote being call twice due to information update
 -- This can be obserbed by changes in Earnix_Demand (probability from model)
*/
create or replace temp table unique_led as
select 
* except(rank)
,case when VEHKMS="K" then 0.88
      when VEHKMS="L" then 0.9 
      when VEHKMS="M" then 0.94
      when VEHKMS="N" then 0.98
                      else 1 end as lowkm_loading
,case when VEHKMS in ("K","L","M","N") then 'LowKM'
                                       else 'Otherwise' end as AnnualKM_Banding,                      
from(
  select
  parse_date('%Y-%m-%d', RTEDAT) as RTEDAT
  ,CLIENT_NUMBER
  ,VEHKMS
  ,INSNAM
  ,ADJUSTMENT_FACTOR
  ,EARNIX_DEMAND
  ,row_number() over(partition by client_number,CORVEH,EARNIX_DEMAND order by FILE_KEY) as rank
  from `data-lake-prod-31d7.rating_log_motor_earnix.PC_SLS_*`
  where 1=1
    and UNDPRD=18
    and RATING_PROCESS_MODE in ("LED")
    and RTEDAT >='2022-03-01'
    and PAYTRM="L"
    and MEDTYP="CM"    
    )
where rank=1
;

/* 2.
 -- Define Discount criteria
 -- Edge cases can of observed in this table if any.
 -- When a client number is repeated but have discounted & loaded reason at the same time.
*/
create temp table discount_reason as
select
*
,case when OC_Discount <1                                              then "Discounted"
      when (
           (DT_trunc = "2022-03-01" and EARNIX_DEMAND<0.36756381037855834)
            or
           (DT_trunc = "2022-04-01" and EARNIX_DEMAND<0.35901945610869135)
           )
          and INSNAM in ('BUDGET DIRECT', 'AUTO GENERAL SERVICES P/L') then "Previous Insurer BD"
      when (
           (DT_trunc = "2022-03-01" and EARNIX_DEMAND<0.36756381037855834)
            or
           (DT_trunc = "2022-04-01" and EARNIX_DEMAND<0.35901945610869135)
           )
          and OC_Discount >0                                           then "Margin not Allowed"
                                                                       else "Loaded" end as REASON
from (
  select
  *,
  DATE_TRUNC(RTEDAT, MONTH) as DT_trunc,
  ADJUSTMENT_FACTOR/0.85*lowkm_loading as OC_Discount
  from unique_led
    )
;

/* 3.
 -- Find EDGE cases where it is loaded & discounted at different part of sales journey
*/
create or replace table `pricing-nonprod-687b.ML.AL_edgeCase` as  
select
CLIENT_NUMBER
from(
    select
    client_number
    ,count(client_number) as cnt
    from (
      select
      client_number
      ,REASON
      from discount_reason
      group by 
      client_number
      ,REASON
          )
     group by  client_number    
    )
where cnt>1
;
            
/* 4.
 -- Summartied for python chart percentage Discount
*/ 
select
RTEDAT as DATE
,REASON
,AnnualKM_Banding
,count(*) as QUOTE_COUNT
from discount_reason
group by
RTEDAT 
,REASON
,AnnualKM_Banding
