import datetime
import json, urllib2

import random

# Currently not in use
# def get_week_o_date(year):
#     month_number = {
#         'January':      '01',
#         'February':     '02',
#         'March':        '03',
#         'April':        '04',
#         'May':          '05',
#         'June':	        '06',
#         'July':	        '07',
#         'August':       '08',
#         'September':    '09',
#         'October':      '10',
#         'November':     '11',
#         'December':     '12'
#     }
# 
#     url = 'https://www.ed.ac.uk/semester-dates/20%i' % year
#     data = urllib2.urlopen(url).read()
#     refrence_code = '''<h2>Semester 1</h2>
# 
# <table align="left" class="table">
# 	<caption>'''
# 
#     a = data.find(refrence_code)+len(refrence_code)
#     b = data[a:].find(' - ')
#     d,m = data[a:a+b].split(' ')
#     m = month_number[m]
#     print d,m

def week_to_date(year, week, day=1):
    return datetime.datetime.strptime('%s-%s-%s'%(year,week,day), '%Y-%W-%w')


def w_ics_header(f, name, **kws):
    header = {
        "X-WR-CALNAME":     name,
        "VERSION":          "2.0",
        "PRODID":           "FROM-CTB",
        "CALSCALE":         "GREGORIAN",
        "METHOD":           "PUBLISH",
        "X-WR-TIMEZONE":    "Europe/London"
    }
    header.update(kws)

    f.write("BEGIN:VCALENDAR\n")
    for (k,v) in header.iteritems():
        f.write("%s:%s\n" % (k, v))

def w_ics_fotter(f):
    f.write("END:VCALENDAR")

def w_ics_event(f, event):
    f.write('BEGIN:VEVENT\n')

    for (k,v) in event.iteritems():
         f.write(("%s:%s\n" % (k, v)).encode('utf8'))
    f.write('END:VEVENT\n')


## TODO export csv instead

def ctb_download(url):
    data = urllib2.urlopen(url).read()
    return json.loads(data);

def r_ctb_event(year, week, event):
    date = week_to_date(year, week, event['day']+1)\
            .strftime('%Y%m%d')
            # .strftime('%d/%m/%Y')

    def time_format(x):
        #return "%s:%s" % (format(x,'02'), format(x%2*30,'02') ) 
        return "%s%s" % (format(x/2,'02'), format(x%2*30,'02') ) 

    start_time = time_format(event['start'])
    end_time = time_format(event['end'])

    loc = event['location'][0]
    #return {
    #    "Start time": ,
    #    "DTEND":    (date+'T'+end_time+'00Z'),
    #    "SUMMARY":  event['name'],
    #    "LOCATION": "r:%s  \tb:%s  \tc:%s"\
    #            % (loc['room'], loc['building'], loc['campus'])
    #}
    return {
        "DTSTART":  (date+'T'+start_time+'00Z'),
        "DTEND":    (date+'T'+end_time+'00Z'),
        "SUMMARY":  event['name'],
        "LOCATION": "r:%s  \tb:%s  \tc:%s"\
                % (loc['room'], loc['building'], loc['campus'])
    }

#def CTB_json_to_csv(url, year, outfile):
#    week_offset = -23
#
#    data = ctb_download(url)
#
#    f = open(outfile, 'w')
#
#    colms = { 
#            "Subject": "SUMMARY",
#            ""
#    }
#
#    f.write()
#
#    w_ics_header(f, "CTB_Timetable")
#    for event in data:
#        for (w,k) in enumerate(event['week_pattern']):
#            if k != '1': continue
#            ev = r_ctb_event(year, w + week_offset, event)
#            w_ics_event(f, ev)
#    w_ics_fotter(f)
#    f.close()

def CTB_json_to_ics(url, year, outfile):
    week_offset = -23

    data = ctb_download(url)

    f = open(outfile, 'w')
    w_ics_header(f, "CTB_Timetable")
    for event in data:
        for (w,k) in enumerate(event['week_pattern']):
            if k != '1': continue
            ev = r_ctb_event(year, w + week_offset, event)
            w_ics_event(f, ev)
    w_ics_fotter(f)
    f.close()

def genurl(courses, period):
    return "https://browser.ted.is.ed.ac.uk/generate?" \
            + 'courses=' + ','.join(courses) + '&' \
            + 'period=' + period + '&' \
            + 'format=json'

if __name__ == "__main__":
    period = "SEM2" 
    courses = [
        "MATH11120_SV1_SEM2", # Algebraic Geometry
        # "MATH11135_SV1_SEM2", # Functional Analysis
        "MATH10080_SV1_SEM2", # Galois Theory
        "PGPH11099_SV1_SEM2", # Gauge Theories in Particle Physics
        "MATH11138_SV1_SEM2", # Geometry of General Relativity
        "MATH11137_SV1_SEM2", # Nonlinear Schrodinger Equations
        "MATH11201_SV1_SEM2", # Topics in Mathematical Physics
        "MATH11144_SV1_SEM2"  # Topics in Ring and Representation Theory
    ]

    url = genurl(courses, period)
    CTB_json_to_ics(url, 2020, "out.ics")
