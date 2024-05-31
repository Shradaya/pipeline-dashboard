LATE_APPLIED_APPROVED_QUERY = """SELECT COALESCE(COUNT(leave_days_count), 0) total_count,
        COALESCE(SUM(
            CASE
                WHEN applied_late is true THEN 1
                ELSE 0
            END
        ), 0) as late_applied_leave,
        COALESCE(SUM(
            CASE
                WHEN approved_late is true THEN 1
                ELSE 0
            END
        ), 0) as late_approved_leave,
        COALESCE(SUM(
            CASE
                WHEN applied_late is true
                and status != 'REJECTED' THEN 1
                ELSE 0
            END
        ), 0) late_applied_leave_not_rejected
        from
            final.fact_leaves fl
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
"""
