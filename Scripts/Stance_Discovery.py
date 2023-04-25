#!/usr/bin/env python
# coding: utf-8

# In[2]:


# from huggingface_hub import from_pretrained_keras
# import numpy as np
# # import gradio as gr
# import transformers
import tensorflow as tf


# In[3]:


from huggingface_hub import from_pretrained_keras
import numpy as np
# import gradio as gr
import transformers


# In[4]:


from huggingface_hub import from_pretrained_keras
import numpy as np
# import gradio as gr
import transformers
import tensorflow as tf

class BertSemanticDataGenerator(tf.keras.utils.Sequence):
    """Generates batches of data."""
    def __init__(
        self,
        sentence_pairs,
        labels,
        batch_size=32,
        shuffle=True,
        include_targets=True,
    ):
        self.sentence_pairs = sentence_pairs
        self.labels = labels
        self.shuffle = shuffle
        self.batch_size = batch_size
        self.include_targets = include_targets
        # Load our BERT Tokenizer to encode the text.
        # We will use base-base-uncased pretrained model.
        self.tokenizer = transformers.BertTokenizer.from_pretrained(
            "bert-base-uncased", do_lower_case=True
        )
        self.indexes = np.arange(len(self.sentence_pairs))
        self.on_epoch_end()

    def __len__(self):
        # Denotes the number of batches per epoch.
        return len(self.sentence_pairs) // self.batch_size

    def __getitem__(self, idx):
        # Retrieves the batch of index.
        indexes = self.indexes[idx * self.batch_size : (idx + 1) * self.batch_size]
        sentence_pairs = self.sentence_pairs[indexes]

        # With BERT tokenizer's batch_encode_plus batch of both the sentences are
        # encoded together and separated by [SEP] token.
        encoded = self.tokenizer.batch_encode_plus(
            sentence_pairs.tolist(),
            add_special_tokens=True,
            max_length=128,
            return_attention_mask=True,
            return_token_type_ids=True,
            pad_to_max_length=True,
            return_tensors="tf",
        )

        # Convert batch of encoded features to numpy array.
        input_ids = np.array(encoded["input_ids"], dtype="int32")
        attention_masks = np.array(encoded["attention_mask"], dtype="int32")
        token_type_ids = np.array(encoded["token_type_ids"], dtype="int32")

        # Set to true if data generator is used for training/validation.
        if self.include_targets:
            labels = np.array(self.labels[indexes], dtype="int32")
            return [input_ids, attention_masks, token_type_ids], labels
        else:
            return [input_ids, attention_masks, token_type_ids]

model = from_pretrained_keras("keras-io/bert-semantic-similarity")
labels = ["contradiction", "entailment", "neutral"]


    


# In[5]:


import pickle


# In[6]:


Pickle_path = '../Pickle_Files/'

with open(Pickle_path+"tweets_list.pkl", "rb") as f:
    tweets = pickle.load(f)


# In[7]:


sentence_pairs = []

for tweet in tweets:
    if tweet != '' or tweet is not None:
        sentence_pairs.append(["Covid-19 is dangerous",str(tweet)])
    else:
        sentence_pairs.append(["Neutral","Neutral"])
        


# In[8]:


sentence_pairs = np.array(sentence_pairs)


# In[9]:


data = sentence_pairs[:]  # your list of 106802 values
batch_size = 128  # number of values to pick at a time
num_batches = len(data) // batch_size  # total number of batches


# In[10]:


data = sentence_pairs[:]  # your list of 106802 values
batch_size = 128  # number of values to pick at a time
num_batches = len(data) // batch_size  # total number of batches

predictions = []

for i in range(num_batches):
    print(i)
    batch = data[i * batch_size : (i + 1) * batch_size]
    test_data = BertSemanticDataGenerator(
    batch, labels=None, batch_size=128, shuffle=False, include_targets=False )
    probs = model.predict(test_data[0])
    predictions.append(probs)

    # do something with the batch of 128 values
#     print(batch)
    
# handle any remaining values that didn't fit into a full batch
if len(data) % batch_size != 0:
    batch = data[num_batches * batch_size :]
    test_data = BertSemanticDataGenerator(
    batch, labels=None, batch_size=128, shuffle=False, include_targets=False )
    probs = model.predict(test_data[0])
    predictions.append(probs)



with open(Pickle_path+"Stance_predictions_list.pkl", "wb") as f:
    pickle.dump(predictions, f)
