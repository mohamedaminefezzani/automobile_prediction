from functions import *
import joblib
import time
import pandas as pd
from datetime import date
from sklearn.preprocessing import StandardScaler
from flask import Flask, render_template, request, make_response
import os

app = Flask(__name__)

# Load the model, scaler and encoders
ml_model = joblib.load('Model&Encoders/Car Price Prediction %91.pkl')

scaler = joblib.load('Model&Encoders/standard_scaler.pkl')

le = {}
cat_features = ['Company', 'Model', 'Fuel', 'Transmission', 'Drivetrain']
for col in cat_features:
    le[col] = joblib.load(f'Model&Encoders/label_encoder_{col}.pkl')

# Configure the app
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get form values
        company = str(request.form.get('company')).strip().upper()
        model = str(request.form.get('model')).strip().upper()
        year = int(request.form.get('year').strip())
        kms = float(request.form.get('kms').strip())
        fuel = str(request.form.get('fuel')).strip()
        trns = str(request.form.get('trns')).strip()
        drvtrn = str(request.form.get('drvtrn')).strip()
        tax = int(request.form.get('tax').strip())
        
        # Feature engineer
        age = date.today().year - year # Age

        avgKms = avgKm(age, kms) # AvgKms
        
        kmsBin = kmBin(kms) # KmsBin

        avgKmsBin = avgKmBin(avgKms) # AvgKmsBin

        # Place features in a dataframe

        df = pd.DataFrame({'Company': company, 'Model': model, 'Year': year, 'Kilometers': kms,
                           'Fuel': fuel, 'Transmission': trns, 'Drivetrain': drvtrn,
                           'Taxrate': tax, 'Age': age, 'AvgKms': avgKms,
                           'KilometersBin': kmsBin, 'AvgKmsBin': avgKmsBin,},index=[0])
        print('Dataframe created successfully!') # Log
        print(df)

        # Encode categorical features
        for col, enc in le.items():
            df[col] = enc.fit_transform(df[col])
        print('Categorical features encoded successfully!') # Log

        # Scale data
        df = scaler.transform(df)
        print('Data scaled successfully!') # Log

        #Predict price
        result = ml_model.predict(df)[0]
        print(f'Predicted Price : {result:.3f} TND')

        timestamp = int(time.time())
        return render_template('index.html', result=result, timestamp=timestamp)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
