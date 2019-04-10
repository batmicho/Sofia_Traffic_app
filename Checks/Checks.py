import json

class Checks:
    allstopsid = None

    #all_stop_ids = open('busstops.json')

    def __init__(self, allstopsid):
        self.allstopsid = allstopsid

    def validids(self, stopid):

        all_busstops_ids = open(self.allstopsid)
        stops_ids_json = json.load(all_busstops_ids)
        for all_stopids in stops_ids_json:
            if stopid == all_stopids['c']:
                newStop = stopid

        return newStop
