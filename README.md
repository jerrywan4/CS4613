# Mini Camelot Game

### Author
Jerry Wan

Artificial Intelligence
Professor Edward Wong

## Game Instructions:
1.	Unzip the .zip file to an easily accessible location
2.	Open terminal or command prompt
3.	Navigate to the directory where the .zip file was unzipped 
4.	Run the .py file (usually `python3 camelot.py`)

## Code design
This code simulates a mini camelot game in the user’s terminal. The code creates a board with different values representing the different states of each location on the board. 
“EMPTY” represents spaces on the board that are invalid locations/out of range of the game
“O” represents spaces on the board that game pieces can move to
“White” represents the white player (human) game pieces
“Black” represents the black player (AI) game pieces
“GOAL” represents the castles

The code first asks the player to choose if he or she would like to go first
Then the code asks the player to choose a game difficulty 1, 2, or 3
The code generates moves separately for the player and the AI
The way that the code generates moves is it checks whether or not there is a capturing move to be made, if there is, it is the only move that the player or AI can make
Then if there is not a capturing move, it looks for moves (cantering moves or regular moves) and adds them to a list of moves that each piece can make
The AI selects a move based on the return value (a move) from the alpha beta search function
The difficulty of the game changes the initial depth level of the alpha beta search function (1, 2, or 3)
The evaluation function used in this code is:
1000(0.2(number of player pieces – number of AI pieces)/5) + (0.4(-1/minimum distance to black castle)) + (0.4(1/minimum distance to white castle))
This returns a number between -1000 to 1000. This looks at both strategies of winning by capturing all enemy pieces or winning by reaching the goal. The weight in this evaluation function heavily favors reaching the castle because it generally takes less total effort over time to reach the castle rather than spend the time to take every enemy piece (I discovered this through playing the game over and over again).
