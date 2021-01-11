
def download(url):
    import urllib2
    return urllib2.urlopen(url).read();

def CTB_url_client():
    def __init__(self, url):
        self.url = url

class Event():
    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        if self.data.has_key(key):
            return self.data[key]
        return None

    def __getattr__(self, name):
        return self[name]

class Course():
    events = []

    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        if self.data.has_key(key):
            return self.data[key]
        return None

class Timetable():
    courses = []
    events = []

    def course_by_code(self, code):
        for course in self.courses:
            print(course.full_code)
            if course.full_code == code:
                return course
        return None

    def export_as_ics(self, filename):
        from icsFormat import Calender, Event

class Timetable_JSON(Timetable):
    def __init__(self, json_file):
        self.json_file = json_file
        self.reader(json_file)
        print(len(self.events))

    def reader(self, file):
        import json
        data = json.loads(file)

        for item in data:
            event = Event(item)
            self.events.append(event)

            '''course = self.course_by_code(event.course[0]['full_code'])
            print(type(course))
            print(str(course))
            if course == None:
                course = Course(event.course[0])
                self.courses.append(course)
            else:
                course.data.update(event.course[0])
            course.events.append(event)
            event.course = course'''


url_base = "https://browser.ted.is.ed.ac.uk/generate?"
courses = [
  # "MATH11120_SV1_SEM2",
  # "MATH11135_SV1_SEM2",
  # "MATH10080_SV1_SEM2",
  # "PGPH11099_SV1_SEM2",
  # "MATH11138_SV1_SEM2",
  # "MATH11137_SV1_SEM2",
  # "MATH11201_SV1_SEM2",
  "MATH11144_SV1_SEM2"
]
period = "SEM2" 

url = url_base  \
        + 'courses=' + ','.join(courses) + '&'\
        + 'period=' + period + '&'\
        + 'format=json'

from pprint import pprint
import json
data = json.loads(download(url))

pprint(data[0])

ev = {
    'DTSTART':
    'DTEND':
    'SUMMARY': 
    ''
}
    








# Timetable_JSON(download(url))
