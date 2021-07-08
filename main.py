import json
from datetime import datetime

from date_extractor import ExtractDate
from parser import DATE
from natasha import (
    MorphVocab,
    DatesExtractor
)
from IPython.display import display
from yargy.parser import prepare_trees
import re
from yargy.tokenizer import MorphTokenizer
from yargy import (
    Parser,
    or_, rule
)
from viz import viz
import test, test_all_date
from person_extractor import person_extract
from nltk.tokenize import TweetTokenizer
import pymorphy2
from num_dates import num_date_recognize

morph = pymorphy2.MorphAnalyzer()
tknzr = TweetTokenizer()
lines = ['с февраля по апрель позапрошлого года',
         'за второй квартал предыдущего года',
         'за вторую неделю прошлого месяца',
         'за первую неделю сентября прошлого года',
         'за второй день третьей недели второго квартала',
         'за первый месяц 2020 года',
         'за три недели первого квартала 2019 года',
         'за 4 квартал 2020 года',
         'за три дня',
         'за прошлую неделю',
         'за предыдущий месяц',
         'с апреля 2010 года',
         'после апреля 2010 года',
         'за апрель 2010 года',
         'с мая по июнь 2020 года',
         'с февраля по апрель позапрошлого года',
         'до июня текущего года',
         'за последние три года',
         'в 2018 году',
         'с 01.10 по 01.12',
         'со второй по четвертую неделю первого квартала',
         'со второго квартала 2019 по третий квартал 2020',
         'с января по май 2019 и с первого по третий квартал прошлого года'
         ]

