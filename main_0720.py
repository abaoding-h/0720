import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def init_driver():
    options = Options()

    # Mac在这使用独立的selenium用户数据，避免权限冲突
    user_data_dir = "/Users/harvey/selenium_profile"
    os.makedirs(user_data_dir, exist_ok=True)
    options.add_argument(f"--user-data-dir={user_data_dir}")

    options.add_argument("--lang=en-US")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("prefs", {"intl.accept_languages": "en-US,en"})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def search_and_extract(driver, sysname):
    query = f"Summarize {sysname} AI adoption timeline"
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&hl=en&gl=us"

    driver.get(search_url)

    summary = "No AI Overview found"

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-sfe='1'] | //div[@data-subtree='aimfl']"))
        )
    except:
        pass

    # 点"Show more"
    try:
        show_more_button = driver.find_element(By.XPATH, "//div[@class='niO4u VDgVie SlP8xc']//span[text()='Show more']")
        driver.execute_script("arguments[0].click();", show_more_button)
        time.sleep(2)
    except:
        pass

    try:
        # 抓AO的主文本
        overview_elements = driver.find_elements(By.XPATH, "//div[@data-subtree='aimfl']")
        overview_texts = [el.text.strip() for el in overview_elements if el.text.strip()]

        # 抓tl
        timeline_items = driver.find_elements(By.XPATH, "//ul[@class='U6u95']/li")
        timeline_texts = []
        for item in timeline_items:
            timeline_texts.append(item.text.strip())

        if overview_texts or timeline_texts:
            summary = ""
            if overview_texts:
                summary += "\n".join(overview_texts)
            if timeline_texts:
                summary += "\nTimeline:\n" + "\n".join(timeline_texts)
    except:
        pass

    return query, summary

def main():
    input_file = "aha_hosp_w_ai.xlsx"
    output_file = "google_ai_overview_timeline_full.csv"
    output_path = os.path.join(os.getcwd(), output_file)

    if not os.path.exists(input_file):
        print(f"输入文件 {input_file} 不存在，将文件放在脚本同目录下")
        return

    df = pd.read_excel(input_file)
    sysnames = df['sysname'].dropna().drop_duplicates().reset_index(drop=True)

    driver = init_driver()

    print("\n【注意】已打开浏览器,请手动登录Google账号,确保AO显示正常")
    input("登录完成后请按回车继续...\n")

    results = []
    for idx, sysname in enumerate(sysnames):
        print(f"搜索中 ({idx+1}/{len(sysnames)}): {sysname} ...")
        query, summary = search_and_extract(driver, sysname)
        results.append({
            "sysname": sysname,
            "query": query,
            "summary": summary
        })

        pd.DataFrame(results).to_csv(output_path, index=False, encoding='utf-8-sig')
        time.sleep(2)

    driver.quit()
    print(f"\n已完成，结果保存在：{output_path}")

if __name__ == "__main__":
    main()
