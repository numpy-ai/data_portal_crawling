import re, math
import time
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
import selenium.webdriver
import selenium.webdriver.chrome
import selenium.webdriver.chrome.webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import os
import login

def is_element_present(driver, xpath): 
    try: 
        driver.find_element(By.XPATH, xpath) 
        return True 
    except selenium.common.exceptions.NoSuchElementException: 
        return False

# def check_extension(driver, xpath):
#     match xpath:
#         case '//*[@id="contents"]/div[2]/div[1]/div[1]/span':
#             target_extension = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[1]/div[1]/span').get_attribute('innerText')
#             return target_extension
#         case '//*[@id="tab-layer-file"]/div[2]/span':
#             target_extension = driver.find_element(By.XPATH, '//*[@id="tab-layer-file"]/div[2]/span').get_attribute('innerText')
#             return target_extension
#         case _:
#             print("XPATH를 다시 확인하세요.")

def check_last_page(driver: webdriver, pages: list):
    new_pages = []
    for page in pages:
        if '페이지' not in page.get_attribute("innerText"):
            new_pages.append(int(page.get_attribute("innerText")))
    ActionChains(driver).click(pages[-2]).preform()
    if pages[-3].get_attribute("innerText") == new_pages[-1]:
        return True
    else:
        return False

def data_download(driver: webdriver, xpath: str):
    download_btn = driver.find_element(By.XPATH, xpath)
    file_name = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[1]/div[1]/p').text
    if '바로가기' not in download_btn.get_attribute('innerText'):
        ActionChains(driver).click(download_btn).perform()
        check_alert(driver)
        time.sleep(0.5)
        print(f"{file_name} 파일 다운로드 완료")
    else:
        print('외부 사이트 다운은 현재 지원 안 함.')
    driver.back()

def check_alert(driver):
    if EC.alert_is_present():
        try:
            alert = driver.switch_to.alert
            print(alert.text)
            alert.accept()
        except:
            pass
        
def is_alert_present(driver, timeout=5): 
    try: 
        WebDriverWait(driver, timeout).until(EC.alert_is_present()) 
        return True 
    except: 
        return False
    

def get_api(driver: webdriver, xpath: str):
    # application_btn = driver.find_element(By.XPATH, xpath)
    # file_name = driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[1]/div[1]/p').text
    # if '바로가기' not in application_btn.get_attribute('innerText'):
    #     check_alert(driver)
    #     driver.switch_to.window(driver.window_handles[-1])
    #     ActionChains(driver).click(driver.find_element(By.XPATH, '//*[@id="radio4"]')).perform()
    while True:
        try:
            enter_purpose = input('활용목적 입력: ')
        except Exception as e:
            print(str(e))
            print('활용 목적을 다시 입력해주세요.')
            continue
        if enter_purpose:
            break
        else:
            print("활용 목적을 입력해주세요.")
    ActionChains(driver).send_keys_to_element(driver.find_element(By.XPATH, '//*[@id="prcusePurps"]'), enter_purpose).perform()
    ActionChains(driver).click(driver.find_element(By.XPATH, '//*[@id="useScopeAgreAt"]')).perform()
    ActionChains(driver).click(driver.find_element(By.XPATH, '//*[@id="loadingDiv"]/div[2]/button')).perform()
    check_alert(driver)
    time.sleep(1)
    # print(f"{file_name} API 신청 완료")
    # else:
    #     print('외부 사이트 다운은 현재 지원 안 함.')
    driver.close()
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[0])
    
def check_api(driver):
    driver.get('https://www.data.go.kr/iim/api/selectAcountList.do')
    # if len(driver.window_handles) < 2:
    #     driver.execute_script('window.open("https://www.data.go.kr/iim/api/selectAcountList.do");')
    # if len(driver.window_handles) > 1:
    #     driver.switch_to.window(driver.window_handles[-1])
    try:
        application_api_list = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[3]/ul')
        application_apis = application_api_list.find_elements(By.TAG_NAME, 'li')
        api_name_list = []
        for i in range(len(application_apis)):
            api_name_list.append(application_apis[i].find_element(By.CLASS_NAME, 'title').text)
    except Exception as e:
        print(str(e))
    # for index, name in enumerate(api_name_list):
    #     print(f'{index}: {name}')
    time.sleep(1)
    driver.back()
    return api_name_list

