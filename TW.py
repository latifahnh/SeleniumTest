import csv
import os
import re
import time
import unicodedata as ud
from model import Connection
from datetime import datetime
from typing import Match

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#if os.path.exists('/home/tsel-ai/deploy/api/public/crawl/socmed'):
    #os.makedirs('/home/tsel-ai/deploy/api/public/crawl/socmed')
os.path.exists('/home/lat/jensel/images/TW')

db = Connection()
connection = db.connect()

options = Options()
options.add_experimental_option("prefs", {"intl.accept_languaages": "en"})
options.add_argument("--lang=en")
options.add_argument("--headless")
options.add_argument('--no-sandbox')

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")

driver = webdriver.Chrome('/home/lat/chromedriver', chrome_options=options)
time.sleep(5)
driver.get('https:/twitter.com/i/flow/login')
time.sleep(5)

username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='text']")))
username.clear()
username.send_keys("@testingscrappi3")
time.sleep(5)

try:
    username.send_keys(Keys.RETURN)
    stsLogin = 1
except:
    stsLogin = 0
    pass

time.sleep(5)
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
password.clear()
password.send_keys("Password123!")
time.sleep(5)

try:
    password.send_keys(Keys.RETURN)
except:
    pass

listData    = []
listThread  = []
listTweet   = []
match       = False
scrolldow_temp = driver.execute_script("window.scrollTo(0,  window.scrollY + 500);var scrolldown= window.scrollY + 500;return scrolldown;")

