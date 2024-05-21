LATE_APPLIED_APPROVED_QUERY = """SELECT SUM(leave_days_count) total_count,
        SUM(
            CASE
                WHEN applied_late is true THEN 1
                ELSE 0
            END
        ) as late_applied_leave,
        SUM(
            CASE
                WHEN approved_late is true THEN 1
                ELSE 0
            END
        ) as late_approved_leave,
        SUM(
            CASE
                WHEN applied_late is true
                and status != 'REJECTED' THEN 1
                ELSE 0
            END
        ) late_applied_leave_not_rejected
        from
            final.fact_leaves fl
    JOIN final.dim_date_leaves ddl ON ddl.leave_id = fl.leave_id_sk
    JOIN final.dim_date dd ON dd.date_id = ddl.date_id
    {% if selected_project %}
        JOIN final.dim_allocation_leaves dal ON dal.leave_id = fl.leave_id_sk
        JOIN final.dim_allocations da ON da.id = dal.allocation_id
    {% endif %}
    {% if leave_type %}
        JOIN final.dim_leave_types dlt ON dlt.id = fl.leave_type_id
    {% endif %}
    {% if department %}
        JOIN final.dim_departments dd2 ON dd2.id = fl.department_id
    {% endif %}
WHERE 1 = 1
{% if selected_project %}
    and da.name = {{ selected_project }}
{% endif %}
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
"""
