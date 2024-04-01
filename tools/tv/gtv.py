# coding:utf-8
import util

def checkContent(html, year, month, day):
	if not "<option value=\"today\">" + str((int)(year)) + "年" + str((int)(month)) + "月" + str((int)(day)) + "日" in html:
		print(year + "_" + month + "_" + day + "_GTV.htmlの内容が間違っています")

def extractTodays(html):
	splited1 = html.split("<div id =\"today\" class=\"today\">")
	splited2 = splited1[1].split("</div>")
	return splited2[0]

# extractTodaysで切り分けたhtmlを与える
def splitByItem(html):
	splited = html.split("<dl")
	splited.pop(0)
	return splited

# splitByItemで切り分けたhtmlを与える
def extractStartTime(html):
	splited1 = html.split("<dt>")
	splited2 = splited1[1].split("</dt>")
	result = splited2[0].replace(":","")
	if len(result) == 3:
		result = "0" + result
	return result

# splitByItemで切り分けたhtmlを与える
def extractTitle(html):
	splited1 = html.split("<p class=\"title\">")
	if len(splited1) == 1:
		return ""
	else:
		splited2 = splited1[1].split("</p>")
		return util.sanitize(splited2[0])

# splitByItemで切り分けたhtmlを与える
def getInterval(html):
	splited1 = html.split("t")
	splited2 = splited1[1].split("\"")
	return (int)(splited2[0])

def isPaddingNeeded(time):
	pre_chunk = ""
	for chunk in util.standard_programs_timeline["GTV"]:
		if time == util.time_decode_base60(chunk):
			return None
		elif pre_chunk != "" and time < util.time_decode_base60(chunk):
			return util.time_decode_base60(pre_chunk)
		pre_chunk = chunk
	return None

def isPaddingNeeded2(time):
	if time == None:
		return None, None

	for chunk in util.standard_programs_timeline["GTV"]:
		if time == util.time_decode_base60(chunk):
			return None, None
		elif time < util.time_decode_base60(chunk):
			return time, util.get_interval(time, util.time_decode_base60(chunk))
	return None, None

def getCategoryCode(title_name):
	if title_name == "お天気情報":
		return "100101"
	elif title_name == "ライブビュー&ミュージック":
		return "104100"
	elif title_name == "読売デジタルニュース":
		return "100100"
	elif "野球" in title_name or "ライオンズ" in title_name:
		return "101101"
	elif "サッカー" in title_name:
		return "101102"
	elif "クレインサンダーズ" in title_name or "バレー" in title_name:
		return "101104"
	elif "オートレース" in title_name or "川口オート" in title_name:
		return "101108"
	elif "テレビショッピング" in title_name:
		return "102104"
	else:
		return "115115"

def getDescription(title_name):
	if title_name == "お天気情報":
		return "▽降水量や風向きなど最新の気象情報から県内全市町村のポイント予報まで！▽くらしに密着したお天気情報をお届けします"
	elif title_name == "ライブビュー&ミュージック":
		return "▽今の天気は?道路の様子は?▽ぐんまの「今」を音楽とともにライブ映像でお送りします"
	elif title_name == "読売デジタルニュース":
		return "▽読売新聞の取材網による国内外の最新ニュース▽社会・政治・経済の話題から国際・スポーツ・文化まで"
	else:
		return ""
