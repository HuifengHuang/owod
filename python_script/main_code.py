import os
import shutil
import torch
# import clip
from PIL import Image
import json
from tqdm import tqdm
import pickle
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import random
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

class_name = "zebra"
texts = [f'A photo of {class_name}']
device = torch.device(f"cuda:{0}" if torch.cuda.is_available() else "cpu")
model, preprocess = clip.load("ViT-B/16", device=device)
batch_size = 32
threshold = 0.3


def get_text_embedding(texts):
    ### Get text embedding
    texts = clip.tokenize(texts).to(device)
    embeddings = model.encode_text(texts)
    embeddings /= embeddings.norm(dim=-1, keepdim=True)
    text_embedding = embeddings.mean(dim=0, keepdim=True)
    text_embedding /= text_embedding.norm(dim=-1, keepdim=True)
    return text_embedding


def encode_unknown_images(model, preprocess, encoded_file, device='cuda'):
    '''
    Encode unknown images and save the results to a file
    '''
    image_folder = 'unknown_images_try1/images'
    encoded_data = []
    image_paths = [os.path.join(image_folder, fname) for fname in os.listdir(image_folder) if fname.endswith('.jpg')]

    with torch.no_grad():
        for i in tqdm(range(0, len(image_paths), batch_size), desc="Processing batches"):
            batch_paths = image_paths[i:i + batch_size]
            images = []

            for image_path in batch_paths:
                image = Image.open(image_path)
                images.append(preprocess(image).unsqueeze(0))

            image_inputs = torch.cat(images).to(device)
            image_features = model.encode_image(image_inputs)
            image_features /= image_features.norm(dim=-1, keepdim=True)

            for j, image_path in enumerate(batch_paths):
                encoded_data.append((image_path, image_features[j].cpu().numpy()))

    with open(encoded_file, 'wb') as f:
        pickle.dump(encoded_data, f)


def batch_process_with_encoded_data(encoded_file, threshold, batch_size):
    '''
    对编码文件中的数据进行批处理
    根据输入的类别名称进行图片筛选
    '''
    output_dir = f"{class_name}_images"
    with open(encoded_file, 'rb') as f:
        encoded_data = pickle.load(f)
    print(len(encoded_data))
    text_features = get_text_embedding(texts)
    filter_features_list = []
    result_list = []
    for i in tqdm(range(0, len(encoded_data), batch_size), desc="Processing batches"):
        batch_data = encoded_data[i:i + batch_size]
        image_features_list = []
        images_paths = []

        for item in batch_data:
            image_path, image_features = item
            images_paths.append(image_path)
            # bboxs.append(bbox_coords)
            image_features_list.append(image_features)

        image_features_array = np.vstack(image_features_list)
        image_features_tensor = torch.tensor(image_features_array).to(device)

        # 计算相似度
        similarity = (image_features_tensor @ text_features.T).squeeze(1)

        # 筛选出相似度高的图片并保存
        for j, sim in enumerate(similarity):
            if sim.item() > threshold:
                metadata = f"{images_paths[j]} {similarity[j]}"
                result_list.append(metadata)
                filter_features_list.append(image_features_list[j])
                original_image = Image.open(images_paths[j])
                # crop_coords = list(map(float, bboxs[j]))
                # cropped_image = original_image.crop(crop_coords)
                save_path = os.path.join(output_dir, f"{os.path.basename(images_paths[j]).split('.')[0]}_{j}.jpg")
                original_image.save(save_path)

    # 保存结果到文本文件
    txt_path = f"{output_dir}/{class_name}_result.txt"
    with open(txt_path, 'w') as f:
        for item in result_list:
            f.write(item + "\n")
    return filter_features_list


# 加载编码结果并进行聚类
def load_and_cluster_images(image_features_array, num_clusters=20):
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(image_features_array)

    labels = kmeans.labels_

    return labels, image_features_array


# 降维函数
def reduce_dimensionality(features, method='tsne'):
    if method == 'pca':
        pca = PCA(n_components=2)
        reduced_features = pca.fit_transform(features)
    elif method == 'tsne':
        tsne = TSNE(n_components=2, perplexity=30, n_iter=300)
        reduced_features = tsne.fit_transform(features)
    else:
        raise ValueError("Unsupported dimensionality reduction method")
    # print(reduced_features)
    return reduced_features


# 确定聚类数量的方法：手肘法和轮廓系数法
def determine_optimal_clusters(features):
    sse = []
    silhouette_scores = []
    K = range(10, 25)  # 可以根据需要调整范围
    # K = [11]
    # todo

    for k in K:
        print(k)
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(features)
        sse.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(features, kmeans.labels_))

    return K, sse, silhouette_scores


