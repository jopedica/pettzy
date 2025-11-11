# Importa a biblioteca PyMySQL, que é o "driver" para conectar e interagir com o banco de dados MySQL.
import pymysql
# Importa o 'current_app' do Flask para acessar as configurações globais da aplicação (como senhas e hosts).
from flask import current_app

# -------------------------------------------------------
# Conexão
# -------------------------------------------------------
def get_conn():
    """
    Abre uma conexão PyMySQL usando as variáveis de config:
      DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
    """
    # Pega o objeto de configuração do aplicativo Flask atual.
    cfg = current_app.config

    # Usa pymysql para criar e retornar um objeto de conexão com o banco de dados.
    return pymysql.connect(
        # Pega o host do DB das configs, ou usa 'localhost' como padrão.
        host=cfg.get("DB_HOST", "localhost"),
        # Pega a porta, converte para inteiro, ou usa 3306 como padrão.
        port=int(cfg.get("DB_PORT", 3306)),
        # Pega o usuário, ou usa 'root' como padrão.
        user=cfg.get("DB_USER", "root"),
        # Pega a senha.
        password=cfg.get("DB_PASS", "Thor2804!"),
        # Pega o nome do banco de dados, ou usa 'pettzy' como padrão.
        database=cfg.get("DB_NAME", "pettzy"),
        # Configura o cursor para retornar resultados como dicionários Python (ex: {'id': 1, 'name': 'Banho'}),
        # o que é muito mais fácil de trabalhar do que tuplas.
        cursorclass=pymysql.cursors.DictCursor,
        # Desativa o autocommit. Isso significa que precisamos chamar conn.commit() manualmente para salvar
        # qualquer alteração (INSERT, UPDATE, DELETE), nos dando mais controle sobre as transações.
        autocommit=False,
    )

# -------------------------------------------------------
# SERVICES (CRUD)
# Tabela esperada: services(id PK AI, name, description, price DECIMAL, icon, is_active TINYINT)
# -------------------------------------------------------

# READ (Listar todos os serviços)
def services_list(only_active=True):
    # Constrói a consulta SQL base.
    sql = "SELECT * FROM services"
    params = [] # Prepara uma lista para parâmetros, embora não usada aqui, é uma boa prática.

    # Se o parâmetro da função for True (padrão), adiciona um filtro para pegar apenas serviços ativos.
    if only_active:
        sql += " WHERE is_active=1"
    
    # Adiciona a ordenação para que os resultados venham sempre em ordem alfabética pelo nome.
    sql += " ORDER BY name"
    
    # O bloco 'with' garante que a conexão (conn) e o cursor (cur) serão fechados automaticamente no final.
    with get_conn() as conn, conn.cursor() as cur:
        # Executa a consulta SQL montada.
        cur.execute(sql, params)
        # Retorna todas as linhas encontradas pela consulta como uma lista de dicionários.
        return cur.fetchall()

# READ (Pegar um serviço específico pelo ID)
def service_get(service_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        # Executa a consulta, usando %s como placeholder para segurança (evita SQL Injection).
        # O valor (service_id,) é passado separadamente para o driver do banco tratar.
        cur.execute("SELECT * FROM services WHERE id=%s", (service_id,))
        # Retorna apenas a primeira (e única) linha encontrada. Se nada for encontrado, retorna None.
        return cur.fetchone()

# CREATE (Inserir um novo serviço)
def service_insert(name: str, description: str, price, icon: str, is_active: bool):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO services (name, description, price, icon, is_active)
            VALUES (%s, %s, %s, %s, %s)
            """,
            # Passa os valores como uma tupla. O valor booleano 'is_active' é convertido para 1 ou 0.
            (name, description, price, icon, 1 if is_active else 0),
        )
        # Confirma e salva a transação no banco de dados. Sem isso, a inserção não seria efetivada.
        conn.commit()
        # Retorna o ID da linha que acabou de ser inserida. Útil para redirecionar o usuário para a nova página.
        return cur.lastrowid

# UPDATE (Atualizar um serviço existente)
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
            # A ordem dos valores na tupla deve corresponder exatamente aos placeholders (%s) na query.
            (name, description, price, icon, 1 if is_active else 0, service_id),
        )
        # Salva as alterações no banco de dados.
        conn.commit()

# UPDATE (Alternar o status de ativo/inativo)
def service_toggle(service_id: int):
    """
    Alterna is_active (0/1) atomicamente.
    """
    with get_conn() as conn, conn.cursor() as cur:
        # Este é um truque matemático: se is_active for 1, 1-1=0. Se for 0, 1-0=1.
        # Isso inverte o valor diretamente no banco de dados.
        cur.execute("UPDATE services SET is_active = 1 - is_active WHERE id=%s", (service_id,))
        # Salva a alteração.
        conn.commit()

# DELETE (Excluir um serviço)
def service_delete(service_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        # Executa o comando DELETE, garantindo que apenas a linha com o ID correspondente seja removida.
        cur.execute("DELETE FROM services WHERE id=%s", (service_id,))
        # Salva a exclusão no banco de dados.
        conn.commit()   

        # -------------------------------------------------------
# USERS (Cadastro / Login)
# Tabela esperada: users(id, name, email, cpf, phone, password_hash, created_at, updated_at)
# -------------------------------------------------------

def user_get_by_id(user_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        return cur.fetchone()

def user_get_by_email(email: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        return cur.fetchone()

def user_get_by_cpf(cpf: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE cpf=%s", (cpf,))
        return cur.fetchone()

def user_insert(name: str, email: str, cpf_digits: str, phone_digits: str, password_hash: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO users (name, email, cpf, phone, password_hash, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """,
            (name, email, cpf_digits, phone_digits, password_hash),
        )
        conn.commit()
        return cur.lastrowid


# -------------------------------------------------------
# ABOUT_BLOCKS (Quem Somos)
# Tabela esperada: about_blocks(id, title, body, image, icon, section, display_order, created_at, updated_at)
# -------------------------------------------------------

def about_list():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM about_blocks ORDER BY display_order")
        return cur.fetchall()

def about_get(block_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM about_blocks WHERE id=%s", (block_id,))
        return cur.fetchone()

def about_insert(title: str, body: str, image: str, icon: str, section: str, display_order: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO about_blocks (title, body, image, icon, section, display_order, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
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
               SET title=%s, body=%s, image=%s, icon=%s,
                   section=%s, display_order=%s, updated_at=NOW()
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
        cur.execute("SELECT * FROM about_blocks WHERE section=%s", (section,))
        return cur.fetchone()

def about_insert_min(section: str, title_default: str, order: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO about_blocks (title, body, section, display_order, created_at, updated_at)
            VALUES (%s, '', %s, %s, NOW(), NOW())
            """,
            (title_default, section, order),
        )
        conn.commit()
        return cur.lastrowid
