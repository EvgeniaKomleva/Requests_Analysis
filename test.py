


# true markup
"""
quarter_ordinal=2, quarter_cardinal=1, year_modifier=-1
week_ordinal=2, week_cardinal=1, month_modifier=-1
week_ordinal=1, week_cardinal=1, year_modifier=-1, date=DD.09.YYYY
day_ordinal=2, day_cardinal=1, week_ordinal=3, week_cardinal=1, quarter_ordinal=2, quarter_cardinal =1
month_ordinal=1, month_cardinal=1, date=DD.MM.2020
week_cardinal=3, quarter_ordinal=1, quarter_cardinal =1, date=DD.MM.2019
quarter_ordinal=4, quarter_cardinal=1, date=DD.MM.2020
day_cardinal=3
week_modifier=-1, week_cardinal=1
month_modifier=-1, month_cardinal=1

"""
#true_day_ordinal = {' за сегодня ': 0, ' за вчера ': -1, ' за позавчера ': -2, ' за последние два дня ': 2, ' за два прошлых дня ': -2, ' за два предыдущих дня ': -2, ' за день ': 1, ' за один день ': 1, ' за три дня ': 3, ' за десять дней ': 10, ' за двадцать дней ': 20, ' за 1 день ': 1, ' за 3 дня ': 3, ' за 10 дней ': 10, ' три дня назад ': -3, ' за второй день третьей недели второго квартала ': 2, ' справка Сидорова pdf три дня назад ': 3}
#from main import dict_num_day_ordinal

true_quarter_ordinal = {'за второй квартал предыдущего года': 2, 'за второй день третьей недели второго квартала': 2, 'за три недели первого квартала 2019 года': 1}
true_day_ordinal = {'за второй день третьей недели второго квартала': 2, 'за три дня': 3, 'с 01.10 по 01.12': '01'}
true_quarter_cardinal = {'за 4 квартал 2020 года': 4}
true_year_modifier = {'за второй квартал предыдущего года': -1, 'за первую неделю сентября прошлого года': -1}


true_dict_num_day_ordinal = {'за второй день третьей недели второго квартала': 2, 'за три дня': 3, 'с 01.10 по 01.12': '01'}
true_dict_quarter_ordinal  =  {'за второй квартал предыдущего года': 2, 'за второй день третьей недели второго квартала': 2, 'за три недели первого квартала 2019 года': 1, 'за 4й квартал 2020 года':4, 'со второй по четвертую неделю первого квартала': 1, 'со второго квартала 2019 по третий квартал 2020': 2, 'со второго квартала 2019 по третий квартал 2020': 3, 'с января по май 2019 и с первого по третий квартал прошлого года': 3}
true_dict_quarter_cardinal  =  {'за второй квартал предыдущего года':1,'за второй день третьей недели второго квартала':1,'за три недели первого квартала 2019 года':1, 'за 4 квартал 2020 года': 1}
true_dict_year_modifier  =  {'за второй квартал предыдущего года': -1, 'за первую неделю сентября прошлого года': -1,
                             'с февраля по апрель позапрошлого года': -2, 'до июня текущего года': 0,
                             'с января по май 2019 и с первого по третий квартал прошлого года': -1}
true_dict_year_cardinal  =  { 'за последние три года': 3}

true_dict_week_ordinal   =  {'за вторую неделю прошлого месяца' :2,
'за первую неделю сентября прошлого года':1,
'за второй день третьей недели второго квартала':3

}
true_dict_week_cardinal   =  {'за вторую неделю прошлого месяца':1,'за первую неделю сентября прошлого года':1,'за второй день третьей недели второго квартала':1,'за три недели первого квартала 2019 года': 3}
true_dict_month_modifier  =  {'за вторую неделю прошлого месяца': -1, 'за предыдущий месяц':-1}
true_dict_date   =  {} # заполнить
true_dict_day_cardinal  =  {'за второй день третьей недели второго квартала':1, 'за три дня':3}
true_dict_month_ordinal  =  {'за первую неделю сентября прошлого года': 9, 'за первый месяц 2020 года': 1, 'апреля 2010 года': 4,
                             'после апреля 2010 года': 4, 'за апрель 2010 года': 4, 'с мая по июнь 2020 года': 6, 'февраля ': 2,
                             'апрель позапрошлого года': 4, 'до июня текущего года': 0,  'с января по май 2019 и с первого по третий квартал прошлого года': 5}

true_dict_month_cardinal   =  {'за первый месяц 2020 года':1}
true_dict_week_modifier   =  {'за прошлую неделю': -1}
# accuracy - делим количество правильных ответов на все


def accuracy(true, pred):
    shared_items = {k: true[k] for k in true if k in pred and true[k] == pred[k]}
    return len(shared_items)/max(len(true), len(pred))

# тесты для  day_cardinal
tests_true_answ = [true_dict_num_day_ordinal,
                   true_dict_quarter_ordinal,
                   true_dict_quarter_cardinal,
                   true_dict_year_modifier,
                   true_dict_year_cardinal,
                   true_dict_week_ordinal,
                   true_dict_week_cardinal,
                   true_dict_month_modifier,
                   #true_dict_date,  # заполнить
                   true_dict_day_cardinal,
                   true_dict_month_ordinal,  # исправить
                   true_dict_month_cardinal,
                   true_dict_week_modifier]
dicts_name = ['dict_num_day_ordinal' ,
'dict_quarter_ordinal ',
'dict_quarter_cardinal' ,
'dict_year_modifier',
'dict_year_cardinal' ,
'dict_week_ordinal ',
'dict_week_cardinal ',
'dict_month_modifier' ,
#'dict_date ',
'dict_day_cardinal',
'dict_month_ordinal',
'dict_month_cardinal ',
'dict_week_modifier ']



#i = 0
#for dict_ in dicts:
#    print('true_{}'.format( dicts_name[i])  , ' = ',dict_)
#    i = i + 1
def make_test(dict_num_day_ordinal ,
             dict_quarter_ordinal,
             dict_quarter_cardinal,
             dict_year_modifier,
             dict_year_cardinal,
             dict_week_ordinal,
             dict_week_cardinal,
             dict_month_modifier,
             #dict_date,
             dict_day_cardinal,
             dict_month_ordinal,
             dict_month_cardinal,
             dict_week_modifier,
             ):
    dicts = [dict_num_day_ordinal,
             dict_quarter_ordinal,
             dict_quarter_cardinal,
             dict_year_modifier,
             dict_year_cardinal,
             dict_week_ordinal,
             dict_week_cardinal,
             dict_month_modifier,
             #dict_date,
             dict_day_cardinal,
             dict_month_ordinal,
             dict_month_cardinal,
             dict_week_modifier]

    tests_name = ['day_ordinal',
                  'quarter_ordinal ',
                  'quarter_cardinal ',
                  'year_modifier',
                  'year_cardinal',
                  'week_ordinal',
                  'week_cardinal',
                  'month_modifier ',
                  #'date ',  # заполнить
                  'day_cardinal',
                  'month_ordinal',  # исправить
                  'month_cardinal',
                  'week_modifier']

    i = 0
    while i < len(tests_true_answ):
        # print(accuracy(tests_true_answ[i], dicts[i]))
        print("Сущьность :", tests_name[i])
        print("Правильные ответы: ", tests_true_answ[i])
        print("Ответы системы: ", dicts[i])

        try:
            print("Точность :", accuracy(tests_true_answ[i], dicts[i]))
        except:
            # print("________________________")
            print(tests_true_answ[i], dicts[i])
            # print("________________________")
        print("========================")
        i = i + 1