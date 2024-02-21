iimport random

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
POSITION = (0, 0)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

GRID_COLOR = (100, 100, 100)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(self):
    """Метод обработки нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != DOWN:
                self.next_direction = UP
            elif event.key == pygame.K_DOWN and self.direction != UP:
                self.next_direction = DOWN
            elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                self.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                self.next_direction = RIGHT


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=POSITION, body_color=SNAKE_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовка игрового объекта на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для представления яблока."""

    def __init__(self, position=POSITION):
        super().__init__(position, APPLE_COLOR)

    def randomize_position(self, snake_positions, grid_width, grid_height,
                           grid_size):
        """Рандомизация позиции яблока с учетом занятых позиций змейки."""
        if len(snake_positions) >= grid_width * grid_height:
            raise ValueError("Нет свободных позиций для размещения яблока.")
        while True:
            random_position = (
                random.randint(0, grid_width - 1) * grid_size,
                random.randint(0, grid_height - 1) * grid_size)
            if random_position not in snake_positions:
                self.position = random_position
                break


class Snake(GameObject):
    """Класс для представления змейки."""

    def __init__(self, position=None, length=1):
        super().__init__(position, SNAKE_COLOR)
        self.length = length
        self.reset()

    def update_direction(self):
        """Метод обновления направления змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод для получения текущей позиции головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод обновления положения змейки."""
        x, y = self.get_head_position()
        dx, dy = self.direction

        # Новая позиция головы с учетом направления движения
        new_head_position = ((x + dx * GRID_SIZE) % SCREEN_WIDTH,
                             (y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        # Проверка на столкновение с самой собой
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

        # Обновление позиции головы
        self.positions.insert(0, new_head_position)

        # Обновление длины змейки
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Метод сброса змейки в начальное состояние."""
        self.positions = [self.position] if self.position else [
            ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = UP  # Указываем начальное направление
        self.next_direction = None
        self.last = None

    def draw(self, surface):
        """Метод отрисовки змейки на игровом поле."""
        for position in self.positions[:-1]:
            self.position = position
            super().draw(surface)

        if self.positions:
            self.position = self.positions[-1]
            super().draw(surface)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def draw_grid(screen):
    """Функция для отрисовки сетки на игровом поле."""
    for x in range(SCREEN_WIDTH // GRID_SIZE):  # Упрощенный вызов range
        pygame.draw.line(screen, GRID_COLOR, (x * GRID_SIZE, 0),
                         (x * GRID_SIZE, SCREEN_HEIGHT))
    for y in range(SCREEN_HEIGHT // GRID_SIZE):  # Упрощенный вызов range
        pygame.draw.line(screen, GRID_COLOR, (0, y * GRID_SIZE),
                         (SCREEN_WIDTH, y * GRID_SIZE))


def main():
    """Основная функция игры."""
    apple = Apple((random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                   random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
    snake = Snake(((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)))

    while True:
        clock.tick(SPEED)

        # Обновление направления и положения змейки
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        # Проверка столкновений и рост змейки
        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions, GRID_WIDTH, GRID_HEIGHT,
                                     GRID_SIZE)
            snake.length += 1

        # Отрисовка на экране
        pygame.display.flip()
        handle_keys(snake)
        draw_grid(screen)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
