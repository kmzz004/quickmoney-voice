import os, random, json
from flask import Flask, render_template_string, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'quick_money_houdini_v4_2026'

# --- BASE DE DATOS ---
DB_FILE = 'voice_data.json'
def load_db():
    if not os.path.exists(DB_FILE):
        db = {"usuarios": {"mairo": {"pass": "1234", "minutos": 1000.0, "status": "Activa", "callerId": "07874525533", "sip_user": "QM_MAIRO", "sip_pass": "QM99x7"}}}
        save_db(db); return db
    with open(DB_FILE, 'r') as f: return json.load(f)
def save_db(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

# --- CSS PERSONALIZADO (Quick Money Style) ---
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap');
    :root { --gold: #c5a059; --bg: #000000; --card: #09090a; --border: #141416; }
    
    body { background: var(--bg); color: #fff; font-family: 'JetBrains Mono', monospace; margin: 0; padding: 0; min-height: 100vh; overflow-x: hidden; }
    .container { max-width: 400px; margin: 0 auto; padding: 20px; transition: 0.3s; }
    
    /* LOGO HOUDINI CIRCULAR */
    .houdini-logo { width: 85px; height: 85px; border-radius: 50%; border: 2px solid var(--gold); padding: 4px; margin-bottom: 20px; box-shadow: 0 0 15px rgba(197, 160, 89, 0.2); }
    .houdini-mini { width: 32px; height: 32px; border-radius: 50%; border: 1px solid var(--gold); }

    /* MENU LATERAL */
    .overlay-menu { position: fixed; top: 0; left: -100%; width: 80%; height: 100%; background: #050505; z-index: 1000; transition: 0.4s; border-right: 1px solid var(--border); padding: 50px 25px; box-sizing: border-box; }
    .overlay-menu.active { left: 0; }
    .nav-item { padding: 18px 0; border-bottom: 1px solid var(--border); color: #555; text-decoration: none; display: block; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; cursor: pointer;}
    .nav-item:hover, .nav-item.active { color: var(--gold); }

    /* HEADER */
    .header { display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; background: rgba(0,0,0,0.9); backdrop-filter: blur(10px); position: sticky; top: 0; z-index: 900; border-bottom: 1px solid var(--border); }

    /* CARDS */
    .card { background: var(--card); border: 1px solid var(--border); padding: 22px; border-radius: 2px; margin-bottom: 15px; }
    .card-label { font-size: 9px; color: #444; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; }
    .big-value { font-size: 30px; font-weight: 700; color: #fff; margin: 5px 0; }
    
    /* BOTONES */
    .btn-gold { background: var(--gold); color: #000; border: none; width: 100%; padding: 18px; font-weight: 700; text-transform: uppercase; cursor: pointer; border-radius: 2px; font-family: inherit; font-size: 12px; }
    input { width: 100%; background: #000; border: 1px solid var(--border); color: var(--gold); padding: 16px; font-family: inherit; margin-bottom: 20px; border-radius: 2px; box-sizing: border-box; }
    
    .status-badge { background: #080808; border: 1px solid var(--border); padding: 6px 14px; border-radius: 2px; display: inline-flex; align-items: center; font-size: 9px; color: #555; letter-spacing: 1px; margin-bottom: 25px; }
    .dot { width: 6px; height: 6px; background: var(--gold); border-radius: 50%; display: inline-block; margin-right: 10px; box-shadow: 0 0 10px var(--gold); }
    
    .action-btn { background: var(--card); border: 1px solid var(--border); padding: 20px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; cursor: pointer; }
    .tab-content { animation: fadeIn 0.4s ease; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
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
            <img src="https://i.imgur.com/eYn5vA6.png" class="houdini-logo"> <div class="status-badge"><span class="dot"></span> ACCESO AL PANEL</div>
            <h1 style="font-weight: 400; font-size: 26px; margin-bottom: 40px;">Iniciar <i style="font-weight: 700;">Sesión</i></h1>
            <form method="POST" action="/auth" style="text-align: left;">
                <label style="font-size: 10px; color: #333; margin-bottom: 8px; display: block;">USUARIO</label>
                <input name="u" required autocomplete="off">
                <label style="font-size: 10px; color: #333; margin-bottom: 8px; display: block;">CONTRASEÑA</label>
                <input name="p" type="password" required>
                <button class="btn-gold">[ INICIAR SESIÓN ]</button>
            </form>
            <p style="font-size: 10px; color: #222; margin-top: 40px; letter-spacing: 1px;">QUICK MONEY © 2026</p>
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
            <div style="font-weight: 700; margin-bottom: 50px; color: var(--gold); font-size: 13px; letter-spacing: 2px;">🦁 QUICK MONEY</div>
            <div class="nav-item active" onclick="switchTab('dash')">DASHBOARD</div>
            <div class="nav-item" onclick="switchTab('caller')">CALLER ID</div>
            <div class="nav-item" onclick="switchTab('sip')">MI CUENTA</div>
            <div class="nav-item" onclick="switchTab('recarga')">RECARGAR</div>
            <a href="/logout" class="nav-item" style="color: #ff4757; margin-top: 50px; border: none;">CERRAR SESIÓN</a>
        </div>

        <div class="header">
            <img src="https://i.imgur.com/eYn5vA6.png" class="houdini-mini">
            <div style="font-size: 11px; letter-spacing: 2px; font-weight: 700; color:var(--gold);">QUICK MONEY</div>
            <div style="font-size: 22px; cursor: pointer;" onclick="toggleMenu()">☰</div>
        </div>

        <div class="container" id="mainContainer">
            <div id="tab-dash" class="tab-content">
                <div class="status-badge"><span class="dot"></span> DASHBOARD</div>
                <div style="font-size: 22px; margin-bottom: 30px;">Buenos días, <span style="font-style: italic;">{session['user']}</span></div>
                
                <div class="card">
                    <span class="card-label">MINUTOS DISPONIBLES <span style="color:var(--gold)">🕒</span></span>
                    <div class="big-value" style="color:var(--gold)">{u['minutos']}</div>
                    <div style="font-size: 10px; color: #333;">minutos restantes</div>
                </div>

                <div class="card">
                    <span class="card-label">CALLER ID ACTUAL <span style="color:var(--gold)">📞</span></span>
                    <div class="big-value">{u['callerId']}</div>
                    <div style="font-size: 10px; color: #333;">número de identificación</div>
                </div>

                <div style="margin-top: 40px;">
                    <div class="action-btn" onclick="switchTab('caller')">
                        <div><b style="display:block; font-size:13px;">Cambiar Caller ID</b><span style="font-size:10px; color:#444;">Actualiza tu identidad</span></div>
                        <span style="color:var(--gold)">📞</span>
                    </div>
                    <div class="action-btn" onclick="switchTab('recarga')">
                        <div><b style="display:block; font-size:13px;">Recargar Balance</b><span style="font-size:10px; color:#444;">Añadir más minutos</span></div>
                        <span style="color:var(--gold)">↗️</span>
                    </div>
                </div>
            </div>

            <div id="tab-caller" class="tab-content hidden">
                <div class="status-badge"><span class="dot"></span> SPOOFING CONFIG</div>
                <div class="card">
                    <span class="card-label">NUEVA IDENTIDAD</span>
                    <input type="text" id="target_id" placeholder="EJ: +18005550199">
                    <button class="btn-gold" onclick="alert('Identidad actualizada con éxito.')">ACTUALIZAR ID</button>
                </div>
                <button class="btn-gold" style="background:#111; color:#fff; margin-top:10px;" onclick="switchTab('dash')">VOLVER AL PANEL</button>
            </div>

            <div id="tab-sip" class="tab-content hidden">
                <div class="status-badge"><span class="dot"></span> CREDENCIALES SIP</div>
                <div class="card">
                    <span class="card-label">CONFIGURACIÓN MICROSIP</span>
                    <div style="font-size: 12px; line-height: 2.5; color:#555;">
                        USUARIO: <span style="color:#fff">{u['sip_user']}</span><br>
                        CLAVE: <span style="color:#fff">{u['sip_pass']}</span><br>
                        SERVIDOR: <span style="color:#fff">voice.quickmoney.pro</span>
                    </div>
                </div>
                <button class="btn-gold" style="background:#111; color:#fff;" onclick="switchTab('dash')">VOLVER</button>
            </div>
        </div>

        <script>
            function toggleMenu() {{ document.getElementById("sideMenu").classList.toggle("active"); }}
            
            function switchTab(tabId) {{
                document.querySelectorAll('.tab-content').forEach(t => t.classList.add('hidden'));
                document.getElementById('tab-' + tabId).classList.remove('hidden');
                document.getElementById("sideMenu").classList.remove("active");
                window.scrollTo(0,0);
            }}
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
def logout(): session.clear(); return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
