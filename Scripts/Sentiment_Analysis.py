
from libraries import *

def add_sentiment(Text,sentiment_tokenizer_model,sentiment_model): 
    '''
    add sentiment score as a new column, range=[-100,100]
    [Text] : The Text after preprocessing.
    '''
    text_rest=pd.DataFrame(Text,columns=["text"])
    df_copy = deepcopy(text_rest)
    tokenizer = AutoTokenizer.from_pretrained(sentiment_tokenizer_model)
    model = AutoModelForSequenceClassification.from_pretrained(
    pretrained_model_name_or_path=sentiment_model)
    sentiment_analyzer = pipeline('sentiment-analysis',
                                framework='pt',
                                model=model,
                                tokenizer=tokenizer)
    df_copy['sentiment'] = np.nan
    for row in tqdm(range(df_copy.shape[0])):
        if not df_copy['text'].iloc[row]:
            df_copy['sentiment'].iloc[row]=0
        else:
            sentiment = sentiment_analyzer(df_copy['text'].iloc[row])
            score = sentiment[0]['score']
            label = sentiment[0]['label']
            if label == 'POSITIVE':
                df_copy['sentiment'].iloc[row] = 100 * score
            elif label == 'NEGATIVE':
                df_copy['sentiment'].iloc[row] = -100 * score
    return df_copy


### we need tweet list for running sentiment task.  so lets just make a list
tweets_list = ['This is a dummy tweet']


#Example
sentiment_tokenizer_model = 'distilbert-base-uncased'
sentiment_model = 'distilbert-base-uncased-finetuned-sst-2-english'
result=add_sentiment(tweets_list,sentiment_tokenizer_model,sentiment_model)

