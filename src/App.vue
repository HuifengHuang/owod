<template>
    <div id="app" class="wrapper">
        <div class="content">
            <div class="item1" style="width: 20%;">
                <div class="div_border" style="display: flex;justify-content: space-between; width: 100%;height:300px;">
                    <div class="redu_label">降维数据展示</div>
                    <div class="childContainer1" style="width: 300px; height:300px;">
                        <svg id="svg" style="width: 300px; height:300px;" xmlns="http://www.w3.org/2000/svg">
                        </svg>
                    </div>
                </div>

                <div class="div_border" style="width: 100%;height:450px;">
                    <div class="flex_column_center" style="width: 100%;height: 100%;">
                        <ul class="container_ul">
                            <li v-for="(image, index) in chosen_imageData" :key="index">
                                <img :src="image" @click="get_similar_images(index) " style="cursor:pointer;"/>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="item2" style="width: 60%;">
                <div class="div_border flex_between" style="height: 100px;width: 100%;">
                    <div style="height: 100%;width: 80%;border: 2px whitesmoke solid;">
                        <div class="flex_column_center" style="width: 100%;height: 100%;">
                            <ul class="container_ul" style="">
                                <li v-for="(image, index) in similar_imageData" :key="index"><img :src="image"/></li>
                            </ul>
                        </div>
                    </div>
                    <div style="height: 100%;width: 200px;border: 2px whitesmoke solid;">
                        <div class="flex_column_center" style="flex-direction:row;align-items:center;width: 100%;height: 50%;">
                            <div>人工标注类别：</div>
                            <input id="mark_class" type="text" value="elephant" style="width: 80px;height: 20px;">
                        </div>
                        <div class="flex_column_center" style="width: 100%;height: 50%;">
                            <button @click="get_similars">确认标注</button>
                        </div>
                    </div>
                </div>
                <div class="div_border flex_between" style="height: 680px;width: 100%;">
                    <div style="height: 100%;width: 50%;border: 1px black solid;">
                        <div class="flex_column_center" style="width: 100%;height: 100%;">
                            <div class="flex_between" style="padding: 10px;">
                                <h2 style="text-align: center;">Simple</h2>
                                <button @click="Delete" style="margin-left: 100px;">Delete</button>
                            </div>
                            <ul class="container_ul">
                                <li v-for="(image_data, image_name, index) in similar_simple_imageInfo" :key="image_name" v-if="index>0" @click="choose_image_simple(image_name)"
                                             :class="{isSelected:image_data[1]}">
                                    <img :src="image_data[0]"/>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div style="height: 100%;width: 50%;border: 1px black solid;">
                        <div class="flex_column_center" style="width: 100%;height: 100%;">
                            <div class="flex_between" style="padding: 10px;">
                                <h2 style="text-align: center;">Hard</h2>
                                <button @click="Submit" style="margin-left: 100px;">Submit</button>
                            </div>
                            <ul class="container_ul">
                                <li v-for="(image_data, image_name, index) in similar_hard_imageInfo" :key="image_name" v-if="index>0" @click="choose_image_hard(image_name)"
                                             :class="{isSelected:image_data[1]}">
                                    <img :src="image_data[0]"/>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div></div>
                </div>
            </div>

            <div class="item3" style="width: 20%;">
                <div>

                </div>
                <div>
                    
                </div>
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
                chosen_imageInfo:[],
                chosen_imageData:[],
                similar_imageInfo:[],
                similar_imageData:[],
                similar_simple_imageInfo:{},
                similar_hard_imageInfo:{},
                /*  
                    {image_name:[image_data, false], ...}
                */


                delete_simple_imageInfo:[],
                delete_hard_imageInfo:[],
          }
      },
      mounted:function(){
        this.redu_show();
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

        redu_show(){
            fetch('http://127.0.0.1:5000/data')
                .then(response => response.json())
                .then(data => {
                    this.reduce_distribution(data);
                })
                .catch(error => console.error('Error:', error));
        },

        fetch_images(image_name, save){
            var that = this;
            fetch('http://127.0.0.1:5000/images/' + image_name)
            .then(response => response.arrayBuffer())
            .then(data =>{
                var image_data = "data:image/jpeg;base64," + that.arrayBufferToBase64(data);
                if(save=="chosen_imageData"){
                    this.chosen_imageData.push(image_data);
                    this.chosen_imageInfo.push(image_name);
                }else if(save=="similar_imageData"){
                    this.similar_imageData.push(image_data);
                }else if(save=="similar_simple_imageData"){
                    this.similar_simple_imageInfo[image_name].push(image_data);
                    this.similar_simple_imageInfo[image_name].push(false);
                }else if(save=="similar_hard_imageData"){
                    this.similar_hard_imageInfo[image_name].push(image_data);
                    this.similar_hard_imageInfo[image_name].push(false);
                }

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
                this.chosen_imageInfo.length = 0;
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
                ls.selectedItems().each((d,i)=>{
                    this.fetch_images(d[0], "chosen_imageData");
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
          get_similar_images(index){
            var image_path = this.chosen_imageInfo[index];
            this.similar_imageInfo.length = 0;
            this.similar_imageData.length = 0;
            fetch('http://127.0.0.1:5000/simi/'+ image_path )
                .then(response => response.json())
                .then(data => {
                    this.similar_imageInfo = data;
                    for(let i in data){
                        console.log(data[i][0]);
                        this.fetch_images(data[i][0], "similar_imageData");
                    }
                })
                .catch(error => console.error('Error:', error));
          },
          get_similars(){
            this.similar_simple_imageInfo = {};
            this.similar_hard_imageInfo = {};
            var mark_class = document.getElementById("mark_class").value;
            fetch('http://127.0.0.1:5000/similars/'+ mark_class )
                .then(response => response.json())
                .then(data => {
                    for(let i in data[0]){
                        this.similar_simple_imageInfo[data[0][i]] = [];
                        this.fetch_images(data[0][i],"similar_simple_imageData");
                    }
                    for(let i in data[1]){
                        this.similar_hard_imageInfo[data[1][i]] = [];
                        this.fetch_images(data[1][i],"similar_hard_imageData");
                    }
                })
                .catch(error => console.error('Error:', error));
          },
          Delete(){
            var a = 0;
          },
          Submit(){
            var a = 0;
          },
          choose_image_simple(image_name){
            console.log("choose_image_simple:" + image_name);
            if(this.delete_simple_imageInfo.includes(image_name)){
                let indexx = this.delete_simple_imageInfo.indexOf(image_name);
                this.delete_simple_imageInfo.splice(indexx, 1);
                this.similar_simple_imageInfo[image_name][1] = false;
            }else{
                this.delete_simple_imageInfo.push(image_name);
                this.similar_simple_imageInfo[image_name][1] = true;
            }
            console.log(this.delete_simple_imageInfo);
            this.$forceUpdate();
          },
          choose_image_hard(image_name){
            console.log("choose_image_hard:" + image_name);
            if(this.delete_hard_imageInfo.includes(image_name)){
                let indexx = this.delete_hard_imageInfo.indexOf(image_name);
                this.delete_hard_imageInfo.splice(indexx, 1);
                this.similar_hard_imageInfo[image_name][1] = false;
            }else{
                this.delete_hard_imageInfo.push(image_name);
                this.similar_hard_imageInfo[image_name][1] = true;
            }
            console.log(this.delete_hard_imageInfo);
            this.$forceUpdate();
          },
        }
    }
  </script>
  
  
  <style>
      @import './style/global.css';
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