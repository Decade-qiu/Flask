from datetime import datetime

date_str = '20230529220922'
datetime_obj = datetime.strptime(date_str, '%Y%m%d%H%M%S')
formatted_date_str = datetime_obj.strftime('%Y年%m月%d日%H点%M分')

print(formatted_date_str)
