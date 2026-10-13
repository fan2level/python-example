import os
from typing import Optional
from pathlib import Path
import xml.etree.ElementTree as ET

class pXml2Dict:
    tag  ="#tag"
    attr ="#attr"
    text ="#text"
    child="#child"
    def __init__(self, xml: Path):
        self._xml = {}
        try:
            tree = ET.parse(xml.as_posix())
            root = tree.getroot()
        except Exception as e:
            print(f"[exception] {e}")
            return
        self._load0(root, self._xml)

    def _load0(self, node: ET.Element, xml: dict):
        ''' convert xml tag, attribute, text to dict
            and make dict recursive from xml
        '''
        xml[self.tag] = node.tag
        if node.attrib is not None and len(node.attrib) > 0:
            xml[self.attr] = node.attrib
        if node.text is not None and node.text.strip():
            xml[self.text] = node.text
        for node0 in node:
            x = {}
            if self.child not in xml:
                xml[self.child] = []
            xml[self.child].append(x)
            self._load0(node0, x)
    def find_child(self, xml: dict) -> Optional[dict]:
        ''' find #child key and return
            return None if doesn't exist
        '''
        if xml is None or self.child not in xml:
            return None
        return xml[self.child]
    def find_tag(self, xml: dict, tag: str) -> Optional[dict]:
        ''' find #tag key and return matching value under #child
            return None if not exist
        '''
        xchild = self.find_child(xml)
        if xchild is None:
            return None
        return next((x for x in xchild
                     if self.tag in x and x[self.tag] == tag), None)
    def get_tag(self, xml: dict) -> Optional[str]:
        ''' get value matching '#tag' key
            return None if doesn't exist
        '''
        if xml is None or self.tag not in xml:
            return None
        return xml[self.tag]
    def find_attr(self, xml: dict) -> Optional[str]:
        if xml is None or self.attr not in xml:
            return None
        return xml[self.attr]
    def get_attr(self, xml: dict, attr: str) -> Optional[str]:
        xattr = self.find_attr(xml)
        if xattr is None or attr not in xattr:
            return None
        return xattr[attr]
    def get_text(self, xml: dict) -> Optional[str]:
        if xml is None or self.text not in xml:
            return None
        return xml[self.text]
    

if __name__ == '__main__':
    ii = Path("../xml/a.xml")
    p = pXml2Dict(ii)
    print(f"{p._xml=}")
    print(f"done")
