from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from model import Connection
from datetime import date, datetime
import os, time, csv, requests, re, requests

db = Connection()
connection = db.connect()

os.path.exists('/home/tsel-ai/deploy/api/public/crawl/socmed')

#if not os.path.exists('Facebook'):
    #os.makedirs('Facebook')

options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu') 
options.add_argument("--disable-notifications")
options.add_argument('--disable-setuid-sandbox') 
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

#driver = webdriver.Chrome('/home/tsel-ai/bin/chromedriver', chrome_options=options)
driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe', chrome_options=options)
time.sleep(5)
driver.get("http:/www.facebook.com")
time.sleep(5)

username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
username.clear()
username.send_keys("diisi_sendiri")
password.clear()
password.send_keys("diisi_sendiri")

try:
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    stsLogin = 1
except:
    stsLogin = 0
    pass

time.sleep(5)
driver.get("http:/www.facebook.com")
time.sleep(5)

listData        =   []
listAllMedia    =   [] 
ListPost        =   []
listThePost     =   []
driver.execute_script("window.scrollTo(0, window.scrollY + 400)")
match           =  False

height_temp     =  0

if stsLogin == 1:
    print('------------ start ------------ ')
    while(match==False):
        time.sleep(2)
        main_window     =  driver.current_window_handle
        
        try:
            lastFeed    = driver.find_element_by_xpath('//html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[3]/div/div[4]/div/div/div/div/div/div[3]/a')
            
        except Exception as Error:
            # print(Error)
            lastFeed    = ''
            pass

        listFeed    = driver.find_elements_by_xpath("//div[@role='feed']/div/div/div/div/div/div[@role='article']")
        feedLength  = len(listFeed)

        for i in listFeed:

            try:
                listUrlMedia = []
                listImage = []
                thePosts  = []
                scrollElementIntoMiddle = "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);" + "var elementTop = arguments[0].getBoundingClientRect().top;" + "window.scrollBy(0, elementTop-(viewPortHeight/2));"
                
                akunNames = i.find_element_by_xpath("./div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/span/h4/span[1]/a/strong/span")
                driver.execute_script(scrollElementIntoMiddle, akunNames)
                akunName  = akunNames.text.replace('\n','')
                actions = ActionChains(driver)
                actions.move_to_element(akunNames)
                time.sleep(5)
                datePost = i.find_element_by_xpath('./div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span/span/span[2]/span/a')
                actions.move_to_element(datePost).perform()
                time.sleep(5)
                datePost = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/span/div/div/span').text
                joinAkunName = '_'.join(akunName.split())
                joinDatePost = '_'.join(datePost.split())
                idPost = '{}_{}'.format(joinAkunName, joinDatePost)
                time.sleep(5)
                urlImg      = i.find_elements_by_xpath("./div/div/div/div/div/div/div/div[3]/div[2]/div/div/*/*/*/*/div")
                multipleImg = i.find_elements_by_xpath('./div/div/div/div/div/div/div/div[3]/div[2]/div/div/*/*/*/div/a/div/div/div') 
                isMore   = True 
        
                while isMore:

                    try:
                        cekText = i.find_element_by_xpath('//div[contains(text(), "Lihat Selengkapnya")]').text

                        time.sleep(5)
                        if cekText == 'Lihat Selengkapnya':
                            i.find_element_by_xpath('//div[contains(text(), "Lihat Selengkapnya")]').click()
                            isMore = False
                            time.sleep(5)
                        
                        else:
                            isMore = False

                    except Exception as Error:
                        # print(Error)
                        isMore = False
                    
                try:
                    urlImgAdd   = i.find_elements_by_xpath("./div/div/div/div/div/div/div/div[3]/div/div/div/div/div/div/div/div/div/div")
                
                except Exception as Error:
                    # print(Error)
                    urlImgAdd = []

                for media in urlImg:

                    try:
                        time.sleep(2)    
                        urls = media.find_element_by_tag_name('img').get_attribute('src')
                        now = datetime.now()
                        currentTime = now.strftime("%H_%M_%S")
                        akunNameSplit = '_'.join(akunName)

                        now = datetime.now()
                        currentTime = now.strftime("%H_%M_%S")
                        akunNameSplit = '_'.join(akunName)

                        response = requests.get(urls, stream=True)
                        time.sleep(2)    

                        #filename = f"Facebook/{akunName}_{currentTime}.jpg"
                        filename = f"images/{akunName}_{currentTime}.jpg".replace(' ','_')

                        listImage.append({"image_file":response.content,'filename':filename})


                    except Exception as Error:
                        #print(Error)
                        pass
                

                for media in multipleImg:

                    try:    
                        time.sleep(2)
                        urls = media.find_element_by_tag_name('img').get_attribute('src')
                        now = datetime.now()
                        currentTime = now.strftime("%H_%M_%S")
                        akunNameSplit = '_'.join(akunName)

                        now = datetime.now()
                        currentTime = now.strftime("%H_%M_%S")
                        akunNameSplit = '_'.join(akunName)

                        response = requests.get(urls, stream=True)
                        time.sleep(2)    

                        filename = f"images/{akunName}_{currentTime}.jpg".replace(' ','_')

                        listImage.append({"image_file":response.content,'filename':filename})

                    except Exception as Error:
                        # print(Error)
                        pass

                for media in urlImgAdd:

                    try:
                        time.sleep(2)
                        urls = media.find_element_by_tag_name('img').get_attribute('src')
                        now = datetime.now()
                        currentTime = now.strftime("%H_%M_%S")
                        akunNameSplit = '_'.join(akunName)

                        now = datetime.now()
                        currentTime = now.strftime("%H_%M_%S")
                        akunNameSplit = '_'.join(akunName)

                        response = requests.get(urls, stream=True)
                        time.sleep(2)    

                        filename = f"images/{akunName}_{currentTime}.jpg".replace(' ','_')
                        
                        listImage.append({"image_file":response.content,'filename':filename})

                    except Exception as Error:
                        # print(Error)
                        break

                thePost   = i.find_elements_by_xpath("./div/div/div/div/div/div/div/div[3]/div[1]/div/div/div/span/div/div")

                for posts in thePost:
                    
                    try:
                        if posts.text.replace("\n"," "):
                            thePosts.append(posts.text.replace("\n"," "))

                    except Exception as Error:
                        # print(Error)
                        pass
                    
    
                    try:
                        theEmoji = posts.find_elements_by_xpath('./span/img')
                        for emoj in theEmoji: 
                            emoji = emoj.get_attribute('src')
                            emoji = re.findall('\w+(?=.png$)', emoji)
                            emoji = f"U000{emoji[0]}"
                            emoji = emoji.replace('U', r"\U").encode().decode('unicode-escape')
                            thePosts.append(emoji)

                    except Exception as Error:
                        # print(Error)
                        pass
                        
                thePost = ' '.join(thePosts)

                if idPost not in ListPost:

                    for data in listImage:
                        imageFile = data.get('image_file')
                        fileName  = data.get('filename')
                        fileNames = fileName.replace('images/','').replace(' ','_')

                        with open(fileName, 'wb') as handle:
                                handle.write(imageFile)
                        
                        listUrlMedia.append(fileNames)
                    
                    listUrlMedia = list(set(listUrlMedia))
                    urlMedia = '|'.join([urlMedia for urlMedia in listUrlMedia if urlMedia])

                    print([akunName, datePost, thePost,  urlMedia])
                    ListPost.append(idPost)
                    # listData.append([akunName, datePost, thePost,  urlMedia])
                    db.insert('Facebook', akunName, datePost, thePost, urlMedia, connection)

            except Exception as Error:
                #print('2 -> \t', Error)
                pass

        time.sleep(5)

        if lastFeed:
            match = True

        else:
            pass
        

    print('------------ finish ------------ ')

else:
    print('gagal login')

driver.close()
time.sleep(5)
driver.quit()

db.close_connection(connection)

# path = os.getcwd()
# path = os.path.join(path, 'test')

# if not os.path.exists(path):
#     os.mkdir(path)

# header      = ['NICKNAME', 'DATETIME', 'TAGLINE', 'URL_IMAGE']
# pathCSV   = os.path.join(path, 'FB.csv')

# with open(pathCSV, 'w', newline ='', encoding="utf-8") as f: 
#     write = csv.writer(f) 
#     write.writerow(header) 
#     write.writerows(listData) 
