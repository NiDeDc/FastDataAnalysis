import matplotlib.pyplot as plt
import numpy as np
from scipy import signal as sig

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def DrawTimeDomains(data, sensor):
    col = len(data)
    for i in range(col):
        row = len(sensor[i][1])
        for j in range(0, row):
            number = min(sensor[i][1][j][0], len(data[i]) - 1)
            left = sensor[i][1][j][1]
            right = min(sensor[i][1][j][2], len(data[i][number]) - 1)
            x = list(range(left, right + 1))
            single_data = data[i][number][left:right + 1]
            ax = plt.subplot(row, col, j * col + i + 1)
            plt.sca(ax)
            plt.plot(x, single_data)
            # plt.ylim(-2, 2)
            plt.title('通道' + str(sensor[i][0] + 1) + ' #' + str(number) + '光栅时域图')
    # plt.get_current_fig_manager().window.state('zoomed')
    plt.subplots_adjust(left=0.04, bottom=0.05, right=0.98, top=0.93, wspace=0.2, hspace=0.5)
    # plt.tight_layout(rect=(0, 0, 1, 0.5))  # 使子图标题和全局标题与坐标轴不重叠
    plt.show()


def DrawWaterFall(data):
    plt.suptitle('瀑布图')
    source = abs(np.array(data).T)
    plt.imshow(source, cmap='turbo', aspect='auto')
    plt.colorbar()
    # plt.get_current_fig_manager().window.state('zoomed')
    # plt.subplots_adjust(left=0.04, bottom=None, right=0.96, top=None, wspace=None, hspace=0.5)
    plt.show()


def DrawSTFT(data, freq, index):
    sample = data[index]
    f, t, z = sig.stft(sample, window='hann', fs=freq, nperseg=5000)
    result_z = 20 * np.log10(abs(z))
    plt.pcolormesh(t, f[0:int(len(f) * 0.1)], result_z[0:int(len(f) * 0.1), :], cmap='jet')
    # plt.figure()
    plt.title(str(index) + '#光栅频率响应')
    plt.ylabel('频率[Hz]')
    plt.xlabel('时间[s]')
    plt.colorbar()
    plt.show()
