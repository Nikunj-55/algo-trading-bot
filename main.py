from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def run_strategy():
    # Run your strategy script
    subprocess.run(["python", "stratergy.py"])
    return "Trading strategy executed successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
