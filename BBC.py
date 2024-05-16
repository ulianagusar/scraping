import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# код може виконуватись близько 4 годин 

# тут ми посилаєм впошукові запити і збираємо посилання , які видались при пошуку потім
# запиcуєм списки посилань у файли з назвами запитів (для того , щоб якщо пропаде інтернет 
# і тп не пропали отримані резуьтати ) selenium використовується для симулювання 
# дій користувача на сторінках , саме тут для проходу по пагінації (прохід по номерованим сторінкам)
# у випадку з bbc ми не можемо використовувати простий скрабінг , бо від переходу по пагінації не зімінюється url 
# для роботи потрібно встановити драйвер для відповідного браузера і уважно перевіряти версії браузера і драйвера 
# можливо треба буде встановити старішу версію браузера , бо деякі нові версії не підтримуються 
# далі усі файли збираються у файл csv ( to_csv ) , вмдаляються повтори (бо для деякі пошукові запити дають 
# одні й ті самі сайти) а потім уже з кожного окремого посилання на статтю збирається інформація у scrab_article


ukraine = ['ukraine', 'ukrainian', 'kiev', 'kyiv'] 
agro =  [ 'agriculture', 'agricultural', 'agri', 'farm', 'farming', 'farmer', 'grain', 'crop', 'crops', 'plant', 'plants', 'field', 'fields', 'soil', 'land', 'farming', 'crop yield', 'food production', 'agricultural policy'] 


for ag in agro:
    for uk in ukraine   :

        driver = webdriver.Chrome()  

        driver.get(f"https://www.bbc.com/search?q={uk}%20{ag}&edgeauth=eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJrZXkiOiAiZmFzdGx5LXVyaS10b2tlbi0xIiwiZXhwIjogMTcxNTYxOTYwMiwibmJmIjogMTcxNTYxOTI0MiwicmVxdWVzdHVyaSI6ICIlMkZzZWFyY2glM0ZxJTNEdWtyYWluZSUyNTIwYWdyaWN1bHR1cmUifQ.kTfXrpp7YV6WyI7U7g0wcRaAnkoJ1KxAsP7ZS0XOAMU")

        next_page = 2
        res = []
        while True:
            try :
                print(next_page)
                time.sleep(5) 
                # Знаходимо кнопку
                next_page_button = WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'sc-944f9211-1 sc-944f9211-2 hrFvkk fZPXbb') and text()='{next_page}']"))
                )
                links = driver.find_elements(By.TAG_NAME, 'a')
                urls = [link.get_attribute('href') for link in links if link.get_attribute('href') is not None]
                for url in urls :
                    if len(url)>24 and "https://www.bbc.com/news" in url:
                        res.append(url)

                if next_page_button.is_enabled():
                    next_page_button.click()
                    next_page = next_page+1
                else:
                    break
            except TimeoutException as e :
                    links = driver.find_elements(By.TAG_NAME, 'a')
                    urls = [link.get_attribute('href') for link in links if link.get_attribute('href') is not None]
                    for url in urls :
                        if len(url)>24 and "https://www.bbc.com/news" in url:
                            res.append(url)
                    break
        with open(f'{uk}_{ag}.txt', 'w') as file:
                file.write(str(res))
        driver.quit()
        print(res)







