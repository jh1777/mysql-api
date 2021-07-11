from datetime import datetime
from pendulum import instance


from datetime import date
from datetime import datetime
def map(array):
    if array is None: return None
    result = []

    for entry in array:
        new_entry = {}
        for k, v in list(entry.items()):
            if k == "Erstellt":
                new_entry['_created']=v
            if k == "Bearbeitet":
                new_entry['_modified']=v
            if isinstance(v, date) and not isinstance(v, datetime):
                new_entry[k]= datetime.combine(v, datetime.min.time())
            else:
                new_entry[k]=v 
        new_entry.__delitem__('Erstellt')           
        new_entry.__delitem__('Bearbeitet')           
        result.append(new_entry)

    return result