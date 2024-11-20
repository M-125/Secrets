
class Inventory:
    def __init__(self) -> None:
        self.Items=[]
        self.dialogueItems=[]
    
    def PickUp(self,Item):
        Item.remove(Item.window)
        self.Items.append(Item)
    def Drop(self,Item):
        self.Items.remove(Item)
    def has_item(self,name):
        for e in self.Items:
            if e.name==name:
                return True
        return False
    def has_dialogue_item(self,name):
        for e in self.dialogueItems:
            if e==name:
                return True
        return False
    
    def add_dialogue_item(self,name):
        if not self.has_dialogue_item(name):
            self.dialogueItems.append(name)
    
    def add_item(self,Item):
        self.Items.append(Item)