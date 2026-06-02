import psycopg2

conn = psycopg2.connect('postgresql://datatalk_db_s5vu_user:u7YIwQRqoT4sjKv3jj0DXa1R3nqwZ8o1@dpg-d8f4vhernols73anvj6g-a.singapore-postgres.render.com/datatalk_db_s5vu')
cur = conn.cursor()
cur.execute('ALTER TABLE "Dataset" ADD COLUMN IF NOT EXISTS summary TEXT')
conn.commit()
cur.close()
conn.close()
print('Done!')