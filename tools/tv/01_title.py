# coding:utf-8
import os
import sys
import tvlist
import util
import tvkingdom
import patch
import gtv
import nhk_old
import nhk
import bs5
import bs8

# 先に titles_raw.js と descriptions_raw.js を出力する。よく出てくる物に桁数の小さいIDを与える。

def create_diff(s, start_date, types, name_id, chapter_id, category, splited_by_space, desc_id, title_name, description):
	result, title_omitted, desc_omitted  = util.create_diff(s, start_date, types, name_id, chapter_id, category, splited_by_space, desc_id)

	# 題名や概要の現れる回数をかぞえる
	# ただしキー局の同時間帯と同じ場合はかぞえない
	if name_id != None:
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
	return descriptions[d]["id"]

def get_timetable(year, month, day, area):
	result = util.get_target_html(year, month, day, area)
	if result == 0:
		return

	tvkingdom.checkContent(util.htmldata, year, month, day, area)
	program_parts = tvkingdom.splitByStation(util.htmldata)

	for program_part in program_parts:
		isYesterday = False
		pre_esterday = False
		last_programs_interval = 0
		pre_start_time = ""
		start_time = ""
		station_tag = tvlist.get_station_name_tag(tvkingdom.extractStationName(program_part), area)
		if station_tag == "" or station_tag in util.already:
			continue
		util.already.add(station_tag)

		isFirst = True
		item_parts = tvkingdom.splitByItem(program_part)
		for item_part in item_parts:

			if tvkingdom.extractTitleWithIcons(item_part) == "":
				continue

			# 時刻
			pre_start_time_rollback = start_time
			pre_start_time = start_time
			pre_yesterday = isYesterday
			start_time, isYesterday = tvkingdom.extractStartTime(item_part)
			if start_time == "":
				if not isFirst:
					# 番組情報なし
					start_time = util.add_interval(pre_yesterday, pre_start_time, last_programs_interval)
					# パッチあて(情報なしを埋める)
					add_time, add_code, add_title_with_icon, add_desc, add_interval = patch.pad(station_tag, start_time)
					toDelete, delete_interval = patch.delete(station_tag, start_time)
					if add_time != None:
						add_types, add_title_string = tvkingdom.extractIconsFromTitle(add_title_with_icon)
						add_title_name, add_chapter_name, splited_by_space = util.split_title_chapter(add_title_string, station_tag, year, month)
						add_name_id, add_chapter_id = append_title(add_title_name, add_chapter_name)
						add_desc_id = append_description(add_desc)
						last_programs_interval = add_interval
						create_diff(station_tag, add_time, add_types, add_name_id, add_chapter_id, add_code, splited_by_space, add_desc_id, add_title_name, add_desc)
					elif not toDelete:
						create_diff(station_tag, start_time, [], None, None, None, None, None, None, None)
					else:
						start_time = pre_start_time_rollback
				continue

			# パッチあて(削除)
			toDelete, delete_interval = patch.delete(station_tag, start_time)
			if toDelete:
				if delete_interval != None:
					last_programs_interval += delete_interval
				else:
					last_programs_interval += tvkingdom.extractInterval(start_time, item_part)
				start_time = pre_start_time_rollback
				continue

			# ジャンル
			genre_code = tvkingdom.extractCategoryCode(item_part)
			# 題名(アイコン付き)
			name_with_icon = tvkingdom.extractTitleWithIcons(item_part)
			if name_with_icon == "":
				continue
			# アイコン
			types, title_string = tvkingdom.extractIconsFromTitle(name_with_icon)
			# アイコンを取り除いた題名
			title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, station_tag, year, month)
			# 概要(アイコンを含む場合がある)
			summary_with_icon = tvkingdom.extractDescriptionsWithIcons(item_part)
			types2, summary = tvkingdom.extractIconsFromTitle(summary_with_icon)
			types.extend(types2)

			# 放映時間
			last_programs_interval = tvkingdom.extractInterval(start_time, item_part)

			# パッチあて(修正)
			mod_time, mod_code, mod_title_with_icon, mod_desc, mod_interval = patch.modify(station_tag, start_time)
			if mod_time != None:
				start_time = mod_time
			if mod_code != None:
				genre_code = mod_code
			if mod_title_with_icon != None:
				types, title_string = tvkingdom.extractIconsFromTitle(mod_title_with_icon)
				title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, station_tag, year, month)
			if mod_desc != None:
				summary = mod_desc
			if mod_interval != None:
				last_programs_interval = mod_interval

			# パッチあて(追加)
			if not isYesterday:
				add_list = patch.add(station_tag, pre_start_time, start_time)
				for one in add_list:
					add_types, add_title_string = tvkingdom.extractIconsFromTitle(one["title"])
					add_title_name, add_chapter_name, add_splited_by_space = util.split_title_chapter(add_title_string, station_tag, year, month)
					add_name_id, add_chapter_id = append_title(add_title_name, add_chapter_name)
					add_desc_id = append_description(one["desc"])
					#last_programs_interval = one["interval"]
					create_diff(station_tag, one["time"], add_types, add_name_id, add_chapter_id, one["code"], add_splited_by_space, add_desc_id, add_title_name, one["desc"])

			# ID作成
			name_id, chapter_id = append_title(title_name, chapter_name)
			desc_id = append_description(summary)

			create_diff(station_tag, start_time, types, name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, summary)
			isFirst = False

		# パッチあて(末尾に追加)
		add_list = patch.add(station_tag, start_time, None)
		for one in add_list:
			add_types, add_title_string = tvkingdom.extractIconsFromTitle(one["title"])
			add_title_name, add_chapter_name, splited_by_space = util.split_title_chapter(add_title_string, station_tag, year, month)
			add_name_id, add_chapter_id = append_title(add_title_name, add_chapter_name)
			add_desc_id = append_description(one["desc"])
			create_diff(station_tag, one["time"], add_types, add_name_id, add_chapter_id, one["code"], splited_by_space, add_desc_id, add_title_name, one["desc"])

