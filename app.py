import os, random, json
from flask import Flask, render_template_string, request, redirect, session, url_for, jsonify

app = Flask(__name__)
app.secret_key = 'mairo_voip_v1_reinicio_total_2026'

# --- CSS MAESTRO (ESTILO GHOST CALL + ORO QUICK MONEY) ---
CSS = """
<style>
    :root { --gold: #d4af37; --bg: #030304; --card: #09090b; --border: #1a1a1e; --text-muted: #888; }
    body { background: var(--bg); color: #fff; font-family: 'JetBrains Mono', monospace; margin: 0; min-height: 100vh; overflow-x: hidden; }
    
    /* --- UTILIDADES --- */
    .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 25px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .btn { border: none; padding: 14px; border-radius: 8px; font-weight: bold; cursor: pointer; text-transform: uppercase; font-size: 13px; text-decoration: none; display: inline-block; transition: 0.3s; text-align: center;}
    .btn-gold { background: linear-gradient(135deg, #d4af37 0%, #aa8a2e 100%); color: #000; }
    .btn-dark { background: #111; color: #fff; border: 1px solid var(--border); }
    .btn-danger { background: rgba(255, 71, 87, 0.1); color: #ff4757; border: 1px solid #ff4757; }
    input, textarea, select { width: 100%; background: #000; border: 1px solid var(--border); color: #fff; padding: 15px; border-radius: 8px; margin-bottom: 15px; font-family: inherit; font-size: 14px; box-sizing: border-box;}
    .hidden { display: none; }
    .text-gold { color: var(--gold); }
    .text-muted { color: var(--text-muted); }
    
    /* --- HEADER --- */
    header { background: rgba(3, 3, 4, 0.95); padding: 15px 0; position: fixed; top: 0; width: 100%; z-index: 1000; border-bottom: 1px solid var(--border); backdrop-filter: blur(5px); }
    .nav-wrapper { display: flex; justify-content: space-between; align-items: center; }
    .logo { font-size: 20px; font-weight: bold; color: var(--gold); }
    .nav-links { display: flex; gap: 20px; align-items: center; }
    .nav-links a { color: var(--text-muted); text-decoration: none; font-size: 14px; }
    .nav-links a:hover { color: #fff; }

    /* --- LANDING PAGE --- */
    .hero { padding: 150px 0 100px; text-align: center; }
    .hero h1 { font-size: 48px; margin-bottom: 20px; line-height: 1.1; }
    .hero p { color: var(--text-muted); font-size: 18px; max-width: 600px; margin: 0 auto 40px; }
    .feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; padding: 50px 0; }
    .feature-card { text-align: center; }
    .feature-card i { font-size: 40px; color: var(--gold); margin-bottom: 20px; display: block;}

    /* --- DASHBOARD / AUTH --- */
    .main-content { padding: 120px 0 50px; }
    .badge-saldo { background: rgba(212, 175, 55, 0.1); border: 1px solid var(--gold); color: var(--gold); padding: 8px 18px; border-radius: 20px; font-size: 14px; }
    .tab-nav { display: flex; gap: 10px; margin-bottom: 30px; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
    .tab-link { color: var(--text-muted); cursor: pointer; padding: 10px; border-radius: 8px;}
    .tab-link.active { background: #111; color: var(--gold); border: 1px solid var(--border); }
</style>
"""

# --- LANDING PAGE (INICIO PÚBLICO) ---
LANDING_HTML = f"""
<html><head><title>Quick Money Voice - VOIP Anónimo</title>{CSS}</head>
<body>
    <header><div class="container"><div class="nav-wrapper">
        <div class="logo">🦁 QM VOICE</div>
        <div class="nav-links">
            <a href="#features">CARACTERÍSTICAS</a>
            <a href="/login" class="btn-dark btn" style="padding: 10px 20px;">INGRESAR</a>
            <a href="/register" class="btn-gold btn" style="padding: 10px 20px;">REGISTRO</a>
        </div>
    </div></div></header>

    <div class="hero"><div class="container">
        <h1>Llamadas VOIP <span class="text-gold">Totalmente Anónimas</span></h1>
        <p>Toma el control de tu Caller ID. Conecta con MicroSIP y llama sin restricciones. Privacidad absoluta, poder total.</p>
        <a href="/register" class="btn-gold btn" style="padding: 18px 40px; font-size:16px;">EMPEZAR AHORA</a>
    </div></div>

    <div id="features" class="container"><div class="feature-grid">
        <div class="card feature-card"><i>📞</i><h3>Spoofing Real</h3><p class="text-muted">Cambia tu Caller ID a cualquier número sin confirmación.</p></div>
        <div class="card feature-card"><i>🛡️</i><h3>Sin Registros</h3><p class="text-muted">Tu privacidad es nuestra prioridad. No guardamos registros de tus llamadas.</p></div>
        <div class="card feature-card"><i>🌐</i><h3>Soporte MicroSIP</h3><p class="text-muted">Usa MicroSIP en tu PC para llamadas estables y profesionales.</p></div>
    </div></div>
</body></html>
"""

# --- LOGIN / REGISTRO ---
AUTH_HTML = f"""
<html><head><title>{{{{ title }}}}</title>{CSS}</head>
<body style="display:flex; justify-content:center; align-items:center;">
    <div class="card" style="width:360px; text-align:center; border-top:4px solid var(--gold);">
        <h2 class="text-gold">{{{{ title }}}}</h2>
        {{% if error %}}<p style="color:#ff4757; font-size:12px;">{{{{ error }}}}</p>{{% endif %}}
        <form method="POST">
            <input name="u" placeholder="USUARIO" required>
            <input type="password" name="p" placeholder="PASS" required>
            <button class="btn-gold btn" style="width:100%">{{{{ title }}}}</button>
        </form>
        {{% if title == 'INGRESAR' %}}
            <p class="text-muted" style="font-size:12px;">¿No tienes cuenta? <a href="/register" class="text-gold">Regístrate</a></p>
        {{% else %}}
            <p class="text-muted" style="font-size:12px;">¿Ya tienes cuenta? <a href="/login" class="text-gold">Ingresa</a></p>
        {{% endif %}}
    </div>
</body></html>
"""

