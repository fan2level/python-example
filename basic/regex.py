import re

str=""" 
"my name is daniel"  "mobile 8531111453733"[[[[[[--"i like pandas"
"location chennai"! -asfas"aadhaar du2mmy8969769##69869" 
@4343453 "pincode 642002""@mango,@apple,
@berry"

BA_DEF_DEF_  "FieldType" "";
BA_ "GenMsgCycleTime" BO_ 100 1000;
BA_ "GenMsgCycleTime" BO_ 500 100;
BA_ "GenMsgCycleTime" BO_ 101 100;
BA_ "GenMsgCycleTime" BO_ 400 100;
BA_ "GenMsgCycleTime" BO_ 200 100;
BA_ "FieldType" SG_ 100 DRIVER_HEARTBEAT_cmd "DRIVER_HEARTBEAT_cmd; abdcd";
BA_ "FieldType" SG_ 500 IO_DEBUG_test_enum "IO_DEBUG_test_enum";
"""

for m in re.findall(r'BA_\s+(["](.*?)["])\s+(.*?);', str, re.M|re.S):
    print(m)

# for m in re.findall(r'["](.*?)["]',str, re.M|re.S):
#     print(f'<<{m}>>')
#     print()
