
import os 
import time
import sys
import sched
from selenium import webdriver
from selenium.webdriver.common.by import By


scheduler = sched.scheduler(time.time, time.sleep)

CurrentTweets = {}

class Tweet:
    hash = ""
    text = ""
    date = ""

    def __init__(self, hash, text, date):  
        self.hash = hash
        self.text = text 
        self.date = date 


def grabNewTweetsOnSchedule(handle, time):
    scheduler.enter(float(time) * 60.0, 1, grabNewTweets, kwargs={'handle': handle})
    scheduler.run()

def grabInitialTweets(handle):
    driver = setupChromeDriver(handle)
    enumerateTweets(driver)
    driver.quit()


def grabNewTweets(handle):
    driver = setupChromeDriver(handle)
    elements = findTweetElements(driver)
    newTweet = elements[0]
    if saveTweet(newTweet):
        displayTweets()
    driver.quit()
        

def setupChromeDriver(handle):
    url = "https://www.twitter.com/" + handle

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    driver.get(url)

    time.sleep(5)

    return driver


def enumerateTweets(driver):
    elements = findTweetElements(driver)

    if len(elements) >= 5:
        saveTweets(elements, 5)
    elif len(elements) < 5:
        loadMoreTweets(driver, elements)


def findTweetElements(driver):
    return driver.find_elements(By.TAG_NAME, "article")


def loadMoreTweets(driver, elements):
    tweetCount = len(elements)
    saveTweets(elements, tweetCount)

    driver.execute_script('arguments[0].scrollIntoView(true);', elements[len(elements)-1])
    time.sleep(5)

    elements = findTweetElements(driver)
    for e in elements:
        if tweetCount > 4:
            break
        if saveTweet(e):
            tweetCount += 1


def saveTweets(elements, number):
    for i in range(number):
        saveTweet(elements[i])


def saveTweet(element):
    dateElement = element.find_element(By.TAG_NAME, "time")
    dateTimeElement = dateElement.get_property('attributes')[0]
    dateTime = dateTimeElement['value']
    dateHash = hash(dateTime)

    if dateHash not in CurrentTweets:
        CurrentTweets[dateHash] = Tweet(dateHash, element.text, dateTime)
        return True
    return False


def displayTweets():
    os.system('clear')
    for k,v in sorted(CurrentTweets.items(), key=lambda item: item[1].date):
        printTweet(v)


def printTweet(tweet):
    print("Date: {0}\n".format(tweet.date), flush=True)
    print("Text: {0}\n".format(tweet.text), flush=True)
    print("==============================", flush=True)


def main(argv):
    if len(argv) < 1:
        print("not enough args")
        sys.exit(2)
    grabInitialTweets(argv[0])
    displayTweets()

    while True:
        grabNewTweetsOnSchedule(argv[0], argv[1])


if __name__ == "__main__":
    main(sys.argv[1:])