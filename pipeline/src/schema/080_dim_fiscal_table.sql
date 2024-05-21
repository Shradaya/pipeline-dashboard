CREATE TABLE IF NOT EXISTS final.dim_fiscal (
    id SERIAL,
    fiscal_start_date date,
    fiscal_end_date date,
    CONSTRAINT dim_fiscal_pk PRIMARY KEY (id),
    CONSTRAINT dim_fiscal_id_unique UNIQUE (fiscal_start_date, fiscal_end_date)
);