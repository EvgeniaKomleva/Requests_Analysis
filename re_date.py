import re
if __name__ == "__main__":
    date_match = re.findall(r'(\d\d.\d\d.\d\d\d)', 'c 01.10.12 по 01.12.20 ')
    date_match2 = re.findall(r'(\d\d.\d\d)', 'c 01.10 по 01.12 ')

    print("date_object =", len(date_match), date_match2)