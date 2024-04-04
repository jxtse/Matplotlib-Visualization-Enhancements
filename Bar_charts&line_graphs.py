import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取Excel文件
df = pd.read_excel('final data.xlsx', engine='openpyxl')

# 定义'conv+bn_1'和'conv+bn_2'的数据
speedup = df['合的比值3'].dropna().tolist()
speed = df['分开的比值3']

bar_width = 1
num_groups = len(speedup) // 2

# Calculate the spacing between groups of bars
space_between_groups = bar_width * 1.5
group_positions = np.arange(len(speedup)//2) * (bar_width * 2 + space_between_groups)

bars1_positions = group_positions
bars2_positions = [pos + bar_width for pos in bars1_positions]
bars3_positions = [pos + bar_width * 2 for pos in bars1_positions]
bars4_positions = [pos + bar_width * 3 for pos in bars1_positions]

line_positions1 = [pos + 0.5 * bar_width for pos in bars1_positions]
line_positions2 = [pos + 0.5 * bar_width for pos in bars2_positions]

# 绘制柱状图
fig, ax1 = plt.subplots(figsize=(12, 8))
ax1.bar(bars1_positions, speedup[::2], width=bar_width, label='NCHW', color='#4682B4',zorder=3)
ax1.bar(bars2_positions, speedup[1::2], width=bar_width, label='NHWC', color='#FFD700',zorder=3)

ax2 = ax1.twinx()  # 创建第二个纵坐标轴
# 绘制折线图
ax2.plot(line_positions1, speed[::4], label='NCHW_Libtorch', color='#1f77b4', marker='o', zorder=3)  # 圆圈标记
ax2.plot(line_positions1, speed[1::4], label='NHWC_Libtorch', color='#87CEEB', marker='s', zorder=3)  # 正方形标记
ax2.plot(line_positions1, speed[2::4], label='NCHW_BDLO', color='#F7A500', marker='^', zorder=3)  # 三角形标记
ax2.plot(line_positions1, speed[3::4], label='NHWC_BDLO', color='#FFDAB9', marker='*', zorder=3)  

# 设置x轴的刻度标签
center_positions = [pos + 0.5 * bar_width for pos in group_positions]
ax1.set_xticks(center_positions)
ax1.set_xticklabels(['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'])
ax1.set_xlabel(ax1.get_xlabel(), fontsize=24, weight='bold')
# 设置y轴的标签
ax1.set_ylabel('Normalization Speedup \n(LibTorch/BDLO)', fontsize=24,weight='bold')

max_y_value_ax1 = max_y_value_ax2 = 1.5  # 设置主坐标轴的y轴最大值
# 设置主坐标轴的y轴上限和刻度间距
ax1.set_ylim(0, max_y_value_ax1)  # 替换max_y_value_ax1为您希望设置的y轴最大值
# 设置次坐标轴的y轴上限和刻度间距
ax2.set_ylim(0, max_y_value_ax2)  # 替换max_y_value_ax2为您希望设置的y轴最大值

# 设置图表的标题
ax1.set_title('')
# 设置 x 轴刻度标签的字体大小
for label in ax1.get_xticklabels():
    label.set_fontstyle('italic')
    label.set_fontsize(24)
    label.set_fontweight('bold')
for label in ax1.get_yticklabels():
    label.set_fontsize(24)
    label.set_fontweight('bold')

ax1.yaxis.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.5, zorder=2)
ax2.set_yticklabels([]) # 隐藏次坐标轴的y轴刻度标签

# 创建图例
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#4682B4', label='NCHW'),
    Patch(facecolor='#FFD700', label='NHWC'),
    plt.Line2D([0], [0], color='#1f77b4', marker='o', label='NCHW Conv'),
        plt.Line2D([0], [0], color='#F7A500', marker='^', label='NHWC Conv'),
    plt.Line2D([0], [0], color='#87CEEB', marker='s', label='NCHW Pool'),
    plt.Line2D([0], [0], color='#FFDAB9', marker='*', label='NHWC Pool')
]

# 显示图例
ax1.legend(handles=legend_elements, ncol=3, prop={'weight': 'bold','size':20})


# 显示图表
plt.show()