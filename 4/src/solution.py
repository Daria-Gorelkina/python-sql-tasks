import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def get_order_sum(conn, month):
    query = """SELECT c.customer_name, SUM(o.total_amount) AS total
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE EXTRACT(MONTH FROM o.order_date) = %s
    GROUP BY c.customer_name
    """
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(query, [month])
        results = cursor.fetchall()
    output = []
    for row in results:
        output.append(f"Покупатель {row['customer_name']} совершил покупок на сумму {row['total']}")

    return "\n".join(output)
# END
