from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort, session, g
from . import db as dbdao  # DAO com PyMySQL
import re
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("main", __name__)

# ----------------- Helpers -----------------
def _to_float(value, default=0.0):
    """Converte '120,50' ou '120.50' em float."""
    try:
        return float(str(value).replace(",", "."))
    except Exception:
        return default

def _is_checked(name: str) -> bool:
    """Lê checkbox/radio de formulário como booleano."""
    return request.form.get(name) in ("on", "true", "1", "yes")

def _digits_only(s: str) -> str:
    return re.sub(r"\D", "", s or "")

def _cpf_is_valid(cpf_digits: str) -> bool:
    """Valida CPF (11 dígitos) com dígitos verificadores."""
    if not cpf_digits or len(cpf_digits) != 11:
        return False
    if cpf_digits == cpf_digits[0] * 11:
        return False
    nums = [int(c) for c in cpf_digits]
    # DV1
    s1 = sum(nums[i] * (10 - i) for i in range(9))
    dv1 = (s1 * 10) % 11
    if dv1 == 10:
        dv1 = 0
    if dv1 != nums[9]:
        return False
    # DV2
    s2 = sum(nums[i] * (11 - i) for i in range(10))
    dv2 = (s2 * 10) % 11
    if dv2 == 10:
        dv2 = 0
    return dv2 == nums[10]

# ----------------- Sessão / usuário atual -----------------
@bp.before_app_request
def load_logged_in_user():
    uid = session.get("user_id")
    if uid is None:
        g.current_user = None
    else:
        g.current_user = dbdao.user_get_by_id(uid)

@bp.app_context_processor
def inject_user():
    u = getattr(g, "current_user", None)
    first = (u["name"].split()[0]) if (u and u.get("name")) else None
    return {"current_user": u, "current_user_first": first}

# ----------------- PÚBLICO -----------------
@bp.route("/")
def index():
    services = dbdao.services_list(only_active=True)
    return render_template("index.html", services=services, page_title="Início")

@bp.route("/servicos")
def servicos():
    services = dbdao.services_list(only_active=True)
    return render_template("servicos.html", services=services, page_title="Serviços")

@bp.route("/agendamentos")
def agendamentos():
    return render_template("agendamentos.html", page_title="Meus agendamentos")

@bp.route("/quem-somos")
def quem_somos():
    blocks = dbdao.about_list()
    return render_template("quem_somos.html", blocks=blocks, page_title="Quem somos")

# ----------------- Autenticação -----------------
@bp.route("/login", methods=["GET", "POST"])
def login():
    # --- login rápido por GET (somente para desenvolvimento) ---
    if request.method == "GET" and request.args.get("email") and request.args.get("senha"):
        email = request.args["email"].strip().lower()
        senha = request.args["senha"]
        user = dbdao.user_get_by_email(email)
        if user and check_password_hash(user["password_hash"], senha):
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            flash(f"Bem-vindo(a), {user['name'].split()[0]}!", "success")
            return redirect(url_for("main.index"))
        flash("E-mail ou senha inválidos.", "danger")
        return redirect(url_for("main.login"))
    # --- fluxo normal por POST ---
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        senha = request.form.get("senha") or ""
        user = dbdao.user_get_by_email(email)
        if not user or not check_password_hash(user["password_hash"], senha):
            flash("E-mail ou senha inválidos.", "danger")
            return redirect(url_for("main.login"))
        session.clear()
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["user_email"] = user["email"]
        flash(f"Bem-vindo(a), {user['name'].split()[0]}!", "success")
        return redirect(url_for("main.index"))
    return render_template("login.html", page_title="Entrar")

@bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da conta.", "info")
    return redirect(url_for("main.index"))

