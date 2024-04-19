from SimpleQueue import Queue
import copy


"""
Identifies cells in a grid that are 'overflowing'. A cell is considered overflowing if the 
absolute value of its content is greater than or equal to the number of its immediate 
neighbours.

Parameters:
    grid (list of list of int): The grid to check for overflow cells.

Returns:
    list: A list of (row, col) tuples for each overflowing cell. 
    None: If no overflow cells are detected.
"""


def get_overflow_list(grid):
    overflow_list = []  # Initialize an empty list to store coordinates of overflowing cells
    row_count = len(grid)
    col_count = len(grid[0])

    # Iterate over each cell in the grid to check for overflow condition
    for curr_row in range(row_count):
        for curr_col in range(col_count):
            # Get the neighbour count for the cell
            neighbours_count = get_neighbours_count(
                curr_row, curr_col, row_count, col_count)
            # Check if cell is overflowing; if so, add its coordinates to the list
            if abs(grid[curr_row][curr_col]) >= neighbours_count:
                overflow_list.append((curr_row, curr_col))

    # Return the list of overflowing cells or None if the list is empty
    return overflow_list if overflow_list else None


"""
Recursively performs an overflow process in a grid until stability is reached.  Stability 
is reached when all cells have the same sign or no further overflow operations are 
possible.  Each intermediate state of the grid during the overflow process is stored in a_queue.

Parameters:
    grid (list of list of int): The grid to run overflow on.
    a_queue (Queue): A queue object to store the intermediate states of the grid for tracking.

Returns:
    int: The number of overflow iterations performed.
"""


def overflow(grid, a_queue=Queue()):
    # Ensure grid is not empty
    if grid is not None:
        # Get the list of overflowing cells
        overflow_cell_list = get_overflow_list(grid)
        # Proceed if there are any overflowing cells
        if overflow_cell_list is not None:
            # Early exit if all cells already share the same sign
            if not all_signs_equal(grid):
                # Determine the sign of overflow based on the first overflowing cell
                overflow_sign = 1 if grid[overflow_cell_list[0]
                                          [0]][overflow_cell_list[0][1]] > 0 else -1
                # Set all overflowing cells to 0
                for row, col in overflow_cell_list:
                    grid[row][col] = 0
                # Increase the value of neighbour cells based on the overflow sign
                for row, col in overflow_cell_list:
                    increase_neighbour_cells(row, col, grid, overflow_sign)
                # Save the current state of the grid in the queue and recursively call overflow
                a_queue.enqueue(copy.deepcopy(grid))
                return 1 + overflow(grid, a_queue)
        return 0  # Return 0 if no overflow operations were performed


"""
Calculates the number of neighbours for a given cell in a grid.

Parameters:
    row (int): The row index of the cell.
    col (int): The column index of the cell.
    row_count (int): Total number of rows in the grid.
    column_count (int): Total number of columns in the grid.

Returns:
    int: The number of neighbours for the cell.
"""


def get_neighbours_count(row, col, row_count, column_count):
    # Corner cells have 2 neighbours
    if (row == 0 or row == row_count - 1) and (col == 0 or col == column_count - 1):
        return 2
    # Edge but not corner cells have 3 neighbours
    elif row == 0 or row == row_count - 1 or col == 0 or col == column_count - 1:
        return 3
    # Interior cells have 4 neighbours
    else:
        return 4


"""
Checks if all non-zero cells in the grid have the same sign.

Parameters:
    grid (list of list of int): The grid to check.

Returns:
    bool: True if all non-zero cells have the same sign, False otherwise.
"""


def all_signs_equal(grid):
    sign = None
    # Iterate over each cell in the grid
    for row in grid:
        for cell in row:
            # Ignore zero cells
            if cell != 0:
                # Initialize sign for the first non-zero cell
                if sign is None:
                    sign = 1 if cell > 0 else -1
                else:
                    # Check if current cell's sign is different from the initial sign
                    if (sign == 1 and cell < 0) or (sign == -1 and cell > 0):
                        return False
    # Return True if all non-zero cells have the same sign or the grid is empty
    return True


"""
Increases the value of the neighbouring cells of a given cell by 1, adjusting the sign if necessary.

Parameters:
    row (int): Row index of the cell.
    col (int): Column index of the cell.
    grid (list of list of int): The grid to modify.
    sign (int): The sign (+1 or -1) to use for the increment.
"""


def increase_neighbour_cells(row, col, grid, sign):
    row_count = len(grid)
    col_count = len(grid[0])
    to_add = 1 * sign  # Value to add to each neighbour cell

    # If within bounds, adjust neighbouring cells' sign and apply the increment
    if row > 0:
        adjust_cell_sign(row-1, col, grid, sign)
        grid[row-1][col] += to_add
    if row < row_count - 1:
        adjust_cell_sign(row+1, col, grid, sign)
        grid[row+1][col] += to_add
    if col > 0:
        adjust_cell_sign(row, col-1, grid, sign)
        grid[row][col-1] += to_add
    if col < col_count - 1:
        adjust_cell_sign(row, col+1, grid, sign)
        grid[row][col+1] += to_add


"""
Adjusts the sign of a cell's value in the grid, preserving its magnitude.

Parameters:
    row (int): Row index of the cell.
    col (int): Column index of the cell.
    grid (list of list of int): The grid to modify.
    sign (int): The sign (+1 or -1) to apply to the cell's value.
"""


def adjust_cell_sign(row, col, grid, sign):
    # Only adjust non-zero cells
    if grid[row][col] != 0:
        # Adjust sign while preserving magnitude
        grid[row][col] = abs(grid[row][col]) * sign
