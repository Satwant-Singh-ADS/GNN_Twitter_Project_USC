# GNN Twitter Project
This repository contains the code and data for a project analyzing tweets related to Covid-19 in the United States using Graph Neural Networks (GNNs). The aim of the project is to predict the retweet behavior of Twitter users based on their tweet content, user profile information, and network structure.

## Data Collection
The project used Twitter data mainly tweets related to Covid-19 keywords. The tweet IDs were extracted using the COVID-19-TweetIDs repository and then hydrated using the twarc library, which offers a hydration API for Twitter. The data was hydrated from 23 Jan 2020 through Oct 2022. The entire dataset is available on a server at bernoulli2.usc.edu.

The tweet metadata included the timestamp, user data (username, ID, follower count, location, bio), tweet text, retweet statistics (number of retweets), hashtags, and URLs mentioned in the tweet.

## Data Exploration
The project focused on 100K English tweets related to Covid-19 in the United States between 1 May 2020 to 31 May 2020. The following filters were applied to reduce the data:

Tweet Language: English
Location: United States
Tweet Date between 1 May 2020 to 31 May 2020
Tweet contains a URL
Tweet was retweeted at least once
The script used to extract the retweet data is available in the repository.

## Feature Engineering
The following features were extracted from the tweet data:

### Hashtags
A bag-of-words representation was created for the hashtags mentioned in each tweet. The top 1000 hashtags were used to create a 1000-dimension vector for each tweet. The code is available here.

### Stance Vector (entailment, contradiction, neutral)
The stance of each tweet with respect to the statement "Covid-19 is dangerous" was obtained using a pre-trained BERT model. The output is a 3-dimensional vector indicating whether the tweet supports, contradicts, or is neutral with respect to the statement. The code is available here.
### Sentiment Score (-99 to 99)
The sentiment score of each tweet was obtained using a pre-trained model. The output is a score between -99 (negative sentiment) and 99 (positive sentiment). The code is available here.
### Emotion Vector (11 dim)
An 11-dimensional vector indicating the emotions (anger, anticipation, disgust, fear, joy, love, optimism, pessimism, sadness, surprise, trust) expressed in each tweet was obtained using a model trained on 6000 tweets containing emotion-related keywords. The code is available on the Bernoulli server.
### Sentence Encoding of Tweet Text
A pre-trained BERT model was used to encode each tweet into its semantic vector representation. The code is available here





