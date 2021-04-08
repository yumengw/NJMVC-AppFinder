import requests
import csv
import webbrowser
from datetime import datetime
from bs4 import BeautifulSoup

locfile = 'locations.csv'
URL_prefix = 'https://telegov.njportal.com/njmvc/AppointmentWizard/11'
db_host = 'https://telegov.njportal.com/'
non_avail = 'Currently, there are no appointments available at this location.'
for line in csv.DictReader(open(locfile)):

    if int(line['time from home']) > 50: continue
    page = requests.get(URL_prefix + '/' + line['url'])
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())
    if non_avail in str(soup): 
        print(line['Name'] + ' no')
        continue
    else:
        ## find available slots
        timee_list = soup.findAll('a', attrs={'class':'text-primary', 'href':True})
        timee = timee_list[-1]['href'] ## get latest time

        date_string = timee.split('/')[-2]
        time_string = timee.split('/')[-1]
        date_obj = datetime.strptime(date_string + ' ' + time_string, "%Y-%m-%d %H%M")

        if date_obj < datetime(2021, 4, 11): 
            print(line)
            webbrowser.open(db_host + timee)
        else:
            print(line['Name'] + ' earlist ' + str(date_obj.date()))
        #results = soup.find(id='locationsDiv')
        #print(results.prettify())
        #with open("output.html", "w") as file:
        #    file.write(str(soup))
        #break
