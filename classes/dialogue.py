import json
import pygame
class Dialogue:
    def __init__(self,dialogue_name) -> None:
        self.dialogue_name = dialogue_name
        self.dialogues=json.load(open("assets/dialogues/"+dialogue_name+".json"))
        self.current_dialogue=""
    
    def dialogue(self,option=""):

###get dialogue
        if self.current_dialogue=="":
            self.current_dialogue="dialogue/0"
        self.current_dialogue+=option
        dialogue=self.dialogues

        for e in self.current_dialogue.split("/"):
            if e.isnumeric():
                e=int(e)
            dialogue=dialogue[e]

#print dialogue

        if dialogue is str:

            ### move to next dialogue
            strings=self.current_dialogue.split("/")
            while not strings[-1].isnumeric():
                strings.pop()
            if strings[-1]!="dialogue":
                strings[-1]=str(int(strings[-1])+1)
            self.current_dialogue=""
            for e in strings:
                self.current_dialogue+=e
            
            try:
                self.dialogue[self.current_dialogue]
            except IndexError:
                return None
            #return dialogue
            return self.dialogues["name"],dialogue
        

        if dialogue is dict:
            return self.dialogues["name"],dialogue["text"],dialogue["options"]
        
            

