from flask import Flask, render_template, request
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob.classifiers import NaiveBayesClassifier as NBC

app = Flask(__name__)
cl = 0
accuracy = 0

@app.route('/')
def homepage():
    global accuracy
    main()

    return render_template('home.html', sentiment = 0, text = "", accuracy = accuracy * 100)

@app.route('/action', methods=["POST"])
def action():
    global accuracy

    text = request.form.get("text")
    sentiment = estimate(text)

    return render_template('home.html', text = text, sentiment = sentiment, accuracy = accuracy * 100)

@app.route('/update', methods=["POST"])
def update():
    text = request.form.get("text")
    result = request.form.get("result")
    sentiment = estimate(text)

    with open('./static/train.csv', 'a') as fp:
        if result == "1":
            fp.write(text + ',' + sentiment)
        else:
            if sentiment == "pos":
                sentiment = "neg"
            else:
                sentiment = "pos"
            fp.write(text + ',' + sentiment)
        fp.write("\n") 

    main()

    return homepage()

@app.route('/classifier')
def classifier():
    global cl
    global accuracy

    if cl == 0:
        main()

    informative = cl.informative_features(10)
    return render_template('classifier.html', informative = informative, accuracy = accuracy)


def estimate(text):
    global cl

    if cl == 0:
        main()

    prob_dist = cl.prob_classify(text)
    sentiment = prob_dist.max()

    return sentiment


def main():
    global cl, accuracy
    print("// TRAIN DU MODELE")

    with open('./static/train.csv', 'r') as fp:
        cl = NBC(fp, format="csv")

    test = [
        ("J'aime les avions","pos"),
        ("Je n'aime pas la pluie","neg"),
        ("Polytech est une super école","pos"),
        ("Il pleut","neg"),
        ("C'est Noel","pos"),
        ("Je mange une pizza","pos"),
        ("Polytech est la meilleure école du monde","pos"),
        ("Je suis moi","pos"),
        ("Nique toi","neg"),
        ("Il fait beau aujourd'hui","pos"),
        ("il fait pas beau aujourd'hui","neg"),
        ("Il pleut aujourd'hui","neg"),
        ("C'est Noel","pos"),
        ("Il fait beau dans le sud","pos")
    ]
    accuracy = cl.accuracy(test)
    print("// ACCURACY : " + str(accuracy))