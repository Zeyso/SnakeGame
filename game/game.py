import pygame
import random

# Initialisierung von pygame
pygame.init()

# Bildschirmgröße
WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Spiel")

# Farben
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Schlangeneigenschaften
BLOCK_SIZE = 20
SPEED = 8
WINNING_SCORE = 20  # Anzahl der Punkte zum Gewinnen


# Schlangenkörper
class Snake:
    def __init__(self):
        self.body = [(200, 200), (210, 200), (220, 200)]
        self.direction = "LEFT"
        self.score = 0

    def move(self):
        head = list(self.body[0])
        if self.direction == "UP":
            head[1] -= BLOCK_SIZE
        elif self.direction == "DOWN":
            head[1] += BLOCK_SIZE
        elif self.direction == "LEFT":
            head[0] -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            head[0] += BLOCK_SIZE
        self.body.insert(0, tuple(head))
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(WIN, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        for segment in self.body[1:]:
            if head == segment:
                return True
        return False


# Apfel
class Apple:
    def __init__(self):
        self.x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        self.y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)

    def draw(self):
        pygame.draw.rect(WIN, RED, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))


def start_screen():
    font = pygame.font.Font(None, 36)
    text = font.render("Drücke eine Taste, um zu starten.", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(text, text_rect)
    pygame.display.update()
    wait_for_key()


def death_screen(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Du bist gestorben! Punktzahl: {score}.", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(text, text_rect)
    pygame.display.update()
    wait_for_restart()


def win_screen(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Du hast gewonnen! Punktzahl: {score}.", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(text, text_rect)
    pygame.display.update()
    wait_for_restart()


def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                waiting = False


def wait_for_restart():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    main()  # Startet ein neues Spiel
                    waiting = False


def main():
    snake = Snake()
    apple = Apple()
    clock = pygame.time.Clock()

    start_screen()

    running = True
    while running:
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_s and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_a and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_d and snake.direction != "LEFT":
                    snake.direction = "RIGHT"

        snake.move()
        if snake.body[0] == (apple.x, apple.y):
            snake.grow()
            apple = Apple()
            snake.score += 1

        snake.draw()
        apple.draw()

        if snake.check_collision():
            death_screen(snake.score)
            return

        if snake.score >= WINNING_SCORE:  # Überprüfen auf Gewinn
            win_screen(snake.score)
            return

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == "__main__":
    main()