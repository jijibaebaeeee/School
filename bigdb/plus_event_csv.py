import pandas as pd
import random

# 전체 행의 수
total_rows = 1162

df = pd.read_csv('편의점크롤링.csv', encoding='cp949')

# 이벤트 이름과 그에 해당하는 비율을 설정합니다.
# 비율은 전체 행 수에 대한 각 이벤트의 대략적인 비율입니다.
# 실제 할당할 때는 이 비율에 따라 계산하여 할당합니다.
event_names = ['NULL', '2+1', '-30%', '1+1', '-50%', '-70%']
event_proportions = [40, 30, 20, 15, 10, 5]  # 이 비율들은 합이 100이 넘지 않아도 되며, NULL의 비율을 조정하여 총합을 100으로 맞출 수 있습니다.

# 비율에 따라 각 이벤트를 할당합니다.
events_counts = {event: total_rows * proportion // sum(event_proportions) for event, proportion in zip(event_names, event_proportions)}

# NULL 이벤트를 나머지 행 수로 계산합니다.
events_counts['NULL'] = total_rows - sum(events_counts.values())

# 이벤트 리스트를 생성합니다.
events_list = []
for event, count in events_counts.items():
    events_list.extend([event] * count)

# events_list의 길이가 total_rows와 동일한지 확인하고, 그렇지 않다면 NULL로 채웁니다.
if len(events_list) < total_rows:
    events_list.extend(['NULL'] * (total_rows - len(events_list)))

# 이벤트 리스트를 무작위로 섞습니다.
random.shuffle(events_list)

# '행사' 열을 생성하고, 이벤트 리스트를 할당합니다.
df['행사'] = events_list

# 데이터프레임을 새로운 엑셀 파일로 저장합니다.
df.to_csv('편의점크롤링_행사.csv', index=False, encoding='cp949')