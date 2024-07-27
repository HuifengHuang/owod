<template>
    <div id="app">
      <div class="div_border" style="width: 1500px;height:400px;margin: 20px;">
        <button @click="clusters_show();reduce_distribution();">clusters_show</button>
          <div id="View1" style="overflow-y: auto ;width: 100%;height: 300px;margin-top: 50px;">
              <div class="scroll_div" v-for="cluster in clusters" :key="cluster.id">
                  <div class="info_div">
                      <div>cluster_group:</div><div>{{ cluster.id }}</div>
                      <br/>
                      <div>count:</div><div>{{ cluster.count }}</div>
                      <br/>
                      <div>color:</div><div class="div_size_10" :style="{background: cluster.color }"></div>
                  </div>
                  <ul class="vertical_ul">
                      <li v-for="(image, index) in cluster.imageData" :key="index"><img :src="image"/></li>
                  </ul>
              </div>
          </div>
      </div>
      <br/>
  
      <div class="div_border" style="position: relative; width: 400px;height:400px;margin: 20px;">
          <div class="childContainer" style="width: 300px; height:300px;">
              <svg id="svg" style="width: 300px; height:300px;border:1px blue solid" xmlns="http://www.w3.org/2000/svg">
              </svg>
          </div>
      </div>
  
      <div class="div_border" style="position: relative;width: 1058px;height:400px;margin: 20px;">
          <div class="childContainer" style="width: 80%;height: 140px;">
              <ul class="container_ul" id="image_container">
                <li v-for="(image, index) in chosen_imageData" :key="index"><img :src="image"/></li>
              </ul>
          </div>
      </div>
    </div>
  </template>
  
  <script>
    import * as d3 from "d3"
    import lasso from "./d3-lasso"
  
    export default {
      name: 'vue-owod',
      data() {
          return {
                images:"unknown_images_try1/images/000000000025_14166.jpg",
                reduce_distri_data:[],
                clusters:{},    
                /* cluster.id:{
                                cluster.id:0, 
                                cluster.count:100, 
                                cluster.images:["unknown_images_try1/images/000000000025_14166.jpg",...]
                                }
                */
                cluster_imageData:{},
                /*
                    cluster.id:{
                                cluster.id:0,
                                cluster.imageData:[]
                                }
                */
                chosen_imageData:[],
          }
      },
      methods:{
          add_clusters(){
            this.clusters[1]['count'] += 1;
          },
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
              console.log(this.images);
              var colors = d3.scaleQuantize()
                  .domain([0,23])
                  .range(["#5E4FA2", "#3288BD", "#66C2A5", "#ABDDA4", "#E6F598", 
                  "#FFFFBF", "#FEE08B", "#FDAE61", "#F46D43", "#D53E4F", "#9E0142",
                  "#9b3b28","#545394","#2cb930","#7a4d59","#7089d6","#ceec21",
                  "#132b38","#b84cca","#3574e3","#4aaa49","#041a03","#bf782e"]);
              fetch('http://127.0.0.1:5000/cluster_data')
                  .then(response => response.json())
                  .then(data => {
                      // console.log(data); // 这里的data就是后端传送过来的JSON对象
                      // this.main(data);
                      this.reduce_distribution(data);
                      this.clusters = data;
                      for(let key in data){
                          this.clusters[key]['id'] = key;
                          this.clusters[key]['color'] = colors(key);
                          this.clusters[key]['imageData'] = new Array();
                          for(let i=0;i< 100 &&i<data[key]['images'].length;i++){ // #todo 这里如果设置加载图片数量过大会导致fetch失败
                              this.fetch_images_with_key(key, data[key]['images'][i]);
                          }
                          // for(let i=0;i<10;i++){
                          //     console.log(this.clusters[key]['imageData'][i]);
                          // }
                      }
                      // console.log(this.clusters[2]['imageData']);
                  })
                  .catch(error => console.error('Error:', error));
                fetch('http://127.0.0.1:5000/data')
                  .then(response => response.json())
                  .then(data => {
                     this.reduce_distribution(data);
                     this.reduce_distri_data = data;
                  })
                  .catch(error => console.error('Error:', error));
              },
  
          fetch_images_with_key(key, image_name){
              var that = this;
              fetch('http://127.0.0.1:5000/images/' + image_name)
              .then(response => response.arrayBuffer())
              .then(data =>{
                  var image_data = "data:image/jpeg;base64," + that.arrayBufferToBase64(data);
                  this.clusters[key]['imageData'].push(image_data);
                  // console.log(typeof(image_data));
                  this.$forceUpdate()
              });
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
            var xScale = d3.scaleLinear()
                .domain([Xmin-1, Xmax+1])
                .range([0, 300]);
            var yScale = d3.scaleLinear()
                .domain([Ymax+1, Ymin-1])
                .range([0, 300]);
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
          body{
              font-size:0 px;
          }
          *{
              margin:0;
              padding:0;
          }
          div{
              float: left;
          }
          .div_border{
              border: 2px solid black;
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
          .scroll_div{
              display: flex;
              width: 100%;
              height: 140px;
              margin-bottom: 10px;
          }
          .vertical_ul{
              margin-right: 30px;
              list-style-type: none;
              display: flex;
              border: 1px solid red;
              height: 100%;
              flex-grow: 1;
              user-select: none;
              overflow-x: scroll; /* 添加横向滚动 */
              overflow-y: hidden;
              white-space: nowrap; /* 防止标签换行 */
          }
          .info_div{
              margin-left: 50px;
              border: 1px solid black;
              width: 140px;
              height: 140px;
              margin-right: 50px;
          }
          .container_ul {
              list-style-type: none;
              display: flex;
              border: 1px solid red;
              height: 100%;
              width: 100%;
              user-select: none;
              overflow-x: scroll; /* 添加横向滚动 */
              white-space: nowrap; /* 防止标签换行 */
          }
          .div_size_10{
              width: 20px;
              height: 20px;
          }
          li {
              border: 1px solid black;
              width: 100px;
              height: 100px;
              margin: 10px;
          }
          img {
              width: 100px;
              height: 100px;
          }
          .selected {
              stroke: red;
          }
          .childContainer {
              position: absolute;
              top: 0;
              left: 0;
              bottom: 0;
              right: 0;
              margin: auto;
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