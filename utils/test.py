import torch
from torch.autograd import Variable
import numpy as np

def test(dataloader, net, criterion, optimizer, opt):
    test_loss = 0
    correct = 0
    
    lable_correct = np.zeros([30]) #各个lable正确数量
    lable_num = np.zeros([30]) #各个lable总数量
    class_correct = np.zeros([5]) #各分类正确数量
    class_num = np.zeros([5]) #各分类总数量
    
    net.eval()
    for i, (m_node, adj_matrix, annotation, lable, target) in enumerate(dataloader, 0):
        padding = torch.zeros(len(annotation), m_node, opt.state_dim - opt.annotation_dim).double()
        init_input = torch.cat((annotation, padding), 2)
        
        if opt.cuda:
            init_input = init_input.cuda()
            adj_matrix = adj_matrix.cuda()
            annotation = annotation.cuda()
            target = target.cuda()

        init_input = Variable(init_input)
        adj_matrix = Variable(adj_matrix)
        annotation = Variable(annotation)
        target = Variable(target)
        
        output = net(init_input, annotation, adj_matrix, m_node)
        
        test_loss += criterion(output, target).data[0]
        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()
        
        #print('answer:{:d}, output:{:d} ,deep:{:d}'.format(target[0].int(),pred[0][0].int(),lable[0]))
        
        lable_num[lable[0]] += 1
        class_num[target[0] % 5] += 1
        if target[0] == pred[0][0]:
            lable_correct[lable[0]] += 1
            class_correct[target[0] % 5] += 1

    test_loss /= len(dataloader.dataset)
    print('Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)'.format(
        test_loss, correct, len(dataloader.dataset),
        100. * correct / len(dataloader.dataset)))
    
    for i in range(0, 30):
        print('height {}: {} {}'.format(i, lable_num[i], lable_correct[i]))
    for i in range(0, 5):
        print('class {}: {} {}'.format(i, class_num[i], class_correct[i]))
