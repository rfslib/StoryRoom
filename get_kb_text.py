'''
file: get_filename.py
author: rfslib

purpose: allow and get entry of a filename

adapted from https://masterprograming.com/how-to-create-virtual-onscreen-keyboard-using-python-and-tkinter/
note that the above site disappeared the day after (on 20220727)
'''

from tkinter import *
from tkinter import ttk

class get_kb_text(Toplevel):

    def __init__(self, master): # Create the keyboard window, then hide (withdraw) it
        Toplevel.__init__(self, master)

        self.withdraw() # hide already
        
        self.text = StringVar()
        self.text_prompt = StringVar()
        self.text_entry = StringVar()

        self.key_width = 6
        self.font = 'Lucida Console'
        self.font_size = 10.5
        #self.key_offset = self.key_width / 3 # rows are staggered by 1/3 key width
        self.xpad = 6
        self.ypad = 10
        self.xwidth = (12 * (self.key_width * self.font_size) ) + (13 * self.xpad)
        
        self.overrideredirect(True) # don't show title 
        #self.attributes('-alpha', 0.9) # set transparency
        self.attributes('-topmost', 1) # stay on top
        self.geometry('{}x300+100+500'.format(int(self.xwidth)))
        self.resizable(False, False)
        self.config(bg = 'green')    #  add background color

        # display prompt
        self.text_prompt.set('Use the on-screen keyboard: ')
        self.text_label = ttk.Label(self, textvariable=self.text_prompt, anchor='e')
        self.text_label.grid(row=0, column=0, rowspan=1, columnspan=3, ipadx=(self.key_width*3)+(self.xpad*2), ipady=self.ypad)
        
        # text entry area
        self.text_entry.set('')
        text_entry = ttk.Entry(self, state='readonly', textvariable = self.text_entry)
        text_entry.grid(row=0, column=3, rowspan=1, columnspan=10, ipadx=(self.key_width*8)+(self.xpad*7) , ipady=self.ypad, sticky='w')

        # add buttons for the number line
        #self.r1_frame = ttk.Frame(master=self)
        #self.r1_frame.grid(row=1, column=0, columnspan=20)
        ttk.Button(self, text='1', width=6, command=lambda : self.key_press('1')).grid(row=1, column=0, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='2', width=6, command=lambda : self.key_press('2')).grid(row=1, column=1, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='3', width=6, command=lambda : self.key_press('3')).grid(row=1, column=2, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='4', width=6, command=lambda : self.key_press('1')).grid(row=1, column=3, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='5', width=6, command=lambda : self.key_press('5')).grid(row=1, column=4, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='6', width=6, command=lambda : self.key_press('6')).grid(row=1, column=5, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='7', width=6, command=lambda : self.key_press('7')).grid(row=1, column=6, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='8', width=6, command=lambda : self.key_press('8')).grid(row=1, column=7, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='9', width=6, command=lambda : self.key_press('9')).grid(row=1, column=8, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='0', width=6, command=lambda : self.key_press('0')).grid(row=1, column=9, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='Clear', width=(self.key_width*2)+self.xpad, command=self.clear_value
            ).grid(row=1, column=10, columnspan=2, ipadx=self.xpad, ipady=self.ypad)

        # 2nd row (qwerty)
        ttk.Button(self, text='Q' , width=self.key_width, command=lambda : self.key_press('Q')).grid(row=2, column=0, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='W' , width=self.key_width, command=lambda : self.key_press('W')).grid(row=2, column=1, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='E' , width=self.key_width, command=lambda : self.key_press('E')).grid(row=2, column=2, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='R' , width=self.key_width, command=lambda : self.key_press('R')).grid(row=2, column=3, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='T' , width=self.key_width, command=lambda : self.key_press('T')).grid(row=2, column=4, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='Y' , width=self.key_width, command=lambda : self.key_press('Y')).grid(row=2, column=5, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='U' , width=self.key_width, command=lambda : self.key_press('U')).grid(row=2, column=6, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='I' , width=self.key_width, command=lambda : self.key_press('I')).grid(row=2, column=7, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='O' , width=self.key_width, command=lambda : self.key_press('O')).grid(row=2, column=8, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='P' , width=self.key_width, command=lambda : self.key_press('P')).grid(row=2, column=9, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='(' , width=self.key_width, command=lambda : self.key_press('(')).grid(row=2, column=10, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text=')' , width=self.key_width, command=lambda : self.key_press(')')).grid(row=2, column=11, ipadx=self.xpad, ipady=self.ypad)


        # 3rd row (asdfg)
        ttk.Button(self, text='A' , width=self.key_width, command=lambda : self.key_press('A')).grid(row=3, column=0, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='S' , width=self.key_width, command=lambda : self.key_press('S')).grid(row=3, column=1, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='D' , width=self.key_width, command=lambda : self.key_press('D')).grid(row=3, column=2, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='F' , width=self.key_width, command=lambda : self.key_press('F')).grid(row=3, column=3, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='G' , width=self.key_width, command=lambda : self.key_press('G')).grid(row=3, column=4, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='H' , width=self.key_width, command=lambda : self.key_press('H')).grid(row=3, column=5, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='J' , width=self.key_width, command=lambda : self.key_press('J')).grid(row=3, column=6, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='K' , width=self.key_width, command=lambda : self.key_press('K')).grid(row=3, column=7, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='L' , width=self.key_width, command=lambda : self.key_press('L')).grid(row=3, column=8, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='Enter', width=(self.key_width*3)+(self.xpad*2), command=self.process_enter
            ).grid(row=3, column=9, columnspan=3, ipadx=self.xpad, ipady=self.ypad)

        # 4th row (zxcvb)
        ttk.Button(self, text='Z' , width=self.key_width, command=lambda : self.key_press('Z')).grid(row=4, column=0, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='X' , width=self.key_width, command=lambda : self.key_press('X')).grid(row=4, column=1, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='C' , width=self.key_width, command=lambda : self.key_press('C')).grid(row=4, column=2, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='V' , width=self.key_width, command=lambda : self.key_press('V')).grid(row=4, column=3, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='B' , width=self.key_width, command=lambda : self.key_press('B')).grid(row=4, column=4, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='N' , width=self.key_width, command=lambda : self.key_press('N')).grid(row=4, column=5, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='M' , width=self.key_width, command=lambda : self.key_press('M')).grid(row=4, column=6, ipadx=self.xpad, ipady=self.ypad)
        ttk.Button(self, text='.' , width=self.key_width, command=lambda : self.key_press('.')).grid(row=4, column=8, ipadx=self.xpad, ipady=self.ypad)

        # 5th row (space bar)
        space = ttk.Button(self, text='Space' , width=(self.key_width*9)+(self.xpad*8), command=lambda : self.key_press(' '))
        space.grid(row=5, column=0, columnspan=9, ipadx=self.xpad, ipady=self.ypad)

        self.update()

    def key_press(self, num):
        self.text_entry.set(self.text_entry.get() + str(num))

    # function clear button
    def clear_value(self):
        self.text_entry.set('')

    # Enter Button Work Next line Function
    def process_enter(self):
        print(f'>>> Enter tapped. Value: {self.text_entry.get()}')
        self.text.set(self.text_entry.get())
        self.withdraw()
        return self.text

    def get_text(self, prompt):
        print(f'>>> get_text called, prompt: {prompt}')
        self.text_prompt.set(prompt)
        self.text_entry.set('')
        self.deiconify()
        self.focus_force()
        self.wait_variable(self.text)
        return self.text.get()


def test_get_text(data):
    print(f'>>> test_get_text called with {data}')
    ret = gf.get_text('Enter something: ')
    print(f'>>> test_get_text: ret: {ret}')
    ret = gf.get_text('Enter something else: ')
    print(f'>>> test_get_text: ret: {ret}')
    root.unbind('<Escape>')
    root.destroy()

if __name__ == '__main__':
    from time import sleep
    root = Tk()
    root.bind('<Escape>', test_get_text)
    #root.withdraw()
    gf = get_kb_text(root)
    print(f'>>> Get_Filename object: {gf}')
    root.focus_force()
    root.mainloop()


