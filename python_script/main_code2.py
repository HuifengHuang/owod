import os
import shutil
import torch
import clip
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from PIL import Image
import random
from shutil import copyfile
import numpy as np
from tqdm import tqdm
from openai import OpenAI



device = torch.device(f"cuda:{1}" if torch.cuda.is_available() else "cpu")
model, preprocess = clip.load("ViT-B/16", device=device)
batch_size = 32

def get_text_embedding(class_name):
    ### Get text embedding
    texts =  [f'A single whole {class_name}']
    texts = clip.tokenize(texts).to(device)
    embeddings = model.encode_text(texts)
    embeddings /= embeddings.norm(dim=-1, keepdim=True)
    text_embedding = embeddings.mean(dim=0, keepdim=True)
    text_embedding /= text_embedding.norm(dim=-1, keepdim=True)
    return text_embedding

def find_similar_images(encoded_file, image_path,top_n=100):
    ###输入一张图片的路径，找到与之相似的top_n张图片
    ###直接在所有图片中搜索，速度可行
    with open(encoded_file, 'rb') as f:
        encoded_data = pickle.load(f)
    #image_features_list = random.sample(encoded_data, 10000)
    # 提取所有图片的编码
    output_folder=f"similar_images"
    image = Image.open(image_path)
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        target_encoding = model.encode_image(image_input)
        target_encoding /= target_encoding.norm(dim=-1, keepdim=True)
    target_encoding=target_encoding.cpu().numpy()


    image_encodings=[]
    image_add=[]
    for item in encoded_data:
        image_encodings.append(item[1])
        image_add.append(item[0])
    #print(image_encodings[0])
    #print(image_encodings.shape)
    # 计算目标编码与所有图片编码之间的余弦相似度
    similarities = cosine_similarity(target_encoding, image_encodings)[0]
    
    # 获取相似度最高的图片索引
    similar_indices = np.argsort(similarities)[::-1][:top_n]
        # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 复制相似的图片到输出文件夹
    similar_images = [(image_add[i], similarities[i]) for i in similar_indices]
    for i, (image_path, similarity) in enumerate(similar_images):
        output_path = os.path.join(output_folder, f"similar_{i+1}_{similarity}.jpg")
        copyfile(image_path, output_path)
        print(f"Stored: {output_path}, Similarity: {similarity}")

    return similar_images

def get_HardAndSimple(encoded_file,class_name):
    '''
    对编码文件中的数据进行批处理
    根据输入的class_name名称进行图片筛选
    保存的simple图片在文件夹是按照相似度从低到高排序的，推荐出来的时候尽量从高到低推荐出来
    '''

    # 初始化最大相似度
    similarity_list = []
    threshold = 0.25
    output_dir=f"{class_name}_images"
    if not os.path.exists(os.path.join(output_dir,"simple")) or not os.path.exists(os.path.join(output_dir,"hard")):
        os.makedirs(os.path.join(output_dir,"simple"))
        os.makedirs(os.path.join(output_dir,"hard"))

    with open(encoded_file, 'rb') as f:
        encoded_data = pickle.load(f)
    print(len(encoded_data))
    text_features = get_text_embedding(class_name)
    images_paths = []
    for i in tqdm(range(0, len(encoded_data), batch_size), desc="Processing batches"):
        batch_data = encoded_data[i:i + batch_size]
        image_features_list = []
        # images_paths = []
        
        for item in batch_data:
            image_path, image_features = item
            images_paths.append(image_path)
            image_features_list.append(image_features)
        
        image_features_array = np.vstack(image_features_list)
        image_features_tensor = torch.tensor(image_features_array).to(torch.float32)
        text_features = text_features.to(torch.float32)
        
        # 计算相似度
        # print("image_features_tensor:" + type(image_features_tensor))
        # print("text_features:" + type(text_features))
        # print("text_features.T:" + type(text_features.T))
        similarity = (image_features_tensor @ text_features.T).squeeze(1)
        
        # 将相似度添加到列表中
        similarity_list.append(similarity.detach().cpu().numpy())

    all_similarities = np.concatenate(similarity_list)

    ###确定大于0.25相似度的图片个数，展示出来
    min_similarity = 0.25
    image_number = np.sum(all_similarities >= min_similarity)
    print(f"Number of images with similarity >= {min_similarity}: {image_number}")
    # 确定最大值区间的最小值
    bin_interval = 0.005
    max_bin_start = 0.34
    while np.sum(all_similarities >= max_bin_start) < 150 and max_bin_start > 0:
        max_bin_start -= bin_interval
    max_bin_start+=bin_interval
    # 确定区间
    bins = np.arange(max_bin_start - 10 * bin_interval, max_bin_start, bin_interval).tolist()
    bins.append(0.35)
    histogram = np.zeros(len(bins) - 1)
    for j, sim in enumerate(all_similarities):
        if sim > threshold:
            for i in range(len(bins) - 1):
                if bins[i] <= sim < bins[i + 1]:
                    histogram[i] += 1
                    break
            original_image = Image.open(images_paths[j])
            if sim> max_bin_start-bin_interval:
                save_path = os.path.join(output_dir, f"simple/{sim.item():.4f}_{os.path.basename(images_paths[j]).split('.')[0]}.jpg")
                original_image.save(save_path)
            elif sim< max_bin_start-6*bin_interval and sim>max_bin_start-8*bin_interval:
                save_path = os.path.join(output_dir, f"hard/{sim.item()}_{os.path.basename(images_paths[j]).split('.')[0]}.jpg")
                original_image.save(save_path)
        # # 计算相似度在各个区间的分布
        # hist, _ = np.histogram(sim, bins=bins)
        # histogram += hist
    # 打印相似度区间分布
    for bin_start, bin_end, count in zip(bins[:-1], bins[1:], histogram):
        print(f"Similarity range {bin_start:.4f} - {bin_end:.4f}: {count}")


