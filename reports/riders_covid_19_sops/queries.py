########################################
#  SQL Queries for the report
########################################

RIDER_DETAIL = """ SELECT o.`number`,o.rider_id ,r.nic,CONCAT(au.first_name,'',au.last_name),r.mobile_number , 
                sl.has_mask , sl.has_gloves ,sl.has_social_distance ,sl.has_delivery_bag 
                FROM sops_log sl INNER JOIN `order` o ON (sl.order_id = o.id) LEFT OUTER JOIN 
                rider r ON (o.rider_id = r.id) LEFT OUTER JOIN auth_user au ON (r.user_id = au.id) 
                WHERE sl.created_at BETWEEN '{}' AND '{}' """