@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        name  = (request.form.get("nome")  or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        cpf   = _digits_only(request.form.get("cpf"))
        phone = _digits_only(request.form.get("celular"))
        pass1 = request.form.get("senha") or ""
        pass2 = request.form.get("confirmar-senha") or ""

        # validações simples
        if not name or not email or not cpf or not phone or not pass1 or not pass2:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("main.cadastro"))

        if pass1 != pass2:
            flash("As senhas não conferem.", "danger")
            return redirect(url_for("main.cadastro"))

        if len(cpf) != 11 or not _cpf_is_valid(cpf):
            flash("CPF inválido.", "danger")
            return redirect(url_for("main.cadastro"))

        if len(phone) < 10:
            flash("Informe um celular válido (DDD + número).", "danger")
            return redirect(url_for("main.cadastro"))

        # unicidade
        if dbdao.user_get_by_email(email):
            flash("Este e-mail já está cadastrado.", "warning")
            return redirect(url_for("main.cadastro"))
        if dbdao.user_get_by_cpf(cpf):
            flash("Este CPF já está cadastrado.", "warning")
            return redirect(url_for("main.cadastro"))

        # cria usuário
        pwd_hash = generate_password_hash(pass1)
        new_id = dbdao.user_insert(
            name=name,
            email=email,
            cpf_digits=cpf,
            phone_digits=phone,
            password_hash=pwd_hash
        )

        # AUTO-LOGIN após cadastro
        session.clear()
        session["user_id"] = new_id
        session["user_name"] = name
        session["user_email"] = email

        flash(f"Conta criada com sucesso! Bem-vindo(a), {name.split()[0]}!", "success")
        return redirect(url_for("main.index"))

    return render_template("cadastro.html", page_title="Cadastro")


# ----------------- ADMIN WEB (CRUD) -----------------
# Rota legada: jogamos tudo para o dashboard único
@bp.route("/admin/services")
def services_admin():
    return redirect(url_for("main.admin_dashboard"))

@bp.route("/admin/services/new", methods=["GET", "POST"])
def services_new():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        if not name:
            flash("Nome é obrigatório.", "danger")
            return redirect(url_for("main.services_new"))

        dbdao.service_insert(
            name=name,
            description=request.form.get("description", "") or "",
            price=_to_float(request.form.get("price", 0)),
            icon=request.form.get("icon", "") or "",
            is_active=_is_checked("is_active"),
        )
        flash("Serviço cadastrado!", "success")
        return redirect(url_for("main.admin_dashboard"))

    return render_template("admin/service_form.html", service=None, page_title="Novo serviço")

@bp.route("/admin/services/<int:service_id>/edit", methods=["GET", "POST"])
def services_edit(service_id):
    s = dbdao.service_get(service_id)
    if not s:
        abort(404)

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        if not name:
            flash("Nome é obrigatório.", "danger")
            return redirect(url_for("main.services_edit", service_id=service_id))

        dbdao.service_update(
            service_id=service_id,
            name=name,
            description=request.form.get("description", s.get("description", "")),
            price=_to_float(request.form.get("price", s.get("price", 0))),
            icon=request.form.get("icon", s.get("icon", "")),
            is_active=_is_checked("is_active"),
        )
        flash("Serviço atualizado!", "success")
        return redirect(url_for("main.admin_dashboard"))

    return render_template("admin/service_form.html", service=s, page_title="Editar serviço")

@bp.route("/admin/services/<int:service_id>/delete", methods=["POST"])
def services_delete(service_id):
    s = dbdao.service_get(service_id)
    if not s:
        abort(404)
    dbdao.service_delete(service_id)
    flash("Serviço excluído.", "info")
    return redirect(url_for("main.admin_dashboard"))

@bp.route("/admin/services/<int:service_id>/toggle", methods=["POST"])
def services_toggle(service_id):
    s = dbdao.service_get(service_id)
    if not s:
        abort(404)
    dbdao.service_toggle(service_id)
    flash("Status alterado.", "info")
    return redirect(request.referrer or url_for("main.admin_dashboard"))

# ===== ADMIN: QUEM SOMOS =====
@bp.route("/admin/about")
def about_admin():
    return redirect(url_for("main.admin_dashboard"))

@bp.route("/admin/about/new", methods=["GET", "POST"])
def about_new():
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        if not title:
            flash("Título é obrigatório.", "danger")
            return redirect(url_for("main.about_new"))

        dbdao.about_insert(
            title=title,
            body=request.form.get("body", "") or "",
            image=request.form.get("image", "") or "",
            icon=request.form.get("icon", "") or "",
            section=request.form.get("section", "story") or "story",
            display_order=int(request.form.get("display_order", 0) or 0),
        )
        flash("Bloco cadastrado!", "success")
        return redirect(url_for("main.admin_dashboard"))

    return render_template("admin/about_form.html", block=None, page_title="Novo bloco — Quem Somos")

