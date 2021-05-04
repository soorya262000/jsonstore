import os
from .document import configdocument,datadocument
from .util_funcs import get_proper_filename
from .constants import *




class jsonstore():
    def __init__(self):
        self._configstore=configdocument()
        self._datastore=None
    def exit(self):
        #self.datastore.clear_expired()
        if self._datastore:
            self._datastore.close()
        #self.configstore.handle.close()
        #print(self.datastore.get_filename())
        self._configstore.delete(self._datastore.get_filename())
        self._configstore.close()

    def open_store(self,filename=""):
        filename=get_proper_filename(filename)
        self._configstore.check_status(filename)        
        self._datastore=datadocument(filename)
        return self._datastore





    

    @property
    def configstore(self):
        return self._configstore





