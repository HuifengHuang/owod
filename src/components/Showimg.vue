<template>
    <div class="image-gallery">
      <!-- 文件上传输入 -->
      <!-- <input type="file" multiple @change="handleFileUpload" /> -->
        <!-- 按钮区域 -->
        <div class="button-container">
            <div class="button-scroll-wrapper">
                <button
                v-for="(name, index) in names"
                :key="index"
                @click="handleButtonClick(name)"
                >
                {{ name }}
                </button>
            </div>
        </div>
      <!-- 图像展示区域 -->
        <div class="image-grid" ref="imageGrid">
        <div 
          v-for="(imagePath, index) in image_paths" 
          :key="index" 
          class="image-container"
        >
          <img 
            :src="imagePath" 
            alt="Loaded Image" 
            class="image" 
          />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
    //   selectedNodeId: {
    //     type: Object,
    //     required: true,
    //   },
    //   selectedimgId: {
    //     type: Object,
    //     required: true,
    //   },
      name_to_ids: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        // imagesData: [], // 假设这是从某个 JSON 文件加载的图像数据
        // filteredImages: [], // 筛选后的图像
        image_paths:[],
        names:[],
        currentName: null,
        name_to_imgpaths:{}
      };
    },
    
    mounted() {
      // 假设你从 JSON 文件加载图像数据
    //   this.loadImages();
    //   console.log("Component mounted, calling load_imgsbyid...");
    //   this.load_imgsbyid();
    },
    watch: {
    name_to_ids: {
      handler(newVal) {
        console.log("name_to_ids changed:", newVal);
        this.load_imgsbyid(); // 调用方法
      },
      immediate: true, // 立即执行一次
      deep: true, // 深度监听
    },
  },
    methods: {
        load_imgsbyid() {
      fetch('http://127.0.0.1:5000/select_imgids', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.name_to_ids),
      })
        .then(response => response.json())
        .then(data => {
          this.names = data.names;
          this.name_to_imgpaths = data.name_to_imgpaths;
        
          // 将本地文件路径转换为 HTTP URL 或 Blob URL
        //   this.image_paths = data.image_paths.map(path => {
        //     // 如果是本地路径，转换为 HTTP URL
        //     if (path.startsWith("D:")) {
        //       const filename = path.split('\\').pop(); // 提取文件名
        //       return `http://127.0.0.1:5000/images/${filename}`; // 生成 Flask URL
        //     }
        //     return path; // 如果已经是 HTTP URL，直接返回
        //   });

          console.log("Converted image paths:", this.image_paths);
        })
        .catch(error => console.error('Error:', error));
    },
    // 点击按钮时，切换当前显示的图像
    handleButtonClick(name){
        console.log("Button clicked!");
        this.currentName = name;
        console.log("Current name:", this.currentName);
        if (this.name_to_imgpaths[this.currentName]) {
            this.image_paths = this.name_to_imgpaths[this.currentName].map(path => {
                if(path.startsWith("D:")){
                    const filename = path.split('\\').pop(); // 提取文件名
                    return `http://127.0.0.1:5000/images/${filename}`; // 生成 Flask UR
                }
            });
        } else {
            this.image_paths = [];
        }

    }
  },
};
  </script>
  
  <style scoped>
  .image-gallery {
    display: flex;
    flex-direction: column; /* 垂直排列 */
    justify-content: center;
    overflow-x: scroll; /* 允许横向滚动 */
    padding: 10px;
  }
  
  .image-grid {
    display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); /* 动态调整列数 */
  gap: 10px; /* 设置图像之间的间隙 */
  width: 100%;
  max-width: 1200px; /* 限制最大宽度 */
  padding: 10px; /* 图像区域内边距 */
  overflow-y: auto; /* 允许纵向滚动 */
  flex-grow: 1; /* 图像区域占据剩余空间 */
  }
  
  .image {
    width: 100%;
    height: auto;
    border-radius: 8px;
    object-fit: cover;
  }

  .button-container {
  width: 100%;
  overflow-x: auto; /* 允许横向滚动 */
  margin-bottom: 20px; /* 按钮区域与图像区域的间距 */
  padding: 10px 0; /* 上下内边距 */
  background-color: #e3e6e9; /* 按钮区域背景色 */
  border-bottom: 1px solid #ddd; /* 按钮区域底部边框 */
  flex-shrink: 0; /* 防止按钮区域被压缩 */
}

.button-scroll-wrapper {
  display: inline-flex; /* 按钮在一行内显示 */
  gap: 10px; /* 按钮之间的间隙 */
  padding: 0 10px; /* 上下内边距 */
}

.button-container button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #96a0ac;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
  white-space: nowrap; /* 按钮文本不换行 */
}

.button-container button:hover {
  background-color: #67bcf5;
}

.button-container button.active {
  background-color: #67bcf5; /* 高亮选中的按钮 */
  font-weight: bold; /* 加粗选中的按钮文本 */
}
  </style>
  