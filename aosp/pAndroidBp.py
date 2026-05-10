import os,sys
import argparse
from android_bp import BluePrint
from pathlib import Path

class pAospBp(object):
    def __init__(self, aosp_root, debug=False):
        self.root = aosp_root
        self.groups = dict()
        self.bps=list()
        if aosp_root.exists() == False:
            print(f"{aosp_root.as_posix()} is not exit")
            return

        self.add_group('default')
        for root, sub, files in os.walk(aosp_root):
            for file in files:
                if file.endswith(('.bp')) == False:
                    continue
                if file != "Android.bp": #
                    continue
                filepath = Path(root) / Path(file)
                # try:
                #     bp = pAndroidBp(filepath)
                # except Exception as e:
                #     print(f"exception: {filepath.as_posix()}")
                #     continue
                bp = pAndroidBp(filepath, debug)
                self.add(bp)

        # in this time we complete dependency
        for bp in self.bps:
            for m in bp.modules:
                pass
        

    def add(self, bp):
        # classfy group from filepath
        x = next((x for x in self.groups if bp.filepath.as_posix().startswith(str(self.root / x))), None)
        if x is None:
            group = 'default'
        else:
            group = x
        self.groups[group]['bps'].append(bp)

    # {'<group>': {'path':string, 'bps':list()}}
    def add_group(self, group):
        if group not in self.groups:
            self.groups[group] = {'path':group, 'bps':list()}
            x0 = [x for x in self.groups['default']['bps'] if group in x.filepath.as_posix()]
            if x0 is not None:
                self.groups[group]['bps'] = x0
                x1 = [x for x in self.groups['default']['bps'] if group not in x.filepath.as_posix()]
                self.groups['default']['bps'] = x1

    def remove_group(self, group):
        if group == "default":
            return
        if group in self.groups:
            self.groups['default']['bps'].extend(self.groups[group]['bps'])
            del(self.groups[group])

    def get_group(self, group):
        if group in self.groups:
            return self.groups[group]
        return None

    def find_group(self, module_name):
        for group in self.groups:
            for bp in self.groups[group]['bps']:
                m = bp.find_module(module_name)
                if m:
                    return group
        return None
    
    def get_group_depends(self, group):
        depends = set()
        if group in self.groups:
            bps = [x for x in self.groups[group]['bps']]
            if bps is not None:
                dd = [x.depends for x in bps]
                for x in dd:
                    depends.update(x)
        return depends
            
            

    def find_bp(self, module_name):
        for group in self.groups:
            for bp in self.groups[group]['bps']:
                m = bp.find_module(module_name)
                if m:
                    return bp
        return None
    
    def trace_dependency(self, module_name, trace, indent=0):
        bp = self.find_bp(module_name)
        if bp:
            m = bp.find_module(module_name)
            if m:
                if len(m.depends) > 0:
                    print(f"{' '*indent}--------------------------------------------------")
                    print(f"{' '*indent}filepath: {bp.filepath.as_posix()}")
                    m.dump(indent)
                    for d in sorted(m.depends):
                        self.trace_dependency(d, trace, indent+2+4)
                else:
                    # found it
                    print(f"{' '*indent}--------------------------------------------------")
                    print(f"{' '*indent}@@@ {module_name}")
                    x = [x.name if isinstance(x, pAndroidBpM) else x for x in trace]
                    if module_name not in x:
                        trace.append(m)
        else:
            print(f"{' '*indent}--------------------------------------------------")
            print(f"{' '*indent}XXX {module_name}")
            x = [x.name if isinstance(x, pAndroidBpM) else x for x in trace]
            if module_name not in x:
                trace.append(module_name)
    
    def toXml(self):
        pass
    
    def dump(self, indent=0):
        print(f"==================================================")
        print(f"dump Android.bp in {self.root.as_posix()}")
        print(f"--------------------------------------------------")
        for group in self.groups:
            print(f"group: {group}")
            for bp in self.groups[group]['bps']:
                bp.dump(indent+2)
        print(f"==================================================")

class pAndroidBpM(object):
    ''' abstraction `module` in Android.bp
    '''
    def __init__(self, name, module_type):
        self.name = name
        self.type = module_type
        self.defaults = None
        self.depends = set()

    def set_defaults(self, property_default):
        if isinstance(property_default, list):
            self.defaults = property_default

    def add_depends(self, depends):
        self.depends.update(depends)

    def dump(self, indent=0):
        print(f"{' '*indent}==================================================")
        print(f"{' '*indent}name: {self.name} type: {self.type}")
        if self.defaults is not None:
            print(f"{' '*indent}  defaults: {self.defaults}")
        if len(self.depends) > 0:
            print(f"{' '*indent}  depends")
            for depend in sorted(self.depends):
                print(f"{' '*indent}    {depend}")

