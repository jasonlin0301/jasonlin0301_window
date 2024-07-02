import psycopg2
import data

def main():
    try:
        conn = psycopg2.connect("postgresql://tvdi_postgresql_etik_user:M0pQwAscutSJOVqMbHc2KNpD7bdprn2i@dpg-cpscveaj1k6c738l7of0-a.singapore-postgres.render.com/tvdi_postgresql_etik")
        
        # 創建表格 youbike（如果不存在）
        with conn:
            with conn.cursor() as cursor:
                sql = '''
                CREATE TABLE IF NOT EXISTS youbike(
                    _id SERIAL PRIMARY KEY,
                    sna VARCHAR(50) NOT NULL,
                    sarea VARCHAR(50),
                    ar VARCHAR(100),
                    mday TIMESTAMP,
                    updateTime TIMESTAMP,
                    total SMALLINT,
                    rent_bikes SMALLINT,
                    return_bikes SMALLINT,
                    lat REAL,
                    lng REAL,
                    act BOOLEAN,
                    UNIQUE (sna, updateTime)
                );
                '''
                cursor.execute(sql)

        # 加載所有資料從 data 模組中
        all_data = data.load_data()  # 假設 data 模組中有一個名為 load_data() 的函式用來加載資料

        # 插入資料到 youbike 表格中
        with conn:
            with conn.cursor() as cursor:
                insert_sql = '''
                INSERT INTO youbike(sna, sarea, ar, mday, updateTime, total, rent_bikes, return_bikes, lat, lng, act)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (sna, updateTime) DO NOTHING;
                '''
                for site in all_data:
                    cursor.execute(insert_sql, (
                        site['sna'],
                        site['sarea'],
                        site['ar'],
                        site['mday'],
                        site['updateTime'],
                        site['total'],
                        site['rent_bikes'],
                        site['return_bikes'],
                        site['lat'],
                        site['lng'],
                        site['act']
                    ))

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    main()
