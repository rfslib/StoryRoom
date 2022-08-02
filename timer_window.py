"""
file: timer_window.py
author: rfslib
"""

from tkinter import *

from sr_parm import SR_Parm as cfg

class Timer_Window(Toplevel):
    debug = False

    def __init__(self, master):
        Toplevel.__init__(self,master)
        
        # set our look
        self.config(bg=cfg.tw_normbg)
        self.attributes('-alpha', cfg.tw_normalpha) # set transparency
        self.overrideredirect(True) # hide the title bar  
        self.attributes('-topmost', 1) # stay on top     
    
        # set our size and location
        self.xoffset = self.winfo_screenwidth( )
        self.geometry( f'{cfg.tw_mwidth}x{cfg.tw_mheight}+{self.xoffset}+{cfg.tw_yoffset}')

        self._txt = StringVar()
        self._txt.set('waiting for start')
        self._txt_label = Label(master=self, textvariable=self._txt,
            font=(cfg.tw_font, cfg.tw_fontsize), fg=cfg.tw_fontwarn, bg=cfg.tw_warnbg)
        self._txt_label.pack(padx=cfg.tw_padxy * 2, pady=cfg.tw_padxy, side='left')
        self._txt_label.config(bg=cfg.tw_normbg )

        if self.debug:
            print('>>> timer_window: ready')

    def set_txt(self, textin):        
        self._txt.set(str(textin))

    def set_bg(self, background):
        self.config(bg=background)

    def set_fg(self, foreground):
        self.config(fg=foreground)

    def set_label_bg(self, background):
        self._txt_label.config(bg=background)

    def set_alpha(self, alpha):
        self.attributes('-alpha', alpha)

if __name__ == '__main__':
    from time import sleep
    ctr = 0
    root = Tk()
    root.geometry('300x100+0+0')
    root.title('close me to exit test')
    tst = Timer_Window(root)
    root.mainloop()