from Tkinter import *

parent = Tk()
menubar = Menu(parent)
menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='File')
menubar.add_cascade(menu=menu_edit, label='Edit')

parent.mainloop()
