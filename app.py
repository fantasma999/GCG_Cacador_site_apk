from flask import Flask, render_template, request, session, redirect, jsonify
import os, random, json, time, uuid, requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")

# Informações básicas do app
APP_INFO = {
    "version": "1.0",
    "author": "MPLA",
    "app_name": "GCG Caçador",
    "default_withdrawal_address": os.getenv("WITHDRAWAL_ADDRESS", "endereço_padrão")
}

# Credenciais fixas
ADMIN_USER = "admin"
ADMIN_PASS = "Cabinda100%"

# Dados do BTC
btc_data = {
    "enderecos_encontrados": 10,
    "btc_total": 1
}

@app.route("/")
def home():
    if session.get("authenticated"):
        return redirect("/panel")
    return render_template("index.html")

@app.route("/", methods=["POST"])
def login():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    if usuario == ADMIN_USER and senha == ADMIN_PASS:
        session["authenticated"] = True
        return redirect("/panel")
    else:
        return render_template("index.html", erro="Credenciais inválidas")

@app.route("/panel")
def panel():
    if not session.get("authenticated"):
        return redirect("/")
    return render_template("painel.html", info=APP_INFO, dados=btc_data)

@app.route("/verificar")
def verificar():
    if not session.get("authenticated"):
        return redirect("/")
    btc_data["enderecos_encontrados"] += random.randint(1, 3)
    btc_data["btc_total"] += round(random.uniform(0.001, 0.02), 8)
    with open("btc_true.json", "w") as f:
        json.dump(btc_data, f, indent=4)
    return redirect("/panel")

@app.route("/balance_btc")
def balance_btc():
    if not session.get("authenticated"):
        return redirect("/")
    address = os.getenv("BTC_ADDRESS")
    token = os.getenv("BLOCKCYPHER_TOKEN")

    return jsonify({
        "balance": 0.5,
        "confirmations": 10
    })

@app.route("/balance_eth")
def balance_eth():
    if not session.get("authenticated"):
        return redirect("/")
    return jsonify({
        "balance": 1.2
    })

@app.route('/real-withdrawal', methods=['POST'])
def real_withdrawal():
    if not session.get("authenticated"):
        return jsonify({"done": False, "error": "Não autenticado"})

    data = request.get_json()
    destino = data.get('destiny')
    valor = data.get('value')

    # Para fins educacionais
    return jsonify({
        'done': True,
        'message': f'Saque de {valor} BTC enviado para {destino}'
    })

@app.route("/sacar", methods=["POST"])
def sacar():
    if not session.get("authenticated"):
        return redirect("/")
    endereco = request.form.get("endereco")

    log = {
        "destination": endereco,
        "value": btc_data["btc_total"],
        "status": "concluído",
        "timestamp": time.time()
    }

    with open("log_withdrawals.json", "a") as f:
        f.write(json.dumps(log) + "\n")

    return redirect("/panel")

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)