def get_api_Data(driver):
    pass
    

def search():
    
    session = login.login()
    url = 'https://data.go.kr'
    
    base_dir = os.getcwd()
    data_dir = os.path.join(base_dir, "Data")

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", 
                                           {"download.default_directory": data_dir, # 경로 수정 필요
                                            "download.prompt_for_download": False,
                                            "download.directory_upgrade": True,
                                            "safebrowsing.enabled": True})
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument('no-sandbox')
    chrome_options.add_argument('disable-dev-shm-usage')
    chrome_options.add_argument('--disable-popup-blocking')
    # chrome_options.add_argument("headless")
    user_agent=f"Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36"
    chrome_options.add_argument(f"--user-agent={user_agent}")
    
    # driver로 공공데이터포털 사이트에 요청 보내기
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    for cookie in session.cookies:
        driver.add_cookie({'name': cookie.name, 'value': cookie.value, 'path': cookie.path})
    driver.refresh()
    driver.maximize_window()
    time.sleep(1.5)
    # 비밀번호 변경 창 뜰 시에 작동
    # if is_element_present(driver, '//*[@id="password-change-modal"]') or is_element_present(driver, '//*[@id="layer_instt_search"]'):
        # if driver.find_element(By.XPATH, '//*[@id="password-change-modal"]'):    
    try:
        password_change_info_close = driver.find_element(By.XPATH, '//*[@id="password-change-modal"]/a')
        ActionChains(driver).click(password_change_info_close).perform()
    except selenium.common.exceptions.NoSuchElementException:
        pass # 모달이 없으면 그냥 넘어감
    time.sleep(1)
        # if driver.find_element(By.XPATH, '//*[@id="layer_instt_search"]'):
    try:
        layer_instt_search_close = driver.find_element(By.XPATH, '//*[@id="layer_instt_search"]/a')
        ActionChains(driver).click(layer_instt_search_close).perform()
    except selenium.common.exceptions.NoSuchElementException:
        pass # 모달이 없으면 그냥 넘어감
    driver.maximize_window()
    driver.implicitly_wait(3)
    while True:

        # 팝업 뜰 시에 작동
        # try:
        #     layer_popup = driver.find_element(By.XPATH, '//*[@id="layer_popup_info_0"]')
        #     ActionChains(driver).click(layer_popup.find_element(By.XPATH, '//*[@id="layer_popup_info_0"]/div/a')).perform()
        # except selenium.common.exceptions.NoSuchElementException:
        #     pass # 모달이 없으면 그냥 넘어감
        
        enter_keyword = input("어떤 공공데이터를 찾으시나요? (Done 입력 시에 종료됩니다.): ")
        if enter_keyword:
            if enter_keyword == "Done" or enter_keyword == "done":
                break
            input_keyword = driver.find_element(By.XPATH, '//*[@id="keyword"]')
            ActionChains(driver).send_keys_to_element(input_keyword, enter_keyword).perform()
            driver.find_element(By.XPATH, '//*[@id="searchFrm"]/div[1]/button').send_keys(Keys.ENTER)
            # ActionChains(driver).click(search_btn).send_keys(Keys.ENTER).perform()
            data_cnt = driver.find_element(By.XPATH, '//*[@id="mainTotalCnt"]').get_attribute('innerText')
            file_data_ctn = driver.find_element(By.XPATH, '//*[@id="fileCnt2"]').get_attribute('innerText')
            if ',' in file_data_ctn:
                file_data_ctn = int(file_data_ctn.replace(',', ''))
            api_data_ctn = driver.find_element(By.XPATH, '//*[@id="apiCnt"]').get_attribute('innerText')
            if ',' in api_data_ctn:
                api_data_ctn = int(api_data_ctn.replace(',', ''))
            if data_cnt != '0':
                while True:
                    category_list = driver.find_element(By.XPATH, '//*[@id="contents"]/div[8]')
                    enter_category = input("파일데이터/오픈 API 어떤 유형을 찾으시나요?: ")
                    match enter_category:
                        case '파일데이터':
                            ActionChains(driver).click(category_list.find_element(By.XPATH, '//*[@id="dTypeFILE"]/a')).perform()
                            break
                        case '오픈 API':
                            ActionChains(driver).click(category_list.find_element(By.XPATH, '//*[@id="dTypeAPI"]')).perform()
                            break
                        case _:
                            print("다시 입력해 주세요.")
                if enter_category == "파일데이터":    
                    while True:
                        try:    
                            page_bar = driver.find_element(By.XPATH, '//*[@id="fileDataList"]/nav') 
                            current_page = page_bar.find_element(By.XPATH, '//*[@id="fileDataList"]/nav/strong').get_attribute('innerText')[0]
                            dataList = driver.find_elements(By.CLASS_NAME, 'title')
                            newDataList = []
                            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fileDataList"]/nav')))
                            for data in dataList:
                                if data.tag_name == 'span':
                                    newDataList.append(data.get_attribute("innerText"))
                            print(f'현재 페이지: {current_page}페이지')
                            for index, data in enumerate(newDataList):
                                print(f'{index}: {data}')
                            
                            enter_number = input('어느 데이터를 원하시나요?(index 순서로 적어주세요.)\n\
    (다음을 입력하면 다음 페이지, 이전을 입력하면 이전 페이지로 이동합니다.)\n\
    (처음을 입력하면 처음 페이지, 마지막을 입력하면 마지막 페이지로 갑니다.)\n\
    (전체를 입력하면 외부 데이터를 제외한 보이는 모든 데이터를 다운합니다.)\n\
    (완료를 누르면 목록이 닫힙니다.): ')
                            if enter_number in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                                if len(newDataList) == 1:
                                    try:
                                        data_select = driver.find_element(By.XPATH, f'//*[@id="fileDataList"]/div[2]/ul/li')
                                    except Exception as e:
                                        print(str(e))
                                        continue
                                else:
                                    try:
                                        data_select = driver.find_element(By.XPATH, f'//*[@id="fileDataList"]/div[2]/ul/li[{int(enter_number) + 1}]')
                                    except Exception as e:
                                        print(str(e))
                                        continue
                                    if is_element_present(driver, f'//*[@id="fileDataList"]/div[2]/ul/li[{int(enter_number) + 1}]/div[2]/a'):
                                        download_btn = data_select.find_element(By.XPATH, './/a[contains(@class, "button h32 white")]')
                                        if '바로가기' not in download_btn.text:
                                            ActionChains(driver).click(download_btn).perform()
                                        else:
                                            print('외부 사이트 데이터 다운로드는 지원하지 않습니다.')
                                    else:
                                        driver.get(driver.find_element(By.XPATH, f'//*[@id="fileDataList"]/div[2]/ul/li[{int(enter_number) + 1}]/dl/dt/a'))
                                        
                                        if is_element_present(driver, '//*[@id="contents"]/div[2]/div[1]/div[3]/div/a'):
                                            data_download(driver, '//*[@id="contents"]/div[2]/div[1]/div[3]/div/a')
                                        if is_element_present(driver, '//*[@id="tab-layer-file"]/div[2]/div[2]/a'):
                                            data_download(driver, '//*[@id="tab-layer-file"]/div[2]/div[2]/a')
                                        
                                time.sleep(1)
                            
                            elif enter_number == '전체':
                                if len(newDataList) == 1:
                                    if 'CSV' in driver.find_element(By.XPATH, '//*[@id="fileDataList"]/div[2]/ul/li/dl/dt/a').find_element(By.CLASS_NAME, 'tagset').text:
                                        if is_element_present(driver, f'//*[@id="fileDataList"]/div[2]/ul/li/div[2]/a'):
                                            download_btn = driver.find_element(By.XPATH, f'//*[@id="fileDataList"]/div[2]/ul/li/div[2]/a')
                                            if '바로가기' not in download_btn.text:
                                                ActionChains(driver).click(download_btn).perform()
                                            else:
                                                data_name = driver.find_element(By.XPATH, f'//*[@id="fileDataList"]/div[2]/ul/li/dl/dt/a').find_element(By.CLASS_NAME, 'title').text
                                                print(f'{data_name} 데이터는 외부 사이트에서 다운할 수 있습니다.')
                                        else:
                                            driver.get(driver.find_element(By.XPATH, f'//*[@id="fileDataList"]/div[2]/ul/li/div[2]/a').get_attribute('href'))
                                                
                                            if is_element_present(driver, '//*[@id="contents"]/div[2]/div[1]/div[3]/div/a'):
                                                data_download(driver, '//*[@id="contents"]/div[2]/div[1]/div[3]/div/a')
                                            if is_element_present(driver, '//*[@id="tab-layer-file"]/div[2]/div[2]/a') :
                                                data_download(driver, '//*[@id="tab-layer-file"]/div[2]/div[2]/a')
                                    else:
                                        data_name = driver.find_element(By.XPATH, f'//*[@id="fileDataList"]/div[2]/ul/li/dl/dt/a').find_element(By.CLASS_NAME, 'title').text
                                        print(f"{data_name} 데이터는 CSV 파일이 아닙니다.")
                                else:
                                    for index, _ in enumerate(newDataList):
                                        if 'CSV' in driver.find_element(By.XPATH, f'//*[@id="fileDataList"]/div[2]/ul/li[{int(index) + 1}]/dl/dt/a').find_element(By.CLASS_NAME, 'tagset').text:
                                            if is_element_present(driver, f'//*[@id="fileDataList"]/div[2]/ul/li[{int(index + 1)}]/div[2]/a'):
                                                download_btn = driver.find_element(By.XPATH, f'//*[@id="fileDataList"]/div[2]/ul/li[{int(index) + 1}]/div[2]/a')
                                                if '바로가기' not in download_btn.text:
                                                        ActionChains(driver).click(download_btn).perform()
                                                else:
                                                    data_name = driver.find_element(By.XPATH, f'//*[@id="fileDataList"]/div[2]/ul/li[{int(index) + 1}]/dl/dt/a').find_element(By.CLASS_NAME, 'title').text
                                                    print(f'{data_name} 데이터는 외부 사이트에서 다운할 수 있습니다.')
                                            else:
                                                driver.get(driver.find_element(By.XPATH, f'//*[@id="fileDataList"]/div[2]/ul/li[{int(index) + 1}]/dl/dt/a').get_attribute('href'))
                                                
                                                if is_element_present(driver, '//*[@id="contents"]/div[2]/div[1]/div[3]/div/a'):
                                                    data_download(driver, '//*[@id="contents"]/div[2]/div[1]/div[3]/div/a')
                                                if is_element_present(driver, '//*[@id="tab-layer-file"]/div[2]/div[2]/a') :
                                                    data_download(driver, '//*[@id="tab-layer-file"]/div[2]/div[2]/a')
                                        else:
                                            data_name = driver.find_element(By.XPATH, f'//*[@id="fileDataList"]/div[2]/ul/li[{int(index) + 1}]/dl/dt/a').find_element(By.CLASS_NAME, 'title').text
                                            print(f"{data_name} 데이터는 CSV 파일이 아닙니다.")
                            elif enter_number == '완료':
                                driver.get(url)
                                # if is_element_present(driver, '//*[@id="password-change-modal"]') or is_element_present(driver, '//*[@id="layer_instt_search"]'):
                                #     if driver.find_element(By.XPATH, '//*[@id="password-change-modal"]'):    
                                #         password_change_info_close = driver.find_element(By.XPATH, '//*[@id="password-change-modal"]/a')
                                #         ActionChains(driver).click(password_change_info_close).perform()
                                #     time.sleep(1)
                                #     if driver.find_element(By.XPATH, '//*[@id="layer_instt_search"]'):
                                #         layer_instt_search_close = driver.find_element(By.XPATH, '//*[@id="layer_instt_search"]/a')
                                #         ActionChains(driver).click(layer_instt_search_close).perform()
                                try:
                                    password_change_info_close = driver.find_element(By.XPATH, '//*[@id="password-change-modal"]/a')
                                    ActionChains(driver).click(password_change_info_close).perform()
                                except selenium.common.exceptions.NoSuchElementException:
                                    pass # 모달이 없으면 그냥 넘어감
                                time.sleep(1)
                                    # if driver.find_element(By.XPATH, '//*[@id="layer_instt_search"]'):
                                try:
                                    layer_instt_search_close = driver.find_element(By.XPATH, '//*[@id="layer_instt_search"]/a')
                                    ActionChains(driver).click(layer_instt_search_close).perform()
                                except selenium.common.exceptions.NoSuchElementException:
                                    pass # 모달이 없으면 그냥 넘어감
                                break
                            else:
                                try: 
                                    pages = page_bar.find_elements(By.CSS_SELECTOR, 'a')
                                    new_pages = []
                                    for page in pages:
                                        if '페이지' not in page.get_attribute("innerText"):
                                            new_pages.append(int(page.get_attribute("innerText")))
                                    print(pages[-3].get_attribute('innerText'))
                                    print(new_pages)
                                    match enter_number:
                                        case '처음':
                                            ActionChains(driver).click(pages[0]).perform()
                                        case '마지막':
                                            ActionChains(driver).click(pages[-1]).perform()
                                        case '이전' :
                                            if 1 != current_page:
                                                if (current_page - 1) in new_pages:
                                                    current_page -= 1
                                                    if current_page > 10:
                                                        current_page %= 10
                                                    ActionChains(driver).click(pages[current_page + 1]).perform()
                                                else: 
                                                    ActionChains(driver).click(pages[1]).perform()
                                            else:
                                                print("가장 첫 번째 페이지입니다.")
                                        case '다음':
                                            if (current_page + 1) in new_pages:
                                                if (new_pages[-1] + 1) != (current_page + 1):
                                                    current_page += 1
                                                    if current_page % 10 == 0:
                                                        current_page = pages[-3].text
                                                        ActionChains(driver).click(pages[-3]).perform()
                                                    else:
                                                        ActionChains(driver).click(pages[current_page]).perform()
                                            else:
                                                ActionChains(driver).click(pages[-2]).perform()
                                                if file_data_ctn / 10 != math.floor(file_data_ctn / 10):
                                                    if (file_data_ctn // 10) + 1 == current_page:
                                                        print("가장 마지막 페이지입니다.")
                                                   
                                        case _:
                                            print("이전 또는 다음을 입력해주세요.")
                                except Exception as e:
                                    print(str(e))
                        except Exception as e:
                            print(str(e))
                            
                if enter_category == '오픈 API':
                    while True:
                        try:
                            api_name_list = check_api(driver)
                            time.sleep(1)
                            page_bar = driver.find_element(By.XPATH, '//*[@id="apiDataList"]/nav') 
                            current_page = page_bar.find_element(By.XPATH, '//*[@id="apiDataList"]/nav/strong').get_attribute('innerText')[0]
                            dataList = driver.find_elements(By.CLASS_NAME, 'title')
                            newDataList = []
                            for data in dataList:
                                if data.tag_name == 'span':
                                    newDataList.append(data.get_attribute("innerText"))
                            print(f'현재 페이지: {current_page}페이지')
                            for index, data in enumerate(newDataList):
                                print(f'{index}: {data}')
                            
                            enter_number = input('어느 데이터를 원하시나요?(index 순서로 적어주세요.)\n\
    (다음을 입력하면 다음 페이지, 이전을 입력하면 이전 페이지로 이동합니다.)\n\
    (처음을 입력하면 처음 페이지, 마지막을 입력하면 마지막 페이지로 갑니다.)\n\
    (활용신청 현황을 입력하면 현재 활용신청한 API 목록을 보여줍니다.)\n\
    (완료를 누르면 목록이 닫힙니다.): ')
                            if enter_number in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                                if len(newDataList) == 1:
                                    try:
                                        data_select = driver.find_element(By.XPATH, f'//*[@id="apiDataList"]/div[2]/ul/li')    
                                    except Exception as e:
                                        print(str(e))
                                        continue
                                else:
                                    try:
                                        data_select = driver.find_element(By.XPATH, f'//*[@id="apiDataList"]/div[2]/ul/li[{int(enter_number) + 1}]')
                                    except Exception as e:
                                        print(str(e))
                                download_btn = data_select.find_element(By.XPATH, f'//*[@id="apiDataList"]/div[2]/ul/li[{int(enter_number) + 1}]/div[2]/a')
                                if '바로가기' not in download_btn.text:
                                    ActionChains(driver).click(download_btn).perform()
                                    driver.switch_to.window(driver.window_handles[-1])
                                    if is_alert_present(driver):
                                        try:
                                            alert = driver.switch_to.alert
                                            print(alert.text)
                                            alert.accept()
                                            driver.close()
                                            driver.switch_to.window(driver.window_handles[-1])
                                        except Exception as e:
                                            print(str(e))
                                    else:
                                        while True:
                                            try:
                                                enter_purpose = input('활용목적 입력: ')
                                            except Exception as e:
                                                print(str(e))
                                                print('활용 목적을 다시 입력해주세요.')
                                                continue
                                            if enter_purpose:
                                                break
                                            else:
                                                print("활용 목적을 입력해주세요.")
                                        ActionChains(driver).send_keys_to_element(driver.find_element(By.XPATH, '//*[@id="prcusePurps"]'), enter_purpose).perform()
                                        ActionChains(driver).click(driver.find_element(By.XPATH, '//*[@id="useScopeAgreAt"]')).perform()
                                        ActionChains(driver).click(driver.find_element(By.XPATH, '//*[@id="loadingDiv"]/div[2]/button')).perform()
                                        check_alert(driver)
                                    time.sleep(1)
                                    driver.switch_to.window(driver.window_handles[-1])
                                    api_name_list = check_api(driver)
                                    time.sleep(0.5)
                                else:
                                    print('외부 사이트 데이터 APi 신청은 지원하지 않습니다.')
                                    continue
                                time.sleep(1)
                            elif enter_number == '전체':
                                if len(newDataList) == 1:
                                    try:
                                        data_select = driver.find_element(By.XPATH, f'//*[@id="apiDataList"]/div[2]/ul/li')    
                                    except Exception as e:
                                        print(str(e))
                                        continue
                                    download_btn = data_select.find_element(By.XPATH, f'//*[@id="apiDataList"]/div[2]/ul/li/div[2]/a')
                                    if '바로가기' not in download_btn.text:
                                        ActionChains(driver).click(download_btn).perform()
                                        driver.switch_to.window(driver.window_handles[-1])
                                        if is_alert_present(driver):
                                            try:
                                                alert = driver.switch_to.alert
                                                print(alert.text)
                                                alert.accept()
                                                driver.close()
                                                driver.switch_to.window(driver.window_handles[-1])
                                            except Exception as e:
                                                print(str(e))
                                        else:
                                            while True:
                                                try:
                                                    enter_purpose = '개발 목적' # 수정 가능
                                                except Exception as e:
                                                    print(str(e))
                                                    print('활용 목적을 다시 입력해주세요.')
                                                    continue
                                                if enter_purpose:
                                                    break
                                                else:
                                                    print("활용 목적을 입력해주세요.")
                                            ActionChains(driver).send_keys_to_element(driver.find_element(By.XPATH, '//*[@id="prcusePurps"]'), enter_purpose).perform()
                                            ActionChains(driver).click(driver.find_element(By.XPATH, '//*[@id="useScopeAgreAt"]')).perform()
                                            ActionChains(driver).click(driver.find_element(By.XPATH, '//*[@id="loadingDiv"]/div[2]/button')).perform()
                                            check_alert(driver)
                                            driver.close()
                                        time.sleep(1)
                                        driver.switch_to.window(driver.window_handles[-1])
                                        api_name_list = check_api(driver)
                                        time.sleep(0.5)
                                    else:
                                        print('외부 사이트 데이터 APi 신청은 지원하지 않습니다.')
                                        continue
                                else:
                                    for i, data in enumerate(newDataList):
                                        try:
                                            data_select = driver.find_element(By.XPATH, f'//*[@id="apiDataList"]/div[2]/ul/li[{int(i) + 1}]')
                                        except Exception as e:
                                            print(str(e))
                                            continue
                                        download_btn = data_select.find_element(By.XPATH, f'//*[@id="apiDataList"]/div[2]/ul/li[{int(i) + 1}]/div[2]/a')
                                        if '바로가기' not in download_btn.text:
                                            ActionChains(driver).click(download_btn).perform()
                                            driver.switch_to.window(driver.window_handles[-1])
                                            if is_alert_present(driver):
                                                try:
                                                    alert = driver.switch_to.alert
                                                    print(alert.text)
                                                    alert.accept()
                                                    driver.close()
                                                    driver.switch_to.window(driver.window_handles[-1])
                                                except Exception as e:
                                                    print(str(e))
                                            else:
                                                while True:
                                                    try:
                                                        enter_purpose = '개발 목적' # 수저 가능
                                                    except Exception as e:
                                                        print(str(e))
                                                        print('활용 목적을 다시 입력해주세요.')
                                                        continue
                                                    if enter_purpose:
                                                        break
                                                    else:
                                                        print("활용 목적을 입력해주세요.")
                                                ActionChains(driver).send_keys_to_element(driver.find_element(By.XPATH, '//*[@id="prcusePurps"]'), enter_purpose).perform()
                                                ActionChains(driver).click(driver.find_element(By.XPATH, '//*[@id="useScopeAgreAt"]')).perform()
                                                ActionChains(driver).click(driver.find_element(By.XPATH, '//*[@id="loadingDiv"]/div[2]/button')).perform()
                                                check_alert(driver)
                                                driver.close()
                                            time.sleep(1)
                                            driver.switch_to.window(driver.window_handles[-1])
                                            api_name_list = check_api(driver)
                                            time.sleep(0.5)
                                        else:
                                            print('외부 사이트 데이터 APi 신청은 지원하지 않습니다.')
                                            continue
                            elif enter_number == '완료':
                                driver.get(url)
                                # if is_element_present(driver, '//*[@id="password-change-modal"]') or is_element_present(driver, '//*[@id="layer_instt_search"]'):
                                #     if driver.find_element(By.XPATH, '//*[@id="password-change-modal"]'):    
                                #         password_change_info_close = driver.find_element(By.XPATH, '//*[@id="password-change-modal"]/a')
                                #         ActionChains(driver).click(password_change_info_close).perform()
                                #     time.sleep(1)
                                #     if driver.find_element(By.XPATH, '//*[@id="layer_instt_search"]'):
                                #         layer_instt_search_close = driver.find_element(By.XPATH, '//*[@id="layer_instt_search"]/a')
                                #         ActionChains(driver).click(layer_instt_search_close).perform()
                                try:
                                    password_change_info_close = driver.find_element(By.XPATH, '//*[@id="password-change-modal"]/a')
                                    ActionChains(driver).click(password_change_info_close).perform()
                                except selenium.common.exceptions.NoSuchElementException:
                                    pass # 모달이 없으면 그냥 넘어감
                                time.sleep(1)
                                    # if driver.find_element(By.XPATH, '//*[@id="layer_instt_search"]'):
                                try:
                                    layer_instt_search_close = driver.find_element(By.XPATH, '//*[@id="layer_instt_search"]/a')
                                    ActionChains(driver).click(layer_instt_search_close).perform()
                                except selenium.common.exceptions.NoSuchElementException:
                                    pass # 모달이 없으면 그냥 넘어감
                                break
                            elif enter_number == '활용신청 현황':
                                for index, data in enumerate(api_name_list):
                                    print(f'{index}: {data}')
                            elif enter_number == '다운로드':
                                for index, data in enumerate(api_name_list):
                                    print(f'{index}: {data}')
                                select_number = int(input('데이터를 선택해주세요: '))
                                
                            else:
                                try: 
                                    pages = page_bar.find_elements(By.CSS_SELECTOR, 'a')
                                    new_pages = []
                                    
                                    for page in pages:
                                        if '페이지' not in page.get_attribute("innerText"):
                                            new_pages.append(int(page.get_attribute("innerText")))
                                            
                                    if len(pages) < 13:
                                        print(pages[-1].get_attribute('innerText'))
                                    else:
                                        print(pages[-3].get_attribute('innerText'))
                                        
                                    print(new_pages)
                                    print(current_page)
                                    
                                    match enter_number:
                                        
                                        case '처음':
                                            ActionChains(driver).click(pages[0]).perform()
                                        case '마지막':
                                            ActionChains(driver).click(pages[-1]).perform()
                                        case '이전' :
                                            if len(new_pages) >= 9:
                                                if 1 != current_page:
                                                    if (current_page - 1) in new_pages:
                                                        current_page -= 1
                                                        if current_page > 10:
                                                            current_page %= 10
                                                        ActionChains(driver).click(pages[current_page + 1]).perform()
                                                    else:
                                                        ActionChains(driver).click(pages[1]).perform()
                                                else:
                                                    print("가장 첫 번째 페이지입니다.")
                                                    
                                            else:
                                                if len(new_pages) < 2:
                                                    if (current_page - 1) in new_pages:
                                                        ActionChains(driver).click(pages[0]).perform()
                                                        current_page -= 1
                                                else:
                                                    if (current_page - 1) in new_pages:
                                                        current_page -= 1
                                                        ActionChains(driver).click(pages[current_page - 1]).perform()
                                                    else:
                                                        print("가장 첫 번째 페이지입니다.")
                                                
                                        case '다음':
                                            if len(new_pages) >= 9:
                                                if (current_page + 1) in new_pages:
                                                    if (new_pages[-1] + 1) != (current_page + 1):
                                                        current_page += 1
                                                        if current_page % 10 == 0:
                                                            current_page = pages[-3].text
                                                            ActionChains(driver).click(pages[-3]).perform()
                                                        else:
                                                            ActionChains(driver).click(pages[current_page]).perform()
                                                else:
                                                    ActionChains(driver).click(pages[-2]).perform()
                                                    if file_data_ctn / 10 != math.floor(file_data_ctn / 10):
                                                        if (file_data_ctn // 10) + 1 == current_page:
                                                            print("가장 마지막 페이지입니다.")
                                            else:
                                                if len(pages) < 2:
                                                    if (current_page + 1) in new_pages:
                                                        ActionChains(driver).click(pages[-1]).perform()
                                                        current_page = pages[-1].text
                                                    else:
                                                        print('가장 마지막 페이지입니다.')
                                                else:
                                                    if (current_page + 1) in new_pages:
                                                        current_page += 1
                                                        ActionChains(driver).click(pages[current_page - 2]).perform()
                                                    else:
                                                        print('가장 마지막 페이지입니다.')
                                                    
                                        case _:
                                            print("처음, 마지막, 이전,다음을 입력해주세요.")
                                except Exception as e:
                                    print(str(e))
                        except Exception as e:
                            print(str(e))
                            
            else:
                print("검색 결과가 없습니다. 다른 검색어로 검색해주세요.")
                driver.get(url)
                continue
                    
        else:
            continue            

    
    driver.quit()
    
if __name__ == '__main__':
    search()
    