# coding:utf-8
import radio_util

def checkContent(html, year, month, day, station):
	splited1 = html.split("item ui-menu-accordion-title")
	splited2 = splited1[1].split("</a></li>")
	if not year + month + day in splited2[0]:
		print(year + "_" + month + "_" + day + "_" + station + ".htmlの内容が間違っています")

def extractStationName(html):
	splited1 = html.split("class=\"breadcrumb__inner\"")
	splited2 = splited1[1].split("<li>")
	splited3 = splited2[3].split("</li>")
	return splited3[0]

def extractTodays(html, year, month, day):
	splited1 = html.split("class=\"item-outer\" data-day=\"" + year + month + day)
	splited2 = splited1[1].split("class=\"item-outer\" data-day=\"")
	return splited2[0]

# extractTodaysで切り分けたhtmlを与える
def splitByItem(html):
	splited = html.split("--program\" style=\"height: ")
	splited.pop(0)
	return splited

# splitByItemで切り分けたhtmlを与える
def extractStartAndEndTime(html):
	splited1 = html.split("<p class=\"time\">")
	splited2 = splited1[1].split(" ～ ")
	start_time = splited2[0].replace(":","")
	splited3 = splited2[1].split("</p>")
	end_time = splited3[0].replace(":","")
	return start_time, end_time

# splitByItemで切り分けたhtmlを与える
def extractTitle(html):
	splited1 = html.split("<p class=\"title\">")
	splited2 = splited1[1].split("</p>")
	return radio_util.sanitize(splited2[0])

# splitByItemで切り分けたhtmlを与える
def extractDescription(html):
	splited1 = html.split("<p class=\"cast\">")
	splited2 = splited1[1].split("</p>")
	return radio_util.sanitize(splited2[0])

# extractTitleWithIconsの返した文字列を与える
def extractIconsFromTitle(title_string):
	types = ""
	if "【新番組】" in title_string:
		types += "N"
		title_string = title_string.replace("【新番組】","")
	if "【新】" in title_string:
		types += "N"
		title_string = title_string.replace("【新】","")
	if "［新］" in title_string:
		types += "N"
		title_string = title_string.replace("［新］","")
	if "≪新≫" in title_string:
		types += "N"
		title_string = title_string.replace("≪新≫","")
	if "(新)" in title_string:
		types += "N"
		title_string = title_string.replace("(新)","")
	if "【最終回】" in title_string:
		types += "F"
		title_string = title_string.replace("【最終回】","")
	if "【終】" in title_string:
		types += "F"
		title_string = title_string.replace("【終】","")
	if "［終］" in title_string:
		types += "F"
		title_string = title_string.replace("［終］","")
	if "《終》" in title_string:
		types += "F"
		title_string = title_string.replace("《終》","")
	if "(終)" in title_string:
		types += "F"
		title_string = title_string.replace("(終)","")
	if "【再放送】" in title_string:
		types += "R"
		title_string = title_string.replace("【再放送】","")
	if "[再放送]" in title_string:
		types += "R"
		title_string = title_string.replace("[再放送]","")
	if "(再放送)" in title_string:
		types += "R"
		title_string = title_string.replace("(再放送)","")
	if "［再］" in title_string:
		types += "R"
		title_string = title_string.replace("［再］","")
	if "[再]" in title_string:
		types += "R"
		title_string = title_string.replace("[再]","")
	if "(再)" in title_string:
		types += "R"
		title_string = title_string.replace("(再)","")
	if "(再放送)" in title_string:
		types += "R"
		title_string = title_string.replace("(再放送)","")
	if "(再・終)" in title_string:
		types += "RF"
		title_string = title_string.replace("(再・終)","")
	#以下SBSのみ
	if "(特)" in title_string:
		types += "S"
		title_string = title_string.replace("(特)","")
	if "(移)" in title_string:
		types += "M"
		title_string = title_string.replace("(移)","")
	if "(公生)" in title_string:
		types += "L"
		title_string = title_string.replace("(公生)","")
	if "(公開生)" in title_string:
		types += "L"
		title_string = title_string.replace("(公開生)","")
	if "(枠小)" in title_string:
		types += "D"
		title_string = title_string.replace("(枠小)","")
	if "(枠大)" in title_string:
		types += "W"
		title_string = title_string.replace("(枠大)","")
	if "(移・枠小)" in title_string:
		types += "MD"
		title_string = title_string.replace("(移・枠小)","")
	if "(移・枠大)" in title_string:
		types += "MW"
		title_string = title_string.replace("(移・枠大)","")

	return types, title_string.strip()
