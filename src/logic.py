class Logic:
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.colors = self._get_colors()
    
    def _get_colors(self):
        s = set()
        for row in self.board:
            for c in row:
                s.add(c)
        return list(s)

    def parse_board_from_txt(file_path):
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
        return lines
    
    def validate_board(board):
        n_row = len(board)
        n_col = len(board[0]) if board else 0
        colors = set()
        for row in board:
            if len(row) != n_col:
                return False
            for c in row:
                if not ('A' <= c <= 'Z'):
                    return False
                colors.add(c)
        if n_row != n_col:
            return False
        if len(colors) > n_row:
            return False
        return True

    def _permute(self, arr, k):
        if k == 0:
            return [[]]
        result = []
        for i in range(len(arr)):
            remaining = arr[:i] + arr[i+1:]
            for p in self._permute(remaining, k-1):
                result.append([arr[i]] + p)
        return result

    def _comb(self, arr, k):
        result = []
        n = len(arr)
        for mask in range(1 << n): 
            subset = []
            for i in range(n):
                if mask & (1 << i):
                    subset.append(arr[i])
            if len(subset) == k:
                result.append(subset)
        return result

    def _check_rows_cols(self, arr):
        rows = []
        cols = []
        for r, c in arr:
            rows.append(r)
            cols.append(c)
        if (len(rows) == len(set(rows))) and (len(cols) == len(set(cols))):
            return True
        return False

    def _check_distance(self, arr):
        for i in range(len(arr)):
            r1, c1 = arr[i]
            for j in range(i+1, len(arr)):
                r2, c2 = arr[j]
                if abs(r1-r2) <= 1 and abs(c1-c2) <= 1:
                    return False
        return True

    def _check_colors(self, arr):
        seen = []
        for r, c in arr:
            color = self.board[r][c]
            if color in seen:
                return False
            seen.append(color)
        return True
    
    def check_constraint(self, arr):
        return (self._check_rows_cols(arr) and 
                self._check_distance(arr) and 
                self._check_colors(arr))

    def solve_generator(self):
        n = [i for i in range(len(self.board))]
        
        row_combination = self._comb(n, len(self.colors))
        column_combination = self._permute(n, len(self.colors))

        count = 0
        for rows in row_combination:
            for cols in column_combination:
                positions = list(zip(rows, cols))
                count += 1
                
                is_solution = self.check_constraint(positions)
                
                yield positions, count, is_solution
                
                if is_solution:
                    return