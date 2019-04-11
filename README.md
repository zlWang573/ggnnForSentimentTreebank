# ggnnForSentimentTreebank

这是一个使用sentiment treebank训练ggnn，以实现对一句话的情感分析的项目。

所有的工作是建立在此基础之上的：https://github.com/JamesChuanggg/ggnn.pytorch ，
所以将此链接中的内容全部搬运了过来，修改了其中一部分代码，包括以下5份代码:
main.py  model.py  utils/train.py  utils/test.py  utils/data/dataset.py

再加上sentiment treebank数据，来自:https://nlp.stanford.edu/sentiment/code.html ，
然后对其进行加工以符合ggnn的形式，原数据、加工程序C++代码、加工后的数据，全都保存在treebank文件夹中

目前这个项目还无法实现预期的功能，详细内容见document.docx

以下是原README
-------------

# A PyTorch Implementation of GGNN

This is a PyTorch implementation of the Gated Graph Sequence Neural Networks (GGNN) as described in the paper [Gated Graph Sequence Neural Networks](https://arxiv.org/abs/1511.05493) by Y. Li, D. Tarlow, M. Brockschmidt, and R. Zemel. This implementation gets 100% accuracy on node-selection bAbI task 4, 15, and 16. Their official implementation are available in the [yujiali/ggnn](https://github.com/yujiali/ggnn) repo on GitHub.

<img src="images/ggnn.png">    

## What is GGNN?
- Solve graph-structured data and problems
- A gated propagation model to compute node representations
- Unroll recurrence for a fixed number of steps and use backpropogation through time
- An output model to make predictions on nodes

## Requirements
- python==2.7
- PyTorch>=0.2

## Run 
Train and test the GGNN:
```
python main.py --cuda (use GPUs or not)
```

Suggesting configurations for each task:
```
# task 4
python main.py --task_id 4 --state_dim 4 --niter 10
# task 15
python main.py --task_id 15 --state_dim 5 --niter 10
# task 16
python main.py --task_id 16 --state_dim 10 --niter 150
```

## Results
I followed the paper, randomly picking only 50 training examples for training.
Performances are evaluated on 50 random validation examples.

| bAbI Task | Performance |
| ------| ------ | 
| 4 | 100% | 
| 15 | 100% |
| 16 | 100% |

Here's an example of bAbI deduction task (task 15)

<img src="images/babi15.png" width=700>

## Disclaimer
The data processing codes are from official implementation [yujiali/ggnn](https://github.com/yujiali/ggnn).

## TODO 
- [ ] GraphLevel Output

## References
- [Gated Graph Sequence Neural Networks](https://arxiv.org/abs/1511.05493), ICLR 2016
- [yujiali/ggnn](https://github.com/yujiali/ggnn)
