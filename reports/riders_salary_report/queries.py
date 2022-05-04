########################################
#  SQL Queries for the report
########################################


ELIGIBLE_RIDERS_SQL = """SELECT r.id , r.job_model , r.job_type , r.nic , c.name ,r.category,r.cash_in_hand,au.id,
                au.date_joined FROM rider r INNER JOIN city c ON (r.city_id = c.id) INNER JOIN auth_user au ON 
                (r.user_id = au.id) WHERE (r.city_id IS NOT NULL AND r.job_model = 2 AND 
                au.date_joined <= '{}') ORDER BY r.id ASC"""

PICK_UP_DISTANCE_SQL = """select  sum(od.pickup_distance) from `order`o right join rider_earnings re on 
                          o.id=re.order_id  inner join order_distance od on od.order_id = o.id WHERE (re.created_at 
                          BETWEEN '{}' AND '{}') AND re.log_type ='{}' and re.rider_id='{}'"""

RIDER_DROP_OFF_DISTANCE_SQL = """ select sum(od.delivered_distance) from `order`o right join rider_earnings re 
                                  on o.id=re.order_id inner join order_distance od on od.order_id = o.id  
                                  WHERE (re.created_at BETWEEN '{}' AND '{}') AND re.log_type ='{}' and re.rider_id='{}'
                                 """

RIDER_EARNINGS_SQL = """ SELECT  
                        SUM(CASE when re.log_type="PB" then amount  END) as pick_up_distance_bonus ,
                        SUM(CASE when re.log_type="PP" then amount  END) as pick_up_pay ,
                        SUM(CASE when re.log_type="DDP" then amount  END) as drop_off_distance_pay,
                        SUM(CASE when re.log_type="DP" then amount  END) as drop_off_pay,
                        SUM(CASE when re.log_type="DCP" then amount  END) as delivery_charges_based_pay,
                        SUM(CASE when re.log_type="FP" then amount  END) as per_order_pay,
                        SUM(CASE when re.log_type="SBP" then amount  END) as slab_based_pay,
                        SUM(CASE when re.log_type="TP" then amount  END) as tip_pay,

                        COUNT(case when re.log_type="PP" then order_id  END) total_pick_ups,
                        COUNT(case when re.log_type="DP" then order_id  END) total_drop_offs,
                        COUNT(case when re.log_type="FP" then order_id  END) total_per_order_pays,
                        COUNT(case when re.log_type="SBP" then order_id  END) total_slab_based_pays,
                        SUM(CASE when re.log_type="LNB" then amount  END) as total_late_night_bonus_pay
                        from rider_earnings re  where re.created_at BETWEEN '{}' AND '{}' AND re.rider_id ='{}' """

RIDER_EARNING_BY_CATEGORY_SQL = """select 
                                   SUM(CASE when o.category="food" then amount  END) as food,
                                   SUM(CASE when o.category="healthcare" then amount  END) as healthcare,
                                   SUM(CASE when o.category="errand" then amount END) as errand,
                                   SUM(CASE when o.category="books" then amount  END) as books,
                                   SUM(CASE when o.category="beauty" then amount  END) as beauty,
                                   SUM(CASE when o.category="babycare" then amount  END) as babycare,
                                   SUM(CASE when o.category="pantry" then amount  END) as pantry,
                                   SUM(CASE when o.category="pharma" then amount  END) as pharma,
                                   SUM(CASE when o.category="tiffin" then amount  END) as tiffin,
                                   SUM(CASE when o.category="xoom" then amount  END) as xoom
                                   from  rider_earnings re  right join `order` o on re.order_id =  o.id 
                                   WHERE  re.created_at BETWEEN '{}' AND '{}' AND re.rider_id ='{}' """

RIDER_PENALTY_SQL = """select SUM(rp.updated_amount) , COUNT(id) as total_penalty  
                       from rider_penalty rp WHERE rp.created_date BETWEEN  '{}' AND '{}' AND rp.rider_id ='{}'  """

