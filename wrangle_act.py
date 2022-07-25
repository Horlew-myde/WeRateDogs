#!/usr/bin/env python
# coding: utf-8

# # Project: Wrangling and Analyze Data

# ## Data Gathering
# In the cell below, gather **all** three pieces of data for this project and load them in the notebook. **Note:** the methods required to gather each data are different.
# 1. Directly download the WeRateDogs Twitter archive data (twitter_archive_enhanced.csv)

# In[ ]:





# In[97]:


# Import statements
import pandas as pd
import numpy as np
import requests
import tweepy
import os
import json
import time
from timeit import default_timer as timer
import re
import matplotlib.pyplot as plt
import warnings
from IPython.display import Image
from functools import reduce
import re
import seaborn as sns
import datetime
from jupyterthemes import jtplot
jtplot.style(theme='onedork')
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
warnings.simplefilter('ignore')


# In[ ]:





# In[98]:


# Open the csv file
df_twitter_archive = pd.read_csv('twitter-archive-enhanced.csv')
# df_twitter_archive.head()
# df_twitter_archive.tail(5)
# df_twitter_archive.info()
df_twitter_archive.shape


# 2. Use the Requests library to download the tweet image prediction (image_predictions.tsv)

# In[99]:


# Downloading the image prediction file from project link
url = "https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv"
response = requests.get(url, allow_redirects=True)
# Save File into System
with open('image_prediction.tsv', mode ='w', encoding ='UTF-8') as  file:
    file.write(response.text)
pd.read_csv('image_prediction.tsv', sep='\t')


# In[100]:


df_image_prediction = pd.read_csv('image_prediction.tsv', sep='\t')
# df_image_prediction.head()
# df_image_prediction.info()
df_image_prediction.shape


# In[101]:


#Downloading twitter api API and JSON stuff
access_token = "910976278265769984-vE8bThY3afB3SLfXuMC4k1eT7foQNMs"
access_secret = "ZrAtZEB7sVwJkncw70DijwTs4wbBI7j9zd1BjXJ1NG71D"
consumer_key = "gBWzp0bmCRbxLTVyoyaTidBSP"
consumer_secret = "mfWKLtdg1Em7MtS43EsKmqgmaRhoTHwGjT3NEXo5uX7APNUadi"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)


# In[102]:


api = tweepy.API(auth, wait_on_rate_limit=True)


# In[103]:


tweet_ids = df_twitter_archive.tweet_id.values
len(tweet_ids)


# In[104]:


# #from time import default_timer as timer
# count = 0
# fails_dict = {}
# start = timer()
# # save each tweets returned JSON as a new line in a .txt file
# with open ('tweet_json.txt', 'w') as outfile:
#     #This loop will likely take 20-30 minutes to run because of twitter's rate limit
#     for tweet_id in tweet_ids:
#         count += 1
#         print(str(count) + ":" + str(tweet_id))
#         try:
#             tweet = api.get_status(tweet_id, tweet_mode='extended')
#             print("succes")
#             json.dump(tweet._json, outfile)
#             outfile.write('\n')
#         except tweepy.errors.TweepyException as e:
#             print("Fail")
#             fails_dict[tweet_id] = e
#             pass
#     end = timer()
#     print(end - start)
#     print(fails_dict)


# In[105]:


twitter_list = []
# Read the .txt file line by line into a list of dictionaries
for line in open('tweet_json.txt', 'r'):
    twitter_data = json.loads(line)
    twitter_list.append({'tweet_id': twitter_data['id_str'],
                        'retweet_count': twitter_data['retweet_count'],
                        'favorite_count': twitter_data['favorite_count'],
                        'followers_count': twitter_data['user']['followers_count']})


# In[106]:


twitter_list


# In[107]:


# Convert the list of dictionaries to a pandas DataFrame
twitter_data = pd.DataFrame(twitter_list, columns = ['tweet_id', 'retweet_count', 'favorite_count', 'followers_count'])


# In[108]:


twitter_data.head(5)
# twitter_data.info()
# twitter_data.shape


