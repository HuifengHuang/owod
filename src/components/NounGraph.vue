<template>
  <!-- 图形容器 -->
  <div class="graph-container">
    <!-- SVG 容器用于绘制图形 -->
    <svg ref="svg" class="graph" :width="width" :height="height"></svg>
  </div>
</template>

<script>
import * as d3 from "d3"; // 引入 D3.js

export default {
  name: "NounGraph",
  props: {
    graphData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      width: 2000, // 图形宽度
      height: 1000, // 图形高度
      centerNodeId: null, // 当前居中的节点 ID
    };
  },
  mounted() {
    this.createGraph(); // 组件挂载后创建图形
  },
  methods: {
    createGraph() {
      const { nodes, links } = this.graphData; // 解构接收到的图数据

      // 选择 SVG 元素
      const svg = d3.select(this.$refs.svg);

      // // 为每个节点添加模拟深度的 z 属性
      // nodes.forEach((node, index) => {
      //   node.z = Math.random() * 200 - 100; // 设置随机深度
      // });

      // 配置力导向图的仿真
      const simulation = d3
        .forceSimulation(nodes) // 使用节点数据初始化
        .force(
          "link",
          d3.forceLink(links).id((d) => d.id).distance(150) // 设置边的长度
        )
        .force("charge", d3.forceManyBody().strength(-400)) // 节点之间的斥力
        .force("center", d3.forceCenter(this.width / 2, this.height / 2)) // 初始图形居中
        .force("collide", d3.forceCollide().radius(20)); // 防止节点重叠
        // .alphaDecay(0.02) // 调整速度衰减
        // .friction(0.9); // 增加摩擦力

      // **绘制边**
      const link = svg
        .selectAll("line") // 选择所有 `line` 元素
        .data(links) // 绑定边数据
        .join("line") // 更新模式：创建新的边
        .attr("stroke", "#aaa") // 边的颜色
        .attr("stroke-width", (d) => Math.sqrt(d.value)); // 根据权重调整宽度

      // **绘制节点**
      const node = svg
        .selectAll("circle") // 选择所有 `circle` 元素
        .data(nodes) // 绑定节点数据
        .join("circle") // 更新模式：创建新的节点
        .attr("r", (d) => 5 + d.importance/50 * 2) // 节点的半径
        .attr("fill", "steelblue") // 节点颜色
        .style("opacity", 1) // 所有节点初始完全可见
        .call(
          d3
            .drag() // 添加拖拽行为
            .on("start", (event, d) => this.dragStarted(event, d, simulation)) // 拖拽开始
            .on("drag", this.dragged) // 拖拽中
            .on("end", (event, d) => this.dragEnded(event, d, simulation)) // 拖拽结束
        )
        .attr("transform", (d) => `translate(${d.x},${d.y}) scale(${1 + d.z / 200})`); // 根据 z 深度调整节点大小

      // **绘制标签**
      const labels = svg
        .selectAll("text") // 选择所有 `text` 元素
        .data(nodes) // 绑定节点数据
        .join("text") // 更新模式：创建新的标签
        .attr("dx", 15) // 标签的水平偏移
        .attr("dy", 4) // 标签的垂直偏移
        .text((d) => d.name); // 显示节点名称

      // **更新位置：在仿真中调整节点和边的位置**
      simulation.on("tick", () => {
        // 更新边的位置
        link
          .attr("x1", (d) => d.source.x)
          .attr("y1", (d) => d.source.y)
          .attr("x2", (d) => d.target.x)
          .attr("y2", (d) => d.target.y);

        // 更新节点的位置
        node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

        // 更新标签的位置
        labels.attr("x", (d) => d.x).attr("y", (d) => d.y);
      });
      node.on("click", (event, d) => {
        // 高亮相关节点
        node.style("opacity", (n) =>
          links.some((l) => (l.source.id === d.id || l.target.id === d.id) && n.id === (l.source.id === d.id ? l.target.id : l.source.id))
            ? 1
            : 0.1
        );
        // 高亮相关边
        link.style("opacity", (l) =>
          l.source.id === d.id || l.target.id === d.id ? 1 : 0.1
        );
      }).on("dblclick", () => {
        // 恢复原始样式
        node.style("opacity", (d) => (d.importance > 2 ? 1 : 0.3));
        link.style("opacity", (d) => (d.importance > 2 ? 1 : 0.3));
      });

    },

    // 拖拽行为函数
    dragStarted(event, d, simulation) {
      if (!event.active) simulation.alphaTarget(0.9).restart(); // 增加仿真能量
      d.fx = d.x; // 锁定节点的 x 坐标
      d.fy = d.y; // 锁定节点的 y 坐标
    },
    dragged(event, d) {
      d.fx = event.x; // 更新节点的 x 坐标
      d.fy = event.y; // 更新节点的 y 坐标
    },
    dragEnded(event, d, simulation) {
      if (!event.active) simulation.alphaTarget(0); // 停止仿真
      d.fx = null; // 解锁节点的 x 坐标
      d.fy = null; // 解锁节点的 y 坐标
    },
  },
};
</script>

<style>
.graph-container {
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
}

.graph {
  width: 100%;
  height: 100%;
}
</style>
