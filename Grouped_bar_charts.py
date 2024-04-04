import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取Excel文件
df = pd.read_excel('final data.xlsx', engine='openpyxl')
conv_bn_1_data = df['conv+bn3'].dropna().tolist()
conv_bn_2_data = df['conv+bn4'].dropna().tolist()
# 定义'conv+bn_1'和'conv+bn_2'的数据
# conv_bn_1_data = [6.27649, 7.89026, 8.550332, 9.012816, 48.09859, 51.28458, 22.955266, 25.862005, 9.540957, 10.147403, 8.61712, 8.200147, 19.75629, 18.293014, 16.680918, 16.137862]
# conv_bn_2_data = [6.21183, 12.00636, 8.179658, 9.3959, 44.3821, 49.11994, 21.533033, 23.003964, 8.998321, 9.521805, 7.813446, 8.00847, 17.311182, 17.572048, 12.427207, 12.939834]

# 初始化合并后的列表
merged_data = []

# 遍历'conv+bn_1'的数据，并在每两个数据后面插入两个'conv+bn_2'的数据
for i in range(0, len(conv_bn_1_data), 2):
    merged_data.extend([conv_bn_1_data[i], conv_bn_1_data[i + 1]])
    merged_data.extend([conv_bn_2_data[i], conv_bn_2_data[i + 1]])

# 将合并后的数据转换为Pandas DataFrame
df_merged = pd.DataFrame(merged_data, columns=['conv+bn'])

# 为了绘图，我们需要将'c_in, c_out, k_size, input_size, batch_size, loop_time'列的值合并作为横坐标
df_merged['横坐标'] = df['c_in, c_out, k_size, input_size, batch_size, loop_time']

bar_width = 1
group_width = bar_width * 4
num_groups = len(merged_data) // 4

# Calculate the spacing between groups of bars
space_between_groups = bar_width * 1.5
group_positions = np.arange(num_groups) * (bar_width * 4 + space_between_groups)

bars1_positions = group_positions
bars2_positions = [pos + bar_width for pos in bars1_positions]
bars3_positions = [pos + bar_width * 2 for pos in bars1_positions]
bars4_positions = [pos + bar_width * 3 for pos in bars1_positions]

# 绘制柱状图
fig, ax = plt.subplots(figsize=(12, 8))
ax.bar(bars1_positions, merged_data[::4], width=bar_width, label='NCHW_Libtorch', color='#1f77b4',zorder=3)
ax.bar(bars2_positions, merged_data[1::4], width=bar_width, label='NHWC_Libtorch', color='#F7A500',zorder=3)
ax.bar(bars3_positions, merged_data[2::4], width=bar_width, label='NCHW_BDLO', color='#87CEEB',zorder=3)
ax.bar(bars4_positions, merged_data[3::4], width=bar_width, label='NHWC_BDLO', color='#FFDAB9',zorder=3)

# 设置x轴的刻度标签
center_positions = [pos + 1.5 * bar_width for pos in group_positions]
ax.set_xticks(center_positions)
ax.set_xticklabels(['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8'])

# 设置y轴的标签
ax.set_ylabel('Time Comsumption (s)', fontsize=24,weight='bold')

# 设置图表的标题
ax.set_title('')
# 设置 x 轴刻度标签的字体大小
plt.xticks(fontsize=24,weight='bold',zorder=4)
for label in ax.get_xticklabels():
    label.set_fontstyle('italic')
# 设置 y 轴刻度标签的字体大小
plt.yticks(fontsize=24,weight='bold',zorder=4)

ax.yaxis.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.5, zorder=2)

# 创建图例
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#1f77b4', label='NCHW LibTorch'),
    Patch(facecolor='#F7A500', label='NHWC LibTorch'),
    Patch(facecolor='#87CEEB', label='NCHW BDLO'),
    Patch(facecolor='#FFDAB9', label='NHWC BDLO')
]

# 显示图例
ax.legend(handles=legend_elements,prop={'weight': 'bold','size':20})


# 显示图表
plt.show()