# ## Assessing Data
# In this section, detect and document at least **eight (8) quality issues and two (2) tidiness issue**. You must use **both** visual assessment
# programmatic assessement to assess the data.
# 
# **Note:** pay attention to the following key points when you access the data.
# 
# * You only want original ratings (no retweets) that have images. Though there are 5000+ tweets in the dataset, not all are dog ratings and some are retweets.
# * Assessing and cleaning the entire dataset completely would require a lot of time, and is not necessary to practice and demonstrate your skills in data wrangling. Therefore, the requirements of this project are only to assess and clean at least 8 quality issues and at least 2 tidiness issues in this dataset.
# * The fact that the rating numerators are greater than the denominators does not need to be cleaned. This [unique rating system](http://knowyourmeme.com/memes/theyre-good-dogs-brent) is a big part of the popularity of WeRateDogs.
# * You do not need to gather the tweets beyond August 1st, 2017. You can, but note that you won't be able to gather the image predictions for these tweets since you don't have access to the algorithm used.
# 
# 

# In[109]:


twitter_data.head(10)


# In[110]:


twitter_data.info()


# In[111]:


df_image_prediction.head()


# In[112]:


df_image_prediction.duplicated().sum()


# In[113]:


df_twitter_archive.info()


# In[114]:


df_twitter_archive[['rating_numerator', 'rating_denominator']].describe()


# In[ ]:





# In[115]:


df_twitter_archive.rating_numerator.value_counts()


# In[116]:


df_twitter_archive.rating_denominator.value_counts()


# In[117]:


df_twitter_archive.source.value_counts()


# In[118]:


df_twitter_archive.name.value_counts()


# In[119]:


df_twitter_archive.info()


# In[120]:


df_image_prediction.info()


# In[121]:


df_image_prediction.head()


# In[122]:


# twitter_data.info(verbose=False)
twitter_data.info()


# ### For Twitter Data......

# In[123]:


twitter_data.sample(10)


# In[124]:


twitter_data.describe()


# In[125]:


twitter_data.info()


# In[ ]:





# ### For df_twitter_archive........

# In[126]:


df_twitter_archive.rating_numerator.value_counts()


# In[ ]:





# In[127]:


print(df_twitter_archive.loc[df_twitter_archive.rating_numerator == 12, 'text']) 
print('\n')
print(df_twitter_archive.loc[df_twitter_archive.rating_numerator == 420, 'text'])
print('\n')
print(df_twitter_archive.loc[df_twitter_archive.rating_numerator == 1776, 'text']) 


# In[128]:


df_twitter_archive.rating_denominator.value_counts()


# In[129]:


df_twitter_archive['name'].value_counts()


# In[130]:


df_twitter_archive[df_twitter_archive.tweet_id.duplicated()]


# In[131]:


df_twitter_archive.describe()


# ### For df_image_predictions........

# In[132]:


df_image_prediction.sample(10)


# In[133]:


# sample image for s/n 1288 && tweet_id 751205363882532864
Image(url = 'https://pbs.twimg.com/media/CmzRRY1WcAEoxwY.jpg')


# In[134]:


df_image_prediction['p1'].value_counts()


# In[135]:


df_image_prediction['p2'].value_counts()


# In[136]:


df_image_prediction['p3'].value_counts()


# In[137]:


df_image_prediction.info()


# In[138]:


df_image_prediction[df_image_prediction.tweet_id.duplicated()]


# ### Assessment Summary:

# ### Quality issues
# TWITTER ARCHIVE
# 
# #1.only Keep original ratings with images (remove retweets)
# 
# #2.Drop columns not needed for analysis
# 
# #3.Error in datatypes in columns [tweet_id, retweeted_status_user_id, retweeted_status_timestamp, doggo, floofer, pupper, and puppo]
# 
# #4.Correct numerators with decimals 
# 
# #5.Sort Dog Names its very unlikely "a,an,actually" are dog names.
# 
# #6.Missing values in 'name' and dog stages represented as 'None'
# 
# #7.scrub Html strings from source and tweet
# 
# API TABLE (TWITTER DATA)
# 
# 8.Missing tweets
# 
# 9.Error in data type for tweet_id
# 
# IMAGE TABLE (IMAGE PREDICTION TABLE)
# 
# 10.Missing images 2075 obtained, instead of 2356 expected
# 
# 11.Also possess Error in data type for tweet_id
# 
# 

# ### Tidiness issues
# 
# TWITTER ARCHIVE
# 
# #1. merge all 3 dataframe tables together
# 
# #2. Drop any tweet that have no images
# 
# #3. doggo, floofer, pupper and puppo columns in twitter_archive table should be merged into one column named "dog_stage"
# 
# IMAGE PREDICTION
# 2.Image predictions table should be added to twitter archive df
# 
# 3.twitter api table columns(retweet_count, favorite_count, followers_count) should be added to twitter archive table.

