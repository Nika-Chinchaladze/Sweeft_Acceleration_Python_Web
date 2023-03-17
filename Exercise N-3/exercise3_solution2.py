# ======================================== BOMBER FUNCTION ================================== #
def bomber_man(n: int, grid: list):
    if n == 1:
        return grid

    r = len(grid)
    c = len(grid[0])

    # all locations will be filled with bombs:
    if n % 2 == 0:
        return ["O"*c for i in range(r)]

    # another cases:
    n //= 2
    for item in range((n+1) % 2 + 1):
        new_grid = [["O"]*c for i in range(r)]

        # explosion function:
        def bombs_explosion(p, q):
            if 0 <= p < r and 0 <= q < c:
                new_grid[p][q] = "."

        increment_position_x = [0, 0, 0, 1, -1]
        increment_position_y = [0, -1, 1, 0, 0]

        for x in range(r):
            for y in range(c):
                # check bomb existence
                if grid[x][y] == "O":
                    for i, j in zip(increment_position_x, increment_position_y):
                        bombs_explosion(p=x+i, q=y+j)

        grid = new_grid

    return ["".join(member) for member in grid]


# ====================================== GENERATE GRID FROM INPUT ================================== #
try:
    my_time = int(input("Enter Whole Time: "))
    my_row = int(input("Enter Number Of Rows: "))
    my_column = int(input("Enter Number Of Columns: "))

    my_grid = []
    my_level = 1
    for outer_item in range(my_row):
        my_string = ""
        for letter in range(my_column):
            entered_symbol = input(f"{my_level}.{letter+1}) Enter . for empty field or O for Bomb! ").rstrip().upper()
            if entered_symbol in [".", "O"]:
                my_string += entered_symbol
            else:
                my_string += "."

        my_level += 1
        my_grid.append(my_string)

    answer = bomber_man(n=my_time, grid=my_grid)
    print(answer)

except ValueError:
    print("Please Enter Only Integers for => my_time, my_row and my_column inputs! ")
