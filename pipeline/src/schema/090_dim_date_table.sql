CREATE TABLE IF NOT EXISTS final.dim_date (
    date_id SERIAL,
    fiscal_id INT,
    date_value DATE,
    year INT,
    quarter INT,
    month INT,
    day_of_week INT,
    week_of_year INT,
    holiday BOOL,
    CONSTRAINT dim_date_pk PRIMARY KEY (date_id),
    CONSTRAINT fk_fiscal FOREIGN KEY (fiscal_id) REFERENCES final.dim_fiscal(id),
    CONSTRAINT dim_date_value_unique UNIQUE (date_value)
);
