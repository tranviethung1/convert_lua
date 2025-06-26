# File: convert_json_to_custom_csv.py

import csv
import io
import json
import re

# New header (merged with original fields)
header = '''
变量名,name,_desc,_mark1,_mark2,easyEffectFunc,_effect,_easy,skillTimePos,group,groupPower,ignoreControlVal,immuneBuff,dispelBuff,dispelType,overlayType,overlayLimit,skin,isShow,iconResPath,isIconFrame,effectResPath,effectAniName,effectAniChoose,effectResDelay,effectPos,effectAssignLayer,effectOffsetPos,effectShowOnAttack,onceEffectResPath,onceEffectAniName,onceEffectDelay,onceEffectPos,onceEffectAssignLayer,onceEffectOffsetPos,onceEffectWait,linkEffect,effectOnEnd,holderActionType,textResPath,deepCorrect,triggerPriority,specialVal,specialTarget,ignoreHolder,ignoreCaster,triggerBehaviors,limitTimes,lifeRoundType,lifeTimeEnd,buffshader,waveInherit,craftTriggerLimit,gateLimit,noDelWhenFakeDeath,showExplorer,explorerID,showHeldItem,heldItemID,buffActionEffect,stageArgs,skillName,skillName_tw,skillName_en,skillName_kr,_beizhu,skillTypeShow,skillTypeShow_tw,skillTypeShow_en,describe,describe_tw,describe_en,describe_kr,simDesc,simDesc_tw,simDesc_en,simDesc_kr,starEffect,starEffectDesc,starEffectDesc_tw,starEffectDesc_en,starEffectDesc_kr,zawakeEffect,zawakeEffectDesc,zawakeEffectDesc_tw,zawakeEffectDesc_en,zawakeEffectDesc_kr,zawakeSimpleType,zawakeSimpleDesc,zawakeSimpleDesc_tw,zawakeSimpleDesc_en,zawakeSimpleDesc_kr,upLvDesc,upLvDesc_tw,upLvDesc_en,upLvDesc_kr,iconRes,isGlobal,changeUnitTrigger,isCombat,alwaysEffective,passivePriority,skillType,skillType2,skillDamageType,skillNatureType,skillPower,skillHit,weather,cdRound,startRound,passiveStartRound,passiveTriggerType,passiveTriggerArg,posChoose,moveTime,specialChoose,hitFormula,hintTargetType,hintChoose,specialHintChoose,autoHintChoose,targetTypeDesc,targetChooseType,targetTypeDesc_en,targetTypeDesc_kr,targetTypeDesc_tw,_attacktest,damageFormula,_damageFormula,hpFormula,skillCalDamageProcessId,diffSkillCalDmgProcessId,skillProcess,passiveSkillAttrs,activeType,activeCondition,fightingPoint,costMp1,costMp1Args,recoverMp1,widgetEffects,hurtMp1,costID,posC,chargeArgs,skillArgs,conditionValue,spineAction,flashBack,cameraNear,cameraNear_posC,cameraNear_blankTime,cameraNear_scaleArgs,blankTime,scaleArgs,effectBigName,effectBigPos,effectBigFlip,notShowProcedure,hurtPos,sound,allEffectTime
'''.strip().split(',')

# Raw input JSON
raw_text = '''
{
  "id": 3771120,
  "name": "超坏星",
  "overlayType": 1,
  "overlayLimit": 1,
  "isIconFrame": 1,
  "triggerBehaviors": "{{['effectFuncs'] = {'castBuff', 'castBuff', 'castBuff'}, ['triggerPoint'] = 1, ['funcArgs'] = {{{['holder'] = 1, ['lifeRound'] = 3, ['value'] = 'self:defence()*0.4+self:specialDefence()*0.4', ['cfgId'] = 3771111, ['caster'] = 2, __size = 5}}, {{['holder'] = 2, ['lifeRound'] = 2, ['value'] = 'self:defence()*0.18', ['cfgId'] = 3771118, ['caster'] = 2, __size = 5}}, {{['holder'] = 2, ['lifeRound'] = 2, ['value'] = 'self:specialDefence()*0.18', ['cfgId'] = 3771119, ['caster'] = 2, __size = 5}}}, ['nodeId'] = 1, __size = 4}}"
}
'''

parsed_data = json.loads(raw_text)

DEFAULT_VALUE = ''

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

def parse_trigger_behaviors(text):
    # Chuyển về JSON-like syntax
    text = text.replace("__size", '"__size"')
    text = re.sub(r"\[(['\"]?)(\w+)\1\]", r'"\2"', text)  # ["key"] => "key"
    text = text.replace("=", ":")
    text = text.replace("'", '"')
    text = text.replace("{{", "[").replace("}}", "]")

    try:
        obj = json.loads(text)
    except Exception as e:
        print("⚠️ Parse lỗi:", e)
        return text  # fallback về nguyên gốc

    def fmt(val):
        if isinstance(val, dict):
            return "{" + ";".join(f"{k}={fmt(v)}" for k, v in val.items() if k != "__size") + "}"
        elif isinstance(val, list):
            return "<" + ";".join(fmt(v) for v in val) + ">"
        else:
            return str(val)

    return fmt(obj)

