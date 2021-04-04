from tkinter import *

gui = Tk(className=' NJ MVC Appointment Finder')
#greeting = tk.Label(text="Hello, Tkinter")
#window.title('Counting Seconds')
#greeting.pack()
#gui.geometry("500x300")

##
OPTIONS = [
"Jan",
"Feb",
"Mar"
]

variable = StringVar(gui)
variable.set(OPTIONS[0]) # default value

w = OptionMenu(gui, variable, OPTIONS[0], *OPTIONS)
w.pack()

def ok():
    print ("value is:" + variable.get())

button = Button(gui, text="OK", command=ok)
button.pack()

gui.mainloop()
