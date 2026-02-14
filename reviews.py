import os
import json
import time
import sys
import hashlib
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 1. Cấu hình hệ thống
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    # Dành cho các phiên bản Python cũ hơn 3.7
    pass

today = datetime.now().strftime('%d-%m-%Y') 
target_path = os.path.join('data', today)  # Đảm bảo folder này đã tồn tại (ví dụ: 14-02-2026)
input_file = os.path.join(target_path, 'products.json')
output_file = os.path.join(target_path, 'reviews.json')

# --- HÀM 1: MỞ TRÌNH DUYỆT ĐỂ BẠN GIẢI CAPTCHA/LẤY TOKEN ---
def get_session_manual():
    print(f"\n[SYSTEM] 🟢 Đang kích hoạt chế độ xác thực thủ công...")
    options = Options()
    options.add_argument("--start-maximized")
 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Vào một trang sản phẩm để Lazada tạo Session Review
    driver.get("https://www.lazada.vn/products/i3133030071.html") 
    
    print("\n" + "="*70)
    print("🚀 HÀNH ĐỘNG CẦN THIẾT:")
    print("👉 1. Giải Captcha nếu có")
    print("👉 2. Đăng nhập tài khoản Lazada nếu cần")
    print("👉 3. Sau khi trang hiện ra nhận xét, nhấn [ENTER].")
    print("="*70 + "\n")
    input(">>> Nhấn [ENTER] để tiếp tục cào dữ liệu...")
    
    cookies = {c['name']: c['value'] for c in driver.get_cookies()}
    ua = driver.execute_script("return navigator.userAgent;")
    token = cookies.get('_m_h5_tk', '')
    
    driver.quit()
    if not token:
        print("❌ Cảnh báo: Không lấy được Token!")
    return token, cookies, ua

# --- HÀM 2: TÍNH TOÁN CHỮ KÝ MD5 (SIGN) ---
def generate_sign(token, t, data_json):
    token_prefix = token.split('_')[0]
    app_key = "24677475"
    base_str = f"{token_prefix}&{t}&{app_key}&{data_json}"
    return hashlib.md5(base_str.encode('utf-8')).hexdigest()

# --- HÀM 3: LẤY TẤT CẢ TRANG REVIEW CỦA 1 SẢN PHẨM ---
def fetch_item_reviews(item_id, token, cookies, ua):
    item_results = []
    page_no, total_pages = 1, 1
    
    headers = {
        "User-Agent": ua,
        "Referer": f"https://www.lazada.vn/products/-i{item_id}.html",
        "Cookie": "; ".join([f"{k}={v}" for k, v in cookies.items()])
    }

    while page_no <= total_pages:
        t = str(int(time.time() * 1000))
        data_dict = {"itemId": str(item_id), "pageSize": "20", "pageNo": str(page_no)}
        data_json = json.dumps(data_dict, separators=(',', ':'))
        sign = generate_sign(token, t, data_json)
        
        api_url = "https://acs-m.lazada.vn/h5/mtop.lazada.review.item.getpcreviewlist/1.0/"
        params = {
            "jsv": "2.7.2", "appKey": "24677475", "t": t, "sign": sign,
            "api": "mtop.lazada.review.item.getPcReviewList", "v": "1.0",
            "type": "originaljson", "dataType": "json", "data": data_json
        }

        try:
            r = requests.get(api_url, params=params, headers=headers, timeout=10)
            res = r.json()
            ret_msg = res.get('ret', [''])[0]

            if "SUCCESS" in ret_msg:
                reviews = res.get('data', {}).get('module', {}).get('reviews', [])
                for rev in reviews:
                    content = " ".join([c.get('content', '') for c in rev.get('reviewContentList', [])])
                    item_results.append({
                        'id_sp': item_id,
                        'rating': rev.get('rating'),
                        'comment': content.strip(),
                        'time': rev.get('reviewTime'),
                        'sku': rev.get('skuInfo')
                    })
                
                # Cập nhật số trang từ lần gọi đầu tiên
                if page_no == 1:
                    total_pages = res.get('data', {}).get('paging', {}).get('totalPages', 1)
                    total_pages = min(total_pages, 50) # Lấy tối đa 50 trang (1000 cmt)
                
                page_no += 1
                time.sleep(0.1)
            elif "FAIL_SYS_USER_VALIDATE" in ret_msg:
                return None, "BLOCK_CAPTCHA" # Tín hiệu bị chặn
            else:
                return item_results, f"END_OR_ERROR: {ret_msg}"
        except Exception as e:
            return item_results, str(e)
            
    return item_results, "SUCCESS"

# --- HÀM CHÍNH: QUẢN LÝ VÒNG LẶP CÁC SẢN PHẨM ---
def main():
    if not os.path.exists(input_file):
        print(f"❌ Không thấy file {input_file}")
        return

    # A. Tải dữ liệu cũ để chạy tiếp (Checkpoint)
    all_final_data = []
    crawled_ids = set()
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            all_final_data = json.load(f)
            crawled_ids = {str(r['id_sp']) for r in all_final_data}
        print(f"📦 Đã tìm thấy dữ liệu cũ. Bỏ qua {len(crawled_ids)} sản phẩm đã hoàn thành.")

    # B. Lọc danh sách sản phẩm chưa cào
    with open(input_file, 'r', encoding='utf-8') as f:
        all_products = json.load(f)
        remaining_products = [p for p in all_products if str(p['id']) not in crawled_ids]

    if not remaining_products:
        print("✅ Hoàn thành 100% danh sách sản phẩm!")
        return

    # C. Lấy Token lần đầu
    token, cookies, ua = get_session_manual()
    
    idx = 0
    while idx < len(remaining_products):
        p = remaining_products[idx]
        pid = str(p.get('id'))
        pname = p.get('ten_san_pham', 'N/A')[:35]
        
        print(f"🚀 [{idx+1}/{len(remaining_products)}] Đang quét: {pid}")
        
        item_reviews, status = fetch_item_reviews(pid, token, cookies, ua)
        
        if status == "SUCCESS" or "END_OR_ERROR" in status:
            if item_reviews:
                all_final_data.extend(item_reviews)
                # Lưu JSON ngay lập tức
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(all_final_data, f, ensure_ascii=False, indent=4)
                print(f"   ✅ Lấy xong: {len(item_reviews)} reviews.")
            else:
                print(f"   ⚪ Sản phẩm không có nhận xét.")
            
            idx += 1 # Chuyển sang sản phẩm tiếp theo
            time.sleep(0.1)
            
        elif status == "BLOCK_CAPTCHA":
            print(f"\n⚠️ CẢNH BÁO: Lazada đã phát hiện Bot (FAIL_SYS_USER_VALIDATE)!")
            print("🔄 Hãy giải Captcha trên trình duyệt sắp mở ra...")
            token, cookies, ua = get_session_manual()
            # Không tăng idx để vòng lặp chạy lại đúng ID vừa bị lỗi
            
        else:
            print(f"   ❌ Lỗi kết nối ({status}). Thử lại sau 5 giây...")
            time.sleep(5)

    print(f"\n🎉 HOÀN THÀNH! Tổng cộng lấy được {len(all_final_data)} nhận xét.")

if __name__ == "__main__":
    main()