from flask import Flask, request, render_template
from predict import predict_sentiment
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
password = "horcrux"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# login_manager = LoginManager()
# login_manager.init_app(app)

class Predictions(db.Model):
    review = db.Column(db.String(500),primary_key=True)
    sentiment = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"Movie : {self.movie}, Review: {self.review}, Sentiment : {self.sentiment}"

# class Users(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(250), unique=True,
#                          nullable=False)
#     password = db.Column(db.String(250),
#                          nullable=False)
    
@app.route('/')
def hello_word():
    import time
    time.sleep(0.1)
    return "<p>Hello World!</p>"

@app.route('/predict/<pwd>/<review>',methods=['GET'])
@app.route('/predict',methods=['POST'])
def sentiment(pwd=None, review=None):
    if request.method == 'GET':
        if pwd==password:
            r = predict_sentiment(review)
            p = Predictions(review=review, sentiment=r)
            db.session.add(p)
            db.session.commit()
            return f"Review : {review} --> {r}"
        else:
            return 'Authentication Failed!'
    else:
        pwd = request.form['pwd']
        review = request.form['review']
        if pwd==password:
            r = predict_sentiment(review)
            p = Predictions(review=review, sentiment=r)
            db.session.add(p)
            db.session.commit()
            return f"Review : {review} --> {r}"
        else:
            return 'Authentication Failed!'

@app.route('/web_app/predict/<pwd>',methods=['GET'])
def landing_page(pwd):
    if pwd==password:
        return render_template('input_form.html')
    else:
        return 'Authentication Failed!'

@app.route('/submit', methods=['POST'])
def submit():
    # Get the user input from the form
    review = request.form['user_input']
    # Process the input (for now, just display it)
    r = predict_sentiment(review)
    p = Predictions(review=review, sentiment=r)
    db.session.add(p)
    db.session.commit()
    data = {'review':review, 'sentiment':r}
    return render_template('movie_template.html', **data)

@app.route('/monitor')
def monitor():
    items = Predictions.query.all()
    return render_template('monitoring.html', items=items)
