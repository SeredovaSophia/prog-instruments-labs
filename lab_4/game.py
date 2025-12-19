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


class GameState:
    """Класс для управления состоянием игры"""

    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.player = PLAYER_X
        self.game_over = False
        self.winner = None
        self.move_count = 0

    def reset(self):
        """Сброс состояния игры"""
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.player = PLAYER_X
        self.game_over = False
        self.winner = None
        self.move_count = 0

    def make_move(self, row, col):
        """Совершение хода"""
        if not self.is_valid_move(row, col):
            return False

        self.board[row][col] = self.player
        self.move_count += 1

        winner = self.check_winner()
        if winner is not None:
            self.game_over = True
            self.winner = winner
        elif self.move_count == BOARD_SIZE * BOARD_SIZE:
            self.game_over = True
            self.winner = DRAW
        else:
            self.player = PLAYER_O if self.player == PLAYER_X else PLAYER_X

        return True

    def is_valid_move(self, row, col):
        """Проверка, является ли ход допустимым"""
        if row is None or col is None:
            return False
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == EMPTY

    def check_winner(self):
        """Проверка победителя"""
        for row in range(BOARD_SIZE):
            if abs(sum(self.board[row])) == BOARD_SIZE:
                return self.board[row][0]

        for col in range(BOARD_SIZE):
            if abs(sum(self.board[:, col])) == BOARD_SIZE:
                return self.board[0][col]

        diag_sum = sum(self.board[i][i] for i in range(BOARD_SIZE))
        if abs(diag_sum) == BOARD_SIZE:
            return self.board[0][0]

        anti_diag_sum = sum(self.board[i][BOARD_SIZE - 1 - i] for i in range(BOARD_SIZE))
        if abs(anti_diag_sum) == BOARD_SIZE:
            return self.board[0][BOARD_SIZE - 1]

        return None


