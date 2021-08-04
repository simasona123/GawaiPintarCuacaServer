const Chart = window.chartModule.Chart;

var userAccordingTime = [];
var userAccordingSensor = [];
var a1 = 0, b1 = 0, c1 = 0;
Chart.defaults.color = '#ffffff';
Chart.defaults.borderColor = '#383838';
var checkSensor = (item) => {
    if (item.suhu_udara != 0 || item.kelembaban_udara != 0) {
        a1 += 1;
    }
    if (item.tekanan_udara != 0) {
        b1 += 1;
    }
    else {
        c1 += 1;
    }
};
var userAccording = () => {
    let a = 0, b = 0, c = 0;
    let now = Date.now();
    dataResponse.forEach((item, index) => {
        var timestamp = new Date(item.timestamp);
        var differTime = now - timestamp;
        if (differTime <= twoDays) {
            a += 1;
        } else if (differTime > twoDays && differTime <= fiveDays) {
            b += 1;
        } else {
            c += 1;
        }
        checkSensor(item);
    });
    userAccordingTime.push(a);
    userAccordingTime.push(b);
    userAccordingTime.push(c);
    userAccordingSensor.push(a1);
    userAccordingSensor.push(b1);
    userAccordingSensor.push(c1);
};
userAccording();
var ctx = document.getElementById('userCount').getContext('2d');
var ctx1 = document.getElementById('userComparison').getContext('2d');
var ctx2 = document.getElementById('lineChart').getContext('2d');
var userCount = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['< 1 Hari', '1 - 5 Hari', '> 5 Hari'],
        datasets: [{
            label: 'Jumlah User Berdasarkan Waktu Aktif Terakhir',
            data: userAccordingTime,
            backgroundColor: [
                '#a1de93',
                '#f7f48b',
                '#f47c7c',
            ],
            borderColor: '#252525',
        }],
    },
    options: {
        plugins: {
            legend: {
                position: 'bottom',
            }
        }
    }
});
var userComparison = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: ['Suhu dan Kelembaban', 'Tekanan', 'Tanpa',],
        datasets: [{
            label: 'Jumlah User Android Berdasarkan Sensor',
            data: userAccordingSensor,
            backgroundColor: [
                '#70a1d7',
                '#70a1d7',
                '#70a1d7',
            ],
            borderColor: [
                '#252525',
                '#252525',
                '#252525',
            ],
            borderWidth: 1,
        }],
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
            }
        }
    }

});
var xAxis1 = [];
xAxis.forEach((item, index) => {
    item1 = new Date(item);
    xAxis1.push(item1);
});
var stackedLine = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: xAxis1,
        datasets: [{
            label: 'Jumlah Data',
            data: yAxis,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    },
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'week'
                }
            }
        }
    }
});