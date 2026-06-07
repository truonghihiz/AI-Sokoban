from copy import deepcopy

class state:
    def __init__(self, board, state_parent, list_check_point):
        '''storage current board and state parent of this state'''
        self.board = board
        self.state_parent = state_parent
        self.cost = 1
        self.heuristic = 0
        self.check_points = deepcopy(list_check_point)


    #Hàm đệ quy để quay lại về đầu tiên nếu trạng thái hiện tại là mục tiêu
    def get_line(self):
        if self.state_parent is None:
            return [self.board]
        return (self.state_parent).get_line() + [self.board]


    #Tính toán hàm heuristic được sử dụng cho thuật toán a*
    def compute_heuristic(self):
        list_boxes = find_boxes_position(self.board)
        if self.heuristic == 0:
            self.heuristic = self.cost + abs(sum(
                list_boxes[i][0] + list_boxes[i][1] - self.check_points[i][0]
                - self.check_points[i][1] for i in range(len(list_boxes))
            ))
        return self.heuristic

    #Hoạt động quá tải rằng cho phép các bang được lưu trữ trong hàng ưu tiên
    def __gt__(self, other):
        if self.compute_heuristic() > other.compute_heuristic():
            return True
        else:
            return False

    def __lt__(self, other):
        if self.compute_heuristic() < other.compute_heuristic():
            return True
        else:
            return False

def check_win(board, list_check_point):
    for p in list_check_point:
        if board[p[0]][p[1]] != '$':
            return False
    return True


def assign_matrix(board):
    return [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]


def find_position_player(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '@':
                return (x, y)
    return (-1, -1)


def compare_matrix(board_A, board_B):
    if len(board_A) != len(board_B) or len(board_A[0]) != len(board_B[0]):
        return False
    for i in range(len(board_A)):
        for j in range(len(board_A[0])):
            if board_A[i][j] != board_B[i][j]:
                return False
    return True


def is_board_exist(board, list_state):
    for state in list_state:
        if compare_matrix(state.board, board):
            return True
    return False


def is_box_on_check_point(box, list_check_point):
 # ktra một điểm có nằm trong danh sách điểm hay k
    for check_point in list_check_point:
        if box[0] == check_point[0] and box[1] == check_point[1]:
            return True
    return False


def check_in_corner(board, x, y, list_check_point):
    # Avoid out-of-range access for boxes near map borders.
    if x <= 0 or y <= 0 or x >= len(board) - 1 or y >= len(board[0]) - 1:
        return False

    if board[x-1][y-1] == '#':
        if board[x-1][y] == '#' and board[x][y-1] == '#':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x+1][y-1] == '#':
        if board[x+1][y] == '#' and board[x][y-1] == '#':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x-1][y+1] == '#':
        if board[x-1][y] == '#' and board[x][y+1] == '#':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    if board[x+1][y+1] == '#':
        if board[x+1][y] == '#' and board[x][y+1] == '#':
            if not is_box_on_check_point((x, y), list_check_point):
                return True
    return False


def find_boxes_position(board):
    result = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '$':
                result.append((i, j))
    return result


def is_box_can_be_moved(board, box_position):
    def is_open(cell):
        return cell in (' ', '%', '@')

    def in_bounds(x, y):
        return 0 <= x < len(board) and 0 <= y < len(board[0])

    left_move = (box_position[0], box_position[1] - 1)
    right_move = (box_position[0], box_position[1] + 1)
    up_move = (box_position[0] - 1, box_position[1])
    down_move = (box_position[0] + 1, box_position[1])

    if in_bounds(*left_move) and in_bounds(*right_move) and is_open(board[left_move[0]][left_move[1]]) and board[right_move[0]][right_move[1]] not in ('#', '$'):
        return True
    if in_bounds(*right_move) and in_bounds(*left_move) and is_open(board[right_move[0]][right_move[1]]) and board[left_move[0]][left_move[1]] not in ('#', '$'):
        return True
    if in_bounds(*up_move) and in_bounds(*down_move) and is_open(board[up_move[0]][up_move[1]]) and board[down_move[0]][down_move[1]] not in ('#', '$'):
        return True
    if in_bounds(*down_move) and in_bounds(*up_move) and is_open(board[down_move[0]][down_move[1]]) and board[up_move[0]][up_move[1]] not in ('#', '$'):
        return True
    return False


def is_all_boxes_stuck(board, list_check_point):
    box_positions = find_boxes_position(board)
    result = True
    for box_position in box_positions:
        if is_box_on_check_point(box_position, list_check_point):
            return False
        if is_box_can_be_moved(board, box_position):
            result = False
    return result


def is_board_can_not_win(board, list_check_point):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '$':
                if check_in_corner(board, x, y, list_check_point):
                    return True
    return False


def get_next_pos(board, cur_pos):
    x, y = cur_pos[0], cur_pos[1]
    list_can_move = []

    if 0 <= x - 1 < len(board):
        value = board[x - 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x - 1, y))
        elif value == '$' and 0 <= x - 2 < len(board):
            next_pos_box = board[x - 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x - 1, y))
    if 0 <= x + 1 < len(board):
        value = board[x + 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x + 1, y))
        elif value == '$' and 0 <= x + 2 < len(board):
            next_pos_box = board[x + 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x + 1, y))

    if 0 <= y - 1 < len(board[0]):
        value = board[x][y - 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y - 1))
        elif value == '$' and 0 <= y - 2 < len(board[0]):
            next_pos_box = board[x][y - 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y - 1))
    if 0 <= y + 1 < len(board[0]):
        value = board[x][y + 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y + 1))
        elif value == '$' and 0 <= y + 2 < len(board[0]):
            next_pos_box = board[x][y + 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y + 1))
    return list_can_move


def find_list_check_point(board):
    list_check_point = []
    num_of_box = 0
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '$':
                num_of_box += 1
            elif board[x][y] == '%':
                list_check_point.append((x, y))
    if num_of_box < len(list_check_point):
        return [(-1, -1)]
    return list_check_point


def move(board, next_pos, cur_pos, list_check_point):
    new_board = assign_matrix(board)

    nx, ny = next_pos
    px, py = cur_pos

    if new_board[nx][ny] == '#':
        return new_board

    if new_board[nx][ny] == '$':
        bx, by = nx + (nx - px), ny + (ny - py)
        if not (0 <= bx < len(new_board) and 0 <= by < len(new_board[0])):
            return new_board
        if new_board[bx][by] in ('#', '$'):
            return new_board
        new_board[bx][by] = '$'

    if (px, py) in list_check_point:
        new_board[px][py] = '%'
    else:
        new_board[px][py] = ' '

    new_board[nx][ny] = '@'
    return new_board
