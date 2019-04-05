import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment

from xml.etree import ElementTree
from xml.dom import minidom

filename1 = input("Enter the first file name: file1 = ")
filename2 = input("Enter the second file name: file2 = ")
# word = input("Enter the word: w = ")


# filename1 = "testJFLAP.jff"
# filename2 = "testJFLAP2.jff"
union_file_name = "union.jff"
intersection_file_name = "intersection.jff"
# word1 = "abbb"
# word2 = "mmnn"

#point, trans, final, initial
file1 = [[], [], [], [], filename1]
file2 = [[], [], [], [], filename2]
union_file = [[], [], [], [], union_file_name]
intersection_file = [[], [], [], [], intersection_file_name]



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

readFile(file1)
readFile(file2)

upoint = union_file[0]
utrans = union_file[1]
ufinal = union_file[2]
uinitial = union_file[3]

ipoint = intersection_file[0]
itrans = intersection_file[1]
ifinal = intersection_file[2]
iinitial = intersection_file[3]

## init list for new langue
def makeNewFile(f1, f2):
    point1 = f1[0]
    trans1 = f1[1]

    point2 = f2[0]
    trans2 = f2[1]

    i = 0
    for p1 in point1:
        for p2 in point2:
            upoint.append([i, p1[1]+p2[1]])
            ipoint.append([i, p1[1]+p2[1]])
            if file1[3].count(p1[0]) > 0 and file2[3].count(p2[0])> 0:
                uinitial.append(i)
            
            if file1[2].count(p1[0]) > 0 or file2[2].count(p2[0])> 0:
                ufinal.append(i)
            
            if file1[3].count(p1[0]) > 0 and file2[3].count(p2[0])> 0:
                iinitial.append(i)
            
            if file1[2].count(p1[0]) > 0 and file2[2].count(p2[0])> 0:
                ifinal.append(i)
            i = i+1
    
    #id bat dau
    start1 = int(point1[0][0])
    start2 = int(point2[0][0])
    print(start1)
    print(start2)
    for t1 in trans1:
        for t2 in trans2:
            a = point1[int(t1[0])-start1][1] 
            b = point1[int(t1[1])-start1][1] 
            c = point2[int(t2[0])-start2][1]
            d = point2[int(t2[1])-start2][1]
            
            if(t1[2] is(t2[2])):

                # x = [a+c, b+d, t1[2]]
                # if(x in utrans):
                #     continue
                # else:
                for u in upoint:
                    if(u[1] == a+c):
                        x = u[0]
                    if(u[1] == b+d):
                        y = u[0]
                utrans.append([x,y,t1[2]])
                itrans.append([x,y,t1[2]])
            

makeNewFile(file1, file2)

union_file = (upoint, utrans, ufinal, uinitial, union_file_name)
intersection_file = (ipoint, itrans, ifinal, iinitial, intersection_file_name)

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
        state = SubElement(automaton, 'state', id = str(point[0]), name={point[1]})
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

# print(intersection_file[1])
write_jff_file(union_file)
write_jff_file(intersection_file)

