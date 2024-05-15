INSERT INTO final.dim_leave_types (leave_type_id, leave_type_name) 
SELECT DISTINCT
    leave_type_id,
    leave_type_name
FROM std.std_data sd
ON CONFLICT ON CONSTRAINT dim_leave_type_id_unique 
DO NOTHING;
