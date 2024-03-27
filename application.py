from flask import Flask, request, render_template
import logging


import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline


application = Flask(__name__)
app = application


logging.basicConfig(filename='application.log', level=logging.ERROR)


@app.errorhandler(Exception)
def handle_error(error):
    app.logger.error("Unhandled exception: %s", error)
    return "An internal server error occurred.", 500


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/predict_datapoint', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('writing_score')),
                writing_score=float(request.form.get('reading_score'))
            )

            df = data.get_data_as_dataframe()

            pred_pipeline = PredictPipeline()
            results = pred_pipeline.predict(df)

            return render_template('home.html', results=round(results[0], 2))
        except Exception as e:
            app.logger.error("Error processing request: %s", e)
            return "An error occurred while processing your request.", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")