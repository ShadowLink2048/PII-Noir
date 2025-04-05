import pygame
import json
import sys

# initialize the game
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PII Noir - Case player")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("couriernew", 24)

# draw text
def draw_text(surface, text, x, y, line_helper=30):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        rendered = FONT.render(line, True, WHITE)
        surface.blit(rendered, (x, y + i * line_helper))

# load cases
def load_case(filename):
    with open(filename, "r") as f:
        return json.load(f)


# Main Game Loop
def main():
    case = load_case("../data/case1.json")
    clues = case["clues"]
    current_screen = "intro"
    choice_selected = None
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if current_screen == "intro":
                    current_screen = "clues"
                elif current_screen == "clues":
                    current_screen = "choices"
                elif current_screen == "choices":
                    if event.key == pygame.K_1:
                        choice_selected = 0
                        current_screen = "result"
                    elif event.key == pygame.K_2:
                        choice_selected = 1
                        current_screen = "result"

        # 🎬 Scene Logic
        if current_screen == "intro":
            draw_text(screen, case["intro"], 40, 40)
            draw_text(screen, "Press any key to continue...", 40, 500)
        elif current_screen == "clues":
            draw_text(screen, "Clues found:", 40, 40)
            for i, clue in enumerate(clues):
                draw_text(screen, f"- {clue['text']}", 60, 80 + i * 30)
            draw_text(screen, "Press any key to continue...", 40, 500)
        elif current_screen == "choices":
            prompt = case["choices"][0]["prompt"]
            draw_text(screen, prompt, 40, 40)
            for i, option in enumerate(case["choices"][0]["options"]):
                draw_text(screen, f"{i+1}. {option['text']}", 60, 100 + i * 40)
        elif current_screen == "result":
            result_text = case["choices"][0]["options"][choice_selected]["result"]
            tip_text = case["tip"]
            draw_text(screen, "Result:", 40, 40)
            draw_text(screen, result_text, 60, 80)
            draw_text(screen, "Privacy Tip:", 40, 200)
            draw_text(screen, tip_text, 60, 240)
            draw_text(screen, "Press [X] to close window.", 40, 500)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