# ## Cleaning Data
# In this section, clean **all** of the issues you documented while assessing. 
# 
# **Note:** Make a copy of the original data before cleaning. Cleaning includes merging individual pieces of data according to the rules of [tidy data](https://cran.r-project.org/web/packages/tidyr/vignettes/tidy-data.html). The result should be a high-quality and tidy master pandas DataFrame (or DataFrames, if appropriate).

# In[139]:


# Make copies of original pieces of data
twitter_data_clean = twitter_data.copy()
df_image_prediction_clean = df_image_prediction.copy()
df_twitter_archive_clean = df_twitter_archive.copy()


# In[140]:


df_twitter_archive_clean.info()


# ### Issue #1: Quality

# In[ ]:





# #### Define:
# only Keep original ratings with images (remove retweets)

# #### Code: 

# In[141]:


#Delete retweets by filtering the NaN of retweeted_status_user_id
df_twitter_archive_clean = df_twitter_archive_clean[pd.isnull(df_twitter_archive_clean['retweeted_status_user_id'])]


# #### Test:

# In[142]:


print(sum(df_twitter_archive_clean.retweeted_status_user_id.value_counts()))


# ### Issue #1: Quality

# #### Define:
# Drop all columns not needed for analysis

# #### Code

# In[143]:


df_twitter_archive_clean = df_twitter_archive_clean.drop(['in_reply_to_status_id','in_reply_to_user_id','retweeted_status_id',
                                            'retweeted_status_user_id','retweeted_status_timestamp', 'expanded_urls'], 1)


# #### Test

# In[144]:


df_twitter_archive_clean.info()


# ### Issue #2: Quality

# #### Define:
# Datatype Error

# #### Code:

# In[145]:


# Convert tweet_id to str from df_image_prediction, twitter_data, df_twitter_archive, tables.
twitter_data_clean.tweet_id = twitter_data_clean.tweet_id.astype(str)
df_image_prediction_clean.tweet_id = df_image_prediction_clean.tweet_id.astype(str)
df_twitter_archive_clean.tweet_id = df_twitter_archive_clean.tweet_id.astype(str)

# convert source to category datatype
df_twitter_archive_clean.source = df_twitter_archive_clean.source.astype("category")

# convert timestamp to datetime
df_twitter_archive_clean.timestamp = pd.to_datetime(df_twitter_archive_clean.timestamp)


# #### Test

# In[146]:


#confirm code
twitter_data_clean.info()
df_twitter_archive_clean.info()
df_image_prediction_clean.info()


# ### Issue #3: Quality

# #### Define:
# Correct numerators with decimals

# In[147]:


# check to see if some columns were not extracted properly to capture decimals
with pd.option_context('max_colwidth', 200):
    display(df_twitter_archive[df_twitter_archive['text'].str.contains(r"(\d+\.\d*\/\d+)")]
            [['tweet_id', 'text', 'rating_numerator', 'rating_denominator']])


# #### Code:

# In[148]:


# convert to float datatype
df_twitter_archive_clean[['rating_numerator', 'rating_denominator']] = df_twitter_archive_clean[['rating_numerator','rating_denominator']].astype(float)

#update values
df_twitter_archive_clean.loc[(df_twitter_archive_clean.tweet_id == 883482846933004288), 'rating_numerator'] = 13.5
df_twitter_archive_clean.loc[(df_twitter_archive_clean.tweet_id == 786709082849828864), 'rating_numerator'] = 9.75
df_twitter_archive_clean.loc[(df_twitter_archive_clean.tweet_id == 778027034220126208), 'rating_numerator'] = 11.27
df_twitter_archive_clean.loc[(df_twitter_archive_clean.tweet_id == 681340665377193984), 'rating_numerator'] = 9.5
df_twitter_archive_clean.loc[(df_twitter_archive_clean.tweet_id == 680494726643068929), 'rating_numerator'] = 11.26


# #### Test:

# In[149]:


#Test
with pd.option_context('max_colwidth', 200):
    display(df_twitter_archive_clean[df_twitter_archive_clean['text'].str.contains(r"(\d+\.\d*\/\d+)")]
            [['tweet_id', 'text', 'rating_numerator', 'rating_denominator']])


# ### Issue #4: Quality

# #### Define: 
#  Sort Dog Names its very unlikely "a,an,actually" are dog names.

