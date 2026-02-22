import time
import urllib.parse
from skills.base_skill import BaseSkill


class WhatsAppSkill(BaseSkill):
    intent = "whatsapp"

    def __init__(self):
        self.driver = None
        self.wait = None

    # --------------------------------------------------
    # Browser Initialization (LAZY)
    # --------------------------------------------------
    def _init_browser(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.common.by import By

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-data-dir=F:/python/moon0.2/whatsapp_session")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 40)

        self.driver.get("https://web.whatsapp.com")

        print("Scan QR if required...")
        self.wait.until(EC.presence_of_element_located((By.ID, "pane-side")))
        print("WhatsApp Ready.")

    def _ensure_driver(self):
        if self.driver is None:
            print("Launching WhatsApp Web...")
            self._init_browser()

    def _safe_sleep(self, t=2):
        time.sleep(t)

    # --------------------------------------------------
    # COMMAND ROUTER
    # --------------------------------------------------
    def handle(self, text, player):
        text_lower = text.lower()

        if "whatsapp" not in text_lower:
            return False, None

        self._ensure_driver()

        try:
            # SEND MESSAGE
            if "send" in text_lower:
                number, message = self._extract_details(text_lower)
                self._send_message(number, message)
                return True, f"Message sent to {number}"

            # UNREAD COUNT
            elif "read unread" in text_lower or "unread" in text_lower:
                count = self._get_unread_chats()
                return True, f"You have {count} unread chats"

            # READ LAST MESSAGE
            elif "read last message from" in text_lower:
                name = text_lower.split("from")[1].strip()
                msg = self._read_last_message(name)
                return True, f"Last message from {name}: {msg}"

            else:
                return True, "WhatsApp command unclear"

        except Exception as e:
            return True, f"WhatsApp error: {str(e)}"

    # --------------------------------------------------
    # EXTRACT DETAILS
    # --------------------------------------------------
    def _extract_details(self, text):
        if "to" not in text or "message" not in text:
            raise ValueError("Format: send whatsapp to <number> message <text>")

        number = text.split("to")[1].split("message")[0].strip()
        message = text.split("message")[1].strip()
        return number, message

    # --------------------------------------------------
    # SEND MESSAGE (ENTER METHOD)
    # --------------------------------------------------
    def _send_message(self, number, message):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC

        encoded = urllib.parse.quote(message)
        url = f"https://web.whatsapp.com/send?phone={number}&text={encoded}"
        self.driver.get(url)

        # wait for message box
        input_box = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            )
        )

        self._safe_sleep(2)

        # press enter to send
        input_box.send_keys("\n")

    # --------------------------------------------------
    # UNREAD COUNT
    # --------------------------------------------------
    def _get_unread_chats(self):
        from selenium.webdriver.common.by import By

        unread = self.driver.find_elements(
            By.XPATH, '//span[contains(@aria-label,"unread")]'
        )
        return len(unread)

    # --------------------------------------------------
    # READ LAST MESSAGE
    # --------------------------------------------------
    def _read_last_message(self, contact_name):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC

        # search box
        search_box = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@title="Search input textbox"]')
            )
        )

        search_box.click()
        search_box.send_keys("\u0001")  # select all
        search_box.send_keys("\u0008")  # delete
        search_box.send_keys(contact_name)

        self._safe_sleep(2)

        chat = self.driver.find_element(By.XPATH, f'//span[@title="{contact_name}"]')
        chat.click()

        self._safe_sleep(2)

        messages = self.driver.find_elements(
            By.XPATH, '//div[contains(@class,"message-in")]//span[@dir="ltr"]'
        )

        if messages:
            return messages[-1].text
        return "No message found"
