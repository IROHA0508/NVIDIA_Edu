import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font="Malgun Gothic")


df = pd.read_csv(r'C:\Users\sb730\Desktop\NVIDIA교육\실습 자료\subway_by_time.csv', encoding='cp949')

#print(df.info())
df['사용월'] = df['사용월'].astype(str)
df_202606 = df[df['사용월'] == '202606'].copy()


lines = ['1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선']

# lines에 적힌 호선들을 df_202606 columns에서 따로 필터링 하기 위한 코드
df_filtered = df_202606.loc[df_202606['호선명'].isin(lines)].copy() 

df_filtered = df_filtered.sort_values(by='호선명')

morning_list = []
evening_list = []

for line in lines:
    df_line = df_filtered[df_filtered['호선명'] == line]
    
    if not df_line.empty:
        max_morning_idx = df_line['08시-09시 하차인원'].idxmax()
        morning_list.append({
            "호선": line,
            "역명": df_line.loc[max_morning_idx, '지하철역'],
            "인원수": df_line.loc[max_morning_idx, '08시-09시 하차인원']
        })
        max_evening_idx = df_line['18시-19시 하차인원'].idxmax()
        evening_list.append({
            "호선": line,
            "역명": df_line.loc[max_evening_idx, '지하철역'],
            "인원수": df_line.loc[max_evening_idx, '18시-19시 하차인원']
        })


df_morning = pd.DataFrame(morning_list)
df_evening = pd.DataFrame(evening_list)

df_morning["호선_역명"] = df_morning["호선"] + "\n(" + df_morning["역명"] + ")"
df_evening["호선_역명"] = df_evening["호선"] + "\n(" + df_evening["역명"] + ")"

fig, ax1 = plt.subplots(figsize=(12, 7))

sns.barplot(
    data=df_morning, 
    x="호선_역명",
    y="인원수", 
    hue="호선_역명", 
    ax=ax1, 
    palette="crest", 
    legend=False
)
plt.show()

fig, ax2 = plt.subplots(figsize=(12, 7))

sns.barplot(
    data=df_evening, 
    x="호선_역명",
    y="인원수", 
    hue="호선_역명", 
    ax=ax2, 
    palette="crest", 
    legend=False
)

plt.show()