INSERT INTO final.fact_leaves
    (
        leave_id,
        employee_id,
        designation_id,
        department_id,
        leave_type_id,
        start_date,
        end_date,
        created_at,
        updated_at,
        leave_days_count,
        reason,
        status,
        remarks,
        applied_late,
        approved_late
    )
select
    sd.id as leave_id,
    de.id as employee_id,
    dd.id as designation_id,
    dd2.id as department_id,
    dlt.id as leave_type_id,
    sd.start_date as start_date,
    sd.end_date as end_date,
    sd.created_at as created_at,
    sd.updated_at as updated_at,
    sd.leave_days as leave_days_count,
    sd.reason as reason,
    sd.status as status,
    sd.remarks as remarks,
    case
        when sd.start_date - sd.created_at >= 3
        and sd.leave_days = 1 then false
        when sd.start_date - sd.created_at >= 7
        and sd.leave_days = 2 then false
        when sd.start_date - sd.created_at >= 14
        and sd.leave_days >= 3
        and sd.leave_days <= 5 then false
        when sd.start_date - sd.created_at >= 30
        and sd.leave_days >= 6 then false
        else true
    end as applied_late,
    case
        when sd.status = 'APPROVED' and (dlt.leave_type_name = 'Discretionary' or dlt.leave_type_name = 'Annual')
        and sd.start_date - sd.updated_at >= 3
        and sd.leave_days = 1 then false
        when sd.status = 'APPROVED' and (dlt.leave_type_name = 'Discretionary' or dlt.leave_type_name = 'Annual')
        and sd.start_date - sd.updated_at >= 7
        and sd.leave_days = 2 then false
        when sd.status = 'APPROVED' and (dlt.leave_type_name = 'Discretionary' or dlt.leave_type_name = 'Annual')
        and sd.start_date - sd.updated_at >= 14
        and sd.leave_days >= 3
        and sd.leave_days <= 5 then false
        when sd.status = 'APPROVED' and (dlt.leave_type_name = 'Discretionary' or dlt.leave_type_name = 'Annual')
        and sd.start_date - sd.updated_at >= 30
        and sd.leave_days >= 6 then false
        when sd.status <> 'APPROVED' then false
        else true
    end as approved_late
from
    std.std_data sd
    join final.dim_employees de on sd.emp_id = de.employee_id
    left join final.dim_employees dem on sd.team_manager_id = de.employee_id
    left join final.dim_employees delid on sd.leave_issuer_id = de.employee_id
    left join final.dim_employees declid on sd.current_leave_issuer_id = de.employee_id
    join final.dim_designations dd on sd.designation_id = dd.designation_id
    join final.dim_departments dd2 on sd.department_description = dd2.department_name
    join final.dim_leave_types dlt on sd.leave_type_id = dlt.leave_type_id
ON CONFLICT ON CONSTRAINT fact_leave_id_unique 
DO UPDATE 
SET status = EXCLUDED.status;