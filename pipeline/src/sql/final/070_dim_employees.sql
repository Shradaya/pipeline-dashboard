INSERT INTO final.dim_employees (employee_id, team_manager_id, leave_issuer_id, first_name, last_name, middle_name, email, is_hr, is_supervisor) 
SELECT DISTINCT
    emp_id,
    team_manager_id,
    leave_issuer_id,
    first_name,
    last_name,
    middle_name,
    email,
    is_hr,
    is_supervisor
    FROM std.std_data sd
ON CONFLICT ON CONSTRAINT dim_employee_id_unique 
DO NOTHING;

INSERT INTO final.dim_employees (employee_id, team_manager_id, leave_issuer_id, first_name, last_name, middle_name, email, is_hr, is_supervisor) 
SELECT DISTINCT
    current_leave_issuer_id,
    null,
    null,
    leave_issuer_first_name,
    leave_issuer_last_name,
    null,
    current_leave_issuer_email,
    false,
    false
    FROM std.std_data sd
ON CONFLICT ON CONSTRAINT dim_employee_id_unique 
DO NOTHING;

