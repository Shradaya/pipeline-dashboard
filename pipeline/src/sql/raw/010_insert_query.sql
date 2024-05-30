INSERT INTO raw.raw_data (
    id,
    user_id,
    emp_id,
    team_manager_id,
    designation_id,
    designation_name,
    first_name,
    middle_name,
    last_name,
    email,
    is_hr,
    is_supervisor,
    allocations,
    leave_issuer_id,
    current_leave_issuer_id,
    leave_issuer_first_name,
    leave_issuer_last_name,
    current_leave_issuer_email,
    department_description,
    start_date,
    end_date,
    leave_days,
    reason,
    status,
    remarks,
    leave_type_id,
    leave_type_name,
    default_days,
    transferable_days,
    is_consecutive,
    fiscal_id,
    fiscal_start_date,
    fiscal_end_date,
    fiscal_is_current,
    created_at,
    updated_at,
    is_converted
)
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
)
ON CONFLICT ON CONSTRAINT raw_api_data_pk 
DO UPDATE 
SET status = EXCLUDED.status,
updated_at = EXCLUDED.updated_at;

UPDATE raw.raw_data SET transferable_days = '8' WHERE leave_type_name = 'Sick' AND fiscal_id::INT >= 102;
