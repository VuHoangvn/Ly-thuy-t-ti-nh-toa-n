import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment

from xml.etree import ElementTree
from xml.dom import minidom


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
            if(tran[1] == qloop):
                derivative_of_start.append(tran[4])   
                if([start, derivative_of_start] not in derivative): 
                    derivative.append([start, derivative_of_start])
                derivative_of_start = []
                continue
            derivative_of_start.append(tran[4])
            getElement(qloop, tran, file, derivative_of_start)
    if([start, derivative_of_start] not in derivative):    
        derivative.append([start, derivative_of_start])

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
    
    for tran in file[1]:
        if(tran[4] == '$'):
            for t in file[1]:
                if(t[0] == tran[1]):
                    qloop = t[1]
                    start_point = t[4]
        

    for tran in file[1]:
        if(tran[4] == start_point or tran[4] == '$'):
            continue
        if(tran[4] != None and tran[4] not in non_final):
            non_final.append(tran[3])

    for tran in file[1]:
        if(tran[4] == start_point or tran[4] == '$'):
            continue
        if(tran[4] == None and tran[4] not in final and tran[4] not in non_final):
            final.append(tran[3])
        
            
    for tran in file[1]:
        

        if(tran[0] == qloop and tran[3] in non_final_point):
            getDerevative(qloop, tran[3], file, gram)

    print(gram)


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

        pop = SubElement(tran, 'pop')
        pop.text = str(tran[3])

        push = SubElement(tran, 'push')
        push.text = str([tran[4]])

        

    output = prettify(top)
    filename = open(str(file[4]), 'w')
    filename.write(output)
    print(output)



def main():
    readFile(g_file)
    getGrammar(g_file, grammar, final_point, non_final_point)
    ##write_jff_file(chomsky_file)



if __name__ == '__main__':
    main()