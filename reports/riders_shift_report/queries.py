########################################
#  SQL Queries for the report
########################################

SHIFT_DATA = """ SELECT rs.id,h.area_name,rs.started_at ,s.start_at ,s.close_at,CONCAT(au.first_name,'',au.last_name) 
                as name, r.mobile_number ,r.nic , c.name FROM rider_shift rs INNER JOIN shift s ON 
                (rs.shift_id  = s.id) INNER JOIN hotspot h ON (s.hotspot_id = h.id) inner join rider r on 
                rs.rider_id=r.id inner join auth_user au on r.user_id=au.id inner join city c on r.city_id = c.id 
                WHERE (rs.rider_id = '{}' AND s.start_at  BETWEEN '{}' AND '{}'
                AND rs.status IN (0, 1)) """