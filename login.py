import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, getpass, datetime, os, requests

def is_element_present(driver, xpath): 
    try: 
        driver.find_element(By.XPATH, xpath) 
        return True 
    except selenium.common.exceptions.NoSuchElementException: 
        return False

def login():
    
    # Test용 Image 폴더
    # if not os.path.isdir("Image"):
    #     os.mkdir("Image")
    # Capcha 보관용 폴더, Capcha 이미지 파일은 로그인 성공 후 삭제된다.
    if not os.path.isdir("Captcha"):
        os.mkdir("Captcha")
    # 데이터가 다운로드 되는 폴더
    if not os.path.isdir("Data"):
        os.mkdir("Data")
        
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("headless")

    url = 'https://auth.data.go.kr/sso/common-login?client_id=hagwng3yzgpdmbpr2rxn&redirect_url=https://data.go.kr/sso/profile.do'
    
    # driver로 공공데이터포털 사이트에 요청 보내기
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(4)

    while True:
        
        # 보안문자 불러와서 캡쳐 (추출하는 방식은 보안문자가 매번 바뀌어서 캡쳐로 진행, 파일로 만들어졌기 때문에 파일 열어서 확인 가능)
        pull_captcha = driver.find_element(By.ID, "captchaImg")
        chaptcah_img = pull_captcha.screenshot_as_png
        with open("Captcha/Captcha.png", "wb") as f:
            f.write(chaptcah_img)
        
        # 아이디와 비밀번호 입력. 비밀번호는 보이지 않게 입력 가능.
        enter_id = input("아이디 입력: ")
        enter_password = getpass.getpass("비밀번호 입력: ")

        # 아이디를 아이디 입력 칸에 넣어주는 코드
        input_id = driver.find_element(By.ID, "inputUsername")
        ActionChains(driver).send_keys_to_element(input_id, enter_id).perform()

        # 비밀번호를 비밀번호 입력 칸에 넣어주는 코드
        input_password = driver.find_element(By.ID, "inputPassword")
        ActionChains(driver).send_keys_to_element(input_password, enter_password).perform()    
        
        # 보안문자 입력. 열려서 보이는 보안문자를 입력.
        enter_captcha = input("보안문자 입력: ")

        # 보안문자를 보안문자 입력 칸에 넣어주는 코드.
        input_captcha = driver.find_element(By.ID, "captcha")
        ActionChains(driver).send_keys_to_element(input_captcha, enter_captcha).perform()

        # 만약 보안문자, 비밀번호, 아이디를 모두 입력했다면 작동하는 코드. 입력하지 않으면 작동 안 하며 else문으로 빠져 print문 출력.
        try:
            if enter_captcha is not False and enter_password is not False and enter_id is not False:
                login_button = driver.find_element(By.ID, "login-btn")
                ActionChains(driver).click(login_button).perform()
                if is_element_present(driver, '//*[@id="password-change-modal"]') or is_element_present(driver, '//*[@id="layer_instt_search"]'):
                    if driver.find_element(By.XPATH, '//*[@id="password-change-modal"]'):    
                        password_change_info_close = driver.find_element(By.XPATH, '//*[@id="password-change-modal"]/a')
                        ActionChains(driver).click(password_change_info_close).perform()
                    time.sleep(1)
                    if driver.find_element(By.XPATH, '//*[@id="layer_instt_search"]'):
                        layer_instt_search_close = driver.find_element(By.XPATH, '//*[@id="layer_instt_search"]/a')
                        ActionChains(driver).click(layer_instt_search_close).perform()
                # driver.get_screenshot_as_file("Image/login_capture.png")
                time.sleep(1)
                # if os.listdir("Image") is not None:
                #     os.rename("Image/login_capture.png", 
                #             f'Image/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_login_capture.png')
                selenium_cookies = driver.get_cookies()
                break
            else:
                print("모든 내용을 입력해주세요.")
        except selenium.common.exceptions.UnexpectedAlertPresentException as e:
            print(str(e))
            driver.refresh()
    
    session = requests.session()
    
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    driver.quit()
    
    return session
    