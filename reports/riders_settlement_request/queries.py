########################################
#  SQL Queries for the report
########################################

RIDER_SETTLEMENT_SQL = """SELECT sr.created_at, CONCAT(au2.first_name,'',au2.last_name) as rider_name , r.nic, 
                        r.e_wallet_number,CONCAT(au.first_name,'',au.last_name) as agentname, sr.amount , sr.status,sr.source_id  
                        FROM settlement_request sr INNER JOIN rider r ON 
                        (sr.rider_id = r.id) INNER JOIN auth_user au ON (sr.source_id = au.id) inner join auth_user au2
                        on r.user_id = au2.id WHERE (sr.created_at BETWEEN '{}' AND '{}'
                        AND sr.status IN ("IP", "S", "F", "R"))"""