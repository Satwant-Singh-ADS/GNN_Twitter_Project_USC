import pandas as pd

data = {
    'rt_url': [101649, 101650, 101651, 101652, 101653, 101654, 101655, 101656, 101657, 101658],
    'tw_id': [1.258358e+18, 1.259571e+18, 1.259567e+18, 1.259573e+18, 1.259564e+18, 1.259507e+18, 1.259503e+18, 1.259135e+18, 1.259573e+18, 1.259557e+18],
    'hashtag_list': ['', '', '', '', '', '', '#maca,', '#lalege, #lagov', '', '']
}

df_nodup_usa = pd.DataFrame(data)

print(df_nodup_usa)

# Read in your master data DataFrame
master_data_df = df_nodup_usa[:]



# Get the top 10,000 hashtags by frequency
all_hashtags = [hashtag for hashtags in master_data_df['hashtag_list'] for hashtag in hashtags]
top_hashtags = pd.Series(all_hashtags).value_counts()[:1000].index.tolist()



# Filter the hashtag lists in your DataFrame to only include the top 10,000 hashtags
filtered_hashtag_lists = [[hashtag for hashtag in hashtags if hashtag in top_hashtags] for hashtags in master_data_df['hashtag_list']]

# Convert the filtered hashtag lists to a one-hot encoded matrix
mlb = MultiLabelBinarizer()
one_hot_matrix = mlb.fit_transform(filtered_hashtag_lists)

# Create a new DataFrame with the one-hot encoded hashtags
# Create a new DataFrame with a single column of 10,000-element lists of encoded values
encoded_hashtags = []
for row in one_hot_matrix:
    encoded_hashtags.append(row.tolist())

encoded_hashtags_df = pd.DataFrame({'encoded_hashtags': encoded_hashtags})


with open(Pickle_path+"encoded_hashtags_df.pkl", "wb") as f:
    pickle.dump(encoded_hashtags_df, f)



# df_nodup_usa_hashtgs = pd.concat([master_data_df.reset_index(),encoded_hashtags_df],axis=1)

