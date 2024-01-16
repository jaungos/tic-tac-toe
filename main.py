# Jerico Luis A. Ungos
# 2021-68060
# CMSC 170 X-1L

# Import the needed libraries
import numpy as np
import tkinter as tk
from tkinter import messagebox as mb, font as tfont

class GameStates:
    def __init__(self, ai_player):
        self.min_max_algo = MinMaxAlgorithm()

        self.board = ['' for _ in range(9)]
        self.ai_player = ai_player # Specifies whether the AI is player 1 or player 2
        self.user_player = 'X' if self.ai_player == 'O' else 'O' # Specifies whether the user is player 1 or player 2

    # Function that would generate the first move of the AI if the AI is player 1
    def generateFirstMove(self):
        return np.random.randint(0, 9) # Generates a random number from 0 to 8

    # Function that would add the AI's move to the game board
    def addAIMove(self, pressed_button_number):
        # Create a new game state by copying the current game state
        new_game_state = GameStates(self.ai_player)
        new_game_state.board = self.board.copy()

        # Place the AI's symbol in the empty cell
        new_game_state.board[pressed_button_number] = self.ai_player

        return new_game_state

    # Function that would add the user's move to the game board
    def addUserMove(self, pressed_button_number):
        # Create a new game state by copying the current game state
        new_game_state = GameStates(self.ai_player)
        new_game_state.board = self.board.copy()

        # Place the user's symbol in the empty cell
        new_game_state.board[pressed_button_number] = self.user_player

        return new_game_state

    # Function that would check if there is a winner in the game
    def isThereAWinner(self):
        rows = [self.board[row_number * 3: (row_number + 1) * 3] for row_number in range(3)] # Get all the rows in the game board
        columns = [self.board[column_number::3] for column_number in range(3)] # Get all the columns in the game board
        diagonals = [self.board[0::4], self.board[2:7:2]] # Get all the diagonals in the game board

        # Check if there is a winner in the rows, columns, or diagonals
        # Reference: https://www.geeksforgeeks.org/python-ways-to-concatenate-two-lists/
        all_possible_winning_combinations = rows + columns + diagonals

        for combination in all_possible_winning_combinations:
            # Check if the combination is a winning combination by checking if all the elements in a combination are the same and not empty
            if combination.count('X') == 3 or combination.count('O') == 3: return True
        return False

    # Function that would check which player won the game
    def whoWonTheGame(self):
        rows = [self.board[row_number * 3: (row_number + 1) * 3] for row_number in range(3)] # Get all the rows in the game board
        columns = [self.board[column_number::3] for column_number in range(3)] # Get all the columns in the game board
        diagonals = [self.board[0::4], self.board[2:7:2]] # Get all the diagonals in the game board

        # Check if there is a winner in the rows, columns, or diagonals
        # Reference: https://www.geeksforgeeks.org/python-ways-to-concatenate-two-lists/
        all_possible_winning_combinations = rows + columns + diagonals
        
        for winning_combination in all_possible_winning_combinations:
            # Check if the combination is a winning combination by checking if all the elements in a combination are the same and not empty
            if all(element == 'X' for element in winning_combination): return 'X'
            elif all(element == 'O' for element in winning_combination): return 'O'

    # Function that would check if the board is full
    def isBoardFull(self):
        # Check if the board is full by checking if there are no empty cells in the board
        return all(element != '' for element in self.board)

    # Function that would check if the game is over
    def isGameOver(self):
        # Check if the game is over by checking if there is a winner or if the game is a draw
        return self.isThereAWinner() or self.isBoardFull()
    
    # Function that would get all the possible successors of the current game state for the max function
    def getSuccessors(self):
        # Get all the empty cells in the board
        possible_actions = [cell_number for cell_number, cell in enumerate(self.board) if cell == '']

        # Get all the successors of the current game state by placing the AI's symbol in the empty cells
        successors = []
        for action in possible_actions:
            # Create a new game state by copying the current game state
            new_game_state = GameStates(self.user_player)
            new_game_state.board = self.board.copy()

            # Place the AI's name in the empty cell
            new_game_state.board[action] = self.ai_player

            # Append the new game state to the list of successors
            successors.append([action, new_game_state])

        return successors
    
    # Function that would get the utility value of the current game state
    def getUtilityValue(self, current_player):
        # Check if there is a winner in the game
        if self.isThereAWinner(): return 1 if self.whoWonTheGame() == current_player else -1
        else: return 0 # Otherwise, it was only a draw

