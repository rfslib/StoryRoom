'''
file: control_window.py
author: rfslib
'''

from tkinter import *

import logging

from story_room_config import RecordingState, StoryRoomConfiguration as cfg

free_disk = 0

class ControlWindow(Toplevel):

    def __init__(self, master, start_callback, stop_callback, exit_callback, logger:logging):
        Toplevel.__init__(self, master)

        logger.info('ControlWindow init started')

        self._debug = False

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
        self.ttllbl = Label(master=self.ttlframe, text=cfg.c_title_text, font=(cfg.c_bold_font, cfg.c_title_fontsize), bg=cfg.c_bg_color, fg=cfg.fontcolor)
        self.ttllbl.pack(padx=cfg.padxy, pady=cfg.padxy)

        # the 'state/action' frame
        self.state_frame = Frame(master=self, bg=cfg.c_bg_color, padx=cfg.padxy, pady=cfg.padxy)
        self.state_frame.grid(row=1, column=0, columnspan=3, padx=cfg.padxy, pady=cfg.padxy, sticky='ew')
        self.state_line=StringVar()
        self.state_label = Label(master=self.state_frame, textvariable=self.state_line, fg=cfg.c_state_font_color, bg=cfg.c_bg_color,
                            font=(cfg.c_state_font, cfg.c_state_fontsize))
        self.state_label.grid(row=0, column=0, sticky='w')
        self.action_line=StringVar()
        self.state_action = Label(master=self.state_frame, textvariable=self.action_line, fg=cfg.c_action_font_color, bg=cfg.c_bg_color,
                            font=(cfg.c_action_font, cfg.c_action_fontsize))
        self.state_action.grid(row=1, column=0, sticky='w')
        
        # create a frame for interactions (buttons, text entry, etc.)
        self.int_frame = Frame(master=self, bg=cfg.c_bg_color, padx=cfg.padxy, pady=cfg.padxy)
        self.int_frame.grid(row=2, column=0, padx=cfg.padxy, pady=cfg.padxy, sticky='ewn')
        
        self.btn_start = Button(self.int_frame, height=cfg.c_btn_height, relief=GROOVE, bg=cfg.c_btn_bg_color,
            text=cfg.start_btn_txt, fg=cfg.c_btn_idle_color, font=(cfg.c_bold_font, cfg.c_btn_fontsize),
            command=self.start_callback)
        self.btn_start.grid(row=0, column=0, rowspan=2, padx=cfg.padxy, pady=cfg.padxy)
        self.disable_start_button()
        
        self.btn_stop= Button(self.int_frame, height=cfg.c_btn_height, relief=GROOVE, bg=cfg.c_btn_bg_color,
            text=cfg.stop_btn_txt, fg=cfg.c_btn_idle_color, font=(cfg.c_bold_font, cfg.c_btn_fontsize),
            command=self.stop_callback)
        self.btn_stop.grid(row=0, column=1, rowspan=2, padx=cfg.padxy, pady=cfg.padxy)
        self.disable_stop_button()

        self.event_text_1 = StringVar()
        self.events_1 = Label(master=self.int_frame, textvariable=self.event_text_1, anchor='w',
            fg=cfg.info_fontcolor, bg=cfg.c_bg_color, font=(cfg.c_text_font, cfg.c_info_fontsize))
        self.events_1.grid(row=0, column=2, padx=cfg.padxy, pady=cfg.padxy)

        self.event_text_2 = StringVar()
        self.events_2 = Label(master=self.int_frame, textvariable=self.event_text_2, anchor='w',
            fg=cfg.info_fontcolor, bg=cfg.c_bg_color, font=(cfg.c_text_font, cfg.c_info_fontsize))
        self.events_2.grid(row=1, column=2, padx=cfg.padxy, pady=cfg.padxy)

        self.time_left_frame = Frame(master=self, bg=cfg.c_bg_color, padx=cfg.padxy, pady=cfg.padxy)
        self.time_left_frame.grid(row=3, column=0, padx=cfg.padxy, pady=cfg.padxy, sticky='we')
        self._time_left = StringVar()
        self.time_left = Label(master=self.time_left_frame, textvariable=self._time_left, anchor='w',
            fg=cfg.info_fontcolor, bg=cfg.c_bg_color, font=(cfg.c_text_font, cfg.c_time_left_fontsize))
        self.time_left.grid(row=0, column=0, sticky='w')
        self.update

        # "info" frame
        self.info_frame = Frame(master=self, bg=cfg.c_bg_color, padx=cfg.padxy, pady=cfg.padxy)
        self.info_frame.grid(row=6, column=0, padx=cfg.padxy, pady=cfg.padxy, sticky = 'e')

        self.info_line_1 = StringVar()
        self.info_label_1 = Label(master=self.info_frame, textvariable=self.info_line_1, anchor='e',
            fg=cfg.info_fontcolor, bg=cfg.c_bg_color, font=(cfg.c_text_font, cfg.c_info_fontsize))
        self.info_label_1.grid(row=0, column=0, sticky='e')

        self.info_line_2 = StringVar()
        self.info_label_2 = Label(master=self.info_frame, textvariable=self.info_line_2, anchor='e', 
            fg=cfg.info_fontcolor, bg=cfg.c_bg_color, font=(cfg.c_text_font, cfg.c_info_fontsize))
        self.info_label_2.grid(row=1, column=0, sticky='e')

        self.info_line_3 = StringVar()
        self.info_label_3 = Label(master=self.info_frame, textvariable=self.info_line_3, anchor='e', 
            fg=cfg.info_fontcolor, bg=cfg.c_bg_color, font=(cfg.c_text_font, cfg.c_info_fontsize))
        self.info_label_3.grid(row=2, column=0, sticky='e')

        self.update()      
        if self._debug: print('control window ready')

        #self.bind('<Control-Alt-F12>', self.exit_callback)
        self.bind('<Control-q>', self.exit_callback)
        

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

    def set_state_line(self, txt_tuple, text_color):
        self.state_label.config(fg=text_color)
        self.state_line.set(str(txt_tuple[0]))
        self.action_line.set(str(txt_tuple[1]))

    def set_event_line_1(self, textin, text_color=cfg.c_text_info_color):
        self.events_1.config(fg=text_color)
        self.event_text_1.set(str(textin))
    
    def set_event_line_2(self, textin, text_color=cfg.c_text_info_color):
        self.events_2.config(fg=text_color)
        self.event_text_2.set(str(textin))
    
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
    print(f'\n>>> exiting ({e})\n')
    tst.destroy()
    root.destroy()

