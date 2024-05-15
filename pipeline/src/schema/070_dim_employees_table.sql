CREATE TABLE IF NOT EXISTS final.dim_employees (
    id SERIAL,
    employee_id VARCHAR(20),
    team_manager_id VARCHAR(20),
    leave_issuer_id VARCHAR(20),
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    middle_name VARCHAR(200),
    email VARCHAR(100),
    is_hr BOOL,
    is_supervisor BOOL,
    CONSTRAINT dim_employee_pk PRIMARY KEY (id),
    CONSTRAINT dim_employee_id_unique UNIQUE (employee_id)
);
