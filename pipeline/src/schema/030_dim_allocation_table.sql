CREATE TABLE IF NOT EXISTS final.dim_allocations (
    id SERIAL,
    allocation_id VARCHAR(10),
    name VARCHAR(100),
    type_name VARCHAR(100),
    CONSTRAINT dim_allocation_pk PRIMARY KEY (id),
    CONSTRAINT dim_allocation_id_unique UNIQUE (allocation_id)
);
