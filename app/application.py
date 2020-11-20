import pandas as pd
from flask import Flask, jsonify, render_template
# from sqlalchemy import create_engine
from data_training import initial_model, predict, load_db, get_attitude
from getwordcloud import get_Biden, get_trump

application = app = Flask(__name__)

#################################################
#################################################
global tokenizer, tweetPd, model_biden_trump, model_sentiment
model_biden_trump,model_sentiment, tokenizer = initial_model()
tweetPd = load_db()
attitudeJson = None


#################################################
#################################################
@app.route("/")
def entrance():
    """Return the homepage."""
    return render_template("index.html")
@app.route("/loadmodel")
def loadmodel():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/wordcloud")
def wordcloud():
    """Return the homepage."""
    return render_template("wordcloud.html")


@app.route("/predict/<tweet>")
def metapredict(tweet):

    # print("-------2--------->", predict_result)
    predict_result = predict(model_biden_trump, tokenizer, tweet)
    result = predict_result[0][0]
    # print("==========>",result )
    print(result)
    if  result < 0.5:
        name = "Trump"
    else:
        name = "Biden"

    returnJson = {"name": name, "possibility": float(result), "tweet": tweet }

    return jsonify(returnJson)

@app.route("/getwordcloud/<name>")
def getwordcloud(name):
    if name == 'Biden':
        returnJson = { "name": get_Biden()}
    else:
        returnJson =  { "name": get_trump()}

    return jsonify(returnJson)

@app.route("/getattitudeData")
def getattitude():
    global attitudeJson
    
    if attitudeJson == None:
        attitudeJson = {
            "Biden": get_attitude(model_sentiment,tokenizer,  tweetPd, "<JoeBiden>"), 
            "Trump": get_attitude(model_sentiment, tokenizer, tweetPd, "<realDonaldTrump>")
        }

    return jsonify(attitudeJson)

@app.route("/getattitude")
def getattitudehtml():
    return render_template("arritude.html")

@app.route("/presentation")
def presentation():
    return render_template("presentation.html")

if __name__ == "__main__":
    app.run(debug=True)
