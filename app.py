from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok"})

@app.route('/sum', methods=['GET'])
def sum_route():
    a = request.args.get('a')
    b = request.args.get('b')
    try:
        a_f = float(a)
        b_f = float(b)
    except (TypeError, ValueError):
        return jsonify({"error": "invalid input"}), 400
    return jsonify({"sum": a_f + b_f})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)