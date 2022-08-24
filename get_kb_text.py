'''
file: get_kb_text.py
author: rfslib

purpose: allow and get entry of a text string via a virtual keyboard using tkinter

adapted from https://masterprograming.com/how-to-create-virtual-onscreen-keyboard-using-python-and-tkinter/
    20220727: note that the above site disappeared the day after
for font style changes see https://www.pythontutorial.net/tkinter/ttk-style/
'''

from tkinter import *
from tkinter import ttk
from tkinter import font

class get_kb_text(Toplevel):

    debug = False

    def __init__(self, master): # Create the keyboard window, then hide (withdraw) it
        Toplevel.__init__(self, master)

        self.withdraw() # hide already so it doesn't flash while being build
        
        self.text = StringVar()         # update this to force exit
        self.text_prompt = StringVar()  # changeable prompt
        self.text_entry = StringVar()   # where the text string is built

        self.prompt = 'enter something:'
        self.maxlength = 48             # max number of characters in input string

        self.ixpad = 3 # was 6
        self.iypad = 5 # was 10
        self.xpad = 1
        self.ypad = 1
        self.key_width = 4
        paddings = {'ipadx': self.ixpad, 'ipady': self.iypad, 'padx': self.xpad, 'pady': self.ypad}
        entry_font = {'font': ('Consolas Bold', 14)}
        self.style = ttk.Style(self)
        #self.style.configure('TEntry', font=('Consolas Bold', 11))
        self.style.configure('TLabel', font=('Consolas', 10))
        self.style.configure('TButton', font=('Consolas Bold', 14))
        
        self.overrideredirect(True) # don't show title 
        self.attributes('-topmost', True) # stay on top
        self.geometry('+150+300') ## TODO: make this dynamic: bottom of screen, approx centered
        
        self.config(bg = 'Green')    #  add background color 'SystemButtonFace'

        # display prompt
        self.text_prompt.set('Use the on-screen keyboard: ')
        self.text_label = ttk.Label(self, textvariable=self.text_prompt, anchor='e')
        self.text_label.grid(row=0, column=0, rowspan=1, columnspan=3, sticky='we')

        # text entry display area
        self.text_entry.set('')
        text_entry = ttk.Entry(self, state='readonly', textvariable=self.text_entry, **entry_font)
        text_entry.grid(row=0, column=3, rowspan=1, columnspan=8, sticky='we')
            
        # add buttons for the number line
        ttk.Button(self, text='1', width=self.key_width, command=lambda : self._key_press('1')).grid(row=1, column=0, **paddings)
        ttk.Button(self, text='2', width=self.key_width, command=lambda : self._key_press('2')).grid(row=1, column=1, **paddings)
        ttk.Button(self, text='3', width=self.key_width, command=lambda : self._key_press('3')).grid(row=1, column=2, **paddings)
        ttk.Button(self, text='4', width=self.key_width, command=lambda : self._key_press('4')).grid(row=1, column=3, **paddings)
        ttk.Button(self, text='5', width=self.key_width, command=lambda : self._key_press('5')).grid(row=1, column=4, **paddings)
        ttk.Button(self, text='6', width=self.key_width, command=lambda : self._key_press('6')).grid(row=1, column=5, **paddings)
        ttk.Button(self, text='7', width=self.key_width, command=lambda : self._key_press('7')).grid(row=1, column=6, **paddings)
        ttk.Button(self, text='8', width=self.key_width, command=lambda : self._key_press('8')).grid(row=1, column=7, **paddings)
        ttk.Button(self, text='9', width=self.key_width, command=lambda : self._key_press('9')).grid(row=1, column=8, **paddings)
        ttk.Button(self, text='0', width=self.key_width, command=lambda : self._key_press('0')).grid(row=1, column=9, **paddings)
        # backspace options: '‹','←','◄','<-','BACK', 'Back'
        ttk.Button(self, text='Back', width=self.key_width, command=self._process_backspace).grid(row=1, column=10, **paddings) 

        # 2nd row (qwerty)
        ttk.Button(self, text='Q' , width=self.key_width, command=lambda : self._key_press('Q')).grid(row=2, column=0, **paddings)
        ttk.Button(self, text='W' , width=self.key_width, command=lambda : self._key_press('W')).grid(row=2, column=1, **paddings)
        ttk.Button(self, text='E' , width=self.key_width, command=lambda : self._key_press('E')).grid(row=2, column=2, **paddings)
        ttk.Button(self, text='R' , width=self.key_width, command=lambda : self._key_press('R')).grid(row=2, column=3, **paddings)
        ttk.Button(self, text='T' , width=self.key_width, command=lambda : self._key_press('T')).grid(row=2, column=4, **paddings)
        ttk.Button(self, text='Y' , width=self.key_width, command=lambda : self._key_press('Y')).grid(row=2, column=5, **paddings)
        ttk.Button(self, text='U' , width=self.key_width, command=lambda : self._key_press('U')).grid(row=2, column=6, **paddings)
        ttk.Button(self, text='I' , width=self.key_width, command=lambda : self._key_press('I')).grid(row=2, column=7, **paddings)
        ttk.Button(self, text='O' , width=self.key_width, command=lambda : self._key_press('O')).grid(row=2, column=8, **paddings)
        ttk.Button(self, text='P' , width=self.key_width, command=lambda : self._key_press('P')).grid(row=2, column=9, **paddings)

        # 3rd row (asdfg)
        ttk.Button(self, text='A' , width=self.key_width, command=lambda : self._key_press('A')).grid(row=3, column=0, **paddings)
        ttk.Button(self, text='S' , width=self.key_width, command=lambda : self._key_press('S')).grid(row=3, column=1, **paddings)
        ttk.Button(self, text='D' , width=self.key_width, command=lambda : self._key_press('D')).grid(row=3, column=2, **paddings)
        ttk.Button(self, text='F' , width=self.key_width, command=lambda : self._key_press('F')).grid(row=3, column=3, **paddings)
        ttk.Button(self, text='G' , width=self.key_width, command=lambda : self._key_press('G')).grid(row=3, column=4, **paddings)
        ttk.Button(self, text='H' , width=self.key_width, command=lambda : self._key_press('H')).grid(row=3, column=5, **paddings)
        ttk.Button(self, text='J' , width=self.key_width, command=lambda : self._key_press('J')).grid(row=3, column=6, **paddings)
        ttk.Button(self, text='K' , width=self.key_width, command=lambda : self._key_press('K')).grid(row=3, column=7, **paddings)
        ttk.Button(self, text='L' , width=self.key_width, command=lambda : self._key_press('L')).grid(row=3, column=8, **paddings)
        ttk.Button(self, text='Enter', width=(self.key_width*2)+(self.ixpad*1), command=self._process_enter
            ).grid(row=3, column=9, columnspan=2, **paddings)

        # 4th row (zxcvb)
        ttk.Button(self, text='Z' , width=self.key_width, command=lambda : self._key_press('Z')).grid(row=4, column=0, **paddings)
        ttk.Button(self, text='X' , width=self.key_width, command=lambda : self._key_press('X')).grid(row=4, column=1, **paddings)
        ttk.Button(self, text='C' , width=self.key_width, command=lambda : self._key_press('C')).grid(row=4, column=2, **paddings)
        ttk.Button(self, text='V' , width=self.key_width, command=lambda : self._key_press('V')).grid(row=4, column=3, **paddings)
        ttk.Button(self, text='B' , width=self.key_width, command=lambda : self._key_press('B')).grid(row=4, column=4, **paddings)
        ttk.Button(self, text='N' , width=self.key_width, command=lambda : self._key_press('N')).grid(row=4, column=5, **paddings)
        ttk.Button(self, text='M' , width=self.key_width, command=lambda : self._key_press('M')).grid(row=4, column=6, **paddings)
        ttk.Button(self, text='(' , width=self.key_width, command=lambda : self._key_press('(')).grid(row=4, column=7, **paddings)
        ttk.Button(self, text=')' , width=self.key_width, command=lambda : self._key_press(')')).grid(row=4, column=8, **paddings)

        # 5th row (space bar)
        ttk.Button(self, text='Space' , width=(self.key_width*9)+(self.ixpad*7), command=lambda : self._key_press('_')
            ).grid(row=5, column=0, columnspan=9, **paddings)
        ttk.Button(self, text='Clear', width=(self.key_width*2)+(self.ixpad*0), command=self._clear_value
            ).grid(row=5, column=9, columnspan=2, **paddings)

        self.update()
        self.resizable(False, False)
        self._keep_focus_active = None

    def __del__(self):
        self.text.set('') # force a wait_variable to continue? is this a good idea?
        if self._keep_focus_active != None:
            self.after_cancel(self._keep_focus_active)
        #self.destroy()

    def _key_press(self, char):
        if len(self.text_entry.get()) < self.maxlength:
            self.text_entry.set(self.text_entry.get() + str(char))
        else:
            pass # TODO: warn user

    # the 'clear' button resets the entry string to an empty string
    def _clear_value(self):
        self.text_entry.set('')

    # backspace: remove the last character of the entry
    def _process_backspace(self):
        self.text_entry.set(self.text_entry.get()[:-1]) # no exception even when string is empty :p

    # Enter ('Return') Button sets self.text, which triggers the wait_variable in get_text()
    def _process_enter(self):
        self.text.set(self.text_entry.get())

    def _keep_focus(self): # don't allow this to lose focus if waiting for input :p
        self.focus_force()
        self._keep_focus_active = self.after(500, self._keep_focus)

    def _update_prompt(self):
        TODO

    # note that this waits for a changed to text_entry (wait_variable), which is done by _process_enter
    def get_text(self, prompt, maxlength=48): # the public method to get some text
        self.prompt = prompt
        self.text_prompt.set(self.prompt)
        self.text_entry.set('')
        self.maxlength = maxlength
        self.deiconify()
        self.focus_force()
        self._keep_focus()
        self.wait_variable(self.text)
        self.after_cancel(self._keep_focus_active)
        self._keep_focus_active = None
        self.withdraw()
        return self.text.get()

# -------------------testing-------------------------------------------

def test_get_text(data):
    print(f'>>> test_get_text called with {data}')
    ret = '.'
    ctr = 1
    while ret != '':
        ret = gf.get_text(f'Empty string to end({ctr}): ', ctr)
        Label(root, text=f'"{ret}"').pack()
        ctr += 1
        print(f'>>> test_get_text: ret: "{ret}"')
    root.unbind('<Escape>')
    root.destroy()

if __name__ == '__main__':
    root = Tk()
    root.bind('<Escape>', test_get_text)
    Label(root, text='\n press ESC to continue \n').pack()
    root.update()
    gf = get_kb_text(root)
    print(f'>>> Get_Filename object: {gf}')
    root.focus_force()
    root.mainloop()


