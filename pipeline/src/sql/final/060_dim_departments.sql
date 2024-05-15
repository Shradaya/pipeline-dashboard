INSERT INTO final.dim_departments (department_name) 
SELECT DISTINCT
    department_description
FROM std.std_data sd
ON CONFLICT ON CONSTRAINT dim_department_name_unique 
DO NOTHING;
