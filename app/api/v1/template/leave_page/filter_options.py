PROJECT_OPTIONS = """
        SELECT 
            distinct 
            name as label, 
            name as value
        FROM final.dim_allocations;
    """

LEAVE_TYPE_OPTIONS = """
        SELECT 
            distinct 
            leave_type_name as label, 
            leave_type_name as value
        FROM final.dim_leave_types;
    """

DEPARTMENT_OPTIONS = """
            SELECT 
                distinct 
                department_name as label, 
                department_name as value
            FROM final.dim_departments;
        """

DATE_RANGE_OPTIONS = """
            SELECT 
                min(fiscal_start_date) as lower_bound, 
                max(fiscal_end_date) as upper_bound
            FROM final.dim_fiscal;
        """

FISCAL_YEAR_OPTIONS = """
                SELECT 
                    id value,
                    CONCAT('FY', ' (', fiscal_start_date, ') - (', fiscal_end_date, ')') label
                FROM final.dim_fiscal;
            """