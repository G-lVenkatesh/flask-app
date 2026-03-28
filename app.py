from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
        <body style="font-family: Arial; text-align: center; margin-top: 100px;">
            <h1>🚀 Flask App is Live!</h1>
            <p>Deployed on AWS EC2 with Nginx reverse proxy</p>
        </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "App is healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
