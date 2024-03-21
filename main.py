### IMPORTS ###
import sys
import os.path

### CREATE EMPTY STACK ###
stack = [] 

### CREATE EMPTY TRANSITION LIST ###
transitionList = []

### VARIABLES ###
nextAvailState = 1

### DEFINE nfaNode CLASS ###
class nfaNode():
    def __init__ (self, startState, acceptState, symbolread):
        self.startState = startState
        self.acceptState = acceptState
        self.symbolread = symbolread
    def get_startState(self):
        return self.startState
    def get_acceptState(self):
        return self.acceptState
    def get_symbolread(self):
        return self.symbolread
    def __str__ (self):
        return "Start: q" + str(self.startState) + "\nAccept: q" + str(self.acceptState)

### DEFINE transitionNode CLASS ###
class transitionNode():
    def __init__ (self, state1, state2, symbolread):
        self.state1 = state1
        self.state2 = state2
        self.symbolread = symbolread
    def get_state1(self):
        return self.state1
    def get_state2(self):
        return self.state2
    def get_symbol(self):
        return self.symbolread
    def __str__ (self):
        return "(q" + str(self.state1) + ", " + str(self.symbolread) + ") -> q" + str(self.state2)

### CHECK NUMBER OF COMMAND LINE ARGS ###
commandLineArgs = len(sys.argv)
#print (sys.argv)

if commandLineArgs > 2 or commandLineArgs < 2:
    print("Error, too many or too few command line args.\n")
    exit()
elif commandLineArgs == 2:
    #print("2 command line args confirmed.\n")
    file = sys.argv[1] # file is equal to 2nd thing on command line

### CHECK IF sys.argv[1] EXISTS ###
if os.path.isfile(file) == False:
    print("Your file doesn't exist.")
    exit()
elif os.path.isfile(file) == True:
    f = open(file, "r")
    text = f.read() # Read in file
    #print(text)

### CHECK IF FILE CONTAINS UNAUTHORIZED CHARS ###
allowedChars = ['a', 'b', 'c', 'd', 'e', 'E', '&', '*', '|', '\n']
for i in text: # Loop through each char in text
    #print(i)
    if i not in allowedChars: # If char doesn't match one in allowedChars list
        print("Unauthorized character ")
        exit()
#print("All characters are authorized\n") # All chars checked, all chars in allowedChars list

#print(text) # This works for printing file line by line
#print("done\n")

### TURN TEXT FILE INTO A LIST OF LINES ###
listOfLines = text.split('\n')
#for x in range(len(listOfLines)):
    #print ("<" + listOfLines[x] + ">")
listOfLines.pop() # Remove last item from listOfLines... it's empty for some reason

