import os
import util

patch_rule = []

def read_patch_file(year, month, day):
	global patch_rule

	patch_file = []
	path = year + "/" + month + "/" + day + "/" + year + "_" + month + "_" + day + "_patch.txt"
	if os.path.exists(path):
		f = open(path, 'r')
		a = f.read()
		patch_file = a.split("\n")
		f.close()
	else:
		patch_file = []

	patch_rule = []
	hit = False
	stations = ""
	for line in patch_file:
		if line.startswith(">"):
			stations = line.split(" ")[1:]
		elif line.startswith("add"):
			time = line.split(" ")[1]
			patch_rule.append({"stations":stations, "action":"add","time":time,"code":"","title":"","desc":"","interval":0})
		elif line.startswith("modify"):
			splited = line.split(" ")
			time = splited[1]
			if len(splited) == 3:
				new_time = splited[2]
			else:
				new_time = None
			patch_rule.append({"stations":stations, "action":"modify","time":time,"new_time":new_time,"code":None,"title":None,"desc":None,"interval":None})
		elif line.startswith("delete"):
			time = line.split(" ")[1]
			patch_rule.append({"stations":stations, "action":"delete","time":time, "interval":None})
		elif line.startswith("code"):
			code = line.split(" ")[1]
			patch_rule[-1]["code"] = code
		elif line.startswith("title"):
			title = util.sanitize(" ".join(line.split(" ")[1:]))
			patch_rule[-1]["title"] = title
		elif line.startswith("desc"):
			desc = util.sanitize(" ".join(line.split(" ")[1:]))
			patch_rule[-1]["desc"] = desc
		elif line.startswith("interval"):
			interval = line.split(" ")[1]
			patch_rule[-1]["interval"] = (int)(interval)
		elif line.startswith("bs8title"):
			value = line.split(" ")[1]
			if patch_rule[-1]["interval"] == 0:
				patch_rule[-1]["interval"] = 30
			patch_rule[-1]["code"] = getBs8Code(value)
			patch_rule[-1]["title"] = getBs8Title(value)
			patch_rule[-1]["desc"] = getBs8Description(value)

def add(station, pre_start_time, start_time):
	if pre_start_time == None:
		pre_start_time = "0000"
	if start_time == None:
		start_time = "3000"
	if pre_start_time > start_time:
		pre_start_time = "0000"

	result = []
	for rule in patch_rule:
		if station in rule["stations"] and rule["action"] == "add" and rule["time"] > pre_start_time and rule["time"] < start_time:
			result.append({"time":rule["time"], "code":rule["code"], "title":rule["title"], "desc":rule["desc"], "interval":rule["interval"]})

	result_sorted = sorted(result, key=lambda x:x["time"], reverse=False)
	return result_sorted

def pad(station, start_time):
	for rule in patch_rule:
		if station in rule["stations"] and rule["action"] == "add" and rule["time"] == start_time:
			return rule["time"], rule["code"], rule["title"], rule["desc"], rule["interval"]
	return None, None, None, None, None

def modify(station, start_time):
	for rule in patch_rule:
		if station in rule["stations"] and rule["action"] == "modify" and rule["time"] == start_time:
			return rule["new_time"], rule["code"], rule["title"], rule["desc"], rule["interval"]
	return None, None, None, None, None

def delete(station, start_time):
	for rule in patch_rule:
		if station in rule["stations"] and rule["action"] == "delete" and rule["time"] == start_time:
			return True, rule["interval"]
	return False, None

def getBs8Code(value):
	if value == "jewel" or value == "jewel2":
		return "102104"
	else:
		return "104100"

def getBs8Title(value):
	if value == "jewel":
		return "ジュエリーライフNEXT[生]"
	elif value == "jewel2":
		return "麗しの宝石ショッピングConnect"
	elif value == "shower":
		return "Sound Shower"
	elif value == "poland1":
		return "MUSIC:S 欧州鉄道の旅・ポーランド1"
	elif value == "poland2":
		return "MUSIC:S 欧州鉄道の旅・ポーランド2"
	elif value == "austlia1":
		return "MUSIC:S 欧州鉄道の旅・オーストリア1"
	elif value == "austlia2":
		return "MUSIC:S 欧州鉄道の旅・オーストリア2"
	elif value == "italia1":
		return "MUSIC:S 欧州鉄道の旅・イタリア1"
	elif value == "italia2":
		return "MUSIC:S 欧州鉄道の旅・イタリア2"
	elif value == "oranda1":
		return "MUSIC:S 欧州鉄道の旅・オランダ1"
	elif value == "oranda2":
		return "MUSIC:S 欧州鉄道の旅・オランダ2"
	elif value == "spain1":
		return "MUSIC:S 欧州鉄道の旅・スペイン1"
	elif value == "spain2":
		return "MUSIC:S 欧州鉄道の旅・スペイン2"
	elif value == "aqua1":
		return "MUSIC:S 体感！魅惑のアクアリウム1"
	elif value == "aqua2":
		return "MUSIC:S 体感！魅惑のアクアリウム2"
	elif value == "aqua3":
		return "MUSIC:S 体感！魅惑のアクアリウム3"
	elif value == "taki1":
		return "MUSIC:S にっぽん名滝探訪1"
	elif value == "taki2":
		return "MUSIC:S にっぽん名滝探訪2"
	elif value == "taki3":
		return "MUSIC:S にっぽん名滝探訪3"
	elif value == "island1":
		return "MUSIC:S グレートアイランド 悠久の時を生きる1"
	elif value == "island2":
		return "MUSIC:S グレートアイランド 悠久の時を生きる2"
	elif value == "kitchen1":
		return "MUSIC:S キッチン百景1"
	elif value == "kitchen2":
		return "MUSIC:S キッチン百景2"
	elif value == "road1":
		return "MUSIC:S ON THE ROAD1"
	else:
		return ""

