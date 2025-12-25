# TicketCheck

一個基於 **Python + Selenium** 的票務活動檢查工具，  
可自動擷取 **KKTIX** 活動列表中的販售中活動，解析活動頁資訊，並生成 Excel 報表，同時記錄 log 與錯誤截圖。

---

## 功能特點

- ✅ 自動擷取 KKTIX 販售中活動連結  
- ✅ 解析活動頁資訊（標題、日期、票價）  
- ✅ 支援多筆票價顯示（合併輸出）  
- ✅ 自動生成 Excel 報表  
- ✅ log 紀錄（含時間戳）  
- ✅ 發生錯誤時自動截圖保存  
- ✅ 設定檔（JSON）可調整 selector 與抓取數量  

---

## 專案結構

```
TicketCheck/
├── main.py                  # 主程式入口
├── requirements.txt         # Python 依賴套件
├── config/
│   └── sites.json           # 站台與 selector 設定檔
├── utils/
│   ├── web_driver.py        # Selenium Driver 建立與關閉
│   └── data_loader.py       # 設定檔讀取工具
├── reports/
│   └── kktix_report.xlsx    # 檢查結果報表（自動生成）
├── logs/
│   └── ticketcheck_*.log    # 執行 log
└── screenshots/
    └── error_*.png          # 錯誤截圖
```

---

## 安裝步驟

### 1. Clone 專案

```bash
git clone https://github.com/Relo-0/TicketCheck.git
cd TicketCheck
```

### 2. 安裝依賴套件

```bash
pip install -r requirements.txt
```

> ⚠️ 需事先安裝可用的 Selenium WebDriver（如 ChromeDriver），並確保版本與瀏覽器相容。

---

## 配置活動設定

編輯 `config/sites.json`，目前主程式只會使用第一個站台設定：

```json
{
  "sites": [
    {
      "name": "KKTIX",
      "list_url": "https://kktix.com/events",
      "selectors": {
        "event_links": "li.type-selling a.cover",
        "title": "div.header-title h1",
        "date_start": "span.timezoneSuffix:first-of-type",
        "date_end": "span.timezoneSuffix:last-of-type",
        "price": "td.price span.price"
      },
      "max_events": 8,
      "note": "只抓販售中活動，最多8筆"
    }
  ]
}
```

---

## 使用方法

### 執行檢查

```bash
python main.py
```

---

## 輸出結果

### Excel 報表

- `reports/kktix_report.xlsx`

### Log 檔

- `logs/ticketcheck_YYYYMMDD_HHMMSS.log`

### 錯誤截圖

- `screenshots/error_YYYYMMDD_HHMMSS.png`

---

## 已知限制

- 目前僅支援第一個站台設定（`sites[0]`）
- selector 依賴前端 DOM 結構，網站改版需調整設定檔
- 使用 `time.sleep(1)` 等待頁面載入，未使用顯式等待
- 僅擷取票價文字，未進行數值解析

---

## 依賴套件

- selenium  
- pandas  
- openpyxl  

完整依賴請參考 `requirements.txt`