RIDER_BONUS_SQL = """select SUM(bonus_amount) as total_bonus from rider_referral_bonus_log rrbl WHERE 
                     rrbl .created_at BETWEEN  '{}' AND '{}' AND rrbl.referred_by_id ='{}' """

EARNINGS_STATS_SQL = """select SUM(total_time) as total_time ,
                        SUM(total_pause_time) as total_pause_time,
                        SUM(total_problem_time)  as total_problem_time,
                        SUM(total_shift_hours)  as total_shift_hours,
                        SUM(total_over_time)  as total_over_time,
                        SUM(over_time_pay)  as over_time_pay ,
                        SUM(pay)  as total_pay
                        from rider_earnings_stats res inner join rider_shift rs on  res.rider_shift_id = rs.id 
                        where    rs.rider_id = '{}' AND rs.started_at BETWEEN '{}'AND '{}' """

CITY_CONFIGURATIONS_INSTANCE_SQL = """ select cc.hourly_pay_min_app_on_time from city_configuration cc where cc.id =1
               """

RIDER_ORDER_STATS_SQL = """ select COUNT(os.id) as total_orders,
                                COUNT(  os.picked_up_at )  as total_picked_up_orders,
                                COUNT(  os.delivered_at )  as delivered_orders
                                from order_state os inner join `order` o on os.order_id = o.id WHERE (os.assigned_at 
                                BETWEEN '{}' AND '{}'
                                AND o.status in ("Delivered", "Cancelled", "Failed", "Invalid") AND os.rider_id='{}' )"""

RIDER_NON_PAID_FUEL_EARNINGS_SQL = """SELECT SUM(re.amount) as pick_up_and_drop_off_as_fuel_pay FROM rider_earnings re 
                                      WHERE ((re.log_type = "PB" OR re.log_type = "DDP") AND re.is_fuel_paid = False AND 
                                      re.rider_id = '{}') """

ORDER_IDS_SQL = """SELECT re.order_id FROM rider_earnings re WHERE ((re.log_type = "PB" OR re.log_type = "DDP") 
                   AND re.is_fuel_paid = False AND re.rider_id = '{}')"""

RIDER_ORDER_DATES_STATS_SQL = """SELECT COUNT(os.id) as total_orders,
                             Count(CASE WHEN os.picked_up_at IS NOT NULL THEN os.id END) as total_picked_up_orders,
                             Count(CASE WHEN os.delivered_at IS NOT NULL THEN os.id END) as total_delivered_orders
                             from order_state os where (DATE(CONVERT_TZ ( os.assigned_at ,'UTC'  , 'UTC' )) IN {} )
                             AND os.rider_id = '{}' """

RIDER_ORDER_ACCEPT_STATS_SQL = """select COUNT(rarl.id) as total_orders,
                              COUNT(CASE when rarl.log_type="A" then rarl.id end) as accepted_orders,
                              COUNT(CASE when rarl.log_type="R" then rarl.id end) as rejected_orders
                              FROM rider_accept_reject_log rarl where rarl.created_at BETWEEN 
                              '{}' AND '{}' AND rarl .rider_id ='{}' """

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

LOYALTY_BONUS_SQL = """SELECT SUM(ROUND((ro.points) * (ro.value_per_point) )) as loyalty_bouns FROM redemption_request 
                        rr, redemption_option ro  WHERE (rr.rider_id = '{}' AND rr.status = "A" AND rr.updated_at 
                        BETWEEN '{}' AND '{}') """

CERTIFICATE_BONUS_SQL = """SELECT  c.id  ,rc.is_paid,rc.amount_to_pay,c.eligible_after_hours,c.created_at FROM 
                            rider_certificate rc inner join certification c on rc.certificate_id =c.id WHERE 
                            ((rc.created_at BETWEEN '{0}' 
                            AND '{1}' OR rc.paid_at BETWEEN '{0}' AND '{1}') 
                            AND rc.rider_id = '{2}' AND rc.is_active = True) """

