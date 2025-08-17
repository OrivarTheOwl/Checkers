# Checkers game

# Base checkerboard initialization
checkerboard = [
    "    1   2   3   4   5   6   7   8    ",
    "  ┌───┬───┬───┬───┬───┬───┬───┬───┐"  ,
    "A │ ╳ │   │ ╳ │   │ ╳ │   │ ╳ │   │ A",
    "  ├───┼───┼───┼───┼───┼───┼───┼───┤"  ,
    "B │   │ ╳ │   │ ╳ │   │ ╳ │   │ ╳ │ B",
    "  ├───┼───┼───┼───┼───┼───┼───┼───┤"  ,
    "C │ ╳ │   │ ╳ │   │ ╳ │   │ ╳ │   │ C",
    "  ├───┼───┼───┼───┼───┼───┼───┼───┤"  ,
    "D │   │ ╳ │   │ ╳ │   │ ╳ │   │ ╳ │ D",
    "  ├───┼───┼───┼───┼───┼───┼───┼───┤"  ,
    "E │ ╳ │   │ ╳ │   │ ╳ │   │ ╳ │   │ E",
    "  ├───┼───┼───┼───┼───┼───┼───┼───┤"  ,
    "F │   │ ╳ │   │ ╳ │   │ ╳ │   │ ╳ │ F",
    "  ├───┼───┼───┼───┼───┼───┼───┼───┤"  ,
    "G │ ╳ │   │ ╳ │   │ ╳ │   │ ╳ │   │ G",
    "  ├───┼───┼───┼───┼───┼───┼───┼───┤"  ,
    "H │   │ ╳ │   │ ╳ │   │ ╳ │   │ ╳ │ H",
    "  └───┴───┴───┴───┴───┴───┴───┴───┘"  ,
    "    1   2   3   4   5   6   7   8    "
    ]

'''
Unused testing variables

test_increment = 0
test_piece_inputs = ["C8", "F7"]
test_piece_destinations = ["D7", "E8"]
test_limit = len(test_piece_inputs)

Unused testing add-ins to select_piece:
        if test_increment < test_limit:
            selected_piece = test_piece_inputs[test_increment]
        else:
        
Unused testing add-ins to move_piece:
        global test_increment
        if test_increment < test_limit:
            destination = test_piece_destinations[test_increment]
            test_increment += 1
        else:
'''


# Class to deal with white and black pieces
class Piece():
    def __init__(self, color, number):
        self.color = color
        self.position = ""
        self.is_kinged = False
        self.piece_number = number
        

