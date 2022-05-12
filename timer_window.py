"""
    file: timer_window.py
    author: ed c
"""

from tkinter import *

class Timer_Window( Toplevel ):

    debug = 1

    txt = 'timer here'
    ## attributes of the control window
    moffsetx = 0
    moffsety = 400
    mheight = 100
    font = 'Lucida Console'    # primary font for text
    fontsize = 64              # font size
    fontcolor = 'DarkGrey'
    warncolor = "DarkRed"
    alpha = 0.5
    padxy = 4                   # padding inside of frames
    btn_fontsize = 12

    def __init__(self, master):
        Toplevel.__init__(self,master)

        # set our look
        self.overrideredirect( True )
        self.attributes( '-alpha', self.alpha )
    
        # set our size and location
        self.mwidth = self.winfo_screenwidth( )
        print( f'mwidth: {self.mwidth}')
        self.geometry( f'{600}x{self.mheight}+{ -200}+{self.moffsety}')
#---
        self.frame = Frame( master=self,
            borderwidth = self.padxy,
            padx = self.padxy, pady = self.padxy )
        self.frame.grid( row=0, column=0, padx = self.padxy, pady = self.padxy )
        self.grid_columnconfigure( 0, weight=1 )
        self.lbl = Label( master=self.frame,
            text=self.txt, font=('Lucida Console', self.fontsize),
            ).pack( padx = self.padxy, pady = self.padxy)

        self.upd( )

        if self.debug: print( 'timer window ready' )

    def upd( self ):
        print( 'timer upd called' )
        #self.lbl( text='foo')
        self.after( 1000, self.upd )

if __name__ == '__main__':
    root = Tk()
    root.geometry( '300x100+0+0' )
    root.title( 'close me to exit test' )
    tst = Timer_Window( root )
    root.mainloop()