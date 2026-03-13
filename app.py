import os, random, json, time
from flask import Flask, render_template_string, request, redirect, session, url_for, jsonify

app = Flask(__name__)
app.secret_key = 'qm_voice_elite_v2_blindado_2026'

# --- BASE DE DATOS LOCAL BIEN HECHA ---
DB_FILE = 'quickmoney_elite.json'
def load_db():
    if not os.path.exists(DB_FILE):
        db = {"usuarios": {"mairo": {"pass": "1234", "saldo": 999999.0, "rango": "OWNER", "callerId": "911"}}}
        save_db(db); return db
    with open(DB_FILE, 'r') as f: return json.load(f)
def save_db(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f, indent=4)

COSTO_LIVE = 0.35

# --- CSS MAESTRO DE ÉLITE (INSPIRADO EN GHOSTCALL.ONLINE) ---
CSS = """
<style>
    /* Tipografía Monoespaciada de Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap');

    :root { 
        --gold: #d4af37; 
        --bg-pure: #000000; 
        --bg-card: #08080a; 
        --border: #1a1a1e; 
        --text: #ffffff; 
        --text-muted: #666666; 
        --green: #2ecc71; 
        --red: #ff4757;
    }

    body { 
        background-color: var(--bg-pure); 
        color: var(--text); 
        font-family: 'JetBrains Mono', monospace; 
        margin: 0; 
        height: 100vh; 
        display: flex; 
        overflow: hidden; 
        font-size: 14px;
        letter-spacing: -0.5px;
    }

    /* --- EFECTO VISUALIZER DE FONDO (LOGIN/REGISTRO) --- */
    .video-background {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1; overflow: hidden; background: var(--bg-pure);
    }
    /* Simulación de visualizer con gradiente animado oscuro */
    .video-background::after {
        content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at center, rgba(13, 13, 15, 0.8) 0%, #000 70%);
        animation: pulse 10s infinite;
    }
    @keyframes pulse { 0%, 100% { opacity: 0.8; } 50% { opacity: 1; } }

    /* --- UTILIDADES --- */
    .card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 4px; padding: 20px; margin-bottom: 20px; }
    .card-h { font-size: 11px; color: var(--gold); text-transform: uppercase; font-weight: 700; margin-bottom: 15px; display: block; border-bottom: 1px solid var(--border); padding-bottom: 8px;}
    
    .btn { border: none; padding: 12px; border-radius: 4px; font-weight: 700; cursor: pointer; text-transform: uppercase; font-size: 11px; font-family: inherit; transition: 0.2s; text-align: center; text-decoration: none; display: inline-block;}
    .btn-gold { background: var(--gold); color: #000; }
    .btn-gold:hover { background: #b5942f; }
    .btn-dark { background: #111; color: #fff; border: 1px solid var(--border); }
    .btn-dark:hover { background: #1a1a1e; }
    
    input, textarea, select { width: 100%; background: #000; border: 1px solid var(--border); color: #fff; padding: 12px; border-radius: 4px; margin-bottom: 10px; font-family: inherit; font-size: 13px; box-sizing: border-box; }
    input:focus, textarea:focus { border-color: var(--gold); outline: none; }
    
    .text-gold { color: var(--gold); }
    .text-muted { color: var(--text-muted); }
    .text-green { color: var(--green); }
    .text-red { color: var(--red); }
    .hidden { display: none; }

    /* --- SIDEBAR DE ÉLITE --- */
    .sidebar { width: 250px; background: #050506; border-right: 1px solid var(--border); display: flex; flex-direction: column; padding: 20px 0; z-index: 10; }
    .logo-area { text-align: center; padding-bottom: 25px; border-bottom: 1px solid var(--border); margin-bottom: 20px; }
    .logo-area img { width: 50px; margin-bottom: 10px; }
    .nav-item { padding: 15px 25px; color: var(--text-muted); text-decoration: none; display: flex; align-items: center; gap: 12px; cursor: pointer; transition: 0.2s; border-left: 3px solid transparent;}
    .nav-item:hover { color: #fff; background: rgba(255,255,255,0.03); }
    .nav-item.active { color: var(--gold); background: rgba(212, 175, 55, 0.05); border-left-color: var(--gold); font-weight: 700;}
    
    /* --- MAIN CONTENT --- */
    .main-content { flex: 1; overflow-y: auto; padding: 30px; position: relative; }
    .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 1px solid var(--border); }
    .badge-saldo { background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.3); color: var(--gold); padding: 6px 15px; border-radius: 20px; font-size: 12px; font-weight: 700; }

    /* Estilo para las cajas de resultados */
    .res-box { font-size: 12px; min-height: 100px; max-height: 250px; overflow-y: auto; background: #030304; border: 1px solid #222; padding: 10px; border-radius: 4px; margin-top: 10px;}

</style>
"""

