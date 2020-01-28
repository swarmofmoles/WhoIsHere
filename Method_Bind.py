from tkinter import *
import clipboard

root = Tk()
class TextEntry:
    def __init__(self):
        self.e = Entry(root,width = 20)
        self.list = Listbox(root,width = 20,height = 20)
        self.e.bind('<Return>',self.change)
        self.list.bind('<Double-Button-1>',lambda event , a = ANCHOR: self.DoubleClick(event,a))
        
        
        self.e.pack()
        self.list.pack()
    def change(self,event):
        self.e['bg'] = "red"
        self.list.insert(END,self.e.get())
    def DoubleClick(self,event,position):

        self.e.delete(0,len(self.e.get()))
        self.e.insert(0,self.list.get(position))
        print(self.list.get(position))

    def clipenter(self,event):

        for i in clipboard.paste().splitlines():
            self.list.insert(END,i)
            print(i)
 
        
    
        
def key(event):

    print("SPACE")
    
textentry = TextEntry()
root.bind("<Control-v>",textentry.clipenter)

root.mainloop()



