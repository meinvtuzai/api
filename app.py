import os
import json
import time
from datetime import datetime

def scan_directory(directory_path):
    """扫描指定目录下的所有文件并收集信息"""
    file_info_list = []
    
    # 遍历目录下的所有文件和子目录
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            # 获取文件基本信息
            file_size = os.path.getsize(file_path)
            creation_time = os.path.getctime(file_path)
            creation_date = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")
            
            # 尝试获取Android应用包名（仅对APK文件有效）
            package_name = None
            if file_name.lower().endswith('.apk'):
                package_name = get_apk_package_name(file_path)
            
            # 构建文件信息字典
            file_info = {
                "文件名": file_name,
                "路径": file_path,
                "大小(字节)": file_size,
                "app包名": package_name,
                "生成日期": creation_date
            }
            
            file_info_list.append(file_info)
    
    return file_info_list

def get_apk_package_name(apk_path):
    """从APK文件中提取包名（简化实现，实际应用中可能需要更复杂的解析）"""
    # 注意：此为简化示例，实际应用中可能需要使用apktools或androguard等库
    try:
        # 这里仅作为示例，实际需要解析APK的AndroidManifest.xml
        # 以下代码需要安装apkutils2库：pip install apkutils2
        from apkutils import APK
        apk = APK(apk_path)
        return apk.androidmanifest.package
    except Exception as e:
        print(f"无法解析APK包名: {e}")
        return None

def save_to_json(file_info_list, output_path):
    """将文件信息保存为JSON文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(file_info_list, f, ensure_ascii=False, indent=2)
    print(f"扫描完成，结果已保存至: {output_path}")

if __name__ == "__main__":
    # 设置要扫描的目录和输出文件路径
    directory_to_scan = input("25")
    output_file = input("25")
    
    if not os.path.exists(directory_to_scan):
        print(f"目录不存在: {directory_to_scan}")
    else:
        print(f"开始扫描目录: {directory_to_scan}")
        file_info = scan_directory(directory_to_scan)
        save_to_json(file_info, output_file)
        print(f"共扫描到 {len(file_info)} 个文件")
