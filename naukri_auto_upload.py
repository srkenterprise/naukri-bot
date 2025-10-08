# naukri_auto_upload.py
import os, time, traceback, subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
RESUME_PATH = os.path.join(os.getcwd(), "resumes", "SRK_Resume_PO_2025.pdf")
ARTIFACT_DIR = os.path.join(os.getcwd(), "artifacts")
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def print_env_info():
    def run(cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().strip()
            print("CMD:", " ".join(cmd), "=>", out)
        except Exception as e:
            print("CMD:", " ".join(cmd), "=> error:", e)
    print_env = [
        ["python", "--version"],
        ["which", "google-chrome"],
        ["google-chrome", "--version"],
        ["which", "chromedriver"],
        ["chromedriver", "--version"],
    ]
    for c in print_env: run(c)

def save_debug(driver, prefix="failure"):
    try:
        shot = os.path.join(ARTIFACT_DIR, f"{prefix}_screenshot.png")
        page = os.path.join(ARTIFACT_DIR, f"{prefix}_page.html")
        driver.save_screenshot(shot)
        with open(page, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Saved debug artifacts:", shot, page)
    except Exception as e:
        print("Failed to save debug artifacts:", e)

def upload_resume():
    print("🔄 Starting resume upload...")
    print_env_info()

    if not os.path.isfile(RESUME_PATH):
        print("❌ Resume file not found at:", RESUME_PATH)
        # list resume dir for debugging
        print("Contents of cwd:", os.getcwd())
        for root, dirs, files in os.walk(os.path.join(os.getcwd(), "resumes")):
            print("resumes/", root, files)
        raise SystemExit(1)

    options = webdriver.ChromeOptions()
    # binary location fallback (set in workflow too)
    options.binary_location = os.environ.get("CHROME_BIN", "/usr/bin/google-chrome")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())  # auto-download matching chromedriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.naukri.com/nlogin/login")
        print("Opened:", driver.current_url, "| title:", driver.title)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "usernameField"))
        ).send_keys(NAUKRI_EMAIL)
        driver.find_element(By.ID, "passwordField").send_keys(NAUKRI_PASSWORD)
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        print("Clicked login, waiting for profile...")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "View profile"))
        )
        driver.find_element(By.LINK_TEXT, "View profile").click()
        print("Profile opened, waiting for upload input...")

        upload_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        print("Found file input element. Sending resume path:", RESUME_PATH)
        upload_input.send_keys(RESUME_PATH)
        print("📄 Resume upload action performed. Waiting a few seconds...")
        time.sleep(5)
        print("✅ Done (script finished).")

    except Exception:
        traceback.print_exc()
        try:
            save_debug(driver, "failure")
        except Exception as e:
            print("Could not save debug artifacts:", e)
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    upload_resume()
