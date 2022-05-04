########################################
#  SQL Queries for the report
########################################

FORCE_DELIVERABLE_SQL = ''' SELECT o.number as Order_Number,CONCAT(r_user.first_name,r_user.last_name,
                ' (',r.mobile_number,')') as Rider,CONCAT(d_user.first_name, ' ', d_user.last_name) as Deliverer_Name,
                    oi.force_delivered_category_id,oi.force_delivered_description,CONVERT_TZ(o.delivery_time, '+00:00', 
                    '+05:00') as Delivery_Time FROM logistics.order o INNER JOIN logistics.rider r ON o.rider_id = r.id
                    INNER JOIN logistics.auth_user r_user ON r.user_id = r_user.id INNER JOIN
                    logistics.auth_user d_user ON o.force_delivered_by_id = d_user.id INNER JOIN
                    logistics.order_info oi ON o.id = oi.order_id  WHERE o.force_delivered_by_id IS NOT NULL
                     AND DATE(o.delivery_time) between '{}' and '{}';   '''