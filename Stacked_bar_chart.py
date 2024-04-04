import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取Excel文件
df = pd.read_excel('final data.xlsx', engine='openpyxl')

# 定义'conv+bn_1'和'conv+bn_2'的数据
speed = df['separate']
sum = [speed[i] + speed[i+1] for i in range(0, len(speed), 2)]
sum = sum[::2]

# 提取柱子A和柱子B的数据
data_a = speed[::4]  # 奇数索引数据
data_b = speed[1::4]  # 偶数索引数据

print(data_a)
print(data_b)

# 计算所占比例
proportion_a = [a / total * 100 for a, total in zip(data_a, sum)]
proportion_b = [b / total * 100 for b, total in zip(data_b, sum)]

# X轴的位置
ind = np.arange(len(sum))

# 画图
bar_width = 0.35  # 条形的宽度

fig, ax = plt.subplots()

# 堆叠柱状图
bars_a = ax.bar(ind, proportion_a, bar_width, label='NCHW Conv', color='#1f77b4')
bars_b = ax.bar(ind, proportion_b, bar_width, bottom=proportion_a, label='NCHW BN', color='#87CEEB')


# 设置纵坐标的标签
ax.set_ylabel('Proportions (%)')

# 设置x轴的刻度和刻度标签
ax.set_xticks(ind)
ax.set_xticklabels(['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'])

# 设置y轴的标签
ax.set_ylabel('Percentage of Computing Time', fontsize=24,weight='bold')

# 设置图表的标题
ax.set_title('')
# 设置 x 轴刻度标签的字体大小
for label in ax.get_xticklabels():
    label.set_fontstyle('italic')
    label.set_fontsize(24)
    label.set_fontweight('bold')
for label in ax.get_yticklabels():
    label.set_fontsize(24)
    label.set_fontweight('bold')

ax.yaxis.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.5, zorder=2)
# ax2.set_yticklabels([]) # 隐藏次坐标轴的y轴刻度标签

# 显示图例
ax.legend(prop={'weight': 'bold','size':20})

# 显示图表
plt.show()