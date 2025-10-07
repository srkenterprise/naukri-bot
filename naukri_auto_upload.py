import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Config ---
NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
RESUME_PATH = os.path.join(os.getcwd(), "resumes", "SRK_Resume_PO_2025.pdf")
def upload_resume():
    print("🔄 Starting resume upload...")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.naukri.com/nlogin/login")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "usernameField"))
        ).send_keys(NAUKRI_EMAIL)

        driver.find_element(By.ID, "passwordField").send_keys(NAUKRI_PASSWORD)
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.LINK_TEXT, "View profile"))
        ).click()

        # --- Upload resume ---
        upload_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        upload_input.send_keys(RESUME_PATH)  # ✅ now using correct path

        print("✅ Resume uploaded successfully!")
        time.sleep(5)

    except Exception as e:
        print("❌ Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    upload_resume()
