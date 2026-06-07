import os
import pygame

import Astar
from sokoban import (
    assign_matrix,
    check_win,
    find_list_check_point,
    find_position_player,
    get_next_pos,
    move,
)

pygame.init()
pygame.font.init()

SCREEN_SIZE = (640, 640)
MAX_TILE_SIZE = 56
MIN_TILE_SIZE = 28
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Sokoban')
clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, 'Assets_sokoban')


def load_image(*parts):
    path = os.path.join(ASSET_DIR, *parts)
    return pygame.image.load(path).convert_alpha()


person = load_image('player_05.png')
wall = load_image('block_04.png')
box0 = load_image('crate_07.png')
box1 = load_image('crate_10.png')
target = load_image('environment_03.png')
floor_tile = load_image('ground_06.png')

MAPS_RAW = [
    [
        '########',
        '#  %   #',
        '#  $   #',
        '#  @   #',
        '########',
    ],
    [
        '#########',
        '#   %   #',
        '#   $   #',
        '#  #@   #',
        '#  $    #',
        '#   %   #',
        '#########',
    ],
    [
        '#########',
        '#####@# #',
        '#####$% #',
        '#   $   #',
        '#   % $%#',
        '#       #',
        '#########',
    ],
    [
        '#########',
        '#%@ #####',
        '#$$######',
        '#   #####',
        '# $ #####',
        '#  ######',
        '# #######',
        '#% ######',
        '#% ######',
        '#########',
    ]

]


def parse_map(rows):
    return [list(r) for r in rows]


maps = [parse_map(m) for m in MAPS_RAW]
check_points = [find_list_check_point(m) for m in maps]

running = True
scene_state = 'init'
map_number = 0
algorithm = 'Player'
list_board = []
state_length = 0
current_state = 0
ai_error_message = ''


font_title = pygame.font.Font(None, 64)
font_body = pygame.font.Font(None, 28)
font_small = pygame.font.Font(None, 24)


def draw_text(text, font, color, center):
    label = font.render(text, True, color)
    rect = label.get_rect(center=center)
    screen.blit(label, rect)


def get_tile_size(board):
    width = len(board[0])
    height = len(board)
    # Keep board inside panel and preserve footer/header space.
    max_w = 560
    max_h = 350
    by_w = max_w // width
    by_h = max_h // height
    return max(MIN_TILE_SIZE, min(MAX_TILE_SIZE, by_w, by_h))


def get_scaled_sprites(tile_size):
    return {
        'person': pygame.transform.scale(person, (tile_size, tile_size)),
        'wall': pygame.transform.scale(wall, (tile_size, tile_size)),
        'box0': pygame.transform.scale(box0, (tile_size, tile_size)),
        'box1': pygame.transform.scale(box1, (tile_size, tile_size)),
        'target': pygame.transform.scale(target, (tile_size, tile_size)),
        'floor': pygame.transform.scale(floor_tile, (tile_size, tile_size)),
    }


def draw_background():
    screen.fill((24, 28, 36))
    pygame.draw.rect(screen, (36, 41, 52), pygame.Rect(28, 28, 584, 584), border_radius=12)
    pygame.draw.rect(screen, (75, 85, 105), pygame.Rect(28, 28, 584, 584), width=2, border_radius=12)


def render_map(board):
    tile_size = get_tile_size(board)
    sprites = get_scaled_sprites(tile_size)
    width = len(board[0])
    height = len(board)
    indent_x = (SCREEN_SIZE[0] - width * tile_size) // 2
    indent_y = 215

    for i in range(height):
        for j in range(width):
            x = j * tile_size + indent_x
            y = i * tile_size + indent_y
            screen.blit(sprites['floor'], (x, y))

            cell = board[i][j]
            if cell == '#':
                screen.blit(sprites['wall'], (x, y))
            elif cell == '$':
                if (i, j) in check_points[map_number]:
                    screen.blit(sprites['box1'], (x, y))
                else:
                    screen.blit(sprites['box0'], (x, y))
            elif cell == '%':
                screen.blit(sprites['target'], (x, y))
            elif cell == '@':
                screen.blit(sprites['person'], (x, y))


