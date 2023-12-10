import torch
import os

nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
symbols = set()
with open('input.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        for char in line.strip():
            if char not in nums:
                symbols.add(char)


def read_data(file_path: str) -> torch.Tensor:
    """
    Read data from a file and store it in a 140x140 tensor.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Initialize a 140x140 tensor to store characters
    tensor = torch.zeros((140, 140), dtype=torch.int8)

    for i, line in enumerate(lines):
        for j, char in enumerate(line.strip()):
            tensor[i][j] = ord(char)

    return tensor


def get_adjacent_cells(i: int, j: int, length: int, rows: int, cols: int) -> set:
    """
    Get all adjacent cells for a number of given length, including diagonals.
    """
    adjacent_cells = set()

    # Cells before the number
    if j > 0:
        for x in range(i - 1, i + 2):
            if 0 <= x < rows:
                adjacent_cells.add((x, j - 1))
        # Add diagonal cells at the beginning of the line
        if i > 0:
            adjacent_cells.add((i - 1, j - 1))
        if i < rows - 1:
            adjacent_cells.add((i + 1, j - 1))

    # Cells after the number
    if j + length < cols:
        for x in range(i - 1, i + 2):
            if 0 <= x < rows:
                adjacent_cells.add((x, j + length))
        # Add diagonal cells at the end of the line
        if i > 0:
            adjacent_cells.add((i - 1, j + length))
        if i < rows - 1:
            adjacent_cells.add((i + 1, j + length))

    # Cells above and below the number
    for offset in range(length):
        if i > 0:
            adjacent_cells.add((i - 1, j + offset))
        if i < rows - 1:
            adjacent_cells.add((i + 1, j + offset))

    return adjacent_cells


def find_valid_numbers(tensor: torch.Tensor) -> set:
    """
    Find multi-digit numbers that have at least one adjacent cell with a character other than '.'.
    """
    rows, cols = tensor.shape
    valid_numbers = []
    not_valid = []
    for i in range(rows):
        j = 0
        while j < cols:
            if chr(tensor[i, j].item()).isdigit():
                start_j = j
                # Find the end of the number
                while j < cols and chr(tensor[i, j].item()).isdigit():
                    j += 1
                num_len = j - start_j
                number = int(''.join(chr(tensor[i, k].item()) for k in range(start_j, j)))
                # Get adjacent cells
                adjacent_cells = get_adjacent_cells(i, start_j, num_len, rows, cols)
                o = 1
                for x, y in adjacent_cells:
                    charac = chr(tensor[x, y].item())
                    if charac in symbols:
                        valid_numbers.append(number)
                        o = 1
                        break
                    else:
                        o = 0
                if o == 0:
                    # no adjacent symbol
                    not_valid.append(number)
            else:
                j += 1

    return valid_numbers, not_valid


# # Read data from file
file_path = 'input.txt'
tensor = read_data(file_path)

# Find valid numbers
valid_numbers, not_valid = find_valid_numbers(tensor)

final = 0
for val in valid_numbers:
    final += val

print(f"There are {len(not_valid)} numbers that are not valid part numbers.")
print(f"However, ")
print(f"There are {len(valid_numbers)} part numbers that ARE valid!")
_test = str(valid_numbers[:10])[:-1] + " ... " + str(valid_numbers[-10:])[1:]
print(_test)
print(f"The sum of all valid part numbers is {final}.")