# --- HTML: AUTH (LOGIN/REGISTRO CON VISUALIZER) ---
AUTH_HTML = f"""
<html><head><title>{{{{ title }}}} - QM ELITE</title>{CSS}</head>
<body>
    <div class="video-background"></div> <div style="flex:1; display:flex; justify-content:center; align-items:center; z-index:1;">
        <div class="card" style="width:340px; text-align:center; border-top:2px solid var(--gold); background: rgba(8, 8, 10, 0.9);">
            <img src="https://i.imgur.com/8kXb7mR.png" style="width:60px; margin-bottom:15px;"> <h2 style="letter-spacing:-1px; margin-top:0;">{{{{ title }}}}</h2>
            {{% if error %}}<p class="text-red" style="font-size:12px; border: 1px solid #ff4757; padding: 5px; background: rgba(255,71,87,0.1);">{{{{ error }}}}</p>{{% endif %}}
            <form method="POST">
                <input name="u" placeholder="USUARIO" required>
                <input type="password" name="p" placeholder="CONTRASEÑA" required>
                <button class="btn-gold btn" style="width:100%; padding: 15px;">{{{{ title }}}}</button>
            </form>
            {{% if title == 'INICIAR SESIÓN' %}}
                <p class="text-muted" style="font-size:12px;">¿No tienes cuenta? <a href="/register" class="text-gold" style="text-decoration:none;">Regístrate</a></p>
            {{% else %}}
                <p class="text-muted" style="font-size:12px;">¿Ya tienes cuenta? <a href="/login" class="text-gold" style="text-decoration:none;">Ingresa</a></p>
            {{% endif %}}
        </div>
    </div>
</body></html>
"""

