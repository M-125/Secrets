from classes import dialogue,inventory
inv=inventory.Inventory()
dia=dialogue.Dialogue("dial1",inv)
Input=""
opt=""
while opt!=["_end"]:
 
 name,text,opt=dia.dialogue(Input)
 print(f"\n__________________\n[{name}]   {text}")

 Input=input("options: "+str(opt)+"\n__________________\n>")