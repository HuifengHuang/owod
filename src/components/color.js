import * as d3 from "d3";

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateColorHSL(hue, saturation, lightness) {
    return d3.hsl(hue, saturation, lightness).toString();
}

export function generateDistinctColors(count, minHueDifference = 30) {
    const colors = [];
    let lastHue = getRandomInt(0, 360);

    for (let i = 0; i < count; i++) {
        let hue;
        do {
            hue = getRandomInt(0, 360);
        } while (Math.abs(hue - lastHue) < minHueDifference);

        lastHue = hue;
        const color = generateColorHSL(hue, 0.7, 0.5);  // 固定饱和度和亮度，确保颜色鲜艳
        colors.push(color);
    }

    return colors;
}

export function colors_50(){
    const colors = [
        "#FF5733", // 橙红色
        "#33FF57", // 酸橙绿色
        "#3357FF", // 皇室蓝
        "#FF33A6", // 深粉红色
        "#33FFF7", // 天蓝色
        "#F7FF33", // 柠檬黄色
        "#FF3333", // 鲜红色
        "#33FF33", // 明绿色
        "#3333FF", // 经典蓝
        "#FFFF33", // 亮黄色
        "#33FFFF", // 青色
        "#FF33FF", // 洋红色
        "#5733FF", // 紫罗兰色
        "#337AFF", // 淡蓝色
        "#FF337A", // 鲜粉红色
        "#7AFF33", // 浅绿色
        "#FF7A33", // 桔黄色
        "#FF33F7", // 亮粉色
        "#33FF7A", // 薄荷绿色
        "#7A33FF", // 紫罗兰色
        "#33A6FF", // 天空蓝
        "#33FFA6", // 浅绿色
        "#FFA633", // 橙黄色
        "#7AFF33", // 青草绿
        "#337AFF", // 宝石蓝
        "#FF33A6", // 樱桃红
        "#FF7A33", // 珊瑚橙
        "#FF337A", // 草莓红
        "#33FF57", // 绿黄色
        "#3357FF", // 深蓝色
        "#33FFF7", // 青蓝色
        "#FF33F7", // 粉红色
        "#FF5733", // 番茄色
        "#33FF7A", // 青翠绿
        "#FF33FF", // 玫瑰红
        "#33FF33", // 荧光绿色
        "#FF5733", // 火红色
        "#5733FF", // 靛蓝色
        "#FF337A", // 桃红色
        "#FF33FF", // 深粉色
        "#33FFFF", // 电光蓝
        "#FFFF33", // 亮黄色
        "#33FFA6", // 浅绿色
        "#FF7A33", // 珊瑚色
        "#5733FF", // 蓝紫色
        "#FF5733", // 橙色
        "#33FF7A", // 青翠绿
        "#FF33F7", // 亮粉色
        "#33A6FF", // 天空蓝
        "#FF33A6"  // 樱桃红
    ];
    return colors;    
}

export function colors_20(){
    return [
        "#709fc4",
        "#c6daed",
        "#eaa662",
        "#f0caa6",
        "#80b778",
        "#d1bcb3",
        "#d46d69",
        "#e9b1b9",
        "#C9E2D4 ",
        "#d1c6dd",
        "#af8783",
        "#bfd9ae",
        "#d0a2c4",
        "#f0d1dd",
        "#A5B5D9 ",
        "#E9D9B1 ",
        "#b197bf",
        "#F7E3AF ",
        "#B9A896",
        "#D8A499 ",
    ];
}

// "#709fc4",
// "#c6daed",
// "#eaa662",
// "#f0caa6",
// "#80b778",
// "#bfd9ae",
// "#d46d69",
// "#e9b1b9",
// "#b197bf",
// "#d1c6dd",
// "#af8783",
// "#d1bcb3",
// "#d0a2c4",
// "#f0d1dd",
// "#A5B5D9 ",
// "#E9D9B1 ",
// "#C9E2D4 ",
// "#F7E3AF ",
// "#B9A896",
// "#D8A499 ",