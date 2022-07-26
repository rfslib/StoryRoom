'''
file: get_filename.py
author: rfslib

purpose: allow and get entry of a filename
'''

from tkinter import *

from sr_parm import SR_Parm as cfg

class Get_Filename(Toplevel):
    debug = 0

    row1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_']
    row2 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
    row3 = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
    row4 = ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '(', ')']

    def __init__(self, master):
        Toplevel.__init__(self,master)
        
        # set our look
        self.config( bg=cfg.tw_normbg)
        #self.attributes( '-alpha', cfg.tw_normalpha ) # set transparency
        self.overrideredirect( True ) # hide the title bar  
        self.attributes('-topmost', 1) # stay on top     
    
        # set our size and location
        self.geometry( '800x200+100+100')

        # input line
        self.file_name_frame = Frame(master=self, bg=cfg.bg_color)
        self.file_name_frame.grid(row=0, column=0, padx=cfg.padxy, pady=cfg.padxy, sticky = 'e')
        self.file_name=StringVar()
        self.file_name_prompt = Label(master=self.file_name_frame, text='Enter filename: ')
        self.file_name_prompt.grid(row=0, column=0)
        self.file_name_label = Label(master=self.file_name_frame, textvariable=self.info_line_1, anchor='e',
            fg=cfg.info_fontcolor, bg=cfg.bg_color, font=(cfg.font_family, cfg.info_fontsize))
        self.file_name_label.grid(row=0, column=1, sticky='e')

        # row 1 (numbers)
        self.row1_frame = Frame(master=self)
        self.row1_frame.grid(row=1, column=0, sticky='w')
        

        # row 2 ('qwert')

        # row 3 ('asdfg')

        # row 4 ('zxcvb')



    def get_txt( self ):
        return self._txt

    def set_txt( self, textin ):
        self._txt.set( str( textin ) )

if __name__ == '__main__':
    root = Tk()
    root.geometry( '300x100+0+0' )
    root.title( 'close me to exit test' )
    tst = Get_Filename( root )
    fname=tst.get_input()
    tst.destroy()
    print(f'>>>> filename: {fname} <<<<')
    root.mainloop()