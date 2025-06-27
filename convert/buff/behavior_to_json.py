import re

def format_lua_table(lua_str: str) -> str:
    indent = 0
    result = ""
    i = 0
    in_string = False
    string_char = ''

    while i < len(lua_str):
        c = lua_str[i]

        if c in ["'", '"']:
            if not in_string:
                in_string = True
                string_char = c
            elif in_string and c == string_char and lua_str[i - 1] != '\\':
                in_string = False
            result += c
            i += 1
            continue

        if in_string:
            result += c
            i += 1
            continue

        if lua_str[i:i+8] == "__size =":
            while i < len(lua_str) and lua_str[i] not in [',', '}']:
                i += 1
            if i < len(lua_str) and lua_str[i] == ',':
                i += 1
            continue

        if c == '{':
            result += "{\n"
            indent += 1
            result += "    " * indent
        elif c == '}':
            result += "\n"
            indent -= 1
            result += "    " * indent + "}"
        elif c == ',':
            result += ",\n" + "    " * indent
        elif c == '\n':
            result += "\n" + "    " * indent
        else:
            result += c

        i += 1

    return result

def post_process_onSomeFlag(lua_text: str) -> str:
    return re.sub(
        r"\[\s*'onSomeFlag'\s*\]\s*=\s*{\s*'([^']+)'\s*},?",
        r"onSomeFlag=<\1>,",
        lua_text
    )

def condense_func_args(lua_text: str) -> str:
    def convert_block(block: str) -> str:
        kv_pattern = re.findall(r"\['(.*?)'\]\s*=\s*('(?:[^'\\]|\\.)*'|[^,{}]+)", block)
        kv_dict = {k: v.strip("'") for k, v in kv_pattern}
        sorted_items = sorted(kv_dict.items())
        body = ";".join(f"{k}={v}" for k, v in sorted_items)
        return f"<{{{body}}}>"

    def replacer(match):
        block = match.group(0)
        if "['cfgId']" in block:
            return convert_block(block)
        return block

    return re.sub(r"{\s*(\['.*?'\]\s*=\s*[^{}]+,?\s*)+}", replacer, lua_text)

def merge_func_args_blocks(lua_text: str) -> str:
    pattern = re.compile(
        r"\[\s*'funcArgs'\s*\]\s*=\s*{\s*((?:{\s*<\{[^}]+\}>\s*},?\s*)+)}",
        re.DOTALL
    )

    def replacer(match):
        entries = re.findall(r"<\{[^}]+\}>", match.group(0))
        return "funcArgs=<" + ";".join(entries) + ">"

    return pattern.sub(replacer, lua_text)

def simplify_effect_funcs(lua_text: str) -> str:
    pattern = re.compile(
        r"\[\s*'effectFuncs'\s*\]\s*=\s*{\s*([^}]+)\s*}",
        re.DOTALL
    )

    def replacer(match):
        items = re.findall(r"'([^']+)'", match.group(1))
        return "effectFuncs=<" + ";".join(items) + ">"

    return pattern.sub(replacer, lua_text)

def simplify_trigger_times(lua_text: str) -> str:
    pattern = re.compile(
        r"\[\s*'triggerTimes'\s*\]\s*=\s*{\s*([^}]+)\s*}",
        re.DOTALL
    )

    def replacer(match):
        items = re.findall(r"\d+", match.group(1))
        return "triggerTimes=<" + ";".join(items) + ">"

    return pattern.sub(replacer, lua_text)

def simplify_keys(lua_text: str) -> str:
    return re.sub(r"\[\s*'(\w+)'\s*\]\s*=\s*", r"\1=", lua_text)
    
def flatten_top_level_blocks(lua_text: str) -> str:
    blocks = []
    brace_level = 0
    start_idx = None
    for i, c in enumerate(lua_text):
        if c == '{':
            if brace_level == 1 and start_idx is None:
                start_idx = i
            brace_level += 1
        elif c == '}':
            brace_level -= 1
            if brace_level == 1 and start_idx is not None:
                block = lua_text[start_idx:i+1]
                # Làm gọn block
                block = re.sub(r'\s+', '', block.strip())  # Xoá khoảng trắng thừa
                block = re.sub(r'\s*;\s*', ';', block)
                block = re.sub(r',\s*', ';', block)
                block = re.sub(r';+', ';', block)
                block = block.strip(';')
                blocks.append(block)
                start_idx = None

    return "{\n    " + ",\n    ".join(blocks) + "\n}"

from collections import OrderedDict

KEY_ORDER = [
    "nodeId", "triggerPoint", "triggerTimes", "effectFuncs", "funcArgs", "onSomeFlag"
]

def extract_top_level_blocks(lua_text: str) -> list:
    blocks = []
    brace_level = 0
    start = None
    for i, c in enumerate(lua_text):
        if c == '{':
            if brace_level == 1 and start is None:
                start = i
            brace_level += 1
        elif c == '}':
            brace_level -= 1
            if brace_level == 1 and start is not None:
                blocks.append(lua_text[start:i+1])
                start = None
    return blocks

