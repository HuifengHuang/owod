export function getSimilarValue(image_path){
    let image_name = image_path.match(/[^\\]+$/)[0];
    let value = image_name.slice(0,6);
    return parseFloat(value);
}