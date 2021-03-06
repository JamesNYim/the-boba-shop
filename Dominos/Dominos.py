##-----------------------##
# Code by James Yim
# For Stats 80A Final
##-----------------------##

from itertools import count
import random
import matplotlib.pyplot as plt
import numpy as np

#Drawing a domino from the domino set
def drawDomino(dominoSet, playerSet):
        if (len(dominoSet) == 0):
            return
        randIndex = random.randint(0, len(dominoSet) - 1)
        playerSet.append(dominoSet[randIndex])
        dominoSet.remove(dominoSet[randIndex])

#Placing a domino onto the board
def playingDomino(playerSet, dominoBoard):
    dominoPlayed = False
    for playDomino in playerSet:
        if len(dominoBoard) == 0:
            dominoBoard.append(playDomino)
            playerSet.remove(playDomino)
            dominoPlayed = True
            break
        else:
            if dominoBoard[0][0] == playDomino[1]:
                dominoBoard.insert(0, [playDomino[0], playDomino[1]])
                playerSet.remove(playDomino)
                dominoPlayed = True
                break
            elif dominoBoard[0][0] == playDomino[0]:
                dominoBoard.insert(0, [playDomino[1], playDomino[0]])
                playerSet.remove(playDomino)
                dominoPlayed = True
                break
            elif dominoBoard[len(dominoBoard) - 1][1] == playDomino[0]:
                dominoBoard.append([playDomino[0], playDomino[1]])
                playerSet.remove(playDomino)
                dominoPlayed = True
                break
            elif dominoBoard[len(dominoBoard) - 1][1] == playDomino[1]:
                dominoBoard.append([playDomino[1], playDomino[0]])
                playerSet.remove(playDomino)
                dominoPlayed = True
                break
    return dominoPlayed

#Control Strategy (loops through and plays first available domino)
def dumbStrat(playerSet, dominoSet, dominoBoard):
    dominoPlayed = playingDomino(playerSet, dominoBoard)
    if not dominoPlayed:
        drawDomino(dominoSet, playerSet)
        playingDomino(playerSet, dominoBoard)
    return dominoPlayed

#Strategy for prioritizing high value dominos
def valueStrat(playerSet, dominoSet, dominoBoard):
    
    #Sorting the array
    for i in range(1, len(playerSet)):
        currentDominoValue = playerSet[i][0] + playerSet[i][1]
        j = i - 1
        prevCurrentDominoValue = playerSet[j][0] + playerSet[j][1]
        if (currentDominoValue > prevCurrentDominoValue):
            holderDomino = playerSet[j]
            playerSet[j] = playerSet[i]
            playerSet[i] = holderDomino
        

    dominoPlayed = dumbStrat(playerSet, dominoSet, dominoBoard)
    return dominoPlayed




#Strategy for prioritizing domino pairs
def pairStrat(playerSet, dominoSet, dominoBoard):
    
    #Creating pair set
    pairSet = []
    for domino in playerSet:
        if (domino[0] == domino[1]):
            pairSet.append(domino)
            playerSet.remove(domino)

    #playing a domino from set
    hasPlayed = playingDomino(pairSet, dominoBoard)
    if not hasPlayed:
        hasPlayed = playingDomino(playerSet, dominoBoard)
        if not hasPlayed:
            drawDomino(dominoSet, playerSet)
            playingDomino(playerSet, dominoBoard)
    return hasPlayed


    
#Getting the score of a hand
def countingScore(playerSet):
    score = 0
    for domino in playerSet:
        for number in domino:
            score += number
    return score



def playGame(playerToRecord):
    #Making the set of dominos
    dominoSet = [[0, 0], [0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[2,2],[2,3],[2,4],[2,5],[2,6],[3,3],[3,4],[3,5],[3,6],[4,4],[4,5],[4,6],[5,5],[5,6],[6,6]]

    #Getting the domino set for the first player
    playerOneSet = []
    while len(playerOneSet) < 7:
        drawDomino(dominoSet, playerOneSet)
   
    #Getting the domino set for the second player
    playerTwoSet = []
    while len(playerTwoSet) < 7:
        drawDomino(dominoSet, playerTwoSet)

    #The Game of dominos
    playerOneWin = False
    playerTwoWin = False
    gameEnded = False
    dominoPlayBoard = []
    while (not gameEnded):

        #Player One Turn
        playerOnePlayed = dumbStrat(playerOneSet, dominoSet, dominoPlayBoard)

        #Player Two Turn
        playerTwoPlayed = valueStrat(playerTwoSet, dominoSet, dominoPlayBoard)

        #Checking if there is a stalemate
        if not playerOnePlayed and not playerTwoPlayed:
            if (len(dominoSet) == 0):
                gameEnded = True
                if (countingScore(playerOneSet) > countingScore(playerTwoSet)):
                    playerTwoWin = True
                elif (countingScore(playerOneSet) < countingScore(playerTwoSet)):
                    playerOneWin = True

        
        #Checking for a winner
        if (len(playerOneSet) == 0):
            playerOneWin = True
            break

        if (len(playerTwoSet) == 0):
            playerTwoWin = True
            break

    #Printing out win results
    gameResult = 0
    playerOneScore = 0
    playerTwoScore = 0
    
    #If player one wins
    if playerOneWin:
        playerOneScore = countingScore(playerTwoSet)
        #print("Player one has won with a score of: ")
        #print(playerOneScore)
        gameResult = 1
        

    #if player two wins
    if playerTwoWin:
        playerTwoScore = countingScore(playerOneSet)
        #print("Player two has won with a score of: ")
        #print(playerTwoScore)
        gameResult = -1
    
    #Checking which player score to return (For average score)
    if (playerToRecord == 1):
        return playerOneScore
    elif (playerToRecord == 2):
        return playerTwoScore
    else:
        return 0

def main():
    playerOneWinCount = 0
    playerTwoWinCount = 0
    playerOneAverageScore = 0
    gameResult = 0
    gameResult2 = 0
    
    #Running the game (This specific example is to get the average score)
    for i in range(100):
        gameResult += playGame(1)
    playerOneAverageScore = gameResult / 100
    for i in range(100):
        gameResult2 += playGame(2)
    playerTwoAverageScore = gameResult2 / 100
    
    #Printing to terminal
    resultString = "Player One average score is " + str(playerOneAverageScore) + "\n" + "Player Two average score is: " + str(playerTwoAverageScore)
    print(resultString)
    
    # plot
    plt.bar(1, playerOneAverageScore)
    plt.bar(2, playerTwoAverageScore)

    plt.title("Control average score is " + str(playerOneAverageScore) + "\n" + "Value strategy average score is: " + str(playerTwoAverageScore) + "\n")
    plt.xlabel("Blue: Control strategy\nOrange: Value Strategy")
    plt.ylabel("Score ")
    plt.xticks([])
    plt.tight_layout()
    plt.show()
    
    

if __name__ == "__main__":
    main()