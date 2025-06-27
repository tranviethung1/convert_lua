import csv
import io
import json

# Header fields
header2 = '''变量名,name,_desc,_mark1,_mark2,easyEffectFunc,_effect,_easy,skillTimePos,group,groupPower,ignoreControlVal,immuneBuff,dispelBuff,dispelType,overlayType,overlayLimit,skin,isShow,iconResPath,isIconFrame,effectResPath,effectAniName,effectAniChoose,effectResDelay,effectPos,effectAssignLayer,effectOffsetPos,effectShowOnAttack,onceEffectResPath,onceEffectAniName,onceEffectDelay,onceEffectPos,onceEffectAssignLayer,onceEffectOffsetPos,onceEffectWait,linkEffect,effectOnEnd,holderActionType,textResPath,deepCorrect,triggerPriority,specialVal,specialTarget,ignoreHolder,ignoreCaster,triggerBehaviors,limitTimes,lifeRoundType,lifeTimeEnd,buffshader,waveInherit,craftTriggerLimit,gateLimit,noDelWhenFakeDeath,showExplorer,explorerID,showHeldItem,heldItemID,buffActionEffect,stageArgs'''.split(',')

# Raw text input
raw_text = '''
{
  "id": 40110921,
  "name": "周年庆245",
  "overlayType": 1,
  "overlayLimit": 1,
  "isIconFrame": 1,
  "effectAniName": "{'qingchu_loop'}",
  "triggerBehaviors": "<{effectFuncs=<castBuff>;triggerPoint=12;funcArgs=<<{caster=2;cfgId=40110922;holder=1;lifeRound=1;value=800}>>;nodeId=1}>"
}
'''

# Parse JSON text
parsed_buff_data = json.loads(raw_text)

# Convert effectAniName if in {'...'} format
if isinstance(parsed_buff_data.get("effectAniName"), str):
    val = parsed_buff_data["effectAniName"]
    if val.startswith("{'") and val.endswith("'}"):
        parsed_buff_data["effectAniName"] = f"<{val[2:-2]}>"

