from flask import Flask, render_template_string, request, redirect, url_for
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

template_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Motorapp</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background-color: black;
            color: white;
            transition: background-color 0.3s, color 0.3s;
        }
        .pantalla { display: none; padding: 40px; text-align: center; }
        .visible { display: block; }
        .boton {
            padding: 12px 24px;
            margin-top: 20px;
            font-size: 1em;
            border-radius: 10px;
            border: none;
            background-color: #1e90ff;
            color: white;
            cursor: pointer;
        }
        .logos { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; margin-top: 40px; }
        .logos img {
            width: 130px;
            height: 130px;
            object-fit: contain;
            background-color: white;
            border-radius: 20px;
            padding: 10px;
            cursor: pointer;
        }
        .info { max-width: 800px; margin: auto; }
        .info img { width: 100%; max-height: 300px; object-fit: cover; border-radius: 15px; }
        .datos { text-align: left; margin-top: 20px; }
        .datos h3 { color: #00d0ff; margin-bottom: 5px; }
        #top-right-buttons { position: absolute; top: 20px; right: 20px; }
        #top-right-buttons a {
            color: white;
            background-color: #1e90ff;
            padding: 10px 16px;
            border-radius: 10px;
            text-decoration: none;
            margin-left: 10px;
        }
        #botonInicio { position: absolute; top: 20px; left: 60px; }
        #menuHamburguesa {
            position: absolute; top: 20px; left: 20px; cursor: pointer;
        }
        .lineaMenu {
            width: 25px; height: 3px; background-color: white; margin: 5px;
        }
        #configPanel {
            position: absolute;
            top: 60px;
            left: 20px;
            background: #222;
            color: white;
            padding: 15px;
            border-radius: 10px;
            display: none;
        }
        #configPanel input {
            margin-top: 10px;
            padding: 5px;
            width: 80%;
        }
    </style>
</head>
<body>

<div id="menuHamburguesa" onclick="toggleConfig()">
    <div class="lineaMenu"></div>
    <div class="lineaMenu"></div>
    <div class="lineaMenu"></div>
</div>

<div id="configPanel">
    <div>
        <span>⚙️ Configuración</span><br><br>
        <button onclick="cambiarTema()">Cambiar tema</button><br><br>
        <input type="text" id="nombreUsuario" placeholder="Nuevo nombre">
        <button onclick="cambiarNombre()">Cambiar nombre</button>
    </div>
</div>

<div id="top-right-buttons">
    {% if not current_user.is_authenticated %}
        <a href="/login">Iniciar sesión</a>
        <a href="/register">Registrarse</a>
    {% else %}
        <a href="/logout">Cerrar sesión</a>
    {% endif %}
</div>

{% if current_user.is_authenticated %}
<div id="botonInicio">
    <button class="boton" onclick="mostrar('bienvenida')">Inicio</button>
</div>

<div id="bienvenida" class="pantalla visible">
    <h1 id="saludo">Bienvenido a Motorapp</h1>
    <img src="/static/carro.jpg" style="width: 100%; height: 50vh; object-fit: cover;">
    <p>En esta página verás imágenes de diferentes marcas, con su información respectiva. ¡Arranquemos!</p>
    <button class="boton" onclick="mostrar('marcas')">Marcas</button>
</div>

<div id="marcas" class="pantalla">
    <h1>Selecciona una marca</h1>
    <div class="logos">
        {% for marca in marcas %}
        <img src="/static/{{marca}}.png" onclick="mostrarMarca('{{marca}}')">
        {% endfor %}
    </div>
</div>

<div id="info" class="pantalla">
    <div class="info">
        <img id="imagenAuto" src="">
        <div class="datos">
            <h3>Velocidad:</h3><p id="velocidad"></p>
            <h3>Capacidad:</h3><p id="capacidad"></p>
            <h3>Ventas:</h3><p id="ventas"></p>
            <h3>Información general:</h3><p id="infoGeneral"></p>
        </div>
        <button class="boton" onclick="mostrar('marcas')">Volver</button>
    </div>
