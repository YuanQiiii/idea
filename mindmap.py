# auther: hongwei qin
# 主要目标：文本 -> 图像（对特定的字符串进行处理，生成对应的思维导图）
# 关系：
# 1.父子节点关系（两节点之间从属） done
# 2.关联节点关系（两节点之间相关） done
# 3.备注节点关系（节点的备注信息） done
# 运行逻辑：
# 1.读取字符串 done
# 2.解析字符串 done
#    note:
#       1.规定{[(为左标记，}])为右标记(一一配对) done
#       2.{之前的第一个被标记分割开的字符串为{}对应父子节点的根节点，[之前的第一个被标记分割开的字符串为关联节点的根节点，(之前的第一个被标记分割开的字符串为备注节点的根节点 done
#       3.使用递归算法解析字符串，将字符串解析为多叉树结构 done
#   1.使用递归算法解析字符串，对于匹配的左右标记内部的字符串切片出来成一个字串继续递归直到全部解析完毕 done
#   2.使用双指针法从前后寻找第一对匹配的标记，左标记前的字符串作为节点名称向下递归 done


# 3.对除了备注节点之外的节点使用哈希函数生成唯一名称（私有属性，不能被访问，只用于查询关系节点和涂色），使用多叉树结构储存和构建思维导图，并实现可视化
# 4.使用第三方库实现思维导图的可视化（不同对象节点的颜色不同）

# 字符串格式：
# node1{node2{node3{node4}node5{node5(note1)node6[node2]}}} done
# 说明：node1为根节点，node2为node1的子节点，node3为node2的子节点，node4为node3的子节点，node5为node2的子节点,note1是node5的备注节点,node6为node5的子节点，node2为node6的关联节点 done

import hashlib
import matplotlib.pyplot as plt
import networkx as nx

# 定义节点类
class Node:
    def __init__(self, name):
        self.name = name
        self.note = [] # 备注节点
        self.children = [] # 子节点
        self.associations = [] # 关联节点

saved_node = dict() # 保存节点的哈希表

# 找到与左标记匹配的右标记的位置
def find_matching(s, start ,left, right):
    count = 1
    for i in range(start+1,len(s)): # 从后往前找
        if s[i] == left:
            count += 1     
        elif s[i] == right:
            count -= 1
            if count == 0:
                return i
    return -1

# 解析字符串,生成树
def parse_string(s):
    root = None # 初始化根节点
    if (len(s) != 0) and ('{' not in s) and ('[' not in s) and ('(' not in s): # 字符串不为空且不包含左标记
        if s in saved_node:
            return saved_node[s]
        else:
            root = Node(s) # 生成根节点
            saved_node[s] = root
        return root
    i = 0 # 当前位置
    while i < len(s):
        if s[i] in ['{', '[', '(']: # 左标记
            left = s[i] # 左标记
            right = {'{': '}', '[': ']', '(': ')'}[left] # 右标记
            end = find_matching(s,i,left, right)
            if end is None:
                print(f"未匹配的 '{left}' 在位置 {i}")
                break
            content = s[i + 1:end] # 左右标记之间的字符串,左包含右不包含
            name = s[:i].split('}')[-1].split(']')[-1].split(')')[-1] # 左标记之前任意右标记之后的字符串作为节点名称

            if name in saved_node:
                root = saved_node[name]
            else:
                root = Node(name)
                saved_node[name] = root

            node = parse_string(content) # 递归解析左右标记之间的字符串

            if node is not None: # 递归解析的结果不为空
                if left == '(':
                    root.note.append(node)
                elif left == '[':
                    root.associations.append(node)
                elif left == '{':
                    root.children.append(node)
            i = end + 1
        else:
            i += 1
    return root

# 递归生成节点和边
def add_nodes_edges(graph, node, parent=None):
    if node is None or node.name is None:
        return
    
    # 使用哈希函数生成唯一名称
    node_id = hashlib.md5(node.name.encode()).hexdigest()
    
    # 添加节点
    graph.add_node(node_id, label=node.name)
    
    # 添加边
    if parent:
        parent_id = hashlib.md5(parent.name.encode()).hexdigest()
        graph.add_edge(parent_id, node_id)
    
    # 递归添加子节点
    for child in node.children:
        add_nodes_edges(graph, child, node)
    
    # 递归添加备注节点
    for note in node.note:
        add_nodes_edges(graph, note, node)
    
    # 递归添加关联节点
    for assoc in node.associations:
        add_nodes_edges(graph, assoc, node)

# 可视化思维导图
def visualize_mindmap(root):
    graph = nx.DiGraph()
    add_nodes_edges(graph, root)
    
    pos = nx.spring_layout(graph)
    labels = nx.get_node_attributes(graph, 'label')
    
    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, labels=labels, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_family="SimHei")
    plt.title("思维导图")
    plt.show()

# 示例用法
if __name__ == "__main__":
    input_str = 'node1{node2{node3{node4(note1)node5[]}}}'
    root = parse_string(input_str)
    item = saved_node.items()
    for key, value in item:
        print(key, value)
        
    if root:
        # 可视化思维导图
        visualize_mindmap(root)
        print("done")
    else:
        print("未能解析输入字符串。")