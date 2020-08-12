from flask import Flask, render_template, request
from selenium import webdriver
from res.ImageScrapper import image_scrapper
import os


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
#driver_path = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route("/download", methods=["GET","POST"])
def download_image():
    if request.method == "POST":
        try:
            search_string = str(request.form["search_string"])
            quantity = int(request.form["quantity"])

            scrapper_object = image_scrapper()

            try:
                keyword = search_string.replace(" ", "%20").lower()
                print(f" keyword is {keyword} and type is {type(keyword)}, quantity is {quantity} and type {type(quantity)}")

                path, exist = scrapper_object.create_path(query=keyword)

                if exist[0] and quantity <= exist[1]:
                    try:
                        images = scrapper_object.show_image(path=path, query=keyword,max_img=quantity)
                        return render_template("result.html", user_images=images)
                    except Exception as e:
                        print("Exception code rd9-- ", e)
                        return render_template("error.html", exception=e)
                else:
                    try:
                        #driver_path = webdriver.Chrome("3chromedriver.exe")
                        driver_path = os.environ.get("CHROMEDRIVER_PATH")
                        images = scrapper_object.search_and_download(driver=driver_path,driver_options=chrome_options ,
                                                                     search_string=keyword, maximum_imgs=quantity)
                        return render_template("result.html", user_images=images)
                    except Exception as e:
                        print("Exception code g62-- ", e)
                        return render_template("error.html", exception="Failed to load Chrome Driver, Please refresh homepage and Try again")
            except Exception as e:
                    print("Exception code da6-- ",e)
                    return render_template("error.html", exception=e)

        except Exception as e:
            print("exception code d4b-- ",e)
            return render_template("error.html", exception=e)

    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run()
