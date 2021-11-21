import re
import sys
import pyttsx3
from latext import latex_to_text as lat


def fraction(substr):
    pass


def integral(substr):
    # \int_{-1}^x (3 + t^2)\,dt #TODO:: possibly replace dt
    # if there is an underscore there are limits
    limitIndex = substr.find('_')
    if limitIndex == -1:
        return substr.replace('\int', 'integral of ')

    limitIndex += 1
    lim_a = ""
    lim_b = ""
    term_a_done = False
    old = "\int_"
    while substr[limitIndex] != " ":
        if substr[limitIndex] == "^":
            term_a_done = True
        elif term_a_done != True and (substr[limitIndex] != "{") and (substr[limitIndex] != "}"):
            lim_a += substr[limitIndex]
        elif substr[limitIndex] != "{" and substr[limitIndex] != "}":
            lim_b += substr[limitIndex]
        limitIndex += 1
        old += substr[limitIndex]

    return substr.replace(old, 'integral from' + lim_a + ' to ' + lim_b + " ")


def dollarSign(mathStr):
    mathStr = mathStr.strip(('\displaystyle'))
    # {A(x) = \int_{-1}^x (3 + t^2)\,dt}
    if ('int' in mathStr):
        result = integral(mathStr)
    pass


def mathParse(strLine):
    strLine = (strLine.strip('\n'))
    if '\item' in strLine:
        strLine = strLine.strip(('\item'))

        # split string by $ to interpret math
        if '$' in strLine:
            splitStrings = strLine.split('$')
            for i in range(int(len(splitStrings)-1 / 2)):
                splitStrings[i + 1] = dollarSign(splitStrings[i + 1])

            # rejoin string sections
            strLine = " ".join(splitStrings)

        # clear remaining latex syntax
        strLine = lat(strLine)
        return strLine.lstrip()  # returns with whitespace removed

    return ""


if __name__ == '__main__':
    engine = pyttsx3.init()

    f = open("testFile2.tex", 'r')
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
            print(str(num) + " " + strippedLine)
            engine.say(strippedLine)
            engine.runAndWait()
            num += 1
        line = f.readline()