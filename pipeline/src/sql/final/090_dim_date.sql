INSERT INTO
    final.dim_date (
        fiscal_id,
        date_value,
        year,
        quarter,
        month,
        day_of_week,
        week_of_year,
        holiday
    ) WITH fiscal_periods AS (
        SELECT
            id,
            fiscal_start_date,
            fiscal_end_date
        FROM
            final.dim_fiscal
        order by
            fiscal_start_date
    ),
    series AS (
        SELECT
            id as fiscal_id,
            generate_series(fiscal_start_date, fiscal_end_date, '1 day') :: date AS date_value
        FROM
            fiscal_periods
    ),
    final AS (
        SELECT
            fiscal_id,
            date_value,
            EXTRACT(
                year
                FROM
                    date_value
            ) AS year,
            EXTRACT(
                quarter
                FROM
                    date_value
            ) AS quarter,
            EXTRACT(
                month
                FROM
                    date_value
            ) AS month,
            EXTRACT(
                isodow
                FROM
                    date_value
            ) AS day_of_week,
            EXTRACT(
                week
                FROM
                    date_value
            ) AS week_of_year
        FROM
            series
    )
SELECT fiscal_id,
        date_value,
        year,
        quarter,
        month,
        day_of_week,
        week_of_year,
        CASE
            WHEN day_of_week = 6
            OR day_of_week = 7 THEN true
            ELSE false
        END AS holiday
    FROM final
ON CONFLICT ON CONSTRAINT dim_date_value_unique DO NOTHING;