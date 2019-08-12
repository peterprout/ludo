# Team 1
from Team_1_setup import coOrds
from Team_1_constants import *
from Team_1_box_and_button import Box
from Team_1_box_and_button import Button
from Team_1_dice import Dice


class Board:
    """Draws the main Ludo board and the moving pieces.

    It also checks if two pieces are on the same spot. If that is the case,
    then the size of the pieces is changed. It also checks if a piece has
    killed and opponents piece.

    :param my_player: Your player object.
    :type my_player: instance object
    :param all_pieces: All the pieces on the board.
    :type all_pieces: list
    :param colour_to_img: Dictionary that map player colour to images.
    :type colour_to_img: dict

    """

    def __init__(self, my_player, all_pieces, colour_to_img):
        """Takes in genie_owner, my_player, all_pieces, colour_to_img as
            arguments. It also initialises the coordinates list for the home
            positions, the ROLL_BUTTON, PLAYER_FIELD, and the connection to
            the server.
        """
        self.home_coords = []
        self.my_player = my_player
        self.genie_owner = None
        self.dice_object = None
        self.PLAYER_FIELD = Box("", 900, 200, 200, 30, WHITE, 1)
        self.ROLL_BUTTON = None
        self.connection = None
        self.current_player = None
        self.ALL_PIECES = all_pieces
        self.COLOUR_TO_IMG = colour_to_img
        self.c = pygame.time.Clock()

    def add_connection(self, connection):
        """Adds the connection to the board. It creates a new dice object,
            a roll button and the current_player whose turn it is.

        :param connection: connection object, linking this to board.
        :type connection: instance object
        """
        self.connection = connection
        self.dice_object = Dice(connection)
        self.ROLL_BUTTON = Button("ROLL", 900, 430, 200, 30, GREEN, 0,
                                  BRIGHTGREEN, self.dice_object.roll_dice)
        self.current_player = connection.current_player

    def move_piece(self, piece_num, step):
        """This moves the piece assuming the piece is movable.

        If the piece is in the home position, it can onl be moved if a 6 is
        rolled on the dice. It also draws the pieces as they move each step.
        After the piece has move it checks if there is a conflict with another
        piece on the board.

        :param piece_num: Number in index of ``ALL_PIECE`` of this piece
        :type piece_num: int
        :param step: Number of steps/moves by this piece
        :type step: int
        """
        pygame.mixer.Sound.play(MOVE_PIECE)
        moving_piece = self.ALL_PIECES[piece_num]
        if moving_piece.get_position() is None:
            moving_piece.set_position(moving_piece.start)
        else:
            moving_piece.steps_from_start += step
            while step > 0:
                if moving_piece.get_position() == 50 and piece_num < 4:
                    moving_piece.set_position(-1)
                elif moving_piece.get_position() == 11 and 8 > piece_num > 3:
                    moving_piece.set_position(-11)
                elif moving_piece.get_position() == 24 and 12 > piece_num > 7:
                    moving_piece.set_position(-10)
                elif moving_piece.get_position() == 37 and 16 > piece_num > 11:
                    moving_piece.set_position(-20)
                elif piece_num < 8 and moving_piece.get_position() < 0:
                    moving_piece.set_position(moving_piece.get_position() - 1)
                elif 7 < piece_num < 16 and moving_piece.get_position() < 0:
                    moving_piece.set_position(moving_piece.get_position() + 1)
                else:
                    moving_piece.set_position(
                        (moving_piece.get_position() + 1) % 52)
                step -= 1
                self.draw_pieces(65)
                # Limits update to board
                board_rect = pygame.Rect(0, 0, 800, 800)
                pygame.display.update(board_rect)
                self.c.tick(10)
        self.check_conflict(moving_piece)

    def draw_arrows_and_stars(self):
        """Draws the arrows and stars on the board. It also calls the
            ``draw_boxes`` function. The arrows are drawn using pygame's draw
            function. The arrow images are blit on to the board.
        """
        pygame.draw.polygon(SCREEN, RED, (CENTRE, TOP_LEFT, BOTTOM_LEFT), 0)
        pygame.draw.polygon(SCREEN, GREEN, (CENTRE, TOP_LEFT, TOP_RIGHT), 0)
        pygame.draw.polygon(SCREEN, YELLOW, (CENTRE, TOP_RIGHT, BOTTOM_RIGHT),
                            0)
        pygame.draw.polygon(SCREEN, BLUE, (CENTRE, BOTTOM_LEFT, BOTTOM_RIGHT),
                            0)
        pygame.draw.polygon(SCREEN, BLACK, (CENTRE, TOP_LEFT, BOTTOM_LEFT), 1)
        pygame.draw.polygon(SCREEN, BLACK, (CENTRE, TOP_LEFT, TOP_RIGHT), 1)
        pygame.draw.polygon(SCREEN, BLACK, (CENTRE, TOP_RIGHT, BOTTOM_RIGHT), 1)
        pygame.draw.polygon(SCREEN, BLACK, (CENTRE, BOTTOM_LEFT, BOTTOM_RIGHT),
                            1)

        self.draw_boxes()

        # Print Arrows on SCREEN
        SCREEN.blit(UP_ARROW,
                    (BOX_SIZE * 7 + INDENT_BOARD, BOX_SIZE * 14 + INDENT_BOARD))
        SCREEN.blit(DOWN_ARROW, (BOX_SIZE * 7 + INDENT_BOARD, INDENT_BOARD))
        SCREEN.blit(RIGHT_ARROW, (INDENT_BOARD, BOX_SIZE * 7 + INDENT_BOARD))
        SCREEN.blit(LEFT_ARROW,
                    (BOX_SIZE * 14 + INDENT_BOARD, BOX_SIZE * 7 + INDENT_BOARD))

    def draw_boxes(self):
        """Draws rectangles for each position on the board using the boc_pos
            list. It also blits star images on the board.
        """
        box_pos = [[0, -1, -2, -3, -4, -5], [-11, -12, -13, -14, -15, 13],
                   [-6, -7, -8, -9, -10, 26], [39, -16, -17, -18, -19, -20],
                   [51, 1, 2, 3, 4, 18, 19, 20, 21, 22, 23, 50, 24, 49, 48, 47,
                    46, 45, 44, 30, 29, 28, 27, 26, 25,
                    11, 10, 9, 8, 7, 6, 5, 43, 42, 41, 40, 38, 37, 12, 14, 15,
                    16, 17, 31, 32, 33, 34, 35, 36],
                   [8, 34, 21, 47]]
        for item in box_pos[0]:
            pygame.draw.rect(SCREEN, RED, (
                coOrds[item][0], coOrds[item][1], BOX_SIZE, BOX_SIZE), 0)
            pygame.draw.rect(SCREEN, BLACK, (
                coOrds[item][0], coOrds[item][1], BOX_SIZE, BOX_SIZE), 1)
        for item in box_pos[1]:
            pygame.draw.rect(SCREEN, GREEN, (
                coOrds[item][0], coOrds[item][1], BOX_SIZE, BOX_SIZE), 0)
            pygame.draw.rect(SCREEN, BLACK, (
                coOrds[item][0], coOrds[item][1], BOX_SIZE, BOX_SIZE), 1)
        for item in box_pos[2]:
            pygame.draw.rect(SCREEN, YELLOW, (
                coOrds[item][0], coOrds[item][1], BOX_SIZE, BOX_SIZE), 0)
            pygame.draw.rect(SCREEN, BLACK, (
                coOrds[item][0], coOrds[item][1], BOX_SIZE, BOX_SIZE), 1)
        for item in box_pos[3]:
            pygame.draw.rect(SCREEN, BLUE, (
                coOrds[item][0], coOrds[item][1], BOX_SIZE, BOX_SIZE), 0)
            pygame.draw.rect(SCREEN, BLACK, (
                coOrds[item][0], coOrds[item][1], BOX_SIZE, BOX_SIZE), 1)
        for item in box_pos[4]:
            pygame.draw.rect(SCREEN, BLACK, (
                coOrds[item][0], coOrds[item][1], BOX_SIZE, BOX_SIZE), 1)
        for item in box_pos[5]:
            SCREEN.blit(STAR, (coOrds[item][0], coOrds[item][1]))

    def draw_genie(self):
        """Draws the genie on the board depending on who has the genie.
            If no-one has the genie, a lamp is placed in the middle.
        """
        if self.genie_owner == "red":
            SCREEN.blit(GENIE_SMALL, (
                self.home_coords[0][0] + 57, self.home_coords[0][1] + 89))
        elif self.genie_owner == "green":
            SCREEN.blit(GENIE_SMALL, (
                self.home_coords[4][0] + 57, self.home_coords[4][1] + 89))
        elif self.genie_owner == "yellow":
            SCREEN.blit(GENIE_SMALL, (
                self.home_coords[8][0] + 57, self.home_coords[8][1] + 89))
        elif self.genie_owner == "blue":
            SCREEN.blit(GENIE_SMALL, (
                self.home_coords[12][0] + 57, self.home_coords[12][1] + 89))
        else:
            SCREEN.blit(LAMP_SMALL, (CENTRE[0] - 37, CENTRE[1] - 37))

    def draw_pieces(self, check=0):
        """Draws the pieces on the board.

        It goes through all the pieces on the board and draw it in their
        position. If there is a conflict their size changes.
        The pieces flash is they are movable depending on the dice roll.

        """
        piece_in = {}
        temp = None
        for num in range(16):
            piece = self.ALL_PIECES[num]
            piece_pos = piece.get_position()
            # If pieces are movable flash orange.
            if piece.colour == self.current_player and piece.movable \
                    and (check < FPS/4 or (FPS/2 < check < 3*FPS/4)):
                temp = piece.image
                if piece.image.get_width() != 64:
                    piece.image = ORANGE_PIECE_32
                else:
                    piece.image = ORANGE_PIECE
            # If piece in home.
            if piece_pos is None:
                SCREEN.blit(piece.image, self.home_coords[num])
            else:
                if piece.image.get_width() != 64:
                    if piece.get_position() not in piece_in:
                        piece_in[piece.get_position()] = 0
                        SCREEN.blit(piece.image, (
                            coOrds[piece_pos][0], coOrds[piece_pos][1]))
                        piece_in[piece.get_position()] += 1
                    elif piece_in[piece.get_position()] == 1:
                        SCREEN.blit(piece.image, (
                            coOrds[piece_pos][0] + 20, coOrds[piece_pos][1]))
                        piece_in[piece.get_position()] += 1
                    else:
                        SCREEN.blit(piece.image, (
                            coOrds[piece_pos][0] + 10,
                            coOrds[piece_pos][1] + 15))
                else:
                    SCREEN.blit(piece.image, (
                        coOrds[piece_pos][0] - 7, coOrds[piece_pos][1] - 25))
            if temp:
                piece.image = temp
                temp = None

    def draw_board(self, check):
        """Draws the main board.

        It calls the draw_arrows_and_stars function. It also draws the rectangle
        and the circles as home bases for the pieces.

        It then draw the pieces, genie, roll button and displays dice.

        :param check: Indicates if the player and their pieces are flashing.
        :type check: int
        """
        self.draw_arrows_and_stars()

        # Drawing home bases and each players pieces
        colours = [RED, GREEN, YELLOW, BLUE]
        home = [(INDENT_BOARD, INDENT_BOARD),
                (BOX_SIZE * 9 + INDENT_BOARD, INDENT_BOARD),
                (BOX_SIZE * 9 + INDENT_BOARD, BOX_SIZE * 9 + INDENT_BOARD),
                (INDENT_BOARD, BOX_SIZE * 9 + INDENT_BOARD)]
        radius = 28  # Radius of the circles
        home_size = BOX_SIZE * 6
        for i in range(4):
            white_box_x = home[i][0] + BOX_SIZE
            white_box_y = home[i][1] + BOX_SIZE
            white_box_size = BOX_SIZE * 4  # Size of the whote box.
            # Check if home base should flash.
            if self.current_player == "red" and colours[
                    i] == RED and check > FPS/2:
                pygame.draw.rect(SCREEN, ORANGE,
                                 (home[i][0], home[i][1], home_size, home_size))
            elif self.current_player == "green" and colours[
                    i] == GREEN and check > FPS/2:
                pygame.draw.rect(SCREEN, LGREEN,
                                 (home[i][0], home[i][1], home_size, home_size))
            elif self.current_player == "yellow" and colours[
                    i] == YELLOW and check > FPS/2:
                pygame.draw.rect(SCREEN, LYELLOW,
                                 (home[i][0], home[i][1], home_size, home_size))
            elif self.current_player == "blue" and colours[
                    i] == BLUE and check > FPS/2:
                pygame.draw.rect(SCREEN, LBLUE,
                                 (home[i][0], home[i][1], home_size, home_size))
            else:
                pygame.draw.rect(SCREEN, colours[i],
                                 (home[i][0], home[i][1], home_size, home_size))
            pygame.draw.rect(SCREEN, BLACK,
                             (home[i][0], home[i][1], home_size, home_size), 1)
            pygame.draw.rect(SCREEN, WHITE, (
                white_box_x, white_box_y, white_box_size, white_box_size))
            pygame.draw.rect(SCREEN, BLACK, (
                white_box_x, white_box_y, white_box_size, white_box_size), 1)

            circle_1x = white_box_x + BOX_SIZE  # X of the left circles.
            circle_1y = white_box_y + BOX_SIZE  # Y of the top circles.
            circle_2x = white_box_x + (BOX_SIZE * 3)  # X of the right circles.
            circle_2y = white_box_y + (BOX_SIZE * 3)  # Y of the bottom circles.

            # Draw the top left circle.
            pygame.draw.circle(SCREEN, colours[i], (circle_1x, circle_1y),
                               radius, 0)
            pygame.draw.circle(SCREEN, BLACK, (circle_1x, circle_1y), radius, 1)

            # Draw the top right circle.
            pygame.draw.circle(SCREEN, colours[i], (circle_2x, circle_1y),
                               radius, 0)
            pygame.draw.circle(SCREEN, BLACK, (circle_2x, circle_1y), radius, 1)

            # Draw the bottom left circle.
            pygame.draw.circle(SCREEN, colours[i], (circle_1x, circle_2y),
                               radius, 0)
            pygame.draw.circle(SCREEN, BLACK, (circle_1x, circle_2y), radius, 1)

            # Draw the bottom right circle.
            pygame.draw.circle(SCREEN, colours[i], (circle_2x, circle_2y),
                               radius, 0)
            pygame.draw.circle(SCREEN, BLACK, (circle_2x, circle_2y), radius, 1)

            # Co-rodinates of the home position.
            if len(self.home_coords) < 15:
                self.home_coords += [(circle_1x - 32, circle_1y - 64),
                                     (circle_2x - 32, circle_1y - 64),
                                     (circle_1x - 32, circle_2y - 64),
                                     (circle_2x - 32, circle_2y - 64)]
        self.draw_genie()
        self.draw_pieces(check)
        self.PLAYER_FIELD.draw()
        self.dice_object.display_dice(900, 230, self.connection.current_dice)
        self.ROLL_BUTTON.draw()

    def check_conflict(self, moving_piece):
        """Checks if two pieces are in the same position.

        Goes through all the pieces on the board and checks if there is
        a conflict. If there is and the opponents piece is not in a safe
        spot then kill the piece by calling the death_function. Also
        call the check_many_pieces to check if there are other pieces
        that are in conflicting positions.

        :param moving_piece: instance of moving piece
        :type moving_piece: instance object
        """
        for piece in self.ALL_PIECES:
            equal_pos = moving_piece.get_position() == piece.get_position()
            not_equal_colour = moving_piece.colour != piece.colour
            safe_start = moving_piece.get_position() == moving_piece.start
            if equal_pos and not_equal_colour and not safe_start:
                # If player of opposing piece, piece that your piece is landing
                # on, has genie your piece is killed instead
                if piece.colour == self.genie_owner:
                    self.death_function(moving_piece)
                    self.check_many_pieces(piece)
                    break
                if not piece.check_safe_point():
                    self.connection.my_player.special_move = True
                    self.death_function(piece)
                    self.check_many_pieces(moving_piece)
                    break
            self.check_many_pieces(piece)

    def check_many_pieces(self, moving_piece):
        """Checks if there is a conflict in position.

        :param moving_piece: instance of moving piece
        :type moving_piece: instance object
        """
        for num in range(16):
            piece = self.ALL_PIECES[num]
            if piece == moving_piece:
                continue
            if moving_piece.get_position() is not None and \
                    moving_piece.get_position() == piece.get_position():
                piece.image = pygame.transform.scale(piece.image, (32, 32))
                moving_piece.image = pygame.transform.scale(moving_piece.image,
                                                            (32, 32))
                return
        moving_piece.image = self.COLOUR_TO_IMG[moving_piece.colour]

    def death_function(self, piece):
        """
        Sends the piece back to its starting position.
        It retraces its steps all the way back.

        :param piece: instance of this piece
        :type piece: instance object
        """
        pygame.mixer.Sound.play(KILL_PIECE)
        piece.image = self.COLOUR_TO_IMG[piece.colour]
        while piece.get_position() != piece.start:
            piece.set_position((piece.get_position() - 1) % 52)
            self.draw_pieces()
            pygame.display.update()
            self.c.tick(10)
        piece.set_position(None)
        piece.set_steps_from_start(0)

    def disconnect_function(self, colour):
        """
        Sends the piece back to its starting position.

        :param colour: colour of player of disconnected player
        :type colour: str
        """
        low_range = self.get_low_range(colour)
        for num in range(low_range, low_range + 4):
            piece = self.ALL_PIECES[num]
            piece.image = self.COLOUR_TO_IMG[piece.colour]
            piece.movable = None
            self.draw_pieces()
            piece.set_position(None)
            piece.set_steps_from_start(0)

    def get_low_range(self, colour):
        """
        Return low range of player that has disconnected.

        :param colour: Colour of this player.
        :type colour: str
        :return: int representing low range of particular colour
        """
        if colour == "red":
            return 0
        elif colour == "green":
            return 4
        elif colour == "yellow":
            return 8
        elif colour == "blue":
            return 12

    def draw_scoreboard(self, list_of_pieces, x, y, w, h):
        """
        Draws the score board that represent the score of each player. It
        dynamically alter the positions of each player according to their score.

        :param list_of_pieces: A list of all pieces
        :type list_of_pieces: list
        :param x: Left position
        :type x: int
        :param y: Top position
        :type y: int
        :param w: Width
        :type w: int
        :param h: Height
        :type h: int
        :return: A graphical scoreboard
        """
        name = Box("Name", x, y, w, h, BLACK, 1)
        x += w
        score = Box("Score", x, y, w, h, BLACK, 1)
        x += w
        name.draw()
        score.draw()
        # Returns a list of the scores in order: red, green, yellow, blue
        scores = self.get_score(list_of_pieces)
        # If all scores are zero, scoreboard is ordered as default
        color_to_color = {"red": RED, "green": GREEN,
                          "yellow": YELLOW, "blue": BLUE}
        # Used to get the name of the player variable names contains all
        # the names of the
        # players [red, green, yellow, blue]
        colors = ["red", "green", "yellow", "blue"]
        list_of_scores = []
        for i in range(len(self.connection.my_player.names)):
            list_of_scores.append((scores[i], colors[i]))
        if scores != [0, 0, 0, 0]:
            list_of_scores = sorted(list_of_scores)[::-1]
        for i in list_of_scores:
            # Access each player, sort them by score
            # and draw the 4 players on the scoreboard.
            color = color_to_color[i[1]]
            y += h
            x = 900
            name_field = Box(self.connection.my_player.names[colors.index(i[1])], x, y, w, h, color)
            name_field.draw()
            out_line_box = Box("", x, y, w, h, BLACK, 1)
            out_line_box.draw()
            x += w
            score_field = Box(str(i[0]), x, y, w, h, color)
            score_field.draw()
            out_line_box = Box("", x, y, w, h, BLACK, 1)
            out_line_box.draw()
            x += w
            # Draws a marker after your entry to show who you are
            if self.connection.my_player.name == \
                    self.connection.my_player.names[colors.index(i[1])]:
                marker = Box("<", x, y, w, h, WHITE)
                marker.draw()
            else:
                blank = Box("", x, y, w, h, WHITE)
                blank.draw()
        # Returns a list of the scores in order: [red, green, yellow, blue]

    def get_score(self, list_of_pieces):
        """
        Returns a list of the scores in order: ``red, green, yellow, blue``
        """
        red_score = 0
        blue_score = 0
        green_score = 0
        yellow_score = 0
        for piece in list_of_pieces:
            if piece.colour == "red":
                red_score += piece.get_steps_from_start()
            elif piece.colour == "blue":
                blue_score += piece.get_steps_from_start()
            elif piece.colour == "green":
                green_score += piece.get_steps_from_start()
            elif piece.colour == "yellow":
                yellow_score += piece.get_steps_from_start()
        return [red_score, green_score, yellow_score, blue_score]
