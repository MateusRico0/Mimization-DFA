import numpy as np
import pandas as pd

L = []
F = []

#FUNCTIONS:

def equalColum(m,line,pas,States):
    for i in range(States):
        print('1: ',m[i][pas],'2:',m[line][pas],'------- i:',i,'line',line,'pas',pas)
        if(line != i):
            print("join")
            if(m[i][pas] == m[line][pas]):
                return i
    return 0

def checkall(m,line1,line2,pas):
    count = 0
    for i in range(pas):
        i +=1
        if(m[line1][i] == m[line2][i]):
            count += 1
        elif((m[line1][i] == m[line1][0]) and (m[line2][i] == m[line2][0])): # goes to itself
            count += 1

    if(count == pas):
        return 1
    else:
        return 0

def goesto(m,States,Pass,line1,line2):
    aux1 = []
    aux2 = []
    for i in range(States):
        for ii in range(Pass):
            ii += 1
            if(i != line1 and i != line2):
                if( m[i][ii] == line1 and  m[i][ii] == line2):
                   aux1.append(m[i][0])
                elif( m[i][ii] != line1 and m[i][ii] == line2):
                    aux1 = []
                elif( m[i][ii] == line1 and  m[i][ii] != line2):
                    aux2 = []

    if(aux1 == aux2):
        return 1
    else:
        return 0

def listToMatrx(x,stat):    # Convert a list in a matrix
  mat = []
  i = 0
  while x != []:
   mat.append(x[:stat+1]) ####BUG FIX: ESTAVA SÓ STAT E ERA PARA SER STAT+1
   x = x[stat+1:]
   i += 1
  return mat

#it creates a auxiliar state
def auxrow(Pss,stt):
    P = []
    sta = int(stt)+1
    for j in range(Pss):
        P.append(str(sta))
    return P

#READ FILE
NameF = 'trb2.txt'#input("Qual o nome do arquivo? ")

with open(NameF, 'r') as file:
    for line in file:
      for word in line.split():
        L.append(word)

#Defining main variables
Pass = int(L[0])
States = int(L[1])
FinalStates = L[2]
FinalStates = FinalStates.split(",")
for i in range(3):  # Delete all, beside the content table
  L.pop(0)

# Now L is just the matrix, But it is still a list so
LMTR = listToMatrx(L,Pass)
# print(LMTR)

exist = 0

# STEP 0
for i in range(States):
    for ii in range(Pass+1):
        if((LMTR[i][ii] == '-') and (exist == 0)):
            exist += 1
            LMTR.append(auxrow(Pass+1,States))
            States += 1
            LMTR[i][ii] = str(States)
        if((LMTR[i][ii] == '-') and (exist == 1)):
            LMTR[i][ii] = str(States)

mtrBase = np.zeros((States,States))

#STEP 1
for i in range(States):
    for ii in range(States):
        if(i == ii):
            mtrBase[i][ii] = 1
        if((str(i+1) in FinalStates) and (str(ii+1) not in FinalStates)):          #+1 because the array starts in 0
            mtrBase[i][ii] = 1
        if(str(ii+1) in FinalStates and (str(i+1) not in FinalStates)):
            mtrBase[i][ii] = 1
#
# print(LMTR)
print("STEP 1:")
print(mtrBase)
print(LMTR)


mtrsize = States
coiote = 0
papaleguas = 1


#STEP 2
while coiote != papaleguas:
    for i in range(States):
        for ii in range(States-1):
            ii +=1
            for iii in range(Pass):
                iii += 1
                ## because it can be more than one for example 2,6
                aux1 = LMTR[i][iii].split(",")
                aux2 = LMTR[ii][iii].split(",")
                for g in range(len(aux1)):
                    for gg in range(len(aux2)):
                 ##
                        if(mtrBase[int(aux1[g])-1][int(aux2[gg])-1] == 1):
                            if(int(aux1[g])-1 != int(aux2[gg])-1):
                                if(mtrBase[i][ii] == 0 ):
                                    mtrBase[i][ii] = 1
                                    mtrBase[ii][i] = 1
                                    papaleguas += 1
    coiote += 1

print(mtrBase)

#STEP 3
print('\n\n\n\n\n')
LI = [[0 for _ in range(1)] for _ in range(States)]
#LI = [States]
for i in range(States):
    LI[i].append(i+1)
    for ii in range(States):
        if(mtrBase[i][ii] == 0):
            LI[i].append(ii+1)


print(LI)
for i in range(len(LI)):
    LI[i].sort()
print(LI)
#AI = np.asarray(LI, dtype=object)

I = [t for t in (set(tuple(i) for i in LI))]            ## sort so they became equalColum
I = [tuple(ele for ele in sub if ele != 0) for sub in I]    ## remove repeated
print(I)
j = 0
for i in range(len(I)):
    i = i - j
    if(len(I[i]) == 1):             ## removing those that have only one
        I.remove(I[i])
        j += 1

print('l',LMTR)
print('I',I)
h =0
for i in range(len(LMTR)):
    i = i - h
    for ii in range(len(I)):
        print('i',i)
        if(LMTR[i][0] == str(I[ii][0])):
            print(I[ii][0],LMTR[i][0])
            for jj in range(len(I[ii])-1):
                print("entrei")
                print('i',i,'ii',ii)
                jj +=1
                hh = 0
                for j in range(len(LMTR)):
                    j = j - hh
                    print('aqui I',I[ii][jj],'l',LMTR[j][0])
                    if(str(I[ii][jj]) == LMTR[j][0]):
                        print('IMA FUCK',I[ii][jj],LMTR[j][0])
                        LMTR.remove(LMTR[j])
                        h += 1
                        hh += 1



for i in range(len(LMTR)):
    for jj in range(Pass + 1):
        for ii in range(len(I)):
            for j in range(len(I[ii])):    # change number of the original states to the equivalent new one
                if(LMTR[i][jj] == str(I[ii][j])):
                    LMTR[i][jj] = str(I[ii])
print('oi',LMTR)

# NewFinal = []
# for i in range(len(I)):
#     for ii in range(len(I[i])):
#         if(I)

for i in range(len(I)):
    for j in range(len(I[i])):
        for ii in range(len(FinalStates)):
            if(FinalStates[ii] == str(I[i][j])):
                FinalStates[ii] = str(I[i])

#delete repeated
FinalStates = np.unique(FinalStates)

# print(I)
 #STEP 4
backing = 0
for i in range(len(LMTR)):
    i -= backing
    repcount = 0
    if LMTR[i][0] not in FinalStates:
        for ii in range(Pass+1):
            if(LMTR[i][ii] == LMTR[i][0]):
                repcount += 1
        if(repcount == (Pass+1)): #+1 here because the range is considering the firt column counting
            numb = LMTR[i][0]
            LMTR = np.delete(LMTR,i,0)
            States -= 1
            backing += 1
            for j in range(len(LMTR)):
                for jj in range(Pass + 1):          #cleaning all invalid state appearances
                    if (LMTR[j][jj] == str(numb)):
                        LMTR[j][jj] = '-'



# WRITE THE NEW FILE
file1 = open('Minimummm.txt', 'w')
file1.write("Qtd letters: "+str(Pass)+'\n')  # qt letters
file1.write("Number of states: "+str(len(LMTR))+'\n')  # Number of states
file1.write("FinalStates: "+str(FinalStates)+'\n')
for i in range(len(LMTR)):  # the matrix
    for ii in range(Pass+1):
        file1.write(str(LMTR[i][ii])+' ')
    file1.write('\n')
file1.close()

print("DONE :)")
print("Check in the directory for Minimummm.txt")
