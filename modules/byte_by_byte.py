import fuzzer_base

class Fuzzer(fuzzer_base.FuzzerBase):
    def __init__(self,config,data=''):
        super(Fuzzer,self).__init__(config,data)
        self.index=len(data)
        self.byte=1

    def set_data(self,data):
        self.data=data
        self.index=len(data)

    def __iter__(self):
        return self

    def next(self):
        if self.index == 0:
            raise StopIteration
        self.byte=self.byte-1
        if self.byte==0:
            self.index=self.index-1
            self.byte=255
        return self.data[0:self.index]+chr(self.byte)+self.data[self.index+1:]


