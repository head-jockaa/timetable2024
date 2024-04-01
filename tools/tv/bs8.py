# coding:utf-8
import os
import util

htmldata_bs181 = None
htmldata_bs182 = None

def get_html_bs181(year, month, day):
	global htmldata_bs181
	w = util.get_week_of_year(year, month, day)
	path = "./" + year + "/" + month + "/" + w + "week_bs181.html"
	if os.path.exists(path):
		f = open(path, 'r')
		htmldata_bs181 = f.read()
		f.close()
		return True

	return False

def get_html_bs182(year, month, day):
	global htmldata_bs182
	w = util.get_week_of_year(year, month, day)
	path = "./" + year + "/" + month + "/" + w + "week_bs182.html"
	if os.path.exists(path):
		f = open(path, 'r')
		htmldata_bs182 = f.read()
		f.close()
		return True

	return False

def extractTimetableOf(html, year, month, day):
	splited1 = html.split("<nav class=\"time_tab weekly")
	splited2 = splited1[1].split("<span>")
	splited2.pop(0)
	target_column = -1
	hit = False
	for s in splited2:
		target_column += 1
		date_string = month + "/" + day
		if date_string[0] == "0":
			date_string = date_string[1:]
		if s.startswith(date_string):
			hit = True
			break
	if not hit:
		return []

	result = []
	pre_int_from = 0
	which_day = 0
	splited1 = html.split("<div class=\"timetable_content\"")
	splited2 = splited1[1].split("<article ")
	splited2.pop(0)

	for a in splited2:

		splited3 = a.split("style=\"grid-row: ")
		splited4 = splited3[1].split("/")
		int_from = (int)(splited4[0])
		splited5 = splited4[1].split(";")
		int_to = (int)(splited5[0])
		interval = int_to - int_from

		if int_from < pre_int_from:
			which_day += 1

		pre_int_from = int_from

		if target_column != which_day:
			continue

		splited3 = a.split("<p class=\"time\">")
		start_time = splited3[1].split("</p>")[0]
		start_time = start_time.replace(":","")
		if len(start_time) < 4:
			start_time = "0" + start_time

		splited3 = a.split("<p class=\"title\">")
		title_name = util.sanitize(splited3[1].split("</p>")[0])

		desc = getDescription(title_name)
		if desc == "":
			splited3 = a.split("<p class=\"text\">")
			if len(splited3) > 1:
				desc = util.sanitize(splited3[1].split("</p>")[0])

		types = []
		icons = ""
		splited3 = a.split("<ul class=\"icons\">")
		if len(splited3) > 1:
			icons = splited3[1].split("</ul>")[0]
			if "生放送" in icons:
				types.append(util.append_type_name("生"))
			if "字幕" in icons:
				types.append(util.append_type_name("字"))
			if "データ放送" in icons:
				types.append(util.append_type_name("デ"))
			if "再放送" in icons:
				types.append(util.append_type_name("再"))
			if "新番組" in icons:
				types.append(util.append_type_name("新"))
			if "最終回" in icons:
				types.append(util.append_type_name("終"))
			if "二カ国語放送" in icons:
				types.append(util.append_type_name("二"))

		result.append({"start":start_time, "interval":interval, "types":types, "title":title_name, "desc": desc})

	return result

def getCategoryCode(title_name):
	if "MUSIC:S" in title_name:
		return "104100"
	if "アニメ" in title_name:
		return "107100"
	elif "ジュエリーライフ" in title_name or "テレビショッピング" in title_name:
		return "102104"
	elif "リモートシェフ" in title_name:
		return "102105"
	elif "野球" in title_name:
		return "101101"
	elif "FIFA" in title_name:
		return "101102"
	elif "ゴルフ" in title_name or "フジサンケイ" in title_name:
		return "101103"
	elif "V.LEAGUE" in title_name:
		return "101104"
	elif "フィギュアスケート" in title_name:
		return "101109"
	elif "KEIBA" in title_name:
		return "101110"
	elif "ワールドツアー" in title_name or "美景" in title_name or "絶景" in title_name:
		return "108101"
	elif "韓ドラ" in title_name:
		return "103101"
	else:
		return "115115"

