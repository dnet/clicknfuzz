import random 
import fuzzer_base

class Fuzzer(fuzzer_base.FuzzerBase):
    string_chars=list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    def __init__(self,config,data=''):
        super(Fuzzer,self).__init__(config,data)
        self.byte=1
        self.min_chars=4
        self.strings=self.find_strings()
        self.max_iterations=int(config['max_iterations'])
        self.max_length=int(config['max_length'])
        self.min_length=int(config['min_length'])

    def next(self):
        if len(self.strings)==0:
            raise StopIteration

        if self.max_iterations>0:
            self.max_iterations=self.max_iterations-1
            s=self.strings[random.randint(0,len(self.strings)-1)]
            return self.data[0:s[0]]+chr(random.randint(1,255))*random.randint(self.min_length,self.max_length)+self.data[s[1]:]
        else:
            raise StopIteration

    def set_data(self,data):
        self.data=data
        self.strings=self.find_strings()
        
    def find_strings(self):
        i=0
        begin=None
        end=None
        ret=[]

        for c in self.data:
            if c in self.string_chars:
                if begin is None:
                    begin=i
                else:
                    end=i
            else:
                if end is not None:
                    if end-begin>=self.min_chars:
                        ret.append((begin,end))
                    begin=None
                    end=None
            i=i+1
        if begin is not None:
            ret.append((begin,i-1))

        return ret

if __name__ == "__main__":
    import sys
    for f in Fuzzer({"param": "value"},"pinapina pinapina"):
        print f
