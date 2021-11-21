import pyttsx3
from latext import latex_to_text as lat


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
            print(strippedLine)
            engine.say(strippedLine)
            engine.runAndWait()
            num += 1
        line = f.readline()