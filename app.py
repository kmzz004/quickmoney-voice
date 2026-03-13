import os, random, json
from flask import Flask, render_template_string, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'ghost_call_pro_ultra_final_2026'

# --- BASE DE DATOS LOCAL ---
DB_FILE = 'ghost_data.json'

def load_db():
    if not os.path.exists(DB_FILE):
        db = {"usuarios": {"mairo": {"pass": "1234", "minutos": 1000.0, "status": "Activa", "callerId": "07874525533", "sip_user": "QM_MAIRO", "sip_pass": "QM99x7"}}}
        save_db(db); return db
    with open(DB_FILE, 'r') as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

# --- CSS DE ÉLITE (CALIDAD GHOSTCALL.ONLINE) ---
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap');
    :root { --gold: #d4af37; --bg: #000000; --card: #080809; --border: #151517; --text-muted: #555; }
    
    body { background: var(--bg); color: #fff; font-family: 'JetBrains Mono', monospace; margin: 0; padding: 0; min-height: 100vh; font-size: 14px; -webkit-tap-highlight-color: transparent; }
    .container { max-width: 420px; margin: 0 auto; padding: 20px; }
    
    /* SIDEBAR / MENU */
    .overlay-menu { position: fixed; top: 0; left: -100%; width: 80%; height: 100%; background: #050505; z-index: 1000; transition: 0.4s; border-right: 1px solid var(--border); padding: 40px 20px; box-sizing: border-box; }
    .overlay-menu.active { left: 0; }
    .nav-item { padding: 20px 0; border-bottom: 1px solid var(--border); color: #888; text-decoration: none; display: block; font-size: 12px; letter-spacing: 1px; }
    .nav-item.active { color: var(--gold); }

    /* CABECERA */
    .header { display: flex; justify-content: space-between; align-items: center; padding: 20px; background: rgba(0,0,0,0.8); backdrop-filter: blur(10px); position: sticky; top: 0; z-index: 900; border-bottom: 1px solid var(--border); }
    .logo-img { width: 35px; }
    .menu-trigger { font-size: 24px; cursor: pointer; }

    /* DASHBOARD CARDS */
    .card { background: var(--card); border: 1px solid var(--border); padding: 20px; border-radius: 4px; margin-bottom: 15px; position: relative; }
    .card-label { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between; }
    .big-value { font-size: 34px; font-weight: 700; color: #fff; margin: 10px 0; }
    .sub-info { font-size: 11px; color: #333; }

    /* ACCIONES RÁPIDAS */
    .action-btn { background: var(--card); border: 1px solid var(--border); padding: 20px; border-radius: 4px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; cursor: pointer; text-decoration: none; color: #fff; }
    .action-btn:hover { border-color: var(--gold); }
    .action-title { font-weight: 700; font-size: 13px; display: block; margin-bottom: 4px; }
    .action-desc { font-size: 11px; color: var(--text-muted); }

    /* FORMULARIOS */
    input { width: 100%; background: #050505; border: 1px solid var(--border); color: var(--gold); padding: 15px; font-family: inherit; margin-bottom: 20px; border-radius: 4px; box-sizing: border-box; }
    .btn-gold { background: linear-gradient(to right, #d4af37, #b5942f); color: #000; border: none; width: 100%; padding: 18px; font-weight: 700; text-transform: uppercase; cursor: pointer; border-radius: 4px; }
    
    .status-badge { background: #0a0a0a; border: 1px solid var(--border); padding: 5px 12px; border-radius: 20px; display: inline-flex; align-items: center; font-size: 10px; color: #888; margin-bottom: 20px; }
    .dot { width: 6px; height: 6px; background: var(--gold); border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px var(--gold); }
    
    .hidden { display: none; }
</style>
"""

@app.route('/')
def login():
    if 'user' in session: return redirect(url_for('dashboard'))
    return render_template_string(f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">{CSS}</head>
    <body style="display:flex; align-items:center; justify-content:center;">
        <div class="container" style="text-align: center;">
            <img src="https://i.imgur.com/8kXb7mR.png" style="width: 70px; margin-bottom: 20px;">
            <div class="status-badge"><span class="dot"></span> ACCESO AL PANEL</div>
            <h1 style="font-weight: 300; font-size: 28px; margin-bottom: 40px;">Iniciar <i style="font-weight: 700;">Sesión</i></h1>
            <form method="POST" action="/auth" style="text-align: left;">
                <label style="font-size: 10px; color: #444; margin-bottom: 8px; display: block;">USUARIO</label>
                <input name="u" required>
                <label style="font-size: 10px; color: #444; margin-bottom: 8px; display: block;">CONTRASEÑA</label>
                <input name="p" type="password" required>
                <button class="btn-gold">[ INICIAR SESIÓN ]</button>
            </form>
            <p style="font-size: 11px; color: #333; margin-top: 30px;">¿No tienes cuenta? <a href="#" style="color:var(--gold); text-decoration:none;">Contacta por Telegram</a></p>
        </div>
    </body></html>
    """)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('login'))
    db = load_db()
    u = db["usuarios"][session['user']]
    return render_template_string(f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">{CSS}</head>
    <body>
        <div id="sideMenu" class="overlay-menu">
            <div style="font-weight: 700; margin-bottom: 40px; color: var(--gold);">🦁 QUICK MONEY PRO</div>
            <a href="javascript:void(0)" class="nav-item active" onclick="closeMenu()">DASHBOARD</a>
            <a href="#" class="nav-item">CALLER ID</a>
            <a href="#" class="nav-item">DTMF</a>
            <a href="#" class="nav-item">RECARGAR</a>
            <a href="#" class="nav-item">MI CUENTA</a>
            <a href="https://t.me/mairo" class="nav-item">SOPORTE</a>
            <a href="/logout" class="nav-item" style="color: #ff4757; margin-top: 50px;">CERRAR SESIÓN</a>
        </div>

        <div class="header">
            <img src="https://i.imgur.com/8kXb7mR.png" class="logo-img">
            <div class="menu-trigger" onclick="openMenu()">☰</div>
        </div>

        <div class="container">
            <div style="margin-bottom: 30px;">
                <div class="status-badge"><span class="dot"></span> DASHBOARD</div>
                <div style="font-size: 22px;">Buenos días, <span style="font-style: italic;">{session['user']}</span></div>
                <div style="font-size: 11px; color: #444; margin-top: 5px;">Bienvenido a tu panel de control Ghost Call Pro</div>
            </div>

            <div class="card">
                <span class="card-label">MINUTOS DISPONIBLES <span style="color:var(--gold)">🕒</span></span>
                <div class="big-value" style="color:var(--gold);">{u['minutos']}</div>
                <div class="sub-info">minutos restantes</div>
            </div>

            <div class="card">
                <span class="card-label">CALLER ID ACTUAL <span style="color:var(--gold)">📞</span></span>
                <div class="big-value">{u['callerId']}</div>
                <div class="sub-info">número de identificación</div>
            </div>

            <div class="card">
                <span class="card-label">ESTADO DE CUENTA <span style="color:var(--gold)">👤</span></span>
                <div class="big-value">{u['status']}</div>
                <div class="sub-info">cuenta verificada</div>
            </div>

            <div style="margin-top: 40px;">
                <span class="card-label">Acciones Rápidas</span>
                <div class="action-btn">
                    <div><span class="action-title">Cambiar Caller ID</span><span class="action-desc">Actualiza tu número de identificación</span></div>
                    <span style="color:var(--gold)">📞</span>
                </div>
                <div class="action-btn">
                    <div><span class="action-title">Recargar Balance</span><span class="action-desc">Agrega más minutos a tu cuenta</span></div>
                    <span style="color:var(--gold)">↗️</span>
                </div>
            </div>

            <div class="card" style="margin-top: 30px; border-style: dashed; border-color: #222;">
                <span class="card-label">INFORMACIÓN DE CUENTA (SIP)</span>
                <div style="font-size: 12px; line-height: 2;">
                    USUARIO: <span style="color:var(--gold)">{u['sip_user']}</span><br>
                    CONTRASEÑA: <span style="color:var(--gold)">{u['sip_pass']}</span><br>
                    SERVIDOR: <span style="color:var(--gold)">voice.quickmoney.pro</span>
                </div>
            </div>
        </div>

        <script>
            function openMenu() {{ document.getElementById("sideMenu").classList.add("active"); }}
            function closeMenu() {{ document.getElementById("sideMenu").classList.remove("active"); }}
        </script>
    </body></html>
    """)

@app.route('/auth', methods=['POST'])
def auth():
    u, p = request.form.get('u'), request.form.get('p')
    db = load_db()
    if u in db["usuarios"] and db["usuarios"][u]['pass'] == p:
        session['user'] = u
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