def getDescription(title):
	if "ジュエリーライフ" in title:
		return "世界から良質なダイヤモンドとカラーストーンを集めて、おしゃれに使えるジュエリーをお求め安い価格でご紹介いたします。"
	elif "ポーランド1" in title:
		return "ポーランドの平原にショパンの面影を求めて\\n〜ワルシャワからウッチまで〜"
	elif "ポーランド2" in title:
		return "黄金色の秋 ポーランド北部の旅\\n〜グルジョンツからソポトまで〜"
	elif "オーストリア1" in title:
		return "オーストリア・ウィーンからバートイシュル\\n〜ハプスブルク帝国の足跡を訪ねて〜"
	elif "オーストリア2" in title:
		return "オーストリア・ザルツブルクからインスブルック\\n〜オーストリアの世界遺産と塩の道を巡って〜"
	elif "イタリア1" in title:
		return "街を彩る、歴史がつくったイタリア建築をめぐる\\n〜ミラノからチビタヴェッキアまで〜"
	elif "イタリア2" in title:
		return "イタリアの壮大な歴史と大自然に触れる\\n〜ローマからアマルフィまで〜"
	elif "オランダ1" in title:
		return "フェルメールが愛したオランダの光\\n〜デン・ハーグからエンクハウゼン〜"
	elif "オランダ2" in title:
		return "オランダで江戸時代の日本を探す\\n〜アムステルダムからロッテルダム〜"
	elif "スペイン1" in title:
		return "スペインケルト文化が残る最果ての地\\n〜オレンセからリバデオまで〜"
	elif "スペイン2" in title:
		return "ドン・キホーテを生んだ黄金世紀\\n〜トレドからアルマグロまで〜"
	elif "ブルガリア1" in title:
		return "ソフィアからカザンラク\\nブルガリア・文化の交差点からバラの谷を目指して"
	elif "ブルガリア2" in title:
		return "スタラ・ザゴラからヴァルナ\\nブルガリアの栄光をたどる旅"
	elif "スロヴェニア1" in title:
		return "リュブリャナからマリボル\\nスロヴェニア 小さな街に息づく自然と文化"
	elif "スロヴェニア2" in title:
		return "クランからコペル\\nスロヴェニア 歴史と自然が奏でるハーモニー"
	elif "ハンガリー1" in title:
		return "ショプロンからブダペスト\\n王冠がつむぐ忠誠の国ハンガリー\\n国境の街ショプロンから首都ブダペストまで"
	elif "ハンガリー2" in title:
		return "ブダペストからセゲド\\n王冠がつむぐ忠誠の国ハンガリー\\nドナウの真珠ブダペストから学術とグルメの町セゲドまで"
	elif "スコットランド1" in title:
		return "グラスゴーからストランラー\\nスコットランド 詩人ロバート・バーンズの面影をもとめて"
	elif "スコットランド2" in title:
		return "エディンバラからファルカーク\\nスコットランド 独立の歴史を辿って"
	elif "ウェールズ1" in title:
		return "チェスターからホーリーヘッド\\n古の歴史と文化が残るウェールズ"
	elif "ウェールズ2" in title:
		return "カナーヴォンからアバラストウィス\\nウェールズが育んだ大地と海"
	elif "アクアリウム1" in title:
		return "人気の水族館に潜入し日常生活では出会うことのない海の生き物たちをたっぷりとご紹介！\\n美ら海水族館（沖縄）"
	elif "アクアリウム2" in title:
		return "人気の水族館に潜入し日常生活では出会うことのない海の生き物たちをたっぷりとご紹介！\\n鴨川シーワールド（千葉）"
	elif "アクアリウム3" in title:
		return "人気の水族館に潜入し日常生活では出会うことのない海の生き物たちをたっぷりとご紹介！\\n名古屋港水族館（愛知）"
	elif "にっぽん名滝探訪1" in title:
		return "四季折々それぞれの地域に根付いた美しい佇まいを見せている滝。そんな個性豊かな滝の中から厳選した名爆の魅力をたっぷりとお届け！\\n袋田の滝（茨城）　払沢の滝（東京）　嫗仙の滝（群馬）　夕日の滝（神奈川）　月待の滝（茨城）"
	elif "にっぽん名滝探訪2" in title:
		return "四季折々それぞれの地域に根付いた美しい佇まいを見せている滝。そんな個性豊かな滝の中から厳選した名爆の魅力をたっぷりとお届け！\\n吹割の滝（群馬）　横川の滝（茨城）　洒水の滝（神奈川）　天狗滝（東京）　綾滝（東京）"
	elif "にっぽん名滝探訪3" in title:
		return "四季折々それぞれの地域に根付いた美しい佇まいを見せている滝。そんな個性豊かな滝の中から厳選した名爆の魅力をたっぷりとお届け！\\nギーザバンタの滝（沖縄）　爆雪の滝（広島）　濃溝の滝（千葉）　白猪の滝（愛媛）　四方木不動の滝（千葉）"
	elif "悠久の時を生きる1" in title:
		return "日本に数多くある島々。日の出から波、森林、動物・・・そして、そこに暮らす人々の生活の様子などを悠久の歴史と大自然が息づく島の様子をお届け！\\n青島（愛媛）　猿島（神奈川）"
	elif "悠久の時を生きる2" in title:
		return "日本に数多くある島々。日の出から波、森林、動物・・・そして、そこに暮らす人々の生活の様子などを悠久の歴史と大自然が息づく島の様子をお届け！\\n古宇利島　久高島　石垣島（沖縄）"
	elif "キッチン百景1" in title:
		return "作っている所を見るだけで食欲を誘う魅力的なグルメをたっぷりと目で見て味わう\\nピッツァ（ピッツェリア　チーロ東中野店）回転寿司（くら寿司　原宿店）キャンディ（パパブブレ中野店）"
	elif "キッチン百景2" in title:
		return "作っている所を見るだけで食欲を誘う魅力的なグルメをたっぷりと目で見て味わう\\nクレープ、焼き鳥、たこ焼き、うなぎ"
	elif "ROAD1" in title:
		return "バイクに乗って日本各地の魅力的な景色や夜景、迫力たっぷりなコースをお届け！ツーリング気分で気分爽快！\\nしまなみ海道　成田モトクロスパーク　首都高速"
	else:
		return ""
