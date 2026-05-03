# US News Annual Ranking Scraper

This is a Python project designed to scrape university rankings from the U.S. News & World Report website. It collects overall and subject-specific rankings for global universities, saving the data into a CSV file.

---

## Features

- **URL Fetching**: Automatically retrieves a list of university ranking pages.
- **Detailed Data Scraping**: Extracts detailed ranking data for each university, including overall rank, score, and various research metrics across different subjects.
- **CSV Output**: Saves all collected data into a structured CSV file named `usnews.csv`.
- **Resumable**: The script can resume scraping, skipping universities that have already been processed.
- **User-Friendly Progress**: Displays a progress bar to monitor the scraping process.

---

## Prerequisites

- Python 3.x
- Google Chrome browser

---

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd us_news_annual_ranking
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv us_venv
    .\us_venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv us_venv
    source us_venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

The scraping process is divided into two main steps:

### Step 1: Get University URLs

This step uses Selenium to scroll through the U.S. News rankings page and collect the URLs for each university.

**Note**: You may need to manually handle pop-ups (like sign-in prompts or chat boxes) when the browser opens. The script has a 30-second delay (`sleep(30)`) at the beginning to allow for this.

Run the script:
```bash
python get_school_url.py
```
This will generate `schools_url.csv`, which contains the names and URLs of the universities.

### Step 2: Scrape Ranking Data

This script reads the URLs from `schools_url.csv`, scrapes the detailed ranking data for each university, and saves it to `usnews.csv`.

Run the main script:
```bash
python fast_main.py
```
The script will display a progress bar and will automatically skip any universities already present in `usnews.csv`.

---

## File Descriptions

- **`get_school_url.py`**: A script to fetch the URLs of university ranking pages from the main U.S. News site.
- **`fast_score.py`**: Contains the function to parse a single university's page and extract ranking details.
- **`fast_main.py`**: The main script that orchestrates the scraping process by reading URLs and saving the final data.
- **`requirements.txt`**: A list of all Python dependencies required for the project.
- **`schools_url.csv`**: The output file from `get_school_url.py`, containing university names and their URLs.
- **`usnews.csv`**: The final output file with all the scraped ranking data.

---
---

# US News 年度排名爬蟲

這是一個 Python 專案，旨在從 U.S. News & World Report 網站上爬取大學排名。它會收集全球大學的總體排名和各學科排名，並將數據儲存為 CSV 檔案。

---

## 功能

- **URL 獲取**: 自動獲取大學排名頁面的 URL 列表。
- **詳細數據爬取**: 提取每所大學的詳細排名數據，包括不同學科的總體排名、分數和各種研究指標。
- **CSV 輸出**: 將所有收集到的數據儲存到名為 `usnews.csv` 的結構化 CSV 檔案中。
- **可接續執行**: 腳本可以從上次中斷的地方繼續爬取，跳過已處理過的大學。
- **友善的進度顯示**: 顯示進度條以監控爬取過程。

---

## 環境需求

- Python 3.x
- Google Chrome 瀏覽器

---

## 安裝

1.  **複製儲存庫：**
    ```bash
    git clone <repository_url>
    cd us_news_annual_ranking
    ```

2.  **建立並啟用虛擬環境：**
    ```bash
    # Windows
    python -m venv us_venv
    .\us_venv\Scripts\activate

    # macOS/Linux
    python3 -m venv us_venv
    source us_venv/bin/activate
    ```

3.  **安裝所需的套件：**
    ```bash
    pip install -r requirements.txt
    ```

---

## 使用方法

爬取過程分為兩個主要步驟：

### 步驟 1：獲取大學 URL

此步驟使用 Selenium 瀏覽 U.S. News 排名頁面，並收集每所大學的 URL。

**注意**：當瀏覽器打開時，您可能需要手動處理彈出視窗（例如登入提示或聊天框）。腳本開頭有 30 秒的延遲（`sleep(30)`）以便您進行操作。

執行腳本：
```bash
python get_school_url.py
```
這將生成 `schools_url.csv`，其中包含大學的名稱和 URL。

### 步驟 2：爬取排名數據

此腳本會讀取 `schools_url.csv` 中的 URL，爬取每所大學的詳細排名數據，並將其儲存到 `usnews.csv` 中。

執行主腳本：
```bash
python fast_main.py
```
腳本將顯示一個進度條，並會自動跳過 `usnews.csv` 中已存在的大學。

---

## 檔案說明

- **`get_school_url.py`**: 從 U.S. News 主站獲取大學排名頁面 URL 的腳本。
- **`fast_score.py`**: 包含解析單個大學頁面並提取排名詳細資訊的函式。
- **`fast_main.py`**: 組織爬取過程的主腳本，負責讀取 URL 並儲存最終數據。
- **`requirements.txt`**: 專案所需的所有 Python 依賴套件列表。
- **`schools_url.csv`**: `get_school_url.py` 的輸出檔案，包含大學名稱及其 URL。
- **`usnews.csv`**: 包含所有爬取到的排名數據的最終輸出檔案。

