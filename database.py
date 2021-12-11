import psycopg2.extras


conn = psycopg2.connect("dbname=webfinal host=1.14.130.92 user=postgres password=postgres12345689")
# conn = psycopg2.connect("dbname=webfinal host=127.0.0.1 user=postgres password=postgres12345689")

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