def cluster_all_unknown(encoded_file):
    with open(encoded_file, 'rb') as f:
        encoded_data = pickle.load(f)
    '''
    encoded_file中的文件格式如下：
    image_path, bbox, image_features
    '''

    image_features_list = [item[1] for item in encoded_data]
    image_features_list = random.sample(image_features_list, 10000)
    image_features_array = np.vstack(image_features_list)

    # 确定最佳聚类数量
    K, sse, silhouette_scores = determine_optimal_clusters(image_features_array)
    optimal_k = K[np.argmax(silhouette_scores)]
    print(f"Optimal number of clusters: {optimal_k}")
    # # 执行聚类分析
    num_clusters = optimal_k
    labels, image_features_array = load_and_cluster_images(image_features_array, num_clusters=num_clusters)
    # 降维到2D
    reduce_method = 'tsne'
    reduced_features = reduce_dimensionality(image_features_array, method=reduce_method)
    print(reduced_features.shape)
    # 绘制散点图
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=labels, cmap='tab20', alpha=1)
    plt.colorbar(scatter, ticks=range(num_clusters), label='Clusters')
    plt.title("KMeans Clustering of Images (2D PCA)")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.savefig(f"cluster_scatter_plot_{reduce_method}_{num_clusters}.png")
    # 获取轴范围
    x_min, x_max = plt.gca().get_xlim()
    y_min, y_max = plt.gca().get_ylim()

    filter_reduced_features, filter_labels = filter_image(image_features_list, threshold, reduced_features, labels)
    filter_reduced_features = np.vstack(filter_reduced_features)
    print(filter_reduced_features.shape)
    print(len(filter_labels))
    # 绘制散点图
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(filter_reduced_features[:, 0], filter_reduced_features[:, 1], c=filter_labels,
                          cmap=scatter.get_cmap(), alpha=1)
    plt.colorbar(scatter, ticks=range(num_clusters), label='Clusters')
    plt.title("KMeans Clustering of Images (2D PCA)")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    # 设置相同的轴范围
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.savefig(f"cluster_scatter_plot_{reduce_method}_{num_clusters - 1}.png")


def filter_image(image_features_list, threshold, reduced_features, labels):
    text_features = get_text_embedding(texts)
    filter_features_list = []
    filter_reduced_features = []
    filter_labels = []
    for i in tqdm(range(0, len(image_features_list), batch_size), desc="Processing batches"):
        features_list = image_features_list[i:i + batch_size]
        reduced_features_list = reduced_features[i:i + batch_size]
        labels_list = labels[i:i + batch_size]
        image_features_array = np.vstack(features_list)
        image_features_tensor = torch.tensor(image_features_array).to(device)

        # 计算相似度
        similarity = (image_features_tensor @ text_features.T).squeeze(1)

        # 筛选出相似度高的图片并保存
        for j, sim in enumerate(similarity):
            if sim.item() < threshold:
                filter_features_list.append(features_list[j])
                filter_reduced_features.append(reduced_features_list[j])
                filter_labels.append(labels_list[j])
    return filter_reduced_features, filter_labels


def tsne_and_kmeans(encoded_file):
    """
    使用t-SNE降维和k-means聚类
    输出：{[图片名,降维数据（x）,降维数据（y）,标签名],...}
    """

    with open(encoded_file, 'rb') as f:
          encoded_data = pickle.load(f)
    encoded_data_sample = random.sample(encoded_data, 10000)
    image_features_list = [item[1] for item in encoded_data_sample]
    image_names_list = [item[0] for item in encoded_data_sample]
    image_features_array = np.vstack(image_features_list)


     # # 执行聚类分析
    num_clusters = 20
    labels, image_features_array = load_and_cluster_images(image_features_array, num_clusters=num_clusters)
     # print(labels)
     # print(image_features_array)

    reduce_method = 'tsne'
    reduced_features = reduce_dimensionality(image_features_array, method=reduce_method)
     # # 确定最佳聚类数量
     # K, sse, silhouette_scores = determine_optimal_clusters(image_features_array)
     # optimal_k = K[np.argmax(silhouette_scores)]
     # print(f"Optimal number of clusters: {optimal_k}")

    result = constract(image_names_list, reduced_features, labels)
    # output_file = 'data1.py'
    #  # 将结果写入到data.py文件中
    # with open(output_file, 'w') as f:
    #     f.write("def getData():\n")
    #     f.write("    return [\n")
    #     for item in result:
    #         f.write(f"        ['{item[0]}', {item[1]}, {item[2]}, {item[3]}],\n")
    #     f.write("    ]\n")
    return result


def constract(one_dimension, two_dimension, other_one):
    result = []
    for one, two, another in zip(one_dimension, two_dimension, other_one):
        result.append([one, float(two[0]), float(two[1]), int(another)])
    for i in range(1,2):
        print(result[i])
    return result


if __name__ == '__main__':
    encoded_file = 'encoded2.pkl'
    # print(tsne_and_kmeans(encoded_file))

    # cluster_all_unknown(encoded_file)
    # batch_process_with_encoded_data(encoded_file, threshold, batch_size)
