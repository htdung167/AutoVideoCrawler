from enum import unique
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
import time
from TikTokApi import TikTokApi
from dotenv import load_dotenv
import argparse
import pyautogui
from pytube import YouTube, Search

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def get_id_video_from_url(url):
    return url.split("?")[0].split("/")[-1]

def convert_vietnamese_word(word):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    s = ''
    for c in word:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    s = "_".join(s.split(" "))
    return s

def tiktok(driver, keywords, limit=50, login_account=("", ""), unique=True):
    load_more = limit//12 + 5
    api = TikTokApi()
    first_key_word = True

    account_tiktok, password_tiktok = login_account
    if account_tiktok == "" or password_tiktok == "":
        print("Missing nickname or password in env file")
        return
    url = "https://www.tiktok.com/login"
    driver.get(url)
    time.sleep(1)

    # manual login
    gg_button = driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div/div/div[3]')
    # //*[@id="loginContainer"]/div/div/div[4]
    
    gg_button.click()
    print("Waiting 30s for manually login ...")
    time.sleep(5)
    pyautogui.typewrite(account_tiktok)
    pyautogui.press("tab")
    pyautogui.typewrite(password_tiktok)
    pyautogui.press("enter")
    time.sleep(20)

    for keyword in keywords:
        # Get old list url
        with open("./download/list_url.txt", "r") as f:
            lst_url_old = f.read().split("\n")
        lst_id_old = [get_id_video_from_url(url_video) for url_video in lst_url_old]
        
        lst_url = list()
        print(f"Processing keyword {keyword}")

        # check folder
        save_path = f"./download/{keyword}"
        if os.path.exists(save_path):
            continue

        # check first key word
        if first_key_word:
            first_key_word = False
        else:
            driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[3]/div[1]/button[1]').click()
            time.sleep(2)

        # fill keyword and search
        elem = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/form/input')
        elem.send_keys(Keys.CONTROL, 'a')
        elem.send_keys(keyword)

        search_button_elem = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/form/button')
        search_button_elem.click()
        time.sleep(2)

        # Scroll and click "Xem thêm"
        try:
            for i in range(load_more):  
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
                time.sleep(1)
                xemthem_button_xpath = '//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/button'
                if check_exists_by_xpath(driver=driver, xpath=xemthem_button_xpath):
                    driver.find_element(By.XPATH, xemthem_button_xpath).click()
        except:
            pass
        for k in range(5):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)      
                

        # click first video
        driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/div/div[3]/div[1]/div/div/a/div/div[1]').click()
        time.sleep(0.1)

        while True:
            # # check like button and like 
            # number_of_heart_1 = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/button[1]/strong').text
            # ## click button
            # like_button_elem = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/button[1]')
            # like_button_elem.click()
            # time.sleep(random.randint(2, 5))
            # ##

            # number_of_heart_2 = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/button[1]/strong').text
            # if number_of_heart_1 > number_of_heart_2:
            #     like_button_elem = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/button[1]')
            #     like_button_elem.click()
            #     time.sleep(0.1)
            # print(number_of_heart_1, number_of_heart_2)

            try:
                # get and check url 
                url = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/p').text
                
                # unique in every keyword
                if unique:
                    if get_id_video_from_url(url) not in lst_id_old:
                        lst_url.append(url)
                        if len(lst_url) >= limit:
                            break
                else:
                    lst_url.append(url)
                    if len(lst_url) >= limit:
                        break

                time.sleep(0.1)
                # click next 
                down_button_xpath = '//*[@id="app"]/div[2]/div[2]/div[2]/div[3]/div[1]/button[3]'
                if check_exists_by_xpath(driver=driver, xpath=down_button_xpath):
                    driver.find_element(By.XPATH, down_button_xpath).click()
                    time.sleep(random.randint(1, 10) / 10 + 1)
                else:
                    break
            except:
                print(f"Error keyword {keyword}")
                break

        # create folder keyword
        os.mkdir(f"./download/{keyword}")

        with open("./download/list_url.txt", "a") as f:
            f.write("\n".join(lst_url))
            f.write("\n")
        # download video
        print(f"Downloading {len(lst_url)} videos!")
        for idx, url in enumerate(lst_url):
            video_bytes = api.video(url=url).bytes()
            name_video = f"tiktok_{idx+1}_{convert_vietnamese_word(keyword)}.mp4"
            with open(os.path.join(save_path, name_video), "wb") as output:
                output.write(video_bytes)
            print(f"Done {name_video}!")

    print("Done!")
    driver.close()


