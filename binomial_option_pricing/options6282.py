
# coding: utf-8

# # European Option

# In[49]:


import math
class an_option:
    def __init__(self,T,K,putcall):
        self.T=T
        self.K=K#strike price
        self.type=putcall
class underlying:
    def __init__(self,sigma):
        self.sigma=sigma

class environment:
    def __init__(self,r):
        self.r=r
class a_node:
    def __init__(self,t,i,thetree):
        self.t=t
        self.i=i
        self.mytree=thetree#连接前后时间段的不同nodes
    def grow(self):
        u=self.mytree.u
        d=self.mytree.d
        if self.t==0:
            self.S=self.mytree.S0
        else:
           # if self.i==self.mytree.preiod[self.t].n_nodes-1
            if self.i==self.t:
                self.S=self.mytree.periods[self.t-1].nodes[self.i-1].down
            else:
                self.S=self.mytree.periods[self.t-1].nodes[self.i].up
        #self.S=self.mytree.periods[self.t-1].nodes[self.t].up
        self.up=self.S*u
        self.down=self.S*d
    def getCF(self,opt):
        if self.t == self.mytree.N-1:
            if opt.type == 'call':
                self.value=max(0,self.S - opt.K)
            elif opt.type == 'put':
                self.value = max(0, opt.K - self.S)
            else:
                print('Option type "'+ opt.type+'" unknown. Terminating...')
    def discount(self,env):
        if self.t < self.mytree.N-1:
            upvalue=self.mytree.periods[self.t+1].nodes[self.i].value
            dnvalue=self.mytree.periods[self.t+1].nodes[self.i+1].value
            p=self.mytree.p
            self.value=(upvalue*p+dnvalue*(1-p))*math.exp(-self.mytree.dt*env.r)
                    
class a_period:
    def __init__(self,t,thetree):
        self.t=t
        self.n_nodes= t+1
        self.nodes=[]
        self.mytree=thetree
        for i in range(self.n_nodes):self.nodes=self.nodes+[a_node(t,i,self.mytree)]
class a_tree:
    def __init__(self,N):
        self.N = N
        self.periods=[]
        for t in range(self.N):self.periods=self.periods+[a_period(t,self)]#self代表a_tree
    def grow(self):
        for p in self.periods:
            for n in p.nodes: n.grow()
    def getCF(self,opt):
#        for p in self.periods:
        for t in range(self.N-1,-1,-1):
            p=self.periods[t]
            for n in p.nodes: n.getCF(opt)
    def discount(self,env):
        for t in range(self.N-1,-1,-1):
            p=self.periods[t]
            for n in p.nodes: n.discount(env)        
    def price(self,opt,und,S0,env):
        dt=opt.T/self.N
        u=math.exp(und.sigma*math.sqrt(dt))
        d=1/u
        self.u=u
        self.d=d
        self.p=(math.exp(env.r*dt)-d)/(u-d)
        self.S0=S0
        self.dt=dt
        self.grow()
        self.getCF(opt)
        self.discount(env)
        return(self.periods[0].nodes[0].value)
#The lines above describe the framework that we will need to fill in.


class a_position:
    def __init__(self,what=None,howmuch=0):
        self.instrument=what   
        self.n=howmuch
        
class a_strategy:
    def __init__(self,T,und,strikelist,geo = "European"):        #grandma's level has the T and geo
        self.T = T
        self.geo = geo
        self.und =und
        self.setpositions()
        self.strikes(strikelist)
            
    def price(self,tree,S0,env):
        thesum = 0
        for apos in self.positions:
            thesum = thesum + apos.n * tree.price(apos.instrument,self.und,S0,env)
        return(thesum)
        self.price = thesum
            
class stra(a_strategy):
    def setpositions(self):
        self.npos = 2 
        self.positions =                  [a_position(an_option(self.T,None,'call',self.geo),1)]
        self.positions = self.positions + [a_position(an_option(self.T,None,'put',self.geo),1)]

class a_straddle(stra):
    def strikes (self,strikelist):
        self.positions[0].instrument.K = strikelist[0]
        self.positions[1].instrument.K = strikelist[0]
        
class a_strangle(stra):
    def strikes (self,strikelist):
        self.positions[0].instrument.K = strikelist[0]
        self.positions[1].instrument.K = strikelist[1]
    

