########################################
#  SQL Queries for the report
########################################

RIDER_STATS = """SELECT rs.rider_id,CONCAT(au.first_name,'',au.last_name) as ridername ,r.mobile_number,
                rs.total_time ,rs.total_pause_time FROM rider_stats rs
                 INNER JOIN rider r ON (rs.rider_id = r.id) inner join auth_user au on r.user_id=au.id 
                 WHERE rs.created_date = '{}' """

RESUME_TIME = """SELECT rsl.created_at FROM rider_shift_log rsl WHERE (DATE(CONVERT_TZ(rsl.created_at , 'UTC', 'UTC')) = 
                 '{}' AND rsl.rider_id = '{}' AND rsl.log_type = "R")"""

PAUSE_TIME = """SELECT rsl.created_at FROM rider_shift_log rsl WHERE (DATE(CONVERT_TZ(rsl.created_at , 'UTC', 'UTC')) =
                '{}' AND rsl.rider_id = '{}' AND rsl.log_type = "P")"""
