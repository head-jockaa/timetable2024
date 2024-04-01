# coding:utf-8
import os
import util

htmldata_bs152 = None

def get_html_bs152(year, month, day):
	global htmldata_bs152
	w = util.get_week_of_year(year, month, day)
	path = "./" + year + "/" + month + "/" + w + "week_bs152.html"
	if os.path.exists(path):
		f = open(path, 'r')
		htmldata_bs152 = f.read()
		f.close()
		return True

	return False

def extractTimetableOf(html, year, month, day):
	splited1 = html.split("class=\"tt_prog cf\" data-type=\"multi\"")
	splited2 = splited1[1].split("data-day=\"" + year + month + day + "\"")
	splited3 = splited2[1].split("</li>")
	splited4 = splited3[0].split("class=\"tt_prog_box")
	splited4.pop(0)

	result = []
	for a in splited4:
		splited5 = a.split("data-start_time=\"")
		start_time = splited5[1].split("\"")[0]

		splited5 = a.split("data-end_time=\"")
		end_time = splited5[1].split("\"")[0]

		interval = util.get_interval(start_time, end_time)

		splited5 = a.split("<h4 class=\"prog-title\">")
		title_name = util.sanitize(splited5[1].split("<")[0])

		splited5 = a.split("<p class=\"prog-description\">")
		desc = util.sanitize(splited5[1].split("<")[0])

		types = []

		result.append({"start":start_time, "interval":interval, "types":types, "title":title_name, "desc": desc})

	return result

def getCategoryCode(title_name):
	if "野球" in title_name or "ベースボール" in title_name or "ドリームプレーヤーズ" in title_name:
		return "101101"
	else:
		return "115115"
