class Grid:
    def __init__(self, data, vertical=False):
            self._rows = len(data)
            if isinstance(data, list) and isinstance(data[0], list):
                self._grid = [row[:] for row in data]
                self._cols = len(data[0]) if data else 0
            elif isinstance(data, list) and isinstance(data[0], str):
                self._cols = len(data[0].strip()) if data else 0
                self._grid = [list((row.strip())) for row in data]
            else:
                raise ValueError("Invalid data format. Must be a list of lists or a list of strings.")
            if vertical:
                self.transpose_in_place()

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def grid(self):
        return self._grid
    
    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self._grid])

    def __eq__(self, other):
        if not isinstance(other, Grid):
            return False

        if self._rows != other.rows or self._cols != other.cols:
            return False

        for i in range(self._rows):
            for j in range(self._cols):
                if self._grid[i][j] != other.grid[i][j]:
                    return False
        return True

    def __getitem__(self, idx):
        if isinstance(idx, tuple) and len(idx) == 2:
            row, col = idx
            return self._grid[row][col]
        else:
            return self._grid[idx]

    def __setitem__(self, idx, value):
        if isinstance(idx, tuple) and len(idx) == 2:
            row, col = idx
            self._grid[row][col] = value
        else:
            self._grid[idx] = value

    def get_row(self, row_idx):
        return self._grid[row_idx]

    def get_column(self, col_idx):
        return [row[col_idx] for row in self._grid]

    def set_row(self, row_idx, new_row):
        if len(new_row) == self._cols:
            self._grid[row_idx] = new_row
        else:
            raise ValueError(f"Row must have {self._cols} elements.")

    def set_column(self, col_idx, new_column):
        if len(new_column) == self._rows:
            for i in range(self._rows):
                self._grid[i][col_idx] = new_column[i]
        else:
            raise ValueError(f"Column must have {self._rows} elements.")

    def transpose(self):
        transposed_data = [[self._grid[j][i] for j in range(self._rows)] for i in range(self._cols)]
        return Grid(transposed_data)
    
    def transpose_in_place(self):
        self._grid = [[self._grid[j][i] for j in range(self._rows)] for i in range(self._cols)]
        self._rows, self._cols = self._cols, self._rows
    
    def get_columns(self):
        return [self.get_column(i) for i in range(self._cols)]

    def from_columns(self, columns):
        for col_idx, col in enumerate(columns):
            self.set_column(col_idx, col)
        return self
    
    def get_rows(self):
        return [self.get_row(i) for i in range(self._rows)]