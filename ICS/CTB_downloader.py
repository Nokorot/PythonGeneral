
def download(url):
    import urllib2
    return urllib2.urlopen(url).read();

#print download("https://www-eng-x.llnl.gov/documents/a_document.txt").read()

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
            print course.full_code
            if course.full_code == code:
                return course
        return None

    def export_as_ics(self, filename):
        from icsFormat import Calender, Event

        


class Timetable_JSON(Timetable):
    def __init__(self, json_file):
        self.json_file = json_file
        self.reader(json_file)
        print len(self.events)

    def reader(self, file):
        import json
        data = json.loads(file)

        for item in data:
            event = Event(item)
            self.events.append(event)

            '''course = self.course_by_code(event.course[0]['full_code'])
            print type(course)
            print str(course)
            if course == None:
                course = Course(event.course[0])
                self.courses.append(course)
            else:
                course.data.update(event.course[0])
            course.events.append(event)
            event.course = course'''


url_base = "https://browser.ted.is.ed.ac.uk/generate"
url_extsn = '?courses%5B%5D=MATH10076_SV1_SEM1&courses%5B%5D=PHYS11019_SV1_SEM1&period=SEM1&format=json'
url = url_base + url_extsn

Timetable_JSON(download(url))
