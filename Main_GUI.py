"""
Reattempt at an Excel like program because my previous one was not very maintainable and all hosted in a single python file.
Program going to read txt and csv files and allow you to edit them
Made by Alexander Mitchiner


I was asked the point of this program but I realise there is no point, its just interesting to work with this and have something to work towards

To make the program more efficient and to make things easier to wrap my head around, I'm only using inbuilt modules
"""

import tkinter as tk
import turtle
#importing functions from the other file

from RandW import File_Type
from RandW import File_contents
from RandW import Save_Text #Importing these seperately doesn't produce an error

from pathlib import Path

import logging


root = tk.Tk()
root.title("File Reader") #some things to set up my program

path = Path.home()
path = str(path)

path = path + "\Pictures\Saved Pictures\pixil-frame-0.ico"
root.iconbitmap(path)
root.state("zoomed")


Canvas_main = tk.Canvas(root, height = 1080, width = 1920, bg = "grey")
Canvas_main.pack()#the main canvas on which the windows will be placed

def Draw_Text(columns, Canvas, Type):
    #this function draws the columns and returns the list of each one
    if Type == "csv":
        Text_size = int(225/columns)
        #225 is a good number to evenly spread across the screen

        Text = [] #Will be multiple columns for a csv file
        Heading = [] #Will be the first line of a csv file

        for num in range (0, columns):
            #Creates each column
            Text.append("")
            Text[num] = tk.Text(Canvas, height = 55, width = Text_size)
            #turns out 1 unit of window size = 8x
            Canvas.create_window(((num*Text_size*8)+50, 100), window = Text[num], anchor = "nw") #Creates each window for the amount of columns
            
            Heading.append("")
            Heading[num] = tk.Text(Canvas, height = 1, width = Text_size)
            Canvas.create_window(((num*Text_size*8)+50, 75), window = Heading[num], anchor = "nw")
            
        add_button = tk.Button(root, text = "Add Column", command = lambda: add_col()) #Triggers a column to be added to a csv (command not made yet)
        Canvas.create_window((350, 50), window = add_button)

        remove_button = tk.Button(root, text = "Remove Column", command = lambda: remove_col()) #Triggers a column to be added to a csv (command not made yet)
        Canvas.create_window((450, 50), window = remove_button)

    else:
        Text = tk.Text(Canvas, height = 55, width = 225) #Only need one text box for most other files
        Canvas.create_window((50, 100), window = Text, anchor = "nw")
        Heading = tk.Text(Canvas, height = 1, width = 225)
        Canvas.create_window((50, 75), window = Heading, anchor = "nw")
        add_button = []
        remove_button = []

    return Text, Heading, add_button, remove_button

def Add_Text(Text, Contents, Type, Columns, Heading, adding_col):
    #this function adds text to the columns
    #print(Contents) #For debugging
    #logging.info(len(Contents))
    
    if Type == "csv":#adds to each text box before moving on (Adds row 1, column 1; then row 2, column 1 etc until row n, column n)

        if adding_col: #Needs to account for the extra column

            for column_num in range(0, Columns):

                #logging.info("Column num:", column_num) #for debugging
                #logging.info("Column - 1:", Columns - 1)

                if column_num == Columns - 1: #This is the final column so that is accounted for
                    Heading[column_num].insert(tk.END, "")

                    for row_num in enumerate(Contents):
                        Text[column_num].insert(tk.END, "\n") #supposed to create len(Contents) new lines

                else:
                    Heading[column_num].insert(tk.END, (Contents[0][column_num]).replace("\n","")) #need to get rid of the artificial new line but bottom so no new one

                    for row_num, value in enumerate(Contents):
                        Text[column_num].insert(tk.END, (Contents[row_num][column_num]).replace("\n","") + "\n") #makes sure to avoid extra new lines

                Text[column_num].delete("end-1c", tk.END) #removes the tkinter automatic newline

        else:
            for column_num in range(0, Columns):
                Heading[column_num].insert(tk.END, (Contents[0][column_num]).replace("\n",""))

                for row_num in range(1, len(Contents)):
                    Text[column_num].insert(tk.END, (Contents[row_num][column_num]).replace("\n","") + "\n") #makes sure to avoid extra new lines

                Text[column_num].delete("end-1c", tk.END) #removes the tkinter automatic newline

    elif Type == "txt": #Text files don't have columns like a csv so that iteration is cut

        Heading.insert(tk.END, (Contents[0]).replace("\n",""))

        for row_num in range(1, len(Contents)):
            Text.insert(tk.END, (Contents[row_num]).replace("\n","") + "\n")

        Text.delete("end-1c", tk.END) #removes the tkinter automatic newline

    else:
        print("I don't currently support that file type.")

