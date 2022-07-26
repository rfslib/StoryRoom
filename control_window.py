'''
file: control_window.py
author: rfslib
'''

from tkinter import *
from tkinter import ttk

from sr_parm import SR_Parm as cfg

free_disk = 0

class Control_Window(Toplevel):

    def __init__(self, master, start_callback, stop_callback, exit_callback, debug=False):
        Toplevel.__init__(self, master)

        self._debug = debug

        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.exit_callback = exit_callback

        # set our look
        self.config(bg=cfg.bg_color)
        self.overrideredirect(True) # don't show title 
        self.attributes('-alpha', 1.0) # set transparency
        self.attributes('-topmost', 1) # stay on top

        # get our size and location
        self.mwidth = self.winfo_screenwidth()
        self.mheight = self.winfo_screenheight()
        self.moffsetx = 0
        self.moffsety = 0
        if self._debug: # full-width, half-height, down a little
            self.moffsety = 48
            self.mheight = int(self.mheight / 2)
            self.moffsetx = 0
            
        self.geometry( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}')
        if self._debug: print( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}' )
        self.resizable(False, False)

        # set up the window's "title" frame
        self.ttlframe = Frame( master=self, relief = RIDGE, borderwidth=5, bg=cfg.bg_color, padx=cfg.padxy, pady=cfg.padxy )
        self.ttlframe.grid(row=0, column=0, columnspan=3, padx=cfg.padxy, pady=cfg.padxy, sticky='ew')
        self.grid_columnconfigure( 0, weight=1 )
        self.ttllbl = Label(master=self.ttlframe, text=cfg.timer_waiting_message, font=(cfg.font_bold, cfg.fontsize), bg=cfg.bg_color, fg=cfg.fontcolor)
        self.ttllbl.pack(padx=cfg.padxy, pady=cfg.padxy)

        # the 'state/action' frame
        self.state_frame = Frame(master=self, bg=cfg.bg_color, padx=cfg.padxy, pady=cfg.padxy)
        self.state_frame.grid(row=1, column=0, columnspan=3, padx=cfg.padxy, pady=cfg.padxy, sticky='ew')
        self.state_line=StringVar()
        self.state_label = Label(master=self.state_frame, textvariable=self.state_line, fg=cfg.state_font_color, bg=cfg.bg_color,
                            font=(cfg.font_bold, cfg.state_font_size))
        self.state_label.grid(row=0, column=0, sticky='w')
        

        # create a frame for interactions (buttons, text entry, etc.)
        self.int_frame = Frame(master=self, bg=cfg.bg_color, padx=cfg.padxy, pady=cfg.padxy)
        self.int_frame.grid(row=2, column=0, padx=cfg.padxy, pady=cfg.padxy, sticky='ewn')
        self.btn_start= Button(self.int_frame, height=cfg.btn_height, relief=GROOVE, bg=cfg.btn_bg_color,
            text=cfg.start_btn_txt, font=(cfg.font_bold, cfg.btn_fontsize),
            command=self.start_callback)
        self.btn_start.grid(row=0, column=0, padx=cfg.padxy, pady=cfg.padxy)
        self.disable_start_button()
        self.btn_stop= Button(self.int_frame, height=cfg.btn_height, relief=GROOVE, bg=cfg.btn_bg_color,
            text=cfg.stop_btn_txt, font=(cfg.font_bold, cfg.btn_fontsize),
            command=self.stop_callback)
        self.btn_stop.grid(row=0, column=1, padx=cfg.padxy, pady=cfg.padxy)
        self.disable_stop_button()
        self.update

        # "info" frame
        self.info_frame = Frame(master=self, bg=cfg.bg_color, padx=cfg.padxy, pady=cfg.padxy)
        self.info_frame.grid(row=6, column=0, padx=cfg.padxy, pady=cfg.padxy, sticky = 'e')

        self.info_line_1=StringVar()
        self.info_label_1 = Label(master=self.info_frame, textvariable=self.info_line_1, anchor='e',
            fg=cfg.info_fontcolor, bg=cfg.bg_color, font=(cfg.font_family, cfg.info_fontsize))
        self.info_label_1.grid(row=0, column=0, sticky='e')

        self.info_line_2=StringVar()
        self.info_label_2 = Label(master=self.info_frame, textvariable=self.info_line_2, anchor='e', 
            fg=cfg.info_fontcolor, bg=cfg.bg_color, font=(cfg.font_family, cfg.info_fontsize))
        self.info_label_2.grid(row=1, column=0, sticky='e')
        self.update()
              
        if self._debug: 
            self.bind('<Escape>', self.exit_callback)
            print('control window ready')

# ----

    def enable_start_button(self):
        self.btn_start.config(fg=cfg.btn_active_color)
        self.btn_start['state'] = NORMAL

    def disable_start_button(self):
        self.btn_start['state'] = DISABLED
        self.btn_start.config(fg=cfg.btn_idle_color)

    def enable_stop_button(self):
        self.btn_stop.config(fg=cfg.btn_active_color)
        self.btn_stop['state'] = NORMAL

    def disable_stop_button(self):
        self.btn_stop['state'] = DISABLED
        self.btn_stop.config(fg=cfg.btn_idle_color)

    def set_state_line(self, textin, text_color):
        self.state_label.config(fg=text_color)
        self.state_line.set(str(textin))
    
    def set_info_line_1(self, textin, text_color):
        self.info_label_1.config(fg=text_color)
        self.info_line_1.set(str(textin))

    def set_info_line_2(self, textin, text_color):
        self.info_label_2.config(fg=text_color)
        self.info_line_2.set(str(textin))

def test_start_callback():
    pass

def test_stop_callback():
    pass

def test_exit_callback(e):
    tst.destroy()
    root.destroy()

if __name__ == '__main__':
    root = Tk()
    root.geometry( '300x100+0+0' )
    root.title( 'close me to exit test' )
    tst = Control_Window(root, test_start_callback, test_stop_callback, test_exit_callback, debug=True )
    tst.set_state_line('Stately State', cfg.state_font_color)
    tst.set_info_line_1(cfg.info_line.format('Main', 'test', 0), cfg.text_soft_color)
    tst.set_info_line_2(cfg.info_line.format('Backup', 'test', 0), cfg.text_soft_color)
    root.mainloop()