csv_line = {
    '变量名': parsed_data.get('id', ''),
    'name': parsed_data.get('skillName', ''),
    '_desc': parsed_data.get('describe', ''),
    '_mark1': parsed_data.get('_mark1', ''),
    '_mark2': parsed_data.get('_mark2', ''),
    'easyEffectFunc': parsed_data.get('easyEffectFunc', ''),
    '_effect': parsed_data.get('_effect', ''),
    '_easy': parsed_data.get('_easy', ''),
    'skillTimePos': parsed_data.get('skillTimePos', ''),
    'group': parsed_data.get('group', ''),
    'groupPower': parsed_data.get('groupPower', ''),
    'ignoreControlVal': parsed_data.get('ignoreControlVal', ''),
    'immuneBuff': parsed_data.get('immuneBuff', ''),
    'dispelBuff': parsed_data.get('dispelBuff', ''),
    'dispelType': parsed_data.get('dispelType', ''),
    'overlayType': parsed_data.get('overlayType', ''),
    'overlayLimit': parsed_data.get('overlayLimit', ''),
    'skin': parsed_data.get('skin', ''),
    'isShow': parsed_data.get('isShow', ''),
    'iconResPath': parsed_data.get('iconRes', ''),
    'isIconFrame': parsed_data.get('isIconFrame', ''),
    'effectResPath': parsed_data.get('effectResPath', ''),
    'effectAniName': parsed_data.get('effectAniName', ''),
    'effectAniChoose': parsed_data.get('effectAniChoose', ''),
    'effectResDelay': parsed_data.get('effectResDelay', ''),
    'effectPos': parsed_data.get('effectPos', ''),
    'effectAssignLayer': parsed_data.get('effectAssignLayer', ''),
    'effectOffsetPos': parsed_data.get('effectOffsetPos', ''),
    'effectShowOnAttack': parsed_data.get('effectShowOnAttack', ''),
    'onceEffectResPath': parsed_data.get('onceEffectResPath', ''),
    'onceEffectAniName': parsed_data.get('onceEffectAniName', ''),
    'onceEffectDelay': parsed_data.get('onceEffectDelay', ''),
    'onceEffectPos': parsed_data.get('onceEffectPos', ''),
    'onceEffectAssignLayer': parsed_data.get('onceEffectAssignLayer', ''),
    'onceEffectOffsetPos': parsed_data.get('onceEffectOffsetPos', ''),
    'onceEffectWait': parsed_data.get('onceEffectWait', ''),
    'linkEffect': parsed_data.get('linkEffect', ''),
    'effectOnEnd': parsed_data.get('effectOnEnd', ''),
    'holderActionType': parsed_data.get('holderActionType', ''),
    'textResPath': parsed_data.get('textResPath', ''),
    'deepCorrect': parsed_data.get('deepCorrect', ''),
    'triggerPriority': parsed_data.get('triggerPriority', ''),
    'specialVal': parsed_data.get('specialVal', ''),
    'specialTarget': parsed_data.get('specialTarget', ''),
    'ignoreHolder': parsed_data.get('ignoreHolder', ''),
    'ignoreCaster': parsed_data.get('ignoreCaster', ''),
    'triggerBehaviors': parse_trigger_behaviors(parsed_data.get('triggerBehaviors', '')),
    'limitTimes': parsed_data.get('limitTimes', ''),
    'lifeRoundType': parsed_data.get('lifeRoundType', ''),
    'lifeTimeEnd': parsed_data.get('lifeTimeEnd', ''),
    'buffshader': parsed_data.get('buffshader', ''),
    'waveInherit': parsed_data.get('waveInherit', ''),
    'craftTriggerLimit': parsed_data.get('craftTriggerLimit', ''),
    'gateLimit': parsed_data.get('gateLimit', ''),
    'noDelWhenFakeDeath': parsed_data.get('noDelWhenFakeDeath', ''),
    'showExplorer': parsed_data.get('showExplorer', ''),
    'explorerID': parsed_data.get('explorerID', ''),
    'showHeldItem': parsed_data.get('showHeldItem', ''),
    'heldItemID': parsed_data.get('heldItemID', ''),
    'buffActionEffect': parsed_data.get('buffActionEffect', ''),
    'stageArgs': parsed_data.get('stageArgs', ''),
    'skillName': parsed_data.get('skillName', ''),
    'describe': parsed_data.get('describe', ''),
    'simDesc': parsed_data.get('simDesc', ''),
    'starEffectDesc': parsed_data.get('starEffectDesc', ''),
    'zawakeEffect': list_to_str(parsed_data.get('zawakeEffect', '')),
    'zawakeEffectDesc': parsed_data.get('zawakeEffectDesc', ''),
    'zawakeSimpleType': parsed_data.get('zawakeSimpleType', ''),
    'zawakeSimpleDesc': parsed_data.get('zawakeSimpleDesc', ''),
    'upLvDesc': parsed_data.get('upLvDesc', ''),
    'iconRes': parsed_data.get('iconRes', ''),
    'skillNatureType': parsed_data.get('skillNatureType', ''),
    'posChoose': parsed_data.get('posChoose', ''),
    'targetTypeDesc': parsed_data.get('targetTypeDesc', ''),
    'targetChooseType': parsed_data.get('targetChooseType', ''),
    'skillProcess': list_to_str(parse_curly_list(parsed_data.get('skillProcess', ''))),
    'posC': dict_to_custom_string(parsed_data.get('posC', {}), exclude_keys=['__size']),
    'sound': dict_to_custom_string(parsed_data.get('sound', {}), exclude_keys=['__size'])
}

# Ensure all headers exist in csv_line
for key in header:
    csv_line.setdefault(key, DEFAULT_VALUE)

output = io.StringIO()
writer = csv.DictWriter(output, fieldnames=header)
writer.writerow(csv_line)
csv_result = output.getvalue().strip()

with open("tmp.txt", "w", encoding="utf-8", newline="") as f:
    f.write(csv_result)

print("✅ CSV line written with new combined header to tmp.txt")
