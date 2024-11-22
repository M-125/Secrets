import json
class Dialogue:
    def __init__(self,dialogue_name,inventory=None) -> None:
        self.dialogue_name = dialogue_name
        self.dialogues=json.load(open("assets/dialogues/"+dialogue_name+".json"))
        self.current_dialogue=""
        self.ended=False
        self.inventory=inventory
        
        
    def next(self):

        strings=self.current_dialogue.split("/")
        while not strings[-1].isnumeric() and not strings[-1]=="_dialogue":
            strings.pop()
        
        print(strings)
        if strings[-1]!="_dialogue":
            strings[-1]=str(int(strings[-1])+1)
        self.current_dialogue=""
        for e in strings:
            if e !="_dialogue":self.current_dialogue+="/"
            self.current_dialogue+=e
        
        try:
            testdialogue=self.dialogues
            
            for e in self.current_dialogue.split("/"):
        
                    if e.isnumeric():
                        e=int(e)
                    testdialogue=testdialogue[e]
            print("n",self.current_dialogue)
        except Exception:

            strings.pop()
            self.current_dialogue=""
            for e in strings:
                if e !="_dialogue":self.current_dialogue+="/"
                self.current_dialogue+=e
            print("nx",self.current_dialogue)

            if self.current_dialogue=="_dialogue":
                self.ended=True
                return False
            else:
                return self.next()
        
        
        if self.current_dialogue=="_dialogue":
            self.ended=True
            return False
        return True
    
    def jump(self,dial):
        if dial!="":
            self.current_dialogue="_dialogue/"+dial
        else:
            if not self.next():
                return " "," ",["_end"]
        print(self.current_dialogue)
        return self.dialogue() 
    def skip(self):
        if self.next(): return self.dialogue()
        else:   return " "," ",["_end"]

    def change_values(self,d:dict):
        if "_name" in d:
            self.dialogues["name"]=d["_name"]

    def dialogue(self,option=""):
      if not self.ended:
        print(self.current_dialogue)
###get dialogue
        
        if self.current_dialogue=="":
            self.current_dialogue="_dialogue"
        if option!="":self.current_dialogue+="/"+option
        dialogue=self.dialogues
        
        for e in self.current_dialogue.split("/"):
            
            if e.isnumeric():
                e=int(e)
            dialogue=dialogue[e]

#print dialogue
        
        if type(dialogue) == str:
            print(self.current_dialogue)
            if dialogue=="_end":
                if self.next() :
                    return self.dialogue()
                else:
                    return " "," ",["_end"]
            if self.next() :
                return self.dialogues["name"],dialogue,[]
            else:
                return self.dialogues["name"],dialogue,["_end"]
        

        if type(dialogue) == dict:

            self.change_values(dialogue)

            #start dict
            if "start" in dialogue:
                self.current_dialogue+="/start"
                return self.dialogue()
            elif "dialogue" in dialogue:
                self.current_dialogue+="/dialogue"
                return self.dialogue()
            elif "options" in dialogue:return self.dialogues["name"],dialogue["text"],dialogue["options"]
            
            ### JUMP command
            elif "_jump" in dialogue: 
                return self.jump(dialogue["_jump"])
            
            #Jumponly space -- use it for dialogues which should be only seen on jumps
            elif "_jumponly" in dialogue:
                return self.skip()
            
            #checks for dialogue items
            elif "_hasdialogue" in dialogue:
                if self.inventory.has_dialogue_item(dialogue["_hasdialogue"]):
                    return self.jump(dialogue["true"])
                else:
                    return self.jump(dialogue["false"])
            #check for normal items
            elif "_hasitem" in dialogue:
                if self.inventory.has_item(dialogue["_hasitem"]):
                    return self.jump(dialogue["true"])
                else:
                    return self.jump(dialogue["false"])
            elif "_give_dialogue" in dialogue:
                self.inventory.add_dialogue_item(dialogue["_give_dialogue"])
                return self.skip()
            elif "_give_item" in dialogue:
                self.inventory.add_item(dialogue["_give_item"])
                return self.skip()
            elif "text" in dialogue:
                if self.next(): return self.dialogues["name"],dialogue["text"],[]
                else:   return self.dialogues["name"],dialogue["text"],["_end"]
            else:
                return self.skip()
            #return dialogue
        if type(dialogue)==list:
            self.current_dialogue+="/0"
            return self.dialogue()
            
            
      return "_","_",["_end"]
