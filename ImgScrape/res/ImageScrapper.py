# imports
import os
from selenium import webdriver
import numpy as np
import time
import random
import requests


class image_scrapper:
    # def __init__(self, driverpath, query, max_imgs):
    #     self.driverpath = driverpath
    #     self.query = query.replace(" ","%20").lower()
    #     self.max_images = max_imgs

    def create_path(self, query):
        try:
            path = os.path.join("static", query)
            if os.path.exists(path):
                if len(os.listdir(path)) > 1:
                    exist = [True, len(os.listdir(path))]
                else:
                    exist = [False, 0]
            else:
                os.mkdir(path)
                exist = [False, 0]
                print("New Path Created ", path)
            return path, exist
        except Exception as e:
            print("Exception code 3f2 ", e)

    def split_list(self, img_list, parts):
        start = 0
        stop = parts
        new_list = []
        for i in np.arange(np.ceil(len(img_list) / parts)):
            new_list.append(img_list[start:stop])
            start = stop
            stop += parts
        return new_list

    def show_image(self, path, query, max_img):
        # path = self.path
        try:
            img_names = os.listdir(path)

            actual_imgs = []
            for i in img_names:
                if len(actual_imgs) >= max_img:
                    break
                filename, ext = os.path.splitext(i)
                if ext == ".jpg":
                    img_path = query + "/" + i
                    actual_imgs.append(img_path)
            random.shuffle(actual_imgs)
            print("printed frm show_image ", actual_imgs)
            splited_list = self.split_list(actual_imgs, 3)
            return splited_list
        except Exception as e:
            print("exception code fbe ", e)

    def get_img_urls(self, driver, query, max_images, sleep_between_interactions=0.4):
        # driver = self.driverpath
        def scroll_to_end(driver):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(sleep_between_interactions)

        # try:
        #     url = "https://www.google.co.in/search?q=" + query + "&tbm=isch&hl=en&hl=en&tbs=isz%3Al"
        #     print(f"search url is {url}")
        # except Exception as e:
        #     print("Exception code 7e3 -- ",e)

        url = "https://www.google.co.in/search?q=" + query + "&tbm=isch&hl=en&hl=en&tbs=isz%3Al"
        print(f"search url is {url}")
        # driver.set_page_load_timeout(10)
        driver.get(url)

        img_urls = set()
        image_count = 0
        start_result = 0
        while image_count < max_images:
            scroll_to_end(driver)
            thumbnail_imgs = driver.find_elements_by_css_selector("img.Q4LuWd")

            print(f"Found total {len(thumbnail_imgs)} images extracting images")

            for thumbnail in thumbnail_imgs[start_result:len(thumbnail_imgs)]:
                try:
                    thumbnail.click()
                    time.sleep(sleep_between_interactions)
                    imgs = driver.find_elements_by_css_selector("img.n3VNCb")
                except Exception as e:
                    print("ignore this Exception  ", e)
                    continue

                for actual_url in imgs:
                    if actual_url.get_attribute("src") and "http" in actual_url.get_attribute("src"):
                        img_urls.add(actual_url.get_attribute("src"))
                        print(f"image url is {actual_url.get_attribute('src')}")

                image_count = len(img_urls)
                if len(img_urls) >= max_images:
                    print(f"Found {len(img_urls)} image links done")
                    break
            else:
                print(f"found {image_count} images, looking for more")
                time.sleep(10)

                load_more_button = driver.find_elements_by_css_selector(".mye4qd")
                if load_more_button:
                    driver.execute_script("document.querySelector('.mye4qd').click();")
                start_result = len(thumbnail_imgs)

        return img_urls

    def download_and_save(self, query, urls, exist_list, path):
        # if exist_list[0]==True:
        #     counter = exist_list[1]
        #     print("old images present")
        # else:
        counter = 0
        if len(urls) > 0:
            for i, url in enumerate(urls, start=counter):
                file_name = query + "_" + str(i) + ".jpg"
                full_path = os.path.join(path, file_name)
                try:
                    print(f"downloading image no {i}")
                    image_byte = requests.get(url).content
                    with open(full_path, "wb") as f:
                        f.write(image_byte)
                        print(f"Saved image no {i} in {full_path}")
                except Exception as e:
                    print("Exception code 86f-- ", e)  # 3
                    continue

            print("Finished downloading all images")
        else:
            print("No images Try again")

    def search_and_download(self, driver,driver_options, search_string, maximum_imgs):
        try:
            path, exist = self.create_path(query=search_string)
            print(f"path is {path} and exist = {exist}")

            with webdriver.Chrome(driver, chrome_options=driver_options) as wd:
                img_urls = self.get_img_urls(driver=wd, query=search_string, max_images=maximum_imgs,
                                             sleep_between_interactions=0.3)

            self.download_and_save(query=search_string, urls=img_urls, exist_list=exist, path=path)

            img = self.show_image(path=path, query=search_string, max_img=maximum_imgs)

            return img
        except Exception as e:
            print("exception code 91f-- ", e)
