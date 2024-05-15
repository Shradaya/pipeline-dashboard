INSERT INTO final.dim_allocations (allocation_id, name, type_name) 
SELECT DISTINCT
    allocations->>'id' AS id,
    REPLACE(allocations->>'name', '"', '') AS name,
    allocations->>'type' AS type
FROM
    (SELECT jsonb_array_elements(allocations) AS allocations FROM std.std_data sd) AS subquery
ON CONFLICT ON CONSTRAINT dim_allocation_id_unique 
DO NOTHING;
