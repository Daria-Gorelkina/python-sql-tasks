import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def create_post(conn, post):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO posts (title, content, author_id)
            VALUES (%s, %s, %s) RETURNING id;
            """,
            (post['title'], post['content'], post['author_id'])
        )
        post_id = cursor.fetchone()[0]
        conn.commit()
        return post_id

def add_comment(conn, comment):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO comments (post_id, author_id, content)
            VALUES (%s, %s, %s) RETURNING id;
            """,
            (comment_data['post_id'], comment_data['author_id'], comment_data['content'])
        )
        comment_id = cursor.fetchone()[0]
        conn.commit()
        return comment_id

def get_latest_posts(conn, n):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        # Получаем последние n постов
        cursor.execute(
            """
            SELECT p.id, p.title, p.content, p.author_id, p.created_at FROM posts p
            ORDER BY created_at DESC
            LIMIT %s;
            """,
            (n,)
        )
        posts = cursor.fetchall()

        for post in posts:
            cursor.execute(
                "SELECT c.id, c.author_id, c.content, c.created_at "
                "FROM comments c "
                "WHERE c.post_id = %s "
                "ORDER BY c.created_at;",
                (post['id'],)
            )
            post['comments'] = cursor.fetchall()

        return posts
# END
