let image = {}
function readFileDataAsBase64() {
    let file = document.querySelector(
        'input[type=file]')['files'][0];
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = (event) => {
            resolve(event.target.result);
        };

        reader.onerror = (err) => {
            reject(err);
        };

        reader.readAsDataURL(file);
    });
}

function displayString() {
 let file = document.querySelector(
        'input[type=file]')['files'][0];

file1 = readFileDataAsBase64();
console.log(fi)

let data = {

  "color": "string",
  "font": "string",
  "font_size": "string",
  "font_weight": "string",
  "x": "string",
  "y": "string",
  "z": "string",
  "width": "string",
  "height": "string",
  "image": file1,
  "text": "string",
  "type": 1
}
console.log( JSON.stringify([ data ,]))
let formData = new FormData();
formData.append('component',JSON.stringify(data));



fetch("http://127.0.0.1:8000/layout/", {method: "POST",
        body: formData
        });


}
