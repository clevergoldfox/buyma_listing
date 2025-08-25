import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import codecs
import re
import os
import random

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
# chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (recommended for headless)
chrome_options.add_argument("--no-sandbox")  # Avoid sandbox issues
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--enable-unsafe-webgpu")
# chrome_options.add_argument("--enable-unsafe-swiftshader")
chrome_options.add_argument("--window-size=1200,900")
# Initialize driver variable but don't create it yet
driver = None
service = None

import unicodedata

def remove_spechar(text):
    # Normalize to NFD (decompose accented characters)
    normalized = unicodedata.normalize('NFD', text)
    # Remove combining marks (accents)
    ascii_only = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return ascii_only

def get_driver():
    """Get or create Chrome WebDriver instance"""
    global driver, service
    if driver is None:
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
        except Exception as e:
            print(f"Failed to create Chrome WebDriver: {e}")
            return None
    return driver

def human_delay(min_seconds=0.5, max_seconds=2.0):
    """Add random delay to simulate human behavior"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def human_typing(element, text, min_delay=0.1, max_delay=0.3):
    """Simulate human typing with random delays between characters"""
    element.click()
    human_delay(0.2, 0.5)
    element.clear()
    human_delay(0.1, 0.3)
    
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))
    
    human_delay(0.3, 0.8)

def human_scroll(driver, scroll_pause=1.0):
    """Simulate human scrolling behavior"""
    # Get page height
    page_height = driver.execute_script("return document.body.scrollHeight")
    
    # Scroll down gradually
    current_position = 0
    while current_position < page_height:
        scroll_amount = random.randint(100, 300)
        current_position += scroll_amount
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        human_delay(0.5, 1.5)
    
    # Sometimes scroll back up a bit
    if random.random() < 0.3:
        driver.execute_script("window.scrollTo(0, arguments[0]);", current_position - random.randint(50, 150))
        human_delay(0.5, 1.0)

def human_mouse_movement(driver, element):
    """Simulate human mouse movement to element (safe version)"""
    actions = ActionChains(driver)
    # Move to the element with a small random offset within the element's bounds
    try:
        location = element.location
        size = element.size
        offset_x = random.randint(1, max(1, size['width'] - 2))
        offset_y = random.randint(1, max(1, size['height'] - 2))
        actions.move_to_element_with_offset(element, offset_x, offset_y)
        actions.perform()
        human_delay(0.2, 0.5)
    except Exception as e:
        print(f"Mouse movement failed: {e}")
        # Fallback: just move to the element
        try:
            actions.move_to_element(element)
            actions.perform()
            human_delay(0.2, 0.5)
        except Exception as e2:
            print(f"Fallback mouse movement also failed: {e2}")

def wait_for_element(driver, by, value, timeout=10):
    """Wait for element with human-like patience"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except:
        print(f"Element not found: {value}")
        return None

def hide_visible_iframes(driver):
    """Hide visible iframes that may intercept clicks (e.g., ads or overlays)."""
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            try:
                style_attr = iframe.get_attribute("style") or ""
                # Skip if already hidden
                if "display: none" in style_attr:
                    continue
                driver.execute_script("arguments[0].style.display='none';", iframe)
            except Exception as e:
                print(f"Could not hide iframe: {e}")
    except Exception as e:
        print(f"Iframe scan failed: {e}")
    
def login(user, login_url=None):
    driver = get_driver()
    if driver is None:
        print("Failed to get Chrome WebDriver")
        return
        
    if login_url:
        driver.get(login_url)
    
    # Wait for page to load
    human_delay(2, 4)
    
    # Simulate human scrolling
    # human_scroll(driver)
    
    email_input = wait_for_element(driver, By.XPATH, '//input[@id="txtLoginId"]')
    if not email_input:
        print("Email input not found")
        return
    
    # Human-like interaction with email field
    human_mouse_movement(driver, email_input)
    email_input.click()
    # email_string = "youdan55@yahoo.co.jp"
    email_string = user['email']
    human_typing(email_input, email_string)
    
    password_input = wait_for_element(driver, By.XPATH, '//input[@id="txtLoginPass"]')
    if not password_input:
        print("Password input not found")
        return
    
    # Human-like interaction with password field
    human_delay(0.5, 1.0)
    human_mouse_movement(driver, password_input)
    password_input.click()
    # password_string = "15791579aA"
    password_string = user["password"]
    human_typing(password_input, password_string)
    
    # Find and click submit button with human behavior
    submit_button = wait_for_element(driver, By.XPATH, '//input[@type="submit" and @id="login_do"]')
    if not submit_button:
        print("Submit button not found")
        return
    
    human_delay(0.5, 1.0)
    human_mouse_movement(driver, submit_button)
    human_delay(0.5, 1.0)
    submit_button.click()
    human_delay(3, 5)