# --- DASHBOARD (PANEL DE USUARIO) ---
DASHBOARD_HTML = f"""
<html><head><title>Dashboard - Quick Money Voice</title>{CSS}</head>
<body>
    <header><div class="container"><div class="nav-wrapper">
        <div class="logo">🦁 QM VOICE</div>
        <div class="nav-links"><span class="badge-saldo">SALDO: ${{{{ saldo }}}}</span></div>
    </div></div></header>

    <div class="main-content"><div class="container">
        <div class="tab-nav">
            <div class="tab-link active" onclick="showTab('resumen')">📊 RESUMEN</div>
            <div class="tab-link" onclick="showTab('sip')">👤 CREDENCIALES SIP</div>
            <div class="tab-link" onclick="showTab('recarga')">💳 RECARGAR</div>
            <a href="/logout" class="nav-item btn-danger btn" style="margin-left:auto; padding: 10px 20px; font-size:12px;">CERRAR SESIÓN</a>
        </div>

        <div id="tab-resumen" class="tab-content">
            <div class="card" style="border-color:#2ecc71">
                <span class="text-gold" style="font-size:12px;">ESTADO DEL SERVIDOR: ONLINE ✅</span>
                <p style="font-size:12px; color:#888;">Tu línea está activa y lista para usar con MicroSIP.</p>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                <div class="card" style="text-align:center;">
                    <span class="text-muted">MINUTOS DISPONIBLES</span>
                    <h1 class="text-gold" style="font-size:48px; margin:10px 0;">{{{{ minutos }}}}</h1>
                </div>
                <div class="card" style="text-align:center;">
                    <span class="text-muted">CALLER ID ACTUAL</span>
                    <h1 style="font-size:48px; margin:10px 0;">{{{{ callerId }}}}</h1>
                </div>
            </div>
        </div>

        <div id="tab-sip" class="tab-content hidden">
            <div class="card">
                <span class="card-h text-gold">DATOS DE CONEXIÓN (MicroSIP)</span>
                <p class="text-muted" style="font-size:12px; margin-bottom:20px;">Copia estos datos en la configuración de cuenta de MicroSIP.</p>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; font-size:14px;">
                    <p><b>SIP Server:</b> <span class="text-gold">voice.quickmoney.online</span></p>
                    <p><b>Username:</b> <span class="text-gold">QM_{{{{ userId }}}}</span></p>
                    <p><b>Domain:</b> <span class="text-gold">voice.quickmoney.online</span></p>
                    <p><b>Password:</b> <span class="text-gold">**********</span></p>
                </div>
            </div>
        </div>

        <div id="tab-recarga" class="tab-content hidden">
            <div class="card" style="text-align:center;">
                <h3 class="text-gold">Recargar Balance</h3>
                <p class="text-muted">Para recargar minutos, por favor contacta con soporte.</p>
                <a href="https://t.me/mairo" class="btn-gold btn">CONTACTAR A MAIRO (TG)</a>
            </div>
        </div>

    </div></div>

    <script>
        function showTab(tab) {{
            document.querySelectorAll('.tab-content').forEach(t => t.classList.add('hidden'));
            document.querySelectorAll('.tab-link').forEach(n => n.classList.remove('active'));
            document.getElementById('tab-' + tab).classList.remove('hidden');
            event.currentTarget.classList.add('active');
        }}
    </script>
</body></html>
"""

# --- LÓGICA DEL SERVIDOR (BACKEND) ---
# Usamos base de datos local para esta versión de diseño
DB_FILE = 'voice_db.json'
def load_db():
    if not os.path.exists(DB_FILE):
        db = {"usuarios": {"mairo": {"pass": "1234", "saldo": 9999.0, "rango": "OWNER", "callerId": "911"}}}
        save_db(db); return db
    with open(DB_FILE, 'r') as f: return json.load(f)
def save_db(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

@app.route('/')
def index(): return render_template_string(LANDING_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u, p = request.form.get('u'), request.form.get('p')
        db = load_db()
        if u in db["usuarios"] and db["usuarios"][u]['pass'] == p:
            session['user'] = u; return redirect(url_for('dashboard'))
        error = "Usuario o contraseña incorrectos."
    return render_template_string(AUTH_HTML, title='INGRESAR', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        u, p = request.form.get('u'), request.form.get('p')
        db = load_db()
        if u and p and u not in db["usuarios"]:
            db["usuarios"][u] = {"pass": p, "saldo": 0.0, "rango": "VIP", "callerId": "0000000"}
            save_db(db); return redirect(url_for('login'))
        error = "El usuario ya existe."
    return render_template_string(AUTH_HTML, title='REGISTRO', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('login'))
    db = load_db()
    u_data = db["usuarios"][session['user']]
    # Simulación de minutos (Saldo / 0.10 por minuto, por ejemplo)
    minutos = round(u_data['saldo'] / 0.10, 2)
    return render_template_string(DASHBOARD_HTML, saldo=f"{u_data['saldo']:.2f}", minutos=f"{minutos:.2f}", callerId=u_data['callerId'], userId=session['user'].upper())

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