# In[150]:


df_twitter_archive_clean.name.unique()


# #### Code: 

# In[151]:


display(df_twitter_archive_clean['name'][df_twitter_archive_clean['name'].str.match('[a-z]+')])


# In[152]:


df_twitter_archive_clean['name'][df_twitter_archive_clean['name'].str.match('[a-z]+')] = 'None'


# In[153]:


#check code 
display(df_twitter_archive_clean['name'][df_twitter_archive_clean['name'].str.match('[a-z]+')])


# #### Test: 

# In[154]:


# confirm changes
df_twitter_archive_clean.name.value_counts()


# ### Issue #5: Quality

# #### Define: 
#   more than 1 dog stage issue Missing values in 'name' and dog stages represented as 'None'

# #### Code:

# In[155]:


df_twitter_archive_clean['add_all'] = df_twitter_archive_clean.doggo + df_twitter_archive_clean.floofer + df_twitter_archive_clean.pupper + df_twitter_archive_clean.puppo


# In[156]:


df_twitter_archive_clean.add_all.value_counts()


# In[157]:


# create function to check dog stages
def check_stages(archive):
    if archive['add_all'].count('None') == 2:
        return 'Multiple' #this means it has more than one dog stage
    else:
        if archive['add_all'].count('doggo') == 1:
            return 'Doggo'
        elif archive['add_all'].count('floofer') == 1:
            return 'Floofer'
        elif archive['add_all'].count('pupper') == 1:
            return 'Pupper'
        elif archive['add_all'].count('puppo') == 1:
            return 'Puppo'
        else:
            return 'None'

df_twitter_archive_clean['dog_stage'] = df_twitter_archive_clean.apply(check_stages, axis=1)


# In[158]:


df_twitter_archive_clean.info()


# In[159]:


df_twitter_archive_clean.sample(5)


# ###### vanquish Colums not useful for Analysis

# In[160]:


# code
df_twitter_archive_clean.drop(['doggo', 'floofer', 'pupper', 'puppo', 'add_all'], axis=1, inplace=True)


# In[161]:


df_twitter_archive_clean.sample(5)


# #### Test:

# In[162]:


# check new value counts
df_twitter_archive_clean.dog_stage.value_counts()


# In[163]:


df_twitter_archive_clean.info()


# ### Issue #6: Quality

# #### Define: 
# scrub Html strings from source and tweet

# In[164]:


df_twitter_archive_clean.sample(5)


# #### Code: 

# In[165]:


#using Regex to Extract
df_twitter_archive_clean.source = df_twitter_archive_clean.source.str.extract('>([\w\W\s]*)<', expand=True)


# #### Test: 

# In[166]:


#Check Changes
df_twitter_archive_clean.sample(5)


# In[167]:


df_twitter_archive_clean.source.value_counts()


# #### Code: srcub Html strings from tweet

# In[168]:


def htmlraw(s):
        string = s.find("http")
        if string == -1:
            s = s
        else:
            s = s[:string - 1]
        return s
#apply function to colum
df_twitter_archive_clean.text = df_twitter_archive_clean.text.apply(htmlraw)


# #### Test: 

# In[169]:


df_twitter_archive_clean.sample(5)


# In[170]:


for row in df_twitter_archive_clean.text[:3]:
    print(row)


# In[ ]:





# # Tidiness

# ### Issue #1: Tidiness

# #### Define: 
# merge all 3 df tables(archive, image prediction, data) into 1 single table

# #### Code: 

# In[171]:


df_twitter_archive_clean = pd.merge(left=df_twitter_archive_clean, right=twitter_data_clean, how='left', on='tweet_id')
df_total = pd.merge(left=df_twitter_archive_clean, right=df_image_prediction_clean, how='left', on='tweet_id')


# #### Test: 

# In[172]:


#check change
df_total.info()


# ### Issue #2: Tidiness

# #### Define: 
# Drop any tweet that have no images

# #### Code: 

# In[173]:


#Code
df_total.dropna(axis = 0, inplace=True)


# #### Test: 

# In[174]:


#check
df_total.info()


# In[ ]:





# ## Storing Data
# Save gathered, assessed, and cleaned master dataset to a CSV file named "twitter_archive_master.csv".

# In[175]:


df_total.to_csv('twitter_archive_master.csv', index=False)


# ## Analyzing and Visualizing Data
# In this section, analyze and visualize your wrangled data. You must produce at least **three (3) insights and one (1) visualization.**

