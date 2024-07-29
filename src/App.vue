<template>
    <div id="app" class="wrapper">
        <div class="content">
            <div class="item1">
                <div class="div_border" style="position: relative; width: 100%;height:300px;">
                    <div class="childContainer1" style="width: 300px; height:300px;">
                        <svg id="svg" style="width: 300px; height:300px;border:1px blue solid" xmlns="http://www.w3.org/2000/svg">
                        </svg>
                    </div>
                </div>

                <div class="div_border" style="width: 100%;height:450px;">
                    <div class="childContainer2" style="width: 100%;height: 100%;">
                        <ul class="container_ul" id="image_container">
                            <li v-for="(image, index) in chosen_imageData" :key="index"><img :src="image"/></li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="item2" style="width: 60%;">

            </div>

            <div class="item3" style="width: 20%;">
                
            </div>
        </div>
  

  

    </div>
  </template>
  
  <script>
    import * as d3 from "d3"
    import lasso from "./d3-lasso"
    import $ from "jquery";
  
    export default {
      name: 'vue-owod',
      data() {
          return {
                reduce_distri_data:[],
                chosen_imageData:[],
          }
      },
      mounted:function(){
        this.clusters_show();
      },
      methods:{
        arrayBufferToBase64(buffer) {
                //第一步，将ArrayBuffer转为二进制字符串
                var binary = "";
                var bytes = new Uint8Array(buffer);
                var len = bytes.byteLength;
                for (var i = 0; i < len; i++) {
                    binary += String.fromCharCode(bytes[i]);
                }
                //将二进制字符串转为base64字符串
                return window.btoa(binary);
        },

        clusters_show(){
            fetch('http://127.0.0.1:5000/data')
                .then(response => response.json())
                .then(data => {
                    this.reduce_distribution(data);
                })
                .catch(error => console.error('Error:', error));
        },

        fetch_images(image_name){
            var that = this;
            fetch('http://127.0.0.1:5000/images/' + image_name)
            .then(response => response.arrayBuffer())
            .then(data =>{
                var image_data = "data:image/jpeg;base64," + that.arrayBufferToBase64(data);
                this.chosen_imageData.push(image_data);
                // console.log(typeof(image_data));
                this.$forceUpdate()
            });
        },
  
        findMaxMin(dataset,index){
            var max=-9999 , min=9999;
            for(let i in dataset){
                if(dataset[i][index]>max)max = dataset[i][index];
                if(dataset[i][index]<min)min = dataset[i][index];
            }
            return [max,min];
        },
        reduce_distribution(data){
            var colors = d3.scaleQuantize()
                .domain([0,23])
                .range(["#5E4FA2", "#3288BD", "#66C2A5", "#ABDDA4", "#E6F598", 
                "#FFFFBF", "#FEE08B", "#FDAE61", "#F46D43", "#D53E4F", "#9E0142",
                "#9b3b28","#545394","#2cb930","#7a4d59","#7089d6","#ceec21",
                "#132b38","#b84cca","#3574e3","#4aaa49","#041a03","#bf782e"]);
            var svg = d3.select("#svg")
            var dataset = data;
            var [Xmax,Xmin] = this.findMaxMin(dataset,1);
            var [Ymax,Ymin] = this.findMaxMin(dataset,2);
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
                .attr("r",1.5)
                .attr("id",function(d,i){
                    return i;
                })
                .attr("fill",function(d){
                      return colors(d[3]);
                })
                .attr("cx",function(d){
                    return xScale(d[1]);
                })
                .attr("cy",function(d){
                    return yScale(d[2]);
                })
                .style('cursor','pointer');
            this.setLasso();
          },
          setLasso(){
            let circles = d3.selectAll('.circles');
            var lasso_start = () => {
                ls.items() 
                        .classed("not_possible",true)
                        .classed("selected",false);
                this.chosen_imageData.length = 0;
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
                ls.items()
                        .classed("not_possible",false)
                        .classed("possible",false);
                ls.selectedItems()
                        .classed("selected",true);
                ls.selectedItems().each((d)=>{
                    this.fetch_images(d[0]);
            });
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
        }
    }
  </script>
  
  
  <style>
      @import './style/global.css';
          body{
              font-size:0 px;
          }
          *{
              margin:0;
              padding:0;
          }
          h4{
              padding: 5px;
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
          .div_size_10{
              width: 20px;
              height: 20px;
          }

          .selected {
              stroke: red;
          }

          .possible{
              stroke:red;
          }
          .not_possible{
              stroke:black;
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