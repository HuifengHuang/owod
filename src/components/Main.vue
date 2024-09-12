<template>
    
    <div class="wrapper">
        <div class="content">
            <div class="Head">
                <div class="flex_column_center" style="height: 100%;width: 20%;">
                    <span class="head_title">Manual annotation</span>
                </div>
            </div>

            <div class="Main">
                <div class="item1" style="width: 19%;flex-shrink: 0;">
                    <div class="flex_row_bewteen" style="width: 100%;height: 5%;">
                        <span class="view_title">Label Annotation</span>
                    </div>
                    <el-divider></el-divider>
                    <div class="flex_row_center" style="width: 100%;height:38%;border: 1px solid #e9e9e9;">
                        <div style="width: 320px; height:320px;">
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

                    <div style="width: 100%;height:37%;">
                        <el-tabs v-model="tabsName" type="border-card" :stretch="true">
                            <el-tab-pane label="selected images" name="first">
                                <ul class="container_ul" style="width: 100%;height: 250px;">
                                    <li v-for="(image, index) in chosen_imageData" :key="index">
                                        <img :src="image" @click="get_similar_images(index)" :class="{pointer:switch_value}"/>
                                    </li>
                                </ul>
                            </el-tab-pane>                                                                     
                            <el-tab-pane label="similar images" name="second" :disabled="!switch_value">
                                <ul class="container_ul" style="width: 100%;height: 250px;">
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

                <div class="item2" style="flex-grow: 1;height: 100%;">
                    <div class="flex_row_bewteen" style="width: 100%;height: 5%;">
                        <span class="view_title">Manually Rejection And Screening</span>
                    </div>
                    <el-divider></el-divider>
                    <div class="flex_row_bewteen" style="width: 100%;height: 5%;">
                        <span class="describe_label" style="margin-left: 30px;">Similarity Density</span>
                        <div class="flex_row_bewteen" style="height: 100%;width: 30%;">
                            <el-radio-group class="difficulty_radio_group" v-model="difficulty_radio" @input="difficulty_change">
                                <el-radio label="Simple" border class="difficulty_radio">Simple</el-radio>
                                <el-radio label="Hard" border class="difficulty_radio">Hard</el-radio>
                            </el-radio-group>
                        </div>
                    </div>

                    <div style="position: relative; width: 100%;height: 30%;">
                        <div style="width: 100%;height: 80%;margin: 15px auto;">
                            <div id="svg_container" style="width: 85%;height: 100%;margin: 0 auto;">
                                <svg v-show="this.difficulty_radio=='Simple'" id="svg_simple" class="full_fill" xmlns="http://www.w3.org/2000/svg">
                                </svg>
                                <svg v-show="this.difficulty_radio=='Hard'" id="svg_hard" class="full_fill" xmlns="http://www.w3.org/2000/svg">
                                </svg>
                            </div>
                        </div>
                        <div style="width: 85%;margin: -30px auto;">
                            <el-slider  v-model="similarity_value"
                                range
                                :step="0.005"
                                :min="0"
                                :max="1"
                                :show-tooltip="false"
                                @change="handleSliderChange"
                                @input="handleSliderInput"
                                style="margin: 0 10px;"></el-slider>
                        </div>
                        <div style="width: 85%;margin: 30px auto;">
                            <span class="range_label">Current Value:{{ this.real_value_left }} - {{ this.real_value_right }}</span>
                        </div>
                    </div>

                    <div class="flex_column_start" style="height: 60%;width: 100%;margin-top: 50px;">
                        <el-divider></el-divider>
                        <div style="width: 100%;margin: 10px 30px;">
                            <span class="describe_label">{{ this.difficulty_radio }} Group</span>
                        </div>
                        <div class="flex_column_center" style="width: 100%;height: 70%;margin-bottom: 5px;">
                            <ul class="container_ul" style="height: 360px;">
                                <li v-for="(image_data, image_name) in shown_imageInfo" :key="image_name" @click="choose_image(image_name)"
                                            :class="{isSelected:image_data[1]}">
                                    <img :src="image_data[0]"/>
                                </li>
                            </ul>
                        </div>
                        <div style="width: 100%;margin: 3px 5px;">
                            <span class="range_label">Current Selected: {{ this.current_selected_num }}</span>
                        </div>
                        <el-divider></el-divider>
                        
                    </div>
                </div>

                <div class="item3" style="width: 25%;flex-shrink: 0;">
                    <div class="flex_column_start" style="width: 100%;height: 50%;">
                        <div class="flex_row_bewteen" style="width: 100%;height: 10%;">
                            <span class="view_title">Object Description</span>
                        </div>
                        <el-divider></el-divider>
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
                    <div style="width: 106%;height: 3px;background-color: #e9e9e9;margin: 0 0 0 -20px;"></div>
                    <div class="flex_column_center" style="width: 100%;height: 50%;">
                        <div class="flex_row_bewteen" style="width: 100%;height: 10%;">
                            <span class="view_title">Detection Result</span>
                        </div>
                        <el-divider></el-divider>
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
    import { ref } from 'vue';
    import {generateDistinctColors, colors_50} from './color.js';
    import { getSimilarValue , arrayBufferToBase64, findMaxMin, single_class_shown ,density_shown} from "./common.js";
  
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
                similarities_simple:[],
                similarities_hard:[],
                /*  
                    {image_name:[image_data, false], ...}
                */
                delete_simple_imageInfo:[],
                delete_hard_imageInfo:[],

                shown_imageInfo:{},
                delete_imageInfo:[],

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

                similarity_value:[0,1],
                real_value_left:0,
                real_value_right:1,

                simple_similar_value:[0,1],

                className:'',
                current_selected_num:0,
                switch_value:false,
                tabsName:"first",
                difficulty_radio:'Simple',
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
                    this.reduce_distribution(data);
                })
                .catch(error => console.error('Error:', error));
        },

        fetch_images(image_name, save){
            fetch('http://127.0.0.1:5000/images/' + image_name)
            .then(response => response.arrayBuffer())
            .then(data =>{
                var image_data = "data:image/jpeg;base64," + arrayBufferToBase64(data);
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
  
        reduce_distribution(data){
            // const distinctColors = generateDistinctColors(50);
            const color_50 = colors_50();
            var colors = d3.scaleQuantize()
                .domain([0,50])
                .range(color_50);

            var svg = d3.select("#svg")
            var dataset = data;
            var [Xmax,Xmin] = findMaxMin(dataset,1);
            var [Ymax,Ymin] = findMaxMin(dataset,2);
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
                    }
                    for(let i in data[1]){
                        this.similar_hard_imageInfo[data[1][i]] = [];
                        this.fetch_images(data[1][i],"similar_hard_imageData");
                    }
                    this.set_similarities();
                    density_shown("svg_simple", this.similarities_simple);
                    density_shown("svg_hard", this.similarities_hard);
                    this.difficulty_change();
                    this.handleSliderInput();
                    this.handleSliderChange();
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
          choose_image(image_name){
            if(this.delete_imageInfo.includes(image_name)){
                let indexx = this.delete_imageInfo.indexOf(image_name);
                this.delete_imageInfo.splice(indexx, 1);
                this.shown_imageInfo[image_name][1] = false;
                this.current_selected_num--;
            }else{
                this.delete_imageInfo.push(image_name);
                this.shown_imageInfo[image_name][1] = true;
                this.current_selected_num++;
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
                    single_class_shown(this.results_single);
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
          handleSliderChange(){
            this.shown_imageInfo = {};
            var similar_images = {};
            if(this.difficulty_radio == "Simple")similar_images = this.similar_simple_imageInfo;
            else similar_images = this.similar_hard_imageInfo;
            for(let key in similar_images){
                let value = getSimilarValue(key);
                if(value >= this.real_value_left && value <= this.real_value_right){
                    this.shown_imageInfo[key] = similar_images[key];
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
          },
          set_similarities(){
            this.similarities_simple = [];
            this.similarities_hard = [];
            var image_names = Object.keys(this.similar_simple_imageInfo);
            for(let i in image_names){
                this.similarities_simple.push(getSimilarValue(image_names[i]));
            }
            image_names = Object.keys(this.similar_hard_imageInfo);
            for(let i in image_names){
                this.similarities_hard.push(getSimilarValue(image_names[i]));
            }
          },
          handleSliderInput(){
            var similarities = [];
            if(this.difficulty_radio == "Simple")similarities = this.similarities_simple;
            else similarities = this.similarities_hard;
            var v_min = Math.min(...similarities);
            var v_max = Math.max(...similarities);
            console.log(v_min);
            this.real_value_left = (v_min + this.similarity_value[0] * (v_max - v_min)).toFixed(4);
            this.real_value_right = (v_min + this.similarity_value[1] * (v_max - v_min)).toFixed(4);
            this.$forceUpdate();
          },
          difficulty_change(){
            this.handleSliderInput();
            this.handleSliderChange();
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