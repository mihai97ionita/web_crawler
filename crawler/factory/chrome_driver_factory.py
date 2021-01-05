from time import sleep

from selenium import webdriver


def create_web_driver(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.headless = True
    arguments = [f'user-agent={user_agent}', "--window-size=1920,1080", '--ignore-certificate-errors',
                 '--allow-running-insecure-content', "--disable-extensions", "--proxy-server='direct://'",
                 "--start-maximized", '--disable-gpu', '--disable-dev-shm-usage',
                 '--no-sandbox', "--proxy-bypass-list=*"]
    for arg in arguments:
        options.add_argument(arg)
    driver = webdriver.Chrome(executable_path='/bin/chromedriver', options=options)
    driver.get(url)
    sleep(1)
    return driver