def get_timetable_ouj(year, month, day):
	result = util.get_target_html(year, month, day, "OUJ")
	if result == 0:
		return

	ouj.checkContent(util.htmldata, year, month, day)
	program_part = ouj.extractOujOn(util.htmldata)

	item_parts = ouj.splitByItem(program_part)
	for item_part in item_parts:
		# 時刻
		start_time = ouj.extractStartTime(item_part)
		# ジャンル
		genre_code = ouj.getCategoryCode()
		# アイコン
		types = []
		# 題名
		title_string = ouj.extractTitle(item_part)
		if title_string == "":
			continue
		title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, "OU2", year, month)
		name_id, chapter_id = append_title(title_name, chapter_name)
		# 概要
		summary = ouj.extractDescriptions(item_part)
		desc_id = append_description(summary)

		chunk = create_diff("OU2", start_time, types, name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, summary)

def get_timetable_mxtv(year, month, day):
	if "MX2" in util.already:
		return
	result = util.get_target_html(year, month, day, "MX")
	if result == 0:
		return

	mxtv.checkContent(util.htmldata, year, month, day)
	program_part = util.htmldata

	item_parts = mxtv.splitByItem(program_part)
	for item_part in item_parts:
		# 時刻
		start_time = mxtv.extractStartTime(item_part)
		# アイコン
		types = mxtv.extractIcons(item_part)
		# 題名
		title_string = mxtv.extractTitle(item_part)
		if title_string == "":
			continue
		title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, "MX2", year, month)
		name_id, chapter_id = append_title(title_name, chapter_name)
		# ジャンル
		genre_code = mxtv.getCategoryCode(title_name)
		# 概要
		summary = mxtv.extractDescriptions(item_part)
		desc_id = append_description(summary)

		chunk = create_diff("MX2", start_time, types, name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, summary)

