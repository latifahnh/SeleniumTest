from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from model import Connection
from datetime import datetime
import os, time, csv, requests

db = Connection()
connection = db.connect()

os.path.exists('/home/tsel-ai/deploy/api/public/crawl/socmed')

#if not os.path.exists('Instagram'):
    #os.makedirs('Instagram')

options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument("--disable-notifications")
options.add_argument('--disable-setuid-sandbox')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

driver = webdriver.Chrome('/home/lat/chromedriver', chrome_options=options)
#driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe', chrome_options=options)
driver.get("https://www.instagram.com/accounts/login/")

username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
username.clear()
password.clear()
username.send_keys("isi sendiri")
password.send_keys("isi sendiri")
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
print('------------ start ------------ ')
try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Lain Kali")]'))).click()

except Exception as Error:
    # print(Error)
    pass

try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Lain Kali")]'))).click()

except Exception as Error:
    # print(Error)
    pass

try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

except Exception as Error:
    # print(Error)
    pass

try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

except Exception as Error:
    # print(Error)
    pass

try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not now")]'))).click()

except Exception as Error:
    # print(Error)
    pass

try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not now")]'))).click()

except Exception as Error:
    # print(Error)
    pass


listPost        =   []
listData        =   []
listAllMedia    =   []
scrolldow_temp  = driver.execute_script("window.scrollTo(0,  window.scrollY + 500);var scrolldown= window.scrollY + 500;return scrolldown;")
match           =   False


while not match:
    last_count = scrolldow_temp
    scrolldown = driver.execute_script("window.scrollTo(0,  window.scrollY + 500);var scrolldown= document.body.scrollHeight;return scrolldown;")

    driver.execute_script("window.scrollTo(0, window.scrollY + 500);")
    time.sleep(5)

    listFeed    = driver.find_elements_by_xpath("//main/section/div/div/div/div/article")
    #listFeed    = driver.find_elements_by_xpath("//main/section/div/div[3]/div/article")
    #print(len(listFeed))
    if listFeed:



        for i in listFeed:

            linkPost = i.find_element_by_xpath('./div/div[3]/div/div/*[4]/div/a').get_attribute('href')
            print(linkPost)

            if linkPost not in listPost:
                listPost.append(linkPost)

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


