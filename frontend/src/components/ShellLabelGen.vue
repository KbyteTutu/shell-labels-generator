
<template>
    <div>
        <p>可以用鼠标来随意修改下面标签中各个元素的位置、大小等。</p>
        <p>右下角的卖家标记可以双击编辑内容</p>
        <p style="font-size: 5px; color: red;">保存布局、修改字体、添加背景图片等功能筹备中……</p>
    </div>
    <div class="container">
        <div class="canvas-container" style="display: flex; flex-direction: column; align-items: center;">
            <div>
                <canvas id="Label"></canvas>
                <br />
                <!-- <button class="button-spacing" @click="download">下载标签图片</button> -->
            </div>
        </div>
    </div>
    <p>填写这张<a href="https://tutu.gold/fileshare/shells.xlsx" target="_blank">贝壳信息表</a>并在此上传，然后点击生成pdf文件即可</p>
    <div class="xlsx-upload">
        <input type="file" @change="onFileChange" accept=".xlsx" />
        <div v-for="(row, index) in data" :key="index">
            {{ row }}
        </div>
    </div>
    <div>
        <br />
        <button @click="genPdf">生成pdf文件</button>
    </div>
</template>

<script>
import { fabric } from 'fabric';
import { jsPDF } from 'jspdf';
import * as XLSX from 'xlsx';

