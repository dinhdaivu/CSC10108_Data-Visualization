import os

# Đường dẫn tới thư mục chứa các folder cần rename
base_path = "./data"

for folder_name in os.listdir(base_path):
    old_path = os.path.join(base_path, folder_name)
    
    # Kiểm tra có phải folder không
    if os.path.isdir(old_path):
        try:
            # Tách dd-mm-yyyy
            dd, mm, yyyy = folder_name.split("-")
            
            # Tạo tên mới mm-dd-yyyy
            new_name = f"{mm}-{dd}-{yyyy}"
            new_path = os.path.join(base_path, new_name)
            
            # Rename
            os.rename(old_path, new_path)
            print(f"Renamed: {folder_name} -> {new_name}")
        
        except ValueError:
            # Bỏ qua nếu không đúng format
            print(f"Skipped (invalid format): {folder_name}")