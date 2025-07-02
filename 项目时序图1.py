import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator
import random
import os

# 设置中文字体 - 使用您系统中可用的字体
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Arial Unicode MS', 'Hiragino Sans GB', 'STHeiti', 'SimSong', 'Songti SC', 'Yuanti SC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 定义任务和时间 - 严格使用原始文案
tasks = [
    # iOS APP初版上架
    {"Task": "xx端第一次提审", "Start": "2024-12-15", "End": "2024-12-16", "Category": "iOS APP初版上架", "Milestone": False},
    {"Task": "xx端第一次提审被拒", "Start": "2024-12-16", "End": "2024-12-16", "Category": "iOS APP初版上架", "Milestone": False},
    {"Task": "xx端第二次提审", "Start": "2025-01-02", "End": "2025-01-02", "Category": "iOS APP初版上架", "Milestone": False},
    {"Task": "xx端第二次被拒", "Start": "2025-01-07", "End": "2025-01-08", "Category": "iOS APP初版上架", "Milestone": False},

    {"Task": "xx端第三次提审", "Start": "2025-01-09", "End": "2025-01-09", "Category": "iOS APP初版上架", "Milestone": False},
    {"Task": "xx端第三次提审通过", "Start": "2025-01-10", "End": "2001-01-10", "Category": "iOS APP初版上架", "Milestone": True},
    {"Task": "xx端第一次提审", "Start": "2024-12-13", "End": "2024-12-13", "Category": "iOS APP初版上架", "Milestone": False},
    {"Task": "xx端第一次提审被拒", "Start": "2024-12-16", "End": "2024-12-16", "Category": "iOS APP初版上架", "Milestone": False},
    {"Task": "xx端第二次提审", "Start": "2024-12-27", "End": "2024-12-27", "Category": "iOS APP初版上架", "Milestone": False},
    {"Task": "xx端第二次提审被拒", "Start": "2024-12-31", "End": "2024-12-31", "Category": "iOS APP初版上架", "Milestone": False},
     {"Task": "xx端第三次提审", "Start": "2024-12-31", "End": "2024-12-31", "Category": "iOS APP初版上架", "Milestone": False},
    {"Task": "xx端第三次审核通过", "Start": "2024-12-31", "End": "2025-01-02", "Category": "iOS APP初版上架", "Milestone": True},
    # iOS老APP转让
    {"Task": "老xx端APP转让成功", "Start": "2025-02-06", "End": "2025-02-07", "Category": "iOS老APP转让", "Milestone": True},
    {"Task": "老xx端APP转让成功", "Start": "2025-02-07", "End": "2025-02-08", "Category": "iOS老APP转让", "Milestone": True},
    
    # iOS APP改名称和icon
    {"Task": "emobilty改名Lagride", "Start": "2025-02-27", "End": "2025-03-03", "Category": "iOS APP改名称和icon", "Milestone":True},
    {"Task": "xx 改名 xxx", "Start": "2025-02-26", "End": "2025-02-27", "Category": "iOS APP改名称和icon", "Milestone": True},
   
]

# 创建DataFrame
df = pd.DataFrame(tasks)
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])
df['Duration'] = (df['End'] - df['Start']).dt.days + 1  # 计算持续天数

# 按类别排序
categories = ["iOS APP初版上架","iOS老APP转让","iOS APP改名称和icon"]
category_order = {cat: i for i, cat in enumerate(categories)}
df['CategoryOrder'] = df['Category'].map(category_order)
df = df.sort_values(['CategoryOrder', 'Start'])

# 固定非黄色配色，避免黄色背景
colors = {
    'iOS APP初版上架': {'main': '#4ECDC4', 'light': '#C7F2EF', 'dark': '#3AA39C'},
    'iOS老APP转让': {'main': '#5B8FF9', 'light': '#D6E4FF', 'dark': '#3D5A99'},
    'iOS APP改名称和icon': {'main': '#9D65C9', 'light': '#E5D4F0', 'dark': '#7D51A1'}
}

# 设置图表大小和样式
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(16, 7))
fig.patch.set_facecolor('#f8f9fa')
ax.set_facecolor('#f8f9fa')

# 计算y轴位置
y_positions = {}
current_pos = 0
for cat in categories:
    cat_tasks = df[df['Category'] == cat]
    for task in cat_tasks['Task']:
        y_positions[task] = current_pos
        current_pos += 1

# 添加阶段背景色
prev_cat = None
phase_starts = []
phase_ends = []
for i, (idx, row) in enumerate(df.iterrows()):
    if prev_cat != row['Category']:
        if i > 0:
            phase_ends.append(i - 0.5)
        phase_starts.append(i - 0.5)
        prev_cat = row['Category']
phase_ends.append(len(df) - 0.5)

