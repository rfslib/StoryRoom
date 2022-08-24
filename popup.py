"""
file: popup.py
author: rfslib
"""

from tkinter import *

from sr_parm import SR_Parm as cfg

class popup_window(Toplevel):
    debug = False

    def __init__(self, master):
        Toplevel.__init__(self, master)
        
        self.withdraw() # hide until needed

        # set our look
        self.config(bg=cfg.o_bg_color)
        self.overrideredirect(True) # hide the title bar  
        self.attributes('-topmost', True) # stay on top     
    
        # set our size and location
        #self.geometry('924x500+50+50')
        self.geometry('+100+100')
        self.resizable(False, False)

        self._outer_frame = Frame(master=self, bg=cfg.o_bg_color, relief=GROOVE, borderwidth=3, padx=4, pady=4, width=912, height=490)
        self._outer_frame.grid(row=0, column=0, padx=3, pady=3)
        self._txt = StringVar()
        self._txt.set('...')
        self._txt_label = Label(master=self._outer_frame, textvariable=self._txt,
            font=(cfg.o_text_font, cfg.o_text_fontsize))
        self._txt_label.grid(row=0, column=0, padx=2, pady=2, sticky='we')
        self._txt_label.config(bg=cfg.o_bg_color)

        self._btn_ack = Button(master=self._outer_frame, text='Acknowledge', command=self._process_ack,
            height=cfg.o_btn_height, relief=GROOVE, bg=cfg.o_bg_color, font=(cfg.o_btn_font, cfg.o_btn_fontsize))
        self._btn_ack.grid(row=1, column=0, padx=2, pady=16)

        self._keep_focus_active = None
        self.bind('<Return>', self._process_return)

    def wait_for_ack(self, msg):
        self._txt.set(msg)
        self.deiconify()
        self._keep_focus()
        self.wait_variable(self._txt)

    def _process_ack(self):
        self.withdraw()
        self.after_cancel(self._keep_focus_active)
        self._txt.set('')

    def _process_return(self, data):
        self._process_ack()

    def _keep_focus(self): # don't allow this to lose focus if waiting for input :p
        self.focus_force()
        self._keep_focus_active = self.after(500, self._keep_focus)

# -------------------testing-------------------------------------------

def test_wait_for_ack(data):
    ow.wait_for_ack(f'Waiting for ack Waiting for ack Waiting for ack Waiting for ack')
    root.unbind('<Escape>')
    root.destroy()

if __name__ == '__main__':
    root = Tk()
    root.bind('<Escape>', test_wait_for_ack)
    Label(root, text='\n press ESC to continue \n').pack()
    root.update()
    ow = popup_window(root)
    root.focus_force()
    root.mainloop()
