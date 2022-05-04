########################################
#  SQL Queries for the report
########################################

RIDER_SHIFT_QUERY = """ SELECT s.id AS ID ,s.start_at ,s.close_at  ,h.area_name AS HOT_SPOT,c.name AS city ,
                    s.riders_required AS RIDER_REQUIRED  
FROM shift s INNER JOIN hotspot h ON (s.hotspot_id = h.id) 
LEFT OUTER JOIN city c ON (h.city_id = c.id) WHERE DATE(CONVERT_TZ(s.start_at , 'UTC', 'UTC')) BETWEEN '{}' AND '{}'
ORDER by s.id  """
