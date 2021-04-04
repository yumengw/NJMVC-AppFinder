import mechanize

#url = "https://telegov.njportal.com/njmvc/AppointmentWizard/11/104/2021-06-02/1420"
url = "http://duckduckgo.com/html"

br = mechanize.Browser()
br.set_handle_robots(False) # ignore robots
br.open(url)
br.select_form(name="x")
br["q"] = "python"
res = br.submit()
content = res.read()
with open("mechanize_results.html", "w") as f:
    f.write(str(content))
