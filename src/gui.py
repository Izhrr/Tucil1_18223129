import tkinter as tk
import tkinter.messagebox as messagebox
import time
import os
import pyautogui
from logic import Logic

class GUI:
    def __init__(self, root):
        self.root = root
        self.board_data = None
        self.solver = None
        self.rows = 0
        self.cols = 0
        self.cell_size = 40
        self.color_map = {
            'A': '#FF9999', 'B': '#99FF99', 'C': '#9999FF', 'D': '#FFFF99',
            'E': '#FFCC99', 'F': '#CC99FF', 'G': '#99FFFF', 'H': '#E0E0E0',
            'I': '#FFD700', 'J': '#FFA07A', 'K': '#20B2AA', 'L': '#9370DB',
            'M': '#F08080', 'N': '#B0C4DE', 'O': '#40E0D0', 'P': '#D8BFD8',
            'Q': '#BDB76B', 'R': '#00FA9A', 'S': '#4682B4', 'T': '#FFB6C1',
            'U': '#A0522D', 'V': '#7FFFD4', 'W': '#DC143C', 'X': '#8FBC8F',
            'Y': '#F5DEB3', 'Z': '#708090'
        }
        self.solver_iterator = None
        self.running = False
        self.algo_time_ms = 0.0
        self.iterations = 0
        self.input_files = self.get_input_files()
        self.selected_file = None
        self.setup_ui()
        self.draw_board([])

    def get_input_files(self):
        txt_dir = os.path.join(os.getcwd(), 'input')
        files = [f for f in os.listdir(txt_dir) if f.endswith('.txt')]
        return files

    def setup_ui(self):
        self.root.title("Queens LinkedIn Solver")

        # Info frame
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10)
        self.lbl_iter = tk.Label(self.info_frame, text="Jumlah Iterasi: 0", font=("Verdana", 11))
        self.lbl_iter.pack(side=tk.LEFT, padx=10)
        self.lbl_time = tk.Label(self.info_frame, text="Waktu Pencarian: 0.00 ms", font=("Verdana", 11))
        self.lbl_time.pack(side=tk.LEFT, padx=10)

        # Board frame
        self.canvas = tk.Canvas(self.root, width=360, height=360, bg="white")
        self.canvas.pack(padx=20, pady=10)

        # Input frame
        select_frame = tk.Frame(self.root)
        select_frame.pack(pady=5)
        tk.Label(select_frame, text="Pilih Input:", font=("Verdana", 11)).pack(side=tk.LEFT)
        self.input_var = tk.StringVar()
        self.input_var.set(self.input_files[0] if self.input_files else "")
        self.dropdown = tk.OptionMenu(select_frame, self.input_var, *self.input_files)
        self.dropdown.pack(side=tk.LEFT, padx=5)
        self.btn_load = tk.Button(select_frame, text="Load Input", command=self.load_input, bg="#DDDDDD")
        self.btn_load.pack(side=tk.LEFT, padx=5)
        self.btn_start = tk.Button(self.root, text="Start Solving", command=self.start_solving, bg="#DDDDDD", state=tk.DISABLED)
        self.btn_start.pack(pady=10)
        self.btn_save = tk.Button(self.root, text="Save Solution", command=self.save_solution, bg="#DDDDDD", state=tk.DISABLED)
        self.btn_save.pack(pady=5)

    def load_input(self):
        file_name = self.input_var.get()
        file_path = os.path.join(os.getcwd(), 'input', file_name)
        self.board_data = Logic.parse_board_from_txt(file_path)

        # Validasi input
        if not Logic.validate_board(self.board_data):
            messagebox.showerror("Input Invalid")
            self.board_data = None
            self.draw_board([])
            self.btn_start.config(state=tk.DISABLED)
            return
        
        self.rows = len(self.board_data)
        self.cols = len(self.board_data[0])
        self.canvas.config(width=self.cell_size * self.cols, height=self.cell_size * self.rows)
        self.solver = Logic(self.board_data)
        self.solver_iterator = None
        self.running = False
        self.algo_time_ms = 0.0
        self.iterations = 0
        self.lbl_iter.config(text="Jumlah Iterasi: 0")
        self.lbl_time.config(text="Waktu Pencarian: 0.00 ms")
        self.draw_board([])
        self.btn_start.config(state=tk.NORMAL)

    def draw_board(self, queen_positions):
        self.canvas.delete("all")
        if not self.board_data:
            return
        queen_set = set(queen_positions)
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                char = self.board_data[r][c]
                color = self.color_map.get(char, '#FFFFFF')
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                if (r, c) in queen_set:
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text="♕", fill="black", font=("Verdana", 18))
                else:
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=char, fill="#555555", font=("Courier", 14))

    def start_solving(self):
        if not self.running and self.solver:
            self.running = True
            self.algo_time_ms = 0.0
            self.solver_iterator = self.solver.solve_generator()
            self.btn_start.config(state=tk.DISABLED)
            self.run_batch()

    def run_batch(self):
        BATCH_SIZE = 1000
        t_start = time.perf_counter()
        positions = []
        try:
            for _ in range(BATCH_SIZE):
                positions, count, is_solution = next(self.solver_iterator)
                self.iterations = count
                if is_solution:
                    t_end = time.perf_counter()
                    self.algo_time_ms += (t_end - t_start) * 1000
                    self.finish_game(positions, success=True)
                    return
            t_end = time.perf_counter()
            self.algo_time_ms += (t_end - t_start) * 1000
            self.lbl_iter.config(text=f"Jumlah Iterasi: {self.iterations}")
            self.lbl_time.config(text=f"Waktu Pencarian: {self.algo_time_ms:.2f} ms")
            self.draw_board(positions)
            self.root.after(1, self.run_batch)
        except StopIteration:
            t_end = time.perf_counter()
            self.algo_time_ms += (t_end - t_start) * 1000
            self.finish_game(positions, success=False)

    def finish_game(self, positions, success):
        self.lbl_iter.config(text=f"Jumlah Iterasi: {self.iterations}")
        self.lbl_time.config(text=f"Waktu Pencarian: {self.algo_time_ms:.2f} ms")

        for widget in self.root.pack_slaves():
            if isinstance(widget, tk.Message):
                widget.destroy()
        self.draw_board(positions)
        if success:
            tk.Message(self.root, text=f"Solusi ditemukan!", width=300).pack()
            self.btn_save.config(state=tk.NORMAL)
            self.solution_positions = positions
        else:
            tk.Message(self.root, text="Tidak ada solusi ditemukan.", width=300).pack()
            self.btn_save.config(state=tk.DISABLED)
            self.solution_positions = []
        self.running = False
        self.btn_start.config(state=tk.DISABLED)
    
    def save_solution(self):
        if not hasattr(self, "solution_positions") or not self.solution_positions:
            return
        output_dir = os.path.join(os.getcwd(), "test")
        os.makedirs(output_dir, exist_ok=True)
        input_name = self.input_var.get().rsplit(".", 1)[0]
        txt_path = os.path.join(output_dir, f"{input_name}_solution.txt")
        jpg_path = os.path.join(output_dir, f"{input_name}_solution.jpg")

        board = [list(row) for row in self.board_data]
        for r, c in self.solution_positions:
            board[r][c] = '#'
        with open(txt_path, "w") as f:
            for row in board:
                f.write(''.join(row) + '\n')
        self.save_canvas_as_jpg(jpg_path)

    def save_canvas_as_jpg(self, path):
        try:
            x1 = self.info_frame.winfo_rootx()
            y1 = self.info_frame.winfo_rooty()
            w1 = self.info_frame.winfo_width()
            h1 = self.info_frame.winfo_height()
            x2 = self.canvas.winfo_rootx()
            y2 = self.canvas.winfo_rooty()
            w2 = self.canvas.winfo_width()
            h2 = self.canvas.winfo_height()

            left = min(x1, x2)
            right = max(x1 + w1, x2 + w2)
            top = min(y1, y2)
            bottom = max(y1 + h1, y2 + h2)
            width = right - left
            height = bottom - top
            img = pyautogui.screenshot(region=(left, top, width, height))
            img.save(path, 'JPEG')
        except ImportError:
            messagebox.showerror("Error", "library belum di-install. Install dengan 'pip install pyautogui pillow'.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan gambar: {e}")