class MinMaxAlgorithm:
    # Initialize the class
    def __init__(self):
        self.isUserFirstMove = False
        self.player1 = ''
        self.player2 = ''

    # Function that would prompt the user whether they want to go first or not
    def askUserIfTheyWantToGoFirst(self, user_input):
        # Store the user's input into the respective variable
        self.isUserFirstMove = user_input
        self.player1 = 'User' if self.isUserFirstMove else 'Computer'
        self.player2 = 'Computer' if self.isUserFirstMove else 'User'

    # Function that would maximize the utility value of the current game state
    def getMax(self, game_state, alpha_value, beta_value):
        # Check if the current game state is already a terminal state
        if game_state.isGameOver():
            return None, game_state.getUtilityValue('X' if self.player1 == 'Computer' else 'O')
        
        # Initialize the maximum value to a very small number and the action to None
        max_value = -np.inf
        action_to_take = None

        # Get all the possible successors of the current game state
        successors = game_state.getSuccessors()
        for action, successor in successors:
            v = self.getMin(successor, alpha_value, beta_value)

            # Get the maximum value of the current game state
            if v > max_value: 
                max_value = v
                action_to_take = action
            
            # Prune the tree if the maximum value is greater than the beta value
            if v >= beta_value: return action_to_take, max_value

            # Update the alpha value
            alpha_value = max(alpha_value, max_value)

        return action_to_take, max_value
    
    # Function that would minimize the utility value of the current game state
    def getMin(self, game_state, alpha_value, beta_value):
        # Check if the current game state is already a terminal state
        if game_state.isGameOver():
            utility = game_state.getUtilityValue('X' if self.player1 == 'User' else 'O')
            return -utility
            
        # Initialize the minimum value to a very large number and the action to None
        min_value = np.inf

        # Get all the possible successors of the current game state
        successors = game_state.getSuccessors()
        for _, successor in successors:
            _, v = self.getMax(successor, alpha_value, beta_value)

            # Get the minimum value of the current game state
            if v < min_value: min_value = v
            
            # Prune the tree if the minimum value is less than the alpha value
            if v <= alpha_value: return min_value

            # Update the beta value
            beta_value = min(beta_value, min_value)

        return min_value

    # Function that would do the min-max algorithm with alpha-beta pruning
    def evaluate(self, game_state):
        # Start the recursive min-max algorithm with alpha-beta pruning
        action_to_take, _ = self.getMax(game_state, -np.inf, np.inf)

        return action_to_take # Return the best action to take based on the current game state

