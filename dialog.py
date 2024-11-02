import pygame
from utils import load_image

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 25)

dialog_box_width = 500
dialog_box_heigth = 600
padding_bottom = 20

speaker_label_x = 50
speaker_label_y = 50

content_label_x = 50
content_label_y = 75

helper_label_x = 50
helper_label_y = 150

npc_folder_location = "content/albert.npc"


class DialogView:

    def __init__(self, window, dialog_box_sprite="/dialog2.png"):
        self.window_x = window.get_width() / 2 - dialog_box_width
        self.window_y = window.get_height() - dialog_box_heigth
        self.sprite = load_image(dialog_box_sprite)

        self.current_line = 0
        self.last_update = pygame.time.get_ticks()
        self.npc_file = npc_folder_location
        self.npc = "Redcliff"
        self.speaker_label = ""
        self.content_label = ""

        file = open(self.npc_file, "r")
        data = file.read()
        file.close()
        self.lines = data.split("\n")

        self.next_line()

    # Get the next line of dialog
    def next_line(self):
        print(f"current line :{self.current_line}")

        now = pygame.time.get_ticks()
        if now - self.last_update > 800:
            self.last_update = pygame.time.get_ticks()

            if self.current_line >= len(self.lines):
                self.breakdown()
                return
            line = self.lines[self.current_line]

            if line[0] == "-":
                self.player_speak(line)
            elif line[0] == "!":
                self.command(line)
            elif line[0] == "$":
                self.narrate(line)
            else:
                self.npc_speak(line)

            self.current_line = self.current_line + 1

    # npc speak
    def npc_speak(self, line):
        self.speaker_label = self.npc
        self.content_label = line

    # player speak
    def player_speak(self, line):
        self.speaker_label = "You"
        self.content_label = line[1:]

    # Tell story
    def narrate(self, line):
        self.speaker_label = "Commrad Stalin - Personal Notes"
        self.content_label = line[1:]

    # Execute a command - give/take something to player or move npc to place
    def command(self, line):
        pass

    # Check if a key is pressed to move to next line
    def update(self):
        pass

    # Destroy dialog window
    def breakdown(self):
        self.current_line = 0

    def render(self, window):

        SPEAKER = FONT.render(self.speaker_label, 1, (0, 0, 0))
        TEXT = FONT.render(self.content_label, 1, (0, 0, 0))
        DOTS = FONT.render("Press k ...", 1, (0, 0, 0))

        # print(f"speaker: {self.speaker_label}")
        # print(f"content: {self.content_label}")

        window.blit(self.sprite, (self.window_x, self.window_y))
        window.blit(SPEAKER, (self.window_x + 120, self.window_y + 150))
        window.blit(TEXT, (self.window_x + 150, self.window_y + 220))
        window.blit(DOTS, (self.window_x + 750, self.window_y + 320))
