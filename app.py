
from flask import Flask, render_template, request, redirect, session, jsonify
import os, random, json, time, uuid
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "sua_chave_secreta_aqui")

# Informações básicas da aplicação
APP_INFO = {
    "version": "1.0",
    "author": "MPLA",
    "app_name": "GCG Caçador",
    "default_withdrawal_address": os.getenv("WITHDRAWAL_ADDRESS", "endereço_padrão")
}

# Credenciais fixas
ADMIN_USER = "admin"
ADMIN_PASS = "Cabinda100%"

# Dados BTC simulados
btc_data = {
    "enderecos_encontrados": 10,
    "btc_total": 1.0783
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def login():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    
    if usuario == ADMIN_USER and senha == ADMIN_PASS:
        session["authenticated"] = True
        return redirect("/painel")
    else:
        return render_template("index.html", erro="Usuário ou senha incorretos")

@app.route("/painel")
def painel():
    if not session.get("authenticated"):
        return redirect("/")
    return render_template("painel.html", info=APP_INFO, dados=btc_data)

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect("/")

@app.route("/verificar")
def verificar():
    if not session.get("authenticated"):
        return redirect("/")
    
    btc_data["enderecos_encontrados"] += random.randint(1, 3)
    btc_data["btc_total"] += round(random.uniform(0.001, 0.02), 8)
    
    # Salvar dados em arquivo JSON
    with open("btc_data.json", "w") as f:
        json.dump(btc_data, f, indent=4)
    
    return jsonify({
        "status": "sucesso",
        "message": f"{btc_data['btc_total']} BTC Real encontrado!",
        "dados": btc_data
    })

@app.route("/sacar", methods=["POST"])
def sacar():
    if not session.get("authenticated"):
        return redirect("/")
    
    endereco = request.form.get("endereco")
    
    if not endereco:
        return jsonify({"status": "erro", "message": "Endereço é obrigatório"})
    
    # Log da transação
    log = {
        "endereco_destino": endereco,
        "valor": btc_data["btc_total"],
        "status": "concluído",
        "timestamp": time.time(),
        "tipo": "saque_total"
    }
    
    with open("log_saques.json", "a") as f:
        f.write(json.dumps(log) + "\n")
    
    return jsonify({
        "status": "sucesso", 
        "message": f"{btc_data['btc_total']} BTC enviado para {endereco}"
    })

@app.route("/real-withdrawal", methods=["POST"])
def real_withdrawal():
    if not session.get("authenticated"):
        return jsonify({"done": False, "error": "Não autenticado"})
    
    data = request.get_json()
    destino = data.get('destiny')
    valor = data.get('value')
    
    if not destino or not valor:
        return jsonify({"done": False, "error": "Destino e valor são obrigatórios"})
    
    try:
        valor_float = float(valor)
        if valor_float <= 0:
            raise ValueError("Valor deve ser positivo")
    except (ValueError, TypeError):
        return jsonify({"done": False, "error": "Valor inválido"})
    
    # Log da transação
    log = {
        "endereco_destino": destino,
        "valor": valor_float,
        "status": "concluído",
        "timestamp": time.time(),
        "tipo": "saque_parcial",
        "txid": f"tx_{uuid.uuid4().hex[:10]}"
    }
    
    with open("log_saques.json", "a") as f:
        f.write(json.dumps(log) + "\n")
    
    return jsonify({
        "done": True,
        "message": f"Saque de {valor} BTC enviado para {destino}",
        "txid": log["txid"]
    })

@app.route("/balance_btc")
def balance_btc():
    if not session.get("authenticated"):
        return redirect("/")
    
    # Simulação de consulta de saldo
    return jsonify({
        "balance": btc_data["btc_total"],
        "confirmations": random.randint(6, 50),
        "status": "ativo"
    })

@app.route("/balance_eth")
def balance_eth():
    if not session.get("authenticated"):
        return redirect("/")
    
    # Simulação de saldo ETH
    return jsonify({
        "balance": round(random.uniform(0.1, 5.0), 6),
        "status": "ativo"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
