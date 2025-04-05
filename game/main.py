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

# draw button
def draw_button(surface, text, rect, color=(100, 100, 100), text_color=WHITE):
    pygame.draw.rect(surface, color, rect)
    label = FONT.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)

# load case file
def load_case(filename):
    with open(filename, "r") as f:
        return json.load(f)

# main game loop
def main():
    case = load_case("../data/case1.json")
    clues = case["clues"]
    current_screen = "intro"
    choice_selected = None
    clock = pygame.time.Clock()
    running = True
    button_rects = []

    while running:
        screen.fill(BLACK)
        print("Current screen:", current_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif current_screen == "intro" and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                print("Intro screen advanced!")
                current_screen = "clues"

            elif current_screen == "clues" and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                print("Clue screen advanced!")
                current_screen = "choices"

            elif current_screen == "choices" and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(button_rects):
                    if button.collidepoint(mouse_pos):
                        print(f"Choice {i + 1} selected.")
                        choice_selected = i
                        current_screen = "result"

        # display current screen content
        if current_screen == "intro":
            draw_text(screen, case["intro"], 40, 40)
            draw_text(screen, "Press any key or click to continue...", 40, 500)

        elif current_screen == "clues":
            draw_text(screen, "Clues found:", 40, 40)
            for i, clue in enumerate(clues):
                draw_text(screen, f"- {clue['text']}", 60, 80 + i * 30)
            draw_text(screen, "Press any key or click to continue...", 40, 500)

        elif current_screen == "choices":
            prompt = case["choices"][0]["prompt"]
            draw_text(screen, prompt, 40, 40)

            button_rects = []
            for i, option in enumerate(case["choices"][0]["options"]):
                rect = pygame.Rect(60, 100 + i * 60, 600, 40)
                draw_button(screen, f"{i+1}. {option['text']}", rect)
                button_rects.append(rect)

        elif current_screen == "result":
            if choice_selected is not None:
                result_text = case["choices"][0]["options"][choice_selected]["result"]
                tip_text = case["tip"]
                draw_text(screen, "Result:", 40, 40)
                draw_text(screen, result_text, 60, 80)
                draw_text(screen, "Privacy Tip:", 40, 200)
                draw_text(screen, tip_text, 60, 240)
                draw_text(screen, "Press [X] to close window.", 40, 500)
            else:
                draw_text(screen, "Error: No choice selected.", 40, 40)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
