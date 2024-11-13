
class Inventory:
    def __init__(self) -> None:
        self.Items=[]
        self.dialogueItems=[]
    
    def PickUp(self,Item):
        Item.remove(Item.window)
        self.Items.append(Item)
    