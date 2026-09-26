import tkinter as tk
import random
import sys

sys.setrecursionlimit(10**6)

ROWS, COLS = 16, 30
MINES = 99
TILE_SIZE = 24  # Scale up slightly from 16 for better visibility on modern screens

class MinesweeperGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.configure(bg="#C0C0C0")
        self.root.resizable(False, False)
        
        self.num_colors = {
            1: "#0000FF", 2: "#008000", 3: "#FF0000", 4: "#000080",
            5: "#800000", 6: "#008080", 7: "#000000", 8: "#808080"
        }
        
        # Main container with 3D raised border
        self.main_frame = tk.Frame(self.root, bg="#C0C0C0", bd=3, relief=tk.RAISED)
        self.main_frame.pack(padx=6, pady=6)
        
        # Top panel with sunken border
        self.top_frame = tk.Frame(self.main_frame, bg="#C0C0C0", bd=2, relief=tk.SUNKEN)
        self.top_frame.pack(fill=tk.X, padx=6, pady=6)
        
        # Mines digital counter
        self.canvas_mines = tk.Canvas(self.top_frame, width=45, height=25, bg="black", bd=1, relief=tk.SUNKEN, highlightthickness=0)
        self.canvas_mines.pack(side=tk.LEFT, padx=5, pady=4)
        
        # Smiley face button
        self.btn_reset = tk.Button(self.top_frame, text="🙂", font=("Arial", 14), bg="#C0C0C0", bd=2, relief=tk.RAISED, command=self.reset_game, width=2, height=1)
        self.btn_reset.pack(side=tk.LEFT, expand=True)
        
        # Timer digital counter
        self.canvas_timer = tk.Canvas(self.top_frame, width=45, height=25, bg="black", bd=1, relief=tk.SUNKEN, highlightthickness=0)
        self.canvas_timer.pack(side=tk.RIGHT, padx=5, pady=4)
        
        # Grid frame with sunken border
        self.grid_frame = tk.Frame(self.main_frame, bg="#C0C0C0", bd=3, relief=tk.SUNKEN)
        self.grid_frame.pack(padx=6, pady=(0, 6))
        
        # Canvas for the board
        self.canvas = tk.Canvas(self.grid_frame, width=COLS*TILE_SIZE, height=ROWS*TILE_SIZE, bg="#C0C0C0", highlightthickness=0)
        self.canvas.pack()
        
        # Auto-Solve button at the bottom
        self.btn_solve = tk.Button(self.root, text="Auto Solve (4-Way Logic)", font=("Arial", 9), bg="#C0C0C0", bd=2, relief=tk.RAISED, command=self.auto_solve)
        self.btn_solve.pack(pady=(0, 6))
        
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        
        self.timer_id = None
        self.reset_game()
        
    def draw_digital_number(self, canvas, value):
        canvas.delete("all")
        # Draw dark red 888 background
        canvas.create_text(22, 12, text="888", font=("Courier New", 18, "bold"), fill="#500000")
        # Draw actual value
        val_str = f"{max(0, min(999, value)):03d}"
        canvas.create_text(22, 12, text=val_str, font=("Courier New", 18, "bold"), fill="#FF0000")
        
    def reset_game(self):
        self.is_game_over = False
        self.first_click = True
        self.flags = MINES
        self.revealed_count = 0
        self.time_elapsed = 0
        
        self.draw_digital_number(self.canvas_mines, self.flags)
        self.draw_digital_number(self.canvas_timer, 0)
        self.btn_reset.config(text="🙂")
        
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
            
        self.board_state = [["hidden" for _ in range(COLS)] for _ in range(ROWS)]
        self.flag_state = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.mine_matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.count_matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        
        self.draw_entire_board()
        
    def draw_entire_board(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                self.draw_cell(r, c)
                
    def draw_cell(self, r, c):
        x, y = c * TILE_SIZE, r * TILE_SIZE
        state = self.board_state[r][c]
        
        # Clear area
        self.canvas.create_rectangle(x, y, x+TILE_SIZE, y+TILE_SIZE, fill="#C0C0C0", outline="")
        
        if state == "hidden":
            # Raised 3D border
            self.canvas.create_polygon(x, y, x+TILE_SIZE, y, x+TILE_SIZE-3, y+3, x+3, y+3, x+3, y+TILE_SIZE-3, x, y+TILE_SIZE, fill="#FFFFFF", outline="")
            self.canvas.create_polygon(x, y+TILE_SIZE, x+TILE_SIZE, y+TILE_SIZE, x+TILE_SIZE, y, x+TILE_SIZE-3, y+3, x+TILE_SIZE-3, y+TILE_SIZE-3, x+3, y+TILE_SIZE-3, fill="#808080", outline="")
            self.canvas.create_rectangle(x+3, y+3, x+TILE_SIZE-3, y+TILE_SIZE-3, fill="#C0C0C0", outline="")
            
            if self.flag_state[r][c]:
                # Draw Flag
                cx, cy = x + TILE_SIZE/2, y + TILE_SIZE/2
                # Base
                self.canvas.create_line(cx-5, cy+6, cx+5, cy+6, fill="black", width=2)
                # Pole
                self.canvas.create_line(cx, cy+6, cx, cy-5, fill="black", width=2)
                # Flag
                self.canvas.create_polygon(cx, cy-5, cx, cy+1, cx-6, cy-2, fill="red", outline="red")
                
        elif state == "revealed":
            # Flat with 1px border
            self.canvas.create_rectangle(x, y, x+TILE_SIZE, y+TILE_SIZE, fill="#C0C0C0", outline="#808080")
            count = self.count_matrix[r][c]
            if count > 0:
                color = self.num_colors.get(count, "black")
                self.canvas.create_text(x+TILE_SIZE/2, y+TILE_SIZE/2, text=str(count), fill=color, font=("Arial", 12, "bold"))
                
        elif state == "mine":
            self.canvas.create_rectangle(x, y, x+TILE_SIZE, y+TILE_SIZE, fill="#C0C0C0", outline="#808080")
            self.draw_mine(x, y)
            
        elif state == "mine_red":
            self.canvas.create_rectangle(x, y, x+TILE_SIZE, y+TILE_SIZE, fill="red", outline="#808080")
            self.draw_mine(x, y)
            
        elif state == "false_mine":
            self.canvas.create_rectangle(x, y, x+TILE_SIZE, y+TILE_SIZE, fill="#C0C0C0", outline="#808080")
            self.draw_mine(x, y)
            self.canvas.create_line(x+4, y+4, x+TILE_SIZE-4, y+TILE_SIZE-4, fill="red", width=2)
            self.canvas.create_line(x+TILE_SIZE-4, y+4, x+4, y+TILE_SIZE-4, fill="red", width=2)
            
    def draw_mine(self, x, y):
        cx, cy = x + TILE_SIZE/2, y + TILE_SIZE/2
        self.canvas.create_oval(cx-6, cy-6, cx+6, cy+6, fill="black", outline="black")
        self.canvas.create_line(cx, cy-8, cx, cy+8, fill="black", width=2)
        self.canvas.create_line(cx-8, cy, cx+8, cy, fill="black", width=2)
        self.canvas.create_line(cx-6, cy-6, cx+6, cy+6, fill="black", width=2)
        self.canvas.create_line(cx+6, cy-6, cx-6, cy+6, fill="black", width=2)
        self.canvas.create_oval(cx-2, cy-2, cx, cy, fill="white", outline="white")
        
    def update_timer(self):
        if not self.is_game_over and not self.first_click:
            self.time_elapsed += 1
            self.draw_digital_number(self.canvas_timer, self.time_elapsed)
            self.timer_id = self.root.after(1000, self.update_timer)
            
    def generate_mines(self, first_r, first_c):
        mines_placed = 0
        while mines_placed < MINES:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            if abs(r - first_r) + abs(c - first_c) <= 1:
                continue
            if self.mine_matrix[r][c] == 0:
                self.mine_matrix[r][c] = 1
                mines_placed += 1
                
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for r in range(ROWS):
            for c in range(COLS):
                count = 0
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        count += self.mine_matrix[nr][nc]
                self.count_matrix[r][c] = count
                
    def on_left_click(self, event):
        if self.is_game_over: return
        c, r = event.x // TILE_SIZE, event.y // TILE_SIZE
        if r >= ROWS or c >= COLS: return
        if self.board_state[r][c] != "hidden" or self.flag_state[r][c]: return
            
        if self.first_click:
            self.first_click = False
            self.generate_mines(r, c)
            self.update_timer()
            
        if self.mine_matrix[r][c] == 1:
            self.game_over(False, clicked_mine=(r, c))
            return
            
        self.reveal(r, c)
        self.check_win()
        
    def on_right_click(self, event):
        if self.is_game_over or self.first_click: return
        c, r = event.x // TILE_SIZE, event.y // TILE_SIZE
        if r >= ROWS or c >= COLS: return
        if self.board_state[r][c] != "hidden": return
        
        if self.flag_state[r][c]:
            self.flag_state[r][c] = False
            self.flags += 1
        elif self.flags > 0:
            self.flag_state[r][c] = True
            self.flags -= 1
            
        self.draw_digital_number(self.canvas_mines, self.flags)
        self.draw_cell(r, c)
        
    def reveal(self, r, c):
        if r < 0 or r >= ROWS or c < 0 or c >= COLS: return
        if self.board_state[r][c] != "hidden" or self.flag_state[r][c]: return
        
        self.board_state[r][c] = "revealed"
        self.draw_cell(r, c)
        self.revealed_count += 1
        
        if self.count_matrix[r][c] == 0:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.reveal(r + dr, c + dc)
                
    def check_win(self):
        if self.revealed_count == ROWS * COLS - MINES:
            self.game_over(True)
            
    def game_over(self, win, clicked_mine=None):
        self.is_game_over = True
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
            
        self.btn_reset.config(text="😎" if win else "😵")
        
        for r in range(ROWS):
            for c in range(COLS):
                is_mine = (self.mine_matrix[r][c] == 1)
                is_flagged = self.flag_state[r][c]
                
                if win and is_mine and not is_flagged:
                    self.flag_state[r][c] = True
                    self.draw_cell(r, c)
                    
                if not win:
                    if is_mine and not is_flagged:
                        self.board_state[r][c] = "mine_red" if clicked_mine == (r, c) else "mine"
                        self.draw_cell(r, c)
                    elif not is_mine and is_flagged:
                        self.board_state[r][c] = "false_mine"
                        self.draw_cell(r, c)
                        
    def auto_solve(self):
        if self.is_game_over or self.first_click:
            return
            
        B = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        solution_found = False
        
        def check_and_fill():
            for r in range(1, ROWS):
                for c in range(COLS):
                    val = self.count_matrix[r-1][c]
                    if r >= 2: val -= B[r-2][c]
                    if c > 0: val -= B[r-1][c-1]
                    if c < COLS - 1: val -= B[r-1][c+1]
                    if val < 0 or val > 1: return False
                    B[r][c] = val
                    
            for c in range(COLS):
                sum_val = 0
                if ROWS >= 2: sum_val += B[ROWS-2][c]
                if c > 0: sum_val += B[ROWS-1][c-1]
                if c < COLS - 1: sum_val += B[ROWS-1][c+1]
                if sum_val != self.count_matrix[ROWS-1][c]: return False
            return True
            
        def backtrack(c):
            nonlocal solution_found
            if solution_found: return
            
            if c == COLS:
                if check_and_fill():
                    solution_found = True
                return
                
            lo, hi = 0, 1
            if c >= 1:
                base = self.count_matrix[0][c-1] - (B[0][c-2] if c >= 2 else 0)
                if ROWS == 1:
                    if base < 0 or base > 1: return
                    lo = hi = base
                else:
                    lo = max(0, base - 1)
                    hi = min(1, base)
                    if lo > hi: return
                    
            for val in range(lo, hi + 1):
                B[0][c] = val
                ok = True
                
                max_r = min(c, ROWS - 1)
                for r in range(1, max_r + 1):
                    col = c - r
                    rv = self.count_matrix[r-1][col]
                    if r >= 2: rv -= B[r-2][col]
                    if col > 0: rv -= B[r-1][col-1]
                    rv -= B[r-1][col+1]
                    if rv < 0 or rv > 1:
                        ok = False
                        break
                    else:
                        B[r][col] = rv
                        
                if not ok: continue
                backtrack(c + 1)
                if solution_found: return
                
        backtrack(0)
        
        if solution_found:
            for r in range(ROWS):
                for c in range(COLS):
                    if self.board_state[r][c] == "hidden":
                        if B[r][c] == 1:
                            if not self.flag_state[r][c]:
                                self.flag_state[r][c] = True
                                self.flags -= 1
                                self.draw_cell(r, c)
                        else:
                            self.reveal(r, c)
            self.draw_digital_number(self.canvas_mines, self.flags)
            self.check_win()

if __name__ == "__main__":
    root = tk.Tk()
    game = MinesweeperGame(root)
    root.mainloop()
