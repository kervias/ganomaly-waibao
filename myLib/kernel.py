import copy
from lib.data import load_data
from lib.model import Ganomaly
from options import Options
from myLib.myModel import MyModel
from myLib.myTest import MyTest
import gc
import json
import time
import inspect
import ctypes

class Kernel(object):
    def __init__(self):
        self.init_KEYData()

    def init_KEYData(self):
        # 控制数据
        self.isTrain = False  # 是否在训练
        self.isTest = False   # 是否在测试
        self.isTested = False # 是否测试完毕

        # 存储数据
        self.modelTrain = None  # 单例模式，用作训练的类实例
        self.modelTest = None  # 单例模式，用作测试的类实例
        self.modelsData = self.load_data() # 导入外存中的所有模型

        self.testData = {}

    def load_data(self):
        # 1. 从json文件中读取模型的数据
        # 2. 返回数据
        filename = './output/modelsData/models.json'
        data = None
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:  # 此处源文件没有数据,即尚未有模型被训练
                data = {}
        return data


    def get_modelData(self):
        # 将模型数据传递给主类
        return copy.deepcopy(self.modelsData)

    def set_OnemodelData(self, data):
        # 从主类获取一个训练好的模型数据
        filename = './output/modelsData/models.json'
        with open(filename, 'w', encoding="utf-8") as f:
            self.modelsData[data['modelName']] = data
            json.dump(self.modelsData, f, sort_keys=True, indent=2)

    def set_testData(self, data):
        # 从主类获取测试结果，这个可以不需要
        self.testData = data

    def set_modelData(self, data):
        self.modelsData = data
        filename = './output/modelsData/models.json'
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(self.modelsData, f, sort_keys=True, indent=2)


    def startTrain(self, params):
        params['signalInfo'].emit(0, "开始训练...")
        dataset = params['name'] #'cus_mnist_2'
        dataroot = params['path']  #'E:\ProjectSet\Pycharm\WAIBAO\cus_mnist2'

        opt = Options().parse(dataset)
        opt.signal = params['signal']
        opt.load_weights = False
        opt.signalInfo = params['signalInfo']
        opt.lr = params['-lr']
        opt.batchsize = params['-batchsize']
        opt.niter = params['-niter']
        opt.nz = params['-nz']
        opt.desc = params['info']
        opt.dataroot = dataroot
        # opt.isize = 128
        print(opt)

        self.modelTrain = MyModel(opt)
        self.modelTrain.start()


    def startTest(self,params):
        params['signalInfo'].emit(0, "开始检测...")
        dataset = params['modelName']  # 'cus_mnist_2'
        dataroot = params['path']  # 'E:\ProjectSet\Pycharm\WAIBAO\cus_mnist2'
        opt = Options().parse(dataset)
        opt.isTrain = False
        opt.load_weights = True
        opt.signal = params['signal']
        opt.signalInfo = params['signalInfo']
        opt.lr = self.modelsData[dataset]['opt']['lr']
        opt.nz = self.modelsData[dataset]['opt']['nz']
        opt.batchsize = self.modelsData[dataset]['opt']['batchsize']
        opt.dataroot = dataroot

        print(opt)

        self.modelTest = MyTest(opt, [self.modelsData[dataset]['minVal'], self.modelsData[dataset]['maxVal'], self.modelsData[dataset]['proline']])
        self.modelTest.start()

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def kill_thread(self):
        if self.isTrain == True:
            self.stop_thread(self.modelTrain)
            del self.modelTrain
            gc.collect()
        elif self.isTest == True:
            self.stop_thread(self.modelTest)
            del self.modelTest
            gc.collect()


    def stop_thread(self, thread1):
        self._async_raise(thread1.ident, SystemExit)


