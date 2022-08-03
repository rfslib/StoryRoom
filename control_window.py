'''
file: control_window.py
author: rfslib
'''

from tkinter import *

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
        self.config(bg=cfg.c_bg_color)
        self.overrideredirect(True) # don't show title 
        self.attributes('-alpha', 1.0) # set transparency
        self.attributes('-topmost', 1) # stay on top

        # get our size and location
        self.xoffset = self.winfo_screenwidth( )
        #self.geometry( f'{cfg.tw_mwidth}x{cfg.tw_mheight}+{self.xoffset}+{cfg.tw_yoffset}')
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
        self.ttlframe = Frame( master=self, relief = RIDGE, borderwidth=5, bg=cfg.c_bg_color, padx=cfg.padxy, pady=cfg.padxy )
        self.ttlframe.grid(row=0, column=0, columnspan=3, padx=cfg.padxy, pady=cfg.padxy, sticky='ew')
        self.grid_columnconfigure( 0, weight=1 )
        self.ttllbl = Label(master=self.ttlframe, text=cfg.timer_waiting_message, font=(cfg.c_bold_font, cfg.fontsize), bg=cfg.c_bg_color, fg=cfg.fontcolor)
        self.ttllbl.pack(padx=cfg.padxy, pady=cfg.padxy)

        # the 'state/action' frame
        self.state_frame = Frame(master=self, bg=cfg.c_bg_color, padx=cfg.padxy, pady=cfg.padxy)
        self.state_frame.grid(row=1, column=0, columnspan=3, padx=cfg.padxy, pady=cfg.padxy, sticky='ew')
        self.state_line=StringVar()
        self.state_label = Label(master=self.state_frame, textvariable=self.state_line, fg=cfg.state_font_color, bg=cfg.c_bg_color,
                            font=(cfg.c_bold_font, cfg.state_font_size))
        self.state_label.grid(row=0, column=0, sticky='w')
        
        # create a frame for interactions (buttons, text entry, etc.)
        self.int_frame = Frame(master=self, bg=cfg.c_bg_color, padx=cfg.padxy, pady=cfg.padxy)
        self.int_frame.grid(row=2, column=0, padx=cfg.padxy, pady=cfg.padxy, sticky='ewn')
        
        self.btn_start= Button(self.int_frame, height=cfg.c_btn_height, relief=GROOVE, bg=cfg.c_btn_bg_color,
            text=cfg.start_btn_txt, font=(cfg.c_bold_font, cfg.c_btn_fontsize),
            command=self.start_callback)
        self.btn_start.grid(row=0, column=0, padx=cfg.padxy, pady=cfg.padxy)
        self.disable_start_button()
        
        self.btn_stop= Button(self.int_frame, height=cfg.c_btn_height, relief=GROOVE, bg=cfg.c_btn_bg_color,
            text=cfg.stop_btn_txt, font=(cfg.c_bold_font, cfg.c_btn_fontsize),
            command=self.stop_callback)
        self.btn_stop.grid(row=0, column=1, padx=cfg.padxy, pady=cfg.padxy)
        self.disable_stop_button()

        self._time_left = StringVar()
        self.time_left = Label(master=self.int_frame, textvariable=self._time_left, anchor='w',
            fg=cfg.info_fontcolor, bg=cfg.c_bg_color, font=(cfg.c_text_font, cfg.c_time_left_fontsize))
        self.time_left.grid(row=0, column=2, sticky='w')
        self.update

        # "info" frame
        self.info_frame = Frame(master=self, bg=cfg.c_bg_color, padx=cfg.padxy, pady=cfg.padxy)
        self.info_frame.grid(row=6, column=0, padx=cfg.padxy, pady=cfg.padxy, sticky = 'e')

        self.info_line_1 = StringVar()
        self.info_label_1 = Label(master=self.info_frame, textvariable=self.info_line_1, anchor='e',
            fg=cfg.info_fontcolor, bg=cfg.c_bg_color, font=(cfg.c_text_font, cfg.info_fontsize))
        self.info_label_1.grid(row=0, column=0, sticky='e')

        self.info_line_2 = StringVar()
        self.info_label_2 = Label(master=self.info_frame, textvariable=self.info_line_2, anchor='e', 
            fg=cfg.info_fontcolor, bg=cfg.c_bg_color, font=(cfg.c_text_font, cfg.info_fontsize))
        self.info_label_2.grid(row=1, column=0, sticky='e')

        self.info_line_3 = StringVar()
        self.info_label_3 = Label(master=self.info_frame, textvariable=self.info_line_3, anchor='e', 
            fg=cfg.info_fontcolor, bg=cfg.c_bg_color, font=(cfg.c_text_font, cfg.info_fontsize))
        self.info_label_3.grid(row=2, column=0, sticky='e')

        self.update()      
        if self._debug: print('control window ready')

        self.bind('<Control-Alt-F4>', self.exit_callback)

# ----

    def enable_start_button(self):
        self.btn_start.config(fg=cfg.c_btn_active_color)
        self.btn_start['state'] = NORMAL

    def disable_start_button(self):
        self.btn_start['state'] = DISABLED
        self.btn_start.config(fg=cfg.c_btn_idle_color)

    def enable_stop_button(self):
        self.btn_stop.config(fg=cfg.c_btn_active_color)
        self.btn_stop['state'] = NORMAL

    def disable_stop_button(self):
        self.btn_stop['state'] = DISABLED
        self.btn_stop.config(fg=cfg.c_btn_idle_color)

    def set_state_line(self, textin, text_color):
        self.state_label.config(fg=text_color)
        self.state_line.set(str(textin))
    
    def set_info_line_1(self, textin, text_color):
        self.info_label_1.config(fg=text_color)
        self.info_line_1.set(str(textin))

    def set_info_line_2(self, textin, text_color):
        self.info_label_2.config(fg=text_color)
        self.info_line_2.set(str(textin))

    def set_info_line_3(self, textin, text_color):
        self.info_label_3.config(fg=text_color)
        self.info_line_3.set(str(textin))

    def set_time_left(self, textin, text_color):
        self.time_left.config(fg=text_color)
        self._time_left.set(str(textin))


## --- testing stuff ensues
#         
def test_exit_callback(e):
    print(f'>>> exiting ({e})')
    tst.destroy()
    root.destroy()

if __name__ == '__main__':
    root = Tk()
    root.geometry( '300x100+0+0' )
    root.title( 'close me to exit test' )
    tst = Control_Window(root, None, None, test_exit_callback, debug=True )
    tst.set_state_line('Stately State', cfg.state_font_color)
    tst.set_info_line_1(cfg.info_line.format('Main System', 'test', 0), cfg.c_text_soft_color)
    tst.set_info_line_2(cfg.info_line.format('Backup System', 'test', 0), cfg.c_text_soft_color)
    tst.set_info_line_3(cfg.info_line.format('USB', 'test', 0), cfg.c_text_soft_color)
    root.mainloop()
