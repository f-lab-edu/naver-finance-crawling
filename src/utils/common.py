from datetime import datetime, time


def format_date(date):
    """
    날짜를 YYYY.MM.DD 형식으로 변환
    :param date: 포맷을 변경할 datetime 객체
    :return:
    """
    return date.strftime("%Y.%m.%d")


def parse_date_range(date_range):
    """
    date_input 에서 선택된 날짜 범위를 datetime 객체로 변환하는 메서드
    :param date_range:
    :return:
    """
    start = datetime.combine(date_range[0], time.min)
    end = datetime.combine(date_range[1], time.max)
    return start, end
