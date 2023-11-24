function toggleTabs(tabType, event) {
    event.preventDefault(); // 기본 앵커 동작 방지
    if (tabType === 'sectors') {
        document.getElementById('sectors_tit').classList.add('on');
        document.getElementById('tema_tit').classList.remove('on');
        document.getElementById('sectors_sub').style.display = 'block';
        document.getElementById('tema_sub').style.display = 'none';
    } else if (tabType === 'tema') {
        document.getElementById('sectors_tit').classList.remove('on');
        document.getElementById('tema_tit').classList.add('on');
        document.getElementById('sectors_sub').style.display = 'none';
        document.getElementById('tema_sub').style.display = 'block';
    }
}

function showleft(tabType, event) {
    event.preventDefault();
    if (tabType === 'left1') {
        document.getElementById('left_tag1').classList.add('active');
        document.getElementById('left_tag2').classList.remove('active');
        document.getElementById('left_tag3').classList.remove('active');
        document.getElementById('left_tag4').classList.remove('active');
        document.getElementById('left_tag5').classList.remove('active');
        document.getElementById('left_data1').style.display = 'block';
        document.getElementById('left_data2').style.display = 'none';
        document.getElementById('left_data3').style.display = 'none';
        document.getElementById('left_data4').style.display = 'none';
        document.getElementById('left_data5').style.display = 'none';
    } else if (tabType === 'left2') {
        document.getElementById('left_tag2').classList.add('active');
        document.getElementById('left_tag1').classList.remove('active');
        document.getElementById('left_tag3').classList.remove('active');
        document.getElementById('left_tag4').classList.remove('active');
        document.getElementById('left_tag5').classList.remove('active');
        document.getElementById('left_data2').style.display = 'block';
        document.getElementById('left_data1').style.display = 'none';
        document.getElementById('left_data3').style.display = 'none';
        document.getElementById('left_data4').style.display = 'none';
        document.getElementById('left_data5').style.display = 'none';
    } else if (tabType === 'left3') {
        document.getElementById('left_tag3').classList.add('active');
        document.getElementById('left_tag1').classList.remove('active');
        document.getElementById('left_tag2').classList.remove('active');
        document.getElementById('left_tag4').classList.remove('active');
        document.getElementById('left_tag5').classList.remove('active');
        document.getElementById('left_data3').style.display = 'block';
        document.getElementById('left_data1').style.display = 'none';
        document.getElementById('left_data2').style.display = 'none';
        document.getElementById('left_data4').style.display = 'none';
        document.getElementById('left_data5').style.display = 'none';
    } else if (tabType === 'left4') {
        document.getElementById('left_tag4').classList.add('active');
        document.getElementById('left_tag1').classList.remove('active');
        document.getElementById('left_tag2').classList.remove('active');
        document.getElementById('left_tag3').classList.remove('active');
        document.getElementById('left_tag5').classList.remove('active');
        document.getElementById('left_data4').style.display = 'block';
        document.getElementById('left_data1').style.display = 'none';
        document.getElementById('left_data2').style.display = 'none';
        document.getElementById('left_data3').style.display = 'none';
        document.getElementById('left_data5').style.display = 'none';
    } else if (tabType === 'left5') {
        document.getElementById('left_tag5').classList.add('active');
        document.getElementById('left_tag1').classList.remove('active');
        document.getElementById('left_tag2').classList.remove('active');
        document.getElementById('left_tag3').classList.remove('active');
        document.getElementById('left_tag4').classList.remove('active');
        document.getElementById('left_data5').style.display = 'block';
        document.getElementById('left_data1').style.display = 'none';
        document.getElementById('left_data2').style.display = 'none';
        document.getElementById('left_data3').style.display = 'none';
        document.getElementById('left_data4').style.display = 'none';
    }
}

function showright(tabType, event) {
    event.preventDefault();
    if (tabType === 'right1') {
        document.getElementById('right_tag1').classList.add('active');
        document.getElementById('right_tag2').classList.remove('active');
        document.getElementById('right_tag3').classList.remove('active');
        document.getElementById('right_tag4').classList.remove('active');
        document.getElementById('right_tag5').classList.remove('active');
        document.getElementById('right_data1').style.display = 'block';
        document.getElementById('right_data2').style.display = 'none';
        document.getElementById('right_data3').style.display = 'none';
        document.getElementById('right_data4').style.display = 'none';
        document.getElementById('right_data5').style.display = 'none';
    } else if (tabType === 'right2') {
        document.getElementById('right_tag2').classList.add('active');
        document.getElementById('right_tag1').classList.remove('active');
        document.getElementById('right_tag3').classList.remove('active');
        document.getElementById('right_tag4').classList.remove('active');
        document.getElementById('right_tag5').classList.remove('active');
        document.getElementById('right_data2').style.display = 'block';
        document.getElementById('right_data1').style.display = 'none';
        document.getElementById('right_data3').style.display = 'none';
        document.getElementById('right_data4').style.display = 'none';
        document.getElementById('right_data5').style.display = 'none';
    } else if (tabType === 'right3') {
        document.getElementById('right_tag3').classList.add('active');
        document.getElementById('right_tag1').classList.remove('active');
        document.getElementById('right_tag2').classList.remove('active');
        document.getElementById('right_tag4').classList.remove('active');
        document.getElementById('right_tag5').classList.remove('active');
        document.getElementById('right_data3').style.display = 'block';
        document.getElementById('right_data1').style.display = 'none';
        document.getElementById('right_data2').style.display = 'none';
        document.getElementById('right_data4').style.display = 'none';
        document.getElementById('right_data5').style.display = 'none';
    } else if (tabType === 'right4') {
        document.getElementById('right_tag4').classList.add('active');
        document.getElementById('right_tag1').classList.remove('active');
        document.getElementById('right_tag2').classList.remove('active');
        document.getElementById('right_tag3').classList.remove('active');
        document.getElementById('right_tag5').classList.remove('active');
        document.getElementById('right_data4').style.display = 'block';
        document.getElementById('right_data1').style.display = 'none';
        document.getElementById('right_data2').style.display = 'none';
        document.getElementById('right_data3').style.display = 'none';
        document.getElementById('right_data5').style.display = 'none';
    } else if (tabType === 'right5') {
        document.getElementById('right_tag5').classList.add('active');
        document.getElementById('right_tag1').classList.remove('active');
        document.getElementById('right_tag2').classList.remove('active');
        document.getElementById('right_tag3').classList.remove('active');
        document.getElementById('right_tag4').classList.remove('active');
        document.getElementById('right_data5').style.display = 'block';
        document.getElementById('right_data1').style.display = 'none';
        document.getElementById('right_data2').style.display = 'none';
        document.getElementById('right_data3').style.display = 'none';
        document.getElementById('right_data4').style.display = 'none';
    }
}

