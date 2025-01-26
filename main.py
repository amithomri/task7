# 211321823 amit homri
import tkinter as tk
from tkinter import messagebox
import random


def show_win_message(event):
    messagebox.showinfo("Result", "You Win!")


def show_lose_message(event):
    messagebox.showinfo("Result", "You Lose!")

class Cell:
    def __init__(self, state, is_mine = False):
        self.state = state
        self.is_revealed = True if state == "revealed" else False
        self.isbomb = is_mine
        self.neighbor_bombs = 0

    def set_is_bomb(self):
        self.isbomb = True
class Board:
    def __init__(self, size_board, nubmer_mines):
        self.size_board = size_board
        self.nubmer_mines = nubmer_mines
        self.grid = self.generate_grid_matrix(size_board)
        self.mines_positions= self.add_mines_to_grid(nubmer_mines)

    # add mines to random places in grids
    def add_mines_to_grid(self,number_of_mines):
        mines_positions_arr=[]
        index = 0
        while index < number_of_mines:
            x_mine = random.randint(0,self.size_board-1)
            y_mine = random.randint(0,self.size_board-1)
            if(x_mine,y_mine) not in mines_positions_arr:
                mines_positions_arr.append((x_mine,y_mine))
                self.grid[x_mine][y_mine].set_is_bomb()
                #self.grid[x_mine][y_mine].isbomb = True
                index = index + 1
        return mines_positions_arr

    #return grid matrix of cells for game
    def generate_grid_matrix( self,size_board):
        matrix_row = []
        game_grid = []
        for i in range(size_board):
            matrix_row = []
            for j in range(size_board):
                matrix_row.append(Cell("hidden", False))
            game_grid.append(matrix_row)
        return game_grid

    #returns cell.neighbor_bomb for given cell in pos x,y
    def calculate_adjacent_mines(self, x, y):
        count_adjacent_mines = 0
        #iterate over neighbors check if contain mine
        for neighbors_x in range(max(0, x - 1), min(self.size_board, x + 2)):
            for neighbors_y in range(max(0, y - 1), min(self.size_board, y + 2)):
                if self.grid[neighbors_x][neighbors_y].isbomb:
                    count_adjacent_mines += 1
        return count_adjacent_mines - self.grid[x][y].isbomb

    #update addject-mines field in every cell in grid.
    def add_adjecent_mines_to_grid(self):
        for x in range(self.size_board):
            for y in range(self.size_board):
                #cant have neighnors containg if it containes number not neccerssary of neighbors
                if not self.grid[x][y].isbomb:
                    self.grid[x][y].neighbor_bombs = self.calculate_adjacent_mines(x, y)
class MineSweeper:
    def __init__(self, my_root, size, num_mines):
        self.root = my_root
        self.num_mines = num_mines
        self.size = size
        self.buttons = []
        self.board = Board(size, num_mines)
        self._create_widgets()

    #return true if player won game all mines not revealed and all non mines revealed
    def checkwin(self):
        for x in range(self.size):
            for y in range(self.size):
                cell = self.board.grid[x][y]
                #didn't win only if we have unrevealed celles that ain't bomb
                if  cell.state != "revealed" and cell.isbomb == False:
                    return False
        return True

    #handling right click to toggle flag on cell
    def _toggle_flag(self, x, y):
        marked_cell=self.board.grid[x][y]
        #if hidden then flag it
        if marked_cell.state == "hidden":
            marked_cell.state = "flagged"
            self.buttons[x][y].config(text="F", bg="yellow")
        # if flagged  then remove flag
        elif marked_cell.state == "flagged":
            marked_cell.state = "hidden"
            self.buttons[x][y].config(text="", bg="light gray")
        # if cell is revealed then pass

    # handling left click event to reveal cell
    def _reveal_cell(self,x,y):
        marked_cell=self.board.grid[x][y]
        #if cell is flagged then pass no revealing while being flagged
        if marked_cell.state == "flagged":
            return
        # if contains mine game over else player lost else reveal cell
        if marked_cell.isbomb:
            show_lose_message(None)
            self.root.quit()
        # doesnt contain main so reveal cell
        else:
            marked_cell.state = "revealed"
            if marked_cell.neighbor_bombs > 0 :
                text_revealed_cell = marked_cell.neighbor_bombs
            else:
                text_revealed_cell = ""
            self.buttons[x][y].config(
                bg="white",
                text=str(text_revealed_cell),
                state=tk.DISABLED)
            #  if no mines nearby reveald neighbors recursively
            if marked_cell.neighbor_bombs == 0:
                self._reveal_recursive(x,y)
            if self.checkwin():
                show_win_message(None)
                self.root.quit()





    def _create_widgets(self):
        for x in range(self.board.size_board):
            row = []
        for y in range(self.board.size_board):
            btn = tk.Button(self.root, width=2, height=1, bg="light gray",
                            command=lambda x1=x, y1=y: self._reveal_cell(x1, y1))
        btn.bind("<Button-3>", lambda e, x2=x, y2=y: self._toggle_flag(x2, y2))
        btn.grid(row=x, column=y)
        row.append(btn)
        self.buttons.append(row)


    def _reveal_recursive(self, x, y):
        #cell = self.board.cells[x][y]
        cell = self.board.grid[x][y]
        if cell.is_revealed or cell.isbomb:
            return
        cell.is_revealed = True
        self.buttons[x][y].config(bg="white", state=tk.DISABLED,
                                text=str(cell.neighbor_bombs) if cell.neighbor_bombs > 0
                                else "")
        if cell.neighbor_bombs == 0:
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                if 0 <= x + dx < self.board.size_board and 0 <= y + dy < self.board.size_board:
                    self._reveal_recursive(x + dx, y + dy)


if __name__ == '__main__':
    s = int(input("Enter the size of the board: "))
    b = int(input("Enter the number of bombs: "))
    root = tk.Tk()
    game = MineSweeper(root, s, b)
    game.root.mainloop()
