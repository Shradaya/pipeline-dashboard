CREATE TABLE IF NOT EXISTS final.dim_allocation_leaves (
    leave_id INT,
    allocation_id INT,
    CONSTRAINT fk_dim_al_leave FOREIGN KEY (leave_id) REFERENCES final.fact_leaves(leave_id_sk),
    CONSTRAINT fk_dim_al_allocation FOREIGN KEY (allocation_id) REFERENCES final.dim_allocations(id),
    CONSTRAINT dim_allocation_leaves_lookup_unique UNIQUE (leave_id, allocation_id)
);
