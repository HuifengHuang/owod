export function getSimilarValue(image_path){
    let image_name = image_path.match(/[^\\]+$/)[0];
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
export function single_class_shown(results_single){
    const keys = Object.keys(results_single);
    const values = Object.values(results_single);
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
}