########################################
#  SQL Queries for the report
########################################

RIDER_DATA = """SELECT r.id,CONCAT(au.first_name,'',au.last_name),r.nic,c.name FROM rider r INNER JOIN city c ON 
                (r.city_id = c.id) inner join auth_user au on r.user_id=au.id  WHERE (r.city_id IS NOT NULL AND r.id IN 
                (SELECT rs.rider_id  FROM rider_shift rs INNER JOIN shift s ON (rs.shift_id = s.id)
                inner join rider r2 on rs.rider_id = r2.id inner join city c2 on r2.city_id = c2.id 
                inner join auth_user au2 on r2.user_id = au2.id 
                WHERE s.start_at BETWEEN '{}' AND '{}'))"""

POINT_STATS = """select SUM(CASE  when lph.points and lph.created_at <= '{0}' then lph.points end) 
                as point_balance_before,SUM(case when lph.points and lph.created_at <= '{1}' 
                then lph.points end) as point_balance_end,SUM(case when lph.points  and lph.created_at 
                BETWEEN '{0}' and '{1}' then lph.points end)as point_earned_between_peroid ,
                SUM(CASE when lph.points and lph.log_type="2" and lph.created_at BETWEEN '{0}' and 
                '{1}' then lph.points end)as redeemed_points,
                SUM(CASE when lph.points and lph.log_type IN ("3","4","5","8","11","12") and lph.created_at BETWEEN 
                '{0}' and '{1}' then lph.points end) as penality_points from loyalty_points_history lph where  
                lph.rider_id='{2}' """