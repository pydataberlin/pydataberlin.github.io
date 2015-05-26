import json
import datetime
import pytz
from lxml import etree
import itertools

other_events = [
        {"bio":"",
         "twitter": "",
         "organisation": "",
         "name": "",
         "firstname": "",
         "title": "Lightning Talks",
         "abstract": "",
         "linkedin": "",
         "duration": "1:00:00",
         "location": "Innospace",
         "time": "4:30:00 PM",
         "date": "5/29/2015",
         "type": "talk",
         "id": "lightning_0" },
        {"bio": "",
         "twitter": "",
         "organisation": "",
         "name": "",
         "firstname": "",
         "title": "Panel Discussion",
         "abstract": "",
         "linkedin": "",
         "duration": "0:40:00",
         "location": "Innospace",
         "time": "11:50:00 AM",
         "date": "5/30/2015",
         "type": "talk",
         "id": "panel_0"}]

raw_talks = None
with open('../_data/keynotes.json', 'r') as f:
    raw_talks = json.loads(f.read())

raw_talks = raw_talks + other_events

def group_talks():
    g = itertools.groupby(raw_talks, lambda t: t['title'])
    talks = []
    for k, v in g:
        t = {}
        values = list(v)
        t['title'] = k
        t['date']  = values[0]['date']
        t['time']  = values[0]['time']

        date = datetime.datetime.strptime(t['date'],'%m/%d/%Y').date()
        time = datetime.datetime.strptime(t['time'], '%I:%M:%S %p')
        dt = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=time.hour,
                minute=time.minute, second=time.second)
        local_dt = pytz.timezone('Europe/Berlin').localize(dt)

        t['isodate'] = date.isoformat()
        t['room'] = values[0]['location']
        t['datetime'] = local_dt
        t['duration'] = values[0]['duration']
        t['persons'] = map(lambda e: e['firstname']+u' '+e['name'], values)
        t['type'] = values[0]['type']
        t['abstract'] = values[0]['abstract']
        t['id'] = values[0]['id']
        talks.append(t)
    return talks

talks = group_talks()

def days():
    days = list(set(map(lambda t:t['isodate'], talks)))
    days.sort()
    return days

def rooms(day):
    rooms = list(set([t['room'] for t in talks if t['isodate']==day]))
    rooms.sort()
    return rooms

def talk_parameters(day, room):
    talk_parameters = [t for t in talks if t['isodate']==day and t['room']==room]
    talk_parameters = sorted(talk_parameters, key=lambda t: t['datetime'])
    return talk_parameters

def events(root):
    for day in days():
        day_item = etree.SubElement(root, 'day', date=day)
        for room in rooms(day):
            room_item = etree.SubElement(day_item, 'room', name=room)
            for talk in talk_parameters(day, room):

                event = etree.SubElement(room_item, 'event', attrib={'id':
                                                                     talk['id']})

                date = etree.SubElement(event, 'date')
                date.text = talk['datetime'].isoformat()

                start = etree.SubElement(event, 'start')
                start.text = talk['datetime'].strftime('%H:%M')

                duration = etree.SubElement(event, 'duration')
                duration.text = talk['duration']

                room_entry = etree.SubElement(event, 'room')
                room_entry.text = room

                title = etree.SubElement(event, 'title')
                title.text = talk['title']

                type = etree.SubElement(event, 'type')
                type.text = talk['type']

                language = etree.SubElement(event, 'language')
                language.text = u'en'

                abstract = etree.SubElement(event, 'abstract')
                abstract.text = talk['abstract']

                persons = etree.SubElement(event, 'persons')
                for p in talk['persons']:
                    person = etree.SubElement(persons, 'person')
                    person.text = p


# Start xml
schedule = etree.Element("schedule")

# General info
conference = etree.SubElement(schedule, "conference")
conference_title = etree.SubElement(conference, "title")
conference_title.text = u"PyData Berlin 2015"
conference_start = etree.SubElement(conference, "start")
conference_start.text = datetime.date(year=2015, month=5, day=29).isoformat()
conference_end = etree.SubElement(conference, "end")
conference_end.text = datetime.date(year=2015, month=5, day=30).isoformat()
conference_days = etree.SubElement(conference, "days")
conference_days.text = u"2"

# Add events
events(schedule)

xml = etree.tostring(schedule, pretty_print=True, xml_declaration=True, encoding="utf-8")
with open('pydata_berlin_voc.xml', 'w') as f:
    f.write(xml)
