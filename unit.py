import csv
import io

# Header fields
header = '''变量名,name,name_tw,name_en,name_vn,name_kr,attributeType,rarity,natureType,natureType2,twinFlag,battleFlag,rectSize,bossCard_id,bossLife,cardID,star,icon,cardIcon,cardIcon2,iconSimple,cardShow,cardShowScale,cardShowPosC,unitRes,skin,show,bansxScale,bansxPosC,passiveSkillList,skillList,combinationObjCardId,combinationSkillId,everyPos,lifeScale,specBind,killResumeMp1,scale,scaleC,scaleCMode,scaleU,scaleX,scaleSkin,bornTime,rebornTime,deathTime,deathSound,fightingPoint,buffId,buffLifeRound,buffProb,buffLevel,buffValue1,hpGrow,speedGrow,damageGrow,specialDamageGrow,defenceGrow,specialDefenceGrow,hpBaseC,speedBaseC,damageBaseC,defenceBaseC,specialDamageBaseC,specialDefenceBaseC,hpC,mp1C,initMp1C,hpRecoverC,mp1RecoverC,mp2RecoverC,damageC,specialDamageC,defenceC,specialDefenceC,defenceIgnoreC,specialDefenceIgnoreC,speedC,strikeC,strikeDamageC,strikeResistanceC,blockC,breakBlockC,blockPowerC,dodgeC,hitC,damageDodgeC,damageHitC,damageAddC,damageSubC,ultimateAddC,ultimateSubC,damageDeepenC,damageReduceC,suckBloodC,reboundC,cureC,natureRestraintC,controlPerC,immuneControlC,effectPowerId,summonCalDamage'''.split(',')

# Clean input
parsed_data = {
		"id" : 3221,
		"name" : "Hozuki Gengetsu (Mizukage Đệ Nhị)",
		"attributeType" : "base",
		"rarity" : 4,
		"natureType" : 4,
		"cardID" : 3221,
		"icon" : "config/portrait/speedranktouxiang/img_3221.png",
		"cardIcon" : "config/portrait/jinglingtouxiang/img_3221.png",
		"cardIcon2" : "config/portrait/jinglingtouxiang2/img_3221.png",
		"iconSimple" : "config/portrait/simple/img_3221.png",
		"cardShow" : "config/big_hero/normal/img_3221.png",
		"unitRes" : "naruto_huanyue/huanyue.skel",
		"show" : "config/big_hero/normal/img_3221.png",
		"bansxPosC" : "__data_t__bansxPosC",
		"passiveSkillList" : [60032216],
		"skillList" : [60032211, 60032212, 60032213],
		"everyPos" : "__data_t__everyPos",
		"hpGrow" : 60.416,
		"speedGrow" : 1.413,
		"damageGrow" : 12.896,
		"specialDamageGrow" : 14.338,
		"defenceGrow" : 5.04,
		"specialDefenceGrow" : 5.618,
		"hpBaseC" : 1.61,
		"speedBaseC" : 1.57,
		"damageBaseC" : 1.61,
		"defenceBaseC" : 1.57,
		"specialDamageBaseC" : 1.79,
		"specialDefenceBaseC" : 1.75,
		"hpC" : 3585,
		"mp1C" : 1000,
		"initMp1C" : 400,
		"damageC" : 765,
		"specialDamageC" : 1062,
		"defenceC" : 349,
		"specialDefenceC" : 464,
		"defenceIgnoreC" : 0,
		"specialDefenceIgnoreC" : 0,
		"speedC" : 89,
		"strikeDamageC" : 15000,
		"strikeResistanceC" : 1500,
		"blockC" : 1000,
		"blockPowerC" : 3000,
		"damageAddC" : 500,
		"damageSubC" : 1000,
		"ultimateSubC" : 500
	}

def convert_dict_to_custom_format(d: dict) -> str:
    return '{' + f"x={d['x']};y={d['y']}" + '}'

def convert_nested_dict_to_custom_format(d: dict) -> str:
    entries = []
    for key, val in d.items():
        if key.startswith('__'):
            continue
        entry = f"'{key}'={{'x'={val['x']};'y'={val['y']}}}"
        entries.append(entry)
    return '{' + ';'.join(entries) + '}'

