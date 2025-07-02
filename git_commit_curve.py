import subprocess
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# 设置中文字体支持
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

def get_git_commits(project_dir):
    """获取指定项目目录下 xxx 的 git 提交记录（限定日期范围）"""
    try:
        author = "xxxxx"
        # 获取提交记录，按日期分组统计提交次数
        log_result = subprocess.run(
            ['git', '-C', project_dir, 'log', '--author', author, 
             '--pretty=format:%ad', '--date=short', '--no-merges'],
            capture_output=True, text=True, check=True
        )
        # 设定日期范围
        start_date = datetime.strptime("2025-03-01", "%Y-%m-%d")
        end_date = datetime.strptime("2025-06-30", "%Y-%m-%d")
        # 解析日期并统计提交次数
        commit_count_by_date = defaultdict(int)
        for line in log_result.stdout.splitlines():
            try:
                date = datetime.strptime(line, '%Y-%m-%d')
                if start_date <= date <= end_date:
                    commit_count_by_date[date] += 1
            except ValueError:
                continue  # 跳过无法解析的日期
        return commit_count_by_date
    except subprocess.CalledProcessError as e:
        print(f"执行git命令出错: {e.stderr}")
        return {}
    except Exception as e:
        print(f"发生未知错误: {e}")
        return {}

def plot_commit_history(commit_count_by_date, project_dir, output_path=None):
    """根据提交记录按日期统计的结果绘制折线图"""
    if not commit_count_by_date:
        print("没有找到提交记录")
        return
    
    # 确保日期是连续的，填充没有提交的日期
    min_date = min(commit_count_by_date.keys())
    max_date = max(commit_count_by_date.keys())
    all_dates = {(min_date + timedelta(days=i)): 0 for i in range((max_date - min_date).days + 1)}
    all_dates.update(commit_count_by_date)
    sorted_dates = sorted(all_dates.items())
    
    dates, counts = zip(*sorted_dates)
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(14, 4), dpi=300)
    
    # 设置背景和边框
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    # 绘制折线图
    ax.plot(dates, counts, color='#3274F7', marker='o', markersize=4, 
            linewidth=2, markeredgecolor='white', markeredgewidth=1)
    
    # 添加填充效果
    ax.fill_between(dates, counts, 0, color='#3274F7', alpha=0.1)
    
    # 设置网格线
    ax.grid(axis='y', linestyle='-', color='#E8E8E8', alpha=0.7, linewidth=0.8)
    ax.grid(axis='x', visible=False)
    
    # 设置边框
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # 设置坐标轴
    ax.set_ylim(0, max(counts) * 1.2 if max(counts) > 0 else 10)
    ax.set_yticks(range(0, int(max(counts) * 1.2) + 1, 5))
    
    # 设置y轴标签
    ax.set_ylabel('单位：次数', fontsize=10, labelpad=10, color='#666666')
    ax.yaxis.set_label_position("left")
    
    # 设置x轴日期格式和刻度
    date_format = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    
    # 调整刻度标签
    plt.xticks(rotation=45, ha='right', fontsize=9, color='#666666')
    plt.yticks(fontsize=9, color='#666666')
    
    # 隐藏刻度线
    ax.tick_params(axis='both', which='both', length=0)
    
    # 添加项目名称、作者和日期范围
    project_name = project_dir.split('/')[-1] if '/' in project_dir else project_dir
    author = "Jack.cai"
    date_range = f"{min_date.strftime('%Y-%m-%d')} - {max_date.strftime('%Y-%m-%d')}"
    plt.figtext(0.02, 0.92, f"项目名称：{project_name}", fontsize=9, ha='left', color='#333333')
    plt.figtext(0.02, 0.88, f"作者：{author}", fontsize=9, ha='left', color='#333333')
    plt.figtext(0.02, 0.84, f"日期范围：{date_range}", fontsize=9, ha='left', color='#333333')
    
    # 优化布局
    plt.tight_layout(rect=[0, 0, 1, 0.9])  # 为顶部文本留出空间
    
    # 保存或显示图表
    if output_path:
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        print(f"图表已保存至: {output_path}")
    else:
        plt.show()

if __name__ == "__main__":
    project_directory = '/Users/xxxxx/Documents/Client/xxx'
    output_image = "/Users/xxxx/Desktop/代码记录.png"
    commit_count_by_date = get_git_commits(project_directory)
    print(commit_count_by_date)  # 调试用
    if commit_count_by_date:
        plot_commit_history(commit_count_by_date, project_directory, output_image)