</div>
{% else %}
<div style="text-align:center; padding: 80px;">
    <h2>Debes iniciar sesión para ver el contenido de Motorapp 🚗🔒</h2>
</div>
{% endif %}

<script>
const datosMarca = {
    volkswagen: { auto: "/static/volkswagen_auto.jpg", velocidad: "210 km/h", capacidad: "5 personas", ventas: "6 millones/año", info: "Fundada en 1937." },
    toyota: { auto: "/static/toyota_auto.jpg", velocidad: "180 km/h", capacidad: "5 personas", ventas: "Líder mundial 2023", info: "Fundada por Kiichiro Toyoda." },
    lamborghini: { auto: "/static/lamborghini_auto.jpg", velocidad: "350 km/h", capacidad: "2 personas", ventas: "8.405 en 2023", info: "Fundada en 1963." },
    ferrari: { auto: "/static/ferrari_auto.jpg", velocidad: "340 km/h", capacidad: "2 personas", ventas: "13.221 en 2023", info: "Fundada por Enzo Ferrari." },
    ford: { auto: "/static/ford_auto.jpg", velocidad: "200 km/h", capacidad: "5 personas", ventas: "4 millones/año", info: "Fundada en 1903." },
    chevrolet: { auto: "/static/chevrolet_auto.jpg", velocidad: "220 km/h", capacidad: "5 personas", ventas: "2.3 millones en 2023", info: "Chevy clásico." },
    pagani: { auto: "/static/pagani_auto.jpg", velocidad: "383 km/h", capacidad: "2 personas", ventas: "Muy pocos", info: "Zonda y Huayra." },
    bugatti: { auto: "/static/bugatti_auto.jpg", velocidad: "420 km/h", capacidad: "2 personas", ventas: "Limitados", info: "Veyron y Chiron." }
};

function mostrar(id) {
    document.querySelectorAll('.pantalla').forEach(p => p.classList.remove('visible'));
    document.getElementById(id).classList.add('visible');
}

function mostrarMarca(marca) {
    const data = datosMarca[marca];
    document.getElementById("imagenAuto").src = data.auto;
    document.getElementById("velocidad").innerText = data.velocidad;
    document.getElementById("capacidad").innerText = data.capacidad;
    document.getElementById("ventas").innerText = data.ventas;
    document.getElementById("infoGeneral").innerText = data.info;
    mostrar("info");
}

function toggleConfig() {
    const panel = document.getElementById("configPanel");
    panel.style.display = panel.style.display === "block" ? "none" : "block";
}

function cambiarTema() {
    const body = document.body;
    const dark = body.style.backgroundColor === "black";
    body.style.backgroundColor = dark ? "white" : "black";
    body.style.color = dark ? "black" : "white";
}

function cambiarNombre() {
    const nuevoNombre = document.getElementById("nombreUsuario").value;
    if (nuevoNombre) {
        document.getElementById("saludo").innerText = `Bienvenido, ${nuevoNombre}`;
    }
}
</script>
</body>
</html>
"""

@app.route("/")
@login_required
def index():
    marcas = ["volkswagen", "toyota", "lamborghini", "ferrari", "ford", "chevrolet", "pagani", "bugatti"]
    return render_template_string(template_html, marcas=marcas)

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
    return '''<form method="post"><h2>Iniciar sesión</h2><input type="text" name="email" placeholder="Correo" required><br><br><input type="password" name="password" placeholder="Contraseña" required><br><br><button type="submit">Ingresar</button><br><br><a href="/register">¿No tienes cuenta? Regístrate</a></form>'''

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
    return '''<form method="post"><h2>Registrarse</h2><input type="text" name="email" placeholder="Correo" required><br><br><input type="password" name="password" placeholder="Contraseña" required><br><br><button type="submit">Registrar</button><br><br><a href="/login">¿Ya tienes cuenta? Inicia sesión</a></form>'''

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









