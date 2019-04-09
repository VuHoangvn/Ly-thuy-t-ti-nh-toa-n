import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment

from xml.etree import ElementTree
from xml.dom import minidom

import copy

CFG_file = input("Enter the input file name: CFG_file = ")
Chomsky_file = input("Enter the output file name: Chomsky_file = ")

grammar = []
chomsky_grammar = []
final_point = []
non_final_point = []

##
## read the input file to get grammar
##


def readFile(file):
    
    f = open(file)
    t = f.read()
    root = ET.fromstring(t)

    left = root.findall(".//left")
    right = root.findall(".//right")

    for i in range(0,len(left)):
        grammar.append([left[i].text, right[i].text])

##
## add the start S0 -> S
##


def add_start_point():
    global chomsky_grammar
    chomsky_grammar = copy.deepcopy(grammar)
    chomsky_grammar = [['S0', grammar[0][0]]] + chomsky_grammar
    non_final_point.append('S0')

##
## find final and non final point
##

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


##
## delete epsilon derivation
##

def delete_n_element(k, n, point, collect, added):
    if(k > n):
       return 
    for i in range (0,len(collect[1])):
        if(point in collect[1]):
            temp = copy.deepcopy(collect)
            if(point == temp[1][i]):
                temp[1] = temp[1][:i] + temp[1][i+1:]
                if([temp[0],temp[1]] not in added):
                    chomsky_grammar.append([temp[0], temp[1]])
                    added.append([temp[0], temp[1]])             
                    
            delete_n_element(k+1, n, point, temp, added)

def eliminate_epsilon_derivative():
    eliminated = []
    added = []

    for der in chomsky_grammar:
        if(der[1] == None and der[0] in non_final_point):
            eliminated.append(der[0])
            chomsky_grammar.remove(der)
            checked = []
            for der1 in chomsky_grammar:
                if(der1 not in checked and der1 not in added):
                    checked.append(der1)
                    if(der1[1] == None):
                        continue
                    for i in der1[1]:         
                        if(der[0] in der1[1]):
                            if(len(der1[1]) == 1):
                                if(der1[0] not in eliminated):
                                    chomsky_grammar.append([der1[0], None])
                            else:  
                                count = 0
                                for e in der1[1]:
                                    if(e == der[0]):
                                        count += 1
                                if(count>0):
                                    delete_n_element(1,count, der[0], der1, added)

##
## delete single derivative
##

def eliminate_single_derivative():
    eliminated = []
    for der in chomsky_grammar:
        if(len(der[1]) == 1 and der[1][0] in non_final_point):
            for der1 in chomsky_grammar:
                if(der[1][0] == der1[0]):
                    
                    if([der[0], der1[1]] not in eliminated and [der[0], der1[1]] not in chomsky_grammar):
                        chomsky_grammar.append([der[0], der1[1]])
                        
            chomsky_grammar.remove(der)
            eliminated.append(der)

##
## convert to standard
##

def conver_to_standard():
    new_state = []
    i = 0
    j = 0
    append = []
    for p in final_point:
        chomsky_grammar.append(['U' + str(j), [p]])
        append.append(['U' + str(j), [p]])
        j += 1
    for der in chomsky_grammar:
        if(len(der[1]) > 2):
            checked = 0
            for state in new_state:
                if(der[1][1:] == state[1]):
                    new_der = []
                    new_der.append(der[1][0])
                    new_der.append(state[0])
                    chomsky_grammar.append([der[0], new_der])
                    checked = 1
                    break 
            if(checked == 0):
                new_state.append(['A' + str(i), der[1][1:]])
                new_der = []
                new_der.append(der[1][0])
                new_der.append('A' + str(i))
                chomsky_grammar.append([der[0], new_der])
            chomsky_grammar.remove(der)
            i += 1
        else:
            if(len(der[1]) == 2):
                for e in range(0, len(der[1])):
                    if(der[1][e] in final_point):
                        for ele in append:
                            if(der[1][e] == ele[1][0]):
                                der[1][e] = ele[0]
    for state in new_state:
        if(len(state[1]) == 2):
            chomsky_grammar.append(state)

##
## convert to Chomsky
##

def convert_CFG_to_Chomsky():
    add_start_point()
    get_final_non_final_point()
    eliminate_epsilon_derivative()
    eliminate_single_derivative()
    eliminate_single_derivative()
    conver_to_standard()


##
## print to file
##

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml()

def write_jff_file(filename):
    top= Element('structure')
    
    type = SubElement(top, 'type')
    type.text = 'grammar'

    for der in chomsky_grammar:
        production = SubElement(top, 'production')
        left = SubElement(production, 'left')
        left.text = str(der[0])
        right = SubElement(production, 'right')
        right.text = str(der[1])
    
    output = prettify(top)
    file = open(filename, 'w')
    file.write(output)


##
## main function
##


def main():
    readFile(CFG_file)
    convert_CFG_to_Chomsky()
    write_jff_file(Chomsky_file)

if __name__ == '__main__':
    main()