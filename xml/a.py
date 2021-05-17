# -*-coding:utf-8-*

import os
from xml.etree.ElementTree import *

tree = parse('a.xml')
root = tree.getroot()

items = [x for x in root.findall('item[@date]') if 'estimate' not in x.attrib]
print(items)
