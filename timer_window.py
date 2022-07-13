"""
file: timer_window.py
author: rfslib

references:
    https://delfstack.com/howto/python-tkinter/how-to-change-the-tkinter-label-text

"""
from tkinter import *
from sr_parm import SR_Parm as parms

class Timer_Window(Toplevel):
    debug = 0
    logit = 0
    foo = 0

    ## countdown stuff
    tw_countdown_seconds = 10
    tw_countdown_active = False
    tw_countdown_complete = False
    tw_countdown_interval = 1
    tw_countdown_warn = 5
    tw_countdown_return = 0 # non-zero value means exec callback at n seconds
    tw_countdown_string = '{} seconds remaining'
    tw_countdown_abort = False
   
    def __init__(self, master):
        Toplevel.__init__(self,master)

        # set our look
        self.config( bg=parms.tw_normbg)
        self.attributes( '-alpha', parms.tw_normalpha ) # set transparency
        self.overrideredirect( True ) # hide the title bar  
        self.attributes('-topmost', 1) # stay on top     
    
        # set our size and location
        self.xoffset = self.winfo_screenwidth( )
        self.geometry( f'{parms.tw_mwidth}x{parms.tw_mheight}+{self.xoffset}+{parms.tw_yoffset}')

        self._txt = StringVar()
        self._txt.set( 'waiting for start' )
        self.lab = Label( master=self, textvariable=self._txt, font=( parms.tw_font, parms.tw_fontsize), 
            fg=parms.tw_fontwarn, bg=parms.tw_warnbg
            )
        self.lab.pack( padx=parms.tw_padxy * 2, pady=parms.tw_padxy, side='left')
        self.lab.config( bg=parms.tw_normbg )

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

    def start_countdown( self, textstring: str, seconds:int , interval: int, warn_at: int, return_at: int, callback ):
        if self.tw_countdown_active: return -1 # a countdown is already active, can't start another
        self.tw_countdown_active = True # set "in-countdown" flag
        if self.logit: print( f'count down {seconds} seconds, update every {interval} seconds')
        self.tw_countdown_string = textstring
        self.countdown_callback = callback
        self.tw_countdown_seconds = seconds
        self.tw_countdown_interval = interval
        self.tw_countdown_warn = warn_at
        self.tw_countdown_return = return_at
        self.tw_countdown_complete = False
        self.tw_countdown_abort = False
        self.attributes( '-alpha', parms.tw_normalpha )
        self.config( bg=parms.tw_normbg )
        self.countdown()  # start the countdown

    def stop_countdown(self, new_callback): # tell the current countdown to stop early
        self.countdown_callback = new_callback
        self.tw_countdown_abort = True

    def countdown( self ):
        if self.tw_countdown_abort: # early stop flag set
            self.set_txt('Stopped')
            if self.logit: print( 'countdown aborted')
            self.attributes( '-alpha', parms.tw_normalpha )
            self.config( bg=parms.tw_normbg )
            self.lab.config( bg=parms.tw_normbg )
            self.tw_countdown_complete = True
            self.tw_countdown_active = False # clear in-countdown flag
            self.countdown_callback()
        elif self.tw_countdown_seconds > self.tw_countdown_return: # still time left
            if self.tw_countdown_seconds <= self.tw_countdown_warn:
                self.attributes( '-alpha', parms.tw_warnalpha )
                self.config( bg=parms.tw_warnbg )
                self.lab.config( bg=parms.tw_warnbg )
            if not ( self.tw_countdown_seconds % self.tw_countdown_interval ): # update at every 'interval'
                self.set_txt( self.tw_countdown_string.format( int( self.tw_countdown_seconds / self.tw_countdown_interval ) ) )
                if self.logit: print( f'countdown at {self.tw_countdown_seconds} seconds')
            self.tw_countdown_seconds -= 1
            self.after( 1000, self.countdown )
        else: # time is up
            self.set_txt( '' )
            if self.logit: print( 'countdown complete')
            self.attributes( '-alpha', parms.tw_normalpha )
            self.config( bg=parms.tw_normbg )
            self.lab.config( bg=parms.tw_normbg )
            self.tw_countdown_complete = True
            self.tw_countdown_active = False # clear in-countdown flag
            self.countdown_callback()

    # TODO: def stop_countdown( self ) # normal stop, or early stop


if __name__ == '__main__':
    root = Tk()
    root.geometry( '300x100+0+0' )
    root.title( 'close me to exit test' )
    tst = Timer_Window( root )
    root.mainloop()