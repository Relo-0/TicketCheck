import logging
from datetime import datetime
from selenium.webdriver.common.by import By
from utils.web_driver import create_driver, close_driver
from utils.data_loader import load_sites_config
import pandas as pd
import time
from pathlib import Path

# ---------- Logging 設定 ----------
log_path = Path("logs")
log_path.mkdir(exist_ok=True)
log_file = log_path / f"ticketcheck_{datetime.now():%Y%m%d_%H%M%S}.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ---------- 主程式 ----------
def main():
    sites = load_sites_config()
    kktix = sites[0]
    sel = kktix["selectors"]

    driver = create_driver()
    driver.get(kktix["list_url"])
    logging.info(f"載入列表頁：{kktix['list_url']}")

    links = driver.find_elements(By.CSS_SELECTOR, sel["event_links"])
    urls = [link.get_attribute("href") for link in links[:kktix["max_events"]]]
    logging.info(f"擷取 {len(urls)} 筆活動連結")

    results = []
    for url in urls:
        try:
            driver.get(url)
            logging.info(f"解析活動：{url}")

            title = driver.find_element(By.CSS_SELECTOR, sel["title"]).text.strip()
            dates = driver.find_elements(By.CSS_SELECTOR, sel["date_start"])
            date_start = dates[0].text.strip() if len(dates) > 0 else ""
            date_end = dates[-1].text.strip() if len(dates) > 1 else ""

            prices = driver.find_elements(By.CSS_SELECTOR, sel["price"])
            price_list = [p.text.strip() for p in prices]
            price_display = ", ".join(price_list) if price_list else "N/A"

            results.append({
                "title": title,
                "date_start": date_start,
                "date_end": date_end,
                "prices": price_display,
                "url": url
            })

            time.sleep(1)

        except Exception as e:
            # 錯誤處理：紀錄 + 截圖
            logging.error(f"錯誤於 {url}: {e}")
            screenshot_name = f"screenshots/error_{datetime.now():%Y%m%d_%H%M%S}.png"
            Path("screenshots").mkdir(exist_ok=True)
            driver.save_screenshot(screenshot_name)
            logging.info(f"截圖已保存：{screenshot_name}")

    close_driver(driver)

    # 匯出報表
    df = pd.DataFrame(results)
    Path("reports").mkdir(exist_ok=True)
    output_path = Path("reports/kktix_report.xlsx")
    df.to_excel(output_path, index=False)
    logging.info(f"報表已輸出：{output_path}")
    print(f"執行完成，log 檔位於：{log_file}")


if __name__ == "__main__":
    main()
