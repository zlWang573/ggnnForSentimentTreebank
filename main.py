import argparse
import random

import torch
import torch.nn as nn
import torch.optim as optim

from model import GGNN
from utils.train import train
from utils.test import test
from utils.data.dataset import bAbIDataset
from utils.data.dataloader import bAbIDataloader

parser = argparse.ArgumentParser() 
#parser.add_argument('--task_id', type=int, default=4, help='bAbI task id')
parser.add_argument('--question_id', type=int, default=0, help='question types')
parser.add_argument('--workers', type=int, help='number of data loading workers', default=2)
parser.add_argument('--batchSize', type=int, default=1, help='input batch size') #每幅图节点数量不同，所以必须是1了
parser.add_argument('--state_dim', type=int, default=5, help='GGNN hidden state size')
parser.add_argument('--n_steps', type=int, default=25, help='propogation steps number of GGNN')
parser.add_argument('--niter', type=int, default=5, help='number of epochs to train for')
parser.add_argument('--lr', type=float, default=0.005, help='learning rate')
parser.add_argument('--cuda', action='store_true', help='enables cuda')
parser.add_argument('--verbal', action='store_true', help='print training info or not')
parser.add_argument('--manualSeed', type=int, help='manual seed')

opt = parser.parse_args()
print(opt)

if opt.manualSeed is None:
    opt.manualSeed = random.randint(1, 10000)
print("Random Seed: ", opt.manualSeed)
random.seed(opt.manualSeed)
torch.manual_seed(opt.manualSeed)

#opt.dataroot = 'babi_data/processed_1/train/%d_graphs.txt' % opt.task_id
#opt.dataroot = 'treebank/treebank_graph.txt'
opt.dataroot = 'treebank/treebank_graph_small.txt'
#opt.dataroot = 'treebank/treebank_graph_OnlyRoot.txt'

if opt.cuda:
    torch.cuda.manual_seed_all(opt.manualSeed)

def main(opt):
    opt.annotation_dim = 2  # for NLP
    
    train_dataset = bAbIDataset(opt.annotation_dim, opt.dataroot, opt.question_id, True)
    train_dataloader = bAbIDataloader(train_dataset, batch_size=opt.batchSize, \
                                      shuffle=True, num_workers=2)

    test_dataset = bAbIDataset(opt.annotation_dim, opt.dataroot, opt.question_id, False)
    test_dataloader = bAbIDataloader(test_dataset, batch_size=opt.batchSize, \
                                     shuffle=True, num_workers=2)

    opt.n_edge_types = train_dataset.n_edge_types
    opt.n_node = train_dataset.n_node 
    net = GGNN(opt)
    net.double()
    print(net)
    criterion = nn.CrossEntropyLoss()

    if opt.cuda:
        net.cuda()
        criterion.cuda()
        
    optimizer = optim.Adam(net.parameters(), lr=opt.lr)
    for epoch in range(0, opt.niter):
        train(epoch, train_dataloader, net, criterion, optimizer, opt)
        test(test_dataloader, net, criterion, optimizer, opt)

if __name__ == "__main__":
    main(opt)
