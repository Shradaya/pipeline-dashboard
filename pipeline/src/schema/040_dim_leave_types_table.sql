CREATE TABLE IF NOT EXISTS final.dim_leave_types (
    id SERIAL,
    fiscal_id INT,
    leave_type_id VARCHAR(10),
    leave_type_name VARCHAR(20),
    default_days INT,
    transferable_days INT,
    CONSTRAINT dim_leave_type_pk PRIMARY KEY (id),
    CONSTRAINT dim_leave_type_id_unique UNIQUE (fiscal_id, leave_type_id)
);
