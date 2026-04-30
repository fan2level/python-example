import os,sys
import argparse
from android_bp import BluePrint

class pAospBp(object):
    def __init__(self, aosp_root):
        self.root = aosp_root
        self.bps=list()
        if os.path.exists(aosp_root) == False:
            print(f"{aosp_root} is not exit")
            return
        for root, sub, files in os.walk(aosp_root):
            for file in files:
                if file.endswith(('.bp')) == False:
                    continue
                if file != "Android.bp":
                    continue
                filepath = os.path.join(root, file)
                # try:
                #     bp = pAndroidBp(filepath)
                # except Exception as e:
                #     print(f"exception: {root}/{file}")
                #     continue
                bp = pAndroidBp(filepath)
                if len(bp.modules) > 0:
                    self.bps.append(bp)

    def find_bp(self, module_name):
        for bp in self.bps:
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
        print(f"dump Android.bp in {self.root}")
        print(f"--------------------------------------------------")
        for bp in sorted(self.bps, key=lambda x: x.file):
            bp.dump(indent=2)
        print(f"==================================================")


class pAndroidBp(object):
    ignore_module_types = ['soong_config_module_type',
                           'soong_config_string_variable',
                           'license',
                           'ndk_library'
                           ]
    def __init__(self, file):
        self.file = file
        self.modules = list()
        self.depends = set()
        try:
            self.bp = BluePrint.from_file(self.file)
        except Exception as e:
            print(f"exception: {file}")
            return

        for bpm in self.bp.modules:
            if bpm.name is None:
                continue
            if bpm.__type__ in self.ignore_module_types:
                continue

            module = {'type':bpm.__type__, 'name':bpm.name, 'depends':set()}
            for prop in ["shared_libs", "static_libs", "deps", "header_libs", "defaults", "java_libs"]:
                value = bpm.__dict__.get(prop)
                if isinstance(value, list):
                    # in case of value have sublist like [[xxx], yyy]
                    flattened = [
                        x
                        for sublist in value 
                        for x in (sublist if isinstance(sublist, list) else [sublist])
                    ]
                    module['depends'].update(flattened)
                    self.depends.update(flattened)

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
        print(f"{' '*indent}file: {self.file}")
        for m in sorted(self.modules, key=lambda x: x['name']):
            self.dump_module(m, indent+2)
        print(f"{' '*indent}  ==================================================")
        print(f"{' '*indent}  all dependency in module")
        print(f"{' '*indent}    depends")
        for d in sorted(self.depends):
            print(f"{' '*indent}      {d}")
    
if __name__ == '__main__':
    # aosp_root = "../../../android-tools/aosp-16.0.0_r2/system"
    # aospbp = pAospBp(aosp_root)
    # module_name = "fastboot"
    # print(f"find {module_name}")
    # aospbp.traverse_dependency(module_name)
    # exit(0)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--aosp_root', '-r', required=True, help="aosp source directory")
    parser.add_argument('--debug', '-d', action='store_true', help="print debug info")
    args = parser.parse_args()
    aosp_root = args.aosp_root
    debug = args.debug

    aospbp = pAospBp(aosp_root)
    aospbp.dump()
