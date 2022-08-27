import json

class SubDb:
    def __init__(self, data: dict | list):
        self.data = data
    
    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise KeyError(f"{key} is not a key of {self.data}")
    
    def __setitem__(self, key, value):
        if type(value) == list or type(value) == dict:
            self.data[key] = SubDb(value)
        else:
            self.data[key] = value
    
    def collapse(self):
        if type(self.data) == dict:
            r = {}
            for k, v in self.data.items():
                if isinstance(v, SubDb):
                    r[k] = v.collapse()
                else:
                    r[k] = v
        else:
            r = []
            for i in self.data:
                if isinstance(i, SubDb):
                    r.append(i.collapse())
                else:
                    r.append(i)
        
        return r

class JsonDb:
    def __init__(self, file: str) -> None:
        self.file = file
        with open(self.file, "r") as f:
            self.data = json.load(f)
    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise KeyError(f"{key} is not a key of {self.data}")
    
    def __setitem__(self, key, value):
        if type(value) == list or type(value) == dict:
            self.data[key] = SubDb(value)
        else:
            self.data[key] = value
        
        with open(self.file, "w") as f:
            f.write(json.dumps(self.collapse()))
    
    def collapse(self):
        if type(self.data) == dict:
            r = {}
            for k, v in self.data.items():
                if isinstance(v, SubDb):
                    r[k] = v.collapse()
                else:
                    r[k] = v
        else:
            r = []
            for i in self.data:
                if isinstance(i, SubDb):
                    r.append(i.collapse())
                else:
                    r.append(i)
        
        return r
    

        