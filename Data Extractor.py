from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import traceback, datetime, winsound, time, sys

def getCourseList():
    mylist = ["2021 Aptitude (Verbal)", "2021 Reasoning & Quants", "2021 Data Structures and Algorithms",
    "2021_Java for Beginners", "2021 Python for Noobs", "2020 Weekly Coding Challenge"]
    return mylist
    
def isNetworkSlow():
    return False

def getState():
    f = open("state.txt", "r")
    a = int(f.read()) + 1
    b = a + 1000000
    f.close()
    return a, b

def writeState(i):
    f = open("state.txt", "w")
    f.write(str(i))
    print(str(i))
    f.close()

def writeFile(driver, link, item, course):
    f = open(str(item + '.txt'), "a")
    f.write(course + "\n")
    testElem = driver.find_element_by_xpath("/html/body/content-root/div/bd-header/div/div/div[2]/div[2]/div[2]")
    test = str(testElem.get_attribute("innerHTML").strip())
    f.write(test + "\n")
    f.write(link + "\n\n")
    f.close()

try:
    seconds = 5
    if isNetworkSlow():
        seconds+= 2
    
    print("Network Slow : " + str(isNetworkSlow()))
    
    driver = webdriver.Firefox()
    driver.get("https://dummyurl.com/login")

    time.sleep(seconds+1)

    username = driver.find_element_by_name("email")
    username.clear()
    username.send_keys("dummyemail@dummy.com")
    
    driver.find_element_by_id("lgnBtn").click()
    
    time.sleep(seconds)

    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys("dummypassword123")
    
    time.sleep(seconds)
    
    driver.find_element_by_id("lgnBtn0").click()

    time.sleep(seconds+4)
    
    print("Login Done")

    mylist = getCourseList()
    
    for item in mylist:
        f = open(str(item + '.txt'), "a")
        f.close()

    f = open("Demo.txt", "a")
    f.close()
        
    a, b = getState()

    for i in range(a,b):
        link = "https://dummyurl.com/result?id=" + str(i)
        driver.get(link)
        courseExists = False
        
        time.sleep(seconds+1)

        elem = driver.find_elements_by_xpath("/html/body/content-root/div/div/bd-header/div/div/div[2]/div[3]/div[2]")
        
        if len(elem) > 0:
            courseElem = elem[0]
            course = str(courseElem.get_attribute("innerHTML").strip())
            for item in mylist:
                index = course.find(item)
                if index!=-1:
                    writeFile(driver, link, item, course)
                    courseExists = True
                    break
            if not courseExists:
                writeFile(driver, link, "Demo", course)
                    
        writeState(i)
        
except Exception as e:
    traceback.print_exc(file = open("logs.txt","a"))
    f = open("logs.txt", "a")
    f.write("TimeStamp : " + str(datetime.datetime.now()) + "\n")
    f.write("End of Exception.\n\n")
    f.close()
    winsound.Beep(2500, 2000)
    sys.exit()
