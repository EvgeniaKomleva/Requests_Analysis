import json
import re
from person_extractor import person_extract


def num_date_recognize(line,str_num,  f, id):
    r = {}
    days = []
    months = []
    years = []
    for m in re.finditer(r'\d\d\.\d\d(\.\d{2,})*', line):
        print(m.group(0)  , "FD")
        date_ent = m.group(0).split('.')
        print(date_ent)
        days.append(date_ent[0])
        months.append(date_ent[1])
        try: years.append(date_ent[2])
        except: print("No year")
    # print(find_date, "FD")
    # line_arr = line.split('.')
    # rint("ARR", line_arr)
        # for
    r = {
        "DateInterval": [
            {
                "id": str(id),
                # "day_ordinal": [
                #     {
                #         "value": 0,
                #         "annotations": {
                #             "annotationStart": 12,
                #             "annotationEnd": 17,
                #             "annotationText": " 01 . 12"
                #         }
                #     }
                # ],
                # "mouth_ordinal": [
                #     {
                #         "value": 1,
                #         "annotations": {
                #             "annotationStart": 12,
                #             "annotationEnd": 17,
                #             "annotationText": " 01 . 12"
                #         }
                #     }
                # ]
            }
        ],
        "documentText": line
    }
    i = 0
    for day in days:
        i = i +1
        m = re.search(day, line)
        if i % 2 == 1:
            entyty = "day_start_ordinal"
        else:
            entyty = "day_end_ordinal"
        r['DateInterval'][0][entyty] =  [
                        {
                            "value": day,
                            "annotations": {
                                "annotationStart": m.start(),
                                "annotationEnd": m.end(),
                                "annotationText": day
                            }
                        }
                    ]
    for mon in months:
        i = i +1
        m = re.search(mon, line)
        if i % 2 == 1:
            entyty = "month_start_ordinal"
        else:
            entyty = "month_end_ordinal"
        r['DateInterval'][0][entyty] =  [
                        {
                            "value": mon,
                            "annotations": {
                                "annotationStart": m.start(),
                                "annotationEnd": m.end(),
                                "annotationText": mon
                            }
                        }
                    ]
    if len(years) != 0:
        for year in years:
            i = i +1
            m = re.search(year, line)
            if i % 2 == 1:
                entyty = "year_start_ordinal"
            else:
                entyty = "year_end_ordinal"
            r['DateInterval'][0][entyty] =  [
                            {
                                "value": year,
                                "annotations": {
                                    "annotationStart": m.start(),
                                    "annotationEnd": m.end(),
                                    "annotationText": year
                                }
                            }
                        ]

    id =id +1
    return r, id