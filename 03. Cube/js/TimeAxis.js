// 主时间轴
function TimeAxis(){
    // 开始显示第一个视频
    setTimeout(function () {
        $("#Cube").show();
        document.getElementById('Page1Video').currentTime = 26;
        $("#Page1").show();
        $("#Page1").css("z-index", 10);
    }, 1000);
    // 第一个视频和第二个视频的切换
    setTimeout(function(){
        $("#Page1").addClass("rotateCubeLeftOut");
        $("#Page2").addClass("rotateCubeLeftIn");
        document.getElementById('Page2Video').currentTime = 29;
        $("#Page2").css("z-index", 5);
        $("#Page2").show();
    }, 4000);
    setTimeout(function(){
        $("#Page2").css("z-index", 20);
    }, 4600);
    setTimeout(function(){
        $("#Page1").removeClass("rotateCubeLeftOut");
        $("#Page2").removeClass("rotateCubeLeftIn");
        $("#Page1").hide();
    }, 5200);
    // 第二个视频和第三个视频的切换
    setTimeout(function(){
        $("#Page2").addClass("rotateCubeLeftOut");
        $("#Page3").addClass("rotateCubeLeftIn");
        document.getElementById('Page3Video').currentTime = 32;
        $("#Page3").css("z-index", 15);
        $("#Page3").show();
    }, 7000);
    setTimeout(function(){
        $("#Page3").css("z-index", 30);
    }, 7600);
    setTimeout(function(){
        $("#Page2").removeClass("rotateCubeLeftOut");
        $("#Page3").removeClass("rotateCubeLeftIn");
        $("#Page2").hide();
    }, 8200);
    //第三个视频和第四个视频的切换
    setTimeout(function(){
        $("#Page3").addClass("rotateCubeDownOut");
        $("#Page4").addClass("rotateCubeDownIn");
        document.getElementById('Page4Video').currentTime = 35;
        $("#Page4").css("z-index", 25);
        $("#Page4").show();
    }, 9000);
    setTimeout(function(){
        $("#Page4").css("z-index", 40);
    }, 9600);
    setTimeout(function(){
        $("#Page3").removeClass("rotateCubeDownOut");
        $("#Page4").removeClass("rotateCubeDownIn");
        $("#Page3").hide();
    }, 10200);
}

$(function(){
    TimeAxis();
})
