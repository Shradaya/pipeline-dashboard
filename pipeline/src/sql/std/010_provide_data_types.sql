-- DROP TABLE BEFORE CREATION
DROP TABLE IF EXISTS std.std_data;

-- CREATE NEW TABLE USING THE RAW DATA
CREATE TABLE IF NOT EXISTS std.std_data AS (
    select
        id,
        user_id,
        emp_id,
        team_manager_id,
        designation_id,
        designation_name,
        first_name,
        CASE WHEN middle_name = 'None' THEN null ELSE middle_name END as middle_name,
        last_name,
        CASE WHEN email = 'None' THEN null ELSE email END as email,
        is_hr :: bool,
        is_supervisor :: bool,
        CASE
            WHEN allocations = 'None' THEN null
            when allocations = '' then null
            ELSE REPLACE(
                REPLACE(allocations, '''', '"'),
                'None',
                '"NONE"'
            ) :: jsonb
        END AS allocations,
        leave_issuer_id,
        current_leave_issuer_id,
        leave_issuer_first_name,
        leave_issuer_last_name,
        current_leave_issuer_email,
        department_description,
        start_date :: date,
        end_date :: date,
        leave_days :: int,
        reason,
        status,
        remarks,
        leave_type_id,
        leave_type_name,
        default_days,
        transferable_days,
        is_consecutive,
        fiscal_id,
        fiscal_start_date::date,
        fiscal_end_date::date,
        fiscal_is_current :: bool,
        created_at :: date,
        updated_at :: date,
        case
            when is_converted = '1' then true
            else false
        end
    from
        raw.raw_data rd
);