PREVIOUS_PAID_SQL = """SELECT  c.id  ,rc.is_paid,rc.amount_to_pay,c.eligible_after_hours,c.created_at FROM 
                        rider_certificate rc inner join certification c on 
                        rc.certificate_id =c.id WHERE ((rc.created_at BETWEEN '{0}' 
                        AND '{1}' OR rc.paid_at BETWEEN '{0}' AND '{1}') 
                        AND rc.rider_id = '{2}' AND rc.is_active = True AND rc.is_paid = TRUE)"""

GET_PAID_FALSE_SQL = """SELECT c.id  ,rc.is_paid,rc.amount_to_pay,c.eligible_after_hours,c.created_at
                        FROM rider_certificate rc inner join certification c on 
                        rc.certificate_id =c.id WHERE ((rc.created_at BETWEEN '{0}' 
                        AND '{1}' OR rc.paid_at BETWEEN '{0}' AND '{1}') 
                        AND rc.rider_id = '{2}' AND rc.is_active = True AND rc.is_paid = FALSE)"""

GET_UPDATE_VALUE_SQL = """UPDATE rider_certificate 
                    SET rider_certificate.is_paid = TRUE , rider_certificate.paid_at = '{3}'
                    WHERE ((rider_certificate.created_at BETWEEN '{0}' 
                    AND '{1}' OR rider_certificate.paid_at BETWEEN '{0}' AND 
                    '{1}') AND rider_certificate.rider_id = '{2}' AND rider_certificate.is_active = True) 
                    """

RIDER_SECURITY_SQL = """ SELECT rsdl.security_deposit,rsdl.month ,rsdl.year  from rider_security_deposit_log rsdl 
                        WHERE rsdl.rider_id = '{}' """

RIDER_SECURITY_DEPOSIT_SQL = """INSERT INTO rider_security_deposit (rider_id, type , amount)
                                VALUES ('{}','{}','{}')"""

GET_RIDER_CERTIFICATE_SQL = """SELECT MIN(rc.updated_at) as certificate_issue_date  FROM rider_certificate rc 
                            WHERE (rc.is_active = True AND rc.rider_id = '{}')"""

GET_INSTANCE_SQL = """select lc.security_deposit from logistics_configuration lc where lc.id =1 """

GET_PENALTY_FAILED_ORDERS = """SELECT sum(o.price) FROM order_state os INNER JOIN `order` o ON (os.order_id = o.id) 
                            INNER JOIN order_info oi ON (o.id = oi.order_id) WHERE (os.assigned_at BETWEEN '{}' AND '{}' 
                            AND oi.edit_reason IN ("Rider not responding", 
                            "Rider Refusal due to Bike/Mobile Malfunction", "Rider Refusal due to customer wrong location", 
                            "Rider Refusal due to Emergency/Urgent work at home", "Rider Refusal due to Long Drop off", 
                            "Rider Refusal due to Long Pick up"," Rider Refusal due to Multitasking",
                            "Rider Refusal due to Out of Zone", "Rider Refusal due to Security Issue", 
                            "Rider refusal due to shift ended","Rider Refusal due to Unstable Health Condition", 
                            "Rider Refusal due to Weather Condition", "Rider refused to work with us",
                            "Unable to find customer location") AND o.rider_id = '{}' AND o.status = "Failed")"""

GET_LOGISTICS_INSTANCE = """select lc.insurance_pay_per_month from logistics_configuration lc where lc.id =1"""

GET_USER_LOGS = """SELECT uscl.action_type , DATE(CONVERT_TZ(uscl.created_at , 'UTC', 'UTC'))
                    FROM user_status_change_log uscl WHERE (uscl.action_type  IN ("Active", "Inactive") AND 
                    uscl.user_id = '{}') ORDER BY uscl.id ASC """
