CREATE TABLE IF NOT EXISTS final.dim_leave_types (
    id SERIAL,
    leave_type_id VARCHAR(10),
    leave_type_name VARCHAR(20),
    CONSTRAINT dim_leave_type_pk PRIMARY KEY (id),
    CONSTRAINT dim_leave_type_id_unique UNIQUE (leave_type_id)
);
