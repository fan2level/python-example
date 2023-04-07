
import os, sys
import argparse
from pathlib import Path
import cantools

# https://cantools.readthedocs.io/en/latest/
class pDBC(object):
    def __init__(self, path):
        try:
            self.__candb = cantools.database.load_file(path)
            self.__path = path
        except Exception as e:
            print(e)
            return

        self.__db = dict()
        self._load()

    def _load(self):
        db = self.__candb
        self.__db['nodes'] = [x.name for x in db.nodes]
        self.__db['messages'] = {x.name:{} for x in db.messages}
        for m in db.messages:
            self.__db['messages'][m.name]['senders'] = [x for x in m.senders]
            if m.receivers:
                self.__db['messages'][m.name]['receivers'] = [x for x in m.receivers]

    @property
    def db(self):
        return self.__db

    @property
    def path(self):
        return self.__path
                
    def toXml(self):
        pass

    def toPuml(self):
        db = self.__db
        model = "MODEL"
        ecu = None
        name = "CAN"
        with open(self.__path.with_suffix('.puml'), 'w', encoding='utf-8') as f:
            f.write("@startuml\n")
            f.write("\n")
            f.write("nwdiag {\n")
            f.write("  title {0} CAN Topology\n".format(model))
            f.write("  network {0} {{\n".format(name))
            senders = set()
            for name in db['messages'].keys():
                [senders.add(x) for x in db['messages'][name]['senders']]
            for sender in senders:
                f.write("    {0}\n".format(sender))
            f.write("  }\n")
            f.write("}\n")
            f.write("\n")
            f.write("@enduml\n")
            pass

if __name__ == '__main__':
    
    dd = Path('dbc')
    ii = Path('abs.dbc')
    # ii = Path('multiple_senders.dbc')
    
    pdbc = pDBC(dd/ii)
    db = pdbc.db
    print("nodes: {0}".format(db['nodes']))
    senders = set([])
    for name in db['messages'].keys():
        # message_name = name
        sender = db['messages'][name]['senders']
        [senders.add(x) for x in sender]
        # receiver = db['messages'][name]['receivers']

    print("senders: {0}".format(senders))

    pdbc.toPuml()
    
    print('done')

