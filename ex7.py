## EX7 - python connect-N ##
EMPTY = '.'
P1 = 'X'
P2 = 'O'
HUMAN = 1
COMPUTER = 2

DIRS = [(0, 1), (1, 0), (1, 1), (1, -1)]

def compute_connect_n(rows, cols):
    # Tic-Tac-Toe mode is handled separately (board must be 3x3)
    if rows == 3 or cols == 3:
        return None  # signal: tic-tac-toe mode

    if rows == 2 or cols == 2:
        return 2

    m = max(rows, cols)
    if 4 <= m <= 5:
        return 3
    if 6 <= m <= 10:
        return 4
    return 5


def init_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    print()
    for r in board:
        print("|" + "|".join(r) + "|")
    # column numbers like ex3
    print(" " + " ".join(str((c+1) % 10) for c in range(cols)))
    print()

def get_player_type(player_num):
    while True:
        ch = input(f"Choose type for player {player_num}: h - human, c - computer: ").strip()
        if ch.lower() == 'h':
            return HUMAN
        if ch.lower() == 'c':
            return COMPUTER
        print("Invalid selection. Enter h or c.")

def is_column_full(board, col):
    return board[0][col] != EMPTY

def is_board_full(board):
    return all(cell != EMPTY for cell in board[0])

def get_free_row(board, col):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return -1

def make_move(board, col, token):
    r = get_free_row(board, col)
    if r == -1:
        return -1
    board[r][col] = token
    return r

def in_bounds(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])

def check_victory(board, last_r, last_c, token, connect_n):
    for dr, dc in DIRS:
        count = 1
        r, c = last_r + dr, last_c + dc
        while in_bounds(board, r, c) and board[r][c] == token:
            count += 1
            r += dr; c += dc
        r, c = last_r - dr, last_c - dc
        while in_bounds(board, r, c) and board[r][c] == token:
            count += 1
            r -= dr; c -= dc
        if count >= connect_n:
            return True
    return False

def central_order(i, cols):
    # center-first ordering כמו ב-C
    if cols % 2 == 1:
        center = cols // 2
        if i == 0:
            return center
        if i % 2 == 1:
            return center - (i + 1) // 2
        return center + i // 2
    else:
        left_mid = cols // 2 - 1
        right_mid = cols // 2
        if i == 0:
            return left_mid
        if i == 1:
            return right_mid
        offset = (i - 2) // 2 + 1
        if i % 2 == 0:
            return left_mid - offset
        return right_mid + offset


def creates_k_in_a_row(board, rows, cols, test_col, token, k):
    # "simulate" drop in column, check if it makes >=k in a row (without permanently changing board)
    if is_column_full(board, test_col):
        return False

    r = get_free_row(board, test_col)
    board[r][test_col] = token

    ok = False
    for dr, dc in DIRS:
        count = 1

        rr, cc = r + dr, test_col + dc
        while in_bounds(board, rr, cc) and board[rr][cc] == token:
            count += 1
            rr += dr
            cc += dc

        rr, cc = r - dr, test_col - dc
        while in_bounds(board, rr, cc) and board[rr][cc] == token:
            count += 1
            rr -= dr
            cc -= dc

        if count >= k:
            ok = True
            break

    board[r][test_col] = EMPTY
    return ok


def computer_choose(board, rows, cols, computer_token, human_token, connect_n):
    # 1) win now
    for i in range(cols):
        c = central_order(i, cols)
        if is_column_full(board, c):
            continue
        r = get_free_row(board, c)
        board[r][c] = computer_token
        if check_victory(board, r, c, computer_token, connect_n):
            board[r][c] = EMPTY
            return c
        board[r][c] = EMPTY

    # 2) block human win
    for i in range(cols):
        c = central_order(i, cols)
        if is_column_full(board, c):
            continue
        r = get_free_row(board, c)
        board[r][c] = human_token
        if check_victory(board, r, c, human_token, connect_n):
            board[r][c] = EMPTY
            return c
        board[r][c] = EMPTY

    # 3) create (connect_n-1) in a row (heuristic)
    target = max(2, connect_n - 1)
    for i in range(cols):
        c = central_order(i, cols)
        if creates_k_in_a_row(board, rows, cols, c, computer_token, target):
            return c

    # 4) block human (connect_n-1)
    for i in range(cols):
        c = central_order(i, cols)
        if creates_k_in_a_row(board, rows, cols, c, human_token, target):
            return c

    # 5) fallback: first available by center priority
    for i in range(cols):
        c = central_order(i, cols)
        if not is_column_full(board, c):
            return c

    return 0


