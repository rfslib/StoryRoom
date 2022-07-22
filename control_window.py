'''
file: control_window.py
author: rfslib
'''

from tkinter import *

free_disk = 0

class Control_Window(Toplevel):

    def __init__(self, master, parms, start_callback, stop_callback, exit_callback, debug=False):
        Toplevel.__init__(self, master)

        self._debug = debug

        self.prm = parms
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.exit_callback = exit_callback

        # set our look
        self.config(bg=self.prm.bg_color)
        self.overrideredirect(True) # don't show title 
        self.attributes('-alpha', 1.0) # set transparency
        self.attributes('-topmost', 1) # stay on top

        # get our size and location
        self.mwidth = self.winfo_screenwidth()
        self.mheight = self.winfo_screenheight()
        self.moffsetx = 0
        self.moffsety = 0
        if self._debug:
            self.mwidth = int( self.mwidth / 2 ) 
            self.mheight = int( self.mheight / 2 ) 
            self.moffsetx = 48
            self.moffsety = 48
        self.geometry( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}')
        if self._debug: print( f'{self.mwidth}x{self.mheight}+{self.moffsetx}+{self.moffsety}' )
        self.resizable(False, False)

        # set up the window's "title" frame
        self.ttlframe = Frame( master=self, relief = RIDGE, borderwidth=5, bg=self.prm.bg_color, padx=self.prm.padxy, pady=self.prm.padxy )
        self.ttlframe.grid(row=0, column=0, columnspan=3, padx=self.prm.padxy, pady=self.prm.padxy, sticky='ew')
        self.grid_columnconfigure( 0, weight=1 )
        self.ttllbl = Label(master=self.ttlframe, text=self.prm.timer_waiting_message, font=(self.prm.font_bold, self.prm.fontsize), bg=self.prm.bg_color, fg=self.prm.fontcolor)
        self.ttllbl.pack(padx=self.prm.padxy, pady=self.prm.padxy)

        # create a frame for interactions (buttons, text entry, etc.)
        self.btnframe = Frame(master=self, bg=self.prm.bg_color, padx=self.prm.padxy, pady=self.prm.padxy)
        self.btnframe.grid(row=2, column=0, padx=self.prm.padxy, pady=self.prm.padxy, sticky='ewn')
        self.ctrl_strt= Button(self.btnframe, height=self.prm.btn_height, relief=GROOVE, bg=self.prm.btn_bg_color,
            text=self.prm.start_btn_txt, font=(self.prm.font_bold, self.prm.btn_fontsize),
            command=self.start_callback)
        self.ctrl_strt.grid(row=0, column=0, padx=self.prm.padxy, pady=self.prm.padxy)
        self.disable_start_button()
        self.ctrl_stop= Button(self.btnframe, height=self.prm.btn_height, relief=GROOVE, bg=self.prm.btn_bg_color,
            text=self.prm.stop_btn_txt, font=(self.prm.font_bold, self.prm.btn_fontsize),
            command=self.stop_callback)
        self.ctrl_stop.grid(row=0, column=1, padx=self.prm.padxy, pady=self.prm.padxy)
        self.disable_stop_button()
        self.update

        # "info" frame
        self.infoline=StringVar()
        self.diskline=StringVar()
        self.infframe = Frame(master=self, bg=self.prm.bg_color, padx=self.prm.padxy, pady=self.prm.padxy)
        self.infframe.grid(row=6, column=0, padx=self.prm.padxy, pady=self.prm.padxy, sticky = 'es')
        self.inflabel = Label(master=self.infframe, textvariable=self.infoline, fg=self.prm.info_fontcolor, bg=self.prm.bg_color,
            font=(self.prm.font_family, self.prm.info_fontsize))
        self.inflabel.pack(padx=self.prm.padxy, pady=self.prm.padxy)
        self.dsklabel = Label(master=self.infframe, textvariable=self.diskline, fg=self.prm.info_fontcolor, bg=self.prm.bg_color,
            font=(self.prm.font_family, self.prm.info_fontsize))
        self.dsklabel.pack(padx=self.prm.padxy, pady=self.prm.padxy)
        self.update()
              
        if self._debug: 
            self.bind('<Escape>', self.exit_callback)
            print('control window ready')

# ----

    def enable_start_button(self):
        self.ctrl_strt.config(fg=self.prm.btn_active_color)
        self.ctrl_strt['state'] = NORMAL

    def disable_start_button(self):
        self.ctrl_strt['state'] = DISABLED
        self.ctrl_strt.config(fg=self.prm.btn_idle_color)

    def enable_stop_button(self):
        self.ctrl_stop.config(fg=self.prm.btn_active_color)
        self.ctrl_stop['state'] = NORMAL

    def disable_stop_button(self):
        self.ctrl_stop['state'] = DISABLED
        self.ctrl_stop.config(fg=self.prm.btn_idle_color)

    def set_infoline(self, textin, text_color):
        self.inflabel.config(fg=text_color)
        self.infoline.set(str(textin))

    def set_diskline(self, textin, text_color):
        self.dsklabel.config(fg=text_color)
        self.diskline.set(str(textin))

def test_start_callback():
    pass

def test_stop_callback():
    pass

def test_exit_callback(e):
    tst.destroy()
    root.destroy()

if __name__ == '__main__':
    from sr_parm import SR_Parm as parms
    root = Tk()
    root.geometry( '300x100+0+0' )
    root.title( 'close me to exit test' )
    tst = Control_Window(root, parms, test_start_callback, test_stop_callback, test_exit_callback, debug=True )
    tst.set_infoline(parms.info_line.format('?','?','?'), parms.text_soft_color)
    tst.set_diskline(parms.disk_line.format(0), parms.text_soft_color)
    root.mainloop()
