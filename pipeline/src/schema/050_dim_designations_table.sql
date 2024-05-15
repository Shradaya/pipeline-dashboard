CREATE TABLE IF NOT EXISTS final.dim_designations (
    id SERIAL,
    designation_id VARCHAR(10),
    designation_name VARCHAR(50),
    CONSTRAINT dim_designation_pk PRIMARY KEY (id),
    CONSTRAINT dim_designation_id_unique UNIQUE (designation_id)
);