# In[176]:


twitter_archive_master = pd.read_csv('twitter_archive_master.csv')


# In[177]:


twitter_archive_master.info()


# #### Issue :

# #### Define:
# Reconversion of data types in the new "twitter_archive_master.csv" haven being lost after saving previous file to csv.

# #### Code :

# In[178]:


twitter_archive_master.timestamp = pd.to_datetime(twitter_archive_master.timestamp)
twitter_archive_master.tweet_id = twitter_archive_master.tweet_id.astype(str)
twitter_archive_master.dog_stage = twitter_archive_master.dog_stage.astype("category")
twitter_archive_master[['retweet_count', 'favorite_count', 'followers_count']] = twitter_archive_master[['retweet_count', 'favorite_count', 'followers_count']].astype(int)
twitter_archive_master.source = twitter_archive_master.source.astype("category")
twitter_archive_master[['rating_numerator', 'rating_denominator']] = twitter_archive_master[['rating_numerator', 'rating_denominator']].astype(float)


# #### Test :

# In[179]:


twitter_archive_master.head(3)


# In[180]:


twitter_archive_master.info()


# ### Insights:
# 1.Most used twitter source ( Device most used for tweeting)
# 
# 2.Popular dog names in tweets
# 
# 3.Most popular dog breed amongst users
# 
# 4.Dog_stage popularity Amongst users

# ### Visualization

# ### Insight 1:

# In[181]:


# Device most used for tweeting ....... (no android user???.. quite suspicious... lol)


# In[182]:


popular_devices = twitter_archive_master['source'].value_counts()
popular_devices


# In[183]:


#Popular twitter source plot "ptsp"
ptsp = popular_devices.plot.bar(color = 'orange', fontsize = 10)
ptsp.figure.set_size_inches(10, 8)
plt.title('Most used Twitter source', color = 'gray', fontsize = '15')
plt.xlabel('platform', color = 'pink', fontsize = '15')
plt.ylabel('Number of tweets', color = 'blue', fontsize = '15');
plt.legend(loc='upper right')
# plt.show()


# In[184]:


#popular dog names excluding the None names occurence


# In[185]:


p_dog = twitter_archive_master.name.value_counts()[1:12]


# In[186]:


#plot
doggy = p_dog.plot.bar(color = 'blue', fontsize = 13)

#figure size(width, height)
doggy.figure.set_size_inches(10, 7);

#Add labels
plt.title('Most popular Dog names', color = 'black', fontsize = '13')
plt.xlabel('Name', color = 'black', fontsize = '13')
plt.ylabel('Number of occurrence', color = 'black', fontsize = '13');


# ### Insight 2:

# In[187]:


twitter_archive_master['p1'].value_counts()


# In[188]:


# Histogram to visualize dog breeeds >25
top_breed = twitter_archive_master.groupby('p1').filter(lambda x: len(x) >= 25)

top_breed['p1'].value_counts().plot(kind = 'bar', color= 'lime')
plt.title('Most Rated Dog Breed')
plt.xlabel('Count')
plt.ylabel('Breed of dog');


# In[ ]:





# ### Insight 3:

# In[189]:


# Plotting time vs. tweets
sns.set_context()
plt.figure(figsize=(10, 10));
plt.xlim([datetime.date(2015, 11, 30), datetime.date(2017, 7, 30)]);

plt.xlabel('Year and Month')
plt.ylabel('Tweets Count')

plt.plot(twitter_archive_master.timestamp, twitter_archive_master.retweet_count);
plt.title('We Rate Dogs Tweets over Time');


# In[190]:


# #plot
# sns.set_context()
# plt.subplots(figsize=(25, 16))
# plt.plot(twitter_archive_master.timestamp, twitter_archive_master.retweet_count)
# plt.title('Retweets over time', color = 'black', fontsize = '18')
# plt.xlabel('Year and month', color = 'black', fontsize = '18')
# plt.ylabel('Number of retweets', color = 'black', fontsize = '18');


# ### Insight 4:

# In[191]:


#Dog_stage popularity count


# In[192]:


twitter_archive_master['dog_stage'].value_counts()


# In[193]:


twitter_archive_master['dog_stage'].value_counts().plot(kind = 'bar', color= 'yellow')
plt.title('Popular Dog Stage')
plt.xlabel('Count')
plt.ylabel('Dog Stage');

