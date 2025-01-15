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
                    <!-- <div class="flex_row_center" style="width: 100%;height:50%;border: 1px solid #e9e9e9;margin: 5px;">
                        <div style="width: 400px; height:400px;">
                            <svg id="svg_combine" style="width: 400px; height:400px;" xmlns="http://www.w3.org/2000/svg">
                            </svg>
                        </div>
                    </div> -->
                    <div class="flex_row_center" style="width: 100%;height:100%;">
                        <!-- <div class="flex_row_center" style="width: 50%;height:95%;border: 1px solid #e9e9e9;margin: 5px;">
                            <svg id="svg_image" style="width: 350px; height:350px;" xmlns="http://www.w3.org/2000/svg">
                            </svg>
                        </div>
                        <div class="flex_row_center" style="width: 50%;height:95%;border: 1px solid #e9e9e9;margin: 5px;">
                            <svg id="svg_text" style="width: 350px; height:350px;" xmlns="http://www.w3.org/2000/svg">
                            </svg>
                        </div> -->
                        <div>
                            <h1>名词共现网络</h1>
                            <NounGraph :graphData="graphData" />
                        </div>
                    </div>
                </div>

                <div class="item2" style="flex-grow: 1;height: 100%;">
                    <div class="flex_column_start" style="height: 90%;width: 100%;margin-top: 30px;padding-top: 19px;">
                        <div class="flex_column_center" style="width: 100%;height: 100%;margin-bottom: 5px;">
                            <ul class="container_ul" style="height: 700px;">
                                <li v-for="(item, index) in Selected_data" :key="index" class="li_right flex_row_left">
                                    <img :src="item.image"/>
                                    <img :src="item.raw_image"/>
                                    <span style="width: 200px;">{{ item.text }}</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <el-button type="info" style="height: 30px;padding: 0 20px;margin-right: 5px; font-size: medium;"
                            @click="F5">
                            刷新</el-button>
                </div>

                <div class="item3" style="width: 20%;flex-shrink: 0;">
                    <div class="scrollable-container" style="height: 90%; width: 100%; overflow-y: auto; margin-top: 30px; padding-top: 19px;">
                    <div class="matrix-container" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px;">
                        <div v-for="(item, index) in Selected_data" :key="index" class="image-item">
                        <img :src="item.image" alt="Image" class="uniform-image"/>
                        <img :src="item.raw_image" alt="Raw Image" class="uniform-image"/>
                        <!-- <span style="width: 100%; text-align: center;">{{ item.text }}</span> -->
                        </div>
                    </div>
                    </div>
                    <el-button type="info" style="height: 30px; padding: 0 20px; margin-right: 5px; font-size: medium;" @click="F5">
                    刷新
                    </el-button>
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
    import { ref } from 'vue';
    import {generateDistinctColors, colors_50, colors_20} from './color.js';
    import { getSimilarValue , arrayBufferToBase64, findMaxMin, single_class_shown ,density_shown, overall_class_shown} from "./common.js";
    import graphDataJson from "../assets/GranDf_caption_gcg_noun_graph.json"
    import graphtestJson from "../assets/graph_data_with_importance.json"
    export default {
      name: 'vue-owod',
      components: {
        NounGraph, // 注册组件
    },
      data() {
          return {
                Raw_data:[],
                //["图片路径","文本描述","原图名称","x坐标","y坐标"]
                Selected_data:[],
                //["本图片二进制数据","原图二进制数据","文本描述"]
                // graphData: graphDataJson,
                graphData: graphtestJson,
          }
      },
      mounted:function(){
        this.redu_show();

      },
      methods:{
        redu_show(){
            fetch('http://127.0.0.1:5000/data')
                .then(response => response.json())
                .then(data => {
                    this.Raw_data = data;
                    this.reduce_distribution(data);
                    this.image_redu_shown(data);
                    this.text_redu_shown(data);
                })
                .catch(error => console.error('Error:', error));
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