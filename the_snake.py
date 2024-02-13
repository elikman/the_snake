from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
SPEED = 20

GRID_COLOR = (100, 100, 100)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Тут опишите все классы игры.
class GameObject:
    def __init__(self, position, body_color):
        """Базовый класс для игровых объектов."""
        self.position = position
        self.body_color = body_color

class Apple(GameObject):
    def __init__(self, position):
        """Класс для представления яблока."""
        super().__init__(position, APPLE_COLOR)

    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

        
class Snake(GameObject):
    def __init__(self, position, length=1):
        """Класс для представления змейки."""
        super().__init__(position, SNAKE_COLOR)
        self.length = length
        self.positions = [position]
        self.direction = UP  # Указываем начальное направление
        self.next_direction = None
        self.last = None
        
    def handle_keys(game_object):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game_object.direction != DOWN:
                    game_object.next_direction = UP
                elif event.key == pygame.K_DOWN and game_object.direction != UP:
                    game_object.next_direction = DOWN
                elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                    game_object.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                    game_object.next_direction = RIGHT

    def update_direction(self):
        """Метод обновления направления змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод для получения текущей позиции головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Метод обновления направления змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод обновления положения змейки."""
        # Логика обновления положения змейки
        head_position = self.get_head_position()
        new_head_position = (head_position[0] + self.direction[0] * GRID_SIZE, head_position[1] + self.direction[1] * GRID_SIZE)

    # Проверка на столкновение со стеной
        if not (0 <= new_head_position[0] < SCREEN_WIDTH and 0 <= new_head_position[1] < SCREEN_HEIGHT):
            self.reset()
            return

        # Проверка на столкновение с самой собой
        if new_head_position in self.positions[2:]:
            self.reset()
            return

        # Обновление позиции головы
        self.positions.insert(0, new_head_position)

        # Обновление длины змейки
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Метод сброса змейки в начальное состояние."""
        # Логика сброса змейки
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
        
    def draw(self, surface):
        """Метод отрисовки змейки на игровом поле."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)



def draw_grid(screen):
    """Функция для отрисовки сетки на игровом поле."""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

def main():
    # Создаем экземпляры классов:
    apple = Apple((randint(0, GRID_WIDTH - 1) * GRID_SIZE, randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
    snake = Snake(((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)))

    while True:
        clock.tick(SPEED)

        # Обработка событий и обновление направления змейки
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.next_direction = RIGHT
                    
        snake.handle_keys()

        # Обновление направления змейки
        snake.update_direction()

        # Обновление положения змейки
        snake.move()

        # Логика проверки столкновений, роста змейки, появления яблока и отрисовки
        if snake.get_head_position() == apple.position:
            apple = Apple((randint(0, GRID_WIDTH - 1) * GRID_SIZE, randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
            snake.length += 1
            
        # Отрисовка на экране
        screen.fill(BOARD_BACKGROUND_COLOR)
        draw_grid(screen)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()

if __name__ == '__main__':
    main()
