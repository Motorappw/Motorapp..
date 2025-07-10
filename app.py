from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.secret_key = 'motorapp_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@login_required
def index():
    marcas = ["volkswagen", "toyota", "lamborghini", "ferrari", "ford", "chevrolet", "pagani", "bugatti"]
    return render_template("informacion.html", marcas=marcas)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("index"))
        return "Credenciales incorrectas"
    return '''
    <form method="post">
        <h2>Iniciar sesión</h2>
        <input type="text" name="email" placeholder="Correo" required><br><br>
        <input type="password" name="password" placeholder="Contraseña" required><br><br>
        <button type="submit">Ingresar</button>
        <br><br>
        <a href="/register">¿No tienes cuenta? Regístrate</a>
    </form>
    '''

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if User.query.filter_by(email=email).first():
            return "El correo ya está registrado"
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("index"))
    return '''
    <form method="post">
        <h2>Registrarse</h2>
        <input type="text" name="email" placeholder="Correo" required><br><br>
        <input type="password" name="password" placeholder="Contraseña" required><br><br>
        <button type="submit">Registrar</button>
        <br><br>
        <a href="/login">¿Ya tienes cuenta? Inicia sesión</a>
    </form>
    '''

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
