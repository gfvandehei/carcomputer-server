var interiorChart = null;
var exteriorChart = null;

function initializeCharts(){
    let interiorCanvas = document.getElementById("interiorChart").getContext("2d");
    let exteriorCanvas = document.getElementById("exteriorChart").getContext("2d");

    interiorChart = new Chart(interiorCanvas, {
        type: "line",
        data: {
            labels: [],
            datasets:[{
                label: "temperature",
                data: new Array(100),
                fill: false,
                tension: 0.1,
                borderColor: 'rgb(255, 0, 0)'
            },
            {
                label: "humidity",
                data: new Array(100),
                fill: false,
                tension: 0.1,
                borderColor: 'rgb(0,0,255)'
            }]
        },
        options: {}
    })

    exteriorChart = new Chart(exteriorCanvas, {
        type: "line",
        data: {
            labels: [],
            datasets:[{
                label: "temperature",
                data: new Array(100),
                fill: false,
                tension: 0.1,
                borderColor: 'rgb(255, 0, 0)',
            },
            {
                label: "humidity",
                data: new Array(100),
                fill: false,
                tension: 0.1,
                borderColor: 'rgb(0, 0, 255)',
            }]
        },
        options: {
            showLines: true
        }
    });
}

function parseAPIClimateToValueJSON(apidata){

}

function updateInteriorChart(newData){
    //parse new data
    console.log(newData);
    let timestamps = [];
    //interiorChart.data = newData;
    let temparr = newData.map((value, i, arr) => {
        timestamps.push(value.timestamp);
        return Number.parseInt(value.data.temperature);
    })
    let humarr = newData.map((value, i, arr) => {
        return Number.parseInt(value.data.humidity);
    })
    interiorChart.data.labels = new Array(temparr.length).fill(0);
    for(let i=0;i<humarr.length;i++){
        interiorChart.data.datasets[0].data[i] = temparr[i];
        interiorChart.data.datasets[1].data[i] = humarr[i];
    }
    interiorChart.update();
}

function updateExteriorChart(newData){
    //parse new data
    console.log(newData);
    let timestamps = [];
    //interiorChart.data = newData;
    let temparr = newData.map((value, i, arr) => {
        timestamps.push(value.timestamp);
        return Number.parseInt(value.data.temperature);
    })
    let humarr = newData.map((value, i, arr) => {
        return Number.parseInt(value.data.humidity);
    })
    exteriorChart.data.labels = new Array(temparr.length).fill(0);
    for(let i=0;i<humarr.length;i++){
        exteriorChart.data.datasets[0].data[i] = temparr[i];
        exteriorChart.data.datasets[1].data[i] = humarr[i];
    }
    exteriorChart.update();
}