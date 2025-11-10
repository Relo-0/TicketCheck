from utils.web_driver import create_driver, close_driver
from utils.data_loader import load_sites_config
from selenium.webdriver.common.by import By
import pandas as pd
import time


def main():
    sites = load_sites_config()
    kktix = sites[0]  # 目前只用 KKTIX
    sel = kktix["selectors"]

    driver = create_driver()
    driver.get(kktix["list_url"])
    print(f"載入：{kktix['list_url']}")

    links = driver.find_elements(By.CSS_SELECTOR, sel["event_links"])
    urls = [link.get_attribute("href") for link in links[:kktix["max_events"]]]
    print(f"共擷取 {len(urls)} 筆活動：\n")

    results = []
    for url in urls:
        try:
            driver.get(url)
            print(f"解析活動：{url}")

            title = driver.find_element(By.CSS_SELECTOR, sel["title"]).text.strip()

            # 日期（可能有兩個 span.timezoneSuffix）
            dates = driver.find_elements(By.CSS_SELECTOR, sel["date_start"])
            date_start = dates[0].text.strip() if len(dates) > 0 else ""
            date_end = dates[-1].text.strip() if len(dates) > 1 else ""

            # 票價（有多個 span.currency-value）
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

            time.sleep(1)  # 稍微延遲，避免被判定爬蟲
        except Exception as e:
            print("抓取錯誤：", e)

    close_driver(driver)

    # 輸出報表
    df = pd.DataFrame(results)
    output_path = "reports/kktix_report.xlsx"
    df.to_excel(output_path, index=False)
    print(f"\n報表已輸出：{output_path}")


if __name__ == "__main__":
    main()
