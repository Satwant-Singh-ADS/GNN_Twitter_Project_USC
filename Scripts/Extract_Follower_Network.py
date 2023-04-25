import gzip
import json

from tqdm import tqdm
from twarc import Twarc
from pathlib import Path

import time



import json

from tqdm import tqdm
from twarc import Twarc
from pathlib import Path


# In[3]:
import gzip
import json

from tqdm import tqdm
from twarc import Twarc
from pathlib import Path

import time


consumer_key = "ur-key"

consumer_secret = "ur-key"

access_token = "ur-key"

access_token_secret = "ur-key"



print("Start Time : {}".format(time.ctime()))

twarc = Twarc(consumer_key, consumer_secret, access_token, access_token_secret)


def raw_newline_count(fname):
    """
    Counts number of lines in file
    """
    f = open(fname, 'rb')
    f_gen = _reader_generator(f.raw.read)
    return sum(buf.count(b'\n') for buf in f_gen)


# In[4]:


def _reader_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)




import os

### Keep txt files in current working directory or change code below. Each txt file contains list of twitter screen names. We use twarc follower_ids API to get list of all followers


for path in Path("./").iterdir():
    if path.name.endswith('_ids.txt'):
        with open(path) as fin:
            ids = [w.replace("\n",'') for w in fin.readlines()]
            
        with tqdm(total=len(ids)) as pbar:
            for screen_nm in ids:
                write_path = screen_nm+"_followers.txt"
                if not os.path.isfile(write_path):
                    
                    with open(write_path, 'w') as output:
                        try:
                            for follower in twarc.follower_ids(screen_nm):
#                                 print(screen_nm,follower)
                                output.write(follower+"\n")
                        except:
                            print("error")
                elif os.stat(write_path).st_size == 0:
                    with open(write_path, 'w') as output:
                        try:
                            for follower in twarc.follower_ids(screen_nm):
#                                 print(screen_nm,follower)
                                output.write(follower+"\n")
                        except:
                            print("error")
                    
                    pbar.update(1)
                    print(path) 
            
