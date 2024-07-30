from dotenv import load_dotenv
import psycopg2
import os
load_dotenv()



def get_areas() -> list[tuple]:
    conn = psycopg2.connect(os.environ['POSTGRESQL_TOKEN'])
    with conn:
        with conn.cursor() as cursor:
            sql ='''
            select * from dash_web;
            '''

            cursor.execute(sql)
            return cursor.fetchall()
    conn.close()

def get_snaOfArea(area:str) -> list[tuple]:
    conn = psycopg2.connect(os.environ['POSTGRESQL_TOKEN'])
    with conn:
        with conn.cursor() as cursor:
            sql ='''
            站名 VARCHAR(20),
	        平均氣溫 VARCHAR(20),
	        絕對最高氣溫 VARCHAR(20),
	        絕對最低氣溫 VARCHAR(40),
	        總日照時數h VARCHAR(20),
	        總日射量MJ/m2 VARCHAR(200),
	        Year VARCHAR(20),
	        Month VARCHAR(20),
            行政區 VARCHAR(20),
            )
            '''

            cursor.execute(sql,(area,))
            return cursor.fetchall()
    conn.close()
