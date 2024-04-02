# Maltais, 20244617
# Zhang, 20207461

import math

#Fonction à compléter. Ne modifiez pas sa signature.
#N : Force maximale
#k : Nombre de fenêtres disponibles
#Valeur de retour : le nombre minimal de tests qu'il faut faire 
#                   en pire cas pour déterminer le seuil de solidité 
#                   d'une fenêtre
#Doit retourner la réponse comme un int.
#
#Function to complete. Do not change its signature.
#N : Maximum force
#k : Number of windows available
#return value : Minimum number of tests needed in the worst case
#               to find the solidity threshold of a window
#Must return the answer as an int. 


def pure_maths(N, k):

    last = (k - 1) + (N / (2**(k-1)))//1
    if(N / (2**(k-1)) >= 2):
        last -= 1

    if(2**(k-1) >= N):
        last = math.ceil(math.log2(N))

    return last

def minTrials(n, k):

    # Initialize array of size (n+1) and m as moves.

    dp = [0 for i in range(n+1)]

    m = 0

    while dp[n] < k:

        m += 1

        for x in range(n, 0, -1):

            dp[x] += 1 + dp[x - 1]
        
    return m


def dynamic(N, k, trucs):

    if(2**(k-1) >= N):
        return math.ceil(math.log2(N)) + trucs

    if(k == 1):
        return N - 1 + trucs
    
    if(N <= 2):
        return 1 + trucs
    
    if(N == 3):
        return dynamic(N // 2, k, trucs + 1)


    val1 = dynamic((N // 2) - 1, k-1, trucs + 1)
    #Mirroir ne brise pas
    val2 = dynamic(N // 2, k, trucs + 1)


    #On essaie des splits differents
    minSplit = max(val1,val2)

    for i in range(3,N // 4):
        minSplit = min(minSplit, max(dynamic((N // i) - 1, k-1, trucs + i - 1), dynamic(N // i, k, trucs + i-1)))


    return min(max(val1,val2), minSplit)



def vitre(N, k):
    return dynamic(N,k,0)


#Fonction main, vous ne devriez pas avoir à modifier
#Main function, you shouldn't have to modify it
def main(args):
    N = int(args[0])
    k = int(args[1])

    answer = vitre(N,k)
    print(answer)

if __name__ == '__main__':
    main(sys.argv[1:])