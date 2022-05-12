"""
    file: control_window.py
    author: ed c
"""

from tkinter import *

class Control_Window(Toplevel):

    debug = 1

    ## attributes of the console screen
    mwidth = 500
    mheight = 300
    moffsetx = 0
    moffsety = 200
    ctrl_title = 'Story Room'       # title
    ctrl_font = 'Lucida Console'    # primary font for text
    ctrl_fontsize = 48              # font size
    ctrl_fontcolor = '#100010'
    ctrl_entry = 'set filename'     # Button text for filename entry
    ctrl_entrysize = 12             # font size for filename entry
    ctrl_bg = '#efffef'             # background color
    frame_pad = 4                   # padding inside of frames

    def __init__(self, master):
        Toplevel.__init__(self,master)

        # set our look
        self.config( bg=self.ctrl_bg)
        self.overrideredirect( True )
    
        # get our size and location
        self.mwidth = self.winfo_screenwidth( )
        self.mheight = self.winfo_screenmmheight( )
        if not self.debug:
            self.moffsetx = 0
            self.moffsety = 0
        self.geometry( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}')

        # #pass self as the parent to all the child widgets instead of window
        # title = Entry(self,relief=FLAT, bg="#BAD0EF", bd=0)
        # title.pack(side=TOP)
        # scrollBar = Scrollbar(self, takefocus=0, width=20)
        # self.textArea = Text(self, height=4, width=1000, bg="#BAD0EF", font=("Times", "14"))
        # scrollBar.pack(side=RIGHT, fill=Y)
        # self.textArea.pack(side=LEFT, fill=Y)
        # scrollBar.config(command=self.textArea.yview)
        # self.textArea.config(yscrollcommand=scrollBar.set)
        # self.textArea.insert(END, self.message)
        #self.mainloop() #leave this to the root window
        self.upd()

      
    def run(self):
      self.display_note_gui()


    def msg(self, txt):
        self.textArea.insert( END, txt )


    def upd( self ):
        self.msg( '. \n' )
        self.after( 1000, self.upd ) 
