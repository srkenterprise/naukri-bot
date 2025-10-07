from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import subprocess

def install_chrome():
    subprocess.run(["sudo", "apt-get", "update"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "google-chrome-stable"], check=True)

def upload_resume():
    print("🔄 Installing Chrome...")
    install_chrome()

    print("🚀 Starting resume upload...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.naukri.com/nlogin/login")

    email = os.getenv("NAUKRI_EMAIL")
    password = os.getenv("NAUKRI_PASSWORD")

    print("🧠 Logging in...")
    driver.find_element(By.ID, "usernameField").send_keys(email)
    driver.find_element(By.ID, "passwordField").send_keys(password)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()

    time.sleep(5)
    print("✅ Logged in successfully!")

    # Example: Go to profile page (update this URL if needed)
    driver.get("https://www.naukri.com/mnjuser/profile")

    time.sleep(5)
    print("📄 Resume upload simulated successfully!")

    driver.quit()

if __name__ == "__main__":
    upload_resume()
