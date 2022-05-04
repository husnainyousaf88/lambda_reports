########################################
#  SQL Queries for the report
########################################

INSURANCE_DATA_SQL = """SELECT ri.rider_id , MAX(ri.id) AS id FROM rider_insurance ri WHERE ri.created_at 
                        BETWEEN '{}' AND '{}' GROUP BY ri.rider_id ORDER BY NULL """

RIDER_INSURANCE_SQL = """SELECT r.nic,CONCAT(au.first_name,'',au.last_name) as rider_name,c.name,ri.effective_date,ri.churn_date from rider_insurance ri inner join rider r on ri.rider_id = r.id inner join auth_user au on r.user_id = au.id 
                        inner join city c on r.city_id = c.id WHERE ri.id in ('{}')"""