def get_timetable_gtv(year, month, day):
	result = util.get_target_html(year, month, day, "GTV")
	if result == 0:
		return

	gtv.checkContent(util.htmldata, year, month, day)
	program_part = gtv.extractTodays(util.htmldata)

	item_parts = gtv.splitByItem(program_part)
	start_time = None
	for item_part in item_parts:
		# 時刻
		start_time = gtv.extractStartTime(item_part)
		if start_time == "":
			continue

		# パッチあて(削除)
		toDelete, delete_interval = patch.delete("GTV2", start_time)
		if toDelete:
			continue

		# 題名
		title_with_icon = gtv.extractTitle(item_part)
		if title_with_icon == "":
			continue
		# アイコン
		types, title_string = tvkingdom.extractIconsFromTitle(title_with_icon)
		# 題名
		title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, "GTV2", year, month)
		# ジャンル
		genre_code = gtv.getCategoryCode(title_name)
		# 概要
		summary = gtv.getDescription(title_name)

		# パッチあて(修正)
		mod_time, mod_code, mod_title_with_icon, mod_desc, mod_interval = patch.modify("GTV2", start_time)
		if mod_time != None:
			start_time = mod_time
		if mod_code != None:
			genre_code = mod_code
		if mod_title_with_icon != None:
			types, title_string = tvkingdom.extractIconsFromTitle(mod_title_with_icon)
			title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, "GTV2", year, month)
		if mod_desc != None:
			summary = mod_desc
		if mod_interval != None:
			last_programs_interval = mod_interval

		# ID作成
		name_id, chapter_id = append_title(title_name, chapter_name)
		desc_id = append_description(summary)

		chunk = create_diff("GTV2", start_time, types, name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, summary)

	name_id, chapter_id = append_title("この時間は031chをご覧ください。", None)
	desc_id = append_description("録画は031chで行ってください。")
	chunk = create_diff("GTV2", "0000", [], name_id, chapter_id, "115115", False, desc_id, "この時間は031chをご覧ください。", "録画は031chで行ってください。")

	# パッチあて(末尾に追加)
	add_list = patch.add("GTV2", start_time, None)
	for one in add_list:
		add_types, add_title_string = tvkingdom.extractIconsFromTitle(one["title"])
		add_title_name, add_chapter_name, splited_by_space = util.split_title_chapter(add_title_string, "GTV2", year, month)
		add_name_id, add_chapter_id = append_title(add_title_name, add_chapter_name)
		add_desc_id = append_description(one["desc"])
		create_diff("GTV2", one["time"], add_types, add_name_id, add_chapter_id, one["code"], splited_by_space, add_desc_id, add_title_name, one["desc"])

def get_timetable_mietv(year, month, day):
	result = util.get_target_html(year, month, day, "MTV")
	if result == 0:
		return

	mietv.checkContent(util.htmldata, year, month, day)
	program_part = mietv.extractMtv2(util.htmldata)

	item_parts = mietv.splitByItem(program_part)
	for item_part in item_parts:
		# 時刻
		start_time = mietv.extractStartTime(item_part)
		if start_time == "":
			continue
		# アイコン付き題名
		title_with_icon = mietv.extractTitleWithIcons(item_part)
		if title_with_icon == "":
			continue
		# アイコン
		types, title_string = mietv.extractIcons(title_with_icon)
		# 題名
		title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, "MTV2", year, month)
		name_id, chapter_id = append_title(title_name, chapter_name)
		# ジャンル
		genre_code = mietv.getCategoryCode(title_name)
		# 概要
		summary = mietv.extractDescriptions(item_part)
		desc_id = append_description(summary)

		chunk = create_diff("MTV2", start_time, types, name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, summary)

def get_timetable_suntv(year, month, day):
	result = util.get_target_html(year, month, day, "SUN")
	if result == 0:
		return

	suntv.checkContent(util.htmldata, year, month, day)
	program_part = suntv.extractTodays(util.htmldata)

	item_parts = suntv.splitByItem(program_part)
	for item_part in item_parts:
		# 時刻
		start_time = suntv.extractStartTime(item_part)
		if start_time == "":
			continue
		# アイコン
		types = suntv.extractIcons(item_part)
		# 題名
		title_string = suntv.extractTitle(item_part)
		title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, "SUN2", year, month)
		name_id, chapter_id = append_title(title_name, chapter_name)
		# ジャンル
		genre_code = suntv.getCategoryCode(title_name)
		# 概要
		summary = suntv.extractDescription(item_part)
		desc_id = append_description(summary)

		chunk = create_diff("SUN2", start_time, types, name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, summary)

