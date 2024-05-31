HIGHEST_LEAVE_COUNT_QUERY = """
SELECT
	TRIM(CONCAT(de.last_name, ', ', de.first_name, ' ', de.middle_name)) full_name,
	COUNT(*) leave_count
FROM
	final.fact_leaves fl
    join final.dim_employees de on
        fl.employee_id = de.id
    JOIN final.dim_date_leaves ddl ON ddl.leave_id = fl.leave_id_sk
    JOIN final.dim_date dd ON dd.date_id = ddl.date_id
    {% if selected_project %}
        JOIN (SELECT leave_id FROM final.dim_allocation_leaves 
        JOIN final.dim_allocations da ON da.id = dal.allocation_id
        WHERE da.name = {{ selected_project }}) dal ON dal.leave_id = fl.leave_id_sk
    {% endif %}
    {% if leave_type %}
        JOIN final.dim_leave_types dlt ON dlt.id = fl.leave_type_id
    {% endif %}
    {% if department %}
        JOIN final.dim_departments dd2 ON dd2.id = fl.department_id
    {% endif %}
WHERE fl.status not in ['CANCELLED', 'REJECTED']
{% if leave_type %}
    and dlt.leave_type_name = {{ leave_type }}
{% endif %}
{% if department %}
    and dd2.department_name = {{ department }}
{% endif %}
{% if start_date %}
    and dd.date_value >= {{ start_date }}
{% endif %}
{% if end_date %}
    and dd.date_value <= {{ end_date }}
{% endif %}
GROUP BY
	de.first_name,
	de.last_name,
	de.middle_name
HAVING COUNT(leave_days_count) > 0 and COUNT(leave_days_count) is not null
ORDER BY
	leave_count desc
"""