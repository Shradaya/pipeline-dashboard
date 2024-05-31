LEAVE_BALANCE_QUERY = """
    SELECT
        DISTINCT
        TRIM(CONCAT(de.last_name, ', ', de.first_name, ' ', de.middle_name)) AS full_name,
        leave_type_name,
        CASE
            WHEN available_leave_count <= 0 THEN 0
            ELSE available_leave_count
        END AS available_leave_count,
        CASE
            WHEN available_leave_count <= 0 THEN ABS(remaining_leave_count)
            ELSE available_leave_count - remaining_leave_count
        END AS leaves_taken,
        CASE
            WHEN available_leave_count <= 0 THEN 0
            ELSE remaining_leave_count
        END AS remaining_leave_count
    FROM
        final.calculated_leave_counts clc
    JOIN final.dim_employees de ON
        clc.employee_id = de.id
    JOIN final.fact_leaves fl ON
        fl.employee_id = de.id
    JOIN final.dim_fiscal df ON
        clc.fiscal_id = df.id
    {% if selected_project %}
        JOIN (SELECT leave_id FROM final.dim_allocation_leaves 
        JOIN final.dim_allocations da ON da.id = dal.allocation_id
        WHERE da.name = {{ selected_project }}) dal ON dal.leave_id = fl.leave_id_sk
    {% endif %}
    {% if department %}
        JOIN final.dim_departments dd2 ON dd2.id = fl.department_id
    {% endif %}
    WHERE fl.status not in ['CANCELLED', 'REJECTED']
        {% if fiscal_year %}
            AND df.id = {{ fiscal_year }}
        {% endif %}
        {% if leave_type %}
            AND leave_type_name = {{ leave_type }}
        {% endif %}
        {% if department %}
            and dd2.department_name = {{ department }}
        {% endif %}
    ORDER BY
        full_name
    LIMIT 50;
"""
