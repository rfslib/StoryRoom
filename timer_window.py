"""
    file: timer_window.py
    author: ed c

    references:
        https://delfstack.com/howto/python-tkinter/how-to-change-the-tkinter-label-text

"""


from itertools import count
from subprocess import call
from tkinter import *
from turtle import color

class Timer_Window( Toplevel ):

    debug = 0
    logit = 0
    foo = 0

    ## countdown stuff
    countdown_seconds = 10
    countdown_active = False
    countdown_complete = False
    countdown_interval = 1
    countdown_warn = 5
    countdown_string = '{} seconds remaining'

    ## attributes of the control window
    #moffsetx = 0
    mwidth = 1920
    yoffset = 0
    xoffset = 0
    mheight = 100
    font = 'Lucida Console'    # primary font for text
    fontsize = 64              # font size
    fontcolor = 'DarkGrey'
    fontwarn = 'Black' # 'DarkRed'
    normbg = 'Grey' # 'Grey'
    warnbg = 'DarkRed'
    normalpha = 0.5
    warnalpha = 0.9
    padxy = 4                   # padding inside of frames
    btn_fontsize = 12

    def __init__(self, master):
        Toplevel.__init__(self,master)

        # set our look
        self.config( bg=self.normbg)
        self.attributes( '-alpha', self.normalpha ) # set transparency
        self.overrideredirect( True ) # hide the title bar
        
    
        # set our size and location
        self.xoffset = self.winfo_screenwidth( )
        self.geometry( f'{self.mwidth}x{self.mheight}+{self.xoffset}+{self.yoffset}')

        self._txt = StringVar()
        self._txt.set( 'waiting for start' )
        self.lab = Label( master=self, textvariable=self._txt, font=('Lucida Console', self.fontsize), 
            fg=self.fontwarn, bg=self.warnbg
            )
        self.lab.pack( padx=self.padxy * 2, pady=self.padxy, side='left')
        self.lab.config( bg=self.normbg )

        if self.debug: self.upd( )
        if self.logit: print( 'timer window ready' )

    def get_txt( self ):
        return self._txt

    def set_txt( self, textin ):
        self._txt.set( str( textin ) )

    def upd( self ):
        if self.debug: print( 'timer upd called' )
        self.set_txt( self.foo  )
        self.foo += 1
        self.after( 1000, self.upd )

    def start_countdown( self, textstring, seconds, interval, warn_at, callback ):
        if self.countdown_active: return -1 # a countdown is already active, can't start another
        self.countdown_active = True # set "in-countdown" flag
        if self.logit: print( f'count down {seconds} seconds, update every {interval} seconds')
        self.countdown_string = textstring
        self.countdown_callback = callback
        self.countdown_seconds = seconds
        self.countdown_interval = interval
        self.countdown_warn = warn_at
        self.countdown_complete = False
        self.attributes( '-alpha', self.normalpha )
        self.config( bg=self.normbg )
        self.countdown()  # start the countdown

    def countdown( self ):
        if self.countdown_seconds > 0:
            if self.countdown_seconds <= self.countdown_warn:
                self.attributes( '-alpha', self.warnalpha )
                self.config( bg=self.warnbg )
                self.lab.config( bg=self.warnbg )
            if not ( self.countdown_seconds % self.countdown_interval ): # update at every 'interval'
                self.set_txt( self.countdown_string.format( int( self.countdown_seconds / self.countdown_interval ) ) )
                if self.logit: print( f'countdown at {self.countdown_seconds} seconds')
            self.countdown_seconds -= 1
            self.after( 1000, self.countdown )
        else:
            self.set_txt( '' )
            if self.logit: print( 'countdown complete')
            self.attributes( '-alpha', self.normalpha )
            self.config( bg=self.normbg )
            self.lab.config( bg=self.normbg )
            self.countdown_complete = True
            self.countdown_active = False # clear in-countdown flag
            self.countdown_callback()

    # TODO: def stop_countdown( self ) # normal stop, or early stop


if __name__ == '__main__':
    root = Tk()
    root.geometry( '300x100+0+0' )
    root.title( 'close me to exit test' )
    tst = Timer_Window( root )
    root.mainloop()