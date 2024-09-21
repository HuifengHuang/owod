import json


def get_result_new(json_file1,json_file2):
    # 读取JSON文件
    with open(json_file1, "r") as json_file1:
        data1 = json.load(json_file1)
    with open(json_file2, "r") as json_file2:
        data2 = json.load(json_file2)
    ap_values1 = data1["AP50"]
    ap_values2 = data2["AP50"]
    Known_ap_values1 = data1["Known AP50"]
    Pre_ap_values2 = data2["Prev class AP50"]
    Cur_ap_values2 = data2["Current class AP50"]
    Known_ap_values2 = data2["Known AP50"]

    # Create a dictionary matching classes with AP values
    class_ap_old = {cls: ap for cls, ap in zip(data1["class_names"], ap_values1)}
    class_ap_new = {cls: ap for cls, ap in zip(data2["class_names"], ap_values2)}
    ####这个是整体结果，这个展示在主结果界面上
    print("Previous-old :", Known_ap_values1)
    print("Previous-new :", Pre_ap_values2)
    print("Current :", Cur_ap_values2)
    print("All :", Known_ap_values2)

    overall_result = {
      "Previous-old": Known_ap_values1,
      "Previous-new": Pre_ap_values2,
      "Current": Cur_ap_values2,
      "All": Known_ap_values2
    }

    #####这个是具体的单个类结果
    for cls, ap in class_ap_old.items():
        print(f"{cls}: {ap}")
    for cls, ap in class_ap_new.items():
        print(f"{cls}: {ap}")

    return [overall_result, class_ap_old, class_ap_new]


if __name__ == '__main__':
    file1 = "result_data1.json"
    file2 = "result_data2.json"
    get_result_new(file1, file2)
