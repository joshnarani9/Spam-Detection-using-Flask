from flask import Flask,render_template,request,url_for

#EDA Packages
import pandas as pd
import numpy as np

# ML Packages
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")
def pr(my_prediction):
    if my_prediction == '0':
        return 'not spam'
    else:
        return 'spam'
    
@app.route("/",methods=['POST'])
def predict():
	# Link to dataset from github
	#url = "YoutubeSpamMergedData.csv"
	df= pd.read_csv('YoutubeSpamMergedData.csv')
	df_data = df[["CONTENT","CLASS"]]
	# Features and Labels
	df_x = df_data['CONTENT']
	df_y = df_data.CLASS
    # Extract Feature With CountVectorizer
	corpus = df_x
	cv = CountVectorizer()
	X = cv.fit_transform(corpus) # Fit the Data
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, df_y, test_size=0.33, random_state=42)
	#Naive Bayes Classifier
	from sklearn.naive_bayes import MultinomialNB
	clf = MultinomialNB()
	clf.fit(X_train,y_train)
	clf.score(X_test,y_test)
	#Alternative Usage of Saved Model
	# ytb_model = open("naivebayes_spam_model.pkl","rb")
	# clf = joblib.load(ytb_model)
    
	if request.method == 'POST':
		comment = request.form['comment']
		data = [comment]
		vect = cv.transform(data).toarray()
        #my_prediction = clf.predict(vect)
		prediction=pr(clf.predict(vect))
	return render_template('results.html',prediction = prediction,comment = comment)
	


if __name__ == '__main__':
	app.run(port=4996,debug=True)