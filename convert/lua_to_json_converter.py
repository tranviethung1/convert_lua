import re
import json
import sys

def parse_lua_table_comment(comment):
    original = comment.strip()

    # Nếu là danh sách đơn giản kiểu {123, 456}, chuyển thành JSON array
    if re.match(r'^\{\s*-?\d+(\.\d+)?(,\s*-?\d+(\.\d+)?)*\s*\}$', original):
        array_content = original.strip('{}')
        array_items = []
        for x in array_content.split(','):
            x = x.strip()
            if '.' in x:
                array_items.append(float(x))
            else:
                array_items.append(int(x))
        return array_items

    # Nếu là bảng key-value
    # Chuyển ['key'] = hoặc [123] = thành "key": hoặc "123":
    comment = re.sub(r"\[\s*'([^']+)'\s*\]\s*=", r'"\1":', original)  # ['key']
    comment = re.sub(r"\[\s*(\d+)\s*\]\s*=", r'"\1":', comment)       # [123]
    comment = re.sub(r"(?<!\")\b(\w+)\s*=", r'"\1":', comment)        # key = 
    comment = comment.replace("'", '"')                               # 'abc' -> "abc"
    return json.loads(comment)

def parse_lua_file(content):
    result = {}
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Bỏ qua dòng rỗng
        if not line or line.startswith("--"):
            i += 1
            continue

        # Trường dạng đặc biệt: field = __data_t__xxx[...]
        match_data_t = re.match(r'(\w+)\s*=\s*__data_t__\w+\[\d+\]', line)
        if match_data_t:
            key = match_data_t.group(1)
            # Kiểm tra dòng sau là comment table
            if i + 1 < len(lines):
                comment_line = lines[i + 1].strip()
                comment_match = re.match(r"--\s*(\{.*\})", comment_line)
                if comment_match:
                    lua_table_str = comment_match.group(1)
                    try:
                        value = parse_lua_table_comment(lua_table_str)
                        result[key] = value
                        i += 2
                        continue
                    except Exception as e:
                        print(f"Lỗi parse comment table ở dòng {i+2}: {e}")
        else:
            # Dạng thông thường: key = value
            match_normal = re.match(r'(\w+)\s*=\s*(.+?)[,]?\s*$', line)
            if match_normal:
                key, value = match_normal.groups()
                value = value.strip().strip(',')

                # Nếu là chuỗi trong '...' hoặc "..."
                if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                    result[key] = value[1:-1]
                # Nếu là số
                elif re.match(r'^\d+(\.\d+)?$', value):
                    result[key] = float(value) if '.' in value else int(value)
                # Nếu là boolean
                elif value in ['true', 'false']:
                    result[key] = True if value == 'true' else False
                else:
                    # Nếu là bảng dạng {1,2,...} mà không có comment => giữ nguyên string
                    result[key] = value
        i += 1

    return result

if __name__ == "__main__":

    try:
        with open("input_data.lua", "r", encoding="utf-8") as f:
            content = f.read().strip()
        parsed = parse_lua_file(content)

        # In kết quả ra màn hình
        print(json.dumps(parsed, indent=2, ensure_ascii=False))

        # Ghi vào file convert.json
        with open("output_data.json", "w", encoding="utf-8") as out:
            json.dump(parsed, out, indent=2, ensure_ascii=False)

        print("✅ Đã ghi kết quả vào file convert.json")
    except Exception as e:
        print("❌ Lỗi:", e)
