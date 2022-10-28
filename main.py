# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 17:02:56 2022

@author: benro
"""

from Models import *

# Initialise model
dfa = NFA()

# Set the states for the model
states = ['s', 1, 2, 3]
dfa.setStates(states)

# Set the alphabet for the model
alphabet = set()
alphabet.add('a');  alphabet.add('b');  alphabet.add('c')
dfa.setAlphabet(alphabet)

# Initialise transitions
dfa.addTransition('s', 'e', 1); dfa.addTransition('s', 'e', 2); dfa.addTransition('s', 'e', 3)
dfa.addTransition(1, 'b', 1);   dfa.addTransition(1, 'c', 1)
dfa.addTransition(2, 'a', 2);   dfa.addTransition(2, 'c', 2)
dfa.addTransition(3, 'a', 3);   dfa.addTransition(3, 'b', 3)

# Intialise initial and accepting states
dfa.setInitialState('s')
dfa.setAcceptingStates(['s', 1, 2, 3])

import random

# inp = ''.join([list(alphabet)[int(random.random() * 3) - 1] for _ in range(5)])
# dfa.check(inp, verbose = 1)

print(str(dfa))
print(str(FiniteAutomata().toDFA(dfa)))