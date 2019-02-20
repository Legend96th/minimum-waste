class Stick: # Representing a stick, each stick may be composed of sub-sticks
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

    def add(self, stick): # Add a substick that compose the main stick
        if self.sum+stick.size>self.size:
            return False
        else:
            self.sum+=stick.size
            self.composed.append(stick)
            return True

    def evaluate_lost(self): # count all the stick size - the stick that is actually used
        return self.size-self.sum
    
    def pprint(self):
        if self.size!=0:
            print("-- Stick(size="+str(self.size),end='')
            for i in self.composed:
                i.pprint()
            print(")  -- ",end='')
    def __str__(self):
        if self.size!=0:
            s="-- Stick(size="+str(self.size)
            for i in self.composed:
                s+=str(i)
            s+=")  -- "
            return s
        else:
            return ""

    def __add__(self, stick2): # Adding 2 substicks produce 1 big stick
        s=Stick(size=self.size+stick2.size)
        s.add(self)
        s.add(stick2)
        return s

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

    def write(self, file="cuts"): # Write a readable set of stick in a file
        w=open(file,'w')
        w.write("STICK ARCHITECTURE : \n")
        w.write(str(self)+"\n")
        w.write("Lost value : "+str(self.evaluate_lost())+"\n")
        w.write("Sticks remaining to craft : "+str(self.needs)+"\n")
        w.write("Sticks remaining for the crafter : "+str(self.max_sizes)+"\n")
        w.close()

    def evaluate_lost(self): # Evaluate the lost = every stick size - its lost
        summ = 0
        for i in self.sticks:
            summ+=i.evaluate_lost()
        
        return summ
    
    def pprint(self):
        for i in self.sticks:
            i.pprint()
        print("\n")

    def __str__(self):
        s=""
        for i in self.sticks:
            s+=str(i)
        return s

def create_set(needs, max_sizes): # Create a set from a list of need and the list of what the crafter have
    se_t=SetStick()
    everything, last_everything, rest, max_sizes = combinations(needs, max_sizes)
    for i in everything:
        s=Stick(size=0)
        for j in i:
            s+=Stick(size=j)
        se_t.add(s)
    for i in last_everything:
        s=Stick(size=i)
        for j in last_everything[i]:
            s2=Stick(size=j)
            s.add(s2)
        se_t.add(s)
    se_t.pprint()
    se_t.needs=rest
    se_t.max_sizes=max_sizes
    print("lost : "+str(se_t.evaluate_lost()))
    return se_t

def get_max(max_sizes): # Get the biggest avaiable stick from the crafter
    maxi=0
    for i in max_sizes:
        if max_sizes[i]!=0 and i>maxi:
            maxi=i
    return maxi


def combinations(needs, max_sizes):  
    max_stick=0
    for i in max_sizes:
        if max_sizes[i]>0 and i>max_stick:
            max_stick=i
    
    everything=[]
    alr=[]
    used=[]
    i=0
    while i<len(needs) and get_max(max_sizes)!=0:  # We generate the optimal sticks with 0 loss
        if i not in used:
            s=()
            summ=needs[i]
            lise=[]
            lised=[]
            answer, lise= combine(s,needs, max_sizes, i, used, lised, summ)
            if answer:
                summ=0
                for j in lise:
                    s+=(j,)
                    summ+=j
                    alr.append(j)
                max_sizes[summ]-=1
                everything.append(s)
        i+=1
    for i in alr:
        needs.remove(i)
    needs.sort()
    maxi=get_max(max_sizes)
    last_everything={}
    while len(needs)!=0 and maxi!=0: # Now that we create the maximum of 0 lost sticks, we can produce the ones with loss
        s=()
        lek=[]
        summ=0
        i=0
        while i <len(needs) and summ+needs[i]<=maxi:
            summ+=needs[i]
            lek.append(needs[i])
            s+=(needs[i],)
            i+=1
        for b in lek:
            needs.remove(b)
        max_sizes[maxi]-=1
        last_everything[maxi]=(s)
        maxi=get_max(max_sizes)
    
    return everything, last_everything, needs, max_sizes

def combine(s ,needs, max_sizes, i, used, lise, summ):# Get the optimal combination of stick to minimize loss
    lise.append(needs[i])
    used.append(i)
    if summ in list(max_sizes.keys()):
        if max_sizes[summ]>0:
            return True, lise
    for j in range(len(needs)):
        if summ+needs[j] in list(max_sizes.keys()):
            if max_sizes[summ+needs[j]]>0 and j not in used:
                lise.append(needs[j])
                used.append(j)
                return True, lise
    for j in range(len(needs)):
        if j not in used:
            summ+=needs[j]
            lisex=[]
            answer, lisex= combine(s, needs, max_sizes,j, used, lise,summ)
            if answer:
                lise=lisex
                return True, lise
            summ-=needs[j]
    used.remove(i)
    lise.remove(needs[i])
    return False, []

def parse_file(file="needs"): # Read a file from where it gets inputs
    f=open(file, 'r')
    r=f.readlines()
    mar=r[0].split('=')[1]
    mar2=mar.split(';')
    max_sizes={}
    for i in mar2:
        g=i.split(":")
        max_sizes[int(g[0])]=int(g[1])
    neer=r[1].split('=')[1]
    mar2=neer.split(';')
    br={}
    needs=[]
    for i in mar2:
        g=i.split(":")
        br[int(g[0])]=int(g[1])
    for j in br:
        needs+=[j]*br[j]
    return max_sizes, needs

max_sizes, needs=parse_file()
se_t= create_set(needs, max_sizes)
se_t.write("cuts")