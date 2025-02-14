from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, LoginManager
from models import Usuario, Voo
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '12345-54321'  

db.init_app(app)

# login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# routes
# index route
# used to select filters for flights
@app.route("/")
@login_required
def index():
    mercados = db.session.query(Voo.mercado).distinct().all()
    mercados = [m[0] for m in mercados]
    return render_template("index.html", mercados=mercados)

# login route
# used to login to application
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = Usuario.query.filter_by(username=username).first()
        
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha incorretos.", "danger")
    return render_template("login.html")

# register route
# used to register new user
@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if Usuario.query.filter_by(username=username).first():
            flash("Usuário já existe.", "warning")
        else:
            new_user = Usuario(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Usuário criado com sucesso.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

# logout route
# used to log out user
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# get voos route
# returns the flights with desired filters
@app.route("/get_voos", methods=["GET"])
@login_required
def get_voos():
    mercado = request.args.get("mercado", "todos")
    ano_inicio = request.args.get("ano_inicio")
    mes_inicio = request.args.get("mes_inicio")
    ano_fim = request.args.get("ano_fim")
    mes_fim = request.args.get("mes_fim")

    # filter by market
    if mercado == "todos":
        query = db.session.query(Voo)
    else:
        query = db.session.query(Voo).filter(Voo.mercado == mercado)
    
    # filter by date
    if ano_inicio and mes_inicio:
        query = query.filter((Voo.ano > int(ano_inicio)) | ((Voo.ano == int(ano_inicio)) & (Voo.mes >= int(mes_inicio))))
    if ano_fim and mes_fim:
        query = query.filter((Voo.ano < int(ano_fim)) | ((Voo.ano == int(ano_fim)) & (Voo.mes <= int(mes_fim))))
    
    voos = query.all()  
    dados = [{"ano": voo.ano, "mes": voo.mes, "rpk": voo.rpk, "mercado": voo.mercado} for voo in voos]
    
    return jsonify(dados)

if __name__ == "__main__":
    app.run(debug=True)
