CREATE TABLE IF NOT EXISTS final.dim_departments (
    id SERIAL,
    department_name VARCHAR(50),
    CONSTRAINT dim_department_pk PRIMARY KEY (id),
    CONSTRAINT dim_department_name_unique UNIQUE (department_name)
);
