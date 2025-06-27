import csv
import io
import json
import re  # ✅ thêm dòng này để dùng re.sub()

header = '''变量名,eventID,_name,delay,sound,damageSeg,hpSeg,segInterval,shaker,music,zOrder,move,show,effectType,effectRes,effectArgs,otherEventIDs,follow,onlyTargetShow,jumpFlag,control'''.split(',')

raw_text = '''
{
  "id": 361131,
  "eventID": 717016,
  "damageSeg": [
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05,
    0.05
  ],
  "segInterval": "{0, 266.6, 266.6, 700, 233.3, 133.3, 133.3, 133.3, 133.3, 133.3, 133.3, 166.6, 166.6, 266.6, 733.3, 1933.3, 266.6, 233.3, 266.6, 100}",
  "shaker": {
    "beginT": 0,
    "disy": 30,
    "endT": 200,
    "disx": 20,
    "count": 1,
    "interval": 0,
    "isRepeat": true,
    "__size": 7
  }
}
'''

parsed_data = json.loads(raw_text)

def parse_curly_list(value):
    if isinstance(value, str):
        return list(map(int, re.findall(r'\d+', value)))
    return value

def list_to_str(val):
    return f"<{';'.join(str(x) for x in val)}>" if isinstance(val, list) else val

# ✅ Cập nhật hàm để loại __size ở mọi cấp độ
def dict_to_custom_string(data, exclude_keys=None):
    if not isinstance(data, dict):
        return data
    if exclude_keys is None:
        exclude_keys = []

    def format_value(v):
        if isinstance(v, bool):
            return str(v).lower()
        elif isinstance(v, list):
            return list_to_str(v)
        elif isinstance(v, dict):
            return dict_to_custom_string(v, exclude_keys)  # truyền xuống tiếp
        return v

    return "{" + ";".join(f"{k}={format_value(v)}" for k, v in data.items() if k not in exclude_keys) + "}"

def format_bool(val):
    return str(val).upper() if isinstance(val, bool) else val

csv_line = {}
csv_line['变量名'] = parsed_data.get('变量名', parsed_data.get('id', 0))
csv_line['eventID'] = parsed_data.get('eventID', '')
csv_line['_name'] = parsed_data.get('_name', '')
csv_line['delay'] = parsed_data.get('delay', '')
csv_line['sound'] = parsed_data.get('sound', '')
csv_line['damageSeg'] = list_to_str(parsed_data.get('damageSeg', ''))
csv_line['hpSeg'] = list_to_str(parsed_data.get('hpSeg', ''))
csv_line['segInterval'] = list_to_str(parse_curly_list(parsed_data.get('segInterval', '')))
csv_line['shaker'] = dict_to_custom_string(parsed_data.get('shaker', ''), exclude_keys=["__size"])
csv_line['music'] = parsed_data.get('music', '')
csv_line['zOrder'] = parsed_data.get('zOrder', '')
csv_line['move'] = parsed_data.get('move', '')
csv_line['show'] = parsed_data.get('show', '')
csv_line['effectType'] = parsed_data.get('effectType', '')
csv_line['effectRes'] = parsed_data.get('effectRes', '')
csv_line['effectArgs'] = dict_to_custom_string(parsed_data.get('effectArgs', ''), exclude_keys=["__debug", "__size"])
csv_line['otherEventIDs'] = list_to_str(parsed_data.get('otherEventIDs', ''))
csv_line['follow'] = dict_to_custom_string(parsed_data.get('follow', ''), exclude_keys=["__size"])
csv_line['onlyTargetShow'] = format_bool(parsed_data.get('onlyTargetShow', 'TRUE'))
csv_line['jumpFlag'] = format_bool(parsed_data.get('jumpFlag', ''))
csv_line['control'] = dict_to_custom_string(parsed_data.get('control', ''), exclude_keys=["__size"])


# Ghi file CSV
output = io.StringIO()
writer = csv.DictWriter(output, fieldnames=header)
writer.writerow(csv_line)
csv_result = output.getvalue().strip()

with open("effect_event_tmp.txt", "w", encoding="utf-8", newline="") as f:
    f.write(csv_result + "\n")

print("✅ CSV line written to effect_event_tmp.txt")