def youtube(driver, keywords, limit=50, unique=True):
    first_keyword = True
    url = "https://www.youtube.com/"
    driver.get(url)
    time.sleep(2)
    with open("./download_youtube/list_url.txt") as f:
        lst_url_old = f.read().split("\n")

    for keyword in keywords:
        lst_url = []
        # Check folder
        save_path = f"./download_youtube/{keyword}"
        if os.path.exists(save_path):
            continue

        if first_keyword:
            first_keyword = False
        else:
            driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[1]/ytd-topbar-logo-renderer/a/div')
        
        # Fill search bar
        search_elem = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/input')
        search_elem.send_keys(Keys.CONTROL, 'a')
        search_elem.send_keys(keyword)

        # Click search button
        driver.find_element(By.XPATH, '//*[@id="search-icon-legacy"]').click()
        
        # Scroll 10 times
        for i in range(5):
            try:
                for k in range(5):
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
            except:
                continue

        # get links
        try:
            if len(lst_url) >= limit:
                break
            id_video = 1
            scroll_patient = 0
            while True:
                try:
                    url_video = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{id_video}]/div[1]/ytd-thumbnail/a").get_attribute("href")
                    scroll_patient = 0
                except:
                    if scroll_patient >= 5:
                        break
                    for k in range(10):
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                        scroll_patient += 1
                    time.sleep(1)
                if unique:
                    if url_video not in lst_url_old:
                        lst_url.append(url_video)
                else:
                    lst_url.append(url_video)
                id_video += 1
        except:
            pass
                
            
        print(lst_url)
        print("Downloading...")

        # Save for unique
        with open("./download_youtube/list_url.txt", "a") as f:
            f.write("\n".join(lst_url))
            f.write("\n")

        # Download video
        for url_video in lst_url:
            try:
                yt = YouTube(url_video)
            except:
                print(f"Cannot download {url_video}")
                continue
            ytt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            print(f"Downloading {yt.title}")
            try:
                ytt.download(save_path)
                print(f"Done {yt.title}!")
            except:
                print(f"Cannot download {yt.title}")

    print("Done!")

    


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--unique", type=str, default="true", help="Url of video in site is different.")
    parser.add_argument("--limit", type=int, default=50, help="Maximum count of videos to download per keyword.")
    parser.add_argument("--type", type=str, default="tiktok", help="Download from tiktok or youtube")
    # parser.add_argument("--youtube", type=str, default="true", help="Download from youtube.com")
    args = parser.parse_args()
    _unique = True if str(args.unique).lower() == 'true' else False
    _limit = int(args.limit)
    _type = str(args.type)
    if _type == "tiktok":
        _tiktok = True
        _youtube = False
    elif _type == "youtube":
        _tiktok = False
        _youtube = True
    else:
        _tiktok = False
        _youtube = False
    #################################################################
    # Note: 
    # conda create -n Crawl_Tiktok_env
    # conda install pip
    # python -m pip install --upgrade pip
    # pip install -r requirement.txt
    # conda activate Crawl_Tiktok_env
    ##################################################################

    PATH = "./chromedriver/chromedriver.exe"
    chrome_options = Options()
    # chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(PATH, options=chrome_options)
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

    # _tiktok = False
    if _tiktok:
        load_dotenv()
        account_tiktok = os.getenv('ACCOUNT_TIKTOK')
        password_tiktok = os.getenv('PASSWORD_TIKTOK')
        if not os.path.exists("./download"):
            os.mkdir("./download")
            with open("./download/list_url.txt", 'w', encoding="UTF-8") as f:
                f.write("hello_tiktok\n")
        

    if _youtube:
        if not os.path.exists("./download_youtube"):
            os.mkdir("./download_youtube")
            with open("./download_youtube/list_url.txt", 'w', encoding="UTF-8") as f:
                f.write("hello_youtube\n")

    with open("./keywords.txt", "r", encoding='UTF-8') as f:
        keywords = f.read().split("\n")

    print(keywords)


    # Runnnn
    if _tiktok:
        tiktok(driver, keywords, limit=_limit, unique=_unique, login_account=(account_tiktok, password_tiktok))
    
    if _youtube:
        youtube(driver, keywords, limit=_limit, unique=_unique)