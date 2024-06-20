const video = document.getElementById('video');
const canvas = document.getElementById('output');
const ctx = canvas.getContext('2d');
const saveFrameButton = document.getElementById('saveFrame');
let shoulderCoordinates = [];
let shoulderResults = [];
let chestResults = [];

async function setupCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false
    });
    video.srcObject = stream;
    return new Promise((resolve) => {
        video.onloadedmetadata = () => {
            resolve(video);
        };
    });
}

async function loadBodyPix() {
    const model = bodySegmentation.SupportedModels.BodyPix;
    const segmenterConfig = {
        architecture: 'MobileNetV1',
        outputStride: 16,
        quantBytes: 4,
        multiplier: 1.0,
    };
    segmenter = await bodySegmentation.createSegmenter(model, segmenterConfig);
}

function showBanner() {
    return new Promise((resolve) => {
        var banner = document.getElementById('banner');
        banner.style.display = 'block';

        // Set a timer to remove the banner after 6 seconds
        setTimeout(function() {
            banner.style.display = 'none';
            resolve();
        }, 6000);
    });
}

async function detectBody() {
    const segmentationConfig = {multiSegmentation: false, segmentBodyParts: true, internalResolution: "full"};
    const segmentation = await segmenter.segmentPeople(video, segmentationConfig);
    console.log(segmentation)
    const foregroundColor = {r: 255, g: 255, b: 255, a: 255};
    const backgroundColor = {r: 0, g: 0, b: 0, a: 255};
    const coloredPartImage = await bodySegmentation.toBinaryMask(segmentation,foregroundColor,backgroundColor);

    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.putImageData(coloredPartImage, 0, 0);
    drawLine();
    requestAnimationFrame(detectBody);
}

function detectShoulder() {
    const dataURL = canvas.toDataURL('image/png');
    console.log("dataURL")
    fetch('/detect_shoulder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: dataURL })
    })
    .then(response => response.json())
    .then(data => {
        const resultSection = document.getElementById('shoulderResult');
        if (data.shoulder !== undefined) {
            resultSection.textContent = `Shoulder detection result: ${data.shoulder.result}`;
            if(data.shoulder.result >= 34 && data.shoulder.result <= 48){
                shoulderResults.push(data.shoulder.result);            
            }
            shoulderCoordinates = data.shoulder.keypoints;
            console.log(shoulderCoordinates);
        } else {
            resultSection.textContent = 'Error detecting shoulder';
        }
    })
    .catch(error => {
        const resultSection = document.getElementById('shoulderResult');
        resultSection.textContent = 'Error evaluating shoulders';
        console.error('Error:', error);
    });
}

function detectChest() {
    const dataURL = canvas.toDataURL('image/png');
    fetch('/detect_chest', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: dataURL })
    })
    .then(response => response.json())
    .then(data => {
        const resultSection = document.getElementById('chestResult');
        if (data.chest !== undefined) {
            resultSection.textContent = `Chest detection result: ${data.chest.result}`;
            chestResults.push(data.chest.result);
        } else {
            resultSection.textContent = 'Error detecting chest';
        }
    })
    .catch(error => {
        const resultSection = document.getElementById('chestResult');
        resultSection.textContent = 'Error evaluating chest';
        console.error('Error:', error);
    });
}

function drawLine() {
    if(shoulderCoordinates.length > 0){
        const [x1, y1, x2, y2] = shoulderCoordinates;
        ctx.strokeStyle = 'red';
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.lineWidth = 3;
        ctx.stroke();
    }
}

function collectShoulderData() {
    return new Promise((resolve) => {
        const intervalId = setInterval(() => {
            detectShoulder();
        }, 1000);

        setTimeout(() => {
            clearInterval(intervalId);
            resolve(shoulderResults);
        }, 15000);
    });
}

function collectChestData() {
    return new Promise((resolve) => {
        const intervalId = setInterval(() => {
            detectChest();
        }, 1000);

        setTimeout(() => {
            clearInterval(intervalId);
            resolve(chestResults);
        }, 15000);
    });
}

setupCamera().then(() => {
    loadBodyPix().then(() => {
        detectBody();
        return collectShoulderData();
    })
    .then((shoulderResults) => {
        document.getElementById('shoulderResult').style.display = 'none';
        const average = array => array.reduce((a, b) => a + b) / array.length;
        const shoulderPrediction = average(shoulderResults)
        const resultElement = document.getElementById('display-result-shoulder');
        resultElement.textContent = `Shoulder prediction: ${shoulderPrediction}`;
        resultElement.style.display = 'block';
    })
    .then(() => {
        return showBanner();
    })
    .then(() => {
        return collectChestData();
    })
    .then((chestResults) => {
        document.getElementById('chestResult').style.display = 'none';
        const average = array => array.reduce((a, b) => a + b) / array.length;
        const chestPrediction = average(chestResults)
        const resultElement = document.getElementById('display-result-chest');
        resultElement.textContent = `Chest prediction: ${chestPrediction}`;
        resultElement.style.display = 'block';
    })
    .catch((error) => {
        console.error("Error during setup or data collection:", error);
    });
});
