import requests
import csv
import webbrowser
from datetime import datetime
from bs4 import BeautifulSoup

locfile = 'locations.csv'
URL_prefix = 'https://telegov.njportal.com/njmvc/AppointmentWizard/11'

non_avail = 'Currently, there are no appointments available at this location.'
for line in csv.DictReader(open(locfile)):
    if int(line['time from home']) > 60: continue
    page = requests.get(URL_prefix + '/' + line['url'])
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())
    if non_avail in str(soup): 
        print(line['Name'] + ' no')
        continue
    else:
        ## find date
        datee = soup.findAll('label', attrs={'class':'control-label'})[-1].text
        date_string = ' '.join(datee.split()[-3:])

        timee_list = soup.findAll('a', attrs={'style':'text-decoration:none !important;'})
        if len(timee_list) < 1: continue
        timee = timee_list[-1].text ## get latest time
        time_string = ' '.join(timee.split()[:-1])

        date_obj = datetime.strptime(date_string + time_string, "%B %d, %Y:%I:%M %p")

        if date_obj < datetime(2021, 5, 2): 
            print(line)
            webbrowser.open(URL_prefix + '/' + line['url'] + '/' + str(date_obj.strftime("%Y-%m-%d/%H%M")))
        else:
            print(line['Name'] + ' earlist ' + str(date_obj.date()))
        #results = soup.find(id='locationsDiv')
        #print(results.prettify())
        #with open("output.html", "w") as file:
        #    file.write(str(soup))
        #break
