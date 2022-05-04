########################################
#  SQL Queries for the report
########################################

ELIGIBLE_RIDERS_SQL = """ SELECT r.id, r.cash_in_hand,CONCAT(au.first_name,'',au.last_name) as ridername ,c.name,
                        r.mobile_number ,r.nic FROM rider r INNER JOIN city c ON (r.city_id = c.id) INNER JOIN 
                        auth_user au ON (r.user_id = au.id) WHERE (r.cash_in_hand > 0.0 AND r.city_id IS NOT NULL AND 
                        au.is_active = True) """

SETTLEMENT_SQL = """SELECT rc.created_at FROM rider_cash rc 
                    WHERE (DATE(CONVERT_TZ(rc.created_at , 'UTC', 'UTC')) <= '{}' AND rc.log_type 
                    IN (4, 5) AND rc.rider_id = '{}') ORDER BY rc.id DESC limit 1 """

LOGISTICS_CONFIGURATION_SQL = """select lc.enforce_fuel_deduction_date from logistics_configuration lc """

RIDER_CASH_SUM_SQL = """SELECT sum(case when rc.trans_type = 'c' then amount  end) as trans_type_c,
                        sum(case when rc.trans_type = 'd' then amount  end) as trans_type_d
                        FROM rider_cash rc WHERE (DATE(CONVERT_TZ(rc.created_at , 'UTC', 'UTC')) > '{}'
                        AND rc.log_type IN (1, 2, 3) AND rc.rider_id = '{}') """

EQUIPMENT_COST_SQL = """SELECT sum(rel.cost) as amount FROM rider_equipment_log rel WHERE (rel.created_at 
                                BETWEEN '{}' AND '{}' AND rel.rider_id = '{}')"""

PICK_UP_DISTANCE_SQL = """select  sum(od.pickup_distance) from `order`o right join rider_earnings re 
                          on o.id=re.order_id inner join order_distance od on od.order_id = o.id  WHERE (re.created_at 
                          BETWEEN '{}' AND '{}') AND re.log_type ='{}' and re.rider_id='{}'
                          """

DROP_OFF_DISTANCE_SQL = """ select sum(od.delivered_distance) from `order`o right join rider_earnings re on 
                                o.id=re.order_id inner join order_distance od on od.order_id = o.id  WHERE 
                                (re.created_at BETWEEN '{}' AND '{}') AND re.log_type ='{}' and re.rider_id='{}' """

RIDER_EARNING_SQL = """SELECT  
                        SUM(CASE when re.log_type="PB" then amount  END) as pick_up_distance_bonus ,
                        SUM(CASE when re.log_type="DDP" then amount  END) as drop_off_distance_pay
                        from rider_earnings re  where re.created_at BETWEEN '{}' AND '{}' AND re.rider_id ='{}' """