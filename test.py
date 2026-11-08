# Добавляем зависимости


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Указываем где находится ChromeDriver (наш Dockerfile уже скачал его)
chromedriver_path = "/usr/bin/chromedriver"

# Опции для Chrome
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')  # Ignores certificate errors
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')  # Bypass OS security model; often necessary on Linux
options.add_argument('--window-size=1920,1080')   # запятая вместо x
options.add_argument('--start-maximized')         # подстраховка

# Инициализация Driver
s = Service(chromedriver_path)
driver = webdriver.Chrome(service=s, options=options)
wait = WebDriverWait(driver, 10)

# Открыть страницу
driver.get("http://qa-stand-login.inzhenerka.tech/login")
# Напечатать название страницы
print(driver.title)


wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("admin")
wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys("admin123")

button = driver.find_element(By.XPATH, "//button[contains(., 'Войти')]")
print("окно:", driver.get_window_size())
print("кнопка:", button.rect)

print(driver.execute_script(
    "const r = arguments[0].getBoundingClientRect();"
    "const el = document.elementFromPoint(r.x + r.width/2, r.y + r.height/2);"
    "return el ? el.outerHTML.slice(0, 200) : 'null';", button
))

# Ждём, пока кнопка реально станет кликабельной
button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[normalize-space()='Войти']")
))
button.click()

# Ждём перехода/приветствия
wait.until(EC.presence_of_element_located((By.XPATH, "//h2[1]")))
print(driver.find_element(By.XPATH, "//h2[1]").text)

# Держать браузер открытым после завершения теста (например, 10 секунд)
time.sleep(5)
print('OK')

# Закрыть окно браузера
driver.quit()