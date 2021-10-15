from tkinter import *

main_window = Tk()

#Labels
Label(main_window, text="Enter your name").grid(row=0, column=0)

Label(main_window, text="What is your age?").grid(row=1, column=0)

#Text Input
name1 = Entry(main_window, width=50, borderwidth=5)
age1 = Entry(main_window, width=50, borderwidth=5)
name1.grid(row=0, column=1)
age1.grid(row=1, column=1)


def on_click():
    print(f"My name is " + str(name1.get()) + " and my age is " + str(age1.get()) + '.')


#Buttons!
Button(main_window, text="Click me!", command=on_click).grid(row=2, column=1)

main_window.mainloop()