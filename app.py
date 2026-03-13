import os, random, json
from flask import Flask, render_template_string, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'houdini_ghost_elite_2026'

# --- BASE DE DATOS ---
DB_FILE = 'ghost_data.json'
def load_db():
    if not os.path.exists(DB_FILE):
        db = {"usuarios": {"mairo": {"pass": "1234", "minutos": 1000.0, "status": "Activa", "callerId": "07874525533", "sip_user": "QM_MAIRO", "sip_pass": "QM99x7"}}}
        save_db(db); return db
    with open(DB_FILE, 'r') as f: return json.load(f)
def save_db(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

# --- CSS HOUDINI CUSTOM COLORS ---
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap');
    :root { --gold: #e2b04a; --bg: #000000; --card: #0a0a0b; --border: #161618; --text-muted: #555; }
    
    body { background: var(--bg); color: #fff; font-family: 'JetBrains Mono', monospace; margin: 0; padding: 0; min-height: 100vh; overflow-x: hidden; }
    .container { max-width: 420px; margin: 0 auto; padding: 20px; transition: 0.4s; }
    
    /* MENU OVERLAY */
    .overlay-menu { position: fixed; top: 0; left: -100%; width: 85%; height: 100%; background: #050505; z-index: 1000; transition: 0.4s; border-right: 1px solid var(--border); padding: 50px 25px; box-sizing: border-box; }
    .overlay-menu.active { left: 0; }
    .nav-item { padding: 18px 0; border-bottom: 1px solid var(--border); color: #666; text-decoration: none; display: block; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; cursor: pointer;}
    .nav-item:hover { color: var(--gold); }

    /* HEADER */
    .header { display: flex; justify-content: space-between; align-items: center; padding: 20px; background: rgba(0,0,0,0.9); backdrop-filter: blur(15px); position: sticky; top: 0; z-index: 900; border-bottom: 1px solid var(--border); }
    .logo-houdini { width: 30px; height: 30px; border-radius: 50%; border: 1px solid var(--gold); }

    /* DASHBOARD ELEMENTS */
    .card { background: var(--card); border: 1px solid var(--border); padding: 22px; border-radius: 2px; margin-bottom: 15px; position: relative; }
    .card-label { font-size: 9px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; }
    .big-value { font-size: 32px; font-weight: 700; color: #fff; margin: 8px 0; }
    
    /* ACCIONES RÁPIDAS INTERACTIVAS */
    .action-btn { background: var(--card); border: 1px solid var(--border); padding: 20px; border-radius: 2px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; cursor: pointer; transition: 0.3s; }
    .action-btn:hover { border-color: var(--gold); background: #0d0d0f; }
    .action-title { font-weight: 700; font-size: 13px; display: block; margin-bottom: 4px; }
    .action-desc { font-size: 10px; color: var(--text-muted); }

    /* BOTONES Y INPUTS */
    .btn-gold { background: var(--gold); color: #000; border: none; width: 100%; padding: 18px; font-weight: 700; text-transform: uppercase; cursor: pointer; border-radius: 2px; letter-spacing: 1px; }
    input { width: 100%; background: #000; border: 1px solid var(--border); color: var(--gold); padding: 16px; font-family: inherit; margin-bottom: 20px; border-radius: 2px; box-sizing: border-box; }
    
    .status-badge { background: #0a0a0a; border: 1px solid var(--border); padding: 6px 14px; border-radius: 2px; display: inline-flex; align-items: center; font-size: 9px; color: #666; letter-spacing: 1px; margin-bottom: 20px; }
    .dot { width: 6px; height: 6px; background: var(--gold); border-radius: 50%; display: inline-block; margin-right: 10px; box-shadow: 0 0 12px var(--gold); }
    
    .tab-content { animation: fadeIn 0.5s ease; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
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
            <img src="https://i.imgur.com/8kXb7mR.png" style="width: 70px; border-radius: 50%; border: 2px solid var(--gold); padding: 5px; margin-bottom: 25px;">
            <div class="status-badge"><span class="dot"></span> HOUDINI ACCESS</div>
            <h1 style="font-weight: 400; font-size: 26px; margin-bottom: 40px; letter-spacing: -1px;">Iniciar <i style="font-weight: 700; color:var(--gold);">Sesión</i></h1>
            <form method="POST" action="/auth" style="text-align: left;">
                <input name="u" placeholder="USUARIO" required>
                <input name="p" type="password" placeholder="CONTRASEÑA" required>
                <button class="btn-gold">[ INICIAR SESIÓN ]</button>
            </form>
            <p style="font-size: 10px; color: #333; margin-top: 40px; letter-spacing: 1px;">¿SIN CUENTA? CONTACTA POR TELEGRAM</p>
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
            <div style="font-weight: 700; margin-bottom: 50px; color: var(--gold); font-size: 14px; letter-spacing: 2px;">🦁 QUICK MONEY PRO</div>
            <div class="nav-item" onclick="switchTab('dash')">DASHBOARD</div>
            <div class="nav-item" onclick="switchTab('caller')">CALLER ID</div>
            <div class="nav-item" onclick="switchTab('dtmf')">DTMF KEYPAD</div>
            <div class="nav-item" onclick="switchTab('recarga')">RECARGAR</div>
            <div class="nav-item" onclick="switchTab('sip')">MI CUENTA (SIP)</div>
            <a href="/logout" class="nav-item" style="color: #ff4757; margin-top: 60px; border:none;">CERRAR SESIÓN</a>
        </div>

        <div class="header">
            <img src="https://i.imgur.com/8kXb7mR.png" class="logo-houdini">
            <div style="font-size: 10px; letter-spacing: 2px; font-weight: 700;">HOUDINI PRO</div>
            <div style="font-size: 24px; cursor: pointer;" onclick="toggleMenu()">☰</div>
        </div>

        <div class="container" id="mainContainer">
            <div id="tab-dash" class="tab-content">
                <div class="status-badge"><span class="dot"></span> DASHBOARD ACTIVE</div>
                <div style="font-size: 20px; margin-bottom: 30px;">Buenos días, <span style="color:var(--gold);">{session['user']}</span></div>
                
                <div class="card">
                    <span class="card-label">MINUTOS <span style="color:var(--gold)">🕒</span></span>
                    <div class="big-value">{u['minutos']}</div>
                </div>
                <div class="card" onclick="switchTab('caller')" style="cursor:pointer">
                    <span class="card-label">CALLER ID <span style="color:var(--gold)">📞</span></span>
                    <div class="big-value">{u['callerId']}</div>
                </div>

                <div style="margin-top: 35px;">
                    <div class="action-btn" onclick="switchTab('caller')">
                        <div><span class="action-title">Cambiar Caller ID</span><span class="action-desc">Spoofing instantáneo</span></div>
                        <span style="color:var(--gold)">📞</span>
                    </div>
                    <div class="action-btn" onclick="switchTab('recarga')">
                        <div><span class="action-title">Recargar Balance</span><span class="action-desc">Añadir minutos</span></div>
                        <span style="color:var(--gold)">↗️</span>
                    </div>
                </div>
            </div>

            <div id="tab-caller" class="tab-content hidden">
                <div class="status-badge"><span class="dot"></span> CALLER ID CONFIG</div>
                <div class="card">
                    <span class="card-label">NUEVO CALLER ID</span>
                    <input type="text" placeholder="+1 (800) 000-0000" id="new_id">
                    <button class="btn-gold" onclick="updateID()">ACTUALIZAR IDENTIDAD</button>
                </div>
                <button class="btn-gold" style="background:#111; color:#fff; margin-top:10px;" onclick="switchTab('dash')">VOLVER</button>
            </div>

            <div id="tab-sip" class="tab-content hidden">
                <div class="status-badge"><span class="dot"></span> SIP CREDENTIALS</div>
                <div class="card">
                    <span class="card-label">MICRO SIP CONFIG</span>
                    <div style="font-size: 12px; line-height: 2.5; color:#888;">
                        USER: <span style="color:#fff">{u['sip_user']}</span><br>
                        PASS: <span style="color:#fff">{u['sip_pass']}</span><br>
                        HOST: <span style="color:#fff">voice.quickmoney.pro</span>
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

            function updateID() {{
                const val = document.getElementById('new_id').value;
                if(val) {{
                    alert("Caller ID actualizado a: " + val);
                    switchTab('dash');
                }}
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
