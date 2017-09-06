# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date: 2017-09-05 22:56:16
# @Last Modified by:   Alan Lau
# @Last Modified time: 2017-09-05 22:56:16

import math
import random
import numpy as np
from datetime import datetime
from pprint import pprint as p
import matplotlib.pyplot as plt

# 随机生成100个二维平面点
dataset = np.random.rand(500, 2)


class Canopy:
    def __init__(self, dataset):
        self.dataset = dataset
        self.t1 = 0
        self.t2 = 0

    # 设置初始阈值
    def setThreshold(self, t1, t2):
        if t1 > t2:
            self.t1 = t1
            self.t2 = t2
        else:
            print('t1 needs to be larger than t2!')

    # 使用欧式距离进行距离的计算
    def euclideanDistance(self, vec1, vec2):
        return math.sqrt(((vec1 - vec2)**2).sum())

    # 根据当前dataset的长度随机选择一个下标
    def getRandIndex(self):
        return random.randint(0, len(self.dataset) - 1)

    def clustering(self):
        if self.t1 == 0:
            print('Please set the threshold.')
        else:
            canopy = []  # 用于存放最终归类结果
            while len(self.dataset) != 0:
                rand_index = self.getRandIndex()
                current_center = self.dataset[rand_index]  # 随机获取一个中心点，定为P点
                current_center_list = []  # 初始化P点的canopy类容器
                delete_list = []  # 初始化P点的删除容器
                self.dataset = np.delete(
                    self.dataset, rand_index, 0)  # 删除随机选择的中心点P
                for datum_j in range(len(self.dataset)):
                    datum = self.dataset[datum_j]
                    distance = self.euclideanDistance(
                        current_center, datum)  # 计算选取的中心点P到每个点之间的距离
                    if distance < self.t1:
                        # 若距离小于t1，则将点归入P点的canopy类
                        current_center_list.append(datum)
                    if distance < self.t2:
                        delete_list.append(datum_j)  # 若小于t2则归入删除容器
                # 根据删除容器的下标，将元素从数据集中删除
                self.dataset = np.delete(self.dataset, delete_list, 0)
                canopy.append(
                    {'canopy_center': current_center, 'canopy_component': current_center_list})
        return canopy


def showCanopy(canopy, dataset, t1, t2):
    fig = plt.figure()
    sc = fig.add_subplot(111)
    colors = ['brown', 'peru', 'blue', 'y', 'r', 'sienna', 'dodgerblue', 'deeppink', 'orangered', 'peru', 'blue', 'y', 'r',
              'gold', 'dimgray', 'darkorange', 'peru', 'blue', 'y', 'r', 'cyan', 'tan', 'orchid', 'peru', 'blue', 'y', 'r', 'sienna']
    markers = ['*', 'h', 'H', '+', '1', '2', '3', ',', 'v', 'H', '+', '1', '2', '^',
               '<', '>', '.', '4', 'H', '+', '1', '2', 's', 'p', 'x', 'D', 'd', '|', '_']
    centers = [center['canopy_center'] for center in canopy]
    for i in range(len(dataset)):
        datum = dataset[i]
        strcenters = [str(ele) for ele in centers]
        if str(datum) in strcenters:
            index = strcenters.index(str(datum))
            t1_circle = plt.Circle(
                xy=(datum[0], datum[1]), radius=t1, color='dodgerblue', fill=False)
            t2_circle = plt.Circle(
                xy=(datum[0], datum[1]), radius=t2, color='skyblue', alpha=0.6)
            sc.add_artist(t1_circle)
            sc.add_artist(t2_circle)
            sc.plot(datum[0], datum[1],
                    marker=markers[index], color=colors[index], markersize=10)
        else:
            sc.plot(datum[0], datum[1], 'o', color='black', markersize=1.5)
    maxvalue = np.amax(dataset)
    minvalue = np.amin(dataset)
    plt.xlim(minvalue - t1, maxvalue + t1)
    plt.ylim(minvalue - t1, maxvalue + t1)
    plt.show()


def main():
    t1 = 0.6
    t2 = 0.4
    gc = Canopy(dataset)
    gc.setThreshold(t1, t2)
    canopy = gc.clustering()
    print('Get %s initial centers.' % len(canopy))
    showCanopy(canopy, dataset, t1, t2)


if __name__ == '__main__':
    t_s = datetime.now()
    main()
    t_e = datetime.now()
    usedtime = t_e - t_s
    print('[%s]' % usedtime)
