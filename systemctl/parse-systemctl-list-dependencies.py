import sys
import re
from pprint import pprint
import json

p1=re.compile(r'.*\|-(?P<unit>.*)')
p2=re.compile(r'.*\`(?P<unit>.*)')
p3=re.compile(r'( \||  | `)')

def parse_list_dependencies(filepath):
    units = list()
    with open (filepath) as f:
        lines = f.readlines()
        unit_base = {"name": lines[0].strip(), "depth": 0, "down": list(), "up": None}
        units.append(unit_base)

        for line in lines[1:]:
            line = line.strip()
            c = re.findall(p3, line)
            if c:
                depth_c = len(c)

            unit = dict()
            unit["depth"] = depth_c
            m = re.search(p1, line)
            if m:
                unit['name'] = m.group('unit')
            else:
                m = re.search(p2, line)
                if m:
                    unit['name'] = m.group('unit')

            if 'name' not in unit:
                raise Exception("parsing error")

            units.append(unit)
    return units

def print_units(units, indent=0, name=None):
    for unit in units:
        print(f"{' '*indent}{unit}")
        if unit["name"] == name:
            break
    print()

def toJson(units, output="a.json"):
    with open(output, "w", encoding="utf-8") as f:
        json.dump(units, f, indent=2)
    
if __name__ == '__main__':
    finput = 'a.txt'

    units = parse_list_dependencies(finput)
    print(f"unit count: {len(units)}")

    unit_b = units[0]
    # print_units(units)
    for unit in units[1:]:
        try:
            # down level
            if unit["depth"] > unit_b["depth"]:
                if "down" not in unit_b:
                    unit_b["down"] = list()
                unit_b["down"].append(unit["name"])
                unit["up"] = unit_b["name"]
            # level same
            elif unit["depth"] == unit_b["depth"]:
                xx = next((x for x in units if x["name"] == unit_b["up"]), None)
                if xx:
                    xx["down"].append(unit["name"])
                    unit["up"] = unit_b["up"]
                else:
                    print(f"mismatch: {unit_b['name']}/{unit_b['up']}")
            # level up
            else:
                depth_b_count = unit_b["depth"]
                depth_count = unit["depth"]
                unit_b_temp = unit_b
                for count in range(depth_count, depth_b_count):
                    xx = next((x for x in units if x["name"] == unit_b_temp["up"]), None)
                    if xx:
                        unit_b_temp = xx
                        unit["up"] = xx["up"]
        except Exception as e:
            print(f"exception: {e}")
            print(f"  {unit_b}")
            print_units(units, 4, unit["name"])

        unit_b = unit

    # pprint(units)
    toJson(units)
