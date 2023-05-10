import spacy
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

import sentence_transformers
import transformers

import tqdm

tweets_list = ['My name is Tommy Trojan','I am a proud Trojan']


#-SentenceTransformer('all-MiniLM-L6-v2')
#-spacy.load('en_core_web_sm')

!python3 -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')
model = SentenceTransformer('all-MiniLM-L6-v2')  ##### downloading pretrained model for encodeing senteces into 364 dim vectors

data_embeddings = []
for des in tqdm(tweets_list):
    embeddings = model.encode(des,)
    data_embeddings.append(embeddings)
    
embeddings_output = data_embeddings