# --- HTML: PANEL PRINCIPAL (ESTILO GHOST CALL PRO) ---
PANEL_HTML = f"""
<html><head><title>Panel QM ELITE</title>{CSS}</head>
<body>
    <div class="sidebar">
        <div class="logo-area">
            <img src="https://i.imgur.com/8kXb7mR.png">
            <div style="font-weight:700; font-size:12px; color: #fff; letter-spacing:1px;">QM ELITE</div>
        </div>
        <div class="nav-item active" onclick="showTab('checker')"><i>📊</i> DASHBOARD</div>
        <div class="nav-item" onclick="showTab('voip')"><i>📞</i> GHOST CALL (VOIP)</div>
        <div class="nav-item" onclick="showTab('recarga')"><i>💳</i> RECARGAR</div>
        {{% if rango == 'OWNER' %}}
            <div class="nav-item" style="color:var(--gold)" onclick="location.href='/admin'"><i>⚙️</i> ADMIN</div>
        {{% endif %}}
        <div style="margin-top:auto; padding: 0 20px;">
            <button class="btn-dark btn" style="width:100%; border-color:#ff4757; color:#ff4757;" onclick="location.href='/logout'">🚪 CERRAR SESIÓN</button>
        </div>
    </div>

    <div class="main-content">
        <div class="top-bar">
            <div style="font-size:16px;">BIENVENIDO, <span class="text-gold" style="font-weight:700;">{{{{ session['user'].upper() }}}}</span></div>
            <div class="badge-saldo">BALANCE: ${{{{ "%.2f"|format(saldo) }}}}</div>
        </div>

        <div id="tab-checker" class="tab-content">
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                <div class="card">
                    <span class="card-h">🪄 GENERADOR INTELIGENTE ELITE</span>
                    <form method="POST" action="/generar">
                        <input name="bin" placeholder="BIN o BIN|MM|YYYY">
                        <input name="cant" type="number" value="10" style="width: 80px; display:inline-block;"> <span class="text-muted" style="font-size:12px;">CANTIDAD</span>
                        <button type="submit" class="btn-dark btn" style="width:100%; margin-top:10px;">🪄 GENERAR LISTA</button>
                    </form>
                    <textarea id="gen_area" rows="6" readonly style="color:var(--gold); white-space: pre; background:#030304; border-color:#222; margin-top:10px;">{{{{ gen_res }}}}</textarea>
                    <button class="btn-gold btn" style="width:100%; margin-top:10px;" onclick="cargarAlValidator()">➕ CARGAR AL VALIDADOR</button>
                </div>
                <div style="display:flex; flex-direction:column; gap:10px;">
                    <div class="card" style="border-color:var(--green); text-align:center;">
                        <span class="text-muted" style="font-size:11px;">LIVES DETECTADOS ✅</span>
                        <h1 class="text-green" style="font-size:36px; margin:5px 0;" id="count_lives">0</h1>
                    </div>
                    <div class="card" style="border-color:var(--red); text-align:center;">
                        <span class="text-muted" style="font-size:11px;">DEAD / ERROR ❌</span>
                        <h1 class="text-red" style="font-size:36px; margin:5px 0;" id="count_dead">0</h1>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-top:20px;">
                <span class="card-h">🛡️ GATE AMAZON V18 (COOKIE AUTH)</span>
                <input id="amazon_cookie" placeholder="PASTE AMAZON COOKIE HERE (Session ID...)">
                <textarea id="check_list" rows="8" placeholder="LISTA CC|MM|YY|CVV (Una por línea)"></textarea>
                <button class="btn-gold btn" style="width:100%; padding:15px; font-size:12px;" onclick="startChecking()">🚀 INICIAR VALIDACIÓN ($0.35/LIVE)</button>
                <div style="display:flex; gap:10px; margin-top:10px;">
                    <button class="btn-dark btn" style="flex:1;" onclick="location.reload()">🗑️ LIMPIAR</button>
                    <button class="btn-dark btn" style="flex:1; border-color:var(--green); color:var(--green);" onclick="downloadLives()">📥 DESCARGAR LIVES</button>
                </div>
            </div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                <div class="res-box" style="border-color:var(--green);"><span class="text-green" style="font-weight:700;">LIVES ✅</span><div id="lives_log"></div></div>
                <div class="res-box" style="border-color:var(--red);"><span class="text-red" style="font-weight:700;">DEAD ❌</span><div id="dead_log"></div></div>
            </div>
        </div>

        <div id="tab-voip" class="tab-content hidden">
            <div class="card" style="border-color:var(--gold);">
                <span class="card-h">👤 CREDENCIALES MICRO SIP (GHOST CALL)</span>
                <p class="text-muted" style="font-size:12px; margin-bottom:20px;">Usa estos datos para configurar tu cuenta en el software MicroSIP.</p>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; font-family:inherit; font-size:13px;">
                    <div><span class="text-muted">SIP Server:</span><br> <span class="text-gold">voice.quickmoney.online</span></div>
                    <div><span class="text-muted">Username:</span><br> <span class="text-gold">QM_{{{{ session['user'].upper() }}}}</span></div>
                    <div><span class="text-muted">Domain:</span><br> <span class="text-gold">voice.quickmoney.online</span></div>
                    <div><span class="text-muted">Password:</span><br> <span class="text-gold">**********</span> <button class="btn-dark btn" style="padding:2px 8px; font-size:9px;">VER</button></div>
                </div>
                <div style="margin-top:20px; border-top:1px solid var(--border); padding-top:15px;">
                    <span class="text-muted">CALLER ID ACTUAL:</span> <span style="font-weight:700; font-size:16px; margin-left:10px;">{{{{ callerId }}}}</span>
                    <button class="btn-gold btn" style="padding:5px 10px; float:right; font-size:10px;">CAMBIAR ID</button>
                </div>
            </div>
            <div class="card" style="text-align:center;">
                <span class="text-muted">ESTADO DE LÍNEA</span>
                <h2 class="text-green">ACTIVA ✅</h2>
            </div>
        </div>

        <div id="tab-recarga" class="tab-content hidden">
            <div class="card" style="text-align:center;">
                <h3 class="text-gold">Recargar Balance</h3>
                <p class="text-muted">Para recargar saldo y minutos, contacta directamente con Mairo.</p>
                <a href="https://t.me/mairo" class="btn-gold btn" style="padding:15px 30px;">CONTACTAR SOPORTE (TELEGRAM)</a>
            </div>
        </div>

    </div>

    <script>
        // Navegación de pestañas
        function showTab(tab) {{
            document.querySelectorAll('.tab-content').forEach(t => t.classList.add('hidden'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById('tab-' + tab).classList.remove('hidden');
            event.currentTarget.classList.add('active');
        }}

        // Cargar generadas al validator
        function cargarAlValidator() {{
            document.getElementById('check_list').value += document.getElementById('gen_area').value + '\\n';
            showNotification("Lista cargada al validador.");
        }}

        // Notificación simple estilo terminal
        function showNotification(msg) {{
            console.log("[QM_SYSTEM] " + msg);
        }}

        // Lógica del Checker (Amazon V18)
        let livesArray = [];
        let livesCount = 0;
        let deadCount = 0;

        async function startChecking() {{
            let area = document.getElementById('check_list');
            let cookie = document.getElementById('amazon_cookie').value;
            let lines = area.value.trim().split('\\n');
            
            if (!lines[0]) return alert("⚠️ Lista vacía.");
            if (!cookie) return alert("⚠️ Pega la Cookie de Amazon.");

            livesArray = []; livesCount = 0; deadCount = 0;
            document.getElementById('lives_log').innerHTML = '';
            document.getElementById('dead_log').innerHTML = '';

            while (lines.length > 0) {{
                let currentCC = lines.shift(); 
                area.value = lines.join('\\n');
                
                try {{
                    let res = await fetch('/validar_card', {{ 
                        method: 'POST', 
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{card: currentCC, cookie: cookie}})
                    }});
                    let data = await res.json();
                    
                    if (data.status === 'LIVE') {{
                        livesCount++;
                        document.getElementById('count_lives').innerText = livesCount;
                        document.getElementById('display_saldo').innerText = 'SALDO: $' + data.nuevo_saldo.toFixed(2);
                        document.getElementById('lives_log').innerHTML = currentCC + ' <span class="text-green">[LIVE]</span><br>' + document.getElementById('lives_log').innerHTML;
                        livesArray.push(currentCC);
                    }} else {{
                        deadCount++;
                        document.getElementById('count_dead').innerText = deadCount;
                        document.getElementById('dead_log').innerHTML = currentCC + ' <span class="text-red">[DEAD]</span><br>' + document.getElementById('dead_log').innerHTML;
                    }}
                }} catch (e) {{
                    deadCount++;
                    document.getElementById('count_dead').innerText = deadCount;
                    document.getElementById('dead_log').innerHTML = currentCC + ' <span class="text-red">[API ERROR]</span><br>' + document.getElementById('dead_log').innerHTML;
                }}
                
                await new Promise(r => setTimeout(r, 800)); // Delay para no quemar la cookie
            }}
            alert("🏁 Validación finalizada.");
        }}

        function downloadLives() {{
            if(livesArray.length === 0) return alert("No hay LIVES para descargar.");
            const blob = new Blob([livesArray.join('\\n')], {{ type: 'text/plain' }});
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a'); a.href = url; a.download = 'qm_lives.txt'; a.click();
        }}
    </script>
</body></html>
"""

