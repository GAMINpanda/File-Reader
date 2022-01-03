"""
Original Project by Alexander Mitchiner
This file holds the functions that find the type of file and put the file text onto the GUI
Master file is Main_GUI.py
"""
import logging

def File_Type():
    with open("cache.txt", "r") as cache:
        name = cache.readline()
    Type = name.split(".")[1]
    #splits cached file at . to find file type
    return Type, name

def File_contents(Type, name):
    if Type == "txt":
        #literally just copies content as it is (probably inefficient for large files, will fix if I ever finish the program)
        with open(name, "r") as file:
            contents = file.readlines()

    elif Type == "csv":
        #has to go through longer process because of commas
        with open(name, "r") as file:

            temp = file.readlines()
            contents = [] #creates empty contents list

            file.seek(0,0) #Otherwise file would return empty since pointer has moved

            for value in temp:
                #removes the comma then adds the line to contents as readlines() increments on its own
                line = file.readline()
                line_list = line.split(",")
                contents.append(line_list)

    else:
        #if I don't have support for file type this will be recieved
        contents = "Don't support file type"

    #logging.info("Contents: ",contents)

    return contents

def Save_Text(Text, Columns, Type, name, Heading): #Function to copy the text boxes and save the file appropriately
    #logging.info("Columns = ", Columns)
    Rows_Text = []

    if Type == "csv":
        for col_num in range(0, Columns):
            #logging.info(col_num) #for debugging
            All_Col_Text = (Heading[col_num].get("1.0","end-1c") + "\n") + (Text[col_num].get("1.0","end-1c")) #Adds the Headings to the Text for easier saving
            All_Col_Text = All_Col_Text.split("\n")
            Rows_Text.append(All_Col_Text) #This thing copies each text box and splits each line apart so it would be a 2D list

        #logging.info(Rows_Text)
        Lines = len(Rows_Text[0]) #just getting amount of lines (could've changed)

        file = open(name, "w") #Just clears the file
        file.close()

        with open(name, "a") as file:#Opens file so text can be added

            for line_num, value in enumerate(Rows_Text[0]): #Adds text to file line by line rather than column by column

                for col_num in range(0, Columns):

                    #logging.info("Col_num: ",col_num,"Line_num: ", line_num)#for debugging

                    if col_num == (Columns - 1):

                        if line_num == (Lines - 1):
                            #logging.info(Rows_Text[col_num][line_num], "last adding")
                            file.write(Rows_Text[col_num][line_num]) #Adding a new line on the last line would create an unwanted new line

                        else:
                            #logging.info(Rows_Text[col_num][line_num], "adding new line")
                            file.write(Rows_Text[col_num][line_num] + "\n") #New line would start at the end of another

                    else:
                        #logging.info(Rows_Text[col_num][line_num], "adding new comma")
                        file.write(Rows_Text[col_num][line_num] + ",")


    else:
        All_Col_Text = (Heading.get("1.0","end-1c") + "\n") + (Text.get("1.0","end-1c")) #Adds the Headings to the Text for easier saving
        All_Col_Text = All_Col_Text.split("\n")
        Rows_Text = All_Col_Text

        #logging.info(Rows_Text)
        Lines = len(Rows_Text)

        file = open(name, "w") #Just clears the file
        file.close()

        with open(name, "a") as file:#Opens file so text can be added

            for line_num in range(0, Lines): #Adds text to file line by line rather than column by column

                if line_num == (Lines-1):
                    #logging.info(Rows_Text[col_num][line_num], "last adding") #for debugging
                    file.write(Rows_Text[line_num]) #Adding a new line on the last line would create an unwanted new line

                else:
                    #logging.info(Rows_Text[col_num][line_num], "adding new line") #for debugging
                    file.write(Rows_Text[line_num] + "\n") #New line would start at the end of another

