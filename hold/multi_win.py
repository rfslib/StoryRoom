"""
https://stackoverflow.com/questions/36315156/how-do-i-run-multiple-tkinter-windows-simultaneously-in-python
"""

from tkinter import *
#from threading import Thread #no longer needed

class type1(Toplevel):
    nid = 0
    message = ""

    def __init__(self, master, nid, title, message):
      Toplevel.__init__(self,master)
      self.nid = nid 
      self.title(title) #since toplevel widgets define a method called title you can't store it as an attribute

      self.message = message
      self.display_note_gui() #maybe just leave that code part of the __init__?


    def display_note_gui(self): 
      '''Tkinter to create a note gui window with parameters '''    
      #no window, just self
      self.geometry("200x200")
      self.configure(background="#BAD0EF")
      #pass self as the parent to all the child widgets instead of window
      title = Entry(self,relief=FLAT, bg="#BAD0EF", bd=0)
      title.pack(side=TOP)
      scrollBar = Scrollbar(self, takefocus=0, width=20)
      self.textArea = Text(self, height=4, width=1000, bg="#BAD0EF", font=("Times", "14"))
      scrollBar.pack(side=RIGHT, fill=Y)
      self.textArea.pack(side=LEFT, fill=Y)
      scrollBar.config(command=self.textArea.yview)
      self.textArea.config(yscrollcommand=scrollBar.set)
      self.textArea.insert(END, self.message)
      #self.mainloop() #leave this to the root window
      self.upd()

      
    def run(self):
      self.display_note_gui()


    def msg(self, txt):
        self.textArea.insert( END, txt )


    def upd( self ):
        self.msg( '. \n' )
        self.after( 1000, self.upd ) 


class type2(Toplevel):
    nid = 0
    message = ""

    def __init__(self, master, nid, title, message):
      Toplevel.__init__(self,master)
      self.nid = nid
      self.attributes( '-alpha', 0.5 ) 
      self.message = message
      self.display_note_gui() #maybe just leave that code part of the __init__?


    def display_note_gui(self): 
      '''Tkinter to create a note gui window with parameters '''    
      #no window, just self
      self.geometry("200x200")
      self.configure(background="#BAD0EF")
      #pass self as the parent to all the child widgets instead of window
      title = Entry(self,relief=FLAT, bg="#BAD0EF", bd=0)
      title.pack(side=TOP)
      scrollBar = Scrollbar(self, takefocus=0, width=20)
      self.textArea = Text(self, height=4, width=1000, bg="#BAD0EF", font=("Times", "14"))
      scrollBar.pack(side=RIGHT, fill=Y)
      self.textArea.pack(side=LEFT, fill=Y)
      scrollBar.config(command=self.textArea.yview)
      self.textArea.config(yscrollcommand=scrollBar.set)
      self.textArea.insert(END, self.message)
      #self.mainloop() #leave this to the root window
      self.upd()


    def run(self):
      self.display_note_gui()


    def msg(self, txt):
        self.textArea.insert( END, txt )


    def upd( self ):
        self.msg( '. \n' )
        self.after( 1000, self.upd ) 
        

root = Tk()
root.withdraw() #hide the root so that only the notes will be visible

new_note1 = type1(root, 0, "Hello", "Hi, how are you?")
#new_note1.start()
#new_note1.join()


new_note2 = type2(root, 1, "2", "How's everyone else?")
#new_note2.start()
#new_note2.join()

root.mainloop() #still call mainloop on the root