for i, cat in enumerate(categories):
    if i < len(phase_starts):
        start = phase_starts[i]
        end = phase_ends[i]
        ax.axhspan(start, end, facecolor=colors[cat]['light'], alpha=0.3, zorder=0)

# 绘制甘特图横条和里程碑
for i, task in enumerate(df.itertuples()):
    start_date = task.Start
    end_date = task.End
    duration = task.Duration
    y_pos = y_positions[task.Task]
    
    # 根据里程碑状态选择不同的绘制方式
    if task.Milestone:
        # 里程碑使用菱形标记
        ax.scatter(mdates.date2num(start_date), y_pos, 
                  s=150, marker='D', color=colors[task.Category]['dark'], 
                  edgecolor='white', zorder=5)
        
        # 为里程碑添加垂直参考线
        ax.axvline(x=mdates.date2num(start_date), ymin=0, ymax=1, 
                  color=colors[task.Category]['dark'], linestyle='--', 
                  alpha=0.3, zorder=1)
        
        # 任务描述 - 只显示任务名
        ax.text(mdates.date2num(start_date) + 0.5, y_pos, 
                f" {task.Task}", 
                va='center', ha='left', fontsize=10, 
                color='black', fontweight='bold')
    else:
        # 普通任务使用横条
        ax.barh(y_pos, duration, left=mdates.date2num(start_date), 
               color=colors[task.Category]['main'], edgecolor='white', 
               alpha=0.8, height=0.5, zorder=3)
        
        # 在横条上添加任务名称
        if duration > 3:  # 只在较长的任务条上添加文字
            ax.text(mdates.date2num(start_date) + duration/2, y_pos, 
                   f"{task.Task}", 
                   va='center', ha='center', fontsize=10, 
                   color='white', fontweight='bold')
        
        # 任务描述 - 不添加额外解释
        ax.text(mdates.date2num(end_date) + 0.5, y_pos, 
                f" {task.Task}", 
                va='center', ha='left', fontsize=9, 
                color='#555555')

# 设置x轴格式为日期
date_format = mdates.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(date_format)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2, byweekday=0))  # 每两周一作为主刻度
ax.xaxis.set_minor_locator(mdates.DayLocator(interval=7))  # 每周作为次刻度

# 添加网格线
ax.grid(axis='x', which='major', linestyle='-', linewidth=0.5, color='#dddddd', zorder=0)
ax.grid(axis='x', which='minor', linestyle=':', linewidth=0.3, color='#eeeeee', zorder=0)

# 设置y轴刻度
ax.set_yticks(list(y_positions.values()))
ax.set_yticklabels([])  # 隐藏默认的y轴标签

# 添加类别标签
for i, cat in enumerate(categories):
    cat_tasks = df[df['Category'] == cat]
    if not cat_tasks.empty:
        first_task = cat_tasks.iloc[0]['Task']
        last_task = cat_tasks.iloc[-1]['Task']
        mid_point = (y_positions[first_task] + y_positions[last_task]) / 2
        
        # 在左侧添加类别标签
        ax.text(-0.01, mid_point, cat, 
                transform=ax.get_yaxis_transform(),
                ha='right', va='center', fontsize=12, 
                fontweight='bold', color=colors[cat]['dark'],
                bbox=dict(facecolor='white', edgecolor=colors[cat]['dark'], 
                          boxstyle='round,pad=0.5', alpha=0.8))

# 设置图表标题和标签
plt.title('iOS APP审核和应用时间管理', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('上线日期', fontsize=12, labelpad=10)

# 添加图例
milestone_marker = plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='gray', 
                             markersize=10, label='代表性事件')
normal_patch = mpatches.Patch(color='gray', label='常规', alpha=0.7)

legend_elements = [milestone_marker, normal_patch]
for cat in categories:
    legend_elements.append(mpatches.Patch(color=colors[cat]['main'], 
                                         label=cat, alpha=0.7))

ax.legend(handles=legend_elements, loc='upper center', 
         bbox_to_anchor=(0.5, -0.05), ncol=5, frameon=True, 
         fancybox=True, shadow=True)

# 设置y轴范围，留出空间放标题和图例
ax.set_ylim(-2, len(df))

# 调整x轴范围，前后各留出一些空间
start_date = df['Start'].min()
end_date = df['End'].max()
date_range = (end_date - start_date).days
buffer_days = max(7, int(date_range * 0.05))  # 至少7天或5%的缓冲
ax.set_xlim(mdates.date2num(start_date - timedelta(days=buffer_days)),
           mdates.date2num(end_date + timedelta(days=buffer_days)))

# 隐藏边框
for spine in ax.spines.values():
    spine.set_visible(False)

# 调整布局
plt.tight_layout()
plt.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.95)

# 保存高分辨率图片到桌面
output_path = os.path.expanduser('/Users/jack.cai/Desktop/app_timeline.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()
