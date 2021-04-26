from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import pickle
import sklearn
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def Home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method=='POST':
        
        Date_time = request.form['date']
        Year = int(pd.to_datetime(Date_time, format="%Y-%m-%dT%H:%M").year)
        Month = int(pd.to_datetime(Date_time, format="%Y-%m-%dT%H:%M").month)
        Day = int(pd.to_datetime(Date_time, format="%Y-%m-%dT%H:%M").day)
        
        High = float(request.form['high_level'])
        Low = float(request.form['low_level'])
        Open = float(request.form['open'])
        Close = float(request.form['close'])
        Volume = float(request.form['volume'])
        
        pred = model.predict([[High, Low, Open, Close, Volume, Year, Month, Day]])
        output = np.round(pred[0],2)
        
        if (output<0):
            return render_template('home.html', prediction="Can't find a market cap ")
        else:
            return render_template('home.html', prediction="The Market Cap is ${}".format(output))
        
    else:
        return render_template('home.html')
    


if __name__ == "__main__":
    app.run(debug=True)