import io
import json
import os
import re

import requests
from PIL import Image
from flask import Flask, request, jsonify

from flask_cors import CORS
from data1 import getData
# from get_result import get_result_new
# from main_code import tsne_and_kmeans
# from main_code2 import find_similar_images, get_HardAndSimple, ChatWithLLM
# from result_view import get_result

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/data')
def data():
    """
    获取降维和聚类数据
    """
    encoded_file = 'encoded2.pkl'

    print("start t-sne and k-means...")
    return json.dumps(getData())
    # return json.dumps(tsne_and_kmeans(encoded_file))


@app.route('/images/<path:filename>', methods=["GET"])
def get_images(filename):
    """
    获取图片比特流
    """
    img_url = './' + filename
    with open(img_url, 'rb') as f:
        a = f.read()
    '''对读取的图片进行处理'''
    img_stream = io.BytesIO(a)
    img = Image.open(img_stream)

    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    # print(imgByteArr)
    return imgByteArr


# @app.route('/simi/<path:filename>', methods=["GET"])
# def get_similar_images(filename):
#     """
#     获取相似图片名和相似度
#     """
#     image_path = './' + filename
#     encoded_file = 'encoded2.pkl'
#     return json.dumps(find_similar_images(encoded_file, image_path))


# @app.route('/similars/<class_name>', methods=["GET"])
# def get_similars(class_name):
#     """
#     获取相似图片名和相似度
#     """
#     encoded_file = 'encoded2.pkl'
#     get_HardAndSimple(encoded_file, class_name)
#     simple_dir = os.path.join(f"{class_name}_images", "simple")
#     hard_dir = os.path.join(f"{class_name}_images", "hard")
#     try:
#         simple_files = [os.path.join(simple_dir, f) for f in os.listdir(simple_dir) if os.path.isfile(os.path.join(simple_dir, f))]
#         hard_files = [os.path.join(hard_dir, f) for f in os.listdir(hard_dir) if os.path.isfile(os.path.join(hard_dir, f))]
#         file_list = [simple_files, hard_files]
#         print(file_list)
#         return file_list
#     except Exception as e:
#         return str(e)


# @app.route('/delete_image', methods=["POST"])
# def delete_image():
#     images = request.get_json()
#     for image in images:
#         delete_file(image)

#     return jsonify({
#         'message': 'Data received successfully!',
#     }), 200


# @app.route('/detection_results', methods=["GET"])
# def get_detection_results():
#     file1 = "result_data1.json"
#     file2 = "result_data2.json"
#     return get_result_new(file1, file2)


# @app.route('/text_result/<class_name>', methods=["GET"])
# def get_text_result(class_name):
#     return ChatWithLLM(class_name, model_type='gpt-4o-ca')


# @app.route('/get_single_result', methods=["GET"])
# def get_single_result():
#   describes = request.get_json()
#   for key, value in describes.items():
#     file_path = os.path.join(key + "_images", "describes.txt")
#     with open(file_path, 'w', encoding="utf-8") as file:
#       file.write('\n'.join(str(i) for i in value))
#   return jsonify({
#     'message': 'Data received successfully!',
#   }), 200


# @app.route('/text_submit', methods=["GET"])
# def text_submit():
#     texts = request.get_json()
#     folder_name =  ""


# ### 以下路由为测试路由 ###
# @app.route('/test/<file>', methods=["GET"])
# def get_images_test(file):
#     return file


# def delete_file(file_path):
#     try:
#         os.remove(file_path)
#         print(f"File '{file_path}' has been deleted successfully.")
#     except FileNotFoundError:
#         print(f"File '{file_path}' not found.")
#     except PermissionError:
#         print(f"Permission denied: unable to delete '{file_path}'.")
#     except Exception as e:
#         print(f"An error occurred while deleting the file: {e}")


app.run()
