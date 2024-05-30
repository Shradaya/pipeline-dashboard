CREATE TABLE IF NOT EXISTS std.std_data (
	id varchar(255) NOT NULL,
	user_id varchar(255) NULL,
	emp_id varchar(255) NULL,
	team_manager_id varchar(255) NULL,
	designation_id varchar(255) NULL,
	designation_name varchar(255) NULL,
	first_name varchar(255) NULL,
	middle_name varchar NULL,
	last_name varchar(255) NULL,
	email varchar NULL,
	is_hr bool NULL,
	is_supervisor bool NULL,
	allocations jsonb NULL,
	leave_issuer_id varchar(255) NULL,
	current_leave_issuer_id varchar(255) NULL,
	leave_issuer_first_name varchar(255) NULL,
	leave_issuer_last_name varchar(255) NULL,
	current_leave_issuer_email varchar(255) NULL,
	department_description varchar(255) NULL,
	start_date date NULL,
	end_date date NULL,
	leave_days int4 NULL,
	reason text NULL,
	status varchar(255) NULL,
	remarks text NULL,
	leave_type_id varchar(255) NULL,
	leave_type_name varchar(255) NULL,
	default_days int4 NULL,
	transferable_days int4 NULL,
	is_consecutive varchar(255) NULL,
	fiscal_id varchar(255) NULL,
	fiscal_start_date date NULL,
	fiscal_end_date date NULL,
	fiscal_is_current bool NULL,
	created_at date NULL,
	updated_at date NULL,
	"case" bool NULL,
    CONSTRAINT std_api_data_uk UNIQUE (id)
);