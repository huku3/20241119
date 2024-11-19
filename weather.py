from flask import Flask, render_template, request, flash, redirect
from dotenv import load_dotenv
import requests, os, secrets

load_dotenv()


api_key = os.getenv("API_KEY")

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)


@app.route("/", methods=["GET", "POST"])
def index():

    weather_data = None
    if request.method == "POST":
        city = request.form["city"]

        if not city:
            flash("都市名を入力してください。", "error")
            return redirect('/')
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ja&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            flash("天気データを取得しました!", "success")
            weather_data = response.json()
        else:
            flash("天気の情報を取得出来ませんでした。正しい都市名を入力してください。", "error")
            return redirect('/')
    return render_template("index.html", weather_data=weather_data)


if __name__ == ("__main__"):
    app.run(port=8000, debug=True)
