import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment

from xml.etree import ElementTree
from xml.dom import minidom


Chomsky_file = input("Enter the output file name: Chomsky_file = ")
input_string = input("Enter the input string: input_string = ")
n = len(input_string)

grammar = []
final_point = []
non_final_point = []
table = []
##################################
def readFile(file):
    
    f = open(file)
    t = f.read()
    root = ET.fromstring(t)

    left = root.findall(".//left")
    right = root.findall(".//right")

    for i in range(0,len(left)):
        grammar.append([left[i].text, right[i].text])

###################################
def get_final_non_final_point():
    for der in grammar:
        if(not der[0].islower()):
            if(der[0] not in non_final_point):
                non_final_point.append(der[0])
        else:
            if(der[0] not in final_point):
                final_point.append(der[0])
        if(der[1] == None):
            continue
        for d in der[1]:
            if(not d[0].islower()):
                if(d[0] not in non_final_point):
                    non_final_point.append(d[0])
            else:
                if(d[0] not in final_point):
                    final_point.append(d[0])
####################################
def make_table():
    for i in range(0,n):
        x = []
        for i in range(0,n):
            x.append([])
        table.append(x)
def Check_String():
    make_table()

    start = grammar[0][0]

    ## execute epsilon
    if(input_string == ''):
        for der in grammar:
            if(der[0] == start):
                if(der[1] == None):
                    return True
    
    ## execute 1-length substring
    for i in range(0, n):
        for c in non_final_point:
            for der in grammar:
                if(der[0] == c and der[1] == input_string[i]):
                    table[i][i].append(c)
    
    ##  execute l-length substring
    for l in range(2, n+1):
        for i in range(1, n-l+2):
            j = i+l-1
            for k in range(i, j):
                for der in grammar:
                    if(len(der[1]) == 2):
                        if(der[1][0] in table[i-1][k-1] and der[1][1] in table[k][j-1]):
                            table[i-1][j-1].append(der[0])
    print(table)
    if(start in table[0][n-1]):
        return True  
    return False
    



####################################    
def main():
    readFile(Chomsky_file)
    get_final_non_final_point()
    if(Check_String()):
        print('Yes')
    else:
        print('No')

if __name__ == '__main__':
    main()