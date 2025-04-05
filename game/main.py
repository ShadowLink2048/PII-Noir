import pygame
import json
import sys
import os
from dialogue import get_dialogue

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PII Noir - Case Selector")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("couriernew", 24)

def draw_text(surface, text, x, y, max_width=700, font=FONT, color=WHITE, spacing=5):
    words = text.split(" ")
    lines = []
    line = ""

    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())

    for line in lines:
        rendered = font.render(line, True, color)
        surface.blit(rendered, (x, y))
        y += rendered.get_height() + spacing

    return y  # Return final y value for stacking


def draw_button(surface, text, rect, color=(100, 100, 100), text_color=WHITE, padding=10):
    pygame.draw.rect(surface, color, rect)

    # Text wrapping logic
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test_line = f"{line} {word}".strip()
        if FONT.size(test_line)[0] <= rect.width - 2 * padding:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)

    total_height = len(lines) * FONT.get_height()
    y_offset = rect.centery - total_height // 2

    for i, line in enumerate(lines):
        label = FONT.render(line, True, text_color)
        label_rect = label.get_rect(centerx=rect.centerx, y=y_offset + i * FONT.get_height())
        surface.blit(label, label_rect)


def load_case(filename):
    with open(filename, "r") as f:
        return json.load(f)

def list_cases(folder="../data"):
    return sorted([f for f in os.listdir(folder) if f.endswith(".json")])

def main():
    current_screen = "menu"
    choice_selected = None
    case = None
    case_id = ""
    clues = []
    dialogue_ids = []
    dialogue_index = 0
    showing_dialogue = False
    button_rects = []
    case_files = list_cases()
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif current_screen == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(button_rects):
                    if button.collidepoint(mouse_pos):
                        case_path = f"../data/{case_files[i]}"
                        case_id = os.path.splitext(case_files[i])[0].lower().replace(" ", "_").replace("&", "and")
                        case = load_case(case_path)
                        clues = case["clues"]
                        dialogue_ids = case.get("dialogue", [])
                        dialogue_index = 0
                        showing_dialogue = bool(dialogue_ids)
                        current_screen = "dialogue" if showing_dialogue else "intro"

            elif current_screen == "dialogue" and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                dialogue_index += 1
                if dialogue_index >= len(dialogue_ids):
                    current_screen = "intro"
                    showing_dialogue = False

            elif current_screen == "intro" and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                current_screen = "clues"

            elif current_screen == "clues" and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                current_screen = "choices"

            elif current_screen == "choices" and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(button_rects):
                    if button.collidepoint(mouse_pos):
                        choice_selected = i
                        current_screen = "result"

            elif current_screen == "result" and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                current_screen = "menu"
                choice_selected = None

        if current_screen == "menu":
            draw_text(screen, "PII Noir - Select a Case", 40, 40)
            button_rects = []
            for i, case_file in enumerate(case_files):
                title = os.path.splitext(case_file)[0].replace("_", " ").title()
                rect = pygame.Rect(60, 100 + i * 60, 600, 40)
                draw_button(screen, title, rect)
                button_rects.append(rect)

        elif current_screen == "dialogue" and showing_dialogue:
            if dialogue_index < len(dialogue_ids):
                dialogue = get_dialogue(case_id, dialogue_ids[dialogue_index])
                if dialogue:
                    y = 40
                    y = draw_text(screen, f"{dialogue['speaker']}:", 40, y)
                    y += 10  # Space between speaker and lines
                    for line in dialogue["lines"]:
                        y = draw_text(screen, line, 60, y)
                        y += 5
                    draw_text(screen, "Click or press any key to continue...", 40, HEIGHT - 40)

        elif current_screen == "intro":
            draw_text(screen, case["intro"], 40, 40)
            draw_text(screen, "Press any key or click to continue...", 40, HEIGHT - 40)

        elif current_screen == "clues":
            y = draw_text(screen, "Clues found:", 40, 40)
            for clue in clues:
                y = draw_text(screen, f"- {clue['text']}", 60, y)
            draw_text(screen, "Press any key or click to continue...", 40, HEIGHT - 40)

        elif current_screen == "choices":
            y = draw_text(screen, case["choices"][0]["prompt"], 40, 40)
            button_rects = []
            for i, option in enumerate(case["choices"][0]["options"]):
                rect = pygame.Rect(60, y + 20 + i * 60, 600, 40)
                draw_button(screen, f"{i+1}. {option['text']}", rect)
                button_rects.append(rect)

        elif current_screen == "result":
            if choice_selected is not None:
                result_text = case["choices"][0]["options"][choice_selected]["result"]
                tip_text = case["tip"]
                y = draw_text(screen, "Result:", 40, 40)
                y = draw_text(screen, result_text, 60, y + 10)
                y = draw_text(screen, "Privacy Tip:", 40, y + 30)
                draw_text(screen, tip_text, 60, y + 10)

                # 🔘 Add back-to-menu button
                return_rect = pygame.Rect(300, 500, 200, 40)
                draw_button(screen, "Back to Menu", return_rect)
                button_rects = [return_rect]
            else:
                draw_text(screen, "Error: No choice selected.", 40, 40)


        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
