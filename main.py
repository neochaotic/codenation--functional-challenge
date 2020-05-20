from datetime import datetime
import itertools as it
import pprint

records = [
    {'source': '48-996355555', 'destination': '48-666666666', 'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097', 'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097', 'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788', 'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788', 'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099', 'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697', 'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099', 'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697', 'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097', 'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564627800, 'start': 1564626000}
]


def is_daytime(arg):
    return 6 <= arg.hour < 22


def convert_datetime(arg):
    return datetime.fromtimestamp(arg)


def calc_sec(dt_end, dt_start):
    end = convert_datetime(dt_end)
    start = convert_datetime(dt_start)
    if is_daytime(end) and is_daytime(start):
        diff = (end - start).seconds
    elif not is_daytime(end) and not is_daytime(start):
        diff = 0
    elif is_daytime(end):
        diff = (end - start.replace(hour=6)).seconds
    else:
        diff = (end.replace(hour=22) - start).seconds
    return diff


def calc_bill(sec):
    min = sec // 60
    return 0.36 + (min * 0.09)


def classify_by_phone_number(rec):
    k_func = lambda x: x['source']
    cal_s = map(lambda x: {'source': x['source'], 'total': calc_sec(x['end'], x['start'])}, rec)
    bill = map(lambda x: {'source': x['source'], 'total': calc_bill(x['total'])}, cal_s)
    gro_bill = it.groupby(sorted(bill, key=k_func), k_func)
    total = [{'source': k, 'total': round(sum(x['total'] for x in g), 2)} for k, g in gro_bill]
    return sorted(total, key=lambda x: x['total'], reverse=True)


if __name__ == '__main__':
    pprint.pprint(classify_by_phone_number(records))
