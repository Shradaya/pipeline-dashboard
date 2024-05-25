CREATE OR REPLACE PROCEDURE final.calculate_available_leave_counts()
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
    prev_available_leave_count INT;
	prev_remaining_leave_count INT;
BEGIN
    CREATE TABLE IF NOT EXISTS final.calculated_leave_counts (
        employee_id INT,
        fiscal_id INT,
        leave_type_name VARCHAR(100),
        available_leave_count INT,
        remaining_leave_count INT
    );
   TRUNCATE final.calculated_leave_counts;

    FOR rec IN 
        SELECT
			fl.employee_id,
			dd.fiscal_id,
			dlt.leave_type_name,
			max(dlt.default_days) default_leave_count_for_fiscal,
			max(dlt.transferable_days) transferable_leave_count,
			max(fl.leave_days_count) as leaves_taken
		FROM
			final.fact_leaves fl
		JOIN final.dim_date_leaves ddl ON
			fl.leave_id_sk = ddl.leave_id
		JOIN final.dim_date dd ON
			dd.date_id = ddl.date_id
		JOIN final.dim_leave_types dlt ON
			fl.leave_type_id = dlt.id
		WHERE
			fl.status <> 'CANCELLED'
			and fl.status <> 'REJECTED'
		GROUP BY
			fl.employee_id,
			dd.fiscal_id,
			dlt.leave_type_name order by  employee_id, leave_type_name, fiscal_id
    LOOP
        IF rec.fiscal_id = 1 THEN
            prev_available_leave_count := rec.default_leave_count_for_fiscal;
           	prev_remaining_leave_count := rec.default_leave_count_for_fiscal - rec.leaves_taken;
        ELSE
            IF rec.leave_type_name = 'Sick' THEN
                IF EXISTS (
                    SELECT 1 
                    FROM final.calculated_leave_counts 
                    WHERE employee_id = rec.employee_id 
                        AND fiscal_id = rec.fiscal_id - 1 
                        AND leave_type_name = 'Annual'
                ) THEN
                    SELECT available_leave_count, remaining_leave_count
                    INTO prev_available_leave_count, prev_remaining_leave_count
                    FROM final.calculated_leave_counts
                    WHERE employee_id = rec.employee_id
                        AND leave_type_name = 'Annual'
                        AND fiscal_id = rec.fiscal_id - 1;
                    
                    prev_available_leave_count := prev_available_leave_count + LEAST(prev_remaining_leave_count, rec.transferable_leave_count);
                    prev_remaining_leave_count := prev_available_leave_count - rec.leaves_taken;
                ELSE
                    SELECT available_leave_count, remaining_leave_count
                    INTO prev_available_leave_count, prev_remaining_leave_count
                    FROM final.calculated_leave_counts
                    WHERE employee_id = rec.employee_id
                        AND leave_type_name = rec.leave_type_name
                        AND fiscal_id = rec.fiscal_id - 1;
                    
                    prev_available_leave_count := prev_available_leave_count + LEAST(prev_remaining_leave_count, rec.transferable_leave_count);
                    prev_remaining_leave_count := prev_available_leave_count - rec.leaves_taken;
                END IF;
            ELSE
                SELECT available_leave_count, remaining_leave_count
                INTO prev_available_leave_count, prev_remaining_leave_count
                FROM final.calculated_leave_counts
                WHERE employee_id = rec.employee_id
                    AND leave_type_name = rec.leave_type_name
                    AND fiscal_id = rec.fiscal_id - 1;
                
                prev_available_leave_count := prev_available_leave_count + LEAST(prev_remaining_leave_count, rec.transferable_leave_count);
                prev_remaining_leave_count := prev_available_leave_count - rec.leaves_taken;
            END IF;
        END IF;

        IF prev_available_leave_count IS NOT NULL OR prev_remaining_leave_count IS NOT NULL THEN
            INSERT INTO final.calculated_leave_counts (employee_id, fiscal_id, leave_type_name, available_leave_count, remaining_leave_count)
            VALUES (rec.employee_id, rec.fiscal_id, rec.leave_type_name, prev_available_leave_count, prev_remaining_leave_count);
        END IF;
    END LOOP;
END;
$$;

CALL final.calculate_available_leave_counts();