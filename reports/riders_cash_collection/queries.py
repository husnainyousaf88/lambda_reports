########################################
#  SQL Queries for the report
########################################

JAZZ_CASH_COLLECTION_SQL = """SELECT r.id, jccl.rider_cash_id, jccl.actual_receivables ,rc.created_at,r.nic , 
                        CONCAT(au.first_name, ' ' , au.last_name) RiderName, c.name,jccl.auth_id ,rc.amount  
                        FROM jazz_cash_collection_log jccl  INNER JOIN rider_cash rc ON (jccl.rider_cash_id = rc.id) 
                        INNER JOIN rider r ON (rc.rider_id = r.id) INNER join auth_user au on (r.user_id=au.id) 
                        INNER join city c on (r.city_id=c.id)
                        WHERE (rc.created_at BETWEEN '{}' AND '{}' 
                        AND r.city_id IS NOT NULL) ORDER BY rc.created_at DESC """

RIDER_CASH_SQL = """SELECT rc.id FROM rider_cash rc WHERE (rc.id < '{}' AND rc.payment_type = "JC" 
                AND rc.rider_id = '{}' AND rc.source = "Jazz Cash" 
                AND rc.trans_type = "d") ORDER BY rc.created_at DESC limit 1"""

RIDER_CASH_ID_SQL = """select rc.id from rider_cash rc  where (rc.id > '{}' and rc.id <='{}' and rc.rider_id ='{}'
                        and rc.trans_type="d") ORDER by rc.id DESC"""

RIDER_CASH_IDS_SQL = """select rc.id from rider_cash rc  where ( rc.id <='{}' and rc.rider_id ='{}' and 
                        rc.trans_type="d") ORDER by rc.id DESC """

RIDER_FUEL_EARNING_SQL = """SELECT rfeal.order_ids FROM rider_fuel_earning_adjusted_log rfeal WHERE rfeal.rider_cash_id 
                            IN (SELECT rc.id FROM rider_cash rc WHERE (rc.id <= '{}' AND rc.rider_id = '{}' AND 
                            rc.trans_type = "d"))"""


PICK_UP_DISTANCE_SQL = """SELECT SUM(od.pickup_distance) as pickup_dist FROM rider_earnings re LEFT join `order` o on 
                          re.order_id = o.id INNER JOIN order_distance od on o.id = od.order_id 
                          WHERE (re.rider_id='{}' and re.order_id IN {} AND re.log_type = "PB")  """

DELIVERED_DISTANCE_SQL = """SELECT SUM(od.delivered_distance)  FROM rider_earnings re LEFT join `order` o on 
                            re.order_id = o.id INNER JOIN order_distance od on o.id = od.order_id WHERE 
                            (re.rider_id='{}' and re.order_id IN {} AND re.log_type = "DDP") """

RIDERS_EARNING_SQL = """SELECT SUM(CASE when re.log_type="PB" then re.amount  END) as pick_up_distance_bonus ,
                        SUM(CASE when re.log_type="DDP" then re.amount  END) as drop_off_distance_pay
                        FROM rider_earnings re   WHERE re.rider_id ='{}' AND re.order_id IN {} """
