import os
from operator import *

ll = [{'grade':'A'},
      {'grade':'B'},
      {'grade':'D'},
      {'grade':'C'}]
print(ll)
print(sorted(ll, key=lambda x:x['grade'], reverse=True))
print(sorted(ll, key=itemgetter('grade'), reverse=True))
