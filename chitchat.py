import pandas as pd
import string
import pyttsx3
import nltk
import warnings

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')
lemmer = nltk.stem.WordNetLemmatizer()


def voice_output(msg):
    engine = pyttsx3.init()
    engine.setProperty('rate', 135)
    engine.setProperty('volume', 0.7)
    engine.say(str(msg))
    engine.runAndWait()


col_list = ["Question", "Answer"]
read_professional=pd.read_csv('onefile.csv',sep=',',usecols=col_list)

question=read_professional["Question"].tolist()
answer=read_professional["Answer"].tolist()

question=[''.join(c for c in str(s) if c not in string.punctuation) for s in question]
for i in range(len(question)):
    question[i]=question[i].lower()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text))


def chit_chat(user_input):
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(question)
    user_vector = TfidfVec.transform([user_input])
    vals = cosine_similarity(user_vector, tfidf)
    similarity = max(vals[0])
    robo_response = ''
    if similarity > [0.8]:
        index = vals[0].tolist().index(similarity)
        robo_response = robo_response + answer[index]
        voice_output(robo_response)
        print('Assistant : {}'.format(robo_response))
    else :
        robo_response = robo_response + "I am sorry! It's beyond my abilities"
        voice_output(robo_response)
        print('Assistant : {}'.format(robo_response))

    return robo_response