export default {
    name: 'ShellLabelGen',
    setup() {
        let canvas = null;

        let input = {
            basicInfo: {
                shellName: "中文名:",
                shellLatin: "拉丁名:",
                shellAuthor: "作者:",
                shellLocation: "地点:",
                shellSize: "尺寸:",
                shellQuality: "品相:",
                shellInfo: "信息:",
                shellSeller: "tutu's label",
            },
            dataInfo: [{
                shellIDValue: "0",
                shellNameValue: "太阳缀壳螺",
                shellLatinValue: "Xenophora solarioides sp.",
                shellAuthorValue: "涛总",
                shellLocationValue: "China",
                shellSizeValue: "100mm",
                shellQualityValue: "F+++/Gem",
                shellFamilyValue: "缀壳螺科",
                shellInfoValue: "葛大店海域8000米深的海沟内",
            }]
        };
        let smallCanvases = [];

        return {
            canvas, input, smallCanvases
        }
    },
    mounted() {
        this.createCanvas(0);
    },
    methods: {
        createCanvas(idx) {
            this.canvas = new fabric.Canvas('Label', {
                width: 235,
                height: 135,
            });

            let background = new fabric.Rect({
                width: this.canvas.width,
                height: this.canvas.height,
                fill: 'white',
                selectable: false,
                evented: false,
            });
            this.canvas.add(background);
            this.canvas.sendToBack(background);

            var border = new fabric.Rect({
                left: 0,
                top: 0,
                fill: 'transparent',
                stroke: '#000',
                strokeWidth: 2,
                width: this.canvas.width - 2,
                height: this.canvas.height - 2,
                selectable: false,
            });

            this.canvas.add(border);
            this.stdFrame(idx);
            return this.canvas;
        }, createTextbox(text, left, top, width, fontsize, edit, canvas) {
            let textbox = new fabric.Textbox(text, {
                left: left,
                top: top,
                width: width,
                fontSize: fontsize,
                editable: edit,
                splitByGrapheme: true,

            });

            // Add a 'moving' event listener to the textbox
            textbox.on('moving', function () {
                let obj = this;
                // Limit the movement within the canvas boundaries
                obj.setCoords();
                if (obj.getBoundingRect().top < 0 || obj.getBoundingRect().left < 0) {
                    obj.top = Math.max(obj.top, 0);
                    obj.left = Math.max(obj.left, 0);
                }
                if (obj.getBoundingRect().top + obj.getBoundingRect().height > canvas.getHeight() || obj.getBoundingRect().left + obj.getBoundingRect().width > canvas.getWidth()) {
                    obj.top = Math.min(obj.top, canvas.getHeight() - obj.getBoundingRect().height + obj.top - obj.getBoundingRect().top);
                    obj.left = Math.min(obj.left, canvas.getWidth() - obj.getBoundingRect().width + obj.left - obj.getBoundingRect().left);
                }
            });

            // canvas.add(textbox);
            return textbox;
        }, stdFrame(idx) {
            const elements = [
                { key: 'shellName', x: 10, y: 10, w: 40, h: 12, editable: false, source: 'basicInfo' },
                { key: 'shellLatin', x: 10, y: 25, w: 40, h: 12, editable: false, source: 'basicInfo' },
                { key: 'shellAuthor', x: 10, y: 40, w: 40, h: 12, editable: false, source: 'basicInfo' },
                { key: 'shellLocation', x: 10, y: 55, w: 40, h: 12, editable: false, source: 'basicInfo' },
                { key: 'shellSize', x: 10, y: 70, w: 40, h: 12, editable: false, source: 'basicInfo' },
                { key: 'shellQuality', x: 110, y: 70, w: 30, h: 12, editable: false, source: 'basicInfo' },
                { key: 'shellInfo', x: 10, y: 85, w: 40, h: 12, editable: false, source: 'basicInfo' },
                { key: 'shellSeller', x: 180, y: 120, w: 40, h: 9, editable: true, source: 'basicInfo' },

                { key: 'shellIDValue', x: 200, y: 5, w: 160, h: 9, editable: true, source: 'dataInfo' },
                { key: 'shellNameValue', x: 55, y: 10, w: 160, h: 12, editable: true, source: 'dataInfo' },
                { key: 'shellLatinValue', x: 55, y: 27, w: 160, h: 10, editable: true, source: 'dataInfo' },
                { key: 'shellAuthorValue', x: 55, y: 41, w: 160, h: 10, editable: true, source: 'dataInfo' },
                { key: 'shellLocationValue', x: 55, y: 56, w: 160, h: 10, editable: true, source: 'dataInfo' },
                { key: 'shellSizeValue', x: 55, y: 70, w: 80, h: 12, editable: true, source: 'dataInfo' },
                { key: 'shellQualityValue', x: 150, y: 70, w: 80, h: 12, editable: true, source: 'dataInfo' },
                { key: 'shellFamilyValue', x: 10, y: 120, w: 80, h: 9, editable: true, source: 'dataInfo' },
                { key: 'shellInfoValue', x: 55, y: 86, w: 160, h: 12, editable: true, source: 'dataInfo' },
            ];
            this.canvas.textBoxes = {};
            elements.forEach(element => {
                const textbox = this.createTextbox(
                    element.source === 'basicInfo' ? this.input.basicInfo[element.key] : this.input.dataInfo[idx][element.key],
                    element.x,
                    element.y,
                    element.w,
                    element.h,
                    element.editable,
                    this.canvas
                );

                this.canvas.add(textbox);
                this.canvas.textBoxes[element.key] = textbox;
            });
        },
        download() {
            // 创建一个链接并设置其 href 属性为画布的数据 URL
            let link = document.createElement('a');
            link.href = this.canvas.toDataURL({ format: 'png' });
            // 将下载文件名设置为 'canvas.png'
            link.download = 'label.png';
            // 模拟点击链接来下载图像
            link.click();
        }, onFileChange(e) {
            const file = e.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) => {
                const data = new Uint8Array(e.target.result);
                const workbook = XLSX.read(data, { type: 'array' });
                const worksheet = workbook.Sheets[workbook.SheetNames[0]];
                let jsonData = XLSX.utils.sheet_to_json(worksheet);

                jsonData = jsonData.map(row => {
                    const values = Object.values(row);
                    return {
                        shellIDValue: values[0],
                        shellNameValue: values[1],
                        shellLatinValue: values[2],
                        shellAuthorValue: values[3],
                        shellLocationValue: values[4],
                        shellSizeValue: values[5],
                        shellQualityValue: values[6],
                        shellFamilyValue: values[7],
                        shellInfoValue: values[8],
                    };
                });
                this.input.dataInfo = jsonData;
                console.log(jsonData);
            };
            reader.readAsArrayBuffer(file);
        },
        genPdf() {
            let canvasList = []
            for (let i = 0; i < this.input.dataInfo.length; i++) {
                let dt = this.input.dataInfo[i];
                // 迭代 dt 中的每个键值对
                for (let key in dt) {
                    let value = dt[key];
                    if (value == null) { value = ''; }

                    if (this.canvas.textBoxes[key]) {
                        this.canvas.textBoxes[key].set({ text: value.toString() });
                    }
                }
                this.canvas.renderAll();
                canvasList.push(this.canvas.toJSON());
            }
            var width = this.canvas.width;
            var height = this.canvas.height;
            async function genPdfPages() {
                let smallCanvasWidth = width;
                let smallCanvasHeight = height;
                let canvasWidth = 730;
                let canvasHeight = 1030;
                let columns = Math.floor(canvasWidth / smallCanvasWidth);
                let rows = Math.floor(canvasHeight / smallCanvasHeight);
                let canvasesPerPage = columns * rows;

                // Create Fabric.js Canvas objects for each page
                let pages = [];
                for (let i = 0; i < Math.ceil(canvasList.length / canvasesPerPage); i++) {
                    pages.push(new fabric.Canvas('canvas' + i, {
                        width: canvasWidth,
                        height: canvasHeight,
                        backgroundColor: 'white',
                    }));
                }

                // Create an array of Promises
                let imagePromises = canvasList.map((canvasData, index) => {
                    return new Promise((resolve) => {
                        let smallCanvas = new fabric.Canvas();
                        smallCanvas.loadFromJSON(canvasData, () => {
                            let smallCanvasDataUrl = smallCanvas.toDataURL({
                                format: 'png',
                                quality: 1,
                            });
                            let pageIndex = Math.floor(index / canvasesPerPage);
                            let positionIndex = index % canvasesPerPage;

                            fabric.Image.fromURL(smallCanvasDataUrl, (img) => {
                                let columnIndex = positionIndex % columns;
                                let rowIndex = Math.floor(positionIndex / columns);

                                img.left = columnIndex * (smallCanvasWidth + 10);
                                img.top = rowIndex * (smallCanvasHeight + 10);

                                pages[pageIndex].add(img);
                                resolve();
                            });
                        });
                    });
                });

                // Wait for all Promises to resolve
                await Promise.all(imagePromises);

                return pages;
            }
            genPdfPages().then((pages) => {
                let pdf = new jsPDF({
                    format: 'a4',
                }
                );

                pages.forEach((page, i) => {
                    if (i !== 0) {
                        pdf.addPage();
                    }
                    let imageData = page.toDataURL({ format: 'jpeg' });
                    pdf.addImage(imageData, 'JPEG', 10, 10);

                });

                pdf.save('labels.pdf');
            });
        }
    },
};


</script>

<style scoped>
.container {
    display: flex;
    height: 100%;
    /* or whatever height you want */
}

.xlsx-upload {
    margin-left: 50px;
}

.sidebar {
    width: 100px;
}

.canvas-container {
    flex-grow: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    /* adjust as needed */
}

.button-spacing {
    margin-right: 20px;
}
</style>