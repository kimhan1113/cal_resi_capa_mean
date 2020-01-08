import shutil
import glob
import os
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import cv2
from tqdm import *

Root = filedialog.askdirectory()
FolderName = os.path.basename(Root)
FileList = os.listdir(Root)
capacitor = []
resistor = []
average = []
eightlength = []
resultList = []
resi_ave = 0
capa_ave = 0
RefHeight = [Folder for Folder in FileList if Folder.endswith('csv')]

# PackageTypeResistor=0
# PackageTypeCapacitor=1

# resistor와 capacitor만 리스트에 추가하는 함수
def seperate_pkg():
    refind_RefHeight = []
    for i in range(0, len(RefHeight)):
        splitted = RefHeight[i].split('_')

        if splitted[3] == '[PkgType]0' or splitted[3] == '[PkgType]1':
            refind_RefHeight.append(RefHeight[i])
        else:
            continue
    return refind_RefHeight

refind_RefHeight = seperate_pkg()

# 해당 폴더에 height값 계산 함수
def average_calculate():

    for k in tqdm(range(0, len(refind_RefHeight))):

        # csv값 load후 정렬
        RefHeightPath = Root + '/' + refind_RefHeight[k]
        RefHeighted = np.genfromtxt(RefHeightPath, delimiter=",",dtype=float,)[:, :-1]
        RefHeighted = RefHeighted.flatten()
        RefHeighted = sorted(RefHeighted, reverse=True)

        # 상위 3% 인덱스 pop 후에 그 후 상위 8% 인덱스의 평균값 계산
        popnum = len(RefHeighted) * (3 / 100)
        popindex = [0] * int(popnum)
        for index in popindex:
            RefHeighted.pop(index)

        prtnum = len(RefHeighted) * (8 / 100)
        prtindex = [0] * int(prtnum)
        sums = 0
        for idx in prtindex:
            sums += RefHeighted[idx]
            eightlength.append(RefHeighted[idx])

        average = sums / len(eightlength)
        resultList.append([refind_RefHeight[k] , average])
    return resultList

if __name__ == '__main__':
    average_calculate()
    # 패키지별로 분류
    for k in range(0, len(resultList)):
        RefHeights = resultList[k][0].split('_')
        if RefHeights[3] == '[PkgType]0':
            resistor.append(resultList[k][1])

        elif RefHeights[3] == '[PkgType]1':
            capacitor.append(resultList[k][1])

    # 해당 패키지가 없으면 0 으로 표기
    resi_ave = sum(resistor) / len(resistor) if (resistor != True) else resi_ave
    capa_ave = sum(capacitor) / len(capacitor) if (capacitor != True) else capa_ave

    # 해당 폴더에 있는 정제된 capacitor , resistor 총합의 평균
    print('Resistor의 평균 = %0.3f , Capacitor의 평균 = %0.3f' % (resi_ave, capa_ave))




