import pandas as pd
from flask import Flask, jsonify, render_template
# from sqlalchemy import create_engine
from data_training import initial_model, predict, load_db, get_attitude, retrieve_current_tweet, get_wordcloud
# from getwordcloud import get_Biden, get_trump

application = app = Flask(__name__)

#################################################
#################################################
global tokenizer, tweetcloudPd, model_biden_trump, model_sentiment, currentTweet
model_biden_trump,model_sentiment, tokenizer = initial_model()
tweetcloudPd = load_db()
attitudeJson = None
currentTweet = None


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
    return jsonify(get_wordcloud(tweetcloudPd, name))

@app.route("/getattitudeData")
def getattitude():
    global attitudeJson
    
    if attitudeJson == None:
        trumpTweet = retrieve_current_tweet("@realDonaldTrump")
        bidenTweet = retrieve_current_tweet("@JoeBiden")
        TrumpMean, valueListTrump = get_attitude(model_sentiment, tokenizer, trumpTweet)
        BidenMean, valueListBiden = get_attitude(model_sentiment, tokenizer, bidenTweet)


        print("===========?", len(trumpTweet) )
        print("===========?", len(bidenTweet) )
        print("===========?", len(valueListTrump) )
        print("===========?", len(valueListBiden) )
        trumpList = []
        i = 0
        for item in valueListTrump:
            trumpList.append({
                "tweet": trumpTweet[i],
                "Negitive": float(item[0]-1)*100,
                "Positive": float(item[0])*100
            })
            i+=1

        bidenList = []
        i = 0
        for item in valueListBiden:
            bidenList.append({
                "tweet": bidenTweet[i],
                "Negitive": float(item[0]-1)*100,
                "Positive": float(item[0])*100
            })
            i+=1
        attitudeJson = {
            # "TrumpTweet": trumpTweet, 
            # "BidenTweet": bidenTweet,

            "Trumplist": trumpList, 
            "Bidenlist": bidenList,

            "Trump": TrumpMean, 
            "Biden": BidenMean, 
        }

    return jsonify(attitudeJson)

@app.route("/getcurrentTweet")
def getcurrentTweet():
    global currentTweet
    
    if currentTweet == None:
        currentTweet = retrieve_current_tweet("@realDonaldTrump")
        currentTweet += retrieve_current_tweet("@JoeBiden")

    return jsonify(currentTweet)


@app.route("/getattitude")
def getattitudehtml():
    return render_template("arritude.html")

@app.route("/presentation")
def presentation():
    return render_template("presentation.html")

if __name__ == "__main__":
    app.run(debug=True)
