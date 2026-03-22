import sys,os
import re

class pNinja(object):
    def __init__(self, ninja):
        self.builddir = "/out"
        self.variables = {}
        self.rules = {}
        self.builds = []

        with open(ninja) as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].rstrip()

            # Skip comments and blank lines
            if not line or line.startswith('#'):
                i += 1
                continue

            # Variable assignment: name = value
            var_match = re.match(r'^(\w+)\s*=\s*(.*)$', line)
            if var_match:
                self.variables[var_match.group(1)] = var_match.group(2).strip()
                i += 1
                continue

            # Rule block: rule rulename
            rule_match = re.match(r'^rule\s+(\w+)', line)
            if rule_match:
                rule_name = rule_match.group(1)
                self.rules[rule_name] = {}
                i += 1
                while i < len(lines) and lines[i].startswith('  '):
                    kv = re.match(r'\s+(\w+)\s*=\s*(.*)', lines[i])
                    if kv:
                        self.rules[rule_name][kv.group(1)] = kv.group(2).strip()
                    i += 1
                continue

            # Build edge: build output: rule input
            build_match = re.match(r'^build\s+(.+?)\s*:\s*(\w+)\s*(.*)', line)
            if build_match:
                self.builds.append({
                    "target": build_match.group(1).split(),
                    "rule":    build_match.group(2),
                    "deps":  build_match.group(3).split(),
                })
                i += 1
                continue
            i += 1

        if "builddir" in self.variables:
            self.builddir = self.variables['builddir']

    def variables(self):
        return self.variables
    def rules(self):
        return self.rules
    def builds(self):
        return self.builds
    def print_target(self, target, indent=0):
        xx = next((x for x in self.builds if x['target'][0] == target), None)
        if xx is None:
            return
        target_name = xx['target'][0]
        target_name = target_name.replace(self.builddir, '/out')
        print(f"{indent*' '}{target_name}")
        for dep in xx['deps']:
            self.print_target(dep, indent+2)

if __name__=='__main__':
    i = 'build.ninja'
    i = 'build-sdk.ninja.windows'
    i = 'build-sdk.ninja.arm64'
    
    target = 'fastboot-host'
    pninja = pNinja(i)
    pninja.print_target(target)
