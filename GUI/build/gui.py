from pathlib import Path
import pyttsx3
from latext import latex_to_text as lat
from tkinter import *
import threading
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog

stop = False
Value = ""

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def fraction(substr):
    index = -1
    for i in range(len(substr)):
        if substr[i] + substr[i + 1] + substr[i + 2] + substr[i + 3] == "frac":
            index = i + 4
            break
    if index == -1:
        return substr

    num_braces = 0
    numerator = ""
    denominator = ""
    old = "frac"
    while num_braces < 2:
        if substr[index] == "}":
            num_braces += 1
        if num_braces == 0 and substr[index] != "{" and substr[index] != "}":
            numerator += substr[index]
        elif num_braces == 1 and substr[index] != "{" and substr[index] != "}":
            denominator += substr[index]
        old += substr[index]
        index += 1

    return substr.replace(old, numerator + " over " + denominator)


def integral(substr):
    # if there is an underscore there are limits
    limitIndex = substr.find('_')
    if limitIndex == -1:
        return substr.replace('\int', 'integral of ')

    limitIndex += 1

    lim_a = ""
    lim_b = ""
    term_a_done = False
    old = "\int_"
    old += substr[limitIndex]

    while substr[limitIndex] != " ":
        if substr[limitIndex] == "^":
            term_a_done = True
        elif term_a_done != True and (substr[limitIndex] != "{") and (substr[limitIndex] != "}"):
            lim_a += substr[limitIndex]
        elif substr[limitIndex] != "{" and substr[limitIndex] != "}":
            lim_b += substr[limitIndex]
        limitIndex += 1
        old += substr[limitIndex]

    return substr.replace(old, 'integral from ' + lim_a + ' to ' + lim_b + " of ")


def summation(substr):
    # if there is an underscore there are limits
    boundIndex = substr.find('_')
    if boundIndex == -1:
        return substr.replace('\sum', 'summation of ')

    boundIndex += 1

    bound_a = ""
    bound_b = ""
    term_a_done = False
    endFound = False
    old = "\sum_"
    old += substr[boundIndex]

    while not endFound or not term_a_done:
        if substr[boundIndex] == "^":
            term_a_done = True
        elif term_a_done != True and (substr[boundIndex] != "{") and (substr[boundIndex] != "}"):
            bound_a += substr[boundIndex]
        elif substr[boundIndex] != "{" and substr[boundIndex] != "}":
            bound_b += substr[boundIndex]

        if term_a_done and substr[boundIndex + 1] == " ":
            endFound = True

        boundIndex += 1
        old += substr[boundIndex]

    return substr.replace(old, 'summation from ' + bound_a + ' to ' + bound_b + " of ")


def dollarSign(mathStr):
    mathStr = mathStr.replace('\displaystyle', "")
    if ('int' in mathStr):
        result = integral(mathStr)
        if ('frac' in mathStr):
            result = fraction(result)
    elif ('frac' in mathStr):
        result = fraction(mathStr)
    elif ('sum' in mathStr):
        result = summation(mathStr)
    else:
        result = mathStr

    return result


def mathParse(strLine):
    strLine = (strLine.strip('\n'))
    if '\item' in strLine:
        strLine = strLine.strip(('\item'))

        # split string by $ to interpret math
        if '$' in strLine:
            dlim = '$'
            splitStrings = [e + dlim for e in strLine.split(dlim) if e]
            for i in range(int(len(splitStrings) / 2)):
                splitStrings[2 * i + 1] = dollarSign(splitStrings[2 * i + 1])

            # rejoin string sections
            strLine = " ".join(splitStrings)

        # clear remaining latex syntax
        strLine = lat(strLine)
        return strLine.lstrip()  # returns with whitespace removed

    return ""


def speech():
    engine = pyttsx3.init()
    f = open(entry_1.get(), 'r')
    lines = f.readlines()
    println = False
    num = 0
    for line in lines:
        if line == "\\begin{enumerate}\n":
            println = True
        elif line == "\\end{enumerate}\n":
            println = False
        if println:
            strippedLine = mathParse(line)
            print(strippedLine)
            engine.say(strippedLine)
            engine.runAndWait()
            num += 1
        line = f.readline()
        if stop:
            break

def select_path(event):
    global output_path

    output_path = filedialog.askopenfilename()
    entry_1.delete(0, END)
    entry_1.insert(0, output_path)


def btn_clicked():
    Value = entry_1.get()
    print(Value)


def player():
    stop = False
    speech()


def stoper():
    stop = True


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("700x600")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=600,
    width=700,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    350.0,
    300.0,
    image=image_image_1
)

canvas.create_rectangle(
    0.0,
    41.0,
    700.0,
    179.0,
    fill="#727272",
    outline="")

canvas.create_rectangle(
    0.0,
    324.0,
    700.0,
    462.0,
    fill="#727272",
    outline="")

canvas.create_rectangle(
    80.0,
    347.0,
    620.0,
    378.0,
    fill="#C4C4C4",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    #command=lambda: threading.Thread(target=player, daemon=True).start(),
    command=lambda: player(),
    relief="flat"
)
button_1.place(
    x=80.0,
    y=393.0,
    width=149.0,
    height=50.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: stoper(),
    relief="flat"
)
button_2.place(
    x=275.0,
    y=393.0,
    width=149.0,
    height=50.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: btn_clicked(),
    relief="flat"
)
button_3.place(
    x=471.0,
    y=393.0,
    width=149.0,
    height=50.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    399.5,
    362.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#727272",
    highlightthickness=0
)
entry_1.place(
    x=194.5,
    y=347.0,
    width=410.0,
    height=29.0
)
entry_1.bind("<1>", select_path)

canvas.create_text(
    85.0,
    352.0,
    anchor="nw",
    text="Path to file:",
    fill="#000000",
    font=("Roboto Bold", 18 * -1)
)

canvas.create_text(
    179.0,
    52.0,
    anchor="nw",
    text="SleepUnderflow",
    fill="#000000",
    font=("Roboto Bold", 48 * -1)
)

canvas.create_text(
    180.0,
    108.0,
    anchor="nw",
    text="Latex-to-speech",
    fill="#000000",
    font=("Roboto", 48 * -1)
)
window.resizable(False, False)
window.mainloop()