def Load(not_have_file, Type, name): #Functions that run on startup

    if not_have_file:
        #print(name)#for debugging
        Type, name = File_Type() #Uses function from the other file

    Contents = File_contents(Type, name) #Literally the contents of the file, whether csv or txt

    if Type == "csv":
        Columns = len(Contents[0]) #bases amount of columns on that of the first line of code (Contents has to be 2d for this to work)

    else:
        Columns = 1 #Only one text box needed

    Text, Heading, add_button, remove_button = Draw_Text(Columns, Canvas_main, Type) #Text variable holds each text box
    #print(Text) #Just to check all text is correctly outputted
    Add_Text(Text, Contents, Type, Columns, Heading, False) #Adds the text

    return Text, Contents, Type, Columns, name, Heading, add_button, remove_button #Just so variables can be used globally

def Load_newtext(): #calls load function after getting the name of the file with a different method

    global Text, Contents, Type, Columns, name, Heading, add_button, remove_button #changes the global variables so when a new file is loaded the same file can be saved

    try: #gets rid of file specific elements such as the text boxes for the new file
        add_button.destroy()
        remove_button.destroy()

        for col_num in range(0, Columns):
            Text[col_num].destroy()
            Heading[col_num].destroy()


    except Exception:
        try:
            remove_button.destroy()
            add_button.destroy()

        except Exception:
            pass

        Text.destroy()
        Heading.destroy()
    
    try: #means if the Load text field is empty the code isn't executed fully
        name = Entry_file.get() #gets value in load text box
        file_split = name.split(".")
        Type = file_split[1]
        Text, Contents, Type, Columns, name, Heading, add_button, remove_button = Load(False, Type, name)
        
    except Exception:
        print("Nothing in Load Text Field Or Error")

def Save_Load(Text, Columns, Type, name, Heading): #just putting them together for ease of use
    Save_Text(Text, Columns, Type, name, Heading)
    Load_newtext()

def add_col(): #function to add an additional column to a csv file
    global Columns, Text, Heading

    Columns = Columns + 1
    File_contents("csv", name)

    Text, Heading, add_button, remove_button = Draw_Text(Columns, Canvas_main, "csv")
    Add_Text(Text, Contents, "csv", Columns, Heading, True)
    Save_Load(Text, Columns, Type, name, Heading)

def remove_col(): #pretty much the same to add_col but to remove a column
    global Columns, Text, Heading

    Columns = Columns - 1
    File_contents("csv", name)

    Text, Heading, add_button, remove_button = Draw_Text(Columns, Canvas_main, "csv")

    Add_Text(Text, Contents, "csv", Columns, Heading, False)
    Save_Load(Text, Columns, Type, name, Heading)