if stsLogin == 1:
    print('------------ start ------------ ')

    while not match:

        last_count = scrolldow_temp
        time.sleep(5)
        scrolldown  = driver.execute_script("window.scrollTo(0,  window.scrollY + 500);var scrolldown= document.body.scrollHeight;return scrolldown;")
        listTweets   = driver.find_elements(By.XPATH,'//main/div/div/div/div/div/div[4]/div/section/div/div/div/div/div/article/div/div/div/div[2]/div[2]')

        try:
            threads =  driver.find_elements(By.XPATH,'//main/div/div/div/div/div/div[4]/div/section/div/div/div/div/div/a')

            if threads:
                for thread in threads:
                    if thread:
                        listThread.extend([thread.get_attribute("href")])


        except Exception as Error:
            # print(Error)
            pass

        for tweet in listTweets:
            listImage       = []
            listUrlMedia    = []
            time.sleep(5)

            try:
                akunName    = tweet.find_elements(By.XPATH,"./div/div/div/div/div/a/div/div/div/span").text
                theTweets   = tweet.find_elements(By.XPATH,"./div[2]/div[1]/div/child::*")
                dateTweet   = tweet.find_elements(By.XPATH,"./div/div/div/div/a/time").get_attribute('datetime')

                theTweet    = []

                for tweets in theTweets:

                    try:
                        if tweets.text.replace("\n"," "):
                            theTweet.append(tweets.text.replace("\n"," "))

                    except Exception as Error:
                        # print(Error)
                        pass

                    try:
                        if tweets.get_attribute('src'):
                            emoji = tweets.get_attribute('src')
                            emoji = re.findall('\w+(?=.svg$)', emoji)
                            emoji = f"U000{emoji[0]}"
                            emoji = emoji.replace('U', r"\U").encode().decode('unicode-escape')
                            theTweet.append(emoji)

                    except Exception as Error:
                        # print(Error)
                        pass

                theTweet = ' '.join(theTweet)

                try:
                    singleImg   = tweet.find_elements(By.XPATH,"./div[2]/div[2]/div/div/div/div/div/a/div/div[2]/div/img").get_attribute('src')
                    now = datetime.now()
                    currentTime = now.strftime("%H_%M_%S")
                    akunNameSplit = '_'.join(akunName)

                    response = requests.get(singleImg, stream=True)
                    filename = '/home/lat/jensel/images/TW/{}_{}.jpg'.format(akunName, currentTime)
                    listImage.append({"image_file":response.content,'filename':filename})

                except Exception as Error:
                    # print(Error)
                    pass


                try:
                    listMltipleImg   = tweet.find_elements(By.XPATH,"./div[2]/div[2]/div[1]/div/div/div/div/div/div/div/a/div/div/img")
                    for multipleImg in listMltipleImg:
                        singleImg = multipleImg.get_attribute('src')
                        now = datetime.now()
                        currentTime = now.strftime("%H_%M_%S")
                        akunNameSplit = '_'.join(akunName)

                        response = requests.get(singleImg, stream=True)
                        filename = '/home/lat/jensel/images/TW/{}_{}.jpg'.format(akunName, currentTime)
                        listImage.append({"image_file":response.content,'filename':filename})

                except Exception as Error:
                    # print(Error)
                    pass

                theTweeted = f'{akunName}_{dateTweet}'
                if theTweeted not in listTweet:

                    for data in listImage:
                        imageFile = data.get('image_file')
                        fileName  = data.get('filename')
                        fileNames = fileName.replace("/home/lat/jensel/images/TW/","")

                        with open(filename, 'wb') as handle:
                                handle.write(imageFile)

                        listUrlMedia.append(fileNames)

                    listUrlMedia = list(set(listUrlMedia))
                    urlMedia = '|'.join([urlMedia for urlMedia in listUrlMedia if urlMedia])

                    listTweet.append(theTweeted)
                    listData.append([akunName, dateTweet, theTweet,  urlMedia])

                    print(akunName, dateTweet, theTweet, urlMedia)
                    db.insert('Twitter', akunName, dateTweet, theTweet, urlMedia, connection)

            except Exception as Error:
                # print(Error)
                pass

        if last_count==scrolldown:
            count  = 0

            while count < 11:

                scrolldown  = driver.execute_script("window.scrollTo(0,  window.scrollY + 100);var scrolldown= document.body.scrollHeight;return scrolldown;")
                if last_count==scrolldown and count < 10:
                    count = count + 1

                else:
                    break

                time.sleep(5)

            if count == 10:
                match = True

        scrolldow_temp = scrolldown
        driver.execute_script("window.scrollTo(0, window.scrollY + 500);")

    for threads in listThread :
        driver.get(threads)
        time.sleep(5)
        currentUrl = driver.current_url
        threadOwn  = re.findall(".*(?=[/status])", currentUrl)

        if threadOwn :
            threadOwn  = threadOwn[0]
            threadOwn  = threadOwn.replace('https:/twitter.com/','')
            threadOwn  = threadOwn.replace('/status','')

        allThread  = driver.find_elements(By.XPATH,"//main/div/div/div/div/div/section/div/div/div/div/div/article")

        akunNameTemp = ''
        for thread in allThread:
            try:
                akunName = thread.find_elements(By.XPATH,"./div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/a/div/div[2]/div/span").text
                akunNameTemp = akunName.replace('@','')
            except:
                akunName = ''
                pass

            if threadOwn == akunNameTemp:
                dateTweet = thread.find_elements(By.XPATH,"./div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/a/time").get_attribute('datetime')

                try:
                    theTweets  = thread.find_elements(By.XPATH,"./div/div/div/div[2]/div/div/div[2]/div/child::*")

                    for tweets in theTweets:

                        try:
                            if tweets.text.replace("\n"," "):
                                theTweet.append(tweets.text.replace("\n"," "))

                        except Exception as Error:
                            # print(Error)
                            pass

                        try:
                            if tweets.get_attribute('src'):
                                emoji = tweets.get_attribute('src')
                                emoji = re.findall('\w+(?=.svg$)', emoji)
                                emoji = f"U000{emoji[0]}"
                                emoji = emoji.replace('U', r"\U").encode().decode('unicode-escape')
                                theTweet.append(emoji)

                        except Exception as Error:
                            # print(Error)
                            pass

                    theTweet = ' '.join(theTweet)

                except Exception as Error:
                    pass

                try:
                    theTweets  = thread.find_elements(By.XPATH,"./div/div/div/div[2]/div[2]/div[2]/div[1]/div/child::*")

                    for tweets in theTweets:

                        try:
                            if tweets.text.replace("\n"," "):
                                theTweet.append(tweets.text.replace("\n"," "))

                        except Exception as Error:
                            # print(Error)
                            pass

                        try:
                            if tweets.get_attribute('src'):
                                emoji = tweets.get_attribute('src')
                                emoji = re.findall('\w+(?=.svg$)', emoji)
                                emoji = f"U000{emoji[0]}"
                                emoji = emoji.replace('U', r"\U").encode().decode('unicode-escape')
                                theTweet.append(emoji)

                        except Exception as Error:
                            # print(Error)
                            pass

                    theTweet = ' '.join(theTweet)

                except Exception as Error:
                    pass

                try:
                    theTweets  = thread.find_elements(By.XPATH,"./div/div/div/div[3]/div[1]/div/div[1]/child::*")

                    for tweets in theTweets:

                        try:
                            if tweets.text.replace("\n"," "):
                                theTweet.append(tweets.text.replace("\n"," "))

                        except Exception as Error:
                            # print(Error)
                            pass

                        try:
                            if tweets.get_attribute('src'):
                                emoji = tweets.get_attribute('src')
                                emoji = re.findall('\w+(?=.svg$)', emoji)
                                emoji = f"U000{emoji[0]}"
                                emoji = emoji.replace('U', r"\U").encode().decode('unicode-escape')
                                theTweet.append(emoji)

                        except Exception as Error:
                            # print(Error)
                            pass

                    theTweet = ' '.join(theTweet)

                except Exception as Error:
                    pass

                try:
                    singleImg  = thread.find_elements(By.XPATH,"./div/div/div/div/div/div/div/div/div/div/a/div/div[2]/div/img")
                    singleImg  = singleImg.get_attribute('src')
                    now = datetime.now()
                    currentTime = now.strftime("%H_%M_%S")
                    akunNameSplit = '_'.join(akunName)

                    response = requests.get(singleImg, stream=True)
                    filename = '/home/lat/jensel/images/TW/{}_{}.jpg'.format(akunName, currentTime)
                    listImage.append({"image_file":response.content,'filename':filename})

                except Exception as Error:
                    listUrlMedia = []

                try:
                    childThread = thread.find_elements(By.XPATH,'./div/div/div/div[2]/div[2]/div[2]/child::*')

                    if len(childThread) > 3:

                        singleImg  = thread.find_elements(By.XPATH,"./div/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/a/div/div[2]/div/img")
                        singleImg  = singleImg.get_attribute('src')
                        now = datetime.now()
                        currentTime = now.strftime("%H_%M_%S")
                        akunNameSplit = '_'.join(akunName)

                        response = requests.get(singleImg, stream=True)
                        filename = '/home/lat/jensel/images/TW/{}_{}.jpg'.format(akunName, currentTime)
                        listImage.append({"image_file":response.content,'filename':filename})

                    else:
                        singleImg  = thread.find_elements(By.XPATH,"./div/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/a/div/div[2]/div/img")
                        singleImg  = singleImg.get_attribute('src')
                        now = datetime.now()
                        currentTime = now.strftime("%H_%M_%S")
                        akunNameSplit = '_'.join(akunName)

                        response = requests.get(singleImg, stream=True)
                        filename = '/home/lat/jensel/images/TW/{}_{}.jpg'.format(akunName, currentTime)
                        listImage.append({"image_file":response.content,'filename':filename})

                except Exception as Error:
                    # print(Error)
                    pass


                theTweeted = f'{akunName}_{dateTweet}'

                if theTweeted not in listTweet:

                    for data in listImage:
                        imageFile = data.get('image_file')
                        fileName  = data.get('filename')
                        fileNames = fileName.replace("/home/lat/jensel/images/TW/","")

                        with open(filename, 'wb') as handle:
                                handle.write(imageFile)

                        listUrlMedia.append(fileNames)

                    listUrlMedia = list(set(listUrlMedia))
                    urlMedia = '|'.join([urlMedia for urlMedia in listUrlMedia if urlMedia])

                    listTweet.append(theTweeted)
                    listData.append([akunName, dateTweet, theTweet,  urlMedia])
                    print(akunName, dateTweet, theTweet, urlMedia)
                    db.insert('Twitter', akunName, dateTweet, theTweet, urlMedia, connection)

    print('------------ finish ------------ ')

else:
    print('gagal login')

driver.close()
time.sleep(5)
driver.quit()

db.close_connection(connection)