for linkPosted in listPost:
    listUrlMedia    = []
    akunName        = ''

    driver.get(linkPosted)
    time.sleep(10)

    try:
        akunName        = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/div/span/a").text

    except Exception as Error:
        #print(Error)
        akunName        = ''

    if akunName:
        try:

            thePost     = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div/span").text.replace("\n"," ")

        except Exception as Error:
            thePost     = ''

        datePost        = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/article/div/div[2]/div/div[2]/div[2]/div/a/div/time").get_attribute('title')

        try:

            try:
                urlImg      =  driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/article/div/div[1]/div/div/div[1]/img").get_attribute("src")

            except:

                urlImg      = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div/div[1]/div/div/div[1]/div[1]/img").get_attribute("src")

            now = datetime.now()
            currentTime = now.strftime("%H_%M_%S")
            akunNameSplit = '_'.join(akunName)

            #filename = f'Instagram/{akunName}_{currentTime}.jpg'
            #filename = 'Instagram/{}_{}.jpg'.format(akunName, currentTime)
            filename = '/home/tsel-ai/deploy/api/public/crawl/socmed/{}_{}.jpg'.format(akunName, currentTime)
            filenames = '{}_{}.jpg'.format(akunName, currentTime)


            with open(filename, 'wb') as handle:
                response = requests.get(urlImg, stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)

            listUrlMedia.append(filenames)

        except Exception as Error:
            #print(Error)
            pass

        # try:
        #     urlVideo    = driver.find_element_by_xpath("//main//div//div//article/div//div//div//div//div//div//video").get_attribute("src")
        #     listUrlMedia.append(urlVideo)

        # except Exception as Error:
        #     print(Error)
        #     pass

        last  = False
        first = False

        while not last:
            urlMedias   = driver.find_elements_by_xpath("//main//div//div//article//div//div//div//div//div[2]//div/button[@tabindex='-1']")
            #print(len(urlMedias))

            if len(urlMedias) == 1  and not first:

                try:
                    img     = driver.find_element_by_xpath("//main//div//div//article//div//div//div//div//div//div//div//div//ul/li[2]/div/div/div/div/img")
                    urls    = img.get_attribute('src')
                    now = datetime.now()
                    currentTime = now.strftime("%H_%M_%S")
                    akunNameSplit = '_'.join(akunName)

                    #filename = f'Instagram/{akunName}_{currentTime}.jpg'
                    filename = '/home/tsel-ai/deploy/api/public/crawl/socmed/{}_{}.jpg'.format(akunName, currentTime)
                    filenames = '{}_{}.jpg'.format(akunName, currentTime)

                    with open(filename, 'wb') as handle:
                        response = requests.get(urls, stream=True)

                        if not response.ok:
                            print(response)

                        for block in response.iter_content(1024):
                            if not block:
                                break

                            handle.write(block)

                    listUrlMedia.append(filenames)

                except Exception as Error:
                    #print(Error)
                    pass
                # try:
                #     video   = driver.find_element_by_xpath("//main//div//div//article//div//div//div//div//div//div//div//div//ul/li[2]/div/div/div/div/video")
                #     urls    = video.get_attribute('src')
                #     listUrlMedia.append(urls)

                # except Exception as Error:
                #     print(Error)

                driver.find_element_by_xpath("//main//div//div//article//div//div//div//div//div//div/button[1]/div").click()
                first = True
                time.sleep(3)


            elif len(urlMedias) == 1 and first :

                try:
                    img     = driver.find_element_by_xpath("//main//div//div//article//div//div//div//div//div//div//div//div//ul/li[3]/div/div/div/div/img")
                    urls    = img.get_attribute('src')

                    now = datetime.now()
                    currentTime = now.strftime("%H_%M_%S")
                    akunNameSplit = '_'.join(akunName)

                    #filename = f'Instagram/{akunName}_{currentTime}.jpg'
                    filename = '/home/tsel-ai/deploy/api/public/crawl/socmed/{}_{}.jpg'.format(akunName, currentTime)
                    filenames = '{}_{}.jpg'.format(akunName, currentTime)

                    with open(filename, 'wb') as handle:
                        response = requests.get(urls, stream=True)

                        if not response.ok:
                            print(response)

                        for block in response.iter_content(1024):
                            if not block:
                                break

                            handle.write(block)

                    listUrlMedia.append(filenames)

                except Exception as Error:
                    #print(Error)
                    pass

                # try:
                #     video   = driver.find_element_by_xpath("//main//div//div//article//div//div//div//div//div//div//div//div//ul/li[3]/div/div/div/div/video")
                #     urls    = video.get_attribute('src')
                #     listUrlMedia.append(urls)

                # except Exception as Error:
                #     print(Error)


                last = True

            elif len(urlMedias) == 2:

                try:
                    img     = driver.find_element_by_xpath("//main//div//div//article//div//div//div//div//div//div//div//div//ul/li[3]/div/div/div/div/img")
                    urls    = img.get_attribute('src')
                    now = datetime.now()
                    currentTime = now.strftime("%H_%M_%S")
                    akunNameSplit = '_'.join(akunName)

                    #filename = f'Instagram/{akunName}_{currentTime}.jpg'
                    filename = '/home/tsel-ai/deploy/api/public/crawl/socmed/{}_{}.jpg'.format(akunName, currentTime)
                    filenames = '{}_{}.jpg'.format(akunName, currentTime)

                    with open(filename, 'wb') as handle:
                        response = requests.get(urls, stream=True)

                        if not response.ok:
                            #print(response)
                            pass

                        for block in response.iter_content(1024):
                            if not block:
                                break

                            handle.write(block)

                    listUrlMedia.append(filenames)

                except Exception as Error:
                    #print(Error)
                    pass

                # try:
                #     video   = driver.find_element_by_xpath("//main//div//div//article//div//div//div//div//div//div//div//div//ul/li[3]/div/div/div/div/video")
                #     urls    = video.get_attribute('src')
                #     listUrlMedia.append(urls)

                # except Exception as Error:
                #     print(Error)

                driver.find_element_by_xpath("//main//div//div//article//div//div//div//div//div[2]//div/button[@tabindex='-1'][2]").click()
                time.sleep(3)

            else:
                last = True


        listUrlMedia = list(set(listUrlMedia))
        urlMedia = '|'.join([urlMedia for urlMedia in listUrlMedia if urlMedia])

        print([akunName, datePost, thePost,  urlMedia])
        # listData.append([akunName, datePost, thePost,  urlMedia])
        db.insert('Instagram', akunName, datePost, thePost, urlMedia, connection)

print('------------ finish ------------ ')
driver.close()
time.sleep(5)
driver.quit()

db.close_connection(connection)

# path = os.getcwd()
# path = os.path.join(path, 'test')

# if not os.path.exists(path):
#     os.mkdir(path)

# header      = ['NICKNAME', 'DATETIME', 'TAGLINE', 'URL_IMAGE']
# pathCSV   = os.path.join(path, 'IG.csv')

# with open(pathCSV, 'w', newline ='', encoding="utf-8") as f:
#     write = csv.writer(f)
#     write.writerow(header)
#     write.writerows(listData)
