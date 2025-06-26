import csv
import io
import json
import re  # ✅ thêm dòng này để dùng re.sub()

header = '''变量名,skillName,skillName_tw,skillName_en,skillName_kr,_beizhu,skillTypeShow,skillTypeShow_tw,skillTypeShow_en,describe,describe_tw,describe_en,describe_kr,simDesc,simDesc_tw,simDesc_en,simDesc_kr,starEffect,starEffectDesc,starEffectDesc_tw,starEffectDesc_en,starEffectDesc_kr,zawakeEffect,zawakeEffectDesc,zawakeEffectDesc_tw,zawakeEffectDesc_en,zawakeEffectDesc_kr,zawakeSimpleType,zawakeSimpleDesc,zawakeSimpleDesc_tw,zawakeSimpleDesc_en,zawakeSimpleDesc_kr,upLvDesc,upLvDesc_tw,upLvDesc_en,upLvDesc_kr,iconRes,isGlobal,changeUnitTrigger,isCombat,alwaysEffective,passivePriority,skillType,skillType2,skillDamageType,skillNatureType,skillPower,skillHit,weather,cdRound,startRound,passiveStartRound,passiveTriggerType,passiveTriggerArg,posChoose,moveTime,specialChoose,hitFormula,hintTargetType,hintChoose,specialHintChoose,autoHintChoose,targetTypeDesc,targetChooseType,targetTypeDesc_en,targetTypeDesc_kr,targetTypeDesc_tw,_attacktest,damageFormula,_damageFormula,hpFormula,skillCalDamageProcessId,diffSkillCalDmgProcessId,skillProcess,passiveSkillAttrs,activeType,activeCondition,fightingPoint,costMp1,costMp1Args,recoverMp1,widgetEffects,hurtMp1,costID,posC,chargeArgs,skillArgs,conditionValue,spineAction,flashBack,cameraNear,cameraNear_posC,cameraNear_blankTime,cameraNear_scaleArgs,blankTime,scaleArgs,effectBigName,effectBigPos,effectBigFlip,notShowProcedure,hurtPos,sound,allEffectTime'''.split(',')

raw_text = '''
{
  "id": 1020911,
  "skillName": "Shikigami-Tăng Giảm",
  "describe": "Florges điều khiển cánh hoa ma pháp tấn công một mục tiêu phe địch, gây #C0xF13B54#ST đặc biệt#C0x5B545B# bằng #C0x3D8A99#100% Công Đặc Biệt#C0x5B545B#+$(skillLevel*4*24)$, tăng 20% tỉ lệ trị liệu cho bản thân 2 hiệp",
  "simDesc": "Florges điều khiển cánh hoa ma pháp tấn công một mục tiêu phe địch",
  "zawakeEffect": [
    79001
  ],
  "zawakeEffectDesc": "Florges điều khiển cánh hoa ma pháp tấn công một mục tiêu phe địch, gây #C0xF13B54#ST đặc biệt#C0x5B545B# bằng #C0x3D8A99#100% Công Đặc Biệt#C0x5B545B#+$(skillLevel*4*24)$, tăng 20% tỉ lệ trị liệu cho bản thân 3 hiệp",
  "zawakeSimpleType": 2,
  "zawakeSimpleDesc": "Tăng 20% tỉ lệ trị liệu cho bản thân 2 hiệp\\n#F20# \\n#F40##C0x5c9970#→Tăng 20% tỉ lệ trị liệu cho bản thân 3 hiệp",
  "upLvDesc": "ST Cố Định +96",
  "iconRes": "ICON/skill/skill/001gqs_skill2.png",
  "skillNatureType": 18,
  "posChoose": 1,
  "targetTypeDesc": "1 kẻ địch",
  "targetChooseType": "single",
  "skillProcess": "{10209111, 10209112}",
  "posC": {
    "y": 0,
    "x": -280,
    "__size": 2
  },
  "sound": {
    "delay": 0,
    "loop": 0,
    "res": "hero_sound/huajiefr_attack.mp3",
    "__size": 3
  }
}
'''

# Escape \n không hợp lệ trong chuỗi JSON
parsed_data = json.loads(raw_text)

def parse_curly_list(value):
    if isinstance(value, str):
        return list(map(int, re.findall(r'\d+', value)))
    return value

def list_to_str(val):
    return f"<{';'.join(str(x) for x in val)}>" if isinstance(val, list) else val

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
            return dict_to_custom_string(v, exclude_keys)
        return v

    return "{" + ";".join(f"{k}={format_value(v)}" for k, v in data.items() if k not in exclude_keys) + "}"

csv_line = {}
csv_line['变量名'] = parsed_data.get('id', '')
csv_line['skillName'] = parsed_data.get('skillName', '')
csv_line['describe'] = parsed_data.get('describe', '')
csv_line['simDesc'] = parsed_data.get('simDesc', '')
csv_line['starEffectDesc'] = parsed_data.get('starEffectDesc', '')
csv_line['zawakeEffect'] = list_to_str(parsed_data.get('zawakeEffect', ''))
csv_line['zawakeEffectDesc'] = parsed_data.get('zawakeEffectDesc', '')
csv_line['zawakeSimpleType'] = parsed_data.get('zawakeSimpleType', '')
csv_line['zawakeSimpleDesc'] = parsed_data.get('zawakeSimpleDesc', '')
csv_line['upLvDesc'] = parsed_data.get('upLvDesc', '')
csv_line['iconRes'] = parsed_data.get('iconRes', '')
csv_line['skillNatureType'] = parsed_data.get('skillNatureType', '')
csv_line['posChoose'] = parsed_data.get('posChoose', '')
csv_line['targetTypeDesc'] = parsed_data.get('targetTypeDesc', '')
csv_line['targetChooseType'] = parsed_data.get('targetChooseType', '')
csv_line['skillProcess'] = list_to_str(parse_curly_list(parsed_data.get('skillProcess', '')))
csv_line['posC'] = dict_to_custom_string(parsed_data.get('posC', {}), exclude_keys=['__size'])
csv_line['effectBigName'] = list_to_str(parsed_data.get('effectBigName', ''))
csv_line['sound'] = dict_to_custom_string(parsed_data.get('sound', {}), exclude_keys=['__size'])
        
# Ghi file CSV
output = io.StringIO()
writer = csv.DictWriter(output, fieldnames=header)

writer.writerow(csv_line)
csv_result = output.getvalue().strip()
with open("tmp.txt", "w", encoding="utf-8", newline="") as f:
    f.write( csv_result)

print("✅ CSV line written to tmp.txt")

