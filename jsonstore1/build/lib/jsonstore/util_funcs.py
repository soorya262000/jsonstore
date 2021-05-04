import os
import datetime
from .constants import *
import re

def get_proper_filename(filename):
        #print(filename)
        if filename!="":
            try:
                if os.path.exists(filename):
                    return filename
                else:
                    with open(filename,'w') as f:
                        pass
                    return filename
            except Exception as e:
                raise e
        name="store_"+str(datetime.datetime.now()).replace(" ","_").replace(":","_").replace(".","_")+".json"
        name=os.path.join(DEFAULT_FILE_NAME,name)
        #print("opening store in location",name)
        with open(name,'w') as f:
            pass
        return name


def is_valid_regex(exp):
    try:
        re.compile(exp)
        return True
    except re.error:
        return False