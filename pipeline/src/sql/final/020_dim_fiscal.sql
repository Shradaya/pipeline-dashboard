INSERT INTO final.dim_fiscal (fiscal_id, fiscal_start_date, fiscal_end_date) 
SELECT DISTINCT
    fiscal_id, fiscal_start_date, fiscal_end_date
FROM
    std.std_data
    order by fiscal_start_date
ON CONFLICT ON CONSTRAINT dim_fiscal_id_unique
DO NOTHING;
