from src.protocols.topic_Tree import Node

root = Node("root", None)

#root.getNode("/weather/tmp/c")

topic = "arroz/temp"
c = 1
split = []
lastindex = 0
for letter in topic[1:]:
    if letter == "/":
        split.append(topic[lastindex:c])
        lastindex = c
    c += 1
split.append(topic[lastindex:])

print(split)
        