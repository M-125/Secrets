import json

class Dialogue:
    def __init__(self,dialogue_name) -> None:
        self.dialogue_name = dialogue_name
        self.dialogues=json.load(open("assets/dialogues/"+dialogue_name+".json"))
        self.current_dialogue=""
        self.ended=False
        
    
    def dialogue(self,option=""):
      if not self.ended:
###get dialogue
        if self.current_dialogue=="":
            self.current_dialogue="dialogue/0"
        if option!="":self.current_dialogue+="/"+option
        dialogue=self.dialogues
        
        for e in self.current_dialogue.split("/"):
            
            if e.isnumeric():
                e=int(e)
            dialogue=dialogue[e]

#print dialogue
        
        if type(dialogue) == str:

            ### move to next dialogue if dialogue part is just some text
            strings=self.current_dialogue.split("/")
            while not strings[-1].isnumeric():
                strings.pop()
            if strings[-1]!="dialogue":
                strings[-1]=str(int(strings[-1])+1)
            self.current_dialogue=""
            for e in strings:
                if e !="dialogue":self.current_dialogue+="/"
                self.current_dialogue+=e
            
            try:
                testdialogue=self.dialogues
                
                for e in self.current_dialogue.split("/"):
            
                     if e.isnumeric():
                         e=int(e)
                     testdialogue=testdialogue[e]
            except Exception:
                self.ended=True
                return self.dialogues["name"],dialogue,["end"] 
            #return dialogue
            return self.dialogues["name"],dialogue,[]
        

        if type(dialogue) == dict:
            if "options" in dialogue:return self.dialogues["name"],dialogue["text"],dialogue["options"]
            else:
            	
                strings=self.current_dialogue.split("/")
            while not strings[-1].isnumeric():
                strings.pop()
            if strings[-1]!="dialogue":
                strings[-1]=str(int(strings[-1])+1)
            self.current_dialogue=""
            for e in strings:
                if e !="dialogue":self.current_dialogue+="/"
                self.current_dialogue+=e
            
            try:
                testdialogue=self.dialogues
                
                for e in self.current_dialogue.split("/"):
            
                     if e.isnumeric():
                         e=int(e)
                     testdialogue=testdialogue[e]
            except Exception:
                self.ended=True
                return self.dialogues["name"],dialogue["text"],["end"] 
            #return dialogue
        if type(dialogue)==list:
            self.current_dialogue+="/0"
            dialogue=dialogue[0]
            
            strings=self.current_dialogue.split("/")
            while not strings[-1].isnumeric():
                strings.pop()
            if strings[-1]!="dialogue":
                strings[-1]=str(int(strings[-1])+1)
            self.current_dialogue=""
            for e in strings:
                if e !="dialogue":self.current_dialogue+="/"
                self.current_dialogue+=e
            
            try:
                testdialogue=self.dialogues
                
                for e in self.current_dialogue.split("/"):
            
                     if e.isnumeric():
                         e=int(e)
                     testdialogue=testdialogue[e]
            except Exception:
                self.ended=True
                return self.dialogues["name"],dialogue["text"],["end"] 
            
            
            return self.dialogues["name"],dialogue,[]
      return "_","_","ended"
