import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment

from xml.etree import ElementTree
from xml.dom import minidom

import copy


##
## initial arrays
##


g_filename = input("Enter the first file name: file = ")

## point, trans, final, initial
g_file = [[], [], [], [], g_filename]
chomsky_file = [[], [], [], [], 'Chomsky.jff']

## final_point and non_final_point

final_point = []
non_final_point = []

## save grammar

grammar = []

chomsky_grammar = []

qloop = None
start_point = None
##
## read jff input file
##


def readFile(file):
    point = file[0]
    trans = file[1]
    initial = file[3]
    final = file[2]
    file_name = file[4]
    
    f = open(file[4])
    t = f.read()
    root = ET.fromstring(t)
    print(root)

    state = root.findall(".//state")
    transition = root.findall(".//transition")
    
    i = 0
    for element in state:
        a = element.get('id')
        b = element.get('name')
        point.append([a,b])
        i = i + 1
    

        for sta in element.iter('final'):
            final.append(element.get('id'))
        for sta in element.iter('initial'):
            initial.append(element.get('id'))

    for element in transition:
        from_p = element[0].text
        to_p = element[1].text
        read_c = element[2].text
        pop_c = element[3].text
        push_c = element[4].text
        
        trans.append([from_p, to_p, read_c, pop_c, push_c])

    file = [point, trans, final, initial, file[4]]

    # print(file[0])
    # print('-------------')
    # print(file[1])
    # print('-------------')
    # print(file[2])
    # print('-------------')
    # print(file[3])
    # print('-------------')
    # print(file[4])
    # print('-------------')



##
## get derivative
##

def getDerevative(qloop,start, file, derivative):
    derivative_of_start = []
    for tran in file[1]:
        
        
        if(tran[3] == start):
            derivative_of_start.append(tran[4]) 
            if(tran[1] == qloop):  
                if([start, derivative_of_start] not in derivative): 
                    derivative.append([start, derivative_of_start])
                
            else:
                getElement(qloop, tran, file, derivative_of_start)
                if([start, derivative_of_start] not in derivative):    
                    derivative.append([start, derivative_of_start])
        derivative_of_start = []
def getElement(qloop, tran, file, derivative_of_start):
     if(tran[1] == qloop):
         return derivative_of_start
     for trans in file[1]:
         if(trans[0] == tran[1]):
             derivative_of_start.append(trans[4])
             getElement(qloop, trans, file, derivative_of_start)
             break


##
## get the grammar
##

def getGrammar(file, gram, final, non_final):
    
    global qloop
    global start_point
    
    for tran in file[1]:
        if(tran[4] == '$'):
            for t in file[1]:
                if(t[0] == tran[1]):
                    qloop = t[1]
                    start_point = t[4]

        

    for tran in file[1]:
        if(tran[4] == '$'):
            continue
        if(tran[4] != None and tran[3] != None and (tran[3] not in non_final)):
            non_final.append(tran[3])

    for tran in file[1]:
        if(tran[4] == '$' or tran[3] == '$'):
            continue
        if(tran[4] == None  and tran[3] not in final and tran[3] not in non_final):
            final.append(tran[3])
        
            
    for tran in file[1]:
        

        if(tran[0] == qloop and tran[3] in non_final_point):
            getDerevative(qloop, tran[3], file, gram)
            
    # print(gram)



##
## Convert CFG to chomsky
##

## execute start point

def execute_start_point():
    global chomsky_grammar
    chomsky_grammar = copy.deepcopy(grammar)
    chomsky_grammar.append(['S0', ['S']])
    # print(chomsky_grammar)

## eliminate A-> epsilon

def delete_n_element(k, n, point, collect, added):
    if(k > n):
       return 
    for i in range (0,len(collect[1])):
        if(point in collect[1]):
            temp = copy.deepcopy(collect)
            if(point == temp[1][i]):
                temp[1].pop(i)
                if([temp[0],temp[1]] not in added):
                    chomsky_grammar.append([temp[0], temp[1]])
                    added.append([temp[0], temp[1]])
                    
                    
                    
            delete_n_element(k+1, n, point, temp, added)
    