function showleftchart(tabType, event) {
    event.preventDefault();
    if (tabType === 'lchart1') {
        document.getElementById('left_chart1').classList.add('active');
        document.getElementById('left_chart2').classList.remove('active');
        document.getElementById('left_chart_main1').style.display = 'block';
        document.getElementById('left_chart_main2').style.display = 'none';
    } else if (tabType === 'lchart2') {
        document.getElementById('left_chart2').classList.add('active');
        document.getElementById('left_chart1').classList.remove('active');
        document.getElementById('left_chart_main2').style.display = 'block';
        document.getElementById('left_chart_main1').style.display = 'none';
    }
}

function showrightchart(tabType, event) {
    event.preventDefault();
    if (tabType === 'rchart1') {
        document.getElementById('right_chart1').classList.add('active');
        document.getElementById('right_chart2').classList.remove('active');
        document.getElementById('right_chart_main1').style.display = 'block';
        document.getElementById('right_chart_main2').style.display = 'none';
    } else if (tabType === 'rchart2') {
        document.getElementById('right_chart2').classList.add('active');
        document.getElementById('right_chart1').classList.remove('active');
        document.getElementById('right_chart_main2').style.display = 'block';
        document.getElementById('right_chart_main1').style.display = 'none';
    }
}

function showkos(tabType, event) {
    event.preventDefault();
    if (tabType === 'kos1') {
        document.getElementById('kospiclick').classList.add('active2');
        document.getElementById('kosdaqclick').classList.remove('active');
        document.getElementById('kospirank').style.display = 'block';
        document.getElementById('kosdaqrank').style.display = 'none';
    } else if (tabType === 'kos2') {
        document.getElementById('kosdaqclick').classList.add('active2');
        document.getElementById('kospiclick').classList.remove('active2');
        document.getElementById('kosdaqrank').style.display = 'block';
        document.getElementById('kospirank').style.display = 'none';
    }
}

// Single Bar Chart
var ctx4 = $("#bar-chart").get(0).getContext("2d");
var myChart4 = new Chart(ctx4, {
    type: "bar",
    data: {
        labels: ["Italy", "France", "Spain", "USA", "Argentina"],
        datasets: [{
            backgroundColor: [
                "rgba(0, 156, 255, .7)",
                "rgba(0, 156, 255, .6)",
                "rgba(0, 156, 255, .5)",
                "rgba(0, 156, 255, .4)",
                "rgba(0, 156, 255, .3)"
            ],
            data: [55, 49, 44, 24, 15]
        }]
    },
    options: {
        responsive: true
    }
});
var ctx4 = $("#bar-chart2").get(0).getContext("2d");
var myChart4 = new Chart(ctx4, {
    type: "bar",
    data: {
        labels: ["Italy", "France", "Spain", "USA", "Argentina"],
        datasets: [{
            backgroundColor: [
                "rgba(0, 156, 255, .7)",
                "rgba(0, 156, 255, .6)",
                "rgba(0, 156, 255, .5)",
                "rgba(0, 156, 255, .4)",
                "rgba(0, 156, 255, .3)"
            ],
            data: [55, 42, 40, 35, 15]
        }]
    },
    options: {
        responsive: true
    }
});
// Single Bar Chart
var ctx4 = $("#bar-chart3").get(0).getContext("2d");
var myChart4 = new Chart(ctx4, {
    type: "bar",
    data: {
        labels: ["Italy", "France", "Spain", "USA", "Argentina"],
        datasets: [{
            backgroundColor: [
                "rgba(0, 156, 255, .7)",
                "rgba(0, 156, 255, .6)",
                "rgba(0, 156, 255, .5)",
                "rgba(0, 156, 255, .4)",
                "rgba(0, 156, 255, .3)"
            ],
            data: [55, 49, 44, 24, 15]
        }]
    },
    options: {
        responsive: true
    }
});
// Single Bar Chart
var ctx4 = $("#bar-chart4").get(0).getContext("2d");
var myChart4 = new Chart(ctx4, {
    type: "bar",
    data: {
        labels: ["Italy", "France", "Spain", "USA", "Argentina"],
        datasets: [{
            backgroundColor: [
                "rgba(0, 156, 255, .7)",
                "rgba(0, 156, 255, .6)",
                "rgba(0, 156, 255, .5)",
                "rgba(0, 156, 255, .4)",
                "rgba(0, 156, 255, .3)"
            ],
            data: [55, 40, 36, 20, 12]
        }]
    },
    options: {
        responsive: true
    }
});