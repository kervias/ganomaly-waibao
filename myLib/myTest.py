import os
from lib.data import load_data
from lib.model import Ganomaly
import threading
import copy


class MyTest(threading.Thread):
    def __init__(self, options, modelData):
        threading.Thread.__init__(self)
        self.option = options
        self.resultNor = None # 测试结果（正常样本）
        self.resultAbn = None # 测试结果（异常样本
        self.desc = '' #测试结果描述
        self.modelData = modelData

    def run(self):
        # self.option.isize = 128
        self.dataloader = load_data(self.option)
        model = Ganomaly(self.option, self.dataloader)
        minVal = self.modelData[0]
        maxVal = self.modelData[1]
        threshold = self.modelData[2]
        resNor, resAbn = model.FinalTest(minVal, maxVal, threshold)
        opt = {}
        opt['path'] = self.option.dataroot
        opt['modelName'] = self.option.dataset
        self.option.signal.emit(copy.deepcopy(resNor), copy.deepcopy(resAbn), copy.deepcopy(opt))


