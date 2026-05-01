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
    
    def traverse_dependency(self, module_name, indent=0):
        b = self.find_bp(module_name)
        if b:
            m = b.find_module(module_name)
            if m:
                if 'depends' in m:
                    b.dump_module(m, indent+4)
                    for d in sorted(m['depends']):
                        self.traverse_dependency(d, indent+8)
                else:
                    # found it
                    print(f"{' '*(indent+4)}==================================================")
                    print(f"{' '*(indent+4)}@@@@@ {module_name}")
        else:
            print(f"{' '*(indent+4)}==================================================")
            print(f"{' '*(indent+4)}can't find {module_name}")
                    
    
    def toXml(self):
        pass
    
    def dump(self, indent=0):
        print(f"==================================================")
        print(f"dump Android.bp in {self.root.as_posix()}")
        print(f"--------------------------------------------------")
        for group in self.groups:
            print(f"group: {group}")
            for bp in self.groups[group]['bps']:
                bp.dump(indent=2)
        print(f"==================================================")


class pAndroidBp(object):
    ignore_module_types = ['soong_config_module_type',
                           'soong_config_string_variable',
                           'license',
                           'ndk_library'
                           ]
    def __init__(self, file, debug=False):
        self.filepath = file
        self.modules = list()
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
            module = {'type':bpm.__type__, 'name':bpm.name, 'depends':set()}
            for prop in ["shared_libs", "static_libs", "deps", "header_libs", "defaults", "java_libs"]:
                if debug:
                    print(f"  property: {prop}")
                value = bpm.__dict__.get(prop)
                if debug:
                    print(f"    value: {value}")
                if isinstance(value, list):
                    xx = self.__flattenlist(value)
                    module['depends'].update(xx)
                    self.depends.update(xx)

            value = bpm.__dict__.get("defaults")
            if isinstance(value, list):
                module['defaults'] = value
            self.modules.append(module)

        for m in self.modules:
            if "defaults" in m:
                for name in m['defaults']:
                    depends = self.get_depends(name)
                    m['depends'].update(depends)
        for m in self.modules:
            if 'depends' in m and len(m['depends']) == 0:
                del(m['depends'])

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
        x = next((x for x in self.modules if x['name'] == module_name), None)
        return x
 
    def get_defaults(self, module_name):
        return next((x['defaults'] for x in self.modules if x['name'] == module_name), None)

    def get_depends(self, module_name):
        x = next((x for x in self.modules if x['name'] == module_name), None)
        if x is not None:
            if "depends" in x:
                return x["depends"]
        return []

    def dump_module(self, module, indent=0):
        print(f"{' '*indent}==================================================")
        print(f"{' '*indent}name: {module['name']} type: {module['type']}")
        if "defaults" in module:
            print(f"{' '*indent}  defaults: {module['defaults']}")
        if "depends" in module:
            print(f"{' '*indent}  depends")
            for d in sorted(module['depends']):
                print(f"{' '*indent}    {d}")
                    
    def dump(self, indent=0):
        print(f"{' '*indent}==================================================")
        print(f"{' '*indent}file: {self.filepath.as_posix()}")
        for m in sorted(self.modules, key=lambda x: x['name']):
            self.dump_module(m, indent+2)
        print(f"{' '*indent}  ==================================================")
        print(f"{' '*indent}  all dependency in module")
        print(f"{' '*indent}    depends")
        for d in sorted(self.depends):
            print(f"{' '*indent}      {d}")
    
if __name__ == '__main__':
    aosp_root = "../../../android-tools/aosp-16.0.0_r2/build"
    aosp_root = "../../../android-tools/aosp-16.0.0_r2/art"
    aosp_root = Path("../../../android-tools/aosp-16.0.0_r2/system")
    aosp_root = Path("../../../android-tools/aosp-16.0.0_r2/")
    aospbp = pAospBp(aosp_root)
    groups = ['build', 'art', 'system']
    [aospbp.add_group(x) for x in groups]
    for group in groups:
        print(f"{group}")
        depends = aospbp.get_group_depends(group)
        for depend in depends:
            g = aospbp.find_group(depend)
            if g and g != group:
                print(f"  {depend:50s} ... {g}")
    
    # aospbp.remove_group("system/core/fastboot")
    # module_name = "fastboot"
    # print(f"find {module_name}")
    # aospbp.traverse_dependency(module_name)
    # aospbp.dump()
    exit(0)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--aosp_root', '-r', required=True, help="aosp source directory")
    parser.add_argument('--debug', '-d', action='store_true', help="print debug info")
    args = parser.parse_args()
    aosp_root = args.aosp_root
    debug = args.debug

    aospbp = pAospBp(aosp_root)
    aospbp.dump()
