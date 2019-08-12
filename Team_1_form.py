# Team 1
from tkinter import *
import json


class Form:
    """
     This class is used to produce all the tkinter screens that will be used by
     the client to enter, exit the lobby, game and show the end screen.

     :param rules_file:
     :type rules_file: str
     :param connection: object connecting this class to the connection.
     :type connection: instance object
     """

    def __init__(self, rules_file, connection):
        self.connection = connection
        self.root = Tk()
        self.root.geometry('+%d+%d' % (100, 100))
        self.filename = rules_file
        self.current_page = None
        self.game_id = None
        self.name = None
        self.player_number = None

    def home_page(self):
        """
        This function produces the home page window that provide options to
        the player, concerning what type of game and if they wish to join a
        lobby
        """
        # Same setup for each new page
        self.root.destroy()
        self.root = Tk()
        self.root.geometry('+%d+%d' % (100, 100))
        self.root.title("Ludo")
        self.current_page = "home_page"
        frame = Frame(self.root)

        ludo_label = Label(frame, text="Ludo", fg="black")
        blank = Label(frame, text="", fg="black")

        # This is the part that varies between pages
        create_game = Button(
            frame, width=30, text="Create Game", command=self.create_game)
        join_public = Button(
            frame, width=30, text="Join Public Game", command=self.join_public)
        join_private = Button(
            frame, width=30, text="Join Private Game", command=self.join_private)
        rules = Button(frame, width=30, text="Rules", command=self.show_rules)

        # Drawing each widget on to the frame
        self.root.minsize(width=220, height=210)
        self.root.maxsize(width=220, height=210)
        self.root.configure(background="white")

        frame.pack()
        frame.configure(background="white")

        ludo_label.grid(row=1, column=1, columnspan=2)
        ludo_label.configure(font=("Arial", 32), background="white")

        blank.grid(row=2, column=3)
        blank.configure(background="white")

        create_game.grid(row=3, column=1, columnspan=2)
        create_game.configure(background="lightgreen")

        join_public.grid(row=4, column=1, columnspan=2)
        join_public.configure(background="lightblue")

        join_private.grid(row=5, column=1, columnspan=2)
        join_private.configure(background="lightgreen")

        rules.grid(row=6, column=1, columnspan=2)
        rules.configure(background="lightblue")

        self.root.mainloop()

    def create_game(self):
        """
        Shows tk window allowing player to create a new game after the player
        clicks the create game button.
        """
        # Same setup for each new page
        self.root.destroy()
        self.root = Tk()
        self.root.title("Ludo")
        self.current_page = "create_game"
        frame = Frame(self.root)

        ludo_label = Label(frame, text="Ludo", fg="black")
        blank = Label(frame, text="", fg="black")
        back = Button(frame, text="Back", command=self.back)

        # This is the part that varies between pages
        label = Label(frame, width=30, text="Create New Game", fg="black")
        room_label = Label(frame, text="Room Code:", fg="black")
        room_entry = Entry(frame, width=20)
        leave_blank = Label(
            frame, width=30, text="Leave blank for Public Game")
        create = Button(frame, width=30, text="Create",
                        command=lambda: self.check_room_code("create", room_entry.get()))

        # Drawing each widget on to the frame
        self.root.minsize(width=220, height=210)
        self.root.maxsize(width=220, height=210)
        self.root.configure(background="white")

        frame.pack()
        frame.configure(background="white")

        ludo_label.grid(row=1, column=1, columnspan=2)
        ludo_label.configure(font=("Arial", 32), background="white")

        blank.grid(row=2, column=3)

        label.grid(row=3, column=1, columnspan=2)
        label.configure(background="white")

        room_label.grid(row=4, column=1)
        room_label.configure(background="white")

        room_entry.grid(row=4, column=2)
        room_entry.configure(background="white")

        leave_blank.grid(row=5, column=1, columnspan=2)
        leave_blank.configure(background="white")

        create.grid(row=6, column=1, columnspan=2)
        create.configure(background="lightgreen")

        back.grid(row=7, column=1)
        back.configure(background="red")
        self.root.mainloop()

    def on_click(self, event):
        """
        Selects the widget after it is clicked

        :param event: An event object gained by clicking on a public game
        :type event: event object
        """
        widget = event.widget
        selection = widget.curselection()
        string = widget.get(selection)
        self.game_id = string.split(" ")[1]
        self.player_number = string.split(" ")[3]

    def check_conflict(self, name, game_id):
        """
        Checks for a conflict.

        :param name: name of player
        :type name: str
        :param game_id: identification for this game
        :type game_id: int
        """
        self.connection.send_check_if_game_is_started(int(game_id))
        # decodes received data.
        data = self.connection.sock.recv(4096).decode()
        msg = json.loads(data)
        if "result" in msg and msg["result"]:
            self.public_room_is_full()
        else:
            self.start_game(name, int(game_id))

    def check_selected(self):
        """
        Checks which type of game was selected by the client.
        """
        if self.player_number is not None:
            if int(self.player_number) == 4:
                self.public_room_is_full()
            else:
                self.connection.send_join_lobby_message(self.game_id)
                self.lobby("public", "", int(self.player_number)+1, self.game_id)

    def public_room_is_full(self):
        """
        Informs the player if the room is full by displaying text.
        """
        self.root.destroy()
        self.root = Tk()
        self.root.geometry('+%d+%d' % (100, 100))
        self.root.title("Ludo")
        self.current_page = "public_room_is_full"
        frame = Frame(self.root)

        ludo_label = Label(frame, text="Ludo", fg="black")
        blank = Label(frame, text="", fg="black")
        back = Button(frame, text="Back", command=self.back)

        # This is the part that varies between pages
        no_room = Label(frame, width=30,
                        text="Current Room is full or deleted", fg="black")
        try_again = Label(
            frame, width=30, text="Please try another room", fg="black")

        # Drawing each widget on to the frame
        self.root.minsize(width=220, height=210)
        self.root.maxsize(width=220, height=210)
        self.root.configure(background="white")

        frame.pack()
        frame.configure(background="white")

        ludo_label.grid(row=1, column=1, columnspan=2)
        ludo_label.configure(font=("Arial", 32), background="white")

        blank.grid(row=2, column=3)
        blank.configure(background="white")

        no_room.grid(row=3, column=1, columnspan=2)
        no_room.configure(background="white")

        try_again.grid(row=4, column=1, columnspan=2)
        try_again.configure(background="white")

        back.grid(row=7, column=1)
        back.configure(background="red")
        self.root.mainloop()

    def join_public(self):
        """Shows public games to  which player can join"""
        # Same setup for each new page
        self.root.destroy()
        self.root = Tk()
        self.root.geometry('+%d+%d' % (100, 100))
        self.root.title("Ludo")
        self.current_page = "join_public"
        frame = Frame(self.root)

        ludo_label = Label(frame, text="Ludo", fg="black")
        blank = Label(frame, text="", fg="black")
        back = Button(frame, text="Back", command=self.back)

        # This is the part that varies between pages
        list_label = Label(frame, width=30, text="List of Games", fg="black")
        list_box = Listbox(frame, width=30)

        # send message to the server
        self.connection.send_join_public_game()

        # receive message from the server
        # decodes received data.
        data = self.connection.sock.recv(4096).decode()
        msg = json.loads(data)
        id_array = msg["game_id"]
        num_array = msg["num"]
        is_public_array = msg["is_public"]
        # Accept public games from server

        # put them in the local connection attribute
        if msg["game_id"]:
            for index in range(len(id_array)):
                if is_public_array[index]:
                    list_box.insert("end", "Game %s --- %s / 4 in lobby" %
                                    (id_array[index], num_array[index]))
        list_box.bind("<<ListboxSelect>>", self.on_click)
        # list_box.pack(side="top", fill="both", expand=True)
        join_game = Button(frame, width=30, text="Join Game",
                           command=lambda: self.check_selected())
        # Drawing each widget on to the frame
        self.root.minsize(width=220, height=345)
        self.root.maxsize(width=220, height=345)
        self.root.configure(background="white")

        frame.pack()
        frame.configure(background="white")

        ludo_label.grid(row=1, column=1, columnspan=2)
        ludo_label.configure(font=("Arial", 32), background="white")

        blank.grid(row=2, column=3)
        blank.configure(background="white")

        list_label.grid(row=3, column=1, columnspan=2)
        list_label.configure(background="white")

        list_box.grid(row=4, column=1, rowspan=3)

        join_game.grid(row=7, column=1, columnspan=2)
        join_game.configure(background="lightblue")

        back.grid(row=8, column=1)
        back.configure(background="red")
        self.root.mainloop()

    def join_private(self):
        """Shows options when client clicks on private game"""
        # Same setup for each new page
        self.root.destroy()
        self.root = Tk()
        self.root.geometry('+%d+%d' % (100, 100))
        self.root.title("Ludo")
        self.current_page = "join_private"
        frame = Frame(self.root)

        ludo_label = Label(frame, text="Ludo", fg="black")
        blank = Label(frame, text="", fg="black")
        back = Button(frame, text="Back", command=self.back)

        # This is the part that varies between pages
        label = Label(frame, width=30, text="Join Private Game", fg="black")
        room_label = Label(frame, text="Enter Room Code:", fg="black")
        room_entry = Entry(frame, width=20)
        join_game = Button(frame, text="Join Game", width=30,
                           command=lambda: self.check_room_code("join", room_entry.get()))

        # Drawing each widget on to the frame
        self.root.minsize(width=220, height=210)
        self.root.maxsize(width=220, height=210)
        self.root.configure(background="white")

        frame.pack()
        frame.configure(background="white")

        ludo_label.grid(row=1, column=1, columnspan=2)
        ludo_label.configure(font=("Arial", 32), background="white")

        blank.grid(row=2, column=3)
        blank.configure(background="white")

        label.grid(row=3, column=1, columnspan=2)
        label.configure(background="white")

        room_label.grid(row=4, column=1)
        room_label.configure(background="white")

        room_entry.grid(row=4, column=2)
        room_entry.configure(background="white")

        join_game.grid(row=5, column=1, columnspan=2)
        join_game.configure(background="lightblue")

        back.grid(row=7, column=1)
        back.configure(background="red")
        self.root.mainloop()

    def update(self, lobby_type, room_code, game_id):
        """
        This is invoked when the update button is pressed, updating the info
        provided to the tk window about the number of players currently in a
        room.

        :param lobby_type: The type of lobby
        :type lobby_type: str
        :param room_code: The identification for this room
        :type room_code: str
        :param game_id: The identification for this game
        :type game_id: int
        """
        # send message to the server
        self.connection.send_join_public_game()

        # receive message from the server
        # decodes received data.
        data = self.connection.sock.recv(4096).decode()
        msg = json.loads(data)
        id_array = msg["game_id"]
        num_array = msg["num"]
        num = num_array[id_array.index(int(game_id))]
        self.lobby(lobby_type, room_code, num, game_id)

    def lobby(self, lobby_type, room_code, player_number, game_id):
        """
        This function is used as the main tk window for each type of lobby.

        :param lobby_type: The type of lobby chosen
        :type lobby_type: str
        :param room_code: Code for the room
        :type room_code: str
        :param player_number: Number of players
        :type player_number: int
        :param game_id: The identification of this game.
        :type game_id: int
        """
        # Same setup for each new page
        self.root.destroy()
        self.root = Tk()
        self.root.geometry('+%d+%d' % (100, 100))
        self.root.title("Ludo")
        frame = Frame(self.root)

        # This is the part that varies between pages
        name_label = Label(frame, text="Player Name:", fg="black")
        name_entry = Entry(frame, width=20)
        if lobby_type == "create":
            self.current_page = "create_lobby"
            if len(room_code) == 0:
                label = Label(frame, width=30,
                              text="New Public Game created", fg="black")
                room_label = Label(frame, width=30, text=("Game " + str(game_id)), fg="black")
            else:
                label = Label(frame, width=30,
                              text="New Private Game created", fg="black")
                room_label = Label(frame, width=30, text=(
                        "Room Code: " + str(room_code)), fg="black")
        elif lobby_type == "public":
            self.current_page = "public_lobby"
            label = Label(frame, width=30, text=("Game " + str(game_id)))
            room_label = Label(frame, width=30, text="", fg="black")
        elif lobby_type == "private":
            self.current_page = "private_lobby"
            label = Label(frame, width=30, text=(
                    "Room Code: " + str(room_code)))
            room_label = Label(frame, width=30, text="", fg="black")

        ludo_label = Label(frame, text="Ludo", fg="black")
        blank = Label(frame, text="", fg="black")
        back = Button(frame, text="Back", command=lambda: self.back(game_id))
        in_lobby = Label(frame, width=30, text=("In Lobby: %s/4" % (str(player_number))),
                         fg="black")  # take in number of players in that game
        start_game = Button(frame, width=30, text="Start Game",
                            command=lambda: self.start_game(name_entry.get(), int(game_id)))

        update = Button(frame, width=30, text="Update Lobby Number",
                        command=lambda: self.update(lobby_type, room_code, game_id))

        # Drawing each widget on to the frame
        self.root.minsize(width=220, height=260)
        self.root.maxsize(width=220, height=260)
        self.root.configure(background="white")

        frame.pack()
        frame.configure(background="white")

        ludo_label.grid(row=1, column=1, columnspan=2)
        ludo_label.configure(font=("Arial", 32), background="white")

        blank.grid(row=2, column=3)
        blank.configure(background="white")

        name_label.grid(row=3, column=1)
        name_label.configure(background="white")
        name_entry.grid(row=3, column=2)
        name_entry.configure(background="white")

        label.grid(row=4, column=1, columnspan=2)
        label.configure(background="white")

        room_label.grid(row=5, column=1, columnspan=2)
        room_label.configure(background="white")

        in_lobby.grid(row=6, column=1, columnspan=2)
        in_lobby.configure(background="white")

        start_game.grid(row=7, column=1, columnspan=2)
        start_game.configure(background="lightgreen")

        update.grid(row=8, column=1, columnspan=2)
        update.configure(background="lightgreen")

        back.grid(row=9, column=1)
        back.configure(background="red")
        self.root.mainloop()

    def no_room(self):
        """
        Invoked if no room is available, this will inform the client that their
        is no room.
        """
        # Same setup for each new page
        self.root.destroy()
        self.root = Tk()
        self.root.geometry('+%d+%d' % (100, 100))
        self.root.title("Ludo")
        self.current_page = "no_room"
        frame = Frame(self.root)

        ludo_label = Label(frame, text="Ludo", fg="black")
        blank = Label(frame, text="", fg="black")
        back = Button(frame, text="Back", command=self.back)

        # This is the part that varies between pages
        no_room = Label(frame, width=30,
                        text="Room Code doesn't exist", fg="black")
        try_again = Label(
            frame, width=30, text="Please try another room code", fg="black")

        # Drawing each widget on to the frame
        self.root.minsize(width=220, height=210)
        self.root.maxsize(width=220, height=210)
        self.root.configure(background="white")

        frame.pack()
        frame.configure(background="white")

        ludo_label.grid(row=1, column=1, columnspan=2)
        ludo_label.configure(font=("Arial", 32), background="white")

        blank.grid(row=2, column=3)
        blank.configure(background="white")

        no_room.grid(row=3, column=1, columnspan=2)
        no_room.configure(background="white")

        try_again.grid(row=4, column=1, columnspan=2)
        try_again.configure(background="white")

        back.grid(row=7, column=1)
        back.configure(background="red")
        self.root.mainloop()

    def already_exists(self, code):
        """
        Inform the player that this room already exits.

        :param code: room code
        :type code: str
        """
        # Same setup for each new page
        self.root.destroy()
        self.root = Tk()
        self.root.geometry('+%d+%d' % (100, 100))
        self.root.title("Ludo")
        self.current_page = "already_exists"
        frame = Frame(self.root)

        ludo_label = Label(frame, text="Ludo", fg="black")
        blank = Label(frame, text="", fg="black")
        back = Button(frame, text="Back", command=self.back)

        # This is the part that varies between pages
        exists = Label(frame, width=30, text=(
                "Room Code %s already exists" % (str(code))), fg="black")
        try_again = Label(
            frame, width=30, text="Please try another room code", fg="black")

        # Drawing each widget on to the frame
        self.root.minsize(width=220, height=210)
        self.root.maxsize(width=220, height=210)
        self.root.configure(background="white")

        frame.pack()
        frame.configure(background="white")

        ludo_label.grid(row=1, column=1, columnspan=2)
        ludo_label.configure(font=("Arial", 32), background="white")

        blank.grid(row=2, column=3)
        blank.configure(background="white")

        exists.grid(row=3, column=1, columnspan=2)
        exists.configure(background="white")

        try_again.grid(row=4, column=1, columnspan=2)
        try_again.configure(background="white")

        back.grid(row=7, column=1)
        back.configure(background="red")
        self.root.mainloop()

    def start_game(self, name, game_id):
        """
        Invoked when a room had met the amount of players necessary for a game.
        This removes the tk window and begins the game.

        :param name: Name of game.
        :type name: str
        :param game_id: Identification for this game.
        :type game_id: int
        """
        if len(name) != 0:
            self.connection.send_start_the_game(game_id, name)
            self.root.destroy()

    def check_room_code(self, check_type, code):
        """
        Checks if the room is private, public, if is exists or not and if your
        code is correct if it is private.

        :param check_type: Checks which window the clients has come from.
        :type check_type: str
        :param code: Password for a private sever.
        :type code: str
        """
        if code != "":  # for private game
            data = {"check_room_code": str(code), "check_type": check_type}
            data = json.dumps(data)
            self.connection.sock.sendall(data.encode())
            # only get game.num when you go to lobby
            # decodes received data.
            data = self.connection.sock.recv(4096).decode()
            msg = json.loads(data)
            exists = msg["exists"]
            if exists:
                if check_type == "create":
                    self.already_exists(code)
                elif check_type == "join":
                    self.connection.send_join_lobby_message(msg["game_id"])
                    self.lobby("private", msg["room_code"],
                               msg["num_of_players"] + 1, msg["game_id"])
            else:
                if check_type == "create":
                    # Automatically creates new game server-side if one
                    # didn't exist
                    self.connection.send_join_lobby_message(msg["new_game_id"])
                    self.lobby("create", code, 1, msg["new_game_id"])
                elif check_type == "join":
                    self.no_room()
        else:  # for public game
            self.connection.send_create_game(code)
            # accepts the id of your newly created game
            data = self.connection.sock.recv(4096).decode()
            msg = json.loads(data)
            self.connection.send_join_lobby_message(msg["game_id"])
            self.lobby("create", code,
                       msg["player_number"] + 1, msg["game_id"], )

    def show_rules(self):
        """
        Produces a document of the rules of the ludo game.
        Pops up a separate page, so there's no ``self.root.destroy()``
        """
        file = open(self.filename, "r")
        data = file.read()
        Label(self.root, text=file.read()).pack()
        self.root = Tk()
        self.root.geometry('+%d+%d' % (100, 100))
        self.root.title("Rules")
        w = Label(self.root, text=data, fg="black", bg="lightblue")
        w.pack()
        self.root.mainloop()

    def back(self, game_id=None):
        """
        Go back from current tk window after pressing back button.
        """
        if self.current_page == "create_game" or self.current_page == "join_public" or \
                self.current_page == "join_private":
            self.home_page()
        elif self.current_page == "no_room":
            self.join_private()
        elif self.current_page == "private_lobby":
            self.connection.send_leave_lobby(game_id)
            self.join_private()
        elif self.current_page == "already_exists":
            self.create_game()
        elif self.current_page == "create_lobby":
            self.connection.send_leave_lobby(game_id)
            self.create_game()
        elif self.current_page == "public_lobby":

            self.connection.send_leave_lobby(game_id)
            self.join_public()
        elif self.current_page == "public_room_is_full":
            self.home_page()

    def run(self):
        """Runs the form"""
        self.home_page()