class BoardRenderer:
    """Класс для отрисовки игрового поля"""

    def __init__(self, screen):
        self.screen = screen

    def draw_board(self):
        """Отрисовка игрового поля"""
        self.screen.fill(BG_COLOR)

        for i in range(1, BOARD_SIZE):
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (0, i * CELL_SIZE),
                (WIDTH, i * CELL_SIZE),
                LINE_WIDTH
            )

        for i in range(1, BOARD_SIZE):
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (i * CELL_SIZE, 0),
                (i * CELL_SIZE, WIDTH),
                LINE_WIDTH
            )

    def draw_figures(self, game_state):
        """Отрисовка крестиков и ноликов"""
        board = game_state.board

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == PLAYER_X:
                    self.draw_cross(row, col)
                elif board[row][col] == PLAYER_O:
                    self.draw_circle(row, col)

    def draw_cross(self, row, col):
        """Отрисовка крестика"""
        start_desc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE)
        end_desc = ((col + 1) * CELL_SIZE - SPACE, (row + 1) * CELL_SIZE - SPACE)
        pygame.draw.line(self.screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

        start_asc = ((col + 1) * CELL_SIZE - SPACE, row * CELL_SIZE + SPACE)
        end_asc = (col * CELL_SIZE + SPACE, (row + 1) * CELL_SIZE - SPACE)
        pygame.draw.line(self.screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

    def draw_circle(self, row, col):
        """Отрисовка нолика"""
        center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
        radius = CELL_SIZE // 3
        pygame.draw.circle(self.screen, CIRCLE_COLOR, center, radius, CIRCLE_WIDTH)

    def draw_winning_line(self, game_state):
        """Отрисовка линии через выигрышные клетки"""
        if not game_state.game_over or game_state.winner == DRAW:
            return

        board = game_state.board

        for row in range(BOARD_SIZE):
            if abs(sum(board[row])) == BOARD_SIZE:
                self.draw_horizontal_line(row)
                return

        for col in range(BOARD_SIZE):
            if abs(sum(board[:, col])) == BOARD_SIZE:
                self.draw_vertical_line(col)
                return

        diag_sum = sum(board[i][i] for i in range(BOARD_SIZE))
        if abs(diag_sum) == BOARD_SIZE:
            self.draw_main_diagonal()
            return

        anti_diag_sum = sum(board[i][BOARD_SIZE - 1 - i] for i in range(BOARD_SIZE))
        if abs(anti_diag_sum) == BOARD_SIZE:
            self.draw_anti_diagonal()
            return

    def draw_horizontal_line(self, row):
        """Отрисовка горизонтальной линии"""
        start_pos = (CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
        end_pos = (WIDTH - CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.line(self.screen, (255, 0, 0), start_pos, end_pos, 10)

    def draw_vertical_line(self, col):
        """Отрисовка вертикальной линии"""
        start_pos = (col * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2)
        end_pos = (col * CELL_SIZE + CELL_SIZE // 2, WIDTH - CELL_SIZE // 2)
        pygame.draw.line(self.screen, (255, 0, 0), start_pos, end_pos, 10)

    def draw_main_diagonal(self):
        """Отрисовка главной диагонали"""
        start_pos = (CELL_SIZE // 2, CELL_SIZE // 2)
        end_pos = (WIDTH - CELL_SIZE // 2, WIDTH - CELL_SIZE // 2)
        pygame.draw.line(self.screen, (255, 0, 0), start_pos, end_pos, 10)

    def draw_anti_diagonal(self):
        """Отрисовка побочной диагонали"""
        start_pos = (WIDTH - CELL_SIZE // 2, CELL_SIZE // 2)
        end_pos = (CELL_SIZE // 2, WIDTH - CELL_SIZE // 2)
        pygame.draw.line(self.screen, (255, 0, 0), start_pos, end_pos, 10)


class UIRenderer:
    """Класс для отрисовки пользовательского интерфейса"""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('arial', 30)

    def draw_status(self, game_state):
        """Отрисовка статуса игры"""
        status_rect = pygame.Rect(0, WIDTH, WIDTH, HEIGHT - WIDTH)
        pygame.draw.rect(self.screen, (40, 40, 40), status_rect)

        if not game_state.game_over:
            player_text = "Ход: Крестики" if game_state.player == PLAYER_X else "Ход: Нолики"
            text_surface = self.font.render(player_text, True, TEXT_COLOR)
            self.screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, WIDTH + 20))
        else:
            if game_state.winner == PLAYER_X:
                result_text = "Крестики победили!"
            elif game_state.winner == PLAYER_O:
                result_text = "Нолики победили!"
            else:
                result_text = "Ничья!"

            text_surface = self.font.render(result_text, True, TEXT_COLOR)
            self.screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, WIDTH + 20))

    def draw_restart_button(self):
        """Отрисовка кнопки перезапуска"""
        button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)

        mouse_pos = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR

        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2, border_radius=10)

        font = pygame.font.SysFont('arial', 28)
        text_surface = font.render("Новая игра", True, TEXT_COLOR)
        self.screen.blit(text_surface, (button_rect.centerx - text_surface.get_width() // 2,
                                        button_rect.centery - text_surface.get_height() // 2))

        return button_rect


class InputHandler:
    """Класс для обработки пользовательского ввода"""

    @staticmethod
    def get_board_position(pos):
        """Получение позиции на доске по координатам мыши"""
        x, y = pos

        if x < 0 or x > WIDTH or y < 0 or y > WIDTH:
            return None

        col = x // CELL_SIZE
        row = y // CELL_SIZE

        return int(row), int(col)


class GameController:
    """Основной контроллер игры"""

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Крестики-Нолики")

        self.game_state = GameState()
        self.board_renderer = BoardRenderer(self.screen)
        self.ui_renderer = UIRenderer(self.screen)
        self.input_handler = InputHandler()

        self.clock = pygame.time.Clock()
        self.restart_button = None

    def run(self):
        """Запуск главного цикла игры"""
        while True:
            self.handle_events()
            self.update_display()
            self.clock.tick(60)

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        """Обработка клика мыши"""
        # Проверка нажатия на кнопку перезапуска
        if self.restart_button and self.restart_button.collidepoint(pos):
            self.game_state.reset()
            return

        if self.game_state.game_over:
            return

        board_pos = self.input_handler.get_board_position(pos)
        if board_pos:
            row, col = board_pos
            self.game_state.make_move(row, col)

    def update_display(self):
        """Обновление отображения"""
        self.board_renderer.draw_board()
        self.board_renderer.draw_figures(self.game_state)
        self.board_renderer.draw_winning_line(self.game_state)
        self.ui_renderer.draw_status(self.game_state)
        self.restart_button = self.ui_renderer.draw_restart_button()

        pygame.display.update()


def main():
    """Главная функция игры"""
    game_controller = GameController()
    game_controller.run()


if __name__ == "__main__":
    main()