
import torch
import torchvision.datasets as dsets
import torchvision.transforms as transforms
from torch.autograd import Variable




def predict():
    path = "static/images"
    dict = {0: '不夜城芦荟', 1: '高砂之翁', 2: '黄丽', 3: '姬玉露', 4: '金琥', 5: '钱串',6:'生石花',7:'熊童子'}
    w=128
    h=128
    c=3

    #获得数据并转化为Tensor
    predict_data = dsets.ImageFolder(root=path,
                                      #transform=transforms.ToTensor()
                                      transform=transforms.Compose([
                                        #改变图片的size，标准化,
                                          transforms.Resize(128),
                                          transforms.CenterCrop(128),
                                          transforms.ToTensor(),
                                          transforms.Normalize((0.5, 0.5, 0.5),
                                                               (0.5, 0.5, 0.5)),
                                      ])
                                      )

    predict_loder = torch.utils.data.DataLoader(dataset=predict_data,
                                                batch_size=1,
                                                shuffle = False,
                                               )
    cnn = torch.load('net.pkl')

    for images, labels in predict_loder:
        images = Variable(images).cuda()
        labels = labels.cuda()
        output = cnn(images)
        print('输出各种多肉的预测值： ', output)
        value, predict = torch.max(output.data, 1)
        #print(predict)
        print(predict.size())
        a = predict.cpu().numpy()
        print('a=',a)
        b = a[0]
        print('最有可能的多肉种类为：第', b, '种')
        print('由此可知此多肉种类为：', dict[b])
        return dict[b],b,output


if __name__ == '__main__':
    predict()