def graph():#This function will graph a csv file that is 2d
    try:
        global used_graph, plotter
        
        if used_graph: #Means a new instance of turtle isn't made every time
            plotter.clear()
            plotter.reset()

        else:
            plotter = turtle.Turtle()

        xy = Entry_graph.get() #The typed values of x and y
        xy = xy.split(",") #User has to seperate by a comma
        x = int(xy[0])
        y = int(xy[1])

        plotter.speed(0)
        plotter.penup()
        plotter.goto(-450, 0)
        plotter.pendown()

        if i.get() == 1:
            x_all = (Text[x].get("1.0","end-1c")).split("\n") #getting all the values from each text box
            x_all_int = list(map(int, x_all))
            max_x = max(x_all_int)

            y_all = (Text[y].get("1.0","end-1c")).split("\n")
            y_all_int = list(map(int, y_all))
            max_y = max(y_all_int)

            Lines = len(x_all) #quick line check

            for Point in range(0, Lines - 1):
                x = ((x_all_int[Point])*(900/max_x)) - 450
                y = (y_all_int[Point])*(250/max_y)
                plotter.goto(x, y)

        else:
            plotter.penup()
            x_all = (Text[x].get("1.0","end-1c")).split("\n") #getting all the values from each text box
            x_all_int = list(map(int, x_all))
            max_x = max(x_all_int)

            y_all = (Text[y].get("1.0","end-1c")).split("\n")
            y_all_int = list(map(int, y_all))
            max_y = max(y_all_int)

            Lines = len(x_all) #quick line check

            for Point in range(0, Lines - 1):
                x = ((x_all_int[Point])*(900/max_x)) - 450
                y = (y_all_int[Point])*(250/max_y)
                plotter.goto(x, y)
                plotter.pendown()
                plotter.circle(1)
                plotter.penup()

            used_graph = True

    except Exception:
        print("Cannot initialize graph.")
    
def mean():
    try:
        val_num = int(Entry_Mean.get())
        total = 0

        List_Text = (Text[val_num].get("1.0", "end-1c")).split("\n")

        for val in List_Text:
            total = total + int(val)

        length = len(List_Text)
        mean = total / length
        Output_Mean.delete(0, tk.END)
        Output_Mean.insert(tk.END, mean)

    except Exception:
        print("Cannot find mean of values")

def main():
    global Text, Contents, Type, Columns, name, Heading, used_graph #These values need to change dynamically
    global add_button, remove_button, Entry_file, save_button, load_button, i, Entry_graph, Entry_Mean #Lots of global values ik but far easier on a small scale than making them all parameters
    global Output_Mean

    used_graph = False
    #It's bad practice to have so many global variables but the tkinter canvas and its elements need to be accessed anywhere

    Text, Contents, Type, Columns, name, Heading, add_button, remove_button = Load(True, "0", "0") #gets inital file parameters and opens the cached file


    #Buttons that are present throughout the program
    Entry_file = tk.Entry(root, width = 15) #The user can put their chosen file to read into this text box and when the load button is clicked that file is loaded
    Canvas_main.create_window((220, 50), window = Entry_file)
    Entry_file.insert(tk.END, name) #so the user knows the file name
    Entry_file.delete(tk.END) #removes the tkinter automatic newline

    save_button = tk.Button(root, text = "Save", command = lambda: Save_Load(Text, Columns, Type, name, Heading)) #Triggers files to save
    Canvas_main.create_window((70, 50), window = save_button)

    load_button = tk.Button(root, text = "Load", command = lambda: Load_newtext()) #Triggers a file to be loaded
    Canvas_main.create_window((120, 50), window = load_button)

    Entry_graph = tk.Entry(root, width = 5) #User can put order of columns to graph
    Canvas_main.create_window((600, 50), window = Entry_graph)
    Entry_graph.insert(tk.END, "0,1")

    graph_button = tk.Button(root, text = "Graph", command = lambda: graph())
    Canvas_main.create_window((550, 50), window = graph_button)

    i = tk.IntVar()
    Graph_Check = tk.Checkbutton(root, text = "Lines?", variable = i, onvalue = 1, offvalue = 0) #This button decides if the graph function connects lines or not
    Canvas_main.create_window((660, 50), window = Graph_Check)

    Entry_Mean = tk.Entry(root, width = 2) #User can put order of columns to graph
    Canvas_main.create_window((800, 50), window = Entry_Mean)
    Entry_Mean.insert(tk.END, "0")

    Output_Mean = tk.Entry(root, width = 10) #User can put order of columns to graph
    Canvas_main.create_window((845, 50), window = Output_Mean)

    mean_button = tk.Button(root, text = "Mean", command = lambda: mean())
    Canvas_main.create_window((770, 50), window = mean_button)

    tk.mainloop()

if __name__ == "__main__":
        main()