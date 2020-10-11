let csv_data = [];

$("#inputfile").change(function () {
    $("#inputfile").attr("hidden", true);
    let r = new FileReader();
    r.readAsText(this.files[0], 'UTF-8');
    r.onload = function() {
        // 1.读取csv文件
        let lines = this.result.split("\n");
        let frame_old = -1;
        for (let t = 0; t <= lines.length - 1; t++){
            let data_1line = lines[t].split(",");
            let frame_id = parseInt(data_1line[0]);
            let row = parseInt(data_1line[1]);
            let col = parseInt(data_1line[2]);
            if (frame_id > frame_old){
                csv_data.push([]);
                csv_data[csv_data.length - 1].push([row, col]);
                frame_old = frame_id;
            }else{
                csv_data[csv_data.length - 1].push([row, col]);
            }
        }
        // 2.准备开始显示散点图
        setTimeout(showScatter(), 1200);
    }
});

function getScatter1Frame(frame_id){
    let scatter_data = [];
    if (frame_id % 2 === 0){
        for (let t = 0; t <= csv_data[frame_id].length - 1; t++){
            const x = csv_data[frame_id][t][1];
            const y = 720 - csv_data[frame_id][t][0];
            scatter_data.push([x, y]);
        }
    }else{
        for (let t = csv_data[frame_id].length - 1; t >= 0; t--) {
            const x = csv_data[frame_id][t][1];
            const y = 720 - csv_data[frame_id][t][0];
            scatter_data.push([x, y]);
        }
    }
    return scatter_data;
}

function showScatter(){
    $("#main").show();
    let mainchart = echarts.init(document.getElementById("main"));
    let frame_id = 0;
    let chart_config = {
        title: {
            text: 'Yil'
        },
        tooltip: {},
        legend: {
            data: ['pass']
        },
        xAxis: {
            min: 0,
            max: 1280
        },
        yAxis: {
            min: 0,
            max: 720
        },
        series: [{
            name: 'value',
            type: 'scatter',
            data: getScatter1Frame(frame_id),
            symbolSize: 7,
            itemStyle: {
                normal:{
                    color: 'green'
                }
            }
        }]
    };
    mainchart.setOption(chart_config);
    setInterval(function(){
        frame_id = frame_id + 1;
        if (frame_id < csv_data.length) {
            chart_config.series[0].data = getScatter1Frame(frame_id);
            mainchart.setOption(chart_config);
        }
    }, 3000);
}