import unittest
from unittest.mock import patch

from driver import SeleniumDriver


class SeleniumDriverTests(unittest.TestCase):
    def test_uses_current_service_api_and_headless_argument(self):
        with patch("driver.os.path.exists", return_value=True):
            scraper = SeleniumDriver(timeout=5)
        self.assertIn("--headless=new", scraper.options.arguments)
        with patch("driver.webdriver.Chrome") as chrome:
            browser = chrome.return_value
            browser.page_source = "<html>result</html>"
            browser.current_url = "https://example.test/"
            result = scraper.get("https://example.test/")
            self.assertEqual(chrome.call_args.kwargs["service"].path, "/usr/bin/chromedriver")
            self.assertIs(chrome.call_args.kwargs["options"], scraper.options)
            self.assertEqual(result.text, "<html>result</html>")
            browser.get.assert_called_once_with("https://example.test/")
            browser.quit.assert_called_once()

    def test_closes_browser_when_navigation_fails(self):
        with patch("driver.os.path.exists", return_value=True):
            scraper = SeleniumDriver(timeout=5)
        with patch("driver.webdriver.Chrome") as chrome:
            chrome.return_value.get.side_effect = RuntimeError("navigation failed")
            with self.assertRaises(RuntimeError):
                scraper.get("https://example.test/")
            chrome.return_value.quit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
