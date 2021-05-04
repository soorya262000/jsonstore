import json
import os
import sys
from abc import ABC,abstractmethod
import datetime
from .handler import handler
from .util_funcs import get_proper_filename,is_valid_regex
from .constants import *
import re

class document(ABC):

    @abstractmethod
    def read(self):
        raise NotImplementedError('To be overridden!')

    @abstractmethod
    def delete(self):
        raise NotImplementedError('To be overridden!')

    
    @abstractmethod
    def add(self):
        raise NotImplementedError('To be overridden!')



    


class datadocument(document):
    def __init__(self,filename=""):
        
        self._meta=metadocument(filename)
        
    def read(self):
        pass

    def get(self,key):
        return self._meta.get(key)       
        
    
    def add(self,key,value,expiry=-1):
        if isinstance(key,str):
            if len(key)<=32:
                if self.get_size(value)<=16:
                    return self._meta.add(key,value,expiry)
                    
                else:
                    return False,"Value size must be less than 16kb"
                    
            else:
                return False,"Key length must be less than or equal to 32"
        else:
            return False,"Key must be a string"        

            
    def delete(self,key):
        return self._meta.delete(key)

    def close(self):
        self._meta.close()

    def get_filename(self):
        return self._meta.get_filename()

    def get_size(self,data):
        return sys.getsizeof(json.dumps(data))/1000
    def change_expiry(self,key):
        pass

    def get_all(self,exp):
        if is_valid_regex(exp):
            return self._meta.get_all(exp)
        else:
            raise Exception("Invalid regex")


    def delete_all(self,exp):
        if is_valid_regex(exp):
            return self._meta.delete_all(exp)
        else:
            raise Exception("Invalid regex")


            
                
            
        
        
    
            
 
   

    

class configdocument(document):
    def __init__(self):
        filename=os.path.join(os.path.dirname(os.path.realpath(__file__)),"config.json")
        #print(filename)
        filename=get_proper_filename(filename)
        self._handle=handler(filename)
        self._data=self.read()
        #print(type(self._data["stores"]))
        ##print(type(self._data))
        
            
    def read(self):
        data=self._handle.read()
        ##print(data,"inside config")
        if data=={}:
            return {"opened_stores":[],"stores":set()}
        else:
            data["stores"]=set(data["stores"])
            return data
    
    def add(self):
        tempdata=self._data.copy()
        tempdata["stores"]=list(tempdata["stores"])
        self._handle.write([tempdata,-2,-2])
        #self._data["stores"]=set(self._data["stores"])
        
    def update(self):
        pass

    def get(self):
        pass
    
    def delete(self,filename):
        if filename in self._data["opened_stores"]:
            self._data["opened_stores"].remove(filename)
            ##print(self._data,"inside delete")
            self.add()

    def close(self):
        self._handle.close()

    def get_stores(self):
        return self._data["stores"]

    def get_open_stores(self):
        return self._data["opened_stores"]

    def check_status(self,filename):
        #print("in check status",self._data)
        if filename in self._data["opened_stores"]:
            raise Exception("store is already open")
        else:
            self._data["opened_stores"].append(filename)
            ##print(self._data,"inside else")
            self._data["stores"].add(filename)
            self.add()

    def nuke_config(self):
        self._data["opened_stores"]=[]
        self.add()
        
    @property
    def handle(self):
        return self._handle


class metadocument(document):

    def __init__(self,filename):
        metafilename=filename+".meta"
        metafilename=get_proper_filename(metafilename)
        self._handle=handler(metafilename)
        self._data_handle=handler(filename)
        self._data=None
        self._data=self.read()
        self._times_modified=0

    def read(self):
        data=self._handle.read()
        if data=={}:
            return {"deleted_blocks":[]}
        else:
            return data
    
    def add(self,key,value,expiry):
        ##print(key,value)
       ##print(self.get_file_size()/1e+6)
        created_at=str(datetime.datetime.now())
        if key in self._data:
            if self.checkvalidity(key):
                return False,"key already present"
            else:
                self.delete(key)
        if self.get_file_size()/1e+6 <= MAX_FILE_SIZE:
            ##print("wwor")
            start,end=self._data_handle.write([value,-1,-1])
            self._data[key]=[start,end-start,created_at,expiry]
            #print(self._data,"inside add")
        else:
            if len(self._data["deleted_blocks"])>0:
                for i in range(len(self._data["deleted_blocks"])):
                   ##print(len(value),(self._data["deleted_blocks"][i][1]-self._data["deleted_blocks"][i][0]))
                    if len(value)<= (self._data["deleted_blocks"][i][1]-self._data["deleted_blocks"][i][0]):
                        start,end=self._data_handle.write([value,self._data["deleted_blocks"][i][0],-1])
                        self._data["deleted_blocks"][i][0]=end
                        self._data[key]=[start,end-start,created_at,expiry]
                        self._times_modified+=1
                        if self._times_modified>=MAX_MOD_COUNT:
                            self.force_write()


                        return True,value


            return False,"Max file size reached"

        self._times_modified+=1
        if self._times_modified>=MAX_MOD_COUNT:
            self.force_write()
        return True,value


        
        
    def update(self):
        pass

    def get(self,key):
        if key in self._data:
            if self.checkvalidity(key):
                data=self._data_handle.read(self._data[key])
                return True,data
            else:
                self.delete(key)
                return False,"key expired"
        else:
            return False,"key not found"


    def get_all(self,exp):
        result=[]
        for val in self._data:
            if val!="deleted_blocks":
                if bool(re.search(exp,val)):
                    result.append(self.get(val))
        return result

    
    def delete(self,key):
        if key in self._data:
            valid=self.checkvalidity(key)
            delete_block=[self._data[key][0],self._data[key][0]+self._data[key][1]]
            del self._data[key]
            self._data["deleted_blocks"].append(delete_block)
            self._times_modified+=1
            if self._times_modified>=MAX_MOD_COUNT:
                self.force_write()
            if valid:
                return True,"key deleted"
            else:
                return False,"key expired"

        else:
            return False,"key not present"

    def delete_all(self,exp):
        result=[]
        for val in self._data:
            if val!="deleted_blocks":
                if bool(re.search(exp,val)):
                    result.append(self.delete(val))
        return result
        
    def close(self):
        self.force_write()
        ##print(self._data)
        self._handle.close()
        self._data_handle.close()

    def force_write(self):
        self._handle.write([self._data,-2,-2])
        ##print(len(self._data))


    def checkvalidity(self,key):
        delta=datetime.datetime.now()-datetime.datetime.strptime(self._data[key][2],'%Y-%m-%d %H:%M:%S.%f')
        if self._data[key][3]!=-1 and (delta.total_seconds()/60 >= self._data[key][3]):
            return False
        else:
            return True

    def get_filename(self):
        return self._data_handle.get_filename()

    def get_file_size(self):
        return self._data_handle.get_file_size()
        
    @property
    def handle(self):
        return self._handle

    @property
    def data_handle(self):
        return self._data_handle
    