def get_timetable_nhk_old(year,month,day,nhk_area):
	result = util.get_target_html(year, month, day, "NHK"+nhk_area)
	if result == 0:
		return

	#print(nhk_area)
	nhk_old.checkContent(util.htmldata, year, month, day, nhk_area)

	station_tags = nhk_old.getTargetPrograms(nhk_area)
	rowspan = [0,0,0,0,0,0,0,0,0,0,0,0]

	program_part = nhk_old.extractTodays(util.htmldata)
	program_cells = nhk_old.splitByItem(program_part)

	for program_cell in program_cells:

		# 放映時間
		interval = nhk_old.getInterval(program_cell)
		# サブチャンネル放送があるか
		colspan = nhk_old.getColspan(program_cell)

		idx = 0
		min_row = 10000
		for i in reversed(range(12)):
			if min_row >= rowspan[i]:
				min_row = rowspan[i]
				idx = i
		rowspan[idx] += interval
		if colspan == 2:
			rowspan[idx+1] += interval

		if (idx == 0 or idx == 2) and colspan == 1:
			g_main_start_time = nhk_old.extractStartTime(program_cell, rowspan[idx])
			g_main_interval = interval
			g_main_title = nhk_old.extractTitle(program_cell)

		if station_tags[idx] == "":
			continue

		# 時刻
		start_time = nhk_old.extractStartTime(program_cell, rowspan[idx])

		# パッチあて(削除)
		toDelete, delete_interval = patch.delete(station_tags[idx], start_time)
		if toDelete:
			continue

		if start_time == "" or start_time >= "2859":

			# パッチあて(追加)
			pad_minute_from = (rowspan[idx]-interval-45)%60
			pad_hour_from = (int)((rowspan[idx]-interval-45-pad_minute_from)/60)+5
			pad_minute_from_str = str(pad_minute_from)
			if pad_hour_from < 10:
				pad_hour_from_str = "0" + str(pad_hour_from)
			else:
				pad_hour_from_str = str(pad_hour_from)
			if pad_minute_from < 10:
				pad_minute_from_str = "0" + str(pad_minute_from)
			else:
				pad_minute_from_str = str(pad_minute_from)

			pad_minute_to = (rowspan[idx]-45)%60
			pad_hour_to = (int)((rowspan[idx]-45-pad_minute_to)/60)+5
			pad_minute_to_str = str(pad_minute_to)
			if pad_hour_to < 10:
				pad_hour_to_str = "0" + str(pad_hour_to)
			else:
				pad_hour_to_str = str(pad_hour_to)
			if pad_minute_to < 10:
				pad_minute_to_str = "0" + str(pad_minute_to)
			else:
				pad_minute_to_str = str(pad_minute_to)
			pad_from = pad_hour_from_str+pad_minute_from_str
			pad_to = pad_hour_to_str+pad_minute_to_str

			if pad_from == "0415":
				pad_from = nhk_old.get_first_time(station_tags[idx])

			add_time, add_code, add_title_with_icon, add_desc, add_interval = patch.pad(station_tags[idx], pad_from)
			if add_time != None:
				add_types, add_title_string = tvkingdom.extractIconsFromTitle(add_title_with_icon)
				add_title_name, add_chapter_name, splited_by_space = util.split_title_chapter(add_title_string, station_tags[idx], year, month)
				add_name_id, add_chapter_id = append_title(add_title_name, add_chapter_name)
				add_desc_id = append_description(add_desc)
				create_diff(station_tags[idx], add_time, add_types, add_name_id, add_chapter_id, add_code, splited_by_space, add_desc_id, add_title_name, add_desc)

				add_list = patch.add(station_tags[idx], pad_from, pad_to)
				for one in add_list:
					add_types, add_title_string = tvkingdom.extractIconsFromTitle(one["title"])
					add_title_name, add_chapter_name, splited_by_space = util.split_title_chapter(add_title_string, station_tags[idx], year, month)
					add_name_id, add_chapter_id = append_title(add_title_name, add_chapter_name)
					add_desc_id = append_description(one["desc"])
					create_diff(station_tags[idx], one["time"], add_types, add_name_id, add_chapter_id, one["code"], splited_by_space, add_desc_id, add_title_name, one["desc"])

			continue

		# アイコン
		types = nhk_old.extractIcons(program_cell)

		# 題名
		title_string = nhk_old.extractTitle(program_cell)
		if (idx == 1 or idx == 3) and g_main_start_time == start_time and g_main_interval == interval and g_main_title == title_string:
			# 同じ番組なのにメインとサブに分かれた変な重複があるので、それを除外する
			continue
		title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, station_tags[idx], year, month)
		name_id, chapter_id = append_title(title_name, chapter_name)

		# ジャンル
		genre_code = nhk_old.getCategoryCode(title_name)

		# 概要
		description = nhk_old.extractDescription(program_cell)
		desc_id = append_description(description)

		bar = create_diff(station_tags[idx], start_time, types, name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, description)



