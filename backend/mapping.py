from datetime import datetime
from pendulum import instance


from datetime import date
from datetime import datetime
import pendulum

now = pendulum.now("Europe/Paris")
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
        if 'Erstellt' in new_entry:
            new_entry.__delitem__('Erstellt')           
        if 'Bearbeitet' in new_entry:
            new_entry.__delitem__('Bearbeitet')
        if not '_created' in new_entry:
            new_entry['_created']=now
        result.append(new_entry)

    return result