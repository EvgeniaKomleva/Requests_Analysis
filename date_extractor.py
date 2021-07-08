class ExtractDate(object):

    def __init__(self):
        self.year = []
        self.quater = []
        self.month = []
        self.week = []
        self.day = []

        self.week_ordinal = []
        self.week_cardinal = []
        self.week_modifier = []
        self.week_start_ordinal = []
        self.week_end_ordinal = []

        self.quarter_ordinal = []
        self.quarter_cardinal = []
        self.quarter_start_ordinal = []
        self.quarter_end_ordinal = []

        self.month_modifier = []
        self.month_ordinal = []
        self.month_cardinal = []

        self.half_year = []
        self.count = []

        self.year_modifier = []
        self.year_cardinal = []
        self.year_start_modifier = []
        self.year_end_modifier = []

        self.date = []

        self.day_ordinal = []
        self.day_cardinal = []
        self.day_modifier = []

        self.start_date = []
        self.end_date = []
        self.year_ordinal = []
        self.quarter_modifier = []

    def get_date(self):
        if self.year != None:
            print("Год: ", match.fact.year)
        if self.quater != None:
            print("Квартал: ", match.fact.quater)
        if self.mouth != None:
            print("Месяц: ", match.fact.mouth)
        if self.week != None:
            print("Неделя: ", match.fact.week)
        if self.day != None:
            print("День: ", match.fact.day)

