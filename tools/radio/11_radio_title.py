# coding:utf-8
import os
import sys
import radio_util
import radiolist
import nhk_radio_old
import nhk_radio
import radiko
import bs531

# 先に radio_titles_raw.js と radio_descriptions_raw.js を出力する。よく出てくる物に桁数の小さいIDを与える。

def create_diff(st, start_date, types, name_id, chapter_id, splited_by_space, desc_id, title_name, description):
	result, title_omitted, desc_omitted = radio_util.create_diff(st, start_date, types, name_id, chapter_id, splited_by_space, desc_id)

	# 題名及び概要の現れる回数をかぞえる
	# ただしキー局の同時間帯と同じ場合はかぞえない
	if not title_omitted:
		num = titles[title_name]["num"]
		titles[title_name]["num"] = num + 1
	if not desc_omitted:
		num = descriptions[description]["num"]
		descriptions[description]["num"] = num + 1

	return result

def append_title(title_name, chapter_name):
	if chapter_name == None:
		if title_name not in titles:
			titles[title_name] = {"id":len(titles), "num":0, "ch":{}}
		return titles[title_name]["id"], None
	else:
		if title_name not in titles:
			titles[title_name] = {"id":len(titles), "num":0, "ch":{}}
		if chapter_name not in titles[title_name]["ch"]:
			titles[title_name]["ch"][chapter_name] = {"id":len(titles[title_name]["ch"])}
		return titles[title_name]["id"], titles[title_name]["ch"][chapter_name]["id"]

def append_description(d):
	if d not in descriptions:
		descriptions[d] = {"id":len(descriptions), "num":0}
	return descriptions[d]

def get_timetable_nhk_old(year,month,day,area):
	result = radio_util.get_target_html(year,month,day,"NHK"+area)
	if result == 0:
		return

	nhk_radio_old.checkContent(radio_util.htmldata, year, month, day, area)

	station_tags = nhk_radio_old.getTargetPrograms(area)
	rowspan = [0,0,0]
	isAfternoon = [False, False, False]

	program_part = nhk_radio_old.extractTodays(radio_util.htmldata)
	program_cells = nhk_radio_old.splitByItem(program_part)

	for program_cell in program_cells:

		# 放映時間
		interval = nhk_radio_old.getInterval(program_cell)

		idx = 0
		min_row = 10000
		for i in reversed(range(3)):
			if min_row >= rowspan[i]:
				min_row = rowspan[i]
				idx = i
		rowspan[idx] += interval

		# スキップ
		if station_tags[idx] == "":
			continue

		# 時刻
		start_time, isAfternoon[idx] = nhk_radio_old.extractStartTime(program_cell, isAfternoon[idx])
		if start_time == "":
			continue

		# 題名
		title_string = nhk_radio_old.extractTitle(program_cell)
		title_name, chapter_name, splited_by_space = radio_util.split_title_chapter(title_string, station_tags[idx], year, month)
		name_id, chapter_id = append_title(title_name, chapter_name)

		# 概要
		description = nhk_radio_old.extractDescription(program_cell)
		desc_id = append_description(description)

		# アイコン
		types = nhk_radio_old.extractIcons(program_cell)

		bar = create_diff(station_tags[idx], start_time, types, name_id, chapter_id, splited_by_space, desc_id, title_name, description)

def get_timetable_nhk(year,month,day,area):
	result = radio_util.get_target_html(year,month,day,"NHK"+area)
	if result == 0:
		return

	nhk_radio.checkContent(radio_util.htmldata, year, month, day, area)

	station_tags = nhk_radio.getTargetPrograms(area)
	program_part = nhk_radio.extractTodays(radio_util.htmldata)
	program_cells = nhk_radio.extractItems(program_part)

	idx = 0
	for station_tag in station_tags:
		if station_tag == "":
			idx += 1
			continue

		items = nhk_radio.extractItemsByChannel(program_cells, idx)
		for item in items:
			# 時刻
			start_time = nhk_radio.extractStartTime(item)
			if start_time == "":
				continue
			# 放映時間
			interval = nhk_radio.getInterval(item)
			# アイコン
			types = nhk_radio.extractIcons(item)
			# 題名
			title_string = nhk_radio.extractTitle(item)
			title_name, chapter_name, splited_by_space = radio_util.split_title_chapter(title_string, station_tag, year, month)
			name_id, chapter_id = append_title(title_name, chapter_name)
			# 概要
			description = nhk_radio.extractDescription(item)
			desc_id = append_description(description)
			bar = create_diff(station_tag, start_time, types, name_id, chapter_id, splited_by_space, desc_id, title_name, description)
		idx += 1

