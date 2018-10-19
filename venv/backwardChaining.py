class instruction:
    instruction = ""
    #Mode = 0 is ^ and mode = 1 is v
    Mode = None
    valid = False
    def __eq__(self, other):
        if(self.instruction == other.instruction and self.Mode == other.Mode):
            return True
        else:
            return False
    def __init__(self, input, mode):
        self.instruction = input
        self.Mode = mode

    def print(self):
            print(self.Mode," ",self.instruction)

class solver:
    # This is the list of instructions
    kbList = []
    # Using a set for the store string instructions to remove duplicates
    kbList1 = set()
    stack = list()
    def __init__(self):
        self.getKB()


    #finds all the KB properties that match
    def getresultKB(self, char):
        solveKBList = []
        for i in self.kbList:
            if i.instruction[-1] == char:
                solveKBList.append(i)
            else:
                continue
        return solveKBList




    #Input validation
    def putKB(self, userinput):
        #Input Checking
        if(not userinput.isalpha() and len(userinput) == 1):
            return False
        if(len(userinput) > 1 and len(userinput) < 5):
            return False
        if (len(userinput) > 5 and userinput[-2] != ">"):
            return False
        if("^" in userinput and "v" in userinput):
            return False
        if(not userinput[-1].isalpha()):
            return False
        #Input is valid, therefore insert into set
        self.kbList1.add(userinput)

        return True


    #Making list of instructions
    def makeKB(self, kbList1):
        for i in kbList1:
            #deciding the modes
            if ("^" in i):
                mode = 0
            elif ("v" in i):
                mode = 1
            else:
                mode = 2
            #Only want AlphaNumeric letters
            S = []
            for c in i:
                if (c.isalpha() and c != 'v'):
                    S.append(c.upper())
                #cleaned A^B^C>D into ABCD + mode = 0
            cleaned = "".join(S)
            #create new item for instruction A^B^C>D into ABCD + mode = 0
            newItem = instruction(cleaned, mode)
            #put into the knowledge base
            self.kbList.append(newItem)

    def getKB(self):
        #getting userinput for KB
        print("Knowledge base is a finite set of formulas of the following three forms\n"+
              "P1^P2^...^Pk => P\nPvP2v...vPk => P\nP\n" +
              "Press ENTER to provide KB with more information else"
				+ " to end, hit '#' followed by ENTER")
        while True :
            userinput = input()
            if("#" in userinput):
                break
            if(not self.putKB(userinput)):
                print("Bad Input" + userinput)
        #make the list of instructions from the string of instructions
        self.makeKB(self.kbList1)

    def dfsSearchTree(self, input):
       startlist = self.getresultKB(input)
       #For checking if input can be proved by at start
       for i in startlist:
           if len(i.instruction) == 1:
               print("Found", i.instruction, "depth 1")
               return True
           if self.solve(startlist):
               return True

    # uses recursion to build dfs tree and solve the statement
    def solve(self, listResults):
        # Loops through all the options
        for i in listResults:
            i.print()
            #if instruction mode 2, it means it's in the list
            if (i.Mode == 2):
                print(i.instruction, "is true")
                return True
            #for AND searches where everything must be true
            if (i.Mode == 0):
                for c in i.instruction[:-1]:

                    newResults = self.getresultKB(c)
                    #if recursion returns false for one, return false for all
                    if not self.solve(newResults):
                        return False
                #Everything was satisfied
                return True

            #for OR searches where one must be true
            elif(i.Mode == 1):
                    for c in i.instruction[:-1]:
                        newResults = self.getresultKB(c)
                        if self.solve(newResults):
                            return True
            print(i.print(), "Doesn't Exist")
        return False



if __name__ == '__main__':
   start = solver()
   while True:
       print("Type any character to search KB or hit @ to terminate");
       toSolve = input()
       if(toSolve == "quit"):
           break
       if start.dfsSearchTree(toSolve):
           print(toSolve, "is in the Knowledgebase")
       else:
           print(toSolve, "is not the Knowledgebase")