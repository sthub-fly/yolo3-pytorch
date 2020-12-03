import torch
import torch.nn as nn
from collections import OrderedDict
from nets.darknet import darknet53

def conv2d(filter_in, filter_out, kernel_size):
    pad = (kernel_size - 1) // 2 if kernel_size else 0
    return nn.Sequential(OrderedDict([
        ("conv", nn.Conv2d(filter_in, filter_out, kernel_size=kernel_size, stride=1, padding=pad, bias=False)),
        ("bn", nn.BatchNorm2d(filter_out)),
        ("relu", nn.LeakyReLU(0.1)),
    ]))


def make_last_layers(filters_list, in_filters, out_filter):
    m = nn.ModuleList([
        # 首先用1*1的卷积调整通道数，在利用3*3的卷积进行特征提取 减少网络参数量
        conv2d(in_filters, filters_list[0], 1),
        conv2d(filters_list[0], filters_list[1], 3),

        conv2d(filters_list[1], filters_list[0], 1),
        conv2d(filters_list[0], filters_list[1], 3),

        conv2d(filters_list[1], filters_list[0], 1),

        conv2d(filters_list[0], filters_list[1], 3),
        nn.Conv2d(filters_list[1], out_filter, kernel_size=1,
                                        stride=1, padding=0, bias=True)
    ])
    return m

class YoloBody(nn.Module):
    def __init__(self, config):
        super(YoloBody, self).__init__()
        self.config = config
        #  backbone
        self.backbone = darknet53(None)  #获取darknext53 的结构，保存在self.backbone

        out_filters = self.backbone.layers_out_filters
        #  last_layer0 3*(5+num_classes)=3*(5+20)=3*(4+1+20)=75
        final_out_filter0 = len(config["yolo"]["anchors"][0]) * (5 + config["yolo"]["classes"])
        self.last_layer0 = make_last_layers([512, 1024], out_filters[-1], final_out_filter0)

        #  embedding1  75
        final_out_filter1 = len(config["yolo"]["anchors"][1]) * (5 + config["yolo"]["classes"])
        self.last_layer1_conv = conv2d(512, 256, 1)
        self.last_layer1_upsample = nn.Upsample(scale_factor=2, mode='nearest')
        # 获得一个26*26*256的特征层
        self.last_layer1 = make_last_layers([256, 512], out_filters[-2] + 256, final_out_filter1)

        #  embedding2  75
        final_out_filter2 = len(config["yolo"]["anchors"][2]) * (5 + config["yolo"]["classes"])
        self.last_layer2_conv = conv2d(256, 128, 1)
        self.last_layer2_upsample = nn.Upsample(scale_factor=2, mode='nearest')
        # 52*52*128
        self.last_layer2 = make_last_layers([128, 256], out_filters[-3] + 128, final_out_filter2)


    def forward(self, x):
        def _branch(last_layer, layer_in):
            for i, e in enumerate(last_layer):
                layer_in = e(layer_in)
                if i == 4:
                    out_branch = layer_in
            return layer_in, out_branch  #5次卷积后的结果保存在out_branch里
        #  backbone 获取主干网络提取的三个特征层
        # x2-》52*52*256  x1-》26*26*512   x0-》13*13*1024
        x2, x1, x0 = self.backbone(x)
        #  yolo branch 0
        out0, out0_branch = _branch(self.last_layer0, x0)

        #  yolo branch 1  5次卷积后的结果进行卷积+上采样
        x1_in = self.last_layer1_conv(out0_branch)
        x1_in = self.last_layer1_upsample(x1_in)
        x1_in = torch.cat([x1_in, x1], 1)    #与主干网络获取的特征层堆叠
        out1, out1_branch = _branch(self.last_layer1, x1_in)

        #  yolo branch 2   继续卷积+上采样
        x2_in = self.last_layer2_conv(out1_branch)
        x2_in = self.last_layer2_upsample(x2_in)
        x2_in = torch.cat([x2_in, x2], 1)
        out2, _ = _branch(self.last_layer2, x2_in)  #5次卷积后的结果用下划线代替
        return out0, out1, out2
        '''
         以下几个out分别表示3个红色框回归预测结果和分类预测结果
         out0->13*13 
         out1->26*26
         out2->52*52
         利用out0,1,2去判断先验框内部是否真实的包含物体，以及这个物体的种类，
         还有怎么样去调整这个先验框可以获得最终的预测结果
        '''

