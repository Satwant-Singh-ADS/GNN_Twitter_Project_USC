import pandas as pd
import json

import re

def get_details_tweet_Retweet(i):
    data_list  = []
    
    rtw_time = i['created_at']
    rtw_id= i['id_str']
    rtw_text = i['full_text']
    rtw_usr_screen = i['user']['screen_name']
    rusr_follow_cnt = i['user']['followers_count']
    retweet_cnt = i['retweet_count']
    rusa_flg = is_US(i)
    
    rt_url = i['entities']['urls'][0]['expanded_url']


    j = i['retweeted_status']

    tw_time = j['created_at']
    tw_id= j['id_str']
    tw_text = j['full_text']
    tw_usr_screen = j['user']['screen_name']
    usr_follow_cnt = j['user']['followers_count']
    usa_flg = is_US(j)

    return [rtw_time,rtw_id,rtw_text,rtw_usr_screen,rusr_follow_cnt,retweet_cnt,rusa_flg,rt_url,\
            tw_time,tw_id,tw_text,tw_usr_screen,\
            usr_follow_cnt,usa_flg
           ]



def is_US(tweet):
    
    location = tweet['user']['location']
    if location:
        
        loc = location.upper().strip()
        
        if 'USA' in loc or 'UNITED STATES' in loc or 'UNITED STATES OF AMERICA' in loc:
            
            return True
        elif len(re.findall(r'\b(ALABAMA|ALASKA|ARIZONA|ARKANSAS|CALIFORNIA|COLORADO|CONNECTICUT|DELAWARE|FLORIDA|GEORGIA|HAWAII|IDAHO|ILLINOIS|INDIANA|IOWA|KANSAS|KENTUCKY|LOUISIANA|MAINE|MARYLAND|MASSACHUSETTS|MICHIGAN|MINNESOTA|MISSISSIPPI|MISSOURI|MONTANA|NEBRASKA|NEVADA|NEW HAMPSHIRE|NEW JERSEY|NEW MEXICO|NEW YORK|NORTH CAROLINA|NORTH DAKOTA|OHIO|OKLAHOMA|OREGON|PENNSYLVANIA|RHODE ISLAND|SOUTH CAROLINA|SOUTH DAKOTA|TENNESSEE|TEXAS|UTAH|VERMONT|VIRGINIA|WASHINGTON|WEST VIRGINIA|WISCONSIN|WYOMING)\b', loc))>0:
            return True
        elif len(re.findall(r'\b(AK|AL|AR|AZ|CA|CO|CT|DC|DE|FL|GA|HI|IA|ID|IL|IN|KS|KY|LA|MA|MD|ME|MI|MN|MO|MS|MT|NC|ND|NE|NH|NJ|NM|NV|NY|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VA|VT|WA|WI|WV|WY)\b', loc))>0:
            return True
        else:
            return False

    
    return False


def dump_2_csv(dd,out_file_name):
    final_data = pd.DataFrame(dd,columns = ["rtw_time","rtw_id","rtw_text","rtw_usr_screen","rusr_follow_cnt","retweet_cnt","rusa_flg","rt_url",\
            "tw_time","tw_id","tw_text","tw_usr_screen",\
            "usr_follow_cnt","usa_flg"])
    final_data.to_csv(out_file_name,sep="|",index=False)

    

import glob

crawl_files = glob.glob("*.jsonl")

for file_name in crawl_files:
    print(file_name)
# file_name = "coronavirus-tweet-id-2020-01-24-16.jsonl"
    with open(file_name) as f:
        users_data = [json.loads(line) for line in f]



    out_file_name = "url_project_data/"+file_name.replace(".jsonl","")+"_URL_DATA.txt"

    dd = []
    for i in users_data:
        if i.get("retweeted_status") is not None:

            if len(i['entities']['urls']) >0:
                dd.append(get_details_tweet_Retweet(i))

    dump_2_csv(dd,out_file_name)

