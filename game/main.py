import pygame
import json
import sys
import os
from dialogue import get_dialogue
from story import Story

# Ensure the required data directory exists for the game to load properly
os.makedirs("../data", exist_ok=True)

# Output confirmation message
"✅ '../data' directory has been created (or already exists). You should now be able to run the game without a FileNotFoundError."


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
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

    return y

def draw_button(surface, text, rect, color=(100, 100, 100), text_color=WHITE, font=FONT, padding=10, max_width=None):
    if max_width is None:
        max_width = rect.width - 2 * padding

    words = text.split(" ")
    lines = []
    line = ""

    for word in words:
        test_line = f"{line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)

    line_height = font.get_height()
    total_height = len(lines) * (line_height + 2)
    rect.height = total_height + 2 * padding

    pygame.draw.rect(surface, color, rect)

    for i, line in enumerate(lines):
        label = font.render(line, True, text_color)
        label_rect = label.get_rect(center=(rect.centerx, rect.y + padding + i * (line_height + 2) + line_height // 2))
        surface.blit(label, label_rect)

def list_cases(folder="../data"):
    return sorted([f for f in os.listdir(folder) if f.endswith(".json")])

def main():
    global screen, WIDTH, HEIGHT
    current_screen = "menu"
    story = None
    story_id = ""
    dialogue_index = 0
    showing_dialogue = False
    button_rects = []
    selected_setting_index = None
    selected_interactable_index = 0
    visited_settings = set()
    visited_interactables = set()
    choice_selected = None
    case_files = list_cases()

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            elif current_screen == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(button_rects):
                    if button.collidepoint(mouse_pos):
                        story_path = f"../data/{case_files[i]}"
                        story_id = os.path.splitext(case_files[i])[0].lower().replace(" ", "_").replace("&", "and")
                        story = Story.from_file(story_path, story_id)
                        dialogue_index = 0
                        showing_dialogue = bool(story.get_dialogue_ids())
                        visited_settings = set()
                        selected_setting_index = None
                        selected_interactable_index = 0
                        visited_interactables = set()
                        current_screen = "dialogue" if showing_dialogue else "intro"

            elif current_screen == "dialogue" and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                dialogue_index += 1
                if dialogue_index >= len(story.get_dialogue_ids()):
                    current_screen = "intro"
                    showing_dialogue = False

            elif current_screen == "intro" and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                current_screen = "investigation_menu"

            elif current_screen == "investigation_menu" and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(button_rects):
                    if button.collidepoint(mouse_pos):
                        selected_setting_index = i
                        selected_interactable_index = 0
                        visited_interactables = set()
                        current_screen = "investigation_detail"

            elif current_screen == "investigation_menu" and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if len(visited_settings) == len(story.get_settings()):
                    current_screen = "choices"

            elif current_screen == "investigation_detail" and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                setting = story.get_settings()[selected_setting_index]
                interactables = setting.get("interactables", [])
                sequential = setting.get("sequential", True)

                if sequential:
                    if selected_interactable_index < len(interactables):
                        visited_interactables.add(selected_interactable_index)
                        selected_interactable_index += 1
                    if selected_interactable_index >= len(interactables):
                        visited_settings.add(selected_setting_index)
                        selected_setting_index = None
                        current_screen = "investigation_menu"
                else:
                    visited_settings.add(selected_setting_index)
                    selected_setting_index = None
                    current_screen = "investigation_menu"

            elif current_screen == "choices" and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(button_rects):
                    if button.collidepoint(mouse_pos):
                        choice_selected = i
                        current_screen = "result"

            elif current_screen == "result" and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                current_screen = "menu"
                choice_selected = None

        screen.fill(BLACK)

        if current_screen == "menu":
            draw_text(screen, "PII Noir - Select a Case", 40, 40)
            button_rects = []
            for i, case_file in enumerate(case_files):
                title = os.path.splitext(case_file)[0].replace("_", " ").title()
                rect = pygame.Rect(60, 100 + i * 60, WIDTH - 120, 40)
                draw_button(screen, title, rect)
                button_rects.append(rect)

        elif current_screen == "dialogue" and showing_dialogue:
            dialogue_ids = story.get_dialogue_ids()
            if dialogue_index < len(dialogue_ids):
                dialogue_id = dialogue_ids[dialogue_index]
                dialogue = get_dialogue(story.get_case_id(), dialogue_id)
                if dialogue:
                    y = 40
                    y = draw_text(screen, f"{dialogue['speaker']}:", 40, y, WIDTH - 80)
                    y += 10
                    for line in dialogue["lines"]:
                        y = draw_text(screen, line, 60, y, WIDTH - 100)
                        y += 5
                    draw_text(screen, "Click or press any key to continue...", 40, HEIGHT - 40, WIDTH - 80)

        elif current_screen == "intro":
            y = draw_text(screen, story.get_intro(), 40, 40, WIDTH - 80)
            draw_text(screen, "Click or press any key to continue...", 40, HEIGHT - 40, WIDTH - 80)

        elif current_screen == "investigation_menu":
            y = draw_text(screen, "Areas Available to Investigate:", 40, 40, WIDTH - 80)
            button_rects = []
            for i, setting in enumerate(story.get_settings()):
                status = "✓" if i in visited_settings else ""
                rect = pygame.Rect(60, y + 20 + i * 60, WIDTH - 120, 40)
                draw_button(screen, f"{status} Investigate {setting['name']}", rect)
                button_rects.append(rect)
            if len(visited_settings) == len(story.get_settings()):
                draw_text(screen, "Click or press any key to proceed...", 40, HEIGHT - 40, WIDTH - 80)

        elif current_screen == "investigation_detail" and selected_setting_index is not None:
            setting = story.get_settings()[selected_setting_index]
            interactables = setting.get("interactables", [])
            sequential = setting.get("sequential", True)
            y = draw_text(screen, f"You investigate {setting['name']}:", 40, 40, WIDTH - 80)

            if sequential and selected_interactable_index < len(interactables):
                y = draw_text(screen, interactables[selected_interactable_index], 60, y + 10, WIDTH - 100)
                draw_text(screen, "Click or press any key to continue investigating...", 40, HEIGHT - 40, WIDTH - 80)
            elif not sequential:
                for item in interactables:
                    y = draw_text(screen, item, 60, y + 10, WIDTH - 100)
                draw_text(screen, "Click or press any key to go back...", 40, HEIGHT - 40, WIDTH - 80)

        elif current_screen == "choices":
            y = draw_text(screen, "What do you do?", 40, 40, WIDTH - 80)
            button_rects = []
            for i, option in enumerate(story.get_choices()):
                rect = pygame.Rect(60, y + 20 + i * 70, WIDTH - 120, 50)
                draw_button(screen, f"{i + 1}. {option['text']}", rect)
                button_rects.append(rect)

        elif current_screen == "result":
            if choice_selected is not None:
                choice_data = story.get_choices()[choice_selected]
                result_text = choice_data.get("result", "")
                tip_text = choice_data.get("tip", story.get_tip())
                y = draw_text(screen, "Result:", 40, 40, WIDTH - 80)
                y = draw_text(screen, result_text, 60, y + 10, WIDTH - 100)
                y = draw_text(screen, "Privacy Tip:", 40, y + 30, WIDTH - 80)
                draw_text(screen, tip_text, 60, y + 10, WIDTH - 100)
            else:
                draw_text(screen, "Error: No choice selected.", 40, 40, WIDTH - 80)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
