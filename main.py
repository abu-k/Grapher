import matplotlib.pyplot as plt
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog


# Creates folder for the graphs
def create_folder(path):
    try:
        if os.path.isdir(path):
            pass
        else:
            os.makedirs(path)
    except IOError as exception:
        raise IOError('%s: %s' % (path, exception.strerror))
    return None


# Iterates over all files in the current folder, if file is .csv calls the data() function for processing
def all_files():
    for i in os.listdir(""):
        if i.split(".")[-1] == "csv":
            data(i)


# If User only wants to analyze one .csv file this function is called, and opens a file dialog for user to select
# a specific file
def only_one():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    data(file_path)
    again = input("Would you like to analise another? (y or n)")
    if again == "y":
        only_one()
    else:
        print("All done")


# The bulk of the processing is here
def data(file_path):
    save_folder = file_path.split("/")[-1].split(".")[0]
    value_dic = {}
    with open(file_path) as f:
        content = f.readlines()
    start_from = 4
    count = 0
    for i in content:
        current_sample = i.strip(",")
        if count >= start_from - 1:
            i = i.strip("\n")
            if i.startswith("Sample"):
                value_dic[current_sample] = []
            elif i == "\n" or i == "," or i == " " or i == "":
                pass
            elif i[0].isdigit():
                if float(i.split(",")[0]) > 0.1:
                    value_dic[current_sample].append((float(i.split(",")[0]), float(i.split(",")[1])))
        else:
            count += 1

    summary = ""
    for i in value_dic.keys():
        summary += (i + ":")
        summary += ("\nNumber of values in " + i + " is: " + str(len(value_dic[i])))

        remove = int(len(value_dic[i]) * .1)
        temp_list = value_dic[i][remove:-remove]
        summary += ("\nAfter removing 10% off each side, number of values\n"
                    "     in " + i + " is " + str(len(temp_list)))
        total = 0
        for j in temp_list:
            total += j[0]
        summary += ("\nAverage of force for " + i + " is " + str(total / len(temp_list)))
        summary += "\n-----------------------------------\n"

        force = []
        displacement = []
        for k in temp_list:
            force.append(k[0])
            displacement.append(k[1])
        df = pd.DataFrame({'x': displacement, 'y': force})
        plt.plot('x', 'y', data=df, linestyle='-', marker='o')
        plt.xlabel("Displacement")
        plt.ylabel("Force")
        sample_title = "Force vs Displacement for " + i + "\nAvg force: " + str(total / len(temp_list))
        plt.title(sample_title)
        create_folder(save_folder)
        plt.savefig(save_folder + "/" + i + ".png")
        print("Saving plot", i + ".png")
        plt.clf()
    print("Writing Summary to output file Output.txt")
    with open(save_folder + "\\Output.txt", "w") as text_file:
        text_file.write(summary)


choice = input("Would you like to analise all csv files in the folder (y or n)?")
if choice == "y":
    all_files()
else:
    only_one()
