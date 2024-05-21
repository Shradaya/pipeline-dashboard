CREATE TABLE IF NOT EXISTS final.fact_leaves (
    leave_id_sk SERIAL,
    leave_id VARCHAR(50),
    employee_id INT,
    designation_id INT,
    department_id INT,
    leave_type_id INT,
    start_date DATE,
    end_date DATE,
    created_at DATE,
    updated_at DATE,
    leave_days_count INT,
    reason TEXT,
    status VARCHAR(100),
    remarks TEXT,
    applied_late BOOL,
    approved_late BOOL,
    CONSTRAINT final_leave_pk PRIMARY KEY (leave_id_sk),
    CONSTRAINT fact_leave_id_unique UNIQUE (leave_id),
    CONSTRAINT fk_dim_employee FOREIGN KEY (employee_id) REFERENCES final.dim_employees(id),
    CONSTRAINT fk_dim_designation FOREIGN KEY (designation_id) REFERENCES final.dim_designations(id),
    CONSTRAINT fk_dim_department FOREIGN KEY (department_id) REFERENCES final.dim_departments(id),
    CONSTRAINT fk_dim_leave_type FOREIGN KEY (leave_type_id) REFERENCES final.dim_leave_types(id)
);