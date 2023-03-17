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


field = [
    ".......",
    "...O...",
    "....O..",
    ".......",
    "OO.....",
    "OO....."
]

answer = bomber_man(n=3, grid=field)
print(answer)
