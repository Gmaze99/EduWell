import joblib
import numpy as np
from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template,request

app = Flask(__name__)

loaded_model = joblib.load(MODEL_OUTPUT_PATH)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':

        lead_time = int(request.form["entry1"])
        no_of_special_request = int(request.form["entry2"])
        avg_price_per_room = float(request.form["entry3"])
        arrival_month = int(request.form["entry4"])
        arrival_date = int(request.form["entry5"])
        market_segment_type = int(request.form["entry6"])
        no_of_week_nights = int(request.form["entry7"])
        no_of_weekend_nights = int(request.form["entry8"])
        type_of_meal_plan = int(request.form["entry9"])
        room_type_reserved = int(request.form["entry10"])
        sleep_quality = int(request.form["entry11"])
        study_time = int(request.form["entry12"])
        past_failures = int(request.form["entry13"])
        past_success = int(request.form["entry14"])
        absences = int(request.form["entry15"])
        presences = int(request.form["entry16"])
        


        features = np.array([[lead_time, no_of_special_request, avg_price_per_room, arrival_month,
        arrival_date, market_segment_type, no_of_week_nights, no_of_weekend_nights,
        type_of_meal_plan, room_type_reserved, sleep_quality, study_time,
        past_failures, past_success, absences, presences]]).reshape(1, -1)

        prediction = loaded_model.predict(features)

        return render_template('index.html', prediction=prediction[0])
    
    return render_template("index.html" , prediction=None)

if __name__=="__main__":
    app.run(host='0.0.0.0' , port=8080)
