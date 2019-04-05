import xml.etree.ElementTree as ET
import queue
from xml.etree.ElementTree import Element, SubElement, Comment

from xml.etree import ElementTree
from xml.dom import minidom

nfa_filename = input("Enter the first file name: file1 = ")

nfa_file = [[], [], [], [], nfa_filename]
dfa_file = [[], [], [], [], 'converted_to_dfa.jff']

closure = []  ## store closure state


## read file jff, convert to array

def readFile(file):
    point = file[0]
    trans = file[1]
    initial = file[3]
    final = file[2]
    
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

    i = 0
    for element in transition:
        a = element[0].text
        b = element[1].text
        c = element[2].text
        trans.append([a,b,c])
        i = i+1

    file = [point, trans, final, initial]


readFile(nfa_file)

## find character in language
character = []
for tran in nfa_file[1]:
    if(tran[2] != None):
        if(not tran[2] in character):
            character.append(tran[2])

dpoint = []
dtrans = []
dinitial = []
dfinal = []

state = []
for i in range(len(nfa_file[0])):
    state.append(0)

## finds the epsilon closure of the NFA state "state" and stores it in to "closure"
def epsilonClosure(closearray):
    for i in range(len(nfa_file[1])):
        if(nfa_file[1][i][2] == None):
            closearray.append([nfa_file[1][i][0], nfa_file[1][i][1]])
   
epsilonClosure(closure)
print(closure)
def findclosure(state, arr):
    for i in closure:
        if (i[0] == state):
            if(not i[1] in arr):
                arr.apped(i[1])
    return arr

def findId(state, arr):
    for i in arr:
        # if(state == i[1]):
        #     return i[0]
        # else:
            if(len(state) == len(i[1])):
                count = 0
                for s in state:
                    if (s in i[1]):
                        count += 1
                if(count == len(state)):
                    return i[0]

def checkElement(arr1, arr2):
    for e2 in arr2:
        count = 0
        if(len(e2) == len(arr1)):
            for e1 in arr1:
                if(not e1 in e2): 
                    count += 1
            if(count == 0):
                return True
    return False 


queue_state = queue.Queue(maxsize=2*len(nfa_file[0]))
new_state = []

def makeNewFile(nfile, dfile):
    a = []
    checked = []
    ## a is E(initial)
    a.append(nfile[3][0])
    for i in closure:
        if(i[0] == nfile[3][0]):
            a.append(i[1])
    
    for element in a:
            for e in closure:
                if (element == e[0]):
                    if (not (e[1] in a)):
                        a.append(e[1])
    
    dfile[3].append(0)
    dfile[0].append([0, 'q0'])
    queue_state.put(a)
    count = 0
    new_state.append([count, a])
    count += 1
    while not queue_state.empty():
        u = queue_state.get()
        v1 = []
        v2 = []
        if(u in checked):
            continue
        else:
            checked.append(u)


        ## Find v that element in u can transport to
        for element in u:
            for tran in nfile[1]:
                if(element == tran[0] and tran[2] == character[0]):
                    if(not tran[1] in v1):
                        v1.append(tran[1])
                if(element == tran[0] and tran[2] == character[1]):
                    if(not tran[1] in v2):
                        v2.append(tran[1])
        

        ## find ev = E(v)
        ev1 = v1
        ev2 = v2
        for element in ev1:
            for e in closure:
                if (element == e[0]):
                    if (not (e[1] in ev1)):
                        ev1.append(e[1])
        
        for element in ev2:
            for e in closure:
                if (element == e[0]):
                    if (not (e[1] in ev2)):
                        ev2.append(e[1])

        if(ev1 == []):
            dfile[0].append([count, 'q' + str(count)])
            dfile[1].append([count, count, character[0]])
            dfile[1].append([count,count, character[1]])
            dfile[1].append([findId(u, new_state), count, character[0]])
            count += 1
        else:
            if(not checkElement(ev1, checked)):
                if(not checkElement(ev1, queue_state.queue)):
                    new_state.append([count, ev1])
                    dfile[0].append([count, 'q' + str(count)])
                    count += 1
                    queue_state.put(ev1)
                dfile[1].append([findId(u, new_state), count-1, character[0]])
                    
            else:
                dfile[1].append([findId(u, new_state), findId(ev1, new_state), character[0]])

        if(ev2 == []):
            dfile[0].append([count, 'q' + str(count)])
            dfile[1].append([count, count, character[0]])
            dfile[1].append([count,count, character[1]])
            dfile[1].append([findId(u, new_state), count, character[1]])
            count += 1
        else:
            if(not checkElement(ev2, checked)):
                if(not checkElement(ev2, queue_state.queue)):
                    new_state.append([count, ev2])
                    dfile[0].append([count, 'q' + str(count)])
                    
                    count += 1
                    queue_state.put(ev2)
                dfile[1].append([findId(u, new_state), count-1, character[1]])
            else:
                dfile[1].append([findId(u, new_state), findId(ev2, new_state), character[1]])
                # print(ev2)
        

          
    for element in new_state:
        for e in element[1]:
            if (e in nfile[2]):
                dfile[2].append(element[0])
                break
    print(checked)
    print(new_state)
    print(dfile[0])
    print(dfile[1])
    print(dfile[2])
    print(dfile[3])
    print(dfile[4])

    

makeNewFile(nfa_file, dfa_file)
    
# makeNewFile(nfa_file)


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

        

    output = prettify(top)
    filename = open(str(file[4]), 'w')
    filename.write(output)
    # print(output)

write_jff_file(dfa_file)