# Manual mapping
buff_csv_line = {}
buff_csv_line['变量名'] = parsed_buff_data.get('id', '')
buff_csv_line['name'] = parsed_buff_data.get('name', '')
buff_csv_line['_desc'] = parsed_buff_data.get('_desc', '')
buff_csv_line['_mark1'] = parsed_buff_data.get('_mark1', '')
buff_csv_line['_mark2'] = parsed_buff_data.get('_mark2', '')
buff_csv_line['easyEffectFunc'] = parsed_buff_data.get('easyEffectFunc', '')
buff_csv_line['_effect'] = parsed_buff_data.get('_effect', '')
buff_csv_line['_easy'] = parsed_buff_data.get('_easy', '')
buff_csv_line['skillTimePos'] = parsed_buff_data.get('skillTimePos', '')
buff_csv_line['group'] = parsed_buff_data.get('group', '')
buff_csv_line['groupPower'] = parsed_buff_data.get('groupPower', '')
buff_csv_line['ignoreControlVal'] = parsed_buff_data.get('ignoreControlVal', '')
buff_csv_line['immuneBuff'] = parsed_buff_data.get('immuneBuff', '')
buff_csv_line['dispelBuff'] = parsed_buff_data.get('dispelBuff', '')
buff_csv_line['dispelType'] = parsed_buff_data.get('dispelType', '')
buff_csv_line['overlayType'] = parsed_buff_data.get('overlayType', '')
buff_csv_line['overlayLimit'] = parsed_buff_data.get('overlayLimit', '')
buff_csv_line['skin'] = parsed_buff_data.get('skin', '')
buff_csv_line['isShow'] = parsed_buff_data.get('isShow', '')
buff_csv_line['iconResPath'] = parsed_buff_data.get('iconResPath', '')
buff_csv_line['isIconFrame'] = parsed_buff_data.get('isIconFrame', '')
buff_csv_line['effectResPath'] = parsed_buff_data.get('effectResPath', '')
buff_csv_line['effectAniName'] = parsed_buff_data.get('effectAniName', '')
buff_csv_line['effectAniChoose'] = parsed_buff_data.get('effectAniChoose', '')
buff_csv_line['effectResDelay'] = parsed_buff_data.get('effectResDelay', '')
buff_csv_line['effectPos'] = parsed_buff_data.get('effectPos', '')
buff_csv_line['effectAssignLayer'] = parsed_buff_data.get('effectAssignLayer', '')
buff_csv_line['effectOffsetPos'] = parsed_buff_data.get('effectOffsetPos', '')
buff_csv_line['effectShowOnAttack'] = parsed_buff_data.get('effectShowOnAttack', '')
buff_csv_line['onceEffectResPath'] = parsed_buff_data.get('onceEffectResPath', '')
buff_csv_line['onceEffectAniName'] = parsed_buff_data.get('onceEffectAniName', '')
buff_csv_line['onceEffectDelay'] = parsed_buff_data.get('onceEffectDelay', '')
buff_csv_line['onceEffectPos'] = parsed_buff_data.get('onceEffectPos', '')
buff_csv_line['onceEffectAssignLayer'] = parsed_buff_data.get('onceEffectAssignLayer', '')
buff_csv_line['onceEffectOffsetPos'] = parsed_buff_data.get('onceEffectOffsetPos', '')
buff_csv_line['onceEffectWait'] = parsed_buff_data.get('onceEffectWait', '')
buff_csv_line['linkEffect'] = parsed_buff_data.get('linkEffect', '')
buff_csv_line['effectOnEnd'] = parsed_buff_data.get('effectOnEnd', '')
buff_csv_line['holderActionType'] = parsed_buff_data.get('holderActionType', '')
buff_csv_line['textResPath'] = parsed_buff_data.get('textResPath', '')
buff_csv_line['deepCorrect'] = parsed_buff_data.get('deepCorrect', '')
buff_csv_line['triggerPriority'] = parsed_buff_data.get('triggerPriority', '')
buff_csv_line['specialVal'] = parsed_buff_data.get('specialVal', '')
buff_csv_line['specialTarget'] = parsed_buff_data.get('specialTarget', '')
buff_csv_line['ignoreHolder'] = parsed_buff_data.get('ignoreHolder', '')
buff_csv_line['ignoreCaster'] = parsed_buff_data.get('ignoreCaster', '')
buff_csv_line['triggerBehaviors'] = parsed_buff_data.get('triggerBehaviors', '')
buff_csv_line['limitTimes'] = parsed_buff_data.get('limitTimes', '')
buff_csv_line['lifeRoundType'] = parsed_buff_data.get('lifeRoundType', '')
buff_csv_line['lifeTimeEnd'] = parsed_buff_data.get('lifeTimeEnd', '')
buff_csv_line['buffshader'] = parsed_buff_data.get('buffshader', '')
buff_csv_line['waveInherit'] = parsed_buff_data.get('waveInherit', '')
buff_csv_line['craftTriggerLimit'] = parsed_buff_data.get('craftTriggerLimit', '')
buff_csv_line['gateLimit'] = parsed_buff_data.get('gateLimit', '')
buff_csv_line['noDelWhenFakeDeath'] = parsed_buff_data.get('noDelWhenFakeDeath', '')
buff_csv_line['showExplorer'] = parsed_buff_data.get('showExplorer', '')
buff_csv_line['explorerID'] = parsed_buff_data.get('explorerID', '')
buff_csv_line['showHeldItem'] = parsed_buff_data.get('showHeldItem', '')
buff_csv_line['heldItemID'] = parsed_buff_data.get('heldItemID', '')
buff_csv_line['buffActionEffect'] = parsed_buff_data.get('buffActionEffect', '')
buff_csv_line['stageArgs'] = parsed_buff_data.get('stageArgs', '')

# Write CSV line
output = io.StringIO()
writer = csv.DictWriter(output, fieldnames=header2)
writer.writerow(buff_csv_line)
csv_result = output.getvalue().strip()

with open("buff_tmp.txt", "w", encoding="utf-8", newline="") as f:
    f.write(csv_result + "\n")

print("✅ Buff CSV line written to buff_tmp.txt")