def reorder_block_keys(block: str) -> str:
    block = simplify_keys(block)
    block = post_process_onSomeFlag(block)
    block = condense_func_args(block)
    block = merge_func_args_blocks(block)
    block = simplify_effect_funcs(block)
    block = simplify_trigger_times(block)

    # Chuyển các dòng thành dict
    items = re.findall(r"(\w+)\s*=\s*(<\{[^}]+\}>|<[^>]+>|[^,]+)", block)
    kv = {k: v.strip().rstrip(',') for k, v in items}

    # Sắp xếp theo KEY_ORDER
    ordered = OrderedDict()
    for k in KEY_ORDER:
        if k in kv:
            ordered[k] = kv[k]

    body = ";".join(f"{k}={v}" for k, v in ordered.items())
    return f"<{{{body}}}>"

def comma_to_semicolon(lua_text: str) -> str:
    # Thay thế dấu phẩy ở cuối dòng (bỏ qua dòng chỉ có dấu phẩy)
    return re.sub(r',\s*$', ';', lua_text, flags=re.MULTILINE)

def remove_quotes(lua_text: str) -> str:
    # Loại bỏ dấu nháy đơn hoặc nháy kép quanh giá trị sau dấu =
    return re.sub(r"(=\s*)'([^']*)'", r"\1\2", lua_text)

def process_holder(lua_text: str) -> str:
    def replacer(match):
        content = match.group(1)
        # Nếu chỉ toàn số
        if re.fullmatch(r'[\d;= ]+', content):
            return f"holder={{{content}}}"
        # Nếu có ký tự chữ, xử lý lại: bỏ nháy, nối bằng ;
        pairs = re.findall(r"(\w+)\s*=\s*['\"]?([^;'\"]+)['\"]?", content)
        body = ";".join(f"{k}={v}" for k, v in pairs)
        return f"holder={{{body}}}"
    return re.sub(r"holder=\{([^}]*)\}", replacer, lua_text)

def simplify_value_lists(lua_text: str) -> str:
    def replacer(match):
        content = match.group(1)
        if re.fullmatch(r'[\d;\s]+', content):  # only digits and separators
            simplified = re.sub(r'\s+', '', content.strip())
            return f"value=<{simplified}>"
        return match.group(0)

    return re.sub(r"value=\{([^}]+)\}", replacer, lua_text)

def wrap_outer_brace_to_angle(lua_text: str) -> str:
    lua_text = lua_text.strip()
    if lua_text.startswith("{") and lua_text.endswith("}"):
        return "<" + lua_text[1:-1].strip() + ">"
    return lua_text

def flatten_to_single_line(lua_text: str) -> str:
    def preserve_value_blocks(text: str) -> str:
        # Đánh dấu value=... là đoạn không được động vào
        protected = []
        def repl(match):
            protected.append(match.group(0))
            return f"__VALUE_BLOCK_{len(protected) - 1}__"

        # 1. Bảo vệ các value=... (có biểu thức hoặc dấu cách)
        text = re.sub(r'value=([^;>\n]+)', repl, text)

        # 2. Làm sạch phần còn lại
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = re.sub(r'\s+', ' ', text).strip()

        # 3. Khôi phục lại các value block
        for idx, val in enumerate(protected):
            text = text.replace(f"__VALUE_BLOCK_{idx}__", val)

        return text

    return preserve_value_blocks(lua_text)

def replace_brace_patterns(lua_text: str) -> str:
    lua_text = re.sub(r';\s*\}', '}', lua_text)
    return lua_text

def convert_triple_brace_to_double_angle(lua_text: str) -> str:
    lua_text = lua_text.replace("{{{", "<<{")
    lua_text = lua_text.replace("}}}", "}>>")
    return lua_text

def remove_unwanted_spaces(lua_text: str) -> str:
    lua_text = re.sub(r'(<{)\s+', r'\1', lua_text)
    lua_text = re.sub(r'(;)\s+', r'\1', lua_text)
    lua_text = re.sub(r'(\})\s+', r'\1', lua_text)
    lua_text = re.sub(r'({)\s+', r'\1', lua_text)
    lua_text = re.sub(r'(,)\s+', r'\1', lua_text)
    return lua_text

# Input Lua string
lua_input = """{{['effectFuncs'] = {'castBuff'}, ['triggerPoint'] = 12, ['funcArgs'] = {{{['holder'] = 14, ['lifeRound'] = 1, ['value'] = 'self:specialDamage()*2.5*(1+0.25*(6-getForceNum(self:force())))', ['cfgId'] = 40110962, ['caster'] = 2, __size = 5}}}, ['nodeId'] = 1, __size = 4}}"""

# Step 1: Format lua
formatted = format_lua_table(lua_input)

# Step 2: Replace onSomeFlag
step2 = post_process_onSomeFlag(formatted)

# Step 3: Condense funcArgs tables
step3 = condense_func_args(step2)

# Step 4: Merge into single funcArgs=<<...>> line
step4 = merge_func_args_blocks(step3)

# Step 5: Simplify effectFuncs
step5 = simplify_effect_funcs(step4)

# Step 5: Simplify triggerTimes
step6 = simplify_trigger_times(step5)

step7 = simplify_keys(simplify_trigger_times(step6))
step8 = comma_to_semicolon(step7)
step9 = remove_quotes(step8)

step10 = process_holder(step9)
step11 = simplify_value_lists(step10)

step12 = wrap_outer_brace_to_angle(step11)

step13 = flatten_to_single_line(step12)

step14 = replace_brace_patterns(step13)

step15 = convert_triple_brace_to_double_angle(step14)

step16 = remove_unwanted_spaces(step15)

# Write to file instead of printing
with open('output_data.json', 'w', encoding='utf-8') as f:
    f.write(step16)

print(f"Output has been written to output_data.json")