def human_choose(board, cols):
    while True:
        s = input(f"Enter column (1-{cols}): ").strip()
        if not s.isdigit():
            print("Invalid input. Enter a number.")
            continue
        col = int(s) - 1
        if col < 0 or col >= cols:
            print(f"Invalid column. Choose between 1 and {cols}.")
            continue
        if is_column_full(board, col):
            print(f"Column {col+1} is full. Choose another column.")
            continue
        return col

def print_board_ttt(board):
    # Prints the 3x3 Tic-Tac-Toe board
    print()
    for r in board:
        print("|" + "|".join(r) + "|")
    print()


def ttt_choose_cell():
    # Ask the user to choose a cell between 1 and 9
    # According to instructions, we can assume the user won't choose an already taken cell
    while True:
        s = input("Enter cell (1-9): ").strip()

        if not s.isdigit():
            print("Invalid input. Enter a number.")
            continue

        cell = int(s)

        if cell < 1 or cell > 9:
            print("Invalid cell. Choose between 1 and 9.")
            continue

        return cell


def run_tic_tac_toe():
    # In this mode the board is always 3x3
    rows = cols = 3
    board = init_board(rows, cols)

    print("Tic-Tac-Toe (3x3)")
    print_board_ttt(board)

    current = 1

    while True:
        token = P1 if current == 1 else P2
        print(f"Player {current} ({token}) turn.")

        # Get chosen cell (1-9)
        cell = ttt_choose_cell()

        # Convert cell number to row and column
        r = (cell - 1) // 3
        c = (cell - 1) % 3

        # Place token
        board[r][c] = token

        print_board_ttt(board)

        # Check victory (3 in a row)
        if check_victory(board, r, c, token, 3):
            print(f"Player {current} ({token}) wins!")
            return

        # Check tie (no empty cells left)
        if all(board[rr][cc] != EMPTY for rr in range(3) for cc in range(3)):
            print("Board full and no winner. It's a tie!")
            return

        # Switch player
        current = 2 if current == 1 else 1

def run_connect_n(rows, cols):
    connect_n = compute_connect_n(rows, cols)
    board = init_board(rows, cols)

    print(f"Connect-N ({rows} rows x {cols} cols)\n")
    p1_type = get_player_type(1)
    p2_type = get_player_type(2)

    print_board(board, cols)

    current = 1
    while not is_board_full(board):
        token = P1 if current == 1 else P2
        ptype = p1_type if current == 1 else p2_type

        print(f"Player {current} ({token}) turn.")

        if ptype == HUMAN:
            col = human_choose(board, cols)
        else:
            other_token = P2 if token == P1 else P1
            col = computer_choose(board, rows, cols, token, other_token, connect_n)
            print(f"Computer chose column {col+1}")

        row = make_move(board, col, token)
        print_board(board, cols)

        if check_victory(board, row, col, token, connect_n):
            print(f"Player {current} ({token}) wins!")
            return

        current = 2 if current == 1 else 1

    print("Board full and no winner. It's a tie!")


def main():
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))

    if rows < 2 or rows > 100 or cols < 2 or cols > 100:
        print("Invalid board size.")
        return

    # If either dimension is 3 -> Tic-Tac-Toe mode
    if rows == 3 or cols == 3:
        run_tic_tac_toe()
        return

    run_connect_n(rows, cols)


if __name__ == "__main__":
    main()
