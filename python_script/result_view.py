import json


def get_result(json_file):
    # 读取JSON文件
    with open(json_file, "r") as json_file:
        data = json.load(json_file)
    ap_values = data["AP50"]
    class_names = data["class_names"]

    Pre_ap_values = data["Prev class AP50"]
    Pre_Precisions50 = data["Prev class Precisions50"]
    Pre_Recall50 = data["Prev class Recall50"]
    Cur_ap_values = data["Current class AP50"]
    Cur_Precisions50 = data["Current class Precisions50"]
    Cur_Recall50 = data["Current class Recall50"]
    Known_ap_values = data["Known AP50"]
    Known_Precisions50 = data["Known Precisions50"]
    Known_Recall50 = data["Known Recall50"]
    # Create a dictionary matching classes with AP values
    class_ap = {cls: ap for cls, ap in zip(class_names, ap_values)}

    ####这个是整体结果，这个展示在主结果界面上
    print("Previous classes AP50:", Pre_ap_values)
    print("Previous classes Precisions50:", Pre_Precisions50)
    print("Previous classes Recall50:",Pre_Recall50)
    print("Current classes AP50:",Cur_ap_values)
    print("Current classes Precisions50:",Cur_Precisions50)
    print("Current classes Recall50:",Cur_Recall50)
    print("All KnownClasses AP50:",Known_ap_values)
    print("All KnownClasses Precisions50:",Known_Precisions50)
    print("All KnownClasses Recall50:",Known_Recall50)
    overall_ap = {
        "Previous classes AP50": Pre_ap_values,
        "Previous classes Precisions50": Pre_Precisions50,
        "Previous classes Recall50": Pre_Recall50,
        "Current classes AP50": Cur_ap_values,
        "Current classes Precisions50": Cur_Precisions50,
        "Current classes Recall50": Cur_Recall50,
        "All KnownClasses AP50": Known_ap_values,
        "All KnownClasses Precisions50": Known_Precisions50,
        "All KnownClasses Recall50": Known_Recall50
    }
    #####这个是具体的单个类结果，搞个可以从主结果界面上弹出的试图，展示具体的结果
    for cls, ap in class_ap.items():
        print(f"{cls}: {ap}")

    return [overall_ap, class_ap]


if __name__ == '__main__':
    get_result('result.json')
