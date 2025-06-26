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
        kv_pattern = re.findall(r"\['(.*?)'\]\s*=\s*([^,{}]+|'[^']*')", block)
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

def flatten_top_level_blocks(lua_text: str) -> str:
    blocks = extract_top_level_blocks(lua_text)
    formatted_blocks = [reorder_block_keys(block) for block in blocks]
    return "{\n    " + ",\n    ".join(formatted_blocks) + "\n}"

# Input Lua string
lua_input = """{{['effectFuncs'] = {'castBuff'}, ['triggerPoint'] = 8, ['funcArgs'] = {{{['holder'] = 2, ['lifeRound'] = 1, ['value'] = 0, ['cfgId'] = 520246, ['caster'] = 2, __size = 5}}}, ['nodeId'] = 1, __size = 4}, {['onSomeFlag'] = {'moreE(self:mp1(),self:mp1Max()) and moreE(self:mp1Max(),1) and (not self:hasBuff(520245)) and less(self:getBuffOverlayCount(520247),2)'}, ['triggerPoint'] = 19, ['nodeId'] = 2, ['funcArgs'] = {{{['holder'] = 2, ['lifeRound'] = 99, ['value'] = 0, ['cfgId'] = 520242, ['caster'] = 2, __size = 5}}, {{['holder'] = 2, ['lifeRound'] = 99, ['cfgId'] = 520243, ['caster'] = 2, ['value'] = 'self:speed()*(0.26+((skillLv(52024) or 0)-1)*0.02)', ['prob'] = 1, __size = 6}}, {{['holder'] = 2, ['lifeRound'] = 99, ['cfgId'] = 520244, ['caster'] = 2, ['value'] = '1200+((skillLv(52024) or 0)-1)*150', ['prob'] = 1, __size = 6}}, {{['holder'] = 2, ['lifeRound'] = 99, ['value'] = 0, ['cfgId'] = 520245, ['caster'] = 2, __size = 5}}, {{['holder'] = 2, ['lifeRound'] = 99, ['value'] = 0, ['cfgId'] = 520247, ['caster'] = 2, __size = 5}}}, ['triggerTimes'] = {1, 1}, ['effectFuncs'] = {'castBuff', 'castBuff', 'castBuff', 'castBuff', 'castBuff'}, __size = 6}}"""

# Step 1: Format lua
formatted = format_lua_table(lua_input)

# # Step 2: Replace onSomeFlag
# step2 = post_process_onSomeFlag(formatted)

# # Step 3: Condense funcArgs tables
# step3 = condense_func_args(step2)

# # Step 4: Merge into single funcArgs=<<...>> line
# step4 = merge_func_args_blocks(step3)

# # Step 5: Simplify effectFuncs
# step5 = simplify_effect_funcs(step4)

# # Step 5: Simplify triggerTimes
# step6 = simplify_trigger_times(step5)

# final_output = simplify_keys(simplify_trigger_times(step6))

# final_output = flatten_top_level_blocks(final_output)

print(formatted)