def listing(products, user, logging=None):
    driver = get_driver()
    if driver is None:
        print("Failed to get Chrome WebDriver")
        return
    
    list_url = "https://www.buyma.com/my/sell/new?tab=b"
    driver.get(list_url)
    human_delay(3, 5)
    while len(driver.find_elements(By.XPATH, '//input[@id="txtLoginId"]')) :
        if logging:
            logging("BUYMAサイトにログイン中...")
        login(user)
        human_delay(3, 5)
    
    list_url = "https://www.buyma.com/my/sell/new?tab=b"
    driver.get(list_url)
    
    product_count = len(products)
    
    for index, product in enumerate(products):
        print("========================================")
        print(f"product {index} : {product[8]}")
        print(f"title, {product[1]}")
        print(f"comment, {product[5]}")
        print(f"price, {product[18]}")
        print(f"mount, {product[21]}")
        print(f"color, {product[13]}")
        print(f"size, {product[14]}")
        try:
        # Fix the file path - use raw string and forward slashes
            images = product[25]
            images_path = []
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            driver.execute_script("arguments[0].value = '';", file_input)
            # Collect all valid file paths first
            for image in images:
                # Convert to absolute path and normalize
                image_path = os.path.abspath(image)
            
                # Verify file exists
                if not os.path.exists(image_path):
                    print(f"Error: File not found: {image_path}")
                    return
                
                images_path.append(image_path)
            
            if not file_input:
                print("File input not found")
                return
            
            # Send all file paths as a single string with newline separators
            all_files_path = '\n'.join(images_path)
            file_input.send_keys(all_files_path)

            # Wait until all images are uploaded (wait for thumbnails to appear)
            try:
                # Adjust the XPath to match the image thumbnail elements after upload
                num_images = len(images_path)
                WebDriverWait(driver, 60).until(
                    lambda d: len(d.find_elements(By.XPATH, "//div[contains(@class, 'bmm-c-image-thumb')]")) >= num_images
                )
                print("All images uploaded.")
            except Exception as e:
                print(f"Image upload wait failed: {e}")
            
            # Find and fill title field
            title_input_xpath = "//p[contains(text(), '商品名')]/ancestor::div[contains(@class, 'bmm-l-grid')]//input[@type='text']"
            title_input = wait_for_element(driver, By.XPATH, title_input_xpath)
            if title_input:
                title_input.clear()
                title = remove_spechar(product[1])
                title_input.send_keys(title)
            else:
                print("Title input not found")
            
            comment_input_xpath = "//p[contains(text(), '商品コメント')]/ancestor::div[contains(@class, 'bmm-l-grid')]//textarea[@class='bmm-c-textarea']"
            comment_input = wait_for_element(driver, By.XPATH, comment_input_xpath)
            comment = remove_spechar(product[5])
            if comment_input:
                comment_input.clear()
                comment_input.send_keys(comment)
            else:
                print("comment input not found")

            category = product[4]
            if len(category.split("/")) == 3:
                pre_cat = product[4].split("/")[0]
                mid_cat = product[4].split("/")[1]
                nex_cat = product[4].split("/")[2]
            elif len(category.split("/")) == 2:
                pre_cat = product[4].split("/")[0]
                mid_cat = product[4].split("/")[1]
                nex_cat = ""

            category_input_xpath = "//p[contains(text(), 'カテゴリ')]/ancestor::div[contains(@class, 'bmm-l-grid')]//div[@class='Select-control']"
            category_input = wait_for_element(driver, By.XPATH, category_input_xpath)
            if not category_input:
                print("category input not found")
                return

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category_input)
            human_delay(0.2, 0.5)

            # Try to close overlays/modals if present (uncomment and improve your modal handling code here)

            # Wait for clickable
            try:
                category_input = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, category_input_xpath))
                )
                category_input.click()
            except Exception as e:
                print(f"Normal click failed: {e}, trying JS click")
                driver.execute_script("arguments[0].click();", category_input)

            # Wait for dropdown menu to appear
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='Select-menu-outer']"))
                )
                
                # Debug: Print all available categories
                try:
                    all_categories = driver.find_elements(By.XPATH, "//div[@class='Select-menu-outer']//*[contains(@class, 'Select-option') or contains(@class, 'Select-option')]")
                except Exception as e:
                    print(f"Could not get available categories: {e}")
                    
            except Exception as e:
                print(f"Dropdown menu did not appear: {e}")
                driver.save_screenshot("dropdown_not_appeared.png")
                return

            wait = WebDriverWait(driver, 30)  # wait up to 10 seconds
            
            # Add debugging and better error handling for category selection
            try:                
                # Try multiple XPath patterns to find the category
                xpath_patterns = [
                    f"//div[@class='Select-menu-outer']//p[contains(text(), '{pre_cat}')]",
                    f"//div[@class='Select-menu-outer']//*[contains(text(), '{pre_cat}')]",
                    f"//div[@class='Select-menu-outer']//div[contains(text(), '{pre_cat}')]",
                    f"//div[@class='Select-menu-outer']//span[contains(text(), '{pre_cat}')]",
                    f"//div[@class='Select-menu-outer']//*[normalize-space()='{pre_cat}']"
                ]
                
                pre_cat_value_tag = None
                for i, xpath in enumerate(xpath_patterns):
                    try:
                        pre_cat_value_tag = wait.until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                        )
                        break
                    except Exception as e:
                        print(f"Pattern {i+1} failed: {e}")
                        continue
                
                if pre_cat_value_tag:
                    pre_cat_value_tag.click()
                else:
                    print(f"All patterns failed for category: {pre_cat}")
                    driver.save_screenshot(f"category_error_{pre_cat}.png")
                    return
                    
            except Exception as e:
                print(f"Failed to find category '{pre_cat}': {e}")
                driver.save_screenshot(f"category_error_{pre_cat}.png")
                return

            cat_divs = driver.find_elements(By.XPATH, category_input_xpath)
            while len(cat_divs) < 2:
                cat_divs = driver.find_elements(By.XPATH, category_input_xpath)
                time.sleep(1)

            try:
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable(cat_divs[1])).click()
            except Exception as e:
                print(f"Failed to click second category dropdown: {e}")
                return

            wait = WebDriverWait(driver, 30)

            try:
                mid_cat_value_tag = wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        f'//div[@class="Select-menu-outer"]//*[contains(text(), "{mid_cat}")]'
                    ))
                )
                mid_cat_value_tag.click()
            except Exception as e:
                print(f"Failed to find subcategory '{mid_cat}': {e}")
                driver.save_screenshot(f"subcategory_error_{mid_cat}.png")
                return

            if nex_cat:
                cat_divs = driver.find_elements(By.XPATH, category_input_xpath)
                while len(cat_divs) < 3:
                    cat_divs = driver.find_elements(By.XPATH, category_input_xpath)
                    time.sleep(1)

                time.sleep(1)

                try:
                    # Switch to default content to avoid iframe interference
                    driver.switch_to.default_content()
                    
                    # Hide iframes that could overlay the control
                    hide_visible_iframes(driver)

                    # Wait for element to be clickable
                    third_cat_element = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable(cat_divs[2])
                    )
                    
                    # Scroll into view with offset to avoid iframe
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", third_cat_element)
                    human_delay(0.5, 1.0)
                    
                    # Try normal click first, then JavaScript click as fallback
                    try:
                        third_cat_element.click()
                    except Exception as e:
                        print(f"Normal click failed: {e}, trying JS click")
                        driver.execute_script("arguments[0].click();", third_cat_element)
                        
                    wait = WebDriverWait(driver, 30)

                    try:
                        nex_cat_value_tag = wait.until(
                            EC.presence_of_element_located((
                                By.XPATH,
                                f'//div[@class="Select-menu-outer"]//*[contains(text(), "{nex_cat}")]'
                            ))
                        )
                        nex_cat_value_tag.click()
                    except Exception as e:
                        print(f"Failed to find subcategory '{nex_cat}': {e}")
                        driver.save_screenshot(f"subcategory_error_{nex_cat}.png")
                        return

                except Exception as e:
                    print(f"Failed to click third category dropdown: {e}")
                    return

            # Find and fill brand field
            brand=""
            match = re.match(r'^([a-zA-Z ]+)', product[2])
            if match:
                brand = match.group(1).strip().upper()
            brand_input_xpath = "//p[contains(text(), 'ブランド')]/ancestor::div[contains(@class, 'bmm-l-grid')]//input[@type='text']"
            brand_input = wait_for_element(driver, By.XPATH, brand_input_xpath)
            if brand_input:
                brand_input.clear()
                brand_input.send_keys(brand)
            else:
                print("brand input not found")

            season_input_xpath = "//p[contains(text(), 'シーズン')]/ancestor::div[contains(@class, 'bmm-l-grid')]//div[@class='Select-control']"
            season_input = wait_for_element(driver, By.XPATH, season_input_xpath)
            if not season_input:
                print("season input not found")
                return

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", season_input)
            human_delay(0.2, 0.5)

            # Try to close overlays/modals if present (uncomment and improve your modal handling code here)

            # Wait for clickable
            try:
                season_input = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, season_input_xpath))
                )
                season_input.click()
            except Exception as e:
                print(f"Normal click failed: {e}, trying JS click")
                driver.execute_script("arguments[0].click();", season_input)
            # time.sleep(5)
            season = product[15]
            wait = WebDriverWait(driver, 30)  # wait up to 10 seconds

            season_value_tag = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f"//div[@class='Select-menu-outer']//*[contains(text(), '{season}')]"
                ))
            )
            season_value_tag.click()

            # time.sleep(10)
            
            tag = product[16]
            pre_tag = tag.split(">")[0]
            nex_tag = tag.split(">")[1]
            tag_input_xpath = "//p[@class='bmm-c-summary__ttl' and contains(text(), 'タグ')]/ancestor::div[contains(@class, 'bmm-l-grid')]//i[contains(@class, 'bmm-c-ico-list-search')]"

            wait = WebDriverWait(driver, 30)
            tag_input_tag = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    tag_input_xpath
                ))
            )
            # tag_input_tag = driver.find_element(By.XPATH, tag_input_xpath)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tag_input_tag)
            time.sleep(0.3)  # let animation complete
            tag_input_tag.click()        

            tag_xpath = f'//label[@class="bmm-c-checkbox bmm-c-checkbox--tag"][.//span[normalize-space()="{nex_tag}"]]//input[@type="checkbox"]'

            try:
                tag_check = wait.until(EC.presence_of_element_located((By.XPATH, tag_xpath)))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tag_check)
                driver.execute_script("arguments[0].click();", tag_check)
            except Exception as e:
                print(f"Failed to click checkbox for tag '{nex_tag}':", e)
                driver.save_screenshot("tag_checkbox_error.png")
            
            tag_sub_btn = driver.find_element(By.XPATH, '//button[text()="選択したタグを設定"]')  
            tag_sub_btn.click()

            color_sel_btn = driver.find_element(By.XPATH, '//li[contains(@class, "sell-variation__tab-item") and contains(text(), "色")]')
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", color_sel_btn)
                color_sel_btn.click()
            except Exception as e:
                print("Normal click failed, using JS click instead:", e)
                driver.execute_script("arguments[0].click();", color_sel_btn)
            
            color = product[13]
            color_sel_sel = driver.find_element(By.XPATH, '//div[@class="sell-color-option"]')
            color_sel_sel.click()
            
            wait = WebDriverWait(driver, 30)
            if not color == "色指定なし":
                color_value_tag = wait.until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        f'//div[@class="Select-menu-outer"]//*[contains(text(), "{color}")]'
                    ))
                )
                color_value_tag.click()
            
                color_name_input = driver.find_element(
                    By.XPATH,
                    "//p[contains(text(), '色・サイズ')]/ancestor::div[contains(@class, 'bmm-l-grid')]//input[@type='text' and contains(@class, 'bmm-c-text-field')]"
                )
                color_name_input.clear()
                color_name_input.send_keys(color)
            
            size = product[14]
            size_sel_btn = driver.find_element(By.XPATH, '//li[contains(@class, "sell-variation__tab-item") and contains(text(), "サイズ")]')
            size_sel_btn.click()
            
            size_sel_sel = driver.find_element(By.XPATH, "//p[contains(text(), '色・サイズ')]/ancestor::div[contains(@class, 'bmm-l-grid')]//div[contains(@class, 'Select-control')]")
            size_sel_sel.click()
            
            wait = WebDriverWait(driver, 30)

            size_value_tag = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f'//div[@class="Select-menu-outer"]//*[contains(text(), "バリエーションあり")]'
                ))
            )
            size_value_tag.click()
            
            wait = WebDriverWait(driver, 30)

            size_name_input = wait.until(EC.presence_of_element_located((
                By.XPATH,
                "//p[contains(text(), '色・サイズ')]/ancestor::div[contains(@class, 'bmm-l-grid')]//input[@type='text' and contains(@class, 'bmm-c-text-field')]"
            )))
            
            if size_name_input:
                size_name_input.clear()
                size_name_input.send_keys(size)
            else:
                print("Not found size_name_input")
            
            mount = product[21]
            mount_input = driver.find_element(By.XPATH, '//div[@class="sell-amount-input"]//input[@type="text"]')
            mount_input.clear()
            mount_input.send_keys(mount)
            
            # sellday = product[]
            # sellday = 20
            
            # sellday_input_xpath = '//p[contains(@class, "sell-buying-schedule-edit-link")]//i[contains(@class, "bmm-c-ico-pencil")]'
            
            # wait = WebDriverWait(driver, 30)
            # sellday_input_tag = wait.until(
            #     EC.presence_of_element_located((
            #         By.XPATH,
            #         sellday_input_xpath
            #     ))
            # )
            # # tag_input_tag = driver.find_element(By.XPATH, tag_input_xpath)
            # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sellday_input_tag)
            # time.sleep(0.3)  # let animation complete
            # sellday_input_tag.click()
            
            # sellday_xpath = f'//input[@type="number" and @name="daysToBuying"]'
            # sellday_input = wait.until(EC.presence_of_element_located((By.XPATH, sellday_xpath)))

            # sellday_input.send_keys(Keys.CONTROL + "a")  # Select all
            # sellday_input.send_keys(Keys.DELETE)         # Delete
            # sellday_input.send_keys(sellday)
            
            # sellday_sub_btn = driver.find_element(By.XPATH, '//button[text()="設定する"]')  
            # sellday_sub_btn.click()

            
            checkbox = driver.find_element(By.XPATH, '//tr[.//p[contains(text(), "DHL EXPRESS")]]//input[@type="checkbox"]')
            driver.execute_script("arguments[0].click();", checkbox)

            # time.sleep(5)

            
            list_limit = product[7]
            list_limit_input_xpath = "//p[contains(text(), '購入期限(日本時間)')]/ancestor::div[contains(@class, 'bmm-l-grid')]//input[@type='text']"
            wait = WebDriverWait(driver, 30)
            list_limit_input = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    list_limit_input_xpath
                ))
            )

            driver.execute_script(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                list_limit_input,
                list_limit
            )

            # time.sleep(3)
            
            purchase_location = product[9]
            purchase_arr = purchase_location.split(">")
            purchase_country = purchase_arr[0]
            purchase_province = purchase_arr[1]
            
            if purchase_country == "日本":
                purchase_location_sel_xpath = "//p[contains(text(), '買付地')]/ancestor::div[contains(@class, 'bmm-c-panel__item')]//input[@type='radio' and @value='domestic']"
                sel_country = purchase_province
            else:
                purchase_location_sel_xpath = "//p[contains(text(), '買付地')]/ancestor::div[contains(@class, 'bmm-c-panel__item')]//input[@type='radio' and @value='overseas']"
                sel_country = purchase_country
            wait = WebDriverWait(driver, 30)
        
            purchase_location_sel = driver.find_element(By.XPATH, purchase_location_sel_xpath)        
            time.sleep(1)
            if not purchase_location_sel.is_selected():
                driver.execute_script("arguments[0].click();", purchase_location_sel)  # JS fallback
                # purchase_location_sel.click()
            
            purchase_sel_xpath = "//p[contains(text(), '買付地')]/ancestor::div[contains(@class, 'bmm-c-panel__item')]//div[@class='Select-control']"
            purchase_sel = wait_for_element(driver, By.XPATH, purchase_sel_xpath)
            if not purchase_sel:
                print("purchase_sel not found")
                return

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", purchase_sel)
            human_delay(0.2, 0.5)

            # Try to close overlays/modals if present (uncomment and improve your modal handling code here)

            # Wait for clickable
            try:
                purchase_sel = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, purchase_sel_xpath))
                )
                purchase_sel.click()
            except Exception as e:
                print(f"Normal click failed: {e}, trying JS click")
                driver.execute_script("arguments[0].click();", purchase_sel)
            
            wait = WebDriverWait(driver, 30)  # wait up to 10 seconds

            purchase_country_value_tag = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f"//div[@class='Select-menu-outer']//div[contains(text(), '{sel_country}')]"
                ))
            )
            purchase_country_value_tag.click()
            
            # time.sleep(2)
            purchase_divs = driver.find_elements(By.XPATH, purchase_sel_xpath)
            if not purchase_country == "日本":
                sel_count = 1
                while len(purchase_divs) < len(purchase_arr):
                    purchase_divs = driver.find_elements(By.XPATH, purchase_sel_xpath)
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(purchase_divs[-1])).click()
                    wait = WebDriverWait(driver, 30)

                    value_tag = wait.until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            f'//div[@class="Select-menu-outer"]//*[contains(text(), "{purchase_arr[sel_count]}")]'
                        ))
                    )
                    value_tag.click()
                    sel_count += 1
                    
                    
            delivery_location = product[11]
            delivery_arr = delivery_location.split(">")
            delivery_country = delivery_arr[0]
            delivery_province = delivery_arr[1]
            
            
            if delivery_country == "日本":
                delivery_location_sel_xpath = "//p[contains(text(), '発送地')]/ancestor::div[contains(@class, 'bmm-c-panel__item')]//input[@type='radio' and @value='domestic']"
                sel_country = delivery_province
            else:
                delivery_location_sel_xpath = "//p[contains(text(), '発送地')]/ancestor::div[contains(@class, 'bmm-c-panel__item')]//input[@type='radio' and @value='overseas']"
                sel_country = delivery_country
            wait = WebDriverWait(driver, 30)
            # delivery_location_sel = wait.until(
            #     EC.element_to_be_clickable((By.XPATH, delivery_location_sel_xpath))
            # )
            
            delivery_location_sel = driver.find_element(By.XPATH, delivery_location_sel_xpath)
            
            # wait = WebDriverWait(driver, 30)
            # delivery_location_sel = wait.until(EC.element_to_be_clickable((By.XPATH, delivery_location_sel_xpath)))

            # driver.execute_script("arguments[0].scrollIntoView(true);", delivery_location_sel)
            time.sleep(1)
            if not delivery_location_sel.is_selected():
                driver.execute_script("arguments[0].click();", delivery_location_sel)  # JS fallback
                # delivery_location_sel.click()
            
            delivery_sel_xpath = "//p[contains(text(), '発送地')]/ancestor::div[contains(@class, 'bmm-c-panel__item')]//div[@class='Select-control']"
            delivery_sel = wait_for_element(driver, By.XPATH, delivery_sel_xpath)
            if not delivery_sel:
                print("delivery_sel not found")
                return

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delivery_sel)
            human_delay(0.2, 0.5)

            # Try to close overlays/modals if present (uncomment and improve your modal handling code here)

            # Wait for clickable
            try:
                delivery_sel = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, delivery_sel_xpath))
                )
                delivery_sel.click()
            except Exception as e:
                print(f"Normal click failed: {e}, trying JS click")
                driver.execute_script("arguments[0].click();", delivery_sel)
            
            wait = WebDriverWait(driver, 30)  # wait up to 10 seconds

            delivery_country_value_tag = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f"//div[@class='Select-menu-outer']//div[contains(text(), '{sel_country}')]"
                ))
            )
            # html_code = delivery_country_value_tag.get_attribute("outerHTML")
            # print("delivery_country_value_tag HTML:", html_code)
            delivery_country_value_tag.click()
            
            # time.sleep(2)
            delivery_divs = driver.find_elements(By.XPATH, delivery_sel_xpath)
            if not delivery_country == "日本":
                sel_count = 1
                while len(delivery_divs) < len(delivery_arr):
                    delivery_divs = driver.find_elements(By.XPATH, delivery_sel_xpath)
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(delivery_divs[-1])).click()
                    wait = WebDriverWait(driver, 30)

                    value_tag = wait.until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            f'//div[@class="Select-menu-outer"]//*[contains(text(), "{delivery_arr[sel_count]}")]'
                        ))
                    )
                    value_tag.click()
                    sel_count += 1
                
            
                
            price = int(product[18])
            price_input_xpath = "//p[contains(text(), '商品価格')]/ancestor::div[contains(@class, 'bmm-l-grid')]//input[@type='text']"
            price_input = wait_for_element(driver, By.XPATH, price_input_xpath)
            price_input.clear()
            price_input.send_keys(price)
            
            duties = product[23]
            duties_check_xpath = "//label[.//span[text()='関税込み (購入者の関税負担なし)']]//input[@type='checkbox']"
            duties_check = wait_for_element(driver, By.XPATH, duties_check_xpath)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, duties_check_xpath)))
            # duties_check = driver.find_element(By.XPATH, duties_check_xpath)
            if duties == "お客様負担":
                if not duties_check.is_selected():
                    driver.execute_script("arguments[0].scrollIntoView(true);", duties_check)
            else:
                if duties_check.is_selected():
                    driver.execute_script("arguments[0].click();", duties_check)

        # Use JS click if needed
                    
            list_memo = product[24]
            list_memo_xpath = "//p[contains(text(), '出品メモ')]/ancestor::div[contains(@class, 'bmm-l-grid')]//textarea[@class='bmm-c-textarea']"
            list_memo_input = wait_for_element(driver, By.XPATH, list_memo_xpath)
            if list_memo_input:
                list_memo_input.clear()
                list_memo_input.send_keys(list_memo)
            else:
                print("list_memo input not found")
                
            buyer_name_input_xpath = "//span[text()='買付先名']/preceding-sibling::input[@type='text']"
            buyer_name_input = wait_for_element(driver, By.XPATH, buyer_name_input_xpath)
            if buyer_name_input:
                buyer_name_input.clear()
                buyer_name_input.send_keys("TESSABIT")
            else:
                print("buyer_name input not found")
                
            buyer_url_input_xpath = "//span[text()='URL']/preceding-sibling::input[@type='text']"
            buyer_url_input = wait_for_element(driver, By.XPATH, buyer_url_input_xpath)
            if buyer_url_input:
                buyer_url_input.clear()
                buyer_url_input.send_keys("https://www.buyma.com/my/sell/new?tab=b")
            else:
                print("buyer_url input not found")
                
            regist_btn = driver.find_element(By.XPATH, '//button[text()="入力内容を確認する"]')
            regist_btn.click()
            
            config_btn_xpath = "//button[text()='注意事項に同意して公開する']"
            config_btn = wait_for_element(driver, By.XPATH, config_btn_xpath)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, config_btn_xpath)))
            
            if config_btn:
                config_btn.click()
            else:
                print("Not found Config btn")
                
            continue_btn_xpath = "//button[text()='続けて出品する']"
            continue_btn = wait_for_element(driver, By.XPATH, continue_btn_xpath)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, continue_btn_xpath)))
            
            if logging:
                logging(f"{product_count}個中{index+1}個出品完了、完了率{round((index+1)/product_count * 100, 2)}%")
            
            if continue_btn:
                continue_btn.click()
            else:
                print("Not found Config btn")
            
            print("Listing process completed")
        except Exception as e:
            print(f"Error in listing process: {e}")
            if logging:
                logging(f"Error in listing process: {e}")
            continue