class GameBoard():
    def __init__(self):
        self.min_max_algorithm = MinMaxAlgorithm()
        self.current_player = ''

    # Function that would make the AI's first move if the AI is player 1
    def makeAIsFirstMove(self):
        # Generate the AI's first move
        ai_first_move = self.game_states.generateFirstMove()
        
        # Update the game board by changing the value of the pressed button with the symbol of the AI
        self.game_states = self.game_states.addAIMove(ai_first_move)
        
        # Place the current player's symbol in the pressed button
        self.buttons[ai_first_move]['text'] = 'X'
        self.buttons[ai_first_move]['disabledforeground'] = '#FF1A0E'

        # Disable the pressed button
        self.buttons[ai_first_move]['state'] = 'disabled'
        
        # Change the current player to the other player
        self.current_player = self.min_max_algorithm.player2

    # Function that would make the AI's move
    def doBestAIMove(self):
        # Get the best move for the AI
        best_move = self.min_max_algorithm.evaluate(self.game_states)
        
        # Update the game board by changing the value of the pressed button with the symbol of the AI
        self.game_states = self.game_states.addAIMove(best_move)

        # Place the current player's symbol in the pressed button
        self.buttons[best_move]['text'] = 'X' if self.current_player == self.min_max_algorithm.player1 else 'O'
        self.buttons[best_move]['disabledforeground'] = '#FF1A0E' if self.current_player == self.min_max_algorithm.player1 else '#0192D2'

        # Disable the pressed button
        self.buttons[best_move]['state'] = 'disabled'
        
        # Check if the game is over
        if self.game_states.isGameOver():
            self.displayResult() # Display the result of the game
            self.restartGame() # Restart the game
        else:
            # Change the current player to the other player
            self.current_player = self.min_max_algorithm.player2 if self.current_player == self.min_max_algorithm.player1 else self.min_max_algorithm.player1

    # Function that would display the result of the game
    def displayResult(self):
        # Check if the game is a draw
        if self.game_states.isBoardFull():
            # Display a message box saying that the game is a draw
            mb.showinfo(title = 'Game Over', message = 'The game is a draw!')
        # Otherwise, check which player won the game
        else:
            # Display a message box saying which player won the game
            mb.showinfo(title = 'Game Over', message = f'{self.current_player} won the game!')

    # Function that would handle when a button is clicked
    def buttonClick(self, pressed_button_number):
        # Check if the pressed button is still available
        if self.game_states.board[pressed_button_number] == '': 
            # Update the game board by changing the value of the pressed button with the symbol of the User
            self.game_states = self.game_states.addUserMove(pressed_button_number)
            
            # Place the current player's symbol in the pressed button
            self.buttons[pressed_button_number]['text'] = 'X' if self.current_player == self.min_max_algorithm.player1 else 'O'
            self.buttons[pressed_button_number]['disabledforeground'] = '#FF1A0E' if self.current_player == self.min_max_algorithm.player1 else '#0192D2'

            # Disable the pressed button
            self.buttons[pressed_button_number]['state'] = 'disabled'
            
            # Check if the game is over
            if self.game_states.isGameOver():
                self.displayResult() # Display the result of the game
                self.restartGame() # Restart the game
            else:
                # Change the current player to the other player
                self.current_player = self.min_max_algorithm.player2 if self.current_player == self.min_max_algorithm.player1 else self.min_max_algorithm.player1

                self.doBestAIMove() # Make the AI's move
                
    # Function that would reset the state of the game board
    def restartGame(self):
        # Reinitialize the cells in the game board
        self.game_states.board = ['' for _ in range(9)]
        for button in self.buttons:
            button['state'] = 'normal'
            button['text'] = ''
        
        # Reset the current player label to the player 1
        self.current_player = self.min_max_algorithm.player1

        # Make the AI's first move if the AI is player 1
        if self.current_player == 'Computer':
            self.makeAIsFirstMove()

    # Function that would initialize the game board
    def initializeGameBoard(self):
        # Create the window
        self.main_window = tk.Tk()
        self.main_window.title("Tic-Tac-Toe")
        self.main_window.geometry("700x700")
        self.main_window.resizable(width = False, height = False)

        # Create the frame
        self.frame = tk.Frame(self.main_window)
        self.frame.pack()

        # Create a popup window asking if the user wants to go first or second
        # Reference: https://www.pythontutorial.net/tkinter/tkinter-askyesno/
        response = mb.askyesno(title = 'Player Order', message = 'Do you want to go first?')
        self.min_max_algorithm.askUserIfTheyWantToGoFirst(response)

        self.game_states = GameStates('O' if self.min_max_algorithm.isUserFirstMove else 'X')
        
        self.current_player = self.min_max_algorithm.player1

        # Create the game board
        self.game_board = tk.Canvas(self.frame, width = 700, height = 80)
        self.game_board.pack()

        # Create the labels in the game board
        self.player1_label = tk.Label(self.frame, text = "Player 1: ", fg = "#FF1A0E", font = tfont.Font(family = "Georgia", size = 18))
        self.player1_label.place(x = 0, y = 0)
        self.player1_name = tk.Label(self.frame, text = self.min_max_algorithm.player1, fg = "#FF1A0E", font = tfont.Font(family = "Courier", size = 18))
        self.player1_name.place(x = 100, y = 3)

        self.player2_label = tk.Label(self.frame, text = "Player 2: ", fg = "#0192D2", font = tfont.Font(family = "Georgia", size = 18))
        self.player2_label.place(x = 0, y = 40)
        self.player2_name = tk.Label(self.frame, text = self.min_max_algorithm.player2, fg = "#0192D2", font = tfont.Font(family = "Courier", size = 18))
        self.player2_name.place(x = 100, y = 43)

        # Create a frame for the buttons
        self.button_frame = tk.Frame(self.main_window)
        self.button_frame.pack(fill = tk.BOTH, expand = 1)

        # Set the minimum size of the rows and columns of the game board
        # Reference: https://stackoverflow.com/questions/45847313/tkinter-grid-columnconfigure-doesnt-work
        for arrangement in range(3):
            self.button_frame.grid_rowconfigure(arrangement, weight = 1)
            self.button_frame.grid_columnconfigure(arrangement, weight = 1)

        # Create the game board's grid
        self.buttons = [tk.Button(self.button_frame, text = '', font = tfont.Font(family = "Comic Sans MS", size = 20), command = lambda current_button_number = button_number: self.buttonClick(current_button_number)) for button_number in range(9)]
        for button_number, button in enumerate(self.buttons):
            button.grid(row = button_number // 3, column = button_number % 3, sticky = 'nsew')

        # Make the AI's first move if the AI is player 1
        if self.current_player == 'Computer':
            self.makeAIsFirstMove()

    # Function that would start the tic-tac-toe game
    def startTicTacToeGame(self):
        self.initializeGameBoard() # Initialize the game board

        # Infinite loop that would run the application
        # It can be terminated by mouse or keyboard interrupt
        self.main_window.mainloop()

tic_tac_toe = GameBoard() # Initialize the game board
tic_tac_toe.startTicTacToeGame() # Display the game board and start the game