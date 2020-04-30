import types

from modules import basics


class DictSavable:
    def __init__(self,defaults,kwargs,exclude=[]):
        self.setfromdict(defaults,exclude=exclude)
        self.setfromdict(kwargs,exclude=exclude)

    def setfromdict(self,dict,*,exclude=[]):
        for k,i in dict.items():
            if k not in exclude:
                setattr(self, k, i)
            
    def getdict(self):
        d={}
        for name in dir(self):
            value = getattr(self,name)
            if ("method" not in str(type(value)) and not name.startswith("SAVETODICT_")) and not name.startswith("__") and name!="bot":
                d[name]=value
        return d

                
    def save(self):
        pass