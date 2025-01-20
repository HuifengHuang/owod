<template>
    
    <div class="wrapper">
        <div class="content">
            <div class="Head">
                <div class="flex_row_start" style="height: 100%;width: 100%;">
                    <span class="head_title">简单降维</span>
                </div>
            </div>

            <div class="Main">
                <div class="item1" style="width: 40%;flex-shrink: 0;">
                    <div class="flex_row_center" style="width: 100%;height:100%;">
                        <div>
                            <h1>名词共现网络</h1>
                            <el-slider v-model="sliderValue" :min="0" :max="100" :step="1" @change="filterNodesByImportance"></el-slider>
                            <NounGraph :graphData="graphData" @node-click="onNodeClick" />
                        </div>
                    </div>
                </div>

                <div class="item2" style="flex-grow: 1;height: 100%;">
                    <Showimg :name_to_ids="name_to_ids"/>
                </div>
                


            </div>

        </div>
  
    </div>
  </template>
  

  <script>
    import * as d3 from "d3";
    import lasso from "./d3-lasso";
    import $ from "jquery";
    import NounGraph from "./NounGraph.vue";
    import Showimg from "./Showimg.vue"
    import { ref } from 'vue';
    import {generateDistinctColors, colors_50, colors_20} from './color.js';
    import { getSimilarValue , arrayBufferToBase64, findMaxMin, single_class_shown ,density_shown, overall_class_shown, filter_glaph} from "./common.js";
    import graphDataJson from "../assets/GranDf_caption_gcg_noun_graph.json"
    import graphtestJson from "../assets/graph_data_with_importance.json"
    import graphfilter from "../assets/filtered_output.json"
    export default {
      name: 'vue-owod',
      components: {
        NounGraph, // 注册组件
        Showimg,
    },
      data() {
          return {
                Raw_data:[],
                //["图片路径","文本描述","原图名称","x坐标","y坐标"]
                // Selected_data:null,
                //["本图片二进制数据","原图二进制数据","文本描述"]
                // graphData: graphDataJson,
                graphData: graphfilter,
                // selectedNodes: null,
                // selectedimgid:null,
                sliderValue: 0,
                range:[0,20],
                filteredNodes:[],
                selected_names:[],
                name_to_ids:{}
          }
      },
      mounted:function(){
        this.redu_show();
      },
      methods:{
        // redu_show(){
        //     fetch('http://127.0.0.1:5000/data')
        //         .then(response => response.json())
        //         .then(data => {
        //             this.Raw_data = data;        
        //             this.reduce_distribution(data);
        //             this.image_redu_shown(data);
        //             this.text_redu_shown(data);
        //         })
        //         .catch(error => console.error('Error:', error));
        // },
         // 根据滑块选择的importance范围筛选节点
        filterNodesByImportance() {
        this.filteredNodes = this.graphData.nodes.filter(node => {
            return node.importance >= this.range[0] && node.importance <= this.range[1];
        });
        
        // 为每个节点增加其连接的节点信息
        this.filteredNodes.forEach(node => {
            node.edges = this.graphData.edges.filter(edge => edge.source === node.id);
        });
        },

        // 处理节点连接图中节点点击事件
        onNodeClick(nodes) {
        this.selectedNodes = nodes; // 更新选中的相关节点信息
        this.select_img();
        },

        select_img(){
            fetch('http://127.0.0.1:5000/select_nodes', {
                method: 'POST', // 使用POST方法
                headers: {
                    'Content-Type': 'application/json' // 设置请求头，表明发送JSON数据
                },
                body: JSON.stringify(
                    this.selectedNodes
                ) // 将数据转换为JSON字符串
                })
                .then(response => response.json()) // 解析JSON格式的响应
                .then(data => {
                    // this.selectedimgid = data.unique_prefixes;  
                    // this.selected_names = data.names;
                    this.name_to_ids = data.name_to_ids;
                }) // 处理解析后的数据
                .catch(error => console.error('Error:', error)); // 处理错误
            },

        fetch_images(dataset){
            var temp = {};
            var path = "image/GranDf/train/" + dataset[2]  + ".jpg";
            fetch('http://127.0.0.1:5000/images/' + dataset[0])
            .then(response => response.arrayBuffer())
            .then(data =>{
                var image_data = "data:image/jpeg;base64," + arrayBufferToBase64(data);
                temp['image'] = image_data;
            });
            fetch('http://127.0.0.1:5000/images/' + path)
            .then(response => response.arrayBuffer())
            .then(data =>{
                var image_data = "data:image/jpeg;base64," + arrayBufferToBase64(data);
                temp['raw_image'] = image_data;
            });
            temp['text'] = dataset[1];
            this.Selected_data.push(temp);
        },
  
        reduce_distribution(data){
            var svg = d3.select("#svg_combine")
            var dataset = data;
            var [Xmax,Xmin] = findMaxMin(dataset,3);
            var [Ymax,Ymin] = findMaxMin(dataset,4);
            let svg_element = document.getElementById("svg_combine");
            let JQsvg = $(svg_element);
            svg_element = JQsvg[0];
            let svg_height = svg_element.style.height;
            let svg_width = svg_element.style.width;
            svg_height = svg_height.replace(/[^0-9]/ig, "");    //去掉px
            svg_width = svg_width.replace(/[^0-9]/ig, "");
            // console.log(svg_height + " " + svg_width);
            var xScale = d3.scaleLinear()
                .domain([Xmin-1, Xmax+1])
                .range([0, svg_width]);
            var yScale = d3.scaleLinear()
                .domain([Ymax+1, Ymin-1])
                .range([0, svg_height]);
            svg.selectAll("circle")
                .data(dataset)
                .enter()
                .append("circle")
                .classed("circles",true)
                .attr("r",1.5)
                .attr("id",function(d,i){
                    return i;
                })
                .attr("cx",function(d){
                    return xScale(d[3]);
                })
                .attr("cy",function(d){
                    return yScale(d[4]);
                })
                // .attr("stroke", "white")
                // .attr("stroke-width", 0.05)
                .style('cursor','pointer');
            this.setLasso();
          },
          image_redu_shown(data){
            var svg = d3.select("#svg_image")
            var dataset = data;
            var [Xmax,Xmin] = findMaxMin(dataset,5);
            var [Ymax,Ymin] = findMaxMin(dataset,6);
            let svg_element = document.getElementById("svg_image");
            let JQsvg = $(svg_element);
            svg_element = JQsvg[0];
            let svg_height = svg_element.style.height;
            let svg_width = svg_element.style.width;
            svg_height = svg_height.replace(/[^0-9]/ig, "");    //去掉px
            svg_width = svg_width.replace(/[^0-9]/ig, "");
            // console.log(svg_height + " " + svg_width);
            var xScale = d3.scaleLinear()
                .domain([Xmin-1, Xmax+1])
                .range([0, svg_width]);
            var yScale = d3.scaleLinear()
                .domain([Ymax+1, Ymin-1])
                .range([0, svg_height]);
            svg.selectAll("circle")
                .data(dataset)
                .enter()
                .append("circle")
                .classed("circles",true)
                .attr("r",1.5)
                .attr("id",function(d,i){
                    return "image" + d[9];
                })
                .attr("cx",function(d){
                    return xScale(d[5]);
                })
                .attr("cy",function(d){
                    return yScale(d[6]);
                })
                // .attr("stroke", "white")
                // .attr("stroke-width", 0.05)
                .style('cursor','pointer');
          },
          text_redu_shown(data){
            var svg = d3.select("#svg_text")
            var dataset = data;
            var [Xmax,Xmin] = findMaxMin(dataset,7);
            var [Ymax,Ymin] = findMaxMin(dataset,8);
            let svg_element = document.getElementById("svg_text");
            let JQsvg = $(svg_element);
            svg_element = JQsvg[0];
            let svg_height = svg_element.style.height;
            let svg_width = svg_element.style.width;
            svg_height = svg_height.replace(/[^0-9]/ig, "");    //去掉px
            svg_width = svg_width.replace(/[^0-9]/ig, "");
            // console.log(svg_height + " " + svg_width);
            var xScale = d3.scaleLinear()
                .domain([Xmin-1, Xmax+1])
                .range([0, svg_width]);
            var yScale = d3.scaleLinear()
                .domain([Ymax+1, Ymin-1])
                .range([0, svg_height]);
            svg.selectAll("circle")
                .data(dataset)
                .enter()
                .append("circle")
                .classed("circles",true)
                .attr("r",1.5)
                .attr("id",function(d,i){
                    return "text" + d[9];
                })
                .attr("cx",function(d){
                    return xScale(d[7]);
                })
                .attr("cy",function(d){
                    return yScale(d[8]);
                })
                // .attr("stroke", "white")
                // .attr("stroke-width", 0.05)
                .style('cursor','pointer');
          },
          setLasso(){
            let circles = d3.selectAll('.circles');
            var svg_image = d3.select("#svg_image");
            var svg_text = d3.select("#svg_text");
            var lasso_start = () => {
                ls.items() 
                        .classed("not_possible",true)
                        .classed("selected",false);
                svg_image.selectAll('.circles').classed("selected",false);
                svg_text.selectAll('.circles').classed("selected",false);
            };
  
            var lasso_draw = () => {
                ls.possibleItems()
                        .classed("not_possible",false)
                        .classed("possible",true);
                ls.notPossibleItems()
                        .classed("not_possible",true)
                        .classed("possible",false);
            };
  
            var lasso_end = () => {
                this.Selected_data = [];
                svg_image.selectAll('.circles').classed("unselected",true);
                svg_text.selectAll('.circles').classed("unselected",true);
                ls.items()
                        .classed("not_possible",false)
                        .classed("possible",false);
                ls.selectedItems()
                        .classed("selected",true);
                ls.selectedItems().each((d,i)=>{
                    this.fetch_images(d);
                    svg_image.select("#image"+d[9]).classed("selected",true).attr("r",3);
                    svg_text.select("#text"+d[9]).classed("selected",true).attr("r",3);
                })
                this.$forceUpdate();
            };
            var svgNode = d3.select("#svg_combine");
            var ls = lasso()
                .closePathDistance(305) 
                .closePathSelect(true) 
                .targetArea(svgNode)
                .items(circles) 
                .on("start",lasso_start) 
                .on("draw",lasso_draw) 
                .on("end",lasso_end); 
  
            svgNode.call(ls);
          },
          F5(){
            this.$forceUpdate();
          },
          async loadGraphData() {
            try {
                // 动态加载 JSON 数据
                const response = await fetch("/graphData.json");
                if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                this.graphData = data; // 将数据赋值到 graphData
            } catch (error) {
                console.error("加载数据失败:", error);
            }
            },
        },
    }
  </script>
  
  
  <style>
    @import '../style/global.css';
          body{
              font-size:0 px; 
          }
          .axis path,
          .axis line{
              fill: none;
              stroke: black;
              shape-rendering: crispEdges;
          }
          .axis text {
              font-family: sans-serif;
              font-size: 11px;
          }

          .selected {
                fill:red;
              stroke: red;
              stroke-width: 3;
              stroke-opacity: 1;
              opacity: 1;
          }

          .possible{
              stroke:black;
              stroke-width: 1;
          }
          .not_possible{
              stroke:white;
          }

          .lasso path{
                fill-opacity: 0.6;
                stroke: rgb(64, 169, 255);
                stroke-width: 2px;
            }

            .lasso .drawn{
                fill-opacity: 0.05;
            }

            .lasso .loop_close{
                fill: none;
                stroke-dasharray: 4, 4;
            }

            .lasso .origin{
                fill: #3399ff;
                fill-opacity: 0.5;
            }

            .uniform-image {
            width: 150px; /* 统一宽度 */
            height: 150px; /* 统一高度 */
            object-fit: cover; /* 保持图像比例并裁剪 */
            }

            .unselected{
                opacity: 0.3;
            }
      </style>