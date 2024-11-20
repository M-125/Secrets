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
            strings.pop()
            self.current_dialogue=""
            for e in strings:
                if e !="dialogue":self.current_dialogue+="/"
                self.current_dialogue+=e
            

            if self.current_dialogue=="dialogue":
                self.ended=True
                return False
            else:
                return self.next()
        return True
    
    def jump(self,dial):
        if dial!="":
            self.current_dialogue="dialogue/"+dial
        else:
            if not self.next():
                return " "," ",["_end"]
        print(self.current_dialogue)
        return self.dialogue() 
    def skip(self):
        if self.next(): return self.dialogue()
        else:   return " "," ",["_end"]

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
            print(self.current_dialogue)
            
            if self.next() :
                return self.dialogues["name"],dialogue,[]
            else:
                return self.dialogues["name"],dialogue,["_end"]
        

        if type(dialogue) == dict:
            print(self.current_dialogue)
            if "options" in dialogue:return self.dialogues["name"],dialogue["text"],dialogue["options"]
            
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
            else:
                if self.next(): return self.dialogues["name"],dialogue["text"],[]
                else:   return self.dialogues["name"],dialogue["text"],["_end"]
            #return dialogue
        if type(dialogue)==list:
            self.current_dialogue+="/0"
            return self.dialogue()
            
            
      return "_","_",["_end"]
