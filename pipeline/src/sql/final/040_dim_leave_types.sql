INSERT INTO final.dim_leave_types (leave_type_id, leave_type_name, default_days, transferable_days) 
SELECT DISTINCT
    leave_type_id,
    leave_type_name,
    default_days,
    transferable_days
FROM std.std_data sd
ON CONFLICT ON CONSTRAINT dim_leave_type_id_unique 
DO NOTHING;
