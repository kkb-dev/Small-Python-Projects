

hangedman = {
    0:"""_________
  |     |
        |
        |
        |
________|___
""",
    1:"""_________
  |     |
  o     |
        |
        |
________|___""",
    2:"""_________
  |     |
  o     |
 /|\    |
        |
________|___""",
    3:"""_________
  |     |
  o     |
 /|\    |
 / \    |
________|___
""",


    }

# Objective
phrase = "I Don't Believe It! Destination Host Unreachable..."
# Take the phrase and split into individual characters
def splitter():
    word_bank = [char for char in phrase]
    return word_bank
wordbank = splitter()


# Characters that will auto appear
default_wordbank = [" ","+",".",",",";",":","'",'"']
# This list stores correct guesses and shows the guesses in the gameboard
correct_wordbank = []
# This stores incorrect guesses
used_wordbank = []


while True:
    try:
        # Print hangedman
        print(hangedman[len(used_wordbank)])
        # Print already used words
        print("Used words: "+str(used_wordbank+correct_wordbank))
        
        # This shows the output of the game
        gameboard = ""
        # For every word in the wordbank check to see if it has been guessed
        for word in wordbank:
            # Check in the correct wordbank to see if it has been guessed
            if word.lower() in (correct_wordbank+default_wordbank):
                gameboard += word
            # If the word is not in the correct wordbank, do not show
            else:
                gameboard += "*"

        if "*" not in gameboard:
            print("You win!")
            break
        
        print(gameboard)
        
        # Lose Condition
        if len(used_wordbank) > 2:
            print("You Lose")
            print("Correct Phrase: " + phrase)
            break


        guess = str(input("Enter character:"))
        if len(guess) != 1:
            raise Exception("Enter one valid character only")
        
        if guess.lower() in wordbank or guess.upper() in wordbank:
            correct_wordbank.append(guess.lower())
        else:
            used_wordbank.append(guess.lower())

        print("\n\n\n\n\n\n\n\n\n--------------------------------")
    except Exception as e:
        print(e)
