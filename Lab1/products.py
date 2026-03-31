import time
import pandas as pd
import requests
import random
import sys
import os
from datetime import datetime
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 1. Cau hinh he thong
try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

# --- HAM 1: MO SELENIUM LAY COOKIE ---
def get_session_manual(url="https://www.lazada.vn/nike-flagship-store/?q=All-Products&from=wangpu&langFlag=vi&pageTypeId=2"):
    print("\n[SYSTEM] 🟢 Đang khởi động Chrome...")
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        print("\n" + "="*70)
        print("🛑 CHẾ ĐỘ THỦ CÔNG:")
        print("👉 1. Giải Captcha nếu có.")
        print("👉 2. Đăng nhập tài khoản Lazada nếu cần.")
        print("✅ Sau khi hoàn thành, nhấn [ENTER] để tiếp tục.")
        print("="*70 + "\n")
        input(">>> Nhấn [ENTER] để bắt đầu crawling...")
        
        cookies = {c['name']: c['value'] for c in driver.get_cookies()}
        ua = driver.execute_script("return navigator.userAgent;")
        driver.quit()
        return cookies, ua
    except Exception as e:
        print(f"❌ Lỗi Selenium: {e}")
        driver.quit()
        return None, None

# --- HAM 2: TRICH XUAT TOAN BO SAN PHAM ---
def extract_everything(item, cat_name):
    # Lay gia va xu ly gia tri mac dinh neu thieu
    price = item.get('price', 0)
    orig_price = item.get('originalPrice', price)
    
    # Xu ly so luong da ban
    sold_str = str(item.get('itemSoldCntShow', '0')).lower()
    sold_num = 0
    if 'k' in sold_str:
        try: sold_num = int(float(sold_str.replace('k', '').replace(' đã bán', '')) * 1000)
        except: sold_num = 0
    else:
        try: sold_num = int(re.sub(r'\D', '', sold_str))
        except: sold_num = 0

    return {
        'id': item.get('itemId', 'N/A'),
        'ten_san_pham': item.get('name', 'N/A'),
        'danh_muc': cat_name,
        'gia_ban': price,
        'gia_goc': orig_price,
        'so_luong_da_ban': sold_num,
        'diem_danh_gia': item.get('ratingScore', 0),
        'so_luot_nhan_xet': item.get('review', 0),
        'dia_diem_kho': item.get('location', 'N/A'),
        'ton_kho': "Còn hàng" if item.get('inStock', True) else "Hết hàng",
        'thuong_hieu': item.get('brandName', 'Nike'),
        'link_san_pham': "https:" + item.get('itemUrl') if str(item.get('itemUrl', '')).startswith('//') else item.get('itemUrl')
    }

# --- HAM 3: CHUONG TRINH CHINH ---
def main():
    cookies, ua = get_session_manual()
    if not cookies: return

    print("\n[2] 🔍 Đang quét danh sách danh mục...")
    api_cat = "https://www.lazada.vn/nike-flagship-store/?ajax=true&from=wangpu&langFlag=vi&page=1&pageTypeId=2&q=All-Products"
    headers = {'User-Agent': str(ua), 'Referer': 'https://www.lazada.vn/', 'X-Requested-With': 'XMLHttpRequest'}
    
    try:
        resp = requests.get(api_cat, headers=headers, cookies=cookies)
        categories = resp.json().get('mods', {}).get('filter', {}).get('filterItems', [])
        cat_list = []
        for f in categories:
            if f.get('name') == 'category':
                cat_list = f.get('options', [])
                break
    except:
        print("❌ Không lấy được danh mục sản phẩm.")
        return

    all_data = []
    base_url = "https://www.lazada.vn/{}/?nike-flagship-store&ajax=true&from=wangpu&m=shop&page={}&q=All-Products"

    for cat in cat_list:
        cat_name = cat.get('title')
        cat_val = cat.get('value')
        print(f"\n🚀 CRAWLING: {cat_name.upper()}")
        
        page = 1
        while True:
            print(f"   --- Trang {page} ---")
            url = base_url.format(cat_val, page)
            if page == 1: url += "&isFirstRequest=true"
            
            try:
                r = requests.get(url, headers=headers, cookies=cookies, timeout=15)
                items = r.json().get('mods', {}).get('listItems', [])
                
                if not items: break

                for item in items:
                    all_data.append(extract_everything(item, cat_name))
                
                print(f"      + Đã lấy được {len(items)} items.")
                page += 1
                time.sleep(random.uniform(2, 3))
            except:
                break

    # 4. Xuat du lieu song song
    if all_data:
        # A. Tạo đường dẫn thư mục
        today = datetime.now().strftime('%m-%d-%Y')
        target_path = os.path.join('data', today)
        
        if not os.path.exists(target_path):
            os.makedirs(target_path)
            print(f"📂 Đã tạo thư mục mới: {target_path}")

        df = pd.DataFrame(all_data)
        
        # B. Thiết lập đường dẫn tệp bên trong thư mục
        csv_path = os.path.join(target_path, 'products.csv')
        json_path = os.path.join(target_path, 'products.json')
        
        # C. Lưu dữ liệu
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        df.to_json(json_path, orient='records', force_ascii=False, indent=4)
        
        print("\n" + "="*50)
        print(f"✅ HOÀN THÀNH!")
        print(f"📊 Tổng số sản phẩm thu thập được: {len(df)}")
        print(f"📁 Dữ liệu được lưu tại thư mục: {target_path}")
        print(f"   📄 {csv_path}")
        print(f"   📄 {json_path}")
        print("="*50)
    else:
        print("\n❌ Không có dữ liệu.")


if __name__ == "__main__":
    main()