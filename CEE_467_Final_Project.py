#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 20:46:21 2018

@author: danieltjondro
"""

from tkinter import *
import tkinter as tk


# Import Shapes Database
# Reading an excel file using Python 
import xlrd 
  
# Give the location of the file 
loc = ("aisc-shapes-database-v15.0h.xlsx") 
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(1)


# Start using tkinter
root = tk.Tk()
root.geometry('800x600')

v = tk.IntVar()
method = tk.StringVar()
component = tk.StringVar()
steel = tk.StringVar()
shape_of_member = tk.StringVar()

T1 = tk.Label(root,text="Which design pholosophy do you follow?")
R_LRFD = tk.Radiobutton(root, text="LRFD", variable=method, value="LRFD")
R_ASD = tk.Radiobutton(root, text="ASD", variable=method, value="ASD")

T2 = tk.Label(root,text="Which structural component are you interested in?")
R_Tension_Members = tk.Radiobutton(root, text="Tension Members", variable=component, value="Tension Members")
R_Compression_Members = tk.Radiobutton(root, text="Compression Members", variable=component, value="Compression Members")
R_Bending_Members = tk.Radiobutton(root, text="Bending_Members", variable=component, value="Bending_Members")
R_Connection = tk.Radiobutton(root, text="Connections", variable=component, value="Connections")

T1.grid(row=0, column=0, sticky="W")
R_LRFD.grid(row=1, column=0, sticky="W")
R_ASD.grid(row=2, column=0, sticky="W",pady=(0,15))

T2.grid(row=4, column=0, sticky="W")
R_Tension_Members.grid(row=5, column=0, sticky="W")
R_Compression_Members.grid(row=6, column=0, sticky="W")
R_Bending_Members.grid(row=7, column=0, sticky="W")
R_Connection.grid(row=8, column=0, sticky="W",pady=(0,15))

T3 = tk.Label(root,text="Which type of steel are you planning to use?")
T3.grid(row=0, column=1, sticky="W")
Type_of_steel1 = tk.Radiobutton(root, text="A36 Steel", variable=steel, value="A36 Steel")
Type_of_steel1.grid(row=1, column=1, sticky="W")
Type_of_steel2 = tk.Radiobutton(root, text="A992 Steel", variable=steel, value="A992 Steel")
Type_of_steel2.grid(row=2, column=1, sticky="W",pady=(0,15))

T4 = tk.Label(root,text="Which type of shape are you planning to use?")
T4.grid(row=4, column=1, sticky="W")
Shape1 = tk.Radiobutton(root, text="Double-Angle", variable=shape_of_member, value="Double-Angle")
Shape1.grid(row=5, column=1, sticky="W")
Shape2 = tk.Radiobutton(root, text="WT9", variable=shape_of_member, value="WT9")
Shape2.grid(row=6, column=1, sticky="W")

Load_Instructions = tk.Label(root, text="Enter either both a dead and live load, or the required strength:")
Load_Instructions.grid(row = 13, column = 0, sticky = "W")
Parameters_1 = tk.Label(root, text="Dead Load (in kips):")
Parameters_1.grid(row=14, column=0, sticky="W")
Entry_1 = tk.Entry(root, bd = 3)
Entry_1.grid(row=15, column = 0, sticky="W")

Parameters_2 = tk.Label(root, text="Live Load (in kips):")
Parameters_2.grid(row=16, column=0, sticky="W")
Entry_2 = tk.Entry(root, bd = 3)
Entry_2.grid(row=17, column = 0, sticky="W",pady=(0,10))

Or = tk.Label(root, text = "or")
Or.grid(row=18, column=0, sticky="W")

Parameters_3 = tk.Label(root, text="Required Strength (in kips):")
Parameters_3.grid(row=14, column=1, sticky="W")
Entry_3 = tk.Entry(root, bd = 3)
Entry_3.grid(row=15,column=1,sticky="W")

def design(): 
    print(Entry_1.get() == '')
    print(Entry_3.get())
    if steel.get() == "A36 Steel":
        Fy = 36
        Fu = 58
    elif steel.get() == "A992 Steel":
        Fy = 50
        Fu = 65
    
    if method.get() == "LRFD":
        if Entry_1.get() == '':
            total_load = float(Entry_3.get())
        else: 
            total_load = (float(1.2) * float(Entry_1.get())) + (float(1.6) * float(Entry_2.get()))
        display = str("%.2f" % total_load)
        label2["text"] = "Factored load = " + display + " kips"
        
        if component.get() == "Tension Members":
            Min_area = total_load/(.90 * Fy)
            if shape_of_member.get() == "Double-Angle":
                best_area = sheet.cell_value(855, 10)
                shape = sheet.cell_value(855, 3)
                for i in range(855,1464):
                    if sheet.cell_value(i, 10) > Min_area and sheet.cell_value(i, 10) < best_area:
                        best_area = sheet.cell_value(i, 10)
                        shape = sheet.cell_value(i, 3)
            elif shape_of_member.get() == "WT9":
                best_area = sheet.cell_value(540, 10)
                shape = sheet.cell_value(540, 3)
                for i in range(540,813):
                    if sheet.cell_value(i, 10) > Min_area and sheet.cell_value(i, 10) < best_area:
                        best_area = sheet.cell_value(i, 10)
                        shape = sheet.cell_value(i, 3)
            tension_l1["text"] = "Minimum required gross area (based on yielding) = " + str("%.2f" % (total_load/(.90 * Fy))) + " square inches"
            tension_shape["text"] = "Based on this minimum gross area, select " + str(shape) + " with area = " + str(best_area)
            tension_l2["text"] = "Minimum effective net area (based on rupture) = " + str("%.2f" % (total_load/(.75 * Fu))) + " square inches"
    
    elif method.get() == "ASD":
        if Entry_1.get() == '':
            total_load = float(Entry_3.get())
        else:
            total_load = float(Entry_1.get()) + float(Entry_2.get()) + Entry_3.get()
        display = str("%.2f" % total_load)
        label2["text"] = "Factored load = " + display +  " kips"
        
        if component.get() == "Tension Members":
            Min_area = total_load * 1.67 / Fy
            if shape_of_member.get() == "Double-Angle":
                best_area = sheet.cell_value(855, 10)
                shape = sheet.cell_value(855, 3)
                for i in range(855,1464):
                    if sheet.cell_value(i, 10) > Min_area and sheet.cell_value(i, 10) < best_area:
                        best_area = sheet.cell_value(i, 10)
                        shape = sheet.cell_value(i, 3)
            elif shape_of_member.get() == "WT9":
                best_area = sheet.cell_value(540, 10)
                shape = sheet.cell_value(540, 3)
                for i in range(540,813):
                    if sheet.cell_value(i, 10) > Min_area and sheet.cell_value(i, 10) < best_area:
                        best_area = sheet.cell_value(i, 10)
                        shape = sheet.cell_value(i, 3)
            tension_l1["text"] = "Minimum required gross area (based on yielding) = " + str("%.2f" % (total_load * 1.67/Fy)) + " square inches"
            tension_shape["text"] = "Based on this minimum gross area, select " + str(shape) + " with area = " + str(best_area)
            tension_l2["text"] = "Minimum effective net area (based on rupture) = " + str("%.2f" % (total_load * 2/(Fu))) + " square inches"

    else:
        total_load = ("Hmm... something doesn't seem right. Please make sure you have chosen both a design " +
        "\n philosophy and a structural component, as well as have inputted load values. Sorry about that!")
        label2["text"] = value

        
#my_Window.geometry('700x500')
    
button = tk.Button(root, text="Design!", command=design)
label2 = tk.Label(root)
tension_l1 = tk.Label(root)
tension_shape = tk.Label(root)
tension_l2 = tk.Label(root)

#def create_window():
#    if method == "LRFD":
#        window = tk.Toplevel(root)
#        #window.geometry('10x10')
#    elif method == "ASD":
#        window = tk.Toplevel(root)
#        #window.geometry('100x100')
#    
#b = tk.Button(root, text="Create new window", command=create_window)
button.grid(row = 20, column = 0, sticky = "W",pady=(0,10))
label2.grid(row = 21, column = 0, sticky = "W")
tension_l1.grid(row = 22, column = 0, sticky = "W")
tension_shape.grid(row = 23, column = 0, sticky = "W")
tension_l2.grid(row = 24, column = 0, sticky = "W")

root.mainloop()