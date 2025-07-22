from PIL import Image
import os
import re

def rgb888_to_rgb565(r, g, b):
    """將 RGB888 轉換為 RGB565 (16-bit 格式)"""
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

def image_to_rgb565_array(image_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    pixel_values = list(img.getdata())
    rgb565_array = []

    for i in range(0, len(pixel_values), width):
        row = []
        for j in range(width):
            r, g, b = pixel_values[i + j]
            val565 = rgb888_to_rgb565(r, g, b)
            row.append(f"0x{val565:04X}")
        rgb565_array.append(row)

    return rgb565_array, width, height

# === 新增：自然排序函式（確保 1.jpg、2.jpg、10.jpg 順序正確）===
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def generate_c_array(image_folder, output_file):
    files = os.listdir(image_folder)
    image_files = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    image_files = sorted(image_files, key=natural_keys)  # ✅ 使用自然排序

    with open(output_file, "w") as f:
        f.write('#include <Arduino.h>\n\n')  # ESP32 適用

        for idx, file in enumerate(image_files):
            image_path = os.path.join(image_folder, file)
            array_data, width, height = image_to_rgb565_array(image_path)
            var_name = f"f{idx + 1}"  # 命名為 f1, f2, ..., fn

            f.write(f"// Image: {file}, size: {width}x{height}\n")
            f.write(f"const uint16_t {var_name}[{width * height}] = {{\n")
            for row in array_data:
                f.write("    " + ", ".join(row) + ",\n")
            f.write("};\n\n")

if __name__ == "__main__":
    image_folder = "./picture"  # 圖片所在資料夾
    output_file = "image_arrays.c"
    generate_c_array(image_folder, output_file)
    print(f"✅ 已成功輸出 RGB565 C 陣列至：{output_file}")