def get_timetable_nhk(year,month,day,nhk_area):
	result = util.get_target_html(year, month, day, "NHK"+nhk_area)
	if result == 0:
		return

	#print(nhk_area)
	nhk.checkContent(util.htmldata, year, month, day, nhk_area)

	station_tags = nhk.getTargetPrograms(nhk_area)
	program_part = nhk.extractTodays(util.htmldata)
	program_cells = nhk.extractItems(program_part)

	idx = 0
	for station_tag in station_tags:
		if station_tag == "":
			idx += 1
			continue

		keysta = util.get_my_key_station(station_tag)
		first_time = util.time_decode_base60(util.standard_programs_timeline[keysta][0])

		items = nhk.extractItemsByChannel(program_cells, idx)
		for item in items:
			# 時刻
			start_time = nhk.extractStartTime(item)
			if start_time == "" or start_time < first_time:
				continue
			# パッチあて(削除)
			toDelete, delete_interval = patch.delete(station_tag, start_time)
			if toDelete:
				continue
			# 放映時間
			interval = nhk.getInterval(item)
			# アイコン
			types = nhk.extractIcons(item)
			# 題名
			title_string = nhk.extractTitle(item)
			title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, station_tag, year, month)
			name_id, chapter_id = append_title(title_name, chapter_name)
			# ジャンル
			genre_code = nhk.getCategoryCode(title_name)
			# 概要
			description = nhk.extractDescription(item)
			desc_id = append_description(description)
			bar = create_diff(station_tag, start_time, types, name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, description)
		idx += 1

		add_list = patch.add(station_tag, None, None)
		for one in add_list:
			add_types, add_title_string = tvkingdom.extractIconsFromTitle(one["title"])
			add_title_name, add_chapter_name, splited_by_space = util.split_title_chapter(add_title_string, station_tag, year, month)
			add_name_id, add_chapter_id = append_title(add_title_name, add_chapter_name)
			add_desc_id = append_description(one["desc"])
			create_diff(station_tag, one["time"], add_types, add_name_id, add_chapter_id, one["code"], splited_by_space, add_desc_id, add_title_name, one["desc"])



def get_timetable_bs4(year, month, day):
	result1 = bs4.get_html_bs141(year, month, day)
	result2 = bs4.get_html_bs142(year, month, day)
	if not result1 or not result2:
		return

	result1 = bs4.extractTimetableOf(bs4.htmldata_bs141, year, month, day)
	result2 = bs4.extractTimetableOf(bs4.htmldata_bs142, year, month, day)
	diff = []
	for r in result2:
		if r not in result1:
			diff.append(r)

	for d in diff:
		# パッチあて(削除)
		toDelete, delete_interval = patch.delete("BN2", d["start"])
		if toDelete:
			continue

		title_name, chapter_name, splited_by_space = util.split_title_chapter(d["title"], "BN2", year, month)
		genre_code = bs4.getCategoryCode(title_name)
		name_id, chapter_id = append_title(title_name, chapter_name)
		desc_id = append_description(" ")
		bar = create_diff("BN2", d["start"], [], name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, " ")

def get_timetable_bs5(year, month, day):
	result = bs5.get_html_bs152(year, month, day)
	if not result:
		return

	result = bs5.extractTimetableOf(bs5.htmldata_bs152, year, month, day)

	for d in result:
		title_name, chapter_name, splited_by_space = util.split_title_chapter(d["title"], "BA2", year, month)
		start_time = d["start"]
		summary = d["desc"]

		name_id, chapter_id = append_title(title_name, chapter_name)
		desc_id = append_description(summary)

		genre_code = bs5.getCategoryCode(title_name)

		bar = create_diff("BA2", start_time, [], name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, summary)