def get_timetable(year,month,day,station):
	result = radio_util.get_target_html(year,month,day,station)
	if result == 0:
		return

	radiko.checkContent(radio_util.htmldata, year, month, day, station)

	station_tag = radiolist.get_station_name_tag(radiko.extractStationName(radio_util.htmldata))

	todays_program = radiko.extractTodays(radio_util.htmldata, year, month, day)

	program_parts = radiko.splitByItem(todays_program)
	for program_part in program_parts:

		# 時刻
		start_time, end_time = radiko.extractStartAndEndTime(program_part)

		# 題名(アイコン付き)
		name_with_icon = radiko.extractTitle(program_part)

		# アイコン
		types, title_string = radiko.extractIconsFromTitle(name_with_icon)

		# 題名
		title_name, chapter_name, splited_by_space = radio_util.split_title_chapter(title_string, station_tag, year, month)
		name_id, chapter_id = append_title(title_name, chapter_name)

		# 概要
		description = radiko.extractDescription(program_part)
		desc_id = append_description(description)

		bar = create_diff(station_tag, start_time, types, name_id, chapter_id, splited_by_space, desc_id, title_name, description)

def get_timetable_bs531(year,month,day):
	result = radio_util.get_target_html(year,month,day,"BS531")
	if result == 0:
		return

	bs531.checkContent(radio_util.htmldata, year, month, day)

	todays_program = bs531.extractTodays(radio_util.htmldata, year, month, day)

	program_parts = bs531.splitByItem(todays_program)
	for program_part in program_parts:

		# 時刻
		start_time = bs531.extractStartTime(program_part)

		# 題名
		title_string = bs531.extractTitle(program_part)

		# 題名
		title_name, chapter_name, splited_by_space = radio_util.split_title_chapter(title_string, "HOUSOUDAIGAKU", year, month)
		name_id, chapter_id = append_title(title_name, chapter_name)

		# 概要
		description = bs531.extractDescription(program_part)
		desc_id = append_description(description)

		types = ""
		bar = create_diff("HOUSOUDAIGAKU", start_time, types, name_id, chapter_id, splited_by_space, desc_id, title_name, description)



if __name__ == "__main__":
	global titles
	global descriptions

	if len(sys.argv) > 1 and len(sys.argv[1]) == 8:
		radio_util.year = sys.argv[1][:4]
		radio_util.months = [sys.argv[1][4:6]]
		radio_util.days = [sys.argv[1][6:]]

	titles = {}
	descriptions = {}


	for month in radio_util.months:
		if not os.path.exists("./radio"+radio_util.year+"/"+month+"/"):
			continue

		radio_util.get_splitter_data(radio_util.year, month)

		for day in radio_util.days:
			if not os.path.exists("./radio"+radio_util.year+"/"+month+"/"+day+"/"):
				continue
			radio_util.reset_temporary_data()

			for nhk_area in radio_util.nhk_areas:
				if (int)(radio_util.year) >= 2025 or (int)(radio_util.year) == 2024 and (int)(month) >= 5 or (int)(radio_util.year) == 2024 and (int)(month) == 4 and (int)(day) == 30:
					get_timetable_nhk(radio_util.year,month,day,nhk_area)
				else:
					get_timetable_nhk_old(radio_util.year,month,day,nhk_area)

			for station in radio_util.stations:
				if station == "HOUSOUDAIGAKU":
					if (int)(radio_util.year) >= 2025 or (int)(radio_util.year) == 2024 and (int)(month) >= 4:
						continue
				get_timetable(radio_util.year,month,day,station)

			if (int)(radio_util.year) >= 2025 or (int)(radio_util.year) == 2024 and (int)(month) >= 4:
				get_timetable_bs531(radio_util.year,month,day)

			print(radio_util.year+"-"+month+"-"+day)

	score_sorted = sorted(titles.items(), key=lambda x:x[1]["num"], reverse=True)
	if not os.path.isdir("scripts"):
		os.makedirs("scripts")
	outfile = open("scripts/radio_titles_raw.js", 'w')
	idx = 0
	for s in score_sorted:
		if idx == 0:
			outfile.write("var titles=[")
		else:
			outfile.write(",\n")
		outfile.write("[\"")
		outfile.write(score_sorted[idx][0])
		outfile.write("\"")
		if len(score_sorted[idx][1]["ch"]) != 0:
			outfile.write(",[\"")
			outfile.write("\",\"".join(score_sorted[idx][1]["ch"]))
			outfile.write("\"]")
		outfile.write("]")
		idx += 1
	outfile.write("];")
	outfile.close()

	score_sorted = sorted(descriptions.items(), key=lambda x:x[1]["num"], reverse=True)
	outfile = open("scripts/radio_descriptions_raw.js", 'w')
	idx = 0
	for s in score_sorted:
		if idx == 0:
			outfile.write("var descriptions=[")
		else:
			outfile.write(",\n")
		outfile.write("\"" + score_sorted[idx][0] + "\"")
		idx += 1
	outfile.write("];")
	outfile.close()