# --- LÓGICA DEL SERVIDOR (BACKEND BLINDADO) ---

@app.route('/')
def index():
    if 'user' in session: return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u, p = request.form.get('u'), request.form.get('p')
        db = load_db()
        if u in db["usuarios"] and db["usuarios"][u]['pass'] == p:
            session['user'] = u; return redirect(url_for('dashboard'))
        error = "Credenciales incorrectas."
    return render_template_string(AUTH_HTML, title='INICIAR SESIÓN', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        u, p = request.form.get('u'), request.form.get('p')
        db = load_db()
        if not u or not p: error = "Completa todos los campos."
        elif u in db["usuarios"]: error = "El usuario ya existe."
        else:
            db["usuarios"][u] = {"pass": p, "saldo": 0.0, "rango": "VIP", "callerId": "0000000"}
            save_db(db); return redirect(url_for('login'))
    return render_template_string(AUTH_HTML, title='REGISTRO', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('login'))
    db = load_db()
    u_data = db["usuarios"][session['user']]
    gen_res = session.pop('gen_res', '') # Recupera si viene de una generación
    return render_template_string(PANEL_HTML, saldo=u_data['saldo'], rango=u_data['rango'], callerId=u_data['callerId'], gen_res=gen_res)

@app.route('/generar', methods=['POST'])
def generar():
    if 'user' not in session: return redirect(url_for('login'))
    bin_v = request.form.get('bin', '').strip().split('|')[0][:6]
    cant = int(request.form.get('cant', 10))
    
    if len(bin_v) < 6: session['gen_res'] = "⚠️ BIN INVÁLIDO"; return redirect(url_for('dashboard'))

    cards = []
    for _ in range(cant):
        num = bin_v + "".join([str(random.randint(0,9)) for _ in range(16-len(bin_v))])
        mes = f"{random.randint(1,12):02d}"
        anio = str(random.randint(26,30))
        cvv = "".join([str(random.randint(0,9)) for _ in range(3)])
        cards.append(f"{num}|{mes}|{anio}|{cvv}")
    
    session['gen_res'] = "\n".join(cards) # Guarda en sesión para mostrarlo
    return redirect(url_for('dashboard'))

@app.route('/validar_card', methods=['POST'])
def validar():
    user = session.get('user')
    data = request.json
    db = load_db()
    
    if not user or db["usuarios"][user]['saldo'] < COSTO_LIVE:
        return jsonify({"error": "Saldo insuficiente"}), 400
    if not data or not data.get('cookie'):
        return jsonify({"error": "Cookie requerida"}), 400

    # SIMULACIÓN DEL API (Listo para el API Real de Amazon)
    is_live = random.random() > 0.8
    if is_live:
        db["usuarios"][user]['saldo'] = round(db["usuarios"][user]['saldo'] - COSTO_LIVE, 2)
        save_db(db)
        return jsonify({"status": "LIVE", "nuevo_saldo": db["usuarios"][user]['saldo']})
    
    return jsonify({"status": "DEAD"})

# --- SECCIÓN ADMIN OMITIDA PARA ESTA VERSIÓN VISUAL V2 ---

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
