from playwright.sync_api import TimeoutError
from urllib.parse import urljoin



class Controller:
    def __init__(self, page):
        self.page = page


    def accept_cookies(self):
        modal_loc  = self.page.get_by_role("button", name="[I'm ready to pump]")
        accept_loc = self.page.locator('#btn-accept-all')

        for loc in [modal_loc, accept_loc]:
            try:
                loc.click(timeout=3000)
            except TimeoutError:
                pass


    def get_urls(self):
        self.page.locator('[type="button"][role="combobox"][aria-label="Sort"]').click()
        self.page.wait_for_timeout(1000)
        for _ in range(10):
            self.page.locator('ArrowDown')
            self.page.locator('ArrowDown')
            self.page.locator('ArrowDown')
            self.page.locator('ArrowDown')
            self.page.locator('ArrowDown')
            self.page.locator('ArrowDown')
            self.page.keyboard.press('ArrowUp')
            self.page.wait_for_timeout(100)
        self.page.keyboard.press('Enter')

        self.page.locator('[type="button"][role="combobox"][aria-label="Sort"]').click()
        self.page.wait_for_timeout(1000)

        self.page.locator('span', has_text='sort: currently live').click()
        self.page.wait_for_timeout(3000)
        base_url = 'https://pump.fun/'
        items = self.page.locator('.grid.grid-col-1 > a').all()
        urls = [urljoin(base_url, a.get_attribute('href')) for a in items]
        return urls


    def spam_messages(self, messages):
        try:
            input_box = self.page.locator('textarea[data-testid="message-input"]').first
            input_box.wait_for(timeout=5000, state='visible')
        except TimeoutError as e:
            print(f'Timeout error: {e}')
        else:
            for msg in messages:
                input_box.fill(msg)
                input_box.press('Enter')
                self.page.wait_for_timeout(3000)

   # def send_reply(self, text, image_path):
      #  self.page.get_by_text('[Post a reply]').click()
      #  self.page.locator('textarea#text').first.fill(text)
      #  self.page.locator('input#image').set_input_files(image_path)
      #  self.page.wait_for_timeout(2000)
      #  self.page.locator('button', has_text='post reply').click()
