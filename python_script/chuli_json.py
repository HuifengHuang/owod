import os
import json

def filter_graph(input_file, output_file,importance_min, importance_max):
    # 读取 JSON 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 筛选节点
    filtered_nodes = [
        node for node in data['nodes']
        if importance_min <= int(node['importance']) <= importance_max
    ]
    # 获取筛选后节点的 ID 列表
    valid_node_ids = {node['id'] for node in filtered_nodes}
    
    # 筛选链接
    filtered_links = [
        link for link in data['links']
        if link['source'] in valid_node_ids and link['target'] in valid_node_ids
    ]
    
    # 生成新的数据结构
    filtered_data = {
        'nodes': filtered_nodes,
        'links': filtered_links
    }

    # 保存到新的 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    return filtered_data

# 使用示例
input_file = 'D:\\博士阶段\\代码\\owod\\src\\assets\\GranDf_caption_gcg_noun_graph.json'
output_file = 'D:\\博士阶段\\代码\\owod\\src\\assets\\filtered_output.json'
importance_min =20
importance_max = 30

filter_graph(input_file, output_file, importance_min, importance_max)
