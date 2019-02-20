import numpy as np 

class Stick:
    def __init__(self, size=12):
        self.size=int(size)
        self.composed=[]
        self.sum=0
    def __eq__(self, bar):
        c1=self.count()
        c2=bar.count()
        if len(c1)!=len(c2):
            return False
        for i in c1:
            try:
                if c1[int(i)]!=c2[int(i)]:
                    return False
            except:
                return False
        return True
    
    def count(self):
        tmp = []
        for i in self.composed:
            tmp.append(int(i.size))
        tmp_set = list(set(tmp))
        tmp_count = {}
        for i in tmp_set:
            tmp_count[i]=tmp.count(i)
        return tmp_count

    def add(self, stick):
        if self.sum+stick.size>self.size:
            return False
        else:
            self.sum+=stick.size
            self.composed.append(stick)
            return True

    def evaluate_lost(self):
        return self.size-self.sum
    
    def pprint(self):
        print("-- Stick(size="+str(self.size)+" composed by ",end='')
        for i in self.composed:
            i.pprint()
        print(")  -- ",end='')

class SetStick:
    def __init__(self, needs=[]):
        self.lost=0
        self.need=0
        for i in needs:
            self.need+=int(i)
        self.sticks=[]

    def add(self, stick):
        self.sticks.append(stick)

    def __eq__(self, set2):
        counted=[]
        for i in self.sticks:
            found = False
            for j in set2.sticks:
                if set2.sticks.index(j) not in counted and i.__eq__(j):
                    found = True
                    counted.append(set2.sticks.index(j))
                    break
            if not found:
                return False
        return True


    def evaluate_lost(self):
        summ = 0
        for i in self.sticks:
            summ+=i.evaluate_lost()
        
        return summ
    
    def pprint(self):
        for i in self.sticks:
            i.pprint()


def CreateSet(needs, max_sizes):
    se_t=SetStick(needs)
    for i in range(0, len(needs)):
        for j in range(i+1, len(needs)):
            if needs[i]+needs[j] in max_sizes.keys:
                print("Heyyy")


max_sizes={12:3,10:2}
needs=[12,5,4,5,4,2,2]
