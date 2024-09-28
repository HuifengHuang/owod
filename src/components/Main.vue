<template>
    
    <div class="wrapper">
        <div class="content">
            <div class="Head">
            </div>

            <div class="Main">
                <div class="item1" style="width: 40%;flex-shrink: 0;">
                    <div class="flex_row_center" style="width: 100%;height:100%;border: 1px solid #e9e9e9;">
                        <div style="width: 500px; height:500px;">
                            <svg id="svg" style="width: 500px; height:500px;" xmlns="http://www.w3.org/2000/svg">
                            </svg>
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

            </div>

        </div>
  

  

    </div>
  </template>
  

  <script>
    import * as d3 from "d3";
    import lasso from "./d3-lasso";
    import $ from "jquery";
    import { ref } from 'vue';
    import {generateDistinctColors, colors_50, colors_20} from './color.js';
    import { getSimilarValue , arrayBufferToBase64, findMaxMin, single_class_shown ,density_shown, overall_class_shown} from "./common.js";
  
    export default {
      name: 'vue-owod',
      data() {
          return {
                Raw_data:[],
                //["图片路径","文本描述","原图名称","x坐标","y坐标"]
                Selected_data:[],
                //["本图片二进制数据","原图二进制数据","文本描述"]
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
            var svg = d3.select("#svg")
            var dataset = data;
            var [Xmax,Xmin] = findMaxMin(dataset,3);
            var [Ymax,Ymin] = findMaxMin(dataset,4);
            let svg_element = document.getElementById("svg");
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
                .attr("r",2)
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
          setLasso(){
            let circles = d3.selectAll('.circles');
            var lasso_start = () => {
                ls.items() 
                        .classed("not_possible",true)
                        .classed("selected",false);
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
                ls.items()
                        .classed("not_possible",false)
                        .classed("possible",false);
                ls.selectedItems()
                        .classed("selected",true);
                ls.selectedItems().each((d)=>{
                    this.fetch_images(d);
                })
                this.$forceUpdate();
                console.log(this.Selected_data);
            };
            var svgNode = d3.select("#svg");
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
        }
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
              stroke: red;
              stroke-width: 1;
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

      </style>