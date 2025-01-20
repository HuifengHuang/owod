
export function getSimilarValue(image_path){
    let image_name = image_path.match(/0\.(.*)/)[0];
    let value = image_name.slice(0,6);
    return parseFloat(value);
}

export function arrayBufferToBase64(buffer) {
    //第一步，将ArrayBuffer转为二进制字符串
    var binary = "";
    var bytes = new Uint8Array(buffer);
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    //将二进制字符串转为base64字符串
    return window.btoa(binary);
}

export function findMaxMin(dataset,index){
    var max=-9999 , min=9999;
    for(let i in dataset){
        if(dataset[i][index]>max)max = dataset[i][index];
        if(dataset[i][index]<min)min = dataset[i][index];
    }
    return [max,min];
}

import * as d3 from "d3";
export function single_class_shown(results_single_old, results_single_new){
    var results = [];
    for(let key in results_single_old){
        var item = {};
        item["name"] = key;
        item["old"] = results_single_old[key];
        item["new"] = results_single_new[key];
        results.push(item);
    }
    const width = 420;
    const marginTop = 20;
    const marginRight = 50;
    const marginBottom = 10;
    const marginLeft = 100;
    const height = results.length * 30 + marginTop + marginBottom;
    var svg = d3.select("#result_single_svg")
        .attr("width", width)
        .attr("height", height);
    
    var xScale = d3.scaleLinear()
        .domain([0,d3.max(results, d => Math.max(d.old, d.new))])
        .range([0 ,  width - marginRight - marginLeft]);

    var fyScale = d3.scaleBand()
        .domain(results.map(d => d.name))
        .range([marginTop, height - marginBottom])
        .padding(0.15)

    var yScale = d3.scaleBand()
        .domain(["old", "new"])
        .range([0, fyScale.bandwidth()])
        .padding(0.05);

    svg.selectAll(".group")
        .data(results)
        .enter()
        .append("g")
        .attr("transform", d => `translate(0,${fyScale(d.name)})`)
        .selectAll("rect")
        .data(d => [
            { key: "old", value: d.old },
            { key: "new", value: d.new }
        ])
        .enter()
        .append("rect")
        .attr("x", marginLeft)
        .attr("y", d => yScale(d.key))
        .attr("width", d => xScale(d.value))
        .attr("height", yScale.bandwidth())
        .attr("class", d => d.key === "old" ? "bar" : "bar2");

    const xAxis = d3.axisTop(xScale);
    const yAxis = d3.axisLeft(fyScale);

    svg.append("g")
        .attr("class", "x-axis")
        .attr("transform", `translate(${marginLeft},${marginTop})`)
        .call(xAxis)

    svg.append("text")
        .attr("transform", `translate(${marginLeft + 290}, ${marginTop - 5})`)
        .text("mAP")
        .attr("text-anchor", "middle")  // 设置文本水平居中对齐
        .attr("dominant-baseline", "middle")  // 设置文本垂直居中对齐
        .attr("font-size", "14px");

    svg.append("g")
      .attr("class", "y-axis")
      .attr("transform", `translate(${marginLeft},0)`)
      .call(yAxis)
      .select("path")  // 选择轴线 path 元素
      .style("display", "none");  // 隐藏轴线

    svg.selectAll(".tick text")
        .style("font-size", "12px");

    svg.append("text")
        .attr("transform", `translate(15, 10)`)
        .text("Old")
        .attr("class", "text_class");
    svg.append("text")
        .attr("transform", `translate(15, 22)`)
        .text("New")
        .attr("class", "text_class");
    svg.append("rect")
        .attr("x", 30)
        .attr("y", 3)
        .attr("width", 40)
        .attr("height", 10)
        .attr("class",  "bar2");
    svg.append("rect")
        .attr("x", 30)
        .attr("y", 16)
        .attr("width", 40)
        .attr("height", 10)
        .attr("class",  "bar");
    svg.selectAll(".text_class")
        .attr("text-anchor", "middle")  // 设置文本水平居中对齐
        .attr("dominant-baseline", "middle")  // 设置文本垂直居中对齐
        .attr("font-size", "12px");
}

