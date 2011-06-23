class FuzzerBase(object):
    def __init__(self,config,data):
        self.config=config
        self.data=data

    def set_data(self,data):
        self.data=data
    
    def __iter__(self):
        return self
