INSERT INTO
    final.dim_allocation_leaves (leave_id, allocation_id)
SELECT
    leave.leave_id_sk,
    da.id
FROM
    (
        SELECT
            fl.leave_id_sk,
            (jsonb_array_elements(sd.allocations) ->> 'name') :: TEXT AS allocation_name
        FROM
            final.fact_leaves fl
            JOIN std.std_data sd ON fl.leave_id = sd.id
    ) leave
JOIN final.dim_allocations da ON leave.allocation_name = da.allocation_name 
ON CONFLICT ON CONSTRAINT dim_allocation_leaves_lookup_unique DO NOTHING;
