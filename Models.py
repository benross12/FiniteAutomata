# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 11:42:02 2022

@author: benro
"""

class State:
    def __init__(self, name):
        self.name = name
        self.transitions = []
    
    def nextState(self, letter):
        '''
        Fetch the next state, based on the letter read

        Parameters
        ----------
        letter : string
            letter read from the word

        Returns
        -------
        State
            The next state in the Automata

        '''
        for t in self.transitions:
            if t.letter == letter:
                return t.end
    
    def __str__(self):
        return f"State - {self.name}"

class Transition:
    def __init__(self, start, letter, end):
        self.start = start
        self.letter = letter
        self.end = end
    
    def __str__(self):
        return f"({self.start.name}, {self.letter}, {self.end.name})"

class FiniteAutomata:
    '''
    Blueprint class for both DFA's and NFA's
    
    Contains methods relevant to both
    '''
    
    def __init__(self):
        
        self.states = None
        self.alphabet = None
        self.initialState = None
        self.acceptingStates = None
                
    def setStates(self, names):
        self.states = [State(name) for name in names]
        
    def setAlphabet(self, a):
        self.alphabet = a
        
    def setInitialState(self, name):
        self.initialState = self.getState(name)
    
    def setAcceptingStates(self, names):
        self.acceptingStates = []
        for name in names:
            self.acceptingStates.append(self.getState(name))
    
    def getState(self, name):
        '''
        Fetch a given state from it's name

        Parameters
        ----------
        name : int
            Name / number of the state

        Returns
        -------
        s : State
            State called name

        '''
        for s in self.states:
            if s.name == name:
                return s
            
    def addTransition(self, startName, letter, endName):
        '''
        Add a transition to the DFA
        
        Adds the transition to the relevant state object

        Parameters
        ----------
        startName : int
            Name / number of the starting state
        letter : string
            Transition letter
        endName : int
            Name / number of the state to move to

        Returns
        -------
        None.

        '''
        
        transition = Transition(self.getState(startName), \
                                letter, self.getState(endName))
            
        self.getState(startName).transitions.append(transition)

    def __str__(self):
        # Get all the parameters as strings
        states = [str(s) for s in self.states]
        acceptingStates = [str(a) for a in self.acceptingStates]
        
        out = f"Alphabet - {self.alphabet}\nStates - {states}\nInitial State - {str(self.initialState)}\nAccepting States - {acceptingStates}\n"
        return out    


class DFA(FiniteAutomata):
    '''
    Implementation of a DFA checking algorithm
    '''
    
    def check(self, word, verbose = 1):
        if any(c not in self.alphabet for c in word):
            if verbose > 0:
                print(f"'{word}' contains letters not in the alphabet")
            return False
        
        # Get the starting state
        current = self.initialState
        wordCopy = word
        
        # Loop through the word until we have read it all
        while len(word) > 0:
            if verbose > 1:
                print(str(current))
                
            current = current.nextState(word[:1])
            word = word[1:]
            
        # Accept the word if we aren't in an accepting state, else reject
        if current in self.acceptingStates:
            if verbose > 0:
                print(f"Accept '{wordCopy}'")
            return True
        else:
            if verbose > 0:
                print(f"Reject '{wordCopy}'")
            return False
        
class NFA(FiniteAutomata):
    '''
    Implementation of an NFA checking algorithm
    '''
    
    def check(self, word, verbose = 1):
        self.alphabet.add('e')
        
        if any(c not in self.alphabet for c in word):
            if verbose > 0:
                print(f"'{word}' contains letters not in the alphabet")
            return False
        
        # Get the starting state
        wordCopy = word
        stack = [(self.initialState, word)]
        
        while len(stack) > 0:
            state = stack.pop(-1)
            
            if verbose > 1:
                print(str(state[0]), state[1])
            
            # if word length is 0 and state is accepting, word is accepted
            if len(state[1]) == 0 and state[0] in self.acceptingStates:
                if verbose > 0:
                    print(f"Accept '{wordCopy}'")
                return True
            
            # Generate the possible next states, and push them to the stack
            for t in state[0].transitions:
                if t.letter == state[1][:1]:
                    newState = (t.end, state[1][1:])
                    stack.append(newState)
                elif t.letter == "e":
                    newState = (t.end, state[1])
                    stack.append(newState)
                    

        # If we haven't found any accepting states, reject the word
        if verbose > 0:
            print(f"Reject '{wordCopy}'")
        return False
            