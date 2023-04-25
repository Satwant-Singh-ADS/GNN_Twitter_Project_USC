
import pandas as pd
import numpy as np

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer



# Preprocess the tweets by removing stop words and tokenizing
stop_words = set(stopwords.words('english'))
tweets_df = pd.DataFrame(tweets_list,columns = ['tw_text'])
tweets_df['tokens'] = tweets_df['tw_text'].apply(lambda x: [w.lower() for w in word_tokenize(x) if w.lower() not in stop_words])

# Convert the tweets into a bag-of-words representation
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(tweets_df['tokens'].apply(lambda x: ' '.join(x)))




# Train an LDA model on the bag-of-words matrix
lda_model = LatentDirichletAllocation(n_components=10, max_iter=100, random_state=42)
lda_model.fit(X)

# Print the top words for each topic
feature_names = vectorizer.get_feature_names()
for topic_idx, topic in enumerate(lda_model.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]))

# Assign each tweet a distribution over the topics
topic_distributions = lda_model.transform(X)
tweets_df['topic_distribution'] = list(topic_distributions)

# Map the top topic for each tweet to a semantic category
topic_labels = {
    0: 'politics',
    1: 'public health',
    2: 'vaccination',
    3: 'epidemiology',
    4: 'social distancing',
    5: 'mental health',
    6: 'pandemic response',
    7: 'testing',
    8: 'treatment',
    9: 'communication'
}
tweets_df['top_topic'] = tweets_df['topic_distribution'].apply(lambda x: np.argmax(x))
tweets_df['semantic_category'] = tweets_df['top_topic'].map(topic_labels)



with open(Pickle_path+"Topic_modelling_results.pkl",'wb') as topic_out:
    pickle.dump(tweets_df,topic_out)
