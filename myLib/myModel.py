import os
from lib.data import load_data
from lib.model import Ganomaly
import threading
import copy
import json

class MyModel(threading.Thread):
    def __init__(self, options):
        threading.Thread.__init__(self)
        self.option = options #模型参数
        self.modelINFO = {}


    def run(self): #训练模型

        # 1. 模型训练
        self.option.signalInfo.emit(-1,"开始导入数据...")
        dataloader = load_data(self.option)
        model = Ganomaly(self.option, dataloader)
        self.option.signalInfo.emit(10, "导入数据完毕！")
        self.modelINFO = model.train()

        # 2. 对训练结果进行处理，生成一个字典
        self.option.signalInfo.emit(100,"")
        self.modelINFO['opt'] = vars(self.option)
        self.modelINFO['opt'].pop('signalInfo')
        signal = self.modelINFO['opt'].pop('signal')

        self.modelINFO['modelName'] = self.modelINFO['opt'].pop('dataset')
        self.modelINFO['raw_path'] = self.modelINFO['opt'].pop('dataroot')
        self.modelINFO['desc'] = self.modelINFO['opt'].pop('desc')

        # 3. 将训练结果字典保存到json文件中
        ## 默认保存路径./output/modelsData/models.json
        # filename = './output/modelsData/models.json'
        # data = {}
        # with open(filename,'r',encoding='utf-8') as f:
        #     try:
        #         data = json.load(f)
        #     except json.decoder.JSONDecodeError: # 此处源文件没有数据,即尚未有模型被训练
        #         data = {}
        # with open(filename, 'w', encoding="utf-8") as f:
        #     data[self.modelINFO['modelName']] = self.modelINFO
        #     json.dump(data,f,sort_keys=True,indent=2)


        # 3. 将训练结果字典通过信号传递给主函数
        signal.emit(copy.deepcopy(self.modelINFO))



    def __str__(self):
        return self.modelINFO.__str__()



