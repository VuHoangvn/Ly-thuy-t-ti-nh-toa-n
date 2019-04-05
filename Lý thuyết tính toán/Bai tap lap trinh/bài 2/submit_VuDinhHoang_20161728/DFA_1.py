import xml.etree.ElementTree as ET

## input filename, word

file = input("Enter the .jff file: file = ")
word = input("Enter the word: w = ")
# word = "abbbb"

f = open(file)
t = f.read()

## read file

root = ET.fromstring(t)
# print (t)
state = root.findall(".//state")
transition = root.findall(".//transition")

# init list contain point, transitions, final note, initial note

point = []
trans = []
final = []
initial = []

# fill out lists
i = 0
for element in state:
    a = element.get('id')
    b = element.get('name')
    point.append([a,b])
    # print(point[i][0], point[i][1])
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
    # print(trans[i][0], trans[i][1], trans[i][2])
    i = i+1

# print("Initial: ", initial)
# print("Final: ", final)

current = point[int(initial[0])][0]

## check word

for character in word:
    for tran in trans:
        if tran[0] == current :
            if tran[2] == character:
                current = tran[1]
                break
# print(current)
count = 0
for fin in final:
    # print(fin)
    if(current == fin):
        count = count + 1

if count == 0:
    print("No")
else:
    print("Yes")