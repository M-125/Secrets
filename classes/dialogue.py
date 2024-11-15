import json
import pygame
class Dialogue:
    def __init__(self,dialogue_name) -> None:
        self.dialogue_name = dialogue_name
        self.dialogues=json.load(open("dialogues/"+dialogue_name))