@bp.route("/admin/about/<int:block_id>/edit", methods=["GET", "POST"])
def about_edit(block_id):
    b = dbdao.about_get(block_id)
    if not b:
        abort(404)

    if request.method == "POST":
        dbdao.about_update(
            block_id=block_id,
            title=request.form.get("title", b.get("title")),
            body=request.form.get("body", b.get("body")),
            image=request.form.get("image", b.get("image", "")),
            icon=request.form.get("icon", b.get("icon", "")),
            section=request.form.get("section", b.get("section", "story")),
            display_order=int(request.form.get("display_order", b.get("display_order", 0)) or 0),
        )
        flash("Bloco atualizado!", "success")
        return redirect(url_for("main.admin_dashboard"))

    return render_template("admin/about_form.html", block=b, page_title="Editar bloco — Quem Somos")

@bp.route("/admin/about/<int:block_id>/delete", methods=["POST"])
def about_delete(block_id):
    b = dbdao.about_get(block_id)
    if not b:
        abort(404)
    dbdao.about_delete(block_id)
    flash("Bloco excluído.", "info")
    return redirect(url_for("main.admin_dashboard"))

# helper: garante que o bloco existe; se não existir, cria com defaults
def _get_or_create_about(section: str, title_default: str, order: int):
    blk = dbdao.about_get_by_section(section)
    if not blk:
        new_id = dbdao.about_insert_min(section, title_default, order)
        blk = dbdao.about_get(new_id)
    return blk

# página única para editar os 4 blocos principais (opcional)
@bp.route("/admin/about/core", methods=["GET", "POST"])
def about_core():
    story   = _get_or_create_about("story",   "Nossa história", 10)
    mission = _get_or_create_about("mission", "Missão",         20)
    vision  = _get_or_create_about("vision",  "Visão",          30)
    values  = _get_or_create_about("values",  "Valores",        40)

    if request.method == "POST":
        # Atualiza cada bloco individualmente
        dbdao.about_update(
            block_id=story["id"],
            title=request.form.get("story_title", story.get("title")),
            body=request.form.get("story_body", story.get("body")),
            image=story.get("image", ""),
            icon=story.get("icon", ""),
            section="story",
            display_order=story.get("display_order", 10),
        )
        dbdao.about_update(
            block_id=mission["id"],
            title=request.form.get("mission_title", mission.get("title")),
            body=request.form.get("mission_body", mission.get("body")),
            image=mission.get("image", ""),
            icon=mission.get("icon", ""),
            section="mission",
            display_order=mission.get("display_order", 20),
        )
        dbdao.about_update(
            block_id=vision["id"],
            title=request.form.get("vision_title", vision.get("title")),
            body=request.form.get("vision_body", vision.get("body")),
            image=vision.get("image", ""),
            icon=vision.get("icon", ""),
            section="vision",
            display_order=vision.get("display_order", 30),
        )
        dbdao.about_update(
            block_id=values["id"],
            title=request.form.get("values_title", values.get("title")),
            body=request.form.get("values_body", values.get("body")),
            image=values.get("image", ""),
            icon=values.get("icon", ""),
            section="values",
            display_order=values.get("display_order", 40),
        )
        flash("Conteúdo atualizado com sucesso!", "success")
        return redirect(url_for("main.about_core"))

    return render_template(
        "admin/about_core.html",
        story=story, mission=mission, vision=vision, values=values,
        page_title="Editar — Quem Somos"
    )

@bp.route("/admin")
@bp.route("/admin/")
@bp.route("/admin/dashboard")
def admin_dashboard():
    # Lista completa (inclui inativos) e blocos
    services = dbdao.services_list(only_active=False)
    blocks = dbdao.about_list()
    return render_template(
        "admin/dashboard.html",
        services=services, blocks=blocks, page_title="Admin"
    )

# ----------------- API -----------------
@bp.get("/api/services")
def api_services_list():
    only_active = request.args.get("active", "true").lower() == "true"
    rows = dbdao.services_list(only_active=only_active)
    return jsonify(rows)

@bp.get("/api/services/<int:service_id>")
def api_services_detail(service_id):
    s = dbdao.service_get(service_id)
    if not s:
        abort(404)
    return jsonify(s)
