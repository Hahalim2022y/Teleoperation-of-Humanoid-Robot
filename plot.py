import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties


# # 指定SimSun字体文件路径
# font_path = 'program_font/simsun.ttc'  # 替换为实际路径
# font_prop = FontProperties(fname=font_path)

# # 全局配置（可选）
# plt.rcParams['font.family'] = font_prop.get_name()
# plt.rcParams['axes.unicode_minus'] = False  # 修复负号显示

#做平滑处理，我觉得应该可以理解为减弱毛刺，，吧  能够更好地看数据走向
def tensorboard_smoothing(x,smooth=0.99):
    x = x.copy()
    weight = smooth
    for i in range(1,len(x)):
        x[i] = (x[i-1] * weight + x[i]) / (weight + 1)
        weight = (weight + 1) * smooth
    return x
 
if __name__ == '__main__':
    
    fig, ax1 = plt.subplots(1, 1)    # a figure with a 1x1 grid of Axes
    
    #设置上方和右方无框
    # ax1.spines['top'].set_visible(False)                   # 不显示图表框的上边框
    # ax1.spines['right'].set_visible(False)  
 
    len_mean = pd.read_csv("logs/teacher.csv") # teacher  wave_left07_poses rew_feet_max_height_for_this_air
  
 
    #设置折线颜色，折线标签
    #使用平滑处理
    # ax1.plot(len_mean['Step'], tensorboard_smoothing(len_mean['Value'], smooth=0.6), color="red",label='all_data')
    ax1.plot(len_mean['Step'], tensorboard_smoothing(len_mean['Value'], smooth=1), color="red")
    #不使用平滑处理
    # ax1.plot(len_mean['Step'], len_mean['Value'], color="red",label='all_data')
 
 
    #s设置标签位置，lower upper left right，上下和左右组合
    # plt.legend(loc = 'lower right')
 
   
    ax1.set_xlabel("iterations")
    ax1.set_ylabel("reward")
    ax1.set_title("Mean_Reward") # Mean_Reward  Rewaed_feet_max_height_for_this_air
    plt.show()
    #保存图片，也可以是其他格式，如pdf
    fig.savefig(fname='./teacher'+'.png', format='png')
 
