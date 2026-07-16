import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as str_meta

df = pd.read_csv('netflix_titles.csv', encoding='utf-8')
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 넷플릭스가 신작을 가장 많이 출시하는 달은?
'''
df['date_added'] = df['date_added'].str.strip()

df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

df['month_added'] = df['date_added'].dt.month

df['month_added'] = df['month_added'].fillna(0)

df['month_added'] = df['month_added'].astype(int)

real_months = df[df['month_added'] != 0]['month_added']

month_counts = real_months.value_counts()

print(month_counts)

month = month_counts.index[0]
count = month_counts.values[0]
print("가장 많이 출력된 월은 %d월이며, %d개의 작품 출시"%(month, count))
'''

# 넷플릭스 관람 등급 중 가장 높은 Top5 ?
'''
df_clean = df.dropna(subset=['rating'])

top5_ratings = df_clean['rating'].value_counts().head(5)

print(top5_ratings)
'''

# 넷플릭스 콘텐츠 연도별 증가량
'''
df_filtered = df[(df['release_year'] >= 2000) & (df['release_year'] <= 2021)]

trend_data = df_filtered.value_counts(['release_year', 'type']).reset_index(name='count')

trend_data = trend_data.sort_values(by='release_year')

plt.figure(figsize=(12, 6))

sns.lineplot(
    x='release_year', 
    y='count', 
    hue='type', 
    marker='o',       # 꺾이는 곳 o 표시
    linewidth=2.5,    
    markersize=6,     
    data=trend_data,
    palette='Set1'
)

# 그래프 세부 디자인
plt.title("넷플릭스 콘텐츠의 최초 개봉 연도별 분포 (2000 - 2021)", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("최초 개봉 연도 (Release Year)", fontsize=12, labelpad=10)
plt.ylabel("보유 콘텐츠 수 (개)", fontsize=12, labelpad=10)
plt.tight_layout()
plt.show()
'''