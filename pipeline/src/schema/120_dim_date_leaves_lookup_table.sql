CREATE TABLE IF NOT EXISTS final.dim_date_leaves (
    leave_id INT,
    date_id INT,
    CONSTRAINT fk_dim_dl_leave FOREIGN KEY (leave_id) REFERENCES final.fact_leaves(leave_id_sk),
    CONSTRAINT fk_dim_dl_date FOREIGN KEY (date_id) REFERENCES final.dim_date(date_id),
    CONSTRAINT dim_date_dates_lookup_unique UNIQUE (leave_id, date_id)
);
