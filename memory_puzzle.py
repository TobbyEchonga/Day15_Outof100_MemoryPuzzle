import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 4
CARD_SIZE = 100
MARGIN = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Puzzle Game")

# Load card images
card_images = []
for i in range(1, GRID_SIZE**2 // 2 + 1):
    img = pygame.image.load(f"card{i}.png")
    img = pygame.transform.scale(img, (CARD_SIZE, CARD_SIZE))
    card_images.extend([img.copy(), img.copy()])

# Shuffle card images
random.shuffle(card_images)

# Create the grid
grid = []
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        index = row * GRID_SIZE + col
        card = {
            "image": card_images[index],
            "rect": pygame.Rect(col * (CARD_SIZE + MARGIN), row * (CARD_SIZE + MARGIN), CARD_SIZE, CARD_SIZE),
            "visible": False,
            "matched": False
        }
        grid.append(card)

# Main game loop
clock = pygame.time.Clock()
selected_cards = []
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN and len(selected_cards) < 2:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for card in grid:
                if not card["visible"] and card["rect"].collidepoint(mouse_x, mouse_y):
                    card["visible"] = True
                    selected_cards.append(card)

    # Check for matching cards
    if len(selected_cards) == 2:
        pygame.time.wait(500)  # Wait for a short duration to show the second card
        if selected_cards[0]["image"] == selected_cards[1]["image"]:
            selected_cards[0]["matched"] = True
            selected_cards[1]["matched"] = True
        for card in selected_cards:
            card["visible"] = False
        selected_cards = []

    # Draw the grid
    screen.fill(WHITE)
    for card in grid:
        if card["visible"] or card["matched"]:
            screen.blit(card["image"], card["rect"])

    # Check for game completion
    if all(card["matched"] for card in grid):
        font = pygame.font.Font(None, 36)
        text = font.render("Congratulations! You Win!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before exiting
        game_over = True

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
