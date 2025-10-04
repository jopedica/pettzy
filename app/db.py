# app/db.py
import pymysql
from flask import current_app

# -------------------------------------------------------
# Conexão
# -------------------------------------------------------
def get_conn():
    """
    Abre uma conexão PyMySQL usando as variáveis de config:
      DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
    """
    cfg = current_app.config
    return pymysql.connect(
        host=cfg.get("DB_HOST", "localhost"),
        port=int(cfg.get("DB_PORT", 3306)),
        user=cfg.get("DB_USER", "root"),
        password=cfg.get("DB_PASS", ""),
        database=cfg.get("DB_NAME", "pettzy"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,  # commit/manual
    )

# -------------------------------------------------------
# SERVICES (CRUD)
# Tabela esperada: services(id PK AI, name, description, price DECIMAL, icon, is_active TINYINT)
# -------------------------------------------------------
def services_list(only_active=True):
    sql = "SELECT * FROM services"
    params = []
    if only_active:
        sql += " WHERE is_active=1"
    sql += " ORDER BY name"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()

def service_get(service_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM services WHERE id=%s", (service_id,))
        return cur.fetchone()

def service_insert(name: str, description: str, price, icon: str, is_active: bool):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO services (name, description, price, icon, is_active)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (name, description, price, icon, 1 if is_active else 0),
        )
        conn.commit()
        return cur.lastrowid

def service_update(service_id: int, name: str, description: str, price, icon: str, is_active: bool):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE services
               SET name=%s,
                   description=%s,
                   price=%s,
                   icon=%s,
                   is_active=%s
             WHERE id=%s
            """,
            (name, description, price, icon, 1 if is_active else 0, service_id),
        )
        conn.commit()

def service_toggle(service_id: int):
    """
    Alterna is_active (0/1) atomically.
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("UPDATE services SET is_active = 1 - is_active WHERE id=%s", (service_id,))
        conn.commit()

def service_delete(service_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM services WHERE id=%s", (service_id,))
        conn.commit()

# -------------------------------------------------------
# ABOUT_BLOCKS (CRUD)
# Tabela esperada: about_blocks(id PK AI, title, body, image, icon, section, display_order)
# -------------------------------------------------------
def about_list():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM about_blocks
            ORDER BY display_order, id
            """
        )
        return cur.fetchall()

def about_get(block_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM about_blocks WHERE id=%s", (block_id,))
        return cur.fetchone()

def about_insert(title: str, body: str, image: str, icon: str, section: str, display_order: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO about_blocks (title, body, image, icon, section, display_order)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (title, body, image, icon, section, display_order),
        )
        conn.commit()
        return cur.lastrowid

def about_update(block_id: int, title: str, body: str, image: str, icon: str, section: str, display_order: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE about_blocks
               SET title=%s,
                   body=%s,
                   image=%s,
                   icon=%s,
                   section=%s,
                   display_order=%s
             WHERE id=%s
            """,
            (title, body, image, icon, section, display_order, block_id),
        )
        conn.commit()

def about_delete(block_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM about_blocks WHERE id=%s", (block_id,))
        conn.commit()

def about_get_by_section(section: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM about_blocks WHERE section=%s ORDER BY id LIMIT 1", (section,))
        return cur.fetchone()

def about_insert_min(section: str, title_default: str, order: int):
    """
    Insere bloco mínimo com título e ordem, body vazio.
    Retorna o id criado.
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO about_blocks (section, title, body, display_order)
            VALUES (%s, %s, '', %s)
            """,
            (section, title_default, order),
        )
        conn.commit()
        return cur.lastrowid

# ---------------- USERS ----------------
def user_get_by_email(email: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email=%s LIMIT 1", (email.lower().strip(),))
        return cur.fetchone()

def user_get_by_cpf(cpf_digits: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE cpf=%s LIMIT 1", (cpf_digits,))
        return cur.fetchone()

def user_insert(name: str, email: str, cpf_digits: str, phone_digits: str, password_hash: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """INSERT INTO users (name, email, cpf, phone, password_hash)
               VALUES (%s, %s, %s, %s, %s)""",
            (name, email.lower().strip(), cpf_digits, phone_digits, password_hash),
        )
        conn.commit()
        return cur.lastrowid

# -------- USERS: fetch by id --------
def user_get_by_id(user_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, name, email FROM users WHERE id=%s", (user_id,))
        return cur.fetchone()
