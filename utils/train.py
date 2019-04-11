import torch
import torch.tensor

from torch.autograd import Variable

def train(epoch, dataloader, net, criterion, optimizer, opt):
    net.train()
    """
    以下m_node为当前图节点数量
        lable为节点与子树上最远叶子节点距离，lable == 0为叶子节点
        lable并不参与运算，用于统计信息
    """
    for i, (m_node, adj_matrix, annotation, lable, target) in enumerate(dataloader, 0): 
        net.zero_grad()
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

        output = net(init_input, annotation, adj_matrix ,m_node)
        
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        if i % int(len(dataloader) / 10 + 1) == 0 :
            print('[%d/%d][%d/%d] Loss: %.4f' % (epoch, opt.niter, i, len(dataloader), loss.data[0]))
