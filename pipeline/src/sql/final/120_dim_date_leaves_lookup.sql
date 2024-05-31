INSERT INTO
    final.dim_date_leaves (leave_id, date_id)
select
    leave_id_sk,
    dd.date_id
from
    (
        select
            leave_id_sk,
            generate_series(start_date, end_date, '1 day') :: date AS date_value
        from
            final.fact_leaves
    ) fl
    join (
        SELECT
            *
        FROM
            final.dim_date ddi
        WHERE
            ddi.holiday = false
    ) dd on dd.date_value = fl.date_value ON CONFLICT ON CONSTRAINT dim_date_dates_lookup_unique DO NOTHING;