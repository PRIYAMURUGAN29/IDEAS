from flask import Flask, render_template, request
import joblib
import pandas as pd
from utils.geocode import get_lat_lon
from utils.aqi_fetcher import get_current_aqi

app = Flask(__name__)

# Load trained model
model = joblib.load('model/risk_model.pkl')

@app.route("/", methods=["GET", "POST"])
def index():
    risk_result = None

    if request.method == "POST":
        age = int(request.form["age"])
        smoker = request.form["smoker"] == "Yes"
        activity = request.form["activity"]
        city = request.form["city"]

        lat, lon = get_lat_lon(city)
        if lat and lon:
            aqi_data = get_current_aqi({"lat": lat, "lon": lon})
            features = pd.DataFrame([[age, smoker, activity, *aqi_data]],
                columns=["age", "smoker", "activity", "PM2.5", "NO2", "O3"])

            prediction = model.predict(features)[0]
            if prediction == 1:
                risk_result = "🔴 High Risk"
            else:
                risk_result = "🟢 Low Risk"
        else:
            risk_result = "Invalid city or location not found."

    return render_template("index.html", risk_result=risk_result)

if __name__ == "__main__":
    app.run(debug=True)
