import pygame
import sys
import numpy as np

pygame.init()



WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 3
CELL_SIZE = WIDTH // BOARD_SIZE
LINE_WIDTH = 15
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = CELL_SIZE // 4

# Цвета
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (52, 152, 219)
BUTTON_HOVER_COLOR = (41, 128, 185)


PLAYER_X = 1
PLAYER_O = -1
EMPTY = 0
DRAW = 0


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-Нолики")


def initialize_game():
    """Инициализация состояния игры"""
    game_state = {
        'board': np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int),
        'player': PLAYER_X,
        'game_over': False,
        'winner': None,
        'move_count': 0
    }
    return game_state


def draw_board():
    """Отрисовка игрового поля"""
    screen.fill(BG_COLOR)

    # Горизонтальные линии
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, i * CELL_SIZE),
            (WIDTH, i * CELL_SIZE),
            LINE_WIDTH
        )


    for i in range(1, BOARD_SIZE):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, WIDTH),
            LINE_WIDTH
        )


def draw_figures(game_state):
    """Отрисовка крестиков и ноликов"""
    board = game_state['board']

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == PLAYER_X:
                # Рисуем крестик
                start_desc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE)
                end_desc = ((col + 1) * CELL_SIZE - SPACE, (row + 1) * CELL_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

                start_asc = ((col + 1) * CELL_SIZE - SPACE, row * CELL_SIZE + SPACE)
                end_asc = (col * CELL_SIZE + SPACE, (row + 1) * CELL_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

            elif board[row][col] == PLAYER_O:
                # Рисуем нолик
                center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
                radius = CELL_SIZE // 3
                pygame.draw.circle(screen, CIRCLE_COLOR, center, radius, CIRCLE_WIDTH)


def draw_status(game_state):
    """Отрисовка статуса игры"""
    font = pygame.font.SysFont('arial', 30)

    # Область статуса
    status_rect = pygame.Rect(0, WIDTH, WIDTH, HEIGHT - WIDTH)
    pygame.draw.rect(screen, (40, 40, 40), status_rect)

    if not game_state['game_over']:
        player_text = "Ход: Крестики" if game_state['player'] == PLAYER_X else "Ход: Нолики"
        text_surface = font.render(player_text, True, TEXT_COLOR)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, WIDTH + 20))
    else:
        if game_state['winner'] == PLAYER_X:
            result_text = "Крестики победили!"
        elif game_state['winner'] == PLAYER_O:
            result_text = "Нолики победили!"
        else:
            result_text = "Ничья!"

        text_surface = font.render(result_text, True, TEXT_COLOR)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, WIDTH + 20))


def draw_restart_button():
    """Отрисовка кнопки перезапуска"""
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)

    # Проверка наведения мыши
    mouse_pos = pygame.mouse.get_pos()
    button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR

    # Рисуем кнопку
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, border_radius=10)

    # Текст кнопки
    font = pygame.font.SysFont('arial', 28)
    text_surface = font.render("Новая игра", True, TEXT_COLOR)
    screen.blit(text_surface, (button_rect.centerx - text_surface.get_width() // 2,
                               button_rect.centery - text_surface.get_height() // 2))

    return button_rect


def get_board_position(pos):
    """Получение позиции на доске по координатам мыши"""
    x, y = pos

    if x < 0 or x > WIDTH or y < 0 or y > WIDTH:
        return None

    col = x // CELL_SIZE
    row = y // CELL_SIZE

    return int(row), int(col)


def is_valid_move(game_state, row, col):
    """Проверка, является ли ход допустимым"""
    if row is None or col is None:
        return False

    board = game_state['board']
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == EMPTY


def make_move(game_state, row, col):
    """Совершение хода"""
    if is_valid_move(game_state, row, col):
        board = game_state['board']
        player = game_state['player']

        board[row][col] = player
        game_state['move_count'] += 1


        winner = check_winner(game_state)
        if winner is not None:
            game_state['game_over'] = True
            game_state['winner'] = winner
        elif game_state['move_count'] == BOARD_SIZE * BOARD_SIZE:
            game_state['game_over'] = True
            game_state['winner'] = DRAW
        else:
            # Смена игрока
            game_state['player'] = PLAYER_O if player == PLAYER_X else PLAYER_X

        return True
    return False


def check_winner(game_state):
    """Проверка победителя"""
    board = game_state['board']

    # Проверка строк
    for row in range(BOARD_SIZE):
        if abs(sum(board[row])) == BOARD_SIZE:
            return board[row][0]

    # Проверка столбцов
    for col in range(BOARD_SIZE):
        if abs(sum(board[:, col])) == BOARD_SIZE:
            return board[0][col]


    diag_sum = 0
    for i in range(BOARD_SIZE):
        diag_sum += board[i][i]
    if abs(diag_sum) == BOARD_SIZE:
        return board[0][0]


    anti_diag_sum = 0
    for i in range(BOARD_SIZE):
        anti_diag_sum += board[i][BOARD_SIZE - 1 - i]
    if abs(anti_diag_sum) == BOARD_SIZE:
        return board[0][BOARD_SIZE - 1]

    return None


def draw_winning_line(game_state):
    """Отрисовка линии через выигрышные клетки"""
    if not game_state['game_over'] or game_state['winner'] == DRAW:
        return

    board = game_state['board']
    winner = game_state['winner']


    for row in range(BOARD_SIZE):
        if abs(sum(board[row])) == BOARD_SIZE:
            start_pos = (CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
            end_pos = (WIDTH - CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 10)
            return


    for col in range(BOARD_SIZE):
        if abs(sum(board[:, col])) == BOARD_SIZE:
            start_pos = (col * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2)
            end_pos = (col * CELL_SIZE + CELL_SIZE // 2, WIDTH - CELL_SIZE // 2)
            pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 10)
            return


    diag_sum = 0
    for i in range(BOARD_SIZE):
        diag_sum += board[i][i]
    if abs(diag_sum) == BOARD_SIZE:
        start_pos = (CELL_SIZE // 2, CELL_SIZE // 2)
        end_pos = (WIDTH - CELL_SIZE // 2, WIDTH - CELL_SIZE // 2)
        pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 10)
        return


    anti_diag_sum = 0
    for i in range(BOARD_SIZE):
        anti_diag_sum += board[i][BOARD_SIZE - 1 - i]
    if abs(anti_diag_sum) == BOARD_SIZE:
        start_pos = (WIDTH - CELL_SIZE // 2, CELL_SIZE // 2)
        end_pos = (CELL_SIZE // 2, WIDTH - CELL_SIZE // 2)
        pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 10)
        return


def reset_game():
    """Сброс игры"""
    return initialize_game()


def main():
    """Главная функция игры"""
    game_state = initialize_game()
    restart_button = None

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Проверка нажатия на кнопку перезапуска
                if restart_button and restart_button.collidepoint(pos):
                    game_state = reset_game()
                    continue

                # Если игра окончена, не обрабатываем клики по полю
                if game_state['game_over']:
                    continue


                board_pos = get_board_position(pos)
                if board_pos:
                    row, col = board_pos
                    make_move(game_state, row, col)


        draw_board()
        draw_figures(game_state)
        draw_winning_line(game_state)
        draw_status(game_state)
        restart_button = draw_restart_button()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()