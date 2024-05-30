LEAVE_COUNT_PER_WEEKDAY_QUERY = """SELECT
    CASE 
        WHEN dd.day_of_week = 2 THEN 'Monday'
        WHEN dd.day_of_week = 3 THEN 'Tuesday'
        WHEN dd.day_of_week = 4 THEN 'Wednesday'
        WHEN dd.day_of_week = 5 THEN 'Thursday'
        WHEN dd.day_of_week = 6 THEN 'Friday'
    END day_of_week,
    COUNT(*)
FROM
    final.fact_leaves fl
    JOIN final.dim_date_leaves ddl ON ddl.leave_id = fl.leave_id_sk
    JOIN final.dim_date dd ON dd.date_id = ddl.date_id
    {% if selected_project %}
        JOIN (SELECT leave_id FROM final.dim_allocation_leaves dal
            JOIN final.dim_allocations da ON da.id = dal.allocation_id 
            WHERE da.name = {{ selected_project }}) dal
        ON dal.leave_id = fl.leave_id_sk
    {% endif %}
    {% if leave_type %}
        JOIN final.dim_leave_types dlt ON dlt.id = fl.leave_type_id
    {% endif %}
    {% if department %}
        JOIN final.dim_departments dd2 ON dd2.id = fl.department_id
    {% endif %}
WHERE 1 = 1 
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
    dd.day_of_week;
"""