all_tests = [
    'отчет Ивана Иванова и Марии  со второго квартала 2019 по третий квартал 2020  ',
    'справка от Иванова Павла Петровича  и Марии',
    'приказ Павлова',
    'мои отчеты c портала',
    'квитанции Иванова ',
    ' со второго квартала 2019 по третий квартал 2020 ',
    ' за сегодня ',
    ' за вчера ',
    ' за позавчера ',
    ' за последний день ',
    ' за последнюю неделю ',
    ' за последний месяц ',
    ' за последний квартал ',
    ' за последнее полугодие ',
    ' за последний год ',
    ' за последние два дня ',
    ' за последние три недели ',
    ' за последние четыре месяца ',
    ' за последние два квартал ',
    ' за последние три года ',
    ' за прошлый день ',
    ' за прошлую неделю ',
    ' за прошлый месяц ',
    ' за прошлый квартал ',
    ' за прошлое полугодие ',
    ' за прошлый год ',
    ' за два прошлых дня ',
    ' за две прошлых недели ',
    ' за три прошлых месяца ',
    ' за четыре прошлых года ',
    ' за предыдущий день ',
    ' за предыдущую неделю ',
    ' за предыдущий месяц ',
    ' за предыдущий квартал ',
    ' за предыдущее полугодие ',
    ' за предыдущий год ',
    ' за два предыдущих дня ',
    ' за две предыдущих недели ',
    ' за три предыдущих месяца ',
    ' за четыре предыдущих года ',
    ' за день ',
    ' за один день ',
    ' за три дня ',
    ' за десять дней ',
    ' за двадцать дней ',
    ' за 1 день ',
    ' за 3 дня ',
    ' за 10 дней ',
    ' за неделю ',
    ' за одну неделю ',
    ' за три недели ',
    ' за десять недель ',
    ' за 1 неделю ',
    ' за 3 недели ',
    ' за 10 недель ',
    ' за месяц ',
    ' за один месяц ',
    ' за три месяца ',
    ' за десять месяцев ',
    ' за 1 месяц ',
    ' за 2 месяца ',
    ' за 3 месяца ',
    ' за 10 месяцев ',
    ' за квартал ',
    ' за один квартал ',
    ' за три квартала ',
    ' за 1 квартал ',
    ' за 3 месяца ',
    ' за полугодие ',
    ' за два полугодия ',
    ' за 2 полугодия ',
    ' за год ',
    ' за один год ',
    ' за три года ',
    ' за десять лет ',
    ' за 1 год ',
    ' за 3 года ',
    ' три дня назад ',
    ' две недели назад ',
    ' два месяца назад ',
    ' полгода назад ',
    ' год назад ',
    ' на прошлой неделе ',
    ' за январь ',
    ' за март 2012го ',
    ' за апрель 2008 ',
    ' за август 2019 года ',
    ' за 2011 год ',
    ' за 2012й ',
    ' за 2021 ',
    ' за второй квартал ',
    ' за июнь прошлого года ',
    ' за август позапрошлого года ',
    ' за первый квартал текущего года ',
    ' за третий квартал позапрошлого года ',
    ' за 2 квартал прошлого года ',
    ' за третий квартал предыдущего года ',
    ' за март месяц прошедшего года ',
    ' за февраль прошлого года ',
    ' за второе полугодие прошлого года ',
    ' за 2 неделю прошлого месяца ',
    ' за первую неделю сентября прошлого года ',
    ' за первый месяц 2020 года ',
    ' за второй день третьей недели второго квартала ',
    ' за 4 квартал 2020 года ',
    ' за три недели первого квартала 2019 года ',
    ' за вторую неделю сентября 2020 года ',
    ' с апреля 2010 года ',
    ' после апреля 2010 года ',
    ' за апрель 2010 года ',
    ' с мая по июнь 2020 года ',
    ' с февраля по апрель позапрошлого года ',
    ' до июня текущего года ',
    ' с января 2011 года по март 2012го ',
    ' с июня по декабрь ',
    ' с 2001 по 2012 гг ',
    ' с первого до десятого апреля 2019 года ',
    ' с августа по октябрь ',
    ' в апреле ',
    ' в марте 2012 года ',
    ' в апреле прошлого года ',
    ' в мае позапрошлого года ',
    ' во втором квартале ',
    ' в прошлом месяце ',
    ' в прошлом году ',
    ' в позапрошлом году ',
    ' в 2018 году ',
    ' в 2005-2010 годах ',
    ' в 2012-2013 гг ',
    ' с 2012 по 2013 ',
    ' c 01.10 по 01.12 ',
    ' с 01.02.2003 по 21.12.2012 ',
    ' с 01.02 по 21.12 ',
    ' с первого по десятое декабря 2012 года ',
    ' с двадцать второго числа апреля месяца ',
    ' с первого полугодия прошлого года ',
    ' с третьего квартала текущего года ',
    ' со второй по четвертую неделю первого квартала ',
    ' с первого по третий квартал прошлого года ',
    ' с 1 по 3 неделю сентября 2013 года ',
    ' со второго квартала 2019 по третий квартал 2020 ',
    ' с января по май 2019 и с первого по третий квартал прошлого года ',
    ' отчет Павлова на портале за прошлую неделю ',
    ' отчет Иванов вики xlsx за прошлый месяц ',
    ' Иванов справка о доходах за прошлый год ',
    ' справка Сидорова pdf три дня назад ',
    ' квитанция от Ивана Петровича на прошлой неделе pdf ',
    ' квартальный отчет Светланы docx за прошлый квартал '
]
FROM_STR_TO_INT = {
    'январь': 1,
    'февраль': 2,
    'первую': 1,
    'третьей': 3,
    'четвертую': 4,
    'одну': 1,
    'март': 3,
    'май': 5,
    'июнь': 6,
    'июль': 7,
    'август': 8,
    'сентябрь': 9,
    'октябрь': 10,
    'ноябрь': 11,
    'декабрь': 12,
    'текущий': 0,
    'апрель': 4,
    'за': 1,
    'три': 3,
    'вторую': 2,
    'первый': 1,
    'третий': 3,
    '4': 4,
    '1': 1,
    '3': 3,
    '2': 2,
    'две': 2,
    '2й': 2,
    '2ю': 2,
    '10': 10,
    'один': 1,
    'прошлый': -1,
    'четвёртый': 4,
    'четыре': 4,
    'два': 2,
    'десять': 10,
    'последний': -0.5,
    'предыдущий': -1,
    'двадцать': 20,
    'сегодня': 0,
    'вчера': -1,
    'позавчера': -2,
    'последнее': -0.5,
    'прошлое': -1,
    'второе': 2,
    'назад': -1,
    'первое': 1,
    'третье': 3,
    'четвертовать': 4
}
dict_num_day_ordinal = {}
dict_quarter_ordinal = {}
dict_quarter_cardinal = {}
dict_year_modifier = {}
dict_year_cardinal = {}
dict_week_ordinal = {}
dict_week_cardinal = {}
dict_month_modifier = {}
dict_date = {}
dict_day_cardinal = {}
dict_month_ordinal = {}
dict_month_cardinal = {}
dict_week_modifier = {}
dict_count = {}
dict_day_modifier = {}
dict_half_year = {}
dict_year_ordinal = {}
dict_quarter_modifier = {}
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--n', default=0,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()


