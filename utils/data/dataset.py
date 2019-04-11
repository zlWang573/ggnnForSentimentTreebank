import numpy as np

def load_graphs_from_file(file_name):
    data_list = []
    edge_list = []
    target_list = []
    annotation_list = []
    with open(file_name,'r') as f:
        for line in f:
            if len(line.strip()) == 0:
                data_list.append([edge_list,target_list,annotation_list])
                edge_list = []
                target_list = []
                annotation_list = []
            else:
                digits = []
                line_tokens = line.split(" ")
                if line_tokens[0] == "?":
                    for i in range(1, len(line_tokens)):
                        digits.append(int(line_tokens[i]))
                    target_list.append(digits)
                else :
                    if line_tokens[0] == "!":
                        for i in range(1, len(line_tokens)):
                            annotation_list.append(int(line_tokens[i]))
                    else:
                        for i in range(len(line_tokens)):
                            digits.append(int(line_tokens[i]))
                        edge_list.append(digits)
    return data_list

def find_max_edge_id(data_list):
    max_edge_id = 0
    for data in data_list:
        edges = data[0]
        for item in edges:
            if item[1] > max_edge_id:
                max_edge_id = item[1]
    return max_edge_id

def find_max_node_id(data_list):
    max_node_id = 0
    for data in data_list:
        edges = data[0]
        for item in edges:
            if item[0] > max_node_id:
                max_node_id = item[0]
            if item[2] > max_node_id:
                max_node_id = item[2]
    return max_node_id

def find_max_task_id(data_list):
    max_node_id = 0
    for data in data_list:
        targe = data[1]
        for item in targe:
            if item[0] > max_node_id:
                max_node_id = item[0]
    return max_node_id

def split_set(data_list):
    n_examples = len(data_list)
    idx = range(n_examples)
    #8544 2210 train_num test_num
    #485 103 for small
    train = idx[:485]
    val = idx[-103:]
    return np.array(data_list)[train],np.array(data_list)[val]

def data_convert(data_list, n_annotation_dim, n_node):
    n_tasks = find_max_task_id(data_list)
    task_data_list = []
    for i in range(n_tasks):
        task_data_list.append([])
    for item in data_list:
        edge_list = item[0]
        target_list = item[1]
        annotation_list = item[2]
        m_nodes = len(annotation_list)
        for target in target_list:
            task_type = target[0]
            task_output = target[-1] - 1
            annotation = np.zeros([m_nodes, n_annotation_dim])
            lable = target[2]
            for i in range(0, 5):
                annotation[target[1]+i-1][1] = 1
            for i in range(0, m_nodes):
                annotation[i][0] = annotation_list[i]*1
            task_data_list[task_type-1].append([m_nodes, edge_list, annotation, lable, task_output])
    return task_data_list

def create_adjacency_matrix(edges, n_nodes, n_edge_types):
    a = np.zeros([n_nodes, n_nodes * n_edge_types * 2])
    for edge in edges:
        src_idx = edge[0]
        e_type = edge[1]
        tgt_idx = edge[2]
        a[tgt_idx-1][(e_type - 1) * n_nodes + src_idx - 1] =  1
        a[src_idx-1][(e_type - 1 + n_edge_types) * n_nodes + tgt_idx - 1] =  1
    return a


class bAbIDataset():
    """
    Load bAbI tasks for GGNN
    """
    def __init__(self, annotation_dim, path, task_id, is_train):
        all_data = load_graphs_from_file(path)
     
        self.n_edge_types =  find_max_edge_id(all_data)
        self.n_tasks = find_max_task_id(all_data)
        self.n_node = find_max_node_id(all_data)

        all_task_train_data, all_task_val_data = split_set(all_data)

        if is_train:
            all_task_train_data = data_convert(all_task_train_data, annotation_dim, self.n_node)
            self.data = all_task_train_data[task_id]
        else:
            all_task_val_data = data_convert(all_task_val_data, annotation_dim, self.n_node)
            self.data = all_task_val_data[task_id]

    def __getitem__(self, index):
        m_node = self.data[index][0]
        am = create_adjacency_matrix(self.data[index][1], m_node, self.n_edge_types)
        annotation = self.data[index][2]
        lable = self.data[index][3]
        target = self.data[index][4]
        return m_node, am, annotation, lable, target

    def __len__(self):
        return len(self.data)

