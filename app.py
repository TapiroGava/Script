from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

STOCKS_FILE = "stocks.json"

def load_stocks():
    try:
        with open(STOCKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"stocks": []}

def save_stocks(data):
    with open(STOCKS_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def index():
    stocks = load_stocks()["stocks"]
    return render_template("index.html", stocks=stocks)

@app.route("/add", methods=["POST"])
def add_stock():
    symbol = request.form.get("symbol")
    target_price = float(request.form.get("target_price"))
    stocks_data = load_stocks()
    stocks_data["stocks"].append({"symbol": symbol, "target_price": target_price})
    save_stocks(stocks_data)
    return jsonify({"message": "Azione aggiunta con successo!"})

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/add", methods=["POST"])   
def add_stock():
    """Aggiunge una nuova azione."""
    symbol = request.form.get("symbol")
    target_price = float(request.form.get("target_price"))
    stocks_data = load_stocks()
    stocks_data["stocks"].append({"symbol": symbol, "target_price": target_price})
    save_stocks(stocks_data)
    return jsonify({"message": "Azione aggiunta con successo!"})

@app.route("/delete", methods=["POST"])
def delete_stock():
    """Rimuove un'azione."""
    symbol = request.form.get("symbol")
    stocks_data = load_stocks()
    stocks_data["stocks"] = [
        stock for stock in stocks_data["stocks"] if stock["symbol"] != symbol
    ]
    save_stocks(stocks_data)
    return jsonify({"message": f"Azione {symbol} eliminata con successo!"})
