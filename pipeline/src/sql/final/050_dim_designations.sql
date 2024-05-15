INSERT INTO final.dim_designations (designation_id, designation_name) 
SELECT DISTINCT
    designation_id,
    designation_name
FROM std.std_data sd
ON CONFLICT ON CONSTRAINT dim_designation_id_unique 
DO NOTHING;
