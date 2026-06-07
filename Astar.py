import time
from queue import PriorityQueue

import sokoban as spf


# A* Tim duong di cho Sokoban.
def AStart_Search(board, list_check_point, timeout_limit=None, max_expanded_states=250000):
    start_time = time.time()
    if spf.check_win(board, list_check_point):
        print('Found win')
        return [board]

    def board_to_key(src_board):
        return tuple(tuple(row) for row in src_board)

    start_state = spf.state(board, None, list_check_point)
    start_state.cost = 0

    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)

    best_cost = {board_to_key(start_state.board): 0}
    expanded_states = 0

    if timeout_limit is None:
        timeout_limit = getattr(spf, 'TIME_OUT', getattr(spf, 'TIMEOUT', 120))

    while not heuristic_queue.empty():
        if time.time() - start_time > timeout_limit:
            print(f'Timeout after {timeout_limit}s, expanded={expanded_states}')
            return []
        if expanded_states >= max_expanded_states:
            print(f'Stopped after max expanded states={max_expanded_states}')
            return []

        now_state = heuristic_queue.get()
        now_key = board_to_key(now_state.board)

        # Skip if we already have a cheaper path to this state.
        if now_state.cost > best_cost.get(now_key, float('inf')):
            continue

        expanded_states += 1
        cur_pos = spf.find_position_player(now_state.board)
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)

        for next_pos in list_can_move:
            move_fn = getattr(spf, 'move', None) or getattr(spf, 'apply_move', None) or getattr(spf, 'make_move', None)
            if move_fn is None:
                raise AttributeError('sokoban module has no move/apply_move/make_move function')

            new_board = move_fn(now_state.board, next_pos, cur_pos, list_check_point)

            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_cost = now_state.cost + 1
            new_key = board_to_key(new_board)
            if new_cost >= best_cost.get(new_key, float('inf')):
                continue

            new_state = spf.state(new_board, now_state, list_check_point)
            new_state.cost = new_cost
            best_cost[new_key] = new_cost

            if spf.check_win(new_board, list_check_point):
                print('Found win')
                return (new_state.get_line(), expanded_states)

            heuristic_queue.put(new_state)

    print('Not Found')
    return []
