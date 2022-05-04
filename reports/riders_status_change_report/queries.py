LOGS_SQL = """SELECT uscl.change_by_id ,CONCAT(au.first_name,'',au.last_name) as agentname ,  au.email,
             au.last_login , r.id,CONCAT(aur.first_name , '' , aur.last_name) as ridername  
            ,uscl.action_type ,uscl.message,uscl.created_at FROM user_status_change_log uscl 
            INNER JOIN auth_user au ON (uscl.change_by_id = au.id)  INNER JOIN rider r ON (uscl.user_id = r.user_id) 
            INNER JOIN auth_user aur ON (aur.id = r.user_id) WHERE uscl.created_at BETWEEN 
            '{}' AND '{}' ORDER BY uscl.created_at DESC
            """