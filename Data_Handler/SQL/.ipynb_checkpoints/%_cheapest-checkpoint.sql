-- The following script count number of cheapest quotes per brand each day

-- DECLARE max_date DATE;
-- SET max_date = (select MAX(quotecompleted) FROM `pricing-nonprod-687b.ML.AL_ARCHIVE`);

select
quotecompleted as QUOTE_DATE,
AFNTY_BRAND,
ranked_1_Y,
ranked_1_N,
ranked_1_Y + ranked_1_N as total
from (
  select *
  from (
        SELECT
          quotecompleted,
          AFNTY_BRAND,
          CASE WHEN partnerrankposition = 1 THEN 'ranked_1_Y'
                                            ELSE 'ranked_1_N' END AS rank_1,
          count( policy_quoteno )  N_quotes
        FROM
          `pricing-nonprod-687b.ML.AL_ARCHIVE`
        where 1=1
        and quotecompleted >='2021-12-01'
    --             AND quotecompleted >= DATE_ADD(max_date, INTERVAL -365 DAY) 
        GROUP BY
          quotecompleted,
          AFNTY_BRAND,
          rank_1 
        )
  pivot (sum(N_quotes)
         for rank_1 in ('ranked_1_Y','ranked_1_N'))
  )
order by    
quotecompleted asc