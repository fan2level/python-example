from pathlib import Path
from pAndroidBp import pAospBp, pAndroidBp

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