def ChatWithLLM(
        category, 
        model_type=None,
        str_num=10
        ):
    prompt = f"""Instructions:
You are an excellent language expert who can clearly use language to describe the unique visual features of various categories.

Task:
You will be given a specific category name and you need to use {str_num} phrase descriptions to describe the appearance characteristics of the category. I can use your characteristic phrases to determine whether the object in a certain picture belongs to this category, but unfortunately you do not have access to pictures of this category.

The following are the requirements for the generated phrases:
-The phrase description is about the visual aspect of images of this category;
-The phrase description is unique to this category and not available in other categories;
-Make sure the description is diverse and not repetitive and can cover a range of visual features of this category;
-Each descrition should describe a certain visual feature of this category;
-Each description should be as concise as possible and limited to 10 words;

Here is a example
###
Category: {{truck}}
Output:
1. Large and boxy cabin structure.
2. Extended cargo bed at the back.
3. Sturdy, heavy-duty tires.
4. Elevated ground clearance.
5. Robust and angular body shape.
###

Question:
Category: {{{category}}}
"""
    print(prompt)
    output_content = None
    try:
        client = OpenAI(
            api_key="sk-I6Okh6eCkUp7t1j5ZyNW5dGpOyhwPB8BjHkN8vGgC8YovJKT",
            base_url="https://api.chatanywhere.tech/v1"
            )
        response = client.chat.completions.create(
            model=model_type,
            messages=[
                {"role": "user", "content": prompt},
            ],
            )
        output_content = response.choices[0].message.content
        print(output_content)
        # 使用splitlines()按行分割字符串
        lines = output_content.strip().splitlines()
        # 遍历每一行，提取序号后面的描述部分
        descriptions = []
        for line in lines:
            # 使用split('.', 1)将每行以第一个点号分割成两部分
            index, desc = line.split('.', 1)
            # 输出提取的描述部分，去除首尾空格
            descriptions.append(desc.strip())
    except Exception as e:
        print("An error occurred:", e)
    assert len(descriptions) == str_num, "The number of descriptions is not 10."
    print('处理后的字符串为：')
    print(descriptions)
    return descriptions


if __name__ == '__main__':
    #image_path = '/home/xuewei/Clip_finetuning/data/RandBox/t2/train/traffic light/000000036836.jpg'
    encoded_file='encoded2.pkl'
    #find_similar_images(encoded_file,image_path)

    category="lady"
    ChatWithLLM(category,model_type='gpt-4o-ca')
    # get_HardAndSimple(encoded_file,category)