def draw_init_scene():
    draw_background()
    draw_text('SOKOBAN', font_title, WHITE, (320, 70))
    draw_text('Left/Right: Level', font_body, WHITE, (320, 125))
    draw_text('Tab: Player/AI   Enter: Start', font_body, WHITE, (320, 160))
    draw_text(f'Level: {map_number + 1}/{len(maps)}', font_body, WHITE, (320, 195))
    draw_text(f'Mode: {algorithm}', font_body, WHITE, (320, 600))
    render_map(maps[map_number])


def draw_loading_scene():
    draw_background()
    draw_text('LOADING...', font_title, WHITE, (320, 320))


def draw_end_scene(found):
    draw_background()
    draw_text('WIN!' if found else 'NOT FOUND', font_title, WHITE, (320, 70))
    draw_text('Enter: Back to menu', font_body, WHITE, (320, 600))
    if ai_error_message:
        draw_text(ai_error_message[:60], font_small, WHITE, (320, 560))

    if algorithm == 'AI' and list_board:
        render_map(list_board[0][state_length - 1])
    else:
        render_map(maps[map_number])


def execute_ai():
    global scene_state, list_board, state_length, current_state, ai_error_message
    list_check_point = check_points[map_number]
    ai_error_message = ''
    try:
        list_board = Astar.AStart_Search(
            assign_matrix(maps[map_number]),
            list_check_point,
            180, 
            300000,
        )
    except Exception as ex:
        print(f'AI error: {ex}')
        list_board = []
        ai_error_message = f'AI error: {ex}'

    if list_board and len(list_board[0]) > 0:
        scene_state = 'playing'
        state_length = len(list_board[0])
        current_state = 0
    else:
        scene_state = 'end'


def handle_player_move(key):
    cur_board = maps[map_number]
    cur_pos = find_position_player(cur_board)
    candidates = get_next_pos(cur_board, cur_pos)

    dx, dy = 0, 0
    if key == pygame.K_UP:
        dx, dy = -1, 0
    elif key == pygame.K_DOWN:
        dx, dy = 1, 0
    elif key == pygame.K_LEFT:
        dx, dy = 0, -1
    elif key == pygame.K_RIGHT:
        dx, dy = 0, 1
    else:
        return

    target_pos = (cur_pos[0] + dx, cur_pos[1] + dy)
    if target_pos in candidates:
        maps[map_number] = move(cur_board, target_pos, cur_pos, check_points[map_number])


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if scene_state == 'init':
                if event.key == pygame.K_RIGHT and map_number < len(maps) - 1:
                    map_number += 1
                elif event.key == pygame.K_LEFT and map_number > 0:
                    map_number -= 1
                elif event.key == pygame.K_TAB:
                    algorithm = 'AI' if algorithm == 'Player' else 'Player'
                elif event.key == pygame.K_RETURN:
                    # Reset current map state before each run.
                    maps[map_number] = parse_map(MAPS_RAW[map_number])
                    scene_state = 'loading'

            elif scene_state == 'playing':
                if algorithm == 'Player':
                    handle_player_move(event.key)
                    if check_win(maps[map_number], check_points[map_number]):
                        scene_state = 'end'

            elif scene_state == 'end':
                if event.key == pygame.K_RETURN:
                    scene_state = 'init'

    if scene_state == 'init':
        draw_init_scene()
    elif scene_state == 'loading':
        draw_loading_scene()
        pygame.display.flip()
        if algorithm == 'AI':
            execute_ai()
        else:
            scene_state = 'playing'
        continue
    elif scene_state == 'playing':
        draw_background()
        if algorithm == 'AI':
            clock.tick(4)
            render_map(list_board[0][current_state])
            current_state += 1
            if current_state >= state_length:
                scene_state = 'end'
        else:
            clock.tick(30)
            render_map(maps[map_number])
            draw_text('Arrow keys to move boxes to targets', font_small, WHITE, (320, 590))
    elif scene_state == 'end':
        solved = check_win(maps[map_number], check_points[map_number]) if algorithm == 'Player' else bool(list_board)
        draw_end_scene(solved)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
