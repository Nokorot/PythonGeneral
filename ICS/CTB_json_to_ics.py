import datetime

def get_week_o_date(year):
    month_number = {
        'January':	'01',
        'February':	'02',
        'March':	'03',
        'April':   	'04',
        'May':      '05',
        'June':	    '06',
        'July':	    '07',
        'August':	'08',
        'September':'09',
        'October':	'10',
        'November':	'11',
        'December':	'12'
    }

    url = 'https://www.ed.ac.uk/semester-dates/20%i' % year
    data = download(url)
    refrence_code = '''<h2>Semester 1</h2>

<table align="left" class="table">
	<caption>'''

    a = data.find(refrence_code)+len(refrence_code)
    b = data[a:].find(' - ')
    d,m = data[a:a+b].split(' ')
    m = month_number[m]
    print d,m

def download(url):
    import urllib2
    return urllib2.urlopen(url).read();

def week_to_date(year, week, day=1):
    return datetime.datetime.strptime('%s-%s-%s'%(year,week,day), '%Y-%W-%w')

ics_header = '''BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:CTB_Timetable
X-WR-TIMEZONE:Europe/London
'''
ics_fotter = '''END:VCALENDAR'''

def CTB_json_to_ics(year):
    in_url = 'https://browser.ted.is.ed.ac.uk/generate?courses%5B%5D=MATH10076_SV1_SEM1&courses%5B%5D=PHYS11019_SV1_SEM1&period=SEM1&format=json'
    out_file = 'CTB_out.ics'

    week_pattern_first = 30

    with open(out_file, 'w') as f:
        import json
        data = json.loads(download(in_url))

        f.write(ics_header)
        for event in data:

            w_parr = event['week_pattern']
            #print [i for (i,k) in zip(range(len(w_parr)),w_parr) if k == '1']
            for w in [i for (i,k) in zip(range(len(w_parr)),w_parr) if k == '1']:

                f.write('BEGIN:VEVENT\n')

                #w = event['week_pattern'].find('1')
                date = week_to_date(year, w + week_pattern_first, event['day']+1).strftime('%Y%m%d')

                time = event['start']
                start_time = format(event['start']/2, '02') + format(event['start']%2*30, '02')
                end_time = format(event['end']/2, '02') + format(event['end']%2*30, '02')

                f.write('DTSTART:%s\n' % (date+'T'+start_time+'00Z'))
                f.write('DTEND:%s\n' % (date+'T'+end_time+'00Z'))

                f.write('SUMMARY:%s\n' % event['name'])

                loc = event['location'][0]
                f.write('LOCATION:r:%s  \tb:%s  \tc:%s\n' % (loc['room'], loc['building'], loc['campus']))

                f.write('END:VEVENT\n')

        f.write(ics_fotter)


#get_week_o_date(1920)
#print week_to_date(2018, 38)
CTB_json_to_ics(2018)