export function overall_class_shown(results_overall){
    var results = [];
    for(let key in results_overall){
        var item = {};
        item["name"] = key;
        item["value"] = results_overall[key];
        results.push(item);
    }
    const width = 420;
    const marginTop = 20;
    const marginRight = 10;
    const marginBottom = 30;
    const marginLeft = 50;
    const height = 240 + marginTop + marginBottom;
    const rectWidth = 40;
    var svg = d3.select("#result_overall_svg")
        .attr("width", width)
        .attr("height", height);

    var yScale = d3.scaleLinear()
        .domain([0, d3.max(results, d => d.value)])
        .range([height - marginBottom, marginTop])

    svg.selectAll("rect")
        .data(results)
        .enter()
        .append("rect")
        .attr("x", function(d){
            if(d.name == "Previous-old"){
                return marginLeft + 40;
            }else if(d.name == "Previous-new"){
                return marginLeft + 81;
            }else if(d.name == "Current"){
                return marginLeft + 160;
            }else if(d.name == "All"){
                return marginLeft + 240;
            }
        })
        .attr("y", d => yScale(d.value))
        .attr("width", rectWidth)
        .attr("height", d => yScale(0) - yScale(d.value))
        .attr("class", d => d.name === "Previous-old" ? "bar2" : "bar");

    svg.append("g")
        .attr("transform", `translate(${marginLeft + 20}, 0)`)
        .call(d3.axisLeft(yScale));

    const xScale = d3.scaleLinear()
        .domain([0, 1000])  // 数据范围
        .range([0, 500]);
    svg.append("g")
        .attr("transform", `translate(${marginLeft + 20}, ${height - marginBottom})`)
        .call(d3.axisBottom(xScale).ticks(0));

    svg.append("text")
        .attr("transform", `translate(${marginLeft + 80}, ${height - marginBottom + 12})`)
        .text("Previous")
        .attr("class", "text_class");
    svg.append("text")
        .attr("transform", `translate(${marginLeft + 180}, ${height - marginBottom + 12})`)
        .text("Current")
        .attr("class", "text_class");
    svg.append("text")
        .attr("transform", `translate(${marginLeft + 260}, ${height - marginBottom + 12})`)
        .text("All")
        .attr("class", "text_class");

    svg.append("text")
        .attr("transform", `translate(${marginLeft + 200}, 10)`)
        .text("Old")
        .attr("class", "text_class");
    svg.append("text")
        .attr("transform", `translate(${marginLeft + 280}, 10)`)
        .text("New")
        .attr("class", "text_class");
    svg.append("rect")
        .attr("x", marginLeft + 215)
        .attr("y", 3)
        .attr("width", 40)
        .attr("height", 10)
        .attr("class",  "bar2");
    svg.append("rect")
        .attr("x", marginLeft + 295)
        .attr("y", 3)
        .attr("width", 40)
        .attr("height", 10)
        .attr("class",  "bar");

    svg.append("text")
        .attr("transform", `translate(${marginLeft + 5}, 10)`)
        .text("mAP")
        .attr("text-anchor", "middle")  // 设置文本水平居中对齐
        .attr("dominant-baseline", "middle")  // 设置文本垂直居中对齐
        .attr("font-size", "14px");


    svg.selectAll(".text_class")
        .attr("text-anchor", "middle")  // 设置文本水平居中对齐
        .attr("dominant-baseline", "middle")  // 设置文本垂直居中对齐
        .attr("font-size", "12px");
}

export function kernelDensityEstimator(kernel, X) {
    return function(V) {
      return X.map(function(x) {
        return [x, d3.mean(V, function(v) { return kernel(x - v); })];
      });
    };
}
  
export function kernelEpanechnikov(k) {
    return function(v) {
        return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
    };
}

export function density_shown(svg_name, similarities){
    // var similarities = [79,54,74,62,85,55,88,85,51,85,54,84,78,47,83,52,62,84,52,79,51,47,78,69,74,83,55,76,78,79,73,77,66,80,74,52,48,80,59,90,80,58,84,58,73,83,64,53,82,59,75,90,54,80,54,83,71,64,77,81,59,84,48,82,60,92,78,78,65,73,82,56,79,71,62,76,60,78,76,83,75,82,70,65,73,88,76,80,48,86,60,90,50,78,63,72,84,75,51,82,62,88,49,83,81,47,84,52,86,81,75,59,89,79,59,81,50,85,59,87,53,69,77,56,88,81,45,82,55,90,45,83,56,89,46,82,51,86,53,79,81,60,82,77,76,59,80,49,96,53,77,77,65,81,71,70,81,93,53,89,45,86,58,78,66,76,63,88,52,93,49,57,77,68,81,81,73,50,85,74,55,77,83,83,51,78,84,46,83,55,81,57,76,84,77,81,87,77,51,78,60,82,91,53,78,46,77,84,49,83,71,80,49,75,64,76,53,94,55,76,50,82,54,75,78,79,78,78,70,79,70,54,86,50,90,54,54,77,79,64,75,47,86,63,85,82,57,82,67,74,54,83,73,73,88,80,71,83,56,79,78,84,58,83,43,60,75,81,46,90,46,74];

    var svg = d3.select("#" + svg_name);
    svg.selectAll("*").remove();
    var container = d3.select('#svg_container');
    var containerWidth = container.node().offsetWidth;
    var containerHeight = container.node().offsetHeight;
    var margin = {top: 1, right: 10, bottom: 20, left: 10};
    var Width = containerWidth - margin.right - margin.left;
    var Height = containerHeight - margin.top - margin.bottom;
    

    var xScale = d3.scaleLinear()
                    .domain([Math.min(...similarities),Math.max(...similarities)])
                    .range([margin.left, Width + margin.left]);
    var yScale = d3.scaleLinear()
                    .range([Height + margin.top, margin.top]);
    var density = kernelDensityEstimator(kernelEpanechnikov(0.005), xScale.ticks(80))(similarities);
    yScale.domain([0, d3.max(density, function(d) { return d[1]; })]);
    svg.append("path")
        .datum(density)
        .attr("fill", "none")
        .attr("stroke", "#000")
        .attr("stroke-width", 1.5)
        .attr("stroke-linejoin", "round")
        .attr("d",  d3.line()
            .curve(d3.curveBasis)
            .x(function(d) { return xScale(d[0]); })
            .y(function(d) { return yScale(d[1]); }));

    const area = d3.area()
        .x(function(d) { return xScale(d[0]); })
        .y1(function(d) { return yScale(d[1]); }) // 曲线顶部
        .y0(yScale(0));  // 基线设为 X 轴的 y(0)

    svg.append("path")
       .datum(density)
       .attr("fill", "#A5A5A5 ") // 设置填充颜色
       .attr("opacity", 0.5)    // 设置透明度
       .attr("d", area);

    svg.append("g")
       .attr("class", "axis axis--x")
       .attr("transform", "translate(0," + (Height) + ")")
       .call(d3.axisBottom(xScale))
     .append("text")
       .attr("x", Width - margin.right)
       .attr("y", -6)
       .attr("fill", "#000")
       .attr("text-anchor", "end")
       .attr("font-weight", "bold");
}

export function filter_glaph(json_glaph, min, max){
    
}