def eliminate_epsilon_derivative():
    
    eliminated = []
    added = []
    
    for der in chomsky_grammar:
        if(len(der[1]) == 1 and None in der[1] and der[0] in non_final_point):
            eliminated.append(der[0])
            chomsky_grammar.remove(der)
            checked = []
            for der1 in chomsky_grammar:
                if(der1 not in checked and der1 not in added):
                    checked.append(der1)
                    for i in der1[1]:         
                        
                        if(der[0] in der1[1]):
                            if(len(der1[1]) == 1):
                                if(der1[0] not in eliminated):
                                    chomsky_grammar.append([der1[0], [None]])
                            else:
                                
                                count = 0
                                for e in der1[1]:
                                    if(e == der[0]):
                                        count += 1
                                if(count>0):
                                    delete_n_element(1,count, der[0], der1, added)

                                
                                
    # print(checked)
    # print(chomsky_grammar)
    # print(eliminated)

## eliminate single derivative

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
    # print(checked)
    # # print(eliminated)
    

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

def convert_CFG_to_Chomsky():
    execute_start_point()
    eliminate_epsilon_derivative()
    eliminate_single_derivative()
    eliminate_single_derivative()
    conver_to_standard()

def make_Chomsky_file(file):
    for i in range(0,4):
        file[0].append([i, 'q' + str(i)])
    file[1].append([0,1,None, None, '$'])
    file[1].append([1,2, None, None, 'S0'])
    file[1].append([2,3,None, '$', None])
    file[3].append(0)
    file[2].append(3)
    i = 4
    for point in final_point:
        file[1].append([2,2,point, point, None])
    for der in chomsky_grammar:
        if(len(der[1]) == 1):
            file[1].append([2,2,None,der[0], der[1][0]])
        else:
            file[0].append([i, 'q' + str(i)])
            file[1].append([2, i, None, der[0], der[1][0]])
            i += 1
            for e in range(1, len(der[1])-1):
                file[1].append([i-1, i, None, None, der[1][e]])
                i += 1
            file[1].append([i-1, 2, None, None, der[1][-1]])

##
## print to jff file
##


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml()


def write_jff_file(file):
    top = Element('structure')

    type = SubElement(top, 'type')
    type.text = 'fa'

    automaton = SubElement(top, 'automaton')
    comment = Comment('This list of states.')
    automaton.append(comment)

    for point in file[0]:
        state = SubElement(automaton, 'state', id = str(point[0]), name=point[1])
        x = SubElement(state, 'x')
        x.text = '10'
        y = SubElement(state, 'y')
        y.text = '20'
        if file[3].count(point[0]) > 0:
            initial = SubElement(state, 'initial')
        
        if file[2].count(point[0]) > 0:
            final = SubElement(state, 'final')
    
    comment = Comment('This list of transitions.')
    automaton.append(comment)

    for trans in file[1]:
        tran = SubElement(automaton, 'transition')
        
        fr = SubElement(tran, 'from')
        fr.text = str(trans[0])

        t = SubElement(tran, 'to')
        t.text = str(trans[1])

        r = SubElement(tran, 'read')
        r.text = str(trans[2])

        left = SubElement(tran, 'left')
        left.text = str(tran[3])

        right = SubElement(tran, 'right')
        right.text = str([tran[4]])

        

    output = prettify(top)
    filename = open(str(file[4]), 'w')
    filename.write(output)
    
    print(output)



def main():
    readFile(g_file)
    getGrammar(g_file, grammar, final_point, non_final_point)
    convert_CFG_to_Chomsky()
    make_Chomsky_file(chomsky_file)
    write_jff_file(chomsky_file)




if __name__ == '__main__':
    main()