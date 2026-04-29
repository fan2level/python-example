# -*-coding:utf-8-*

import os
from pathlib import Path
from xml.etree.ElementTree import *
import random

class pManifest(object):
    def __init__(self, manifest):
        self.__file = manifest
        self.__tree = parse(self.__file)
        self.__root = self.__tree.getroot()
        self.remote = self.__root.find('remote')
        self.default= self.__root.find('default')
        self.superproject = self.__root.find('superproject')
        self.contactinfo = self.__root.find('contactinfo')

    def projects(self):
        return [x for x in self.__root.findall('project')+self.__root.findall('remove-project')]

    def groups(self):
        return {x.get('groups') for x in self.projects() if 'groups' in x.attrib}

    def project(self, path):
        x = next((x for x in self.projects() if x.get('path') == path), None)
        return x

    def add(self, project):
        x = next((x for x in self.projects() if x.get('path') == project.get('path')), None)
        if x is None:
            self.__root.append(project)
        
    def delete(self, project):
        x = next((x for x in self.projects() if x.get('path') == project.get('path')), None)
        if x is not None:
            self.__root.remove(x)

    def write(self):
        if self.__file.exists():
            self.__tree.write(self.__file, encoding='utf-8', xml_declaration=True)
        
    def merge(self, other):
        for p in other.projects():
            if p.tag == 'project':
                x = next((x for x in self.projects() if x.get('path') == p.get('path')), None)
                if x is None:
                    self.add(p)
            elif p.tag == 'remove-project':
                x = next((x for x in self.projects() if x.get('path') == p.get('path')), None)
                if x is not None:
                    self.delete(x)
        return self

    def projects_byGroup(self, group):
        x = [x for x in self.projects() if group == x.get('groups')]
        return x

    def dump_project(self, elem):
        dump = ""
        if elem is not None:
            dump= f'''<{elem.tag} path="{elem.get('path')}"'''
        return dump
            
    def dump(self, groups=False):
        if self.superproject and "revision" in self.superproject.attrib:
            print(f"revision: {self.superproject.get('revision')}")
        print(f"groups: {len(self.groups())}")
        if groups:
            for g in sorted(self.groups()):
                print(f"  {g}")
                for p in self.projects_byGroup(g):
                    print(f"    {p.get('name')}")
        print(f"projects: {len(self.projects())}")
        for p in sorted(self.projects(), key=lambda x: x.get('path')):
            print(f'  {self.dump_project(p)}/>')

def run(project, debug=False):
    if debug:
        print(f"run {project}")
    success = random.randrange(0,2)
    return success
            
if __name__ == '__main__':
    i = Path('madatory.xml')
    m0 = pManifest(i)
    # m0.dump()
    i = Path('default.xml')
    m1 = pManifest(i)
    # m1.dump()
    i = Path('resize.xml')
    m2 = pManifest(i)
    # m2.dump()

    m3 = m1.merge(m0).merge(m2)
    print(f"##################################################")
    print(f"projects: {len(m3.projects())}")
    print(f"##################################################")
    for p in m3.projects():
        if run(p.get('path')):
            p.tag="remove-project"
            m2.add(p)
    m2.dump()
    # m2.write()
    
    
