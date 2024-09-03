import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 
import tensorflow as tf
import pickle
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
import nltk
nltk.data.path.append('.')

# !unzip /usr/share/nltk_data/corpora/wordnet.zip -d /usr/share/nltk_data/corpora/

# nltk.download('stopwords')
# nltk.download('wordnet')
stops = set(stopwords.words('english'))
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
keras_tokenizer = pickle.load(open('./model_files/tokenizer.pkl','rb'))
model = tf.keras.models.load_model('./model_files/kaggle_model.keras')

def predict_sentiment(r):   
    r = [pre_proc_reviews(r)]
    r = keras_tokenizer.texts_to_sequences(r)
    r = pad_sequences(r, maxlen=20)
    y = model.predict(r)
    ans = y.argmax(axis=1)[0]
    return int(ans)

def pre_proc_reviews(r):
    #cleaning
    r = re.sub('[^a-zA-Z]',' ',r)
    r = r.lower()
    #tokenise
    r = word_tokenize(r)
    #stopwords
    r = [w for w in r if w not in stops]
    #lemmatise
    r = [lemmatizer.lemmatize(w) for w in r]
    return r