def getBs8Description(value):
	if value == "jewel":
		return "世界から良質なダイヤモンドとカラーストーンを集めて、おしゃれに使えるジュエリーをお求め安い価格でご紹介いたします。"
	elif value == "poland1":
		return "ポーランドの平原にショパンの面影を求めて\\n〜ワルシャワからウッチまで〜"
	elif value == "poland2":
		return "黄金色の秋 ポーランド北部の旅\\n〜グルジョンツからソポトまで〜"
	elif value == "austlia1":
		return "オーストリア・ウィーンからバートイシュル\\n〜ハプスブルク帝国の足跡を訪ねて〜"
	elif value == "austlia2":
		return "オーストリア・ザルツブルクからインスブルック\\n〜オーストリアの世界遺産と塩の道を巡って〜"
	elif value == "italia1":
		return "街を彩る、歴史がつくったイタリア建築をめぐる\\n〜ミラノからチビタヴェッキアまで〜"
	elif value == "italia2":
		return "イタリアの壮大な歴史と大自然に触れる\\n〜ローマからアマルフィまで〜"
	elif value == "oranda1":
		return "フェルメールが愛したオランダの光\\n〜デン・ハーグからエンクハウゼン〜"
	elif value == "oranda2":
		return "オランダで江戸時代の日本を探す\\n〜アムステルダムからロッテルダム〜"
	elif value == "spain1":
		return "スペインケルト文化が残る最果ての地\\n〜オレンセからリバデオまで〜"
	elif value == "spain2":
		return "ドン・キホーテを生んだ黄金世紀\\n〜トレドからアルマグロまで〜"
	elif value == "aqua1":
		return "人気の水族館に潜入し日常生活では出会うことのない海の生き物たちをたっぷりとご紹介！\\n美ら海水族館（沖縄）"
	elif value == "aqua2":
		return "人気の水族館に潜入し日常生活では出会うことのない海の生き物たちをたっぷりとご紹介！\\n鴨川シーワールド（千葉）"
	elif value == "aqua3":
		return "人気の水族館に潜入し日常生活では出会うことのない海の生き物たちをたっぷりとご紹介！\\n名古屋港水族館（愛知）"
	elif value == "taki1":
		return "四季折々それぞれの地域に根付いた美しい佇まいを見せている滝。そんな個性豊かな滝の中から厳選した名爆の魅力をたっぷりとお届け！\\n袋田の滝（茨城）　払沢の滝（東京）　嫗仙の滝（群馬）　夕日の滝（神奈川）　月待の滝（茨城）"
	elif value == "taki2":
		return "四季折々それぞれの地域に根付いた美しい佇まいを見せている滝。そんな個性豊かな滝の中から厳選した名爆の魅力をたっぷりとお届け！\\n吹割の滝（群馬）　横川の滝（茨城）　洒水の滝（神奈川）　天狗滝（東京）　綾滝（東京）"
	elif value == "taki3":
		return "四季折々それぞれの地域に根付いた美しい佇まいを見せている滝。そんな個性豊かな滝の中から厳選した名爆の魅力をたっぷりとお届け！\\nギーザバンタの滝（沖縄）　爆雪の滝（広島）　濃溝の滝（千葉）　白猪の滝（愛媛）　四方木不動の滝（千葉）"
	elif value == "island1":
		return "日本に数多くある島々。日の出から波、森林、動物・・・そして、そこに暮らす人々の生活の様子などを悠久の歴史と大自然が息づく島の様子をお届け！\\n青島（愛媛）　猿島（神奈川）"
	elif value == "island2":
		return "日本に数多くある島々。日の出から波、森林、動物・・・そして、そこに暮らす人々の生活の様子などを悠久の歴史と大自然が息づく島の様子をお届け！\\n古宇利島　久高島　石垣島（沖縄）"
	elif value == "kitchen1":
		return "作っている所を見るだけで食欲を誘う魅力的なグルメをたっぷりと目で見て味わう\\nピッツァ（ピッツェリア　チーロ東中野店）回転寿司（くら寿司　原宿店）キャンディ（パパブブレ中野店）"
	elif value == "kitchen2":
		return "作っている所を見るだけで食欲を誘う魅力的なグルメをたっぷりと目で見て味わう\\nクレープ、焼き鳥、たこ焼き、うなぎ"
	elif value == "road1":
		return "バイクに乗って日本各地の魅力的な景色や夜景、迫力たっぷりなコースをお届け！ツーリング気分で気分爽快！\\nしまなみ海道　成田モトクロスパーク　首都高速"
	else:
		return ""


