import clipboard
import Esi
import time
import User_base
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Canvas


  
class Table(tk.Frame):  
    def __init__(self, parent=None, rows=tuple()):
        super().__init__(parent)
        
        self.table = ttk.Treeview(self, show="headings", selectmode="browse")


        columns = ('Nickname','Corporation','Alliance','Sec status','Ship Kill','Solo Kill','Ship Lost','Gang Ratio')
        self.table =  ttk.Treeview(self, columns = columns, show='headings')
        
        for col in columns:
            self.table.heading(col,text=col,command=lambda c=col: self.treeview_sort_column(self.table, c,True))
            self.table.column(col,width=120)
  
        for row in rows:
            #print("row" ,row)
            self.table.insert('', tk.END, values=tuple(row))
  
        scrolltable = tk.Scrollbar(self, command=self.table.yview)
        self.table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(expand=tk.YES, fill=tk.BOTH)
        self.c = Canvas(self,width =30,height =30,bg= "white")
        
        self.c.pack(padx = 10,side ='left')
        
        self.label_info = tk.Label(self,text = "XXXXXX",height = 2)
        self.label_info.pack( side='bottom')#expand=tk.YES, ,fill=tk.Y,
        self.click_timer = 0


    def on_tree_select(self,event):
        self.c.create_oval(3,3,30,30,fill = "red")
        self.c.update()
        self.table.bind('<ButtonPress-1>', self.start_motor )
        self.table.bind('<ButtonRelease-1>',self.stop_motor)
        #print(self.click_timer, '   Click time ')
        
            

    def start_motor(self,event):
        
        self.click_timer = time.time()
        print(time.ctime(self.click_timer), " start ")
        
        
        print("start", '{0:.2f}'.format(self.click_timer))
            

    def stop_motor(self,event):
        self.click_timer = time.time() - self.click_timer
        print('{0:.2f}'.format(self.click_timer), " stop")
        #print(time.ctime(self.click_timer), " stop")
        if self.click_timer > 2:
            print('Select item: ')
    ##        for item in self.table.selection():
    ##            item_text = self.table.item(item,"text")
    ##            print(item_text)
            print(self.table.item(self.table.selection())['values'][0])
            url = User_base.user_url_req(self.table.item(self.table.selection())['values'][0])
            #print("on tree: ",url)
            clipboard.copy(url)
            self.c.create_oval(3,3,30,30,fill = "green")
            self.c.update()
            self.label_info['text'] = "скопировано"
            print("self.VIBOR: ",self.click_timer, " Skopirovano")
            self.click_timer = 0
            
            time.sleep(1)
            self.c.delete("all")
        self.c.delete("all")
        
        


    def the_choice_column(self,event):
        if self.table.identify_region(event.x,event.y) == "heading" :
            
            col = self.table.column(self.table.identify_column(event.x))['id']
            self.treeview_sort_column(self.table,col,reverse = False)
        
    def treeview_sort_column(self,table, col,reverse):
        l = [(self.table.set(k, col),  k) for k in self.table.get_children()]

        
        
        if col == "Ship Kill" or col == "Solo Kill" or col == "Ship Lost" or col == "Gang Ratio":
            l.sort(key=lambda t: int(t[0]),reverse=reverse)
        elif col == "Sec status":
            l.sort(key=lambda t: float(t[0]),reverse=reverse)
        else:
            l.sort(reverse=reverse)
    

        for index, (val, k) in enumerate(l):
            self.table.move(k, '', index)

        self.table.heading(col, command=lambda: \
                           self.treeview_sort_column(self.table, col, not reverse))

  
        

        
    def enterclipboard(self,event):
        #Вставка информации о пользователе из буфера обмена
        user_pl= []
       
        for i in clipboard.paste().splitlines():
            user_pl.append(i.strip())
        self.startTime = time.time()
        self.enterdatatable(user_pl)
        
    def enterdatatable(self,user_pl):
        #вставка в таблицу
        print("data ", user_pl)
        i = 0
        b = []
        z = ()
        o=0
        i= 0
        L = []
        #user_search = 
       
        for i in range(len(user_pl)):
            b.append([])


            self.label_info.configure(text = "Обрабатываю информацию о пользователе: " + user_pl[i] + " Осталось обработать: " + str(int(len(user_pl)) - i) )
            root.update()

            users =  User_base.search_nicknames(user_pl[i])
            print("LOOOP USERS",users,users[0])
            for l in range(1):
  
                users[0],users[1],users[2]
                b[i].append(users[0])
                print("B(i)  " , b[i])
                b[i].append(users[1])
                b[i].append(users[2])
                b[i].append(users[3])
                b[i].append(users[4])
                b[i].append(users[5])
                b[i].append(users[6])
                b[i].append(users[7])
                
                
        z = b
        rows = z
        for i in self.table.get_children():
            self.table.delete(i)
        for row in rows:

            self.table.insert('', tk.END, values=tuple(row))
        end_time = "Работа выполнена за: {:.3} sec".format(time.time() - self.startTime)
        self.label_info.configure(text = end_time)



 



if __name__ == "__main__":
    User_base.create_db()
    root = tk.Tk()
    root.lift()
    table= Table()
    root.title(u'WhoIsHere')
    z = [('Вставьте данные',' Ctrl + V',' Please OFF',' Caps Lock ') ]
   
    table = Table(root,  rows=z)

    root.bind("<Control-v>",table.enterclipboard)
    root.bind("<Control-igrave>", table.enterclipboard)
    root.bind('<<TreeviewSelect>>',table.on_tree_select)
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()



    
 



