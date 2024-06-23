const video = document.getElementById('video');
const canvas = document.getElementById('output');
const ctx = canvas.getContext('2d');
const saveFrameButton = document.getElementById('saveFrame');
let shoulderCoordinates = [];
let shoulderResults = [];
let torsoResults = [];
let userInputValue = '';
let shoulderDetectionPart = true;

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
    const foregroundColor = {r: 255, g: 255, b: 255, a: 255};
    const backgroundColor = {r: 0, g: 0, b: 0, a: 255};
    const coloredPartImage = await bodySegmentation.toBinaryMask(segmentation,foregroundColor,backgroundColor);

    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.putImageData(coloredPartImage, 0, 0);
    if(shoulderDetectionPart){
        drawLine();
    }
    requestAnimationFrame(detectBody);
}

function detectShoulder() {
    const dataURL = canvas.toDataURL('image/png');
    fetch('/detect_shoulder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: dataURL, userInput: userInputValue })
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

function detectTorso() {
    const dataURL = canvas.toDataURL('image/png');
    fetch('/detect_torso', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: dataURL, userInput: userInputValue })
    })
    .then(response => response.json())
    .then(data => {
        const resultSection = document.getElementById('torsoResult');
        if (data.torso !== undefined) {
            resultSection.textContent = `Torso detection result: ${data.torso.result}`;
            torsoResults.push(data.torso.result);
        } else {
            resultSection.textContent = 'Error detecting torso';
        }
    })
    .catch(error => {
        const resultSection = document.getElementById('torsoResult');
        resultSection.textContent = 'Error evaluating torso';
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

function collectTorsoData() {
    return new Promise((resolve) => {
        const intervalId = setInterval(() => {
            detectTorso();
        }, 1000);

        setTimeout(() => {
            clearInterval(intervalId);
            resolve(torsoResults);
        }, 15000);
    });
}
document.getElementById('startProcess').addEventListener('click', () => {
    userInputValue = document.getElementById('userInput').value;
    setTimeout(() => {
        // Wait 5 seconds after user input to make time for user to get in position
        // 1. Step = load body segmentation model and start shoulder processing
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
                resultElement.textContent = `Shoulder prediction: ${shoulderPrediction} cm`;
                resultElement.style.display = 'block';
                shoulderDetectionPart = false;
            })
            // 2. Step = after getting shoulder results show banner so user can be guided to raise their hand (T shape)
            .then(() => {
                return showBanner();
            })
            // 3. Step = after user is in T shape, start torso processing
            .then(() => {
                return collectTorsoData();
            })
            .then((torsoResults) => {
                document.getElementById('torsoResult').style.display = 'none';
                const average = array => array.reduce((a, b) => a + b) / array.length;
                const torsoPrediction = average(torsoResults)
                const resultElement = document.getElementById('display-result-torso');
                resultElement.textContent = `Torso prediction: ${torsoPrediction} cm`;
                resultElement.style.display = 'block';
            })
            .catch((error) => {
                console.error("Error during setup or data collection:", error);
            });
        });
    }, 5000); // Wait for 5 seconds
});