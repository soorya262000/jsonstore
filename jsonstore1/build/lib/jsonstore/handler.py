import json
import os
from .constants import *


class handler:
    def __init__(self,filename):
        self._file=self.open_file(filename,'r+')
        
    def write(self,data):
        if data[1]==-1 and data[2]==-1:
            self._file.seek(0,2)
            start=self._file.tell()
            self._file.write(json.dumps(data[0]))
            end=self._file.tell()
            self._file.flush()
            return start,end
        if data[1]==-2 and data[2]==-2:
            self._file.seek(0)
            self._file.write(json.dumps(data[0]))
            self._file.truncate()
            self._file.flush()
        else:
            self._file.seek(data[1])
            self._file.write(json.dumps(data[0]))
            end=self._file.tell()
            self._file.flush()
            return data[1],end
        
    def read(self,data=None):
        if not data:            
            self._file.seek(0)
            data=self._file.read()
            #print(data)
            ##print(data,"inside handler")
            if data=="":
                return dict()
            else:
                return json.loads(data)
        else:
            self._file.seek(data[0])
            value=self._file.read(data[1])
            ##print(value)
            return json.loads(value)
    
    def close(self):
        #print("in close")
        self._file.flush()
        os.fsync(self._file.fileno())
        self._file.close()

    
            

    def get_filename(self):
        return os.path.realpath(self._file.name)

    def get_file_size(self):
        self._file.seek(0,2)
        size=self._file.tell()
        return size

    def open_file(self,filename,mode):
        return open(filename,mode)
