from classes import dialogue
dia=dialogue.Dialogue("dial1")
Input=""
opt=""
while opt!="ended":
 
 name,text,opt=dia.dialogue(Input)
 print(name,text)

 Input=input(opt)