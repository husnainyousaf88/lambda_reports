########################################
#  SQL Queries for the report
########################################

ELIGIBLE_RIDERS_SQL = """ SELECT r.id,CONCAT(au.first_name,'',au.last_name) as rider_name,r.nic,r.mobile_number ,c.name
                         FROM rider r LEFT OUTER JOIN city c ON (r.city_id = c.id) inner join auth_user au on r.user_id = au .id
                        WHERE r.id IN (SELECT rs.rider_id  FROM rider_shift rs INNER JOIN 
                        shift s ON (rs.shift_id = s.id) WHERE s.start_at BETWEEN '{}' AND 
                        '{}') """

ORDER_STATE_SQL = """SELECT COUNT(os.id) as total_orders ,
                    COUNT(CASE when os.id and os.picked_up_at is not null then os.id end) as total_picked_up_orders,
                    COUNT(CASE when os.id and os.delivered_at is not null then os.id end) as delivered_orders
                    FROM order_state os INNER JOIN `order` o ON (os.order_id = o.id) WHERE 
                    (os.assigned_at BETWEEN '{}' AND '{}' AND
                    o.status IN ("Delivered", "Cancelled", "Failed", "Invalid") AND os.rider_id = '{}')"""

RIDER_ON_TIME_DELIVERY_STATS_SQL = """select COUNT(o.id)  from order_state os inner join `order` o ON 
                                       os.order_id = o.id inner join algo_order_times aot on o.id =aot.order_id 
                                       WHERE (os.arrived_for_delivery_at <= (CASE WHEN aot.delivery_time_after_pickup 
                                       IS NOT NULL THEN aot.delivery_time_after_pickup 
                                       WHEN aot.delivery_time_after_pickup IS NULL THEN aot.delivery_time ELSE NULL END) 
                                       AND os.assigned_at BETWEEN '{}' AND '{}' AND os.delivered_at IS NOT NULL AND 
                                       o.status = "Delivered" AND os.rider_id = '{}')"""

RIDER_ON_TIME_PICKUP_STATS_SQL = """select COUNT(os.id)  from order_state os inner join `order` o ON os.order_id = o.id 
                                    inner join algo_order_times aot on o.id =aot.order_id 
                                    WHERE  (os.arrived_at <= (aot.rider_arrival_time) AND 
                                    os.assigned_at BETWEEN '{}' AND '{}' AND o.status IN 
                                    ("Delivered", "Cancelled", "Failed", "Invalid") AND os.picked_up_at IS NOT NULL AND
                                     os.rider_id = '{}') """