def test_state_line_msg_lengths(e):
    from time import sleep
    for state_line in RecordingState:
        tst.set_state_line(state_line.value, cfg.c_state_font_color)
        tst.set_time_left(f'{state_line.name}', 'Black')
        tst.update()
        sleep(3)
    tst.set_state_line(('Showing of state messages is complete', ':)'), cfg.c_state_font_color)
    tst.set_time_left('', 'Black')

if __name__ == '__main__':

    logger = logging.getLogger('ControlWindowTestLog')
    logging.basicConfig(
        filename=r'ControlWindowsTest.log', 
        filemode='w', 
        level=logging.INFO,
        format='%(asctime)s: %(levelname)s: %(message)s',
        datefmt='%Y%m%d_%H%M%S'
    )
    logging.captureWarnings(True)
    logging.info('ControlWindow test started')
    root = Tk()
    root.geometry( '300x100+0+0' )
    root.title( 'close me to exit test' )
    tst = ControlWindow(root, None, None, test_exit_callback, logger)
    tst.set_info_line_1(cfg.info_line.format('Main System', 'test', 0), cfg.c_text_soft_color)
    tst.set_info_line_2(cfg.info_line.format('Backup System', 'test', 0), cfg.c_text_soft_color)
    tst.set_info_line_3(cfg.info_line.format('USB', 'test', 0), cfg.c_text_soft_color)
    tst.bind('<Escape>', test_state_line_msg_lengths)
    tst.set_state_line(('Init complete','Press <Escape> to show all state messages'), cfg.c_state_font_color)
    root.mainloop()
