# coding:utf-8
import radio_util

def checkContent(html, year, month, day):
	if not "<time datetime=\"" + year + "-" + month + "-" + day + "\">" in html:
		print(year + "_" + month + "_" + day + "_BS531.htmlの内容が間違っています")

def extractTodays(html, year, month, day):
	splited1 = html.split("<time datetime=\"" + year + "-" + month + "-" + day + "\">")
	splited2 = splited1[1].split("</tbody>")
	return splited2[0]

# extractTodaysで切り分けたhtmlを与える
def splitByItem(html):
	splited = html.split(" aria-label=\"BS531 ")
	splited.pop(0)
	return splited

# splitByItemで切り分けたhtmlを与える
def extractStartTime(html):
	splited = html.split("分\"")
	start_time = splited[0].replace("00時","24時").replace("時","")
	return start_time

# splitByItemで切り分けたhtmlを与える
def extractTitle(html):
	splited1 = html.split("html\">")
	splited2 = splited1[1].split("</a>")
	return radio_util.sanitize(splited2[0])

# splitByItemで切り分けたhtmlを与える
def extractDescription(html):
	splited1 = html.split("<dd class=\"content-professor\">")
	splited2 = splited1[1].split("</dd>")
	return radio_util.sanitize(splited2[0])

	return types, title_string.strip()
