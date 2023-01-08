import random
from tkinter import *
from tkinter import messagebox






class Player:
    def __init__(self, name, score=0):
        self.name = name
        self.score = score


class Line:
    def __init__(self, row: int, column: int, button: Button, orientation: str, state: bool):
        self.row = row
        self.column = column
        self.button = button
        self.orientation = orientation
        self.state = state

    def __str__(self):
        return self.orientation + str((self.row, self.column))


class Box:
    def __init__(self, row: int, column: int, label: Label, state: bool):
        self.row = row
        self.column = column
        self.label = label
        self.state = state


class Game:

    def __init__(self,gridSize=8):
        self.GRID_SIZE = gridSize
        self.COLOUR_HEADER_BG = "#D190FF"
        self.COLOUR_TURN_ACTIVE = "#3FFF00"
        self.COLOUR_TURN_INACTIVE = "#FFF200"

        self.root = Tk()
        self.root.title('Dots and Boxes')
        self.root.configure(background="white")
        self.start_game()

    def start_game(self):
        self.lineX_list = []
        self.lineY_list = []
        self.active_lineX_list = []
        self.active_lineY_list = []
        self.inactive_lineX_list = []
        self.inactive_lineY_list = []
        self.box_list = []
        self.user_score = 0
        self.bot_score = 0
        self.turn = "User"
        self.set_header()
        self.set_playboard()

    def set_header(self):

        self.header = Frame(self.root, background=self.COLOUR_HEADER_BG,padx=20)
        self.header.grid(row=0)

        self.options = Frame(self.header, background=self.COLOUR_HEADER_BG, pady=20)
        self.turn_label = Label(self.options, text=f"{self.turn}'s turn", foreground="white", font=("Cooper Black", 15),
                                background=self.COLOUR_HEADER_BG)
        self.turn_label.pack(anchor=N)
        self.restart_img = PhotoImage(file="images/restart.png")
        Button(self.options, image=self.restart_img, relief=SUNKEN, borderwidth=0, background=self.COLOUR_HEADER_BG,
               command=self.start_game).pack(anchor=S)
        self.options.grid(row=0, ipadx=240)
        self.score_line = Frame(self.header, background=self.COLOUR_HEADER_BG,pady=10)
        self.score_line.grid(row=1, ipadx=100)
        self.user_img = PhotoImage(file='images/user.png')
        self.bot_img = PhotoImage(file='images/bot.png')

        self.user_frame = Frame(self.score_line, padx=5, pady=5, background=self.COLOUR_TURN_ACTIVE)
        self.user_frame.pack(side=LEFT)

        self.label_user_score = Label(self.score_line, text=f'You: {self.user_score}', padx=20,
                                      background=self.COLOUR_HEADER_BG,
                                      font=("Arial", 20), foreground="#FFFFFF")
        self.label_user_score.pack(side=LEFT)

        self.bot_frame = Frame(self.score_line, padx=5, pady=5, background=self.COLOUR_TURN_INACTIVE)
        self.bot_frame.pack(side=RIGHT)

        self.label_bot_score = Label(self.score_line, text=f'AI: {self.bot_score}', padx=20,
                                     background=self.COLOUR_HEADER_BG,
                                     font=("Arial", 20), foreground="#FFFFFF")
        self.label_bot_score.pack(side=RIGHT)

        user_frame = Frame(self.user_frame, padx=5, pady=5, background=self.COLOUR_TURN_INACTIVE)
        user_frame.pack()
        bot_frame = Frame(self.bot_frame, padx=5, pady=5, background=self.COLOUR_TURN_INACTIVE)
        bot_frame.pack()
        Label(user_frame, image=self.user_img, padx=5, pady=5, borderwidth=10, ).grid()
        Label(bot_frame, image=self.bot_img, padx=5, pady=5, borderwidth=10).grid()

    def set_playboard(self):
        # self.test_entry = Entry(self.root, width=20)
        # self.test_entry.grid(row=2,column=0)
        # self.test_button = Button(self.root,text="Play AI",command=self.play_bot)
        # self.test_button.grid(row=2,column=1)

        self.playboard = Frame(self.root, pady=20, padx=10, background="white", borderwidth=10)
        self.playboard.grid(row=1)

        self.line_x_img = PhotoImage(file='images/line_x.png')
        self.line_y_img = PhotoImage(file='images/line_y.png')
        self.dot_img = PhotoImage(file='images/dot.png')
        self.blank_img = PhotoImage(file='images/blank.png')
        self.user_box_img = PhotoImage(file='images/user_box.png')
        self.bot_box_img = PhotoImage(file='images/bot_box.png')

        for i in range(0, (self.GRID_SIZE * 2) + 1):
            for j in range(0, (self.GRID_SIZE * 2) + 1):
                if i % 2 == 0 and j % 2 == 0:  # dots
                    Label(self.playboard, image=self.dot_img, borderwidth=0, background="white").grid(row=i,
                                                                                                    column=j)
                elif i % 2 == 0 and j % 2 != 0:  # line x
                    line_x_btn = Button(self.playboard, image=self.blank_img, relief=SUNKEN, borderwidth=0,
                                        background="white",
                                        command=lambda x=i, y=j: self.makeLineX(x, y))
                    self.lineX_list.append(Line(i, j, line_x_btn, "x", False))
                    self.inactive_lineX_list.append(Line(i, j, line_x_btn, "x", False))
                    line_x_btn.grid(row=i, column=j)


                elif i % 2 != 0 and j % 2 == 0:  # line y
                    line_y_btn = Button(self.playboard, image=self.blank_img, relief=SUNKEN, borderwidth=0,
                                        background="white",
                                        command=lambda x=i, y=j: self.makeLineY(x, y))
                    self.lineY_list.append(Line(i, j, line_y_btn, "y", False))
                    self.inactive_lineY_list.append(Line(i, j, line_y_btn, "y", False))
                    line_y_btn.grid(row=i, column=j)
                elif i % 2 != 0 and j % 2 != 0:  # box
                    label = Label(self.playboard, image=self.blank_img, borderwidth=0, background="white")
                    self.box_list.append(Box(i, j, label, False))
                    label.grid(row=i, column=j)

        self.root.mainloop()

    def makeLineX(self, row, column):
        for line in self.lineX_list:
            if line.row == row and line.column == column:

                line.button.configure(image=self.line_x_img, relief=SUNKEN, borderwidth=0, background="white")
                print(self.turn,":",line)
                line.state = True
                self.active_lineX_list.append(line)
                if not self.boxCheck():
                    self.turn_change()

    def makeLineY(self, row, column):
        for line in self.lineY_list:
            if line.row == row and line.column == column:
                line.button.configure(image=self.line_y_img, relief=SUNKEN, borderwidth=0, background="white")
                print(self.turn,":",line)
                line.state = True
                self.active_lineY_list.append(line)
                if not self.boxCheck():
                    self.turn_change()

    def boxCheck(self):
        for lineX1 in self.active_lineX_list:
            for lineX2 in self.active_lineX_list:
                if lineX1 != lineX2:
                    if lineX1.column == lineX2.column and (lineX1.row - lineX2.row) == -2:
                        r1 = lineX1.row + 1
                        c1 = lineX1.column - 1

                        r2 = lineX1.row + 1
                        c2 = lineX1.column + 1

                        for lineY1 in self.active_lineY_list:
                            for lineY2 in self.active_lineY_list:
                                if lineY1 != lineY2:

                                    if lineY1.row == lineY2.row and (lineY1.column - lineY2.column) == -2:

                                        if lineY1.row == r1 and lineY1.column == c1 and lineY2.row == r2 and lineY2.column == c2:

                                            for box in self.box_list:
                                                if not box.state:
                                                    if box.row == r1 and box.column == c1 + 1:
                                                        if self.turn == "User":
                                                            box.label.configure(image=self.user_box_img)
                                                        elif self.turn == "AI":
                                                            box.label.configure(image=self.bot_box_img)
                                                            self.root.after(1000, self.play_bot)



                                                        box.state = True
                                                        self.boxCheck()
                                                        self.score_update()


                                                        return True
        return False

    def turn_change(self):
        if self.turn == "User":
            self.user_frame.configure(background=self.COLOUR_TURN_INACTIVE)
            self.bot_frame.configure(background=self.COLOUR_TURN_ACTIVE)
            self.turn = "AI"
            self.root.after(1000,self.play_bot)

        elif self.turn == "AI":
            self.user_frame.configure(background=self.COLOUR_TURN_ACTIVE)
            self.bot_frame.configure(background=self.COLOUR_TURN_INACTIVE)
            self.turn = "User"
        self.turn_label.configure(text=f"{self.turn}'s turn")

    def score_update(self):
        if self.turn == "AI":
            self.bot_score += 1
            self.label_bot_score.configure(text=f'AI: {self.bot_score}')


        elif self.turn == "User":
            self.user_score += 1
            self.label_user_score.configure(text=f'You: {self.user_score}')
        if self.user_score+self.bot_score == self.GRID_SIZE * self.GRID_SIZE:
            if self.user_score > self.bot_score:
                message = "You win!!"
            else:
                message = "AI win!!"
            val = messagebox.askquestion(message,"You want to play again?")
            print(val)
            if val == "yes":
                self.start_game()
            else:
                self.root.destroy()

    def two_linesX_areOpposite(self, lineX1:Line, lineX2:Line):
        return lineX1.column == lineX2.column and (lineX1.row - lineX2.row) == -2

    def lineX_perpendicular_to(self, lineY1: Line):
        r1 = lineY1.row - 1
        c1 = lineY1.column + 1

        r2 = lineY1.row + 1
        c2 = lineY1.column + 1

        for lineX1 in self.active_lineX_list:
            for lineX2 in self.active_lineX_list:
                if lineX1 != lineX2:
                    if not self.lineX_isActive(r2, c2):
                        if lineX1.row == r1 and lineX1.column == c1:
                            return Line(r2,c2,None,'x',False)
                    if not self.lineX_isActive(r1, c1):
                        if lineX1.row == r2 and lineX1.column == c2:
                            return Line(r1,c1,None,'x',False)

    def lineX_isActive(self, row, column):
        for line in self.lineX_list:
            if line.row == row and line.column == column:
                return line.state
        return False
    def two_linesY_areOpposite(self, lineY1: Line, lineY2: Line):
        return lineY1.row == lineY2.row and (lineY1.column - lineY2.column) == -2

    def lineY_perpendicular_to(self, lineX1: Line):
        r1 = lineX1.row + 1
        c1 = lineX1.column - 1

        r2 = lineX1.row + 1
        c2 = lineX1.column + 1

        for lineY1 in self.active_lineY_list:
            for lineY2 in self.active_lineY_list:
                if lineY1 != lineY2:
                    if not self.lineY_isActive(r2, c2):
                        if lineY1.row == r1 and lineY1.column == c1:
                            return Line(r2, c2, None, 'y', False)
                    if not self.lineY_isActive(r1, c1):
                        if lineY1.row == r2 and lineY1.column == c2:
                            return Line(r1,c1,None,'y',False)

    def lineY_isActive(self, row, column):
        for line in self.lineY_list:
            if line.row == row and line.column == column:
                return line.state
        return False

    def two_lineX_arePerpendicularTo(self,lineY1:Line):
        """returns True if two lines are opposite to each other, and perpendicular to given line"""

        # for left side of line
        if self.line_left_up_isActive(lineY1) and self.line_left_down_isActive(lineY1):
            print("Two perpendicular lines are active")
            return True
        # for right side of line
        elif self.line_right_up_isActive(lineY1) and self.line_right_down_isActive(lineY1):
            print("Two perpendicular lines are active")
            return True
        else:
            return False

    def two_lineY_arePerpendicularTo(self,lineX1:Line):
        """returns True if two lines are opposite to each other, and perpendicular to given line"""
        # for upside of line
        if self.line_left_up_isActive(lineX1) and self.line_right_up_isActive(lineX1):
            print("Two perpendicular lines are active")
            return True
        # for downside of line
        elif self.line_left_down_isActive(lineX1) and self.line_right_down_isActive(lineX1):
            print("Two perpendicular lines are active")
            return True
        else:
            return False

    def line_left_up_isActive(self,line):
        if line.orientation == "x":
            return self.lineY_isActive(line.row - 1, line.column - 1)
        elif line.orientation == "y":
            return self.lineX_isActive(line.row - 1, line.column - 1)

    def line_left_down_isActive(self,line):
        if line.orientation == "x":
            return self.lineY_isActive(line.row + 1, line.column - 1)
        elif line.orientation == "y":
            return self.lineX_isActive(line.row + 1, line.column - 1)


    def line_right_up_isActive(self, line):
        if line.orientation == "x":
            return self.lineY_isActive(line.row - 1, line.column + 1)
        elif line.orientation == "y":
            return self.lineX_isActive(line.row - 1, line.column + 1)

    def line_right_down_isActive(self, line):
        if line.orientation == "x":
            return self.lineY_isActive(line.row + 1, line.column + 1)
        elif line.orientation == "y":
            return self.lineX_isActive(line.row + 1, line.column + 1)

    def lineX_up_isActive(self, line):

        return self.lineX_isActive(line.row - 2,line.column)

    def lineX_down_isActive(self, line):
        return self.lineX_isActive(line.row + 2,line.column)

    def lineY_left_isActive(self, line):
        return self.lineY_isActive(line.row, line.column - 2)

    def lineY_right_isActive(self, line):
        return self.lineY_isActive(line.row, line.column + 2)

    def lineX_opposite_and_prep(self,lineX1):
        if self.lineX_up_isActive(lineX1):
            if self.line_left_up_isActive(lineX1):
                print("opposite L active")
                return True
            elif self.line_right_up_isActive(lineX1):
                print("opposite L active")
                return True

        elif self.lineX_down_isActive(lineX1):
            if self.line_left_down_isActive(lineX1):
                print("opposite L active")
                return True
            elif self.line_right_down_isActive(lineX1):
                print("opposite L active")
                return True
        else:
            return False

    def lineY_opposite_and_prep(self,lineY1):
        if self.lineY_left_isActive(lineY1):
            if self.line_left_up_isActive(lineY1):
                print("opposite L active")
                return True
            elif self.line_left_down_isActive(lineY1):
                print("opposite L active")
                return True

        elif self.lineY_right_isActive(lineY1):
            if self.line_right_up_isActive(lineY1):
                print("opposite L active")
                return True
            elif self.line_right_down_isActive(lineY1):
                print("opposite L active")
                return True
        else:
            return False





    def play_bot(self):
        print("play Bot")

        for lineX1 in self.active_lineX_list: # check for line x

            for lineX2 in self.active_lineX_list:
                if lineX1 != lineX2:
                    if self.two_linesX_areOpposite(lineX1, lineX2):

                        # check for any two opposite lines
                        lineY = self.lineY_perpendicular_to(lineX1)

                        if lineY:
                            self.makeLineY(lineY.row, lineY.column)
                            return


        for lineY1 in self.active_lineY_list:
            for lineY2 in self.active_lineY_list:
                if lineY1 != lineY2:
                    if self.two_linesY_areOpposite(lineY1, lineY2):  # check for any two opposite lines
                        lineX = self.lineX_perpendicular_to(lineY1)

                        if lineX:
                            self.makeLineX(lineX.row,lineX.column)
                            return
        count = 0
        while True:
                count += 1
                random_list = [self.lineX_list,self.lineY_list]
                random_ort = random.randint(0,1)
                random_line = random.choice(random_list[random_ort])
                # linestr = self.test_entry.get()
                # line = linestr.split(" ")
                #
                # random_line = Line(int(line[0]),int(line[1]),None,line[2],False)
                # print(random_line)




                if not random_line.state:

                    if random_line.orientation == "x":
                        if not self.two_lineY_arePerpendicularTo(random_line):
                            print("X: Not perpendicular to two lines")
                            if not self.lineX_opposite_and_prep(random_line):
                                print("X: Not L to an line")

                                self.makeLineX(random_line.row, random_line.column)
                                return


                    elif random_line.orientation == "y":
                        if not self.two_lineX_arePerpendicularTo(random_line):
                            print("Y: Not perpendicular to two lines")
                            if not self.lineY_opposite_and_prep(random_line):
                                print("Y: Not L to an line")
                                self.makeLineY(random_line.row, random_line.column)

                                return

                    if count > 2 * len(self.lineX_list):
                        if random_line.orientation == "x":
                            self.makeLineX(random_line.row, random_line.column)
                            return
                        elif random_line.orientation == "y":
                            self.makeLineY(random_line.row, random_line.column)
                            return



Game()

