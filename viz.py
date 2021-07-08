import json
import re

import jsondiff
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

# dict_ = {}
def skip_none(arr):
  #print("arr", arr)
  out = ''
  for el in arr:
    #print(el)
    if el != None:
      out = el
  return out


def viz(str_num, date, line, matches, dict_num_day_ordinal,
        dict_quarter_ordinal,
        dict_quarter_cardinal,
        dict_year_modifier,
        dict_year_cardinal,
        dict_week_ordinal,
        dict_week_cardinal,
        dict_month_modifier,
        dict_date,
        dict_day_cardinal,
        dict_month_ordinal,
        dict_month_cardinal,
        dict_week_modifier, dict_count, dict_day_modifier, dict_half_year,dict_year_ordinal,
             dict_quarter_modifier, id):
    #print(len(matches))
    dict_result = {}
    dict_num = 0
    date_d = {}

    result = {}
    split_index = []
    #split_index.append(0)
    for m in re.finditer(r' со | с | по | до |за | по | в |после ', line):
        index = m.start()
        split_index.append(index)
        #split_on_date = re.split(r'с |по | до ', line)
    if len(split_index) == 0:
        split_index.append(0)
    split_index.append(len(line))
    #print("INTERVALS ", split_index)
    num_split = 0
    for split_loc in split_index:
        num_split = num_split + 1
    interval = []
    result["id"] = str(id)
    id = id +1
    r = {}
    res_atr = []
    out= {}
    id_interval = 0
    #r["DI_count"] = len(split_index)-1
    # фильтровать повторяющиеся мэтчи
    matches_arr = []
    match_num = -1
    for match in matches:
        match_num = match_num + 1
        matches_arr.append(match)
        if match_num != 0:

            match1 = matches_arr[match_num-1].fact.as_json
            match2 = matches_arr[match_num].fact.as_json
            diff_match = jsondiff.diff(match1, match2)
            if len(diff_match) == 0:
                continue
        for i in range(len(split_index)):

        #for match in matches:

            if match.span.start >= split_index[i] and match.span.stop <= split_index[i+1]:

                #if match.span.start<:
                dict_num = dict_num + 1
                dict_match = {}
                val = []
                # interval_index = 1
                # num_di = 0
                # for split in split_index:
                #     num_di = num_di + 1
                #     if split < match.span.stop:
                #         interval_index = num_di
                #         break

                #for m in re.finditer(r'с |по | до ', line):
                #    index, item = m.start(), m.group()
                #    print(index, m, item)
                #dict_match["DI_count"] = len()
                dict_match["start"] = match.span.start
                dict_match["stop"] = match.span.stop
                annotationText = ''
                for tok in match.tokens:
                    annotationText = annotationText +" "+tok.value
                dict_match["annotationText"] = annotationText
                dict_match["word"] = match.tree.root.main.value
                before = morph.parse(match.tokens[0].value)[0]
                p = morph.parse(match.tokens[0].normalized)[0]
                try:
                    d_list = list(match.fact.as_json.items())
                    dict_match["entity"] = list(match.fact.as_json.items())[0][0]
                    dict_match["value"] = list(match.fact.as_json.items())[0][1]

                    #print(isinstance(dict_match["value"], int))

                        #print("DAAAAAte")
                    if (re.search("ordinal", dict_match["entity"])) and (p.tag.POS == 'NUMR') and (before.tag.POS == "ADJF") :
                        dict_match["entity_cardinal"] = dict_match["entity"].replace("ordinal", "cardinal")

                        dict_match["value_cardinal"] = 1
                    if (re.search("ordinal", dict_match["entity"])):
                        if (re.search("year", dict_match["entity"])):
                            date_d["year{}".format(dict_num)] = dict_match["value"]
                        if (re.search("month", dict_match["entity"])):
                            date_d["month{}".format(dict_num)] = dict_match["value"]
                    dict_result[dict_num] = dict_match
                #print("DATE",date)
                #dict_match["date"] = date
                except:
                    dict_match["entity"] = "error"
                    dict_match["value"] = "error"
                    continue



                #dict_match["annotions"] = {dict_match["start"], dict_match["stop"] }
                #result[dict_match["entity"]] = [dict_match["value"], dict_match["annotions"]]
                #if (p.tag.POS == NUMR):
                result_atr = {
                    #("DateInterval{}").format(id_interval):{
                        "value":dict_match["value"],
                        "annotations":{
                            "annotationStart":dict_match["start"],
                            "annotationEnd":dict_match["stop"],
                            "annotationText": dict_match["annotationText"]
                        },
                        #"id_interval":id_interval
                    #}
                }
                #print(result_atr, "______________")

                if (dict_match["entity"]) in result:
                    if result[(dict_match["entity"] )] != result_atr:
                        result[(dict_match["entity"]).replace("_", "_end_")] = [result_atr]
                        #result[(dict_match["entity"]).replace("_", "_start_")] = result[(dict_match["entity"])]

                else:
                    result[(dict_match["entity"])] = [result_atr]
                #print("____________", result)
                r["DateInterval"] = [result]

                #"DI_index": interval_index

        #print(r)
        #print("TAAAAARG", p.tag.POS)
        #dict_result.update(dict_match)
        #print(dict_date1)
        #print(match.tree)
        #json_d.value.append(match.tokens[0].value)
            date.day_modifier.append(match.fact.day_modifier)
            date.half_year.append(match.fact.half_year)
            date.quarter_cardinal.append(match.fact.quarter_cardinal)
            date.quarter_ordinal.append(match.fact.quarter_ordinal)
            date.year_modifier.append(match.fact.year_modifier)
            date.year_cardinal.append(match.fact.year_cardinal)
            date.week_modifier.append(match.fact.week_modifier)
            date.week_ordinal.append(match.fact.week_ordinal)
            date.week_cardinal.append(match.fact.week_cardinal)
            date.month_ordinal.append(match.fact.month_ordinal)
            date.month_cardinal.append(match.fact.month_cardinal)
            date.month_modifier.append(match.fact.month_modifier)
            date.day_cardinal.append(match.fact.day_cardinal)
            date.day_ordinal.append(match.fact.day_ordinal)
            date.start_date.append(match.fact.start_date)
            date.end_date.append(match.fact.end_date)
            date.day_modifier.append(match.fact.day_modifier)
            date.half_year.append(match.fact.half_year)
            date.count.append(match.fact.count)
            date.date.append(match.fact.date)
            date.year_ordinal.append(match.fact.date)
            date.quarter_modifier.append(match.fact.date)
            # date.day.append(match.fact.day)
        if len(str(skip_none(date.quarter_modifier))) > 0:
            print("quarter_modifier: ", skip_none(date.quarter_modifier))
            dict_quarter_modifier["{}".format(line)] = skip_none(date.quarter_modifier)
        if len(str(skip_none(date.year_ordinal))) > 0:
            print("year_ordinal: ", skip_none(date.year_ordinal))
            dict_year_ordinal["{}".format(line)] = skip_none(date.year_ordinal)

        if len(str(skip_none(date.quarter_cardinal))) > 0:
            print("quarter_cardinal: ", skip_none(date.quarter_cardinal))
            dict_quarter_cardinal["{}".format(line)] = skip_none(date.quarter_cardinal)
        if len(str(skip_none(date.quarter_ordinal))) > 0:
            print("quarter_ordinal: ", skip_none(date.quarter_ordinal))
            dict_quarter_ordinal["{}".format(line)] = skip_none(date.quarter_ordinal)
        if len(str(skip_none(date.year_modifier))) > 0:
            print("year_modifier: ", skip_none(date.year_modifier))
            dict_year_modifier["{}".format(line)] = skip_none(date.year_modifier)
        if len(str(skip_none(date.year_cardinal))) > 0:
            print("year_cardinal: ", skip_none(date.year_cardinal))
            dict_year_cardinal["{}".format(line)] = skip_none(date.year_cardinal)

        if len(str(skip_none(date.date))) > 0:
            print("date: ", skip_none(date.date))
            dict_date["{}".format(line)] = skip_none(date.date)
        if len(str(skip_none(date.week_ordinal))) > 0:
            print("week_ordinal: ", skip_none(date.week_ordinal))
            dict_week_ordinal["{}".format(line)] = skip_none(date.week_ordinal)
        if len(str(skip_none(date.week_cardinal))) > 0:
            print("week_cardinal: ", skip_none(date.week_cardinal))
            dict_week_cardinal["{}".format(line)] = skip_none(date.week_cardinal)
        if len(str(skip_none(date.week_modifier))) > 0:
            print("week_modifier: ", skip_none(date.week_modifier))
            dict_week_modifier["{}".format(line)] = skip_none(date.week_modifier)
        if len(str(skip_none(date.month_ordinal))) > 0:
            print("month_ordinal: ", skip_none(date.month_ordinal))
            dict_month_ordinal["{}".format(line)] = skip_none(date.month_ordinal)
        if len(str(skip_none(date.month_cardinal))) > 0:
            print("month_cardinal: ", skip_none(date.month_cardinal))
            dict_month_cardinal["{}".format(line)] = skip_none(date.month_cardinal)
        if len(str(skip_none(date.month_modifier))) > 0:
            print("month_modifier: ", skip_none(date.month_modifier))
            dict_month_modifier["{}".format(line)] = skip_none(date.month_modifier)
        if len(str(skip_none(date.day_cardinal))) > 0:
            print("day_cardinal: ", skip_none(date.day_cardinal))
            dict_day_cardinal["{}".format(line)] = skip_none(date.day_cardinal)
        if len(str(skip_none(date.day_ordinal))) > 0:
            print("day_ordinal: ", skip_none(date.day_ordinal))
            dict_num_day_ordinal["{}".format(line)] = skip_none(date.day_ordinal)
        if len(str(skip_none(date.start_date))) > 0:
            print("start_date: ", skip_none(date.start_date))
            dict_start_date["{}".format(line)] = skip_none(date.start_date)
        if len(str(skip_none(date.end_date))) > 0:
            print("end_date: ", skip_none(date.end_date))
            dict_end_date["{}".format(line)] = skip_none(date.end_date)
        if len(str(skip_none(date.day_modifier))) > 0:
            print("day_modifier: ", skip_none(date.day_modifier))
            dict_day_modifier["{}".format(line)] = skip_none(date.day_modifier)
        if len(str(skip_none(date.half_year))) > 0:
            print("half_year: ", skip_none(date.half_year))
            dict_half_year["{}".format(line)] = skip_none(date.half_year)
        if len(str(skip_none(date.count))) > 0:
            print("count: ", skip_none(date.count))
            dict_count["{}".format(line)] = skip_none(date.count)
    #out[]
    return dict_result, date, result, r, id