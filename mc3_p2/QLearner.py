"""
Template for implementing QLearner  (c) Yuzhou Li
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.alpha = alpha
        self.states = num_states
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.s = 0
        self.a = 0
        self.Q = np.random.rand(100,4)
        self.T = np.array([0]*40000).reshape(100,4,100)
        self.Tc = np.array([0.00001]*40000).reshape(100,4,100)
        self.R = np.array([-0.000001]*400).reshape(100,4)
        

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """

        #self.s = s
        temp = np.random.uniform(0,1)
        if temp<=self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.Q[s,:])
        self.s = s
        self.a = action
        #self.rar = self.rar*self.radr
        if self.verbose: print "s =", s,"a =",action
        return action



    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        #action = rand.randint(0, self.num_actions-1)

        temp = np.random.uniform(0,1)
        if temp<=self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.Q[s_prime,:])
        

        self.Q[self.s,self.a] = (1-self.alpha)*self.Q[self.s,self.a]+self.alpha*(r+self.gamma*self.Q[s_prime,np.argmax(self.Q[s_prime,:])])
        s = self.s
        a = self.a
        #print self.Q
        self.s = s_prime
        self.rar = self.rar*self.radr
        self.a = action

        ########################Dyna Part#####################
        if self.dyna!=0:
            #UPDATE MATRIX#
            self.Tc[s,a,s_prime]+=1
            summ = 0
            for i in range(0,self.num_actions):
                summ += self.Tc[s,a,i]
            self.T[s,a,s_prime] = self.Tc[s,a,s_prime]/summ
            #print self.T
            self.R[s,a] = (1-self.alpha)*self.R[s,a]+self.alpha*r
            #DYNA ITERATION#
            for i in range(0,self.dyna):
                temps = rand.randint(0,99)
                tempa = rand.randint(0,self.num_actions-1)
                tempsp = np.argmax(self.T[temps,tempa,:])
                tempr = self.R[temps,tempa]
                self.Q[temps,tempa] = (1-self.alpha)*self.Q[temps,tempa]+self.alpha*(tempr+self.gamma*self.Q[tempsp,np.argmax(self.Q[tempsp,:])])


        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