# Main class with game logic and workings
class CheckersGame():
    def __init__(self):
        self.pieces = []
        self.turn = "black"
        self.extra_turn = False
        self.run()

    # Displays the board
    def display_board(self):
        for line in checkerboard:
            print(line)

    # Creates black piece objects
    def create_black_pieces(self):
        for i in range(12):
            piece = Piece("black", i + 1)
            self.pieces.append(piece)

    # Creates white piece objects
    def create_white_pieces(self):
        for i in range(12):
            piece = Piece("white", i + 13)
            self.pieces.append(piece)

    # Returns the value of an index of a given letter/number pair
    def get_position_data(self, tile: str):
        letter = tile[0]
        number = int(tile[1])
        letters = "ABCDEFGH"
        return checkerboard[(letters.index(letter.upper()) * 2) + 2][((number - 1) * 4) + 4]
    
    # Returns a list of all tile locations, A1-H8
    def get_all_tile_locations(self):
        all_tiles = []
        letters = "ABCDEFGH"
        for letter in letters:
            for i in range(8):
                all_tiles.append(letter + str(i + 1))
        return all_tiles
    
    # Sets the pieces into their starting positions
    def set_starting_positions(self):
        black_starting_tiles = ["A2", "A4", "A6", "A8", "B1", "B3", "B5", "B7", "C2", "C4", "C6", "C8"]
        white_starting_tiles = ["F1", "F3", "F5", "F7", "G2", "G4", "G6", "G8", "H1", "H3", "H5", "H7"]
        letters = "ABCDEFGH"

        for tile in black_starting_tiles:
            letter, index = tile[0], int(tile[1])
            row = (letters.index(letter.upper()) * 2) + 2
            column = ((index - 1) * 4) + 4
            checkerboard[row] = checkerboard[row][:column] + "○" + checkerboard[row][column + 1:]

        for tile in white_starting_tiles:
            letter, index = tile[0], int(tile[1])
            row = (letters.index(letter.upper()) * 2) + 2
            column = ((index - 1) * 4) + 4
            checkerboard[row] = checkerboard[row][:column] + "●" + checkerboard[row][column + 1:]

        all_tiles = black_starting_tiles + white_starting_tiles
        for piece, value in zip(self.pieces, all_tiles):
            piece.position = value

    # Returns a piece object if a piece in the given position exists
    def select_piece(self):
        selected_piece = input("Select a piece to move: ").upper()
        if selected_piece == "ff".upper():
            return "ff"
        for piece in self.pieces:
            if piece.position == selected_piece:
                return piece
        print("Not a valid piece")
        return False

    # Moves the selected piece to a selected destination
    def move_piece(self, piece: Piece):
        valid_tiles = []
        all_tiles = self.get_all_tile_locations()
        for tile in all_tiles:
            if self.check_tile_matches_rules(piece, tile):
                valid_tiles.append(tile)
        for tile in valid_tiles:
            if self.get_position_data(tile) == "○" or self.get_position_data(tile) == "●":
                if self.check_jump_destination_empty(piece, tile) == False:
                    valid_tiles.remove(tile)

        if len(valid_tiles) == 0:
            print("No valid destinations")
            return False
        print("Valid destinations:")
        for tile in valid_tiles:
            print(tile)
        destination = input("Select destination: ").upper()

        if destination in valid_tiles:
            # Check if destination has an opponent's piece in it
            if self.get_position_data(destination) != " ":
                if self.jump_over_piece(piece, destination) == False:
                    return False
            else:
                self.empty_tile_replace_row(piece, destination)
        elif destination not in valid_tiles:
            print("Invalid destination")
            return False

    # Creates a list of all destinations that are valid for the given piece
    def check_tile_matches_rules(self, piece: Piece, tile: str):

        # Invalid if the tile has an ╳
        if self.get_position_data(tile) == "╳":
            return False
        # Invalid if tile has a piece of the same color
        if piece.color == "black":
            if self.get_position_data(tile) == "○":
                return False
        if piece.color == "white":
            if self.get_position_data(tile) == "●":
                return False
        # Invalid if the tile is more than 1 move away
        letters = "ABCDEFGH"
        numbers = "12345678"
        if abs(letters.index(piece.position[0]) - letters.index(tile[0])) != 1:
            return False
        if abs(numbers.index(piece.position[1]) - numbers.index(tile[1])) != 1:
            return False
        # Invalid if the tile is in the wrong direction if not kinged
        if piece.is_kinged == False:
            if piece.color == "black":
                if letters.index(piece.position[0]) - letters.index(tile[0]) != -1:
                    return False
            if piece.color == "white":
                if letters.index(piece.position[0]) - letters.index(tile[0]) != 1:
                    return False
        return True

    # Reusable function that "rewrites" a row to update it
    def replace_row(self, replaced: str, replacement: str):
        letters = "ABCDEFGH"
        letter, number = replaced[0], int(replaced[1])
        row = (letters.index(letter.upper()) * 2) + 2
        column = ((number - 1) * 4) + 4
        checkerboard[row] = checkerboard[row][:column] + replacement + checkerboard[row][column + 1:]

    # Rewrites rows if the destination tile is empty
    def empty_tile_replace_row(self, piece: Piece, destination: str):
        self.replace_row(piece.position, " ")
        piece.position = destination
        if piece.color == "white":
            self.replace_row(destination, "●")
        elif piece.color == "black":
            self.replace_row(destination, "○")
        self.should_tile_be_kinged(piece)

    # Rewrites rows if the destination tile is an opponent's piece
    def opponent_piece_replace_row(self, jumping_piece: Piece, target_piece: Piece, jump_destination: str):
        self.empty_tile_replace_row(jumping_piece, jump_destination)
        self.replace_row(target_piece.position, " ")
        for piece in self.pieces:
            if piece.position == target_piece.position:
                self.pieces.remove(piece)
                break

    # Sets the piece's is_kinged attribute to True if it reaches the back of the opponent's side
    def should_tile_be_kinged(self, piece: Piece):
        if piece.color == "black":
            if piece.position[0] == "H":
                piece.is_kinged = True
        elif piece.color == "white":
            if piece.position[0] == "A":
                piece.is_kinged = True

    # Checks to see if an opponent's piece can be jumped over, and if so jumps
    def jump_over_piece(self, jumping_piece: Piece, target_piece: str):
        for piece in self.pieces:
            if piece.position == target_piece:
                target_piece = piece
                break

        letters = "ABCDEFGH"
        numbers = "12345678"
        horizontal_direction = -(numbers.index(jumping_piece.position[1]) - numbers.index(target_piece.position[1]))
        vertical_direction = letters.index(jumping_piece.position[0]) - letters.index(target_piece.position[0])

        jump_destination_letter = letters[letters.index(target_piece.position[0]) - vertical_direction]
        jump_destination_number = numbers[numbers.index(target_piece.position[1]) + horizontal_direction]
        jump_destination = jump_destination_letter + jump_destination_number

        if (target_piece.position[0] == "A" or target_piece.position[0] == "H"
            or target_piece.position[1] == "1" or target_piece.position[1] == "8"
            ):
            print("Cannot jump over an edge piece")
            return False

        if self.get_position_data(jump_destination) == " ":
            self.opponent_piece_replace_row(jumping_piece, target_piece, jump_destination)
            self.extra_turn = True
        else:
            print("Jump destination not empty")
            return False
        
    # Checks if the jump destination is empty
    def check_jump_destination_empty(self, jumping_piece, target_piece):
        for piece in self.pieces:
            if piece.position == target_piece:
                target_piece = piece
                break

        letters = "ABCDEFGH"
        numbers = "12345678"
        horizontal_direction = -(numbers.index(jumping_piece.position[1]) - numbers.index(target_piece.position[1]))
        vertical_direction = letters.index(jumping_piece.position[0]) - letters.index(target_piece.position[0])
        try:
            jump_destination_letter = letters[letters.index(target_piece.position[0]) - vertical_direction]
            jump_destination_number = numbers[numbers.index(target_piece.position[1]) + horizontal_direction]
            jump_destination = jump_destination_letter + jump_destination_number
        except IndexError:
            return False

        if (target_piece.position[0] == "A" or target_piece.position[0] == "H"
            or target_piece.position[1] == "1" or target_piece.position[1] == "8"
            ):
            return False
        if self.get_position_data(jump_destination) != " ":
            return False

    # Checks to see if the game has been won
    def is_game_won(self):
        black_pieces = []
        white_pieces = []
        for piece in self.pieces:
            if piece.color == "black":
                black_pieces.append(piece)
            elif piece.color == "white":
                white_pieces.append(piece)
        if len(black_pieces) == 0:
            return "white"
        elif len(white_pieces) == 0:
            return "black"
        else:
            return False

    # Run the game
    def run(self):
        self.create_black_pieces()
        self.create_white_pieces()
        self.set_starting_positions()
        self.display_board()
        print("\nIf you believe no valid moves are available,")
        print('you may always forfeit your turn by typing "ff"')

        while True:
            self.extra_turn = False
            print(f"\n{self.turn.capitalize()}'s turn")
            piece = self.select_piece()
            if piece == False:
                continue
            
            if piece != "ff":
                if piece.color != self.turn:
                    print("Not one of your pieces")
                    continue
                if self.move_piece(piece) == False:
                    continue
                print()
                self.display_board()
            if self.extra_turn == False:
                if self.turn == "black":
                    self.turn = "white"
                elif self.turn == "white":
                    self.turn = "black"
            victor = self.is_game_won()
            if victor != False:
                print(f"\n{victor.capitalize()} wins!")
                break


CheckersGame()