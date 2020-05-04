import xml.etree.ElementTree as ET
# importing tkinter and tkinter.ttk
# and all their functions and classes
from tkinter import *
from tkinter.ttk import *

# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfile

rootGui = Tk()
rootGui.title("VfrFlight4XP")
rootGui.geometry('650x200')

filetoGenerate = ""
name = ""

# This function will be used to open
# file in read mode and only Python files
# will be opened
def open_file():
    global filetoGenerate, name, filename
    file = askopenfile(mode='r')
    if file is not None:
        name = file.name.split("/")[-1].split(".")[0]
        filetoGenerate = file
        filename['text'] = name

label = Label(rootGui, text="Wybierz plik z planem lotu wygenerowanym przez VFR Flight (rozszerzenie .vfr)")
label.pack(side=TOP, pady=10)

filename = Label(rootGui, text="Wprowadź plik")
filename.pack(side=TOP)

btn = Button(rootGui, text='Open', command=lambda: open_file())
btn.pack(side=TOP)

btn = Button(rootGui, text="Wygeneruj plik", command=lambda: generateExport(filetoGenerate, name))
btn.pack(side=TOP, pady=10)

statusLabel = Label(rootGui, text='')
statusLabel.pack(side=TOP, pady=5)


def coord(sec, min, deg):
    coordinates = (float(sec) / 3600) + (float(min) / 60) + float(deg)
    coordinates = str(coordinates).split(".")
    coordinates[1] = coordinates[1][:6]
    coordinates[1] = coordinates[1][::-1].zfill(6)[::-1]
    coordinates = ".".join(coordinates)
    return coordinates

def generateExport(file, name):
    global statusLabel
    if file == '' or name == '':
        statusLabel['text'] = 'Nie wprowadzono pliku'
        return

    tree = ET.parse(file)
    root = tree.getroot()

    points = []

    for elem in root:
        for subelem in elem:
            try:
                coords = []
                for subsubelem in subelem:
                    coords.append(coord(subsubelem.attrib['sec'], subsubelem.attrib['min'], subsubelem.attrib['deg']))

                point = subelem.attrib['name']
                point = point.split("/")
                points.append([point[0], subelem.attrib['alt'], coords[0], coords[1]])
            except Exception as e:
                #print(repr(e))
                pass

    file = open("{}.fms".format(name), "w+")
    file.writelines("I\n3 version\n1\n11\n")

    for point in points:
        line = "1 {point} {alt}00000 {deg1} {deg2}\n".format(
            point=point[0],
            alt=point[1],
            deg1=point[2],
            deg2=point[3]
        )
        file.writelines([line])

    statusLabel['text'] = 'Wygenerowano plik'


mainloop()
# FORMAT
# 1 EPKK 791.000000 50.077778 19.785417
# 1 <name> <alt.000000> <deg1> <deg2>