### BEGIN MAIN LOOP, READING IN 1 SYMBOL AT A TIME ###
for lineBeingExamined in listOfLines:
    n = 0
    lengthOfLine = len(lineBeingExamined)
    #print ("Line being examined: " + lineBeingExamined)
    #print ("Length of line being examined: " + str(lengthOfLine))
    
    #print ("RE: " + lineBeingExamined)
    while n < lengthOfLine:
        symbol = lineBeingExamined[n]

        ### a, b, c, d, e or E SYMBOL READ ###
        #print ("symbol passed in: " + str(symbol))
        if (symbol == 'a') or (symbol =='b') or (symbol == 'c') or (symbol =='d') or (symbol == 'e') or (symbol == 'E'):
            startState = nextAvailState 
            acceptState = nextAvailState + 1
            nfa = nfaNode(startState, acceptState, symbol) # Create new NFA that accepts that symbol
            stack.append(nfa) # Push newly created NFA to stack
            #print (nfa)
            transition = transitionNode(startState, acceptState, symbol) # Create a new transition node
            transitionList.append(transition) # Add transition node to transitionList
            #for x in range(len(transitionList)):
                #print (transitionList[x])
            nextAvailState = nextAvailState + 2 # Update nextAvailState
            n = n + 1
            continue # TODO: Do I need this continue here?

        ### * SYMBOL READ ###
        elif symbol == '*':
            if len(stack) == 0: # Check if stack is empty before pop.
                print ("Attempting to pop from empty stack.  Error.\n")
                exit()
            #if len(stack) != 1: # Must have only one item in stack for * operator
                #print ("Malformed RE.  Error.\n")
                #exit()
            oldnfa = stack.pop()
            startState = nextAvailState
            acceptState = startState
            transition1 = transitionNode(startState, oldnfa.startState, 'E')
            transitionList.append(transition1)
            transition2 = transitionNode(oldnfa.acceptState, startState, 'E')
            transitionList.append(transition2)
            #for x in range(len(transitionList)):
                #print (transitionList[x])
            newnfa = nfaNode(startState, acceptState, 'E')
            #print (newnfa)
            stack.append(newnfa) # Push newly created NFA to stack
            nextAvailState = nextAvailState + 1 # Update nextAvailState
            n = n + 1 # Update n to iterate through lineBeingExamined

        ### & SYMBOL READ ###
        elif symbol == '&':
            if len(stack) == 0: # Check if stack is empty before pop.
                print ("Attempting to pop from empty stack.  Error.\n")
                exit()
            #if len(stack) != 2: # Check if stack is empty before pop.
                #print ("Malformed RE.  Error.\n")
                #exit()
            oldnfa2 = stack.pop() # Pop NFA from top of stack (call it oldnfa2)
            oldnfa1 = stack.pop() # Pop remaining NFA from top of stack (call it oldnfa1)
            startState = oldnfa1.startState # Update startState for newnfa
            acceptState = oldnfa2.acceptState # Update acceptState for newnfa
            newnfa = nfaNode(startState, acceptState, '&') # Create newnfa instance/object
            #print (newnfa)
            stack.append(newnfa) # Push newly created NFA to stack
            transition = transitionNode(oldnfa1.acceptState, oldnfa2.startState, 'E') # Create new transition node
            transitionList.append(transition)
            #for x in range(len(transitionList)):
                #print (transitionList[x])
            # No new states added here, just new transitions from already created states
            n = n + 1 # Prepare to examine next character on line

        ### | SYMBOL READ ###
        else: # symbol is |
            if len(stack) == 0: # Check if stack is empty before pop.
                print ("Attempting to pop from empty stack.  Error.\n")
                exit()
            #if len(stack) != 2: # Check if stack is empty before pop.
                #print ("Malformed RE.  Error.\n")
                #exit()
            oldnfa2 = stack.pop() # Pop NFA from top of stack (call it oldnfa2)
            oldnfa1 = stack.pop() # Pop remaining NFA from top of stack (call it oldnfa1)
            startState = nextAvailState
            acceptState = nextAvailState + 1
            newnfa = nfaNode(startState, acceptState, '|')
            #print (newnfa)
            stack.append(newnfa) # Push newly created NFA to stack
            transition1 = transitionNode(startState, oldnfa1.startState, 'E')
            transitionList.append(transition1)
            transition2 = transitionNode(startState, oldnfa2.startState, 'E')
            transitionList.append(transition2)
            transition3 = transitionNode(oldnfa1.acceptState, acceptState, 'E')
            transitionList.append(transition3)
            transition4 = transitionNode(oldnfa2.acceptState, acceptState, 'E')
            transitionList.append(transition4)
            #for x in range(len(transitionList)):
                #print (transitionList[x])
            nextAvailState = nextAvailState + 2 # Update nextAvailState
            n = n + 1 # Prepare to examine next character on line

    ### PREP FINAL PRINT STATEMENTS ###
    finalnfa = stack.pop()        
    print ("RE: " + lineBeingExamined)
    print (finalnfa)
    sortedTransitionList = sorted(transitionList, key = lambda z: z.get_state1()) # Sort transitionList by 1st element of 3-tuple
    for x in range(len(sortedTransitionList)): # Loop through and print all sorted 3-tuple transitions
        print (sortedTransitionList[x])

    ### PREP TO MOVE TO NEXT LINE ###
    nextAvailState = 1 # Reset nextAvailState to 1, preparing for new line to be read in
    transitionList = [] # Clear the transition list
    print ('\n')
    
### CLOSE FILE AT END ###
f.close() # Close file, all done

