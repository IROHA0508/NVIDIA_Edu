import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font="Malgun Gothic")


df = pd.read_csv('subway_by_time.csv', encoding='cp949')

#print(df.info())
df['사용월'] = df['사용월'].astype(str)
df_202606 = df[df['사용월'] == '202606'].copy()


lines = ['1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선', '8호선', '9호선']
