<template>
    
    <div class="wrapper">
        <div class="content">
            <div class="Head">
                <div class="flex_column_center" style="height: 100%;width: 20%;">
                    <span class="head_title">Manual annotation</span>
                </div>
            </div>

            <div class="Main">
                <div class="item1" style="width: 25%;flex-shrink: 0;">
                    <div class="flex_row_center" style="width: 100%;height:40%;">
                        <div style="width: 320px; height:320px;background-color: ghostwhite">
                            <svg id="svg" style="width: 320px; height:320px;" xmlns="http://www.w3.org/2000/svg">
                            </svg>
                        </div>
                    </div>

                    <div class="flex_row_bewteen" style="width: 100%;height: 6%;">
                        <span class="view_title">Image Shown</span>
                        <el-switch
                        v-model="switch_value"
                        @change="switch_change"
                        active-text="get similar image">
                        </el-switch>
                    </div>

                    <div style="width: 100%;height:43%;">
                        <el-tabs v-model="tabsName" type="border-card" @tab-click="handleClick" stretch='true'>
                            <el-tab-pane label="selected images" name="first">
                                <ul class="container_ul" style="width: 100%;height: 300px;">
                                    <li v-for="(image, index) in chosen_imageData" :key="index">
                                        <img :src="image" @click="get_similar_images(index)" :class="{pointer:switch_value}"/>
                                    </li>
                                </ul>
                            </el-tab-pane>                                                                     
                            <el-tab-pane label="similar images" name="second" :disabled="!switch_value">
                                <ul class="container_ul" style="width: 100%;height: 300px;">
                                    <li v-for="(image, index) in similar_imageData" :key="index">
                                        <img :src="image"/>
                                    </li>
                                </ul>
                            </el-tab-pane>
                        </el-tabs>
                    </div>

                    <div class="input_div" style="width: 100%;height: 8%;">
                        <div class="flex_column_between" style="width: 50%;height: 80%;margin-left: 30px;">
                            <span class="describe_label" style="margin-left: 3px;">Manually Label</span>
                            <el-input v-model="className" placeholder="please input label"></el-input>
                        </div>
                        <div class="flex_column_between" style="width: 30%;height: 80%;justify-content: flex-end;margin-right: 30px;">
                            <el-button type="info" style="height: 30px;padding: 0;font-size: medium;"
                            @click="get_similars(),get_text_result(),get_detection_results(),handleSimpleSlider()">
                            Annotate</el-button>
                        </div>
                    </div>
                </div>

                <div class="item2" style="flex-grow: 1;">
                    <div class="flex_between" style="height: 200px;width: 100%;">
                        <div style="height: 100%;width: 76%;border: 2px whitesmoke solid;">
                            <div class="flex_column_center" style="width: 100%;height: 100%;">
                                <ul class="container_ul">
                                    <li v-for="(image, index) in similar_imageData" :key="index"><img :src="image"/></li>
                                </ul>
                            </div>
                        </div>
                        <div style="height: 100%;width: 250px;border: 2px whitesmoke solid;margin-right: 5px;">
                            <div class="flex_column_center" style="width: 100%;height: 50%;">
                                <el-input v-model="className" placeholder="人工标注：请输入类别"></el-input>
                            </div>
                            <div class="flex_column_center" style="width: 100%;height: 50%;">
                                <el-button type="primary" plain @click="get_similars(),get_text_result(),get_detection_results(),handleSimpleSlider()">确认标注</el-button>
                            </div> <!-- ,get_text_result() -->
                        </div>
                    </div>
                    <div class="flex_between" style="flex-direction: column;height: 580px;width: 100%;">
                        <el-collapse accordion>
                            <el-collapse-item title="Simple" name="1">
                                <el-divider></el-divider>
                                <div class="flex_column_center" style="width: 100%;height: 100%;">
                                    <div class="flex_between" style="padding: 10px;">
                                        <div style="margin-left:50px;width: 100%;">
                                            <el-slider  v-model="simple_similar_value"
                                                show-stops
                                                :step="0.005"
                                                :min="0.28"
                                                :max="0.34"
                                                @change="handleSimpleSlider"></el-slider>
                                        </div>
                                        <div class="flex_column_center">
                                            <label style="font-size: medium;">selected number：{{this.simple_selected_num}}</label>
                                        </div>
                                        <div class="flex_column_center" style="width: 100px;height: 40px;">
                                            <el-button type="primary" plain style="margin: 10px;" @click="Delete()">Delete</el-button>
                                        </div>
                                    </div>
                                    <ul class="container_ul" style="height: 360px;">
                                        <li v-for="(image_data, image_name) in shown_simple_imageInfo" :key="image_name" @click="choose_image_simple(image_name)"
                                                    :class="{isSelected:image_data[1]}">
                                            <img :src="image_data[0]"/>
                                        </li>
                                    </ul>
                                </div>
                            </el-collapse-item>
                            <el-collapse-item title="Hard" name="2">
                                <el-divider></el-divider>
                                <div class="flex_column_center" style="width: 100%;height: 100%;">
                                    <div class="flex_between" style="padding: 10px;">
                                        <div style="margin-left:50px;width: 100%;">
                                            <el-slider  v-model="hard_similar_value"
                                                range
                                                show-stops
                                                :step="0.005"
                                                :min="0.26"
                                                :max="0.31"
                                                @change="handleHardSlider"></el-slider>
                                        </div>
                                        <div class="flex_column_center">
                                            <label style="font-size: medium;">selected number：{{this.hard_selected_num}}</label>
                                        </div>
                                        <div class="flex_column_center" style="width: 100px;height: 40px;">
                                            <el-button type="primary" plain style="margin: 10px;" @click="Submit()">Submit</el-button>
                                        </div>
                                    </div>
                                    <ul class="container_ul" style="height: 360px;">
                                        <li v-for="(image_data, image_name) in shown_hard_imageInfo" :key="image_name" @click="choose_image_hard(image_name)"
                                                    :class="{isSelected:image_data[1]}">
                                            <img :src="image_data[0]"/>
                                        </li>
                                    </ul>
                                </div>
                            </el-collapse-item>
                        </el-collapse>
                    </div>
                </div>

                <div class="item3" style="width: 25%;flex-shrink: 0;">
                    <div class="flex_column_between" style="width: 100%;height: 48%;">
                        <div style="width: 100%;height: 5%;display: flex;">
                            <p class="text_distribe" style="padding: 3px;">对象描述</p>
                        </div>
                        <div style="overflow-y: auto;overflow-x: hidden; width: 100%;height: 70%;background-color: ghostwhite;">
                            <el-checkbox-group v-model="selectedOptions" @change="handleCheckedCitiesChange">
                                <el-checkbox v-for="option in options" :label="option" :key="option">{{option}}</el-checkbox>
                            </el-checkbox-group>
                        </div>
                        <div style="display: flex;flex-direction: column;justify-content: flex-start; width: 100%;height: 25%;">
                            <div style="width: 100%;height: 40px;">
                                <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange" style="margin-top: 10px;">
                                    全选
                                </el-checkbox>
                            </div>
                            <div class="flex_column_center" style="width: 100%;height: 40px;">
                                <el-button type="primary" plain @click="describe_submit()" style="margin: 10px;">确认提交</el-button>
                            </div>
                        </div>
                    </div>
                    <div class="flex_column_center" style="width: 100%;height: 50%;">
                        <div style="width: 100%;height: 5%;display: flex;">
                            <p class="text_distribe" style="padding: 3px;">检测结果</p>
                        </div>
                        <div style="position:relative;width: 100%;height: 80%;background-color: ghostwhite;">
                            <!-- <el-tree :data="results" :props="defaultProps"></el-tree> -->
                            <div v-if="result_overall_shown" class="checkbox-group" style="position: absolute;overflow: auto;width: 100%;height: 100%;">
                                <label v-for="(ap, cls) in results" :key="cls">
                                        <div>
                                            <h3>{{ cls }}</h3>
                                            <h5 style="color: purple;">{{ ap }}</h5>
                                        </div>
                                </label>
                            </div>
                            <div style="position: absolute;overflow: auto;width: 100%; height:100%;">
                                <svg v-show="result_single_shown" id="result_svg" xmlns="http://www.w3.org/2000/svg">
                                </svg>
                            </div>
                        </div>
                        <div class="flex_column_center">
                            <el-button type="primary" plain @click="change_result()" style="margin: 10px;">切换结果</el-button>
                        </div>
                    </div>
                </div>
            </div>

        </div>
  

  

    </div>
  </template>
  

  <script>
    import * as d3 from "d3";
    import lasso from "./d3-lasso";
    import $ from "jquery";
    import {generateDistinctColors, colors_50} from './color.js';
    import { getSimilarValue } from "./common.js";
  
    export default {
      name: 'vue-owod',
      data() {
          return {
                chosen_imageInfo:[],
                chosen_imageData:[],

                similar_imageInfo:[],
                similar_imageData:[],

                similar_simple_imageInfo:{},
                shown_simple_imageInfo:{},
                similar_hard_imageInfo:{},
                shown_hard_imageInfo:{},
                /*  
                    {image_name:[image_data, false], ...}
                */
                delete_simple_imageInfo:[],
                delete_hard_imageInfo:[],

                checkAll: false,
                allOptions:[],
                options: [],
                selectedOptions: [],
                isIndeterminate: true,

                results:{},
                results_overall:{},
                results_single:{},
                result_overall_shown: false,
                result_single_shown: true,

                simple_similar_value:0.3,
                hard_similar_value:[0.26,0.31],

                className:'',
                simple_selected_num:0,
                hard_selected_num:0,
                switch_value:false,
                tabsName:"first",
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
            // const distinctColors = generateDistinctColors(50);
            const color_50 = colors_50();
            var colors = d3.scaleQuantize()
                .domain([0,50])
                .range(color_50);

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
          single_class_shown(){
            const keys = Object.keys(this.results_single);
            const values = Object.values(this.results_single);
            const width = 320;
            const marginTop = 20;
            const marginRight = 10;
            const marginBottom = 0;
            const marginLeft = 100;
            const height = values.length * 20 + marginTop + marginBottom;
            const rectHeight = 15;
            var svg = d3.select("#result_svg")
                .attr("width", width)
                .attr("height", height);
            
            var xScale = d3.scaleLinear()
                .domain([0,100])
                .range([marginLeft ,  width - marginLeft - marginRight]);
            var yScale = d3.scaleBand()
                .domain(values)
                .range([marginTop, height-marginBottom])
                .padding(0.3);
            var yKeyScale = d3.scaleBand()
                .domain(keys)
                .range([marginTop, height-marginBottom])
                .padding(0.3);
            svg.selectAll("rect")
                .data(values)
                .enter()
                .append("rect")
                .attr("x", marginLeft)
                .attr("y", d => yScale(d))
                .attr("width", d => xScale(d))
                .attr("height", rectHeight)
                .attr("fill", "steelblue");
            
            //竖向坐标轴
            svg.append("g")
                .attr("transform", `translate(${marginLeft}, 0)`)
                .call(d3.axisLeft(yKeyScale).tickSizeOuter(0))
                .attr("font-size", 10)

            svg.selectAll(".tick text")
                .style("font-size", "12px");

            svg.append("g")
                .attr("fill", "white")
                .attr("text-anchor", "end")
                .selectAll()
                .data(values)
                .join("text")
                .attr("x", (d) => marginLeft + xScale(d) + 25)
                .attr("y", (d) => yScale(d) + yScale.bandwidth() / 2)
                .attr("dy", "0.35em")
                .attr("font-size", "12px")
                .attr("fill", "black")
                .text(d => d);
          },
          get_similar_images(index){
            if(this.switch_value==false)return;
            this.tabsName = "second";
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
            var mark_class = this.className;
            fetch('http://127.0.0.1:5000/similars/'+ mark_class )
                .then(response => response.json())
                .then(data => {
                    for(let i in data[0]){
                        this.similar_simple_imageInfo[data[0][i]] = [];
                        this.fetch_images(data[0][i],"similar_simple_imageData");
                        this.handleSimpleSlider();
                    }
                    for(let i in data[1]){
                        this.similar_hard_imageInfo[data[1][i]] = [];
                        this.fetch_images(data[1][i],"similar_hard_imageData");
                        this.handleHardSlider();
                    }
                })
                .catch(error => console.error('Error:', error));
            this.$forceUpdate();
          },
          Delete(){
            fetch('http://127.0.0.1:5000/delete_image', {
                method: 'POST', // 使用POST方法
                headers: {
                    'Content-Type': 'application/json' // 设置请求头，表明发送JSON数据
                },
                body: JSON.stringify(
                    this.delete_simple_imageInfo
                ) // 将数据转换为JSON字符串
                })
                .then(response => response.json()) // 解析JSON格式的响应
                .then(data => console.log(data)) // 处理解析后的数据
                .catch(error => console.error('Error:', error)); // 处理错误
            for(let i in this.delete_simple_imageInfo){
                delete this.similar_simple_imageInfo[this.delete_simple_imageInfo[i]];
                delete this.shown_simple_imageInfo[this.delete_simple_imageInfo[i]];
            }
            this.delete_simple_imageInfo.length = 0;
            this.simple_selected_num = 0;
            this.$forceUpdate();
          },
          Submit(){
            var delete_images = [];
            for(let key in this.shown_hard_imageInfo){
                if(!this.delete_hard_imageInfo.includes(key)){
                    delete_images.push(key);
                }
            }
            fetch('http://127.0.0.1:5000/delete_image', {
                method: 'POST', // 使用POST方法
                headers: {
                    'Content-Type': 'application/json' // 设置请求头，表明发送JSON数据
                },
                body: JSON.stringify(
                    delete_images
                ) // 将数据转换为JSON字符串
                })
                .then(response => response.json()) // 解析JSON格式的响应
                .then(data => console.log(data)) // 处理解析后的数据
                .catch(error => console.error('Error:', error)); // 处理错误
            for(const value of delete_images){
                delete this.similar_hard_imageInfo[value];
                delete this.shown_hard_imageInfo[value];
            }
            for(const value of this.delete_hard_imageInfo){
                this.similar_hard_imageInfo[value][1] = false;
                this.shown_hard_imageInfo[value][1] = false;
            }
            this.delete_hard_imageInfo.length = 0;
            this.hard_selected_num = 0;
            this.$forceUpdate();
          },
          choose_image_simple(image_name){
            if(this.delete_simple_imageInfo.includes(image_name)){
                let indexx = this.delete_simple_imageInfo.indexOf(image_name);
                this.delete_simple_imageInfo.splice(indexx, 1);
                this.similar_simple_imageInfo[image_name][1] = false;
                this.shown_simple_imageInfo[image_name][1] = false;
                this.simple_selected_num--;
            }else{
                this.delete_simple_imageInfo.push(image_name);
                this.similar_simple_imageInfo[image_name][1] = true;
                this.shown_simple_imageInfo[image_name][1] = true;
                this.simple_selected_num++;
            }
            this.$forceUpdate();
          },
          choose_image_hard(image_name){
            if(this.delete_hard_imageInfo.includes(image_name)){
                let indexx = this.delete_hard_imageInfo.indexOf(image_name);
                this.delete_hard_imageInfo.splice(indexx, 1);
                this.similar_hard_imageInfo[image_name][1] = false;
                this.hard_selected_num--;
            }else{
                this.delete_hard_imageInfo.push(image_name);
                this.similar_hard_imageInfo[image_name][1] = true;
                this.hard_selected_num++;
            }
            this.$forceUpdate();
          },
          get_text_result(){
            var mark_class = this.className;
            fetch('http://127.0.0.1:5000/text_result/'+ mark_class )
                .then(response => response.json())
                .then(data => {
                    this.options = data;
                    this.allOptions = data;
                })
                .catch(error => console.error('Error:', error));
          },
          get_detection_results(){
            fetch('http://127.0.0.1:5000/detection_results')
                .then(response => response.json())
                .then(data => {
                    this.results_overall = data[0];
                    this.results_single = data[1];
                    this.results = this.results_overall;
                    this.$forceUpdate();
                    this.single_class_shown();
                })
                .catch(error => console.error('Error:', error));
          },
          describe_submit(){
            var describes = {};
            describes[this.className] = this.selectedOptions;
            fetch('http://127.0.0.1:5000/describe_submit', {
                method: 'POST', // 使用POST方法
                headers: {
                    'Content-Type': 'application/json' // 设置请求头，表明发送JSON数据
                },
                body: JSON.stringify(
                    describes
                ) // 将数据转换为JSON字符串
                })
                .then(response => response.json()) // 解析JSON格式的响应
                .then(data => console.log(data)) // 处理解析后的数据
                .catch(error => console.error('Error:', error)); // 处理错误
          },
          change_result(){
            this.result_single_shown = (this.result_single_shown==true)?false:true; 
            this.result_overall_shown = (this.result_overall_shown==true)?false:true; 
            this.$forceUpdate();
          },
          handleCheckAllChange(val) {
                this.selectedOptions = val ? this.allOptions : [];
                this.isIndeterminate = false;
          },
          handleCheckedCitiesChange(value) {
                let checkedCount = value.length;
                this.checkAll = checkedCount === this.options.length;
                this.isIndeterminate = checkedCount > 0 && checkedCount < this.options.length;
          },
          handleSimpleSlider(){
            let min = this.simple_similar_value;
            let max = 1;
            this.shown_simple_imageInfo = {};
            for(let key in this.similar_simple_imageInfo){
                let value = getSimilarValue(key);
                if(value>=min && value<=max){
                    this.shown_simple_imageInfo[key] = this.similar_simple_imageInfo[key];
                }
            }
            this.$forceUpdate();
          },
          handleHardSlider(){
            let min = this.hard_similar_value[0];
            let max = this.hard_similar_value[1];
            this.shown_hard_imageInfo = {};
            for(let key in this.similar_hard_imageInfo){
                let value = getSimilarValue(key);
                if(value>=min && value<=max){
                    this.shown_hard_imageInfo[key] = this.similar_hard_imageInfo[key];
                }
            }
            this.$forceUpdate();
          },
          switch_change(){
            if(this.switch_value==false){
                this.tabsName = "first";
                this.similar_imageData = this.similar_imageInfo = [];
                this.$forceUpdate();
            }
          }
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