import xml.etree.ElementTree as xml

msg = xml.Element("msg")
child = xml.SubElement(msg, "command")
child.text = "command"
child = xml.SubElement(msg, "value")
child.text = "value"
child = xml.SubElement(msg, "topic")
child.text = "topic"
child = xml.SubElement(msg, "type")
child.text = "tipo"
child = xml.SubElement(msg, "serialize")
child.text = "serialize"

gg = {}
for child in msg:
    print(child.tag, child.text)
    gg[child.tag] = child.text
print(gg)
