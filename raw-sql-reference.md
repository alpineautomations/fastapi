# Reference — CRUD with raw SQL (psycopg2)

Snapshot of `app/main.py` from the section **before** switching to SQLAlchemy.
Kept as learning material: this is the "talk to Postgres by hand" version. The
SQLAlchemy version replaces all of the manual connection / cursor / SQL-string
work with an ORM.

## Full code

```python
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Retry loop: keep trying to connect until Postgres answers.
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='ohshit',
            cursor_factory=RealDictCursor,   # rows come back as dicts, not tuples
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "welcome to my api!!"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"post details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"data": updated_post}
```

## Table this code assumes

```sql
CREATE TABLE posts (
    id serial PRIMARY KEY,
    title varchar NOT NULL,
    content varchar NOT NULL,
    published boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now()
);
```

## Lessons learned in this section (the bugs we hit)

| Symptom | Cause | Fix |
| --- | --- | --- |
| `zsh: no matches found: fastapi[all]` | zsh treats `[ ]` as a glob | quote it: `pip install "fastapi[all]"` |
| `pg_config executable not found` building psycopg2 | source build needs Postgres headers | `pip install psycopg2-binary` |
| `could not translate host name "local host"` | space in the host string | `host='localhost'` |
| `password authentication failed for user "postgres"` | wrong password for the role | `ALTER USER postgres PASSWORD '...'` and match it in code |
| Ctrl-C won't kill uvicorn | `while True` retry loop runs at import, before uvicorn installs signal handlers | `lsof -ti:8000 \| xargs kill -9`; loop is fine once connected |
| `relation "post" does not exist` | table is `posts`; unquoted identifiers fold to lowercase | `SELECT * FROM posts` |
| `print(cursor.execute(...))` prints `None` | `execute()` returns `None` | call `cursor.fetchall()` / `fetchone()` |
| `syntax error at or near "."` | `VALUES (%s, %s. %s)` — typo, `.` instead of `,` | `VALUES (%s, %s, %s)` |
| `column "published" of relation "posts" does not exist` (but it's right there in pgAdmin) | column was created as `"published "` — trailing space in the name | `ALTER TABLE posts RENAME COLUMN "published " TO published` |
| `execute() takes from 2 to 3 positional arguments but 5 were given` | passed params as separate args | pass one tuple: `execute(sql, (a, b, c))` |
| `UPDATE ... RETURNING *` changed every row | missing `WHERE id = %s` | add the `WHERE` clause + matching value in the tuple |
| INSERT/UPDATE/DELETE "worked" but nothing persisted | psycopg2 opens a transaction; no autocommit | `conn.commit()` after every write |

### Key rules

- **`%s` placeholders only** — never f-string user input into SQL (injection).
- **Params are always a sequence**: one value still needs a trailing comma —
  `(str(id),)`, not `(str(id))`. A bare string gets iterated character by
  character and you get "not all arguments converted".
- **`commit()` after writes**, `fetchone()` / `fetchall()` after reads.
- `RETURNING *` hands back the row the DB actually wrote (with the real `id`,
  `created_at`, defaults applied).

## What SQLAlchemy replaces

| Raw SQL here | SQLAlchemy equivalent |
| --- | --- |
| `psycopg2.connect(...)` + retry loop | `create_engine(...)` + `SessionLocal` |
| `CREATE TABLE` by hand in psql/pgAdmin | `models.Base.metadata.create_all(bind=engine)` from a `Post(Base)` model |
| `cursor.execute("SELECT * FROM posts")` | `db.query(models.Post).all()` |
| `INSERT ... RETURNING *` + `commit()` | `db.add(obj)`, `db.commit()`, `db.refresh(obj)` |
| `WHERE id = %s` + `fetchone()` | `db.query(models.Post).filter(models.Post.id == id).first()` |
| manual `%s` escaping | ORM parameterizes automatically |
| `RealDictCursor` to get dict rows | Pydantic `response_model` + `from_attributes = True` |