class pAndroidBp(object):
    ''' abstraction `Android.bp`
    '''
    ignore_module_types = [
        "soong_config_module_type",
        "soong_config_string_variable",
        "license",
        "ndk_library"
        ]
    depends_module_property = [
        "shared_libs",
        "static_libs",
        "deps",
        "header_libs",
        "defaults",
        "java_libs"
        ]
    def __init__(self, file, debug=False):
        self.filepath = file
        self.modules = list() #pAndroidBpM
        self.depends = set()
        try:
            # BluePrint only accept string filepath
            self.bp = BluePrint.from_file(str(self.filepath))
        except Exception as e:
            print(f"exception: {file.as_posix()}")
            return

        if debug:
            print(f"{file}")

        for bpm in self.bp.modules:
            if bpm.name is None:
                continue
            if bpm.__type__ in self.ignore_module_types:
                continue

            if debug:
                print(f"bp module: {bpm.name}")
            
            module = pAndroidBpM(bpm.name, bpm.__type__)
            for prop in self.depends_module_property:
                if debug:
                    print(f"  property: {prop}")

                value = bpm.__dict__.get(prop)

                if debug:
                    print(f"    value: {value}")
                if isinstance(value, list):
                    xx = self.__flattenlist(value)
                    module.add_depends(xx)
                    self.depends.update(xx)

            module.set_defaults(bpm.__dict__.get("defaults"))
            self.modules.append(module)

        # this is done after parsing all aosp bp
        # # update depends module by 'defaults' property
        # for module in self.modules:
        #     if module.defaults is not None:
        #         for name in module.defaults:
        #             depends = self.get_depends(name)
        #             module.add_depends(depends)

    def __flattenlist(self, item):
        x1 = [x for x in item if isinstance(x, list)]
        if len(x1) > 0:
            # checkme:
            # only xx is selected in case of [[xx], yy]
            flattened = [
                x
                for sublist in x1 
                for x in (sublist if isinstance(sublist, list) else [sublist])
            ]
            return flattened
        else:
            return item
                
    def find_module(self, module_name):
        module = next((x for x in self.modules if x.name == module_name), None)
        return module
 
    def get_defaults(self, module_name):
        return next((x.defaults for x in self.modules if x.name == module_name), None)

    def get_depends(self, module_name):
        module = next((x for x in self.modules if x.name == module_name), None)
        if module is not None:
            return module.depends
        return []

    def dump(self, indent=0):
        print(f"{' '*indent}==================================================")
        print(f"{' '*indent}file: {self.filepath.as_posix()}")
        for module in sorted(self.modules, key=lambda x: x.name):
            self.module.dump(indent+2)
        print(f"{' '*indent}  ==================================================")
        print(f"{' '*indent}  all dependency in module")
        print(f"{' '*indent}    depends")
        for depend in sorted(self.depends):
            print(f"{' '*indent}      {depend}")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--aosp_root', '-r', required=True, help="aosp source directory")
    parser.add_argument('--debug', '-d', action='store_true', help="print debug info")
    parser.add_argument('--find', help="find module and return AndroidBp")
    parser.add_argument('--trace', help="trace module dependency")

    args = parser.parse_args()
    
    aosp_root = Path(args.aosp_root)
    debug = args.debug
    find = args.find
    trace = args.trace

    aospbp = pAospBp(aosp_root)
    if find:
        print(f"{find}")
        group = aospbp.find_group(find)
        if group:
            print(f"  group: {group}")
        bp = aospbp.find_bp(find)
        if bp:
            print(f"  filepath: {bp.filepath.as_posix()}")
            m = bp.find_module(find)
            m.dump(2)
        else:
            print(f"  None")
    if trace:
        print(f"{trace}")
        depends=list()
        aospbp.trace_dependency(trace, depends)
        print(f"==================================================")
        print(f"depends")
        print(f"==================================================")
        for depend in depends:
            if isinstance(depend, pAndroidBpM):
                print(f"O: {depend.name}")
            else:
                print(f"X: {depend}")
        
