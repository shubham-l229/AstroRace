import pygame
import sys
import random
from queue import PriorityQueue

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Player Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Define neighbors function
def neighbors(node):
    x, y = node
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y, keys, end_pos):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5
        self.keys = keys
        self.end_pos = end_pos
        self.winner = False
        self.can_move = False

    def update(self, obstacles):
        if self.can_move:
            if self.keys:
                keys = pygame.key.get_pressed()
                if keys[self.keys[0]] and self.rect.top > 0:
                    self.rect.y -= self.speed
                if keys[self.keys[1]] and self.rect.bottom < HEIGHT:
                    self.rect.y += self.speed
                if keys[self.keys[2]] and self.rect.left > 0:
                    self.rect.x -= self.speed
                if keys[self.keys[3]] and self.rect.right < WIDTH:
                    self.rect.x += self.speed
            else:
                self.pathfinding(obstacles)

            if self.rect.x >= self.end_pos:
                self.winner = True

    def pathfinding(self, obstacles):
        start_node = (self.rect.x // 50, self.rect.y // 50)
        end_node = (WIDTH // 50 - 2, HEIGHT // 50 - 2)
        path = self.astar(obstacles, start_node, end_node)
        if path:
            next_node = path[1]
            target_x = next_node[0] * 50
            target_y = next_node[1] * 50
            if target_x < self.rect.x:
                self.rect.x -= self.speed
            elif target_x > self.rect.x:
                self.rect.x += self.speed
            elif target_y < self.rect.y:
                self.rect.y -= self.speed
            elif target_y > self.rect.y:
                self.rect.y += self.speed

    def astar(self, obstacles, start, end):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def reconstruct_path(came_from, current):
            total_path = [current]
            while current in came_from:
                current = came_from[current]
                total_path.append(current)
            return total_path[::-1]

        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {spot: float("inf") for spot in obstacles}
        g_score[start] = 0
        f_score = {spot: float("inf") for spot in obstacles}
        f_score[start] = heuristic(start, end)

        while not open_set.empty():
            current = open_set.get()[1]

            if current == end:
                return reconstruct_path(came_from, end)  # Correct indentation here

            for neighbor in neighbors(current):
                if neighbor in g_score and neighbor not in obstacles:
                    temp_g_score = g_score[current] + 1

                    if temp_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + heuristic(neighbor, end)
                        open_set.put((f_score[neighbor], neighbor))

        return None  # Correct indentation here as well
  # Correct indentation here as well





# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Function to reset game
def reset_game():
    player1.rect.topleft = (100, HEIGHT // 2 - 25)
    player2.rect.topleft = (100, HEIGHT // 2 + 25)
    obstacles.empty()
    for _ in range(10):
        obstacle_x = random.randint(start_line_x, finish_line_x)
        obstacle_y = random.randint(0, HEIGHT - 50)
        obstacle = Obstacle(obstacle_x, obstacle_y, 50, 50)
        obstacles.add(obstacle)
    player1.winner = False
    player2.winner = False

# Create players

player1 = Player(RED, 100, HEIGHT // 2 - 25, [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], WIDTH - 100)
player2 = Player(BLUE, 100, HEIGHT // 2 + 25, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], WIDTH - 100)


# Create obstacles (invisible)
# Create obstacles (invisible)
obstacles = pygame.sprite.Group()

# Calculate the area between the start and finish lines
start_line_x = 50
finish_line_x = WIDTH - 50
area_width = finish_line_x - start_line_x

# Generate obstacles within the area between the start and finish lines
for _ in range(10):
    obstacle_x = random.randint(start_line_x, finish_line_x)
    obstacle_y = random.randint(0, HEIGHT - 50)  # Ensure obstacle is fully visible on the screen
    obstacle = Obstacle(obstacle_x, obstacle_y, 50, 50)
    obstacles.add(obstacle)


# Sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(player1, player2)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(obstacles)

    screen.fill(WHITE)

    # Draw start and finish lines
    pygame.draw.line(screen, BLACK, (start_line_x, 0), (start_line_x, HEIGHT), 5)  # Start line
    pygame.draw.line(screen, BLACK, (finish_line_x, 0), (finish_line_x, HEIGHT), 5)  # Finish line

    # Draw start and finish text vertically
    font = pygame.font.SysFont(None, 30)
    start_text = pygame.transform.rotate(font.render("START", True, BLACK), 90)
    finish_text = pygame.transform.rotate(font.render("FINISH", True, BLACK), 90)
    screen.blit(start_text, (start_line_x - 30, HEIGHT // 2 - 10))
    screen.blit(finish_text, (finish_line_x + 10, HEIGHT // 2 - 10))

    obstacles.draw(screen)
    all_sprites.draw(screen)

    winner = None
    if player1.winner:
        winner = "Player 1"
    elif player2.winner:
        winner = "Player 2"

    if winner:
        font = pygame.font.SysFont(None, 36)
        winner_text = font.render(f"Winner: {winner}", True, RED if winner == "Player 1" else BLUE)
        screen.blit(winner_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        font = pygame.font.SysFont(None, 24)
        replay_text = font.render("Press SPACE to play again", True, BLACK)
        screen.blit(replay_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            reset_game()

    if not player1.can_move and not player2.can_move:
        player1.can_move = True
        player2.can_move = True

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
