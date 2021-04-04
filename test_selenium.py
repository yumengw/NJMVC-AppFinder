from selenium import webdriver

webpage = r"https://www.youtube.com/" # edit me
searchterm = "Hurricane Sandy" # edit me

driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(webpage)

sbox = driver.find_element_by_class_name("txtSearch")
sbox.send_keys(searchterm)

submit = driver.find_element_by_class_name("sbtSearch")
submit.click()
