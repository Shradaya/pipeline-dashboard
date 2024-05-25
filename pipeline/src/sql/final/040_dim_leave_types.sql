INSERT INTO
    final.dim_leave_types (
        fiscal_id,
        leave_type_id,
        leave_type_name,
        default_days,
        transferable_days
    )
select
    id fiscal_id,
    leave_type_id,
    leave_type_name,
    default_days,
    transferable_days
FROM
    (
        SELECT
            distinct df.id,
            sd.fiscal_start_date,
            leave_type_id::int,
            leave_type_name,
            default_days,
            transferable_days
        FROM
            std.std_data sd
            join final.dim_fiscal df on sd.fiscal_start_date = df.fiscal_start_date
        order by
            sd.fiscal_start_date,
            leave_type_id::int
    ) a ON CONFLICT ON CONSTRAINT dim_leave_type_id_unique DO NOTHING;