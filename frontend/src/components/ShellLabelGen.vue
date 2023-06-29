
<template>
    <div class="container">
        <div class="canvas-container" style="display: flex; flex-direction: column; align-items: center;">
            <div>
                <canvas id="Label"></canvas>
                <br />
                <button class="button-spacing" @click="download">下载标签图片</button>
                <button @click="genPdf">生成pdf文件</button>
            </div>
        </div>
    </div>
</template>

<script>
import { fabric } from 'fabric';
import { jsPDF } from 'jspdf';
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
                shellAuthorValue: "tsyj",
                shellLocationValue: "China",
                shellSizeValue: "100mm",
                shellQualityValue: "F+++/Gem",
                shellInfoValue: "葛大店海域8000米深的toilet海沟内",
            }]
        };
        let smallCanvases = [];

        return {
            canvas, input, smallCanvases
        }
    },
    mounted() {
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

        function createTextbox(text, left, top, width, fontsize, edit, canvas) {
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
        }

        function stdFrame() {
            // shellName: "中文名:",
            // shellLatin: "拉丁名:",
            // shellAuthor: "作者:",
            // shellLocation: "地点:",
            // shellSize: "尺寸:",
            // shellQuality: "品相:",
            // shellInfo: "信息:",
            // shellSeller: "tutu's label",235 135
            var shellNameBox = createTextbox(this.input.basicInfo['shellName'], 10, 10, 40, 12, false, this.canvas);
            var shellLatin = createTextbox(this.input.basicInfo['shellLatin'], 10, 25, 40, 12, false, this.canvas);
            var shellAuthor = createTextbox(this.input.basicInfo['shellAuthor'], 10, 40, 40, 12, false, this.canvas);
            var shellLocation = createTextbox(this.input.basicInfo['shellLocation'], 10, 55, 40, 12, false, this.canvas);
            var shellSize = createTextbox(this.input.basicInfo['shellSize'], 10, 70, 40, 12, false, this.canvas);
            var shellQuality = createTextbox(this.input.basicInfo['shellQuality'], 110, 70, 30, 12, false, this.canvas);
            var shellInfo = createTextbox(this.input.basicInfo['shellInfo'], 10, 85, 40, 12, false, this.canvas);
            var shellSeller = createTextbox(this.input.basicInfo['shellSeller'], 180, 120, 40, 9, true, this.canvas);


            var shellIDValue = createTextbox(this.input.dataInfo[0]['shellIDValue'], 200, 5, 160, 9, true, this.canvas);
            var shellNameBoxValue = createTextbox(this.input.dataInfo[0]['shellNameValue'], 55, 10, 160, 12, true, this.canvas);
            var shellLatinValue = createTextbox(this.input.dataInfo[0]['shellLatinValue'], 55, 27, 160, 10, true, this.canvas);
            var shellAuthorValue = createTextbox(this.input.dataInfo[0]['shellAuthorValue'], 55, 41, 160, 10, true, this.canvas);
            var shellLocationValue = createTextbox(this.input.dataInfo[0]['shellLocationValue'], 55, 56, 160, 10, true, this.canvas);
            var shellSizeValue = createTextbox(this.input.dataInfo[0]['shellSizeValue'], 55, 70, 80, 12, true, this.canvas);
            var shellQualityValue = createTextbox(this.input.dataInfo[0]['shellQualityValue'], 150, 70, 80, 12, true, this.canvas);
            var shellInfoValue = createTextbox(this.input.dataInfo[0]['shellInfoValue'], 55, 86, 160, 12, true, this.canvas);

            var showArray = []
            showArray.push(shellNameBox);
            showArray.push(shellLatin);
            showArray.push(shellAuthor);
            showArray.push(shellLocation);
            showArray.push(shellSize);
            showArray.push(shellQuality);
            showArray.push(shellInfo);
            showArray.push(shellIDValue);
            showArray.push(shellNameBoxValue);
            showArray.push(shellLatinValue);
            showArray.push(shellQualityValue);
            showArray.push(shellInfoValue);
            showArray.push(shellSeller);
            showArray.push(shellSizeValue);
            showArray.push(shellAuthorValue);
            showArray.push(shellLocationValue);

            showArray.forEach(item => {
                this.canvas.add(item);
            })
        }
        stdFrame.call(this);
    },
    methods: {
        download() {
            // 创建一个链接并设置其 href 属性为画布的数据 URL
            let link = document.createElement('a');
            link.href = this.canvas.toDataURL({ format: 'png' });
            // 将下载文件名设置为 'canvas.png'
            link.download = 'label.png';
            // 模拟点击链接来下载图像
            link.click();
        },
        genPdf() {
            let canvasList = []
            for (let i = 0; i < 30; i++) {
                canvasList.push(this.canvas)
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
                let imagePromises = canvasList.map((smallCanvas, index) => {
                    return new Promise((resolve) => {

                        let smallCanvasDataUrl = smallCanvas.toDataURL();
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