def get_timetable_bs8(year, month, day):
	result1 = bs8.get_html_bs181(year, month, day)
	result2 = bs8.get_html_bs182(year, month, day)
	if not result1 or not result2:
		return

	result1 = bs8.extractTimetableOf(bs8.htmldata_bs181, year, month, day)
	result2 = bs8.extractTimetableOf(bs8.htmldata_bs182, year, month, day)

	diff = []
	for r in result2:
		if r not in result1:
			diff.append(r)

	for d in diff:
		title_name, chapter_name, splited_by_space = util.split_title_chapter(d["title"], "BF2", year, month)
		start_time = d["start"]
		summary = d["desc"]

		# パッチあて(修正)
		mod_time, mod_code, mod_title_with_icon, mod_desc, mod_interval = patch.modify("BF2", start_time)
		if mod_time != None:
			start_time = mod_time
		if mod_desc != None:
			summary = mod_desc

		if mod_code != None:
			genre_code = mod_code
		else:
			genre_code = bs8.getCategoryCode(title_name)

		name_id, chapter_id = append_title(title_name, chapter_name)
		desc_id = append_description(summary)

		bar = create_diff("BF2", start_time, [], name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, summary)

	#パッチあて
	items = patch.add("BF2", None, None)
	for item in items:
		types, title_string = tvkingdom.extractIconsFromTitle(item["title"])
		title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, "BF2", year, month)
		genre_code = item["code"]
		name_id, chapter_id = append_title(title_name, chapter_name)
		desc_id = append_description(item["desc"])
		bar = create_diff("BF2", item["time"], types, name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, item["desc"])

def get_timetable_bs6(year, month, day):
	items = patch.add("BB2", None, None)
	for item in items:
		types, title_string = tvkingdom.extractIconsFromTitle(item["title"])
		title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, "BB2", year, month)
		genre_code = item["code"]
		name_id, chapter_id = append_title(title_name, chapter_name)
		desc_id = append_description(item["desc"])
		bar = create_diff("BB2", item["time"], types, name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, item["desc"])

	items = patch.add("BA2", None, None)
	for item in items:
		types, title_string = tvkingdom.extractIconsFromTitle(item["title"])
		title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, "BA2", year, month)
		genre_code = item["code"]
		name_id, chapter_id = append_title(title_name, chapter_name)
		desc_id = append_description(item["desc"])
		bar = create_diff("BA2", item["time"], types, name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, item["desc"])

	items = patch.add("TVK2", None, None)
	for item in items:
		types, title_string = tvkingdom.extractIconsFromTitle(item["title"])
		title_name, chapter_name, splited_by_space = util.split_title_chapter(title_string, "TVK2", year, month)
		genre_code = item["code"]
		name_id, chapter_id = append_title(title_name, chapter_name)
		desc_id = append_description(item["desc"])
		bar = create_diff("TVK2", item["time"], types, name_id, chapter_id, genre_code, splited_by_space, desc_id, title_name, item["desc"])



if __name__ == "__main__":
	global titles
	global descriptions
	titles = {}
	descriptions = {}

	if len(sys.argv) > 1 and len(sys.argv[1]) == 8:
		util.year = sys.argv[1][:4]
		util.months = [sys.argv[1][4:6]]
		util.days = [sys.argv[1][6:]]

	for month in util.months:
		if not os.path.exists("./" + util.year + "/" + month + "/"):
			continue

		util.get_splitter_data(util.year, month)

		for day in util.days:
			if not os.path.exists("./" + util.year + "/" + month + "/" + day + "/"):
				continue

			util.reset_temporary_data()
			patch.read_patch_file(util.year, month, day)

			for area in util.areas:
				get_timetable(util.year, month, day, area)
			for area in nhk.nhk_areas:
				if (int)(util.year) >= 2025 or (int)(util.year) == 2024 and (int)(month) >= 5 or (int)(util.year) == 2024 and (int)(month) == 4 and (int)(day) == 30:
					get_timetable_nhk(util.year, month, day, area)
				else:
					get_timetable_nhk_old(util.year, month, day, area)
			get_timetable_gtv(util.year, month, day)
			get_timetable_bs5(util.year, month, day)
			get_timetable_bs8(util.year, month, day)
			get_timetable_bs6(util.year, month, day)
			print(util.year + "-" + month + "-" + day)

	score_sorted = sorted(titles.items(), key=lambda x:x[1]["num"], reverse=True)
	if not os.path.isdir("scripts"):
		os.makedirs("scripts")
	outfile = open("scripts/titles_raw.js", 'w')
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
	outfile = open("scripts/descriptions_raw.js", 'w')
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
