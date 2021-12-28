import random

def displayTitle(titleFilePath):
    """
    This Will Print The Hangman Title From An External File Given Through The Parameter titleFilePath Line-By-Line Using The .strip() Function.
    """
    try:
        File = open(titleFilePath)
        for Line in File:
            print(Line.rstrip())
        File.close()

    except FileNotFoundError:
        print(f"File {titleFilePath} Not Found... Exiting Program.")
        exit()

    except IOError:
        print("An Error Occurred While Trying To Access The File... Exiting Program.")
        exit()

def loadHangmanDrawings(hangmanDrawingsFilePath):
    """
    This Will Load All Drawings of Hangman Into A List To Be Used Individually Depending On What Stage Of The Game The Player Is On.
    The Function Opens The File Stated In The Parameter titleFilePath And Splits Each Section Ending With Two New Lines Into Items In A List Called HangingMan.
    """
    try:
        File = open(hangmanDrawingsFilePath)
        HangingMan = File.read().split("\n\n")
        File.close()
        return HangingMan

    except FileNotFoundError:
        print(
            f"File {hangmanDrawingsFilePath} Not Found... Exiting Application.")
        exit()

    except IOError:
        print("An Error Occurred While Trying To Access The File... Exiting Program.")
        exit()

def generateRandomWord(wordsFilePath):
    """
    This Will Generate a Random Word From An External File, Who's Name Is Given By The FileWithWords Paramiter, Which Contains 
    A List Of Words And Set It As The Word For The Current Game By Returning The Word As The Variable GameWord.
    """
    try:
        File = open(wordsFilePath)
        Words = File.read().split("\n")
        File.close()
        GameWord = random.choice(Words)
        return GameWord

    except FileNotFoundError:
        backupWords = ["abruptly", "buffalo", "cricket", "duplex", "fashion", "galaxy"]
        print(f"File {wordsFilePath} Not Found... Using Backup Words")
        GameWord = backupWords[random.randint(1, len(backupWords))]
        return GameWord

    except IOError:
        print("An error occurred while trying to access the file")
        exit()

def wordToUnderscore(randomWord):
    """
    Creates A List Which Contains An Underscore For The Length Of The Random Word Paramiter, Which Will Be Given Later On
    By The Game Word.
    """
    global CurrentState
    CurrentState = ['_' for Letter in randomWord]

def playAgain():
    global GameWord
    global Playing
    global IncorrectGuesses

    # Splits The User's Input To Only The First Character, On The Off Chance They Reply With "Yes" or "No".
    while True:
        
        Again = input("Would You Like To Play Agin? (Y/N)")[0].upper()
        
        if Again == "Y":
            global Lives
            Playing = "Yes"
            GameWord = generateRandomWord("ListOfWords.txt")
            Lives = 7
            IncorrectGuesses = set()
            displayTitle("hangmanword.txt")
            wordToUnderscore(GameWord)
            break
        
        if Again == "N":
            exit()

Playing = "Yes"
Lives = 7
IncorrectGuesses = set()
Win = False
GameWord = generateRandomWord("ListOfWords.txt")
HangingMan = loadHangmanDrawings("Man.txt")

displayTitle("hangmanword.txt")
wordToUnderscore(GameWord)

while True:

    while Playing == "Yes" and Lives > 0:

        # Print First Hanging Man.
        print(HangingMan[7-Lives], "\n")

        # Print Current Sate Of Guessed Word.
        for Item in CurrentState:
            print(Item, end=" ")

        print("")
        print(IncorrectGuesses or "{}") # If The Incorrect Guesses List Is Empty Print "{}".
        print("")

        # Asks The User For A Letter, While Also Removing Any Spaces Between The Characters.
        Input = input("Enter One Or Multiple Guesses: ").lower().replace(" ", "")

        # Check If Each Letter In The Guess Is In The Game Word.
        if Input.isalpha():
            for GuessedCharacter in Input:
                
                # If The Guess Is In IncorrectGuesses Or Has Already Been Guessed & Is Correct, We Skip It.
                if GuessedCharacter in CurrentState or GuessedCharacter in IncorrectGuesses:
                    continue

                # If Any Input Is In The Game Word, A List Is Created Which Will Contain The Respective Posion Of The Guessed Letter Inside Of The Game Word.
                # Example: 
                # GameWord: "Cheese"
                #   UserInput: "e"
                #   CharacterPositions = [2, 3, 5]
                else:
                    if GuessedCharacter in GameWord:
                        CharacterPositions = []

                        # For Each Character In "Gameword", We Check If The Guessed Character Is Equal To The Current Character.
                        # If So, We Add That Character's Index To The Character Positions List.
                        for Index, WordCharacter in enumerate(GameWord):
                            if GuessedCharacter.lower() == WordCharacter.lower():
                                CharacterPositions.append(Index)

                        # For The Number Of Equal Indexes Found, The Respective Index Is Replaced With The Correct Letter.
                        for Index in CharacterPositions:
                            CurrentState[Index] = GameWord[Index]
                    else:
                        Lives -= 1
                        IncorrectGuesses.add(GuessedCharacter)
        else:
            print("\n Please Only Use Letters. \n")

        # Turns The Current Sate Into A String With No Gaps And Compares It To The Correct Word.
        if "".join(CurrentState) == GameWord:
            Win = True
            break
        else:
            Win = False
        
    # Winning / Losing Message.
    if Win:

        # Print Current Sate Of Guessed Word. (Compleated)
        print(HangingMan[7-Lives], "\n")
        print(f"You Win, The Word Was {GameWord.title()}!")
    
    else:

        print(HangingMan[7], "\n")
        print(f"You Lost 😔, The Word Was {GameWord.title()}")
    
    playAgain()