bansxPosC = {"y": 10, "x": 10, "__size": 2}
everyPos = {"lifePos" : {"y" : 310, "x" : 0, "__size" : 2}, "namePos" : {"y" : 230, "x" : 0, "__size" : 2}, "headPos" : {"y" : 190, "x" : 0, "__size" : 2}, "hitPos" : {"y" : 105, "x" : 0, "__size" : 2}, "__size" : 4}

# Manual mapping
csv_line = {}
csv_line['变量名'] = parsed_data.get('变量名', parsed_data.get('id', 0))
csv_line['name'] = parsed_data.get('name', '')
csv_line['name_tw'] = parsed_data.get('name_tw', '')
csv_line['name_en'] = parsed_data.get('name_en', '')
csv_line['name_vn'] = parsed_data.get('name_vn', '')
csv_line['name_kr'] = parsed_data.get('name_kr', '')
csv_line['attributeType'] = parsed_data.get('attributeType', '')
csv_line['rarity'] = parsed_data.get('rarity', '')
csv_line['natureType'] = parsed_data.get('natureType', '')
csv_line['natureType2'] = parsed_data.get('natureType2', '')
csv_line['twinFlag'] = parsed_data.get('twinFlag', '')
csv_line['battleFlag'] = parsed_data.get('battleFlag', '')
csv_line['rectSize'] = parsed_data.get('rectSize', '')
csv_line['bossCard_id'] = parsed_data.get('bossCard_id', '')
csv_line['bossLife'] = parsed_data.get('bossLife', '')
csv_line['cardID'] = parsed_data.get('cardID', '')
csv_line['star'] = parsed_data.get('star', '')
csv_line['icon'] = parsed_data.get('icon', '')
csv_line['cardIcon'] = parsed_data.get('cardIcon', '')
csv_line['cardIcon2'] = parsed_data.get('cardIcon2', '')
csv_line['iconSimple'] = parsed_data.get('iconSimple', '')
csv_line['cardShow'] = parsed_data.get('cardShow', '')
csv_line['cardShowScale'] = parsed_data.get('cardShowScale', '')
csv_line['cardShowPosC'] = parsed_data.get('cardShowPosC', '')
csv_line['unitRes'] = parsed_data.get('unitRes', '')
csv_line['skin'] = parsed_data.get('skin', '')
csv_line['show'] = parsed_data.get('show', '')
csv_line['bansxScale'] = parsed_data.get('bansxScale', '')
csv_line['bansxPosC'] = convert_dict_to_custom_format(bansxPosC)
csv_line['passiveSkillList'] = f"<{';'.join(str(x) for x in parsed_data.get('passiveSkillList', []))}>"
csv_line['skillList'] = f"<{';'.join(str(x) for x in parsed_data.get('skillList', []))}>"
csv_line['combinationObjCardId'] = parsed_data.get('combinationObjCardId', '')
csv_line['combinationSkillId'] = parsed_data.get('combinationSkillId', '')
csv_line['everyPos'] = convert_nested_dict_to_custom_format(everyPos)
csv_line['lifeScale'] = parsed_data.get('lifeScale', '')
csv_line['specBind'] = parsed_data.get('specBind', '')
csv_line['killResumeMp1'] = parsed_data.get('killResumeMp1', '')
csv_line['scale'] = parsed_data.get('scale', '')
csv_line['scaleC'] = parsed_data.get('scaleC', '')
csv_line['scaleCMode'] = parsed_data.get('scaleCMode', '')
csv_line['scaleU'] = parsed_data.get('scaleU', '')
csv_line['scaleX'] = parsed_data.get('scaleX', '')
csv_line['scaleSkin'] = parsed_data.get('scaleSkin', '')
csv_line['bornTime'] = parsed_data.get('bornTime', '')
csv_line['rebornTime'] = parsed_data.get('rebornTime', '')
csv_line['deathTime'] = parsed_data.get('deathTime', '')
csv_line['deathSound'] = parsed_data.get('deathSound', '')
csv_line['fightingPoint'] = parsed_data.get('fightingPoint', '')
csv_line['buffId'] = parsed_data.get('buffId', '')
csv_line['buffLifeRound'] = parsed_data.get('buffLifeRound', '')
csv_line['buffProb'] = parsed_data.get('buffProb', '')
csv_line['buffLevel'] = parsed_data.get('buffLevel', '')
csv_line['buffValue1'] = parsed_data.get('buffValue1', '')
csv_line['hpGrow'] = parsed_data.get('hpGrow', '')
csv_line['speedGrow'] = parsed_data.get('speedGrow', '')
csv_line['damageGrow'] = parsed_data.get('damageGrow', '')
csv_line['specialDamageGrow'] = parsed_data.get('specialDamageGrow', '')
csv_line['defenceGrow'] = parsed_data.get('defenceGrow', '')
csv_line['specialDefenceGrow'] = parsed_data.get('specialDefenceGrow', '')
csv_line['hpBaseC'] = parsed_data.get('hpBaseC', '')
csv_line['speedBaseC'] = parsed_data.get('speedBaseC', '')
csv_line['damageBaseC'] = parsed_data.get('damageBaseC', '')
csv_line['defenceBaseC'] = parsed_data.get('defenceBaseC', '')
csv_line['specialDamageBaseC'] = parsed_data.get('specialDamageBaseC', '')
csv_line['specialDefenceBaseC'] = parsed_data.get('specialDefenceBaseC', '')
csv_line['hpC'] = parsed_data.get('hpC', '')
csv_line['mp1C'] = parsed_data.get('mp1C', '')
csv_line['initMp1C'] = parsed_data.get('initMp1C', '')
csv_line['hpRecoverC'] = parsed_data.get('hpRecoverC', '')
csv_line['mp1RecoverC'] = parsed_data.get('mp1RecoverC', '')
csv_line['mp2RecoverC'] = parsed_data.get('mp2RecoverC', '')
csv_line['damageC'] = parsed_data.get('damageC', '')
csv_line['specialDamageC'] = parsed_data.get('specialDamageC', '')
csv_line['defenceC'] = parsed_data.get('defenceC', '')
csv_line['specialDefenceC'] = parsed_data.get('specialDefenceC', '')
csv_line['defenceIgnoreC'] = parsed_data.get('defenceIgnoreC', '')
csv_line['specialDefenceIgnoreC'] = parsed_data.get('specialDefenceIgnoreC', '')
csv_line['speedC'] = parsed_data.get('speedC', '')
csv_line['strikeC'] = parsed_data.get('strikeC', '')
csv_line['strikeDamageC'] = parsed_data.get('strikeDamageC', '')
csv_line['strikeResistanceC'] = parsed_data.get('strikeResistanceC', '')
csv_line['blockC'] = parsed_data.get('blockC', '')
csv_line['breakBlockC'] = parsed_data.get('breakBlockC', '')
csv_line['blockPowerC'] = parsed_data.get('blockPowerC', '')
csv_line['dodgeC'] = parsed_data.get('dodgeC', '')
csv_line['hitC'] = parsed_data.get('hitC', '')
csv_line['damageDodgeC'] = parsed_data.get('damageDodgeC', '')
csv_line['damageHitC'] = parsed_data.get('damageHitC', '')
csv_line['damageAddC'] = parsed_data.get('damageAddC', '0')
csv_line['damageSubC'] = parsed_data.get('damageSubC', '0')
csv_line['ultimateAddC'] = parsed_data.get('ultimateAddC', '0')
csv_line['ultimateSubC'] = parsed_data.get('ultimateSubC', '0')
csv_line['damageDeepenC'] = parsed_data.get('damageDeepenC', '0')
csv_line['damageReduceC'] = parsed_data.get('damageReduceC', '0')
csv_line['suckBloodC'] = parsed_data.get('suckBloodC', '0')
csv_line['reboundC'] = parsed_data.get('reboundC', '')
csv_line['cureC'] = parsed_data.get('cureC', '')
csv_line['natureRestraintC'] = parsed_data.get('natureRestraintC', '')
csv_line['controlPerC'] = parsed_data.get('controlPerC', '')
csv_line['immuneControlC'] = parsed_data.get('immuneControlC', '')
csv_line['effectPowerId'] = parsed_data.get('effectPowerId', '')
csv_line['summonCalDamage'] = parsed_data.get('summonCalDamage', '')

# Xuất ra file
output = io.StringIO()
writer = csv.DictWriter(output, fieldnames=header)
writer.writerow(csv_line)
csv_result = output.getvalue().strip()

with open("unit_tmp.txt", "w", encoding="utf-8", newline="") as f:
    f.write(csv_result + "\n")

print("✅ CSV line written to unit_tmp.txt")
