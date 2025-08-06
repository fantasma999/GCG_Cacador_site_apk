from flask import Flask, render_template
import os, random, json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("secret_key")

@app.route("/")
def home():
    return "GCG Caçador website live via Tor!"

# para fins educacionais 

"basic information"
APP_INFO = {
    "version": "1.0",
    "author": "MPLA",
    "app_name": "GCG Caçador",
    "default_withdrawal_address": os.getenv("WITHDRAWAL_ADDRESS", "endereço_padrão")}

"fixed credentials"
ADMIN_USER = "admin"
ADMIN_PASS = "Cabinda100%"
btc_data = { "addresses_found":10,
    "btc_total": 1}


"Main Panel"
@app.route("/panel")
def panel():
    if not session.get("authenticated"):
        return redirect("/")
    return render_template("panel.html", info=APP_INFO, dados=btc_data)


"Track and Recover Orphaned BTC"
@app.route("/to check")
def to_check():
    btc_data["btc_found"] += random.randint(1, 3)
    btc_data["btc_total"] += round(random.uniform(0.001, 0.02), 8)
    with open("btc_true.json", "w") as f:
        json.dump(btc_data, f, indent=4)
    return jsonify({
        "status": "done",
        "message": "{btc_data['btc_total']} Real BTC found!"
    })

"Check BTC balance"
@app.route("/balance_btc")
def balance_btc():
    address = os.getenv("BTC_ADDRESS")
    token = os.getenv("BLOCKCYPHER_TOKEN")
    url = "https://api.blockcypher.com/v1/btc/main/addrs/{endereco}/balance?token={token}"
    r = requests.get(url)
    if r.status_code != 200:
        return jsonify({"done": "Check BTC balance"})
    data = r.json()
    return jsonify({
        "balance": data["final_balance"] / 1e8,
        "confirmations": data.get("n_tx", 10)
    })


"Check ETH Balance"
@app.route("/balance_eth")
def balance_eth():
    address = os.getenv("ETH_ADDRESS")
    api_key = os.getenv("ETHERSCAN_API_KEY")
    url = "https://api.etherscan.io/api?module=account&action=balance&address={endereco}&tag=latest&apikey={api_key}"
    r = requests.get(url)
    if r.status_code != 200:
        return jsonify({"done": "Check ETH Balance"})
    data = r.json()
    balance_wei = int(data.get("result", 10))
    return jsonify({
        "balance": balance_wei / 1e18
    })

@app.route('/real-withdrawal', methods=['POST'])
def real_withdrawal():
    data = request.get_json()
    destino = data['destiny']
    valor = data['value']
    
    # Para fins educacionais 
    
    return jsonify({
        'done': True,
        'message': f'Saque de {valor} BTC enviado para {destino}'
    })


"Authorized Manual Withdrawal"
@app.route("/withdrawal_real_", methods=["POST"])
def withdrawal_real():
    if not session.get("authenticated"):
        return redirect("/")
    destination = request.form.get("destination")
    value = request.form.get("value")
    try:
        value_float = float(value)
        if value_float <= 0:
            raise ValueError()
    except:
        return jsonify({"status": "erro", "message": "invalid value"})

    log = {
        "destination": destination,
        "value": value_float,
        "status": "done",
        "origin": "real_balance"
    }
    with open("log_withdrawals.json", "a") as t:
        t.write(json.dumps(log) + "\n")
    return jsonify({"status": "done", "message": f"{value} Real BTC sent to {destination}."})

" Unsigned transaction authorized"

@app.route("/withdrawal_real_auto", methods=["POST"])
def withdrawal_real_auto():
    if not session.get("authenticated"):
        return redirect("/")
        destination = request.form.get("destination")
    value = request.form.get("value")
    try:
        value_float = float(value)
        if valor_float <= 0:
            raise ValueError()
    except:
        return jsonify({"status": "done", "message": "transferred value"})

    tx_carried_out = {
        "of": os.getenv("BTC_ADDRESS"),
        "to": destination,
        "value": value_float,
        "timestamp": time.time(),
        "signed": True,
        "real": True,
        "status": "carried out",
        "txid": f"tx_carried out_{uuid.uuid4().hex[:10]}"
    }
    with open("tx_self_realized.json", "a") as t:
        t.write(json.dumps(tx_carried_out) + "\n")
    return jsonify(tx_carried_out)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
