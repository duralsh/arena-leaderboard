from typing import Any
import psycopg2

class DataBaseDrivers:
    def __init__(self, db_config : dict):
        self.conn = psycopg2.connect(dbname=db_config['dbname'], user=db_config['user'], password=db_config['password'], host=db_config['host'], port=db_config['port'])
    
    def query_buy_weight(self,initial_time) -> list[tuple[Any, ...]]:
        print(f'Querying buy weights...')
        query_time_str = initial_time.strftime('%Y-%m-%d %H:%M:%S')
    
        query = """
        SELECT 
        SUM("Trade2"."amount") AS cnt,
        "Trade2"."traderId",
        "User"."twitterHandle",  
        "User"."twitterPicture",  
        "User"."twitterName"     
        FROM 
        "Trade2"
        JOIN 
        "User" ON "Trade2"."traderId" = "User"."id"
        WHERE 
        "Trade2"."amount" > 0 
        AND "Trade2"."isBuy" = true 
        AND "Trade2"."createdOn" > '2024-3-10 15:09:10'
        GROUP BY 
        "Trade2"."traderId", "User"."twitterHandle", "User"."twitterPicture", "User"."twitterName"  
        ORDER BY 
        cnt DESC;  
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query, (query_time_str,))
            return cur.fetchall()

 

    def get_referrals(self):
        print(f'Querying refferal...')
        query = """
        SELECT * FROM public."Referral"
        ORDER BY id ASC 
        """
        referrals = {}
        with self.conn.cursor() as cur:
            cur.execute(query)
            for record in cur.fetchall():
                referrals[record[2]] = record[3]
        return referrals
    