if __name__ == "__main__":
    TOKENIZER = MorphTokenizer()
    morph_vocab = MorphVocab()
    parser = Parser(DATE)
    num_day_ordinal = []
    str_num = 0
    pred_day_ordinal = []
    n = int(args.n)
    id =0
    print("Введите ", n, " строк с датами:")
    new_lines = []
    for i in range(n):
        line = input()
        new_lines.append(line)
    if len(new_lines)!= 0:
        all_tests = new_lines
    # new_lines - для ввода с консоли
    for line in all_tests:

        print(str_num, "Исходный текст: ", line)
        split_on_date = tknzr.tokenize(line)  # re.split(r'с |по | до ', line)
        complex_date = 0

        for i in range(len(split_on_date)):
            if (split_on_date[i] == 'с' or split_on_date[i] =="со") and (split_on_date[i + 2] == 'по' or split_on_date[i + 2] == 'до' or split_on_date[i + 3] == 'по')\
                    and (line.find('.') == -1):
                complex_date = 1
                complex_word = split_on_date[i + 1]
                complex_word_2 = split_on_date[i + 3]
                print(str_num, "AAAAA", line)
        # else:
        f = open(("output/{}.json").format(str_num), "w+")
        f.seek(0)
        date_match = re.findall(r"(\d\d\.\d\d\.\d\d)", line)
        date_match2 = re.findall(r'(\d\d\.\d\d)', line)
        date_match3 = re.findall(r'(\d\d\.\d\d\.\d\d\d\d)', line)
        if len(date_match)!=0 or len(date_match2)!=0 or len(date_match3)!=0:
            #date_parser(line.replace('.', '-'))
            r, id = num_date_recognize(line,str_num, f, id)
            persons, id = person_extract(line, str_num, id)
            r.update(persons)
            f.write(json.dumps(r, indent=4, ensure_ascii=False))
            f.write('\n')
            f.close()

            str_num = str_num + 1
            continue

        # if len(date_match2) != 0:
        #     persons = person_extract(line, str_num, id)
        #     r.update(persons)
        #     split_vals = date_match2[0].split(".")
        #     # for
        #     r = {
        #         "DateInterval": [
        #             {
        #                 "id": str_num,
        #                 "day_ordinal": [
        #                     {
        #                         "value": split_vals[0],
        #                         "annotations": {
        #                             "annotationStart": 12,
        #                             "annotationEnd": 17,
        #                             "annotationText": " 01 . 12"
        #                         }
        #                     }
        #                 ],
        #                 "mouth_ordinal": [
        #                     {
        #                         "value": split_vals[1],
        #                         "annotations": {
        #                             "annotationStart": 12,
        #                             "annotationEnd": 17,
        #                             "annotationText": " 01 . 12"
        #                         }
        #                     }
        #                 ]
        #             }
        #         ],
        #         "documentText": line
        #     }
        #     f.write(json.dumps(r, indent=4, ensure_ascii=False))
        #     f.write('\n')
        #     f.close()
        #     persons = person_extract(line, str_num, id)
        #     r.update(persons)
        #     str_num = str_num + 1
        #     continue
        # if len(date_match3) != 0:
        #     persons = person_extract(line, str_num, id)
        #     r.update(persons)
        #     str_num = str_num + 1
        #     continue
        str_num = str_num + 1
        z = {}
        for split in [line]:  # split_on_date:
            date = ExtractDate()
            matches = parser.extract(split)

            dict_result, date_dict, result, r, id = viz(str_num, date, split, matches, dict_num_day_ordinal,
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
                                                    dict_week_modifier, dict_count, dict_day_modifier, dict_half_year,
                                                    dict_year_ordinal,
                                                    dict_quarter_modifier, id)
            # print("DICT R", dict_result)
            # try:
            persons, id = person_extract(line, str_num, id)
            r.update(persons)
            print("PERSON", persons)
            z = z.copy()
            z.update(dict_result)
        # if result["id_interval"]
        # print("QQQQQQ", dict_quarter_modifier)
        # Remove duplicate values in dictionary
        # Using loop
        r["documentText"] = line
        temp = []
        res = dict()
        for key, val in dict_result.items():
            if val not in temp:
                temp.append(val)
                res[key] = val
        temp = []
        res_date = dict()
        for key, val in r.items():
            if val not in temp:
                temp.append(val)
                res_date[key] = val
        try:


            for key in list(r["DateInterval"][0]):
                # if

                if re.search('end', key):
                    new_key = key.replace("_end_", "_start_")
                    old_key = key.replace("_end_", "_")
                    r["DateInterval"][0][new_key] = r["DateInterval"][0][old_key]
                    del r["DateInterval"][0][old_key]
        except:
            pass


        if complex_date:
            search = re.search(complex_word, line)
            prev_start = 0
            for key in list(r["DateInterval"][0])[1:]:
                dict_r = r["DateInterval"][0][key]
                start = dict_r[0]["annotations"]["annotationStart"]
                s = search.start()
                if prev_start < search.start() and start > search.start():
                    entyty = key
                    prev_start = start
            if prev_start == search.start() or start == search.start():
                f.write(json.dumps(r, indent=4, ensure_ascii=False))
                f.write('\n')
                f.close()
                continue

            r["DateInterval"][0][entyty.replace("_", "_end_")] = r["DateInterval"][0][entyty]
            print("ENTTT", entyty, complex_word)
            del r["DateInterval"][0][entyty]
            p = morph.parse(complex_word)[0]
            nf = p.normal_form
            p_2 = morph.parse(complex_word_2)[0]
            nf_2 = p_2.normal_form
            # if nf is int:
            #     r["DateInterval"][0] = {
            #         entyty.replace("_", "_start_") : {"value" : nf}}
            # else:
            #     r["DateInterval"][0] = {
            #         entyty.replace("_", "_start_"): {"value": }}
            try:
                value = FROM_STR_TO_INT[nf]
            except:
                value = nf
            search_2 = re.search(complex_word_2, line)
            try:
                value_2 = FROM_STR_TO_INT[nf_2]
            except:
                value_2 = nf_2
            if entyty == 'month_ordinal' or entyty == 'month_cardinal':
                r["DateInterval"][0]['day_start_ordinal'] = {
                    # ("DateInterval{}").format(id_interval):{
                    "value": value,
                    "annotations": {
                        "annotationStart": search.start(),
                        "annotationEnd": search.end(),
                        "annotationText": complex_word
                    },
                    # "id_interval":id_interval
                    # }
                }
                r["DateInterval"][0]['day_end_ordinal'] = {
                    # ("DateInterval{}").format(id_interval):{
                    "value": value_2,
                    "annotations": {
                        "annotationStart": search_2.start(),
                        "annotationEnd": search_2.end(),
                        "annotationText": complex_word_2
                    },
                    # "id_interval":id_interval
                    # }
                }
            else:
                r["DateInterval"][0][entyty.replace("_", '_start_')] = {
                    # ("DateInterval{}").format(id_interval):{
                    "value": value,
                    "annotations": {
                        "annotationStart": search.start(),
                        "annotationEnd": search.end(),
                        "annotationText": complex_word
                    },
                    # "id_interval":id_interval
                    # }
                }
                r["DateInterval"][0][entyty.replace("_", '_end_')] = {
                    # ("DateInterval{}").format(id_interval):{
                    "value": value_2,
                    "annotations": {
                        "annotationStart": search_2.start(),
                        "annotationEnd": search_2.end(),
                        "annotationText": complex_word_2
                    },
                    # "id_interval":id_interval
                    # }
                }

        print("RESULT", r)
        f.write(json.dumps(r, indent=4, ensure_ascii=False))
        f.write('\n')
        final = {}
        print("DATE", res_date)
        print("========================")
        f.close()
    # test_all_date.make_test(dict_num_day_ordinal,
    #                         dict_quarter_ordinal,
    #                         dict_quarter_cardinal,
    #                         dict_year_modifier,
    #                         dict_year_cardinal,
    #                         dict_week_ordinal,
    #                         dict_week_cardinal,
    #                         dict_month_modifier,
    #                         # dict_date,
    #                         dict_day_cardinal,
    #                         dict_day_modifier,
    #                         dict_month_ordinal,
    #                         dict_month_cardinal,
    #                         dict_week_modifier,
    #                         dict_year_ordinal,
    #                         dict_quarter_modifier)
