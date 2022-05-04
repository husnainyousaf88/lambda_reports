########################################
#  SQL Queries for the report
########################################

RIDER_DETAIL = """ SELECT r.id, CONCAT(au.first_name,'',au.last_name) as rider_name ,r.nic ,r.mobile_number ,r.referred_by_id ,r2.id, r2.nic,
                    au.is_active ,r.e_wallet_type ,r.e_wallet_number ,au.date_joined ,r.address ,c.name ,MIN(os2.assigned_at)
                     AS first_order_assigned_at, MIN(os2.picked_up_at) AS first_order_picked_up_at,MIN(os2.delivered_at) 
                     AS first_order_delivered_at,MAX(os2.delivered_at) AS last_order_delivered_at ,
                    (SELECT o.`number` FROM order_state os LEFT OUTER JOIN `order` o 
                    ON (os.order_id = o.id) WHERE os.rider_id = (r.id) ORDER BY os.delivered_at ASC  LIMIT 1) 
                    AS first_delivered_order_num FROM rider r LEFT OUTER JOIN order_state os2 ON (r.id = os2.rider_id) 
                    INNER JOIN auth_user au ON (r.user_id = au.id) LEFT OUTER JOIN city c ON 
                    (r.city_id = c.id) LEFT OUTER JOIN rider r2 ON (r.referred_by_id = r2.id) where r.e_wallet_type = '{}'
                    GROUP BY r.id ORDER BY NULL """