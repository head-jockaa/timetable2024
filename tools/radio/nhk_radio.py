# coding:utf-8
import radio_util

IMG_RE = "data:image/svg+xml,%3csvg%20width='20'%20height='20'%20viewBox='0%200%2020%2020'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M16.4%202.8C16.841%202.8%2017.2%203.159%2017.2%203.6V16.4C17.2%2016.841%2016.841%2017.2%2016.4%2017.2H3.6C3.159%2017.2%202.8%2016.841%202.8%2016.4V3.6C2.8%203.159%203.159%202.8%203.6%202.8H16.4ZM16.4%202H3.6C2.716%202%202%202.716%202%203.6V16.4C2%2017.284%202.716%2018%203.6%2018H16.4C17.284%2018%2018%2017.284%2018%2016.4V3.6C18%202.716%2017.284%202%2016.4%202Z'%20fill='black'/%3e%3cpath%20d='M9.50794%205.48601H4.93594C4.81594%205.48601%204.44394%205.48601%204.44394%205.03101C4.44394%204.57601%204.81594%204.57501%204.93594%204.57501H15.0759C15.1959%204.57501%2015.5799%204.57501%2015.5799%205.03101C15.5799%205.48701%2015.2079%205.48601%2015.0759%205.48601H10.4559V6.67401H13.1799C14.0919%206.67401%2014.4999%206.97401%2014.4999%207.99401V11.222H15.1479C15.2919%2011.222%2015.6399%2011.234%2015.6399%2011.678C15.6399%2012.086%2015.3639%2012.133%2015.1479%2012.133H14.4999V13.921C14.4999%2015.205%2013.9359%2015.205%2012.5079%2015.205C12.3279%2015.205%2011.7999%2015.205%2011.6559%2015.182C11.3199%2015.146%2011.2599%2014.81%2011.2599%2014.666C11.2599%2014.198%2011.6199%2014.198%2011.8119%2014.198C11.9799%2014.198%2012.8799%2014.222%2012.9039%2014.222C13.2279%2014.222%2013.5159%2014.174%2013.5159%2013.67V12.134H6.50794V14.822C6.50794%2014.966%206.50794%2015.314%206.01594%2015.314C5.54794%2015.314%205.52394%2015.014%205.52394%2014.822V12.134H4.82794C4.70794%2012.134%204.33594%2012.134%204.33594%2011.679C4.33594%2011.319%204.57594%2011.223%204.82794%2011.223H5.52394V7.99501C5.52394%206.98701%205.91994%206.67501%206.84394%206.67501H9.50794V5.48601ZM9.50794%208.90601V7.52601H7.04794C6.69994%207.52601%206.50794%207.68201%206.50794%208.06701V8.90701L9.50794%208.90601ZM9.50794%209.72201H6.50794V11.222H9.50794V9.72201ZM10.4559%208.90601H13.5159V8.06601C13.5159%207.68201%2013.3239%207.52501%2012.9759%207.52501H10.4559V8.90501V8.90601ZM13.5159%209.72201H10.4559V11.222H13.5159V9.72201Z'%20fill='black'/%3e%3c/svg%3e"

def checkContent(html, year, month, day, area):
	if not "href=\"https://www.nhk.jp/timetable/" + area + "/radio/\"" in html or not year + "年" + month + "月" + day + "日に" in html:
		print(year + "_" + month + "_" + day + "_NHK" + area + ".htmlの内容が間違っています")	

def getTargetPrograms(nhk_area):
	result = ["", "", ""]
	if not nhk_area in ["080","090","100","110","120","140","210","240","260","280","290","300"]:
		result[0] = "NHK1_" + nhk_area
	if nhk_area == "130":
		result[1] = "NHK2"
	result[2] = "NHKFM_" + nhk_area

	return result

def extractTodays(html):
	splited = html.split("現在の時刻")
	if len(splited) == 1:
		return ""
	return splited[1]

# extractTodaysで切り分けたhtmlを与える
def extractItems(html):
	splited = html.split("class=\"program-table-td")
	splited.pop(0)
	return splited

# extractItemsで切り分けた配列htmlsを与える
# idx 0...第一 1...第二 2...FM
def extractItemsByChannel(htmls, idx):
	result = []
	for html in htmls:
		if " / " + str(idx*8+2) + " / span " in html:
			result.append(html)
	return result

# extractItemsByChannelで切り分けたhtmlを与える
def getInterval(html):
	splited = html.split(" / span ")
	return (int)(splited[1])

# extractItemsByChannelで切り分けたhtmlを与える
def extractStartTime(html):
	splited = html.split("style=\"grid-area: ")
	splited2 = splited[1].split(" / ")
	rowspan = (int)(splited2[0])

	splited = html.split("class=\"time-td\">")
	if len(splited) == 1:
		return ""
	splited2 = splited[1].split("<")
	splited3 = splited2[0].replace("午前","").replace("午後","").strip()
	start_hour = splited3.split(":")[0]
	start_minute = splited3.split(":")[1]
	if "午後" in splited2[0]:
		start_hour = str((int)(start_hour) + 12)
	elif rowspan >= 1186 and "午前" in splited2[0]:
		start_hour = str((int)(start_hour) + 24)
	elif len(start_hour) == 1:
		start_hour = "0" + start_hour
	return start_hour + start_minute

# extractItemsByChannelで切り分けたhtmlを与える
def extractTitle(html):
	splited1 = html.split("class=\"to-dtl\" href=\"javascript:void(0);\">")
	if len(splited1) == 1:
		return ""
	else:
		splited2 = splited1[1].split("</a>")
		result = splited2[0].replace("［新］","").replace("🈟","").replace("［終］","").replace("🈡","")
		return radio_util.sanitize(result)

# extractItemsByChannelで切り分けたhtmlを与える
def extractDescription(html):
	splited1 = html.split("class=\"arrow\">")
	if len(splited1) == 1:
		return ""
	else:
		splited2 = splited1[1].split("</div>")
		return radio_util.sanitize(splited2[0])

# extractItemsByChannelで切り分けたhtmlを与える
def extractIcons(html):
	types = ""
	if IMG_RE in html:
		types += "R"
	if "［新］" in html:
		types += "N"
	if "🈟" in html:
		types += "N"
	if "［終］" in html:
		types += "F"
	if "🈡" in html:
		types += "F"
	return types
