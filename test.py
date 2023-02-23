from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Pool
import time
import pytest
import datetime

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

@pytest.fixture
def context():
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://qa.putraprima.id/")
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.new_release
def test_new_release(context):
    current_year = context.find_element(By.CSS_SELECTOR, "#year").getText()
    assert current_year == str(datetime.datetime.now().year), "Tahun tidak sesuai dengan tahun yang diharapkan (2023)"

    time.sleep(5)

@pytest.mark.success_hitung
def test_success_hitung(context):
    input = context.find_element(By.ID, "input")
    input.send_keys('5')
    hitung = context.find_element(By.ID, 'hitung')
    hitung.click()
    time.sleep(3)

    assert "Faktorial dari" in context.find_element(By.ID, 'result').text
    time.sleep(5)

@pytest.mark.failed_hitung
def test_failed_hitung(context):
    input = context.find_element(By.ID, "input")
    input.send_keys('a')
    hitung = context.find_element(By.ID, 'hitung')
    hitung.click()
    time.sleep(3)

    assert "Please enter an integer" in context.find_element(By.ID, 'result').text
    time.sleep(5)


@pytest.mark.link_text1
def test_link_text1(context):
    Terms_Of_Service = context.find_element(By.LINK_TEXT, 'Terms Of Service')
    Terms_Of_Service.click()
    time.sleep(5)
    assert "Faktorial" in context.title

@pytest.mark.link_text2
def test_link_text2(context):
    Privacy_Policy = context.find_element(By.LINK_TEXT, 'Privacy Policy')
    Privacy_Policy.click()
    time.sleep(5)
    assert "Faktorial" in context.title
    
@pytest.mark.load
def test_load(context):
    page_load_time = context.execute_script("return (window.performance.timing.loadEventEnd - window.performance.timing.navigationStart);")
    threshold = 5000
    assert page_load_time < threshold, f"Page load time ({page_load_time}ms) exceeded threshold ({threshold}ms)"

    if page_load_time > threshold:
        raise AssertionError(f"Page load time ({page_load_time}ms) exceeded threshold ({threshold}ms). Halaman mungkin mengalami masalah atau koneksi internet Anda mungkin lambat.")


