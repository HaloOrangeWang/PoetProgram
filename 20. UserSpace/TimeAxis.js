aa = 3;

window.onload = function(){
    setTimeout(TimeAxis(), 2000);
};

function TimeAxis() {
    let frame_it = 0;
    setInterval(function(){
        if (frame_it <= 124){
            for(let t = 1; t <= 15; t++){
                document.getElementById('GGGGG_' + t).src = "output/" + frame_it + "/img_" + parseInt((t - 1) / 5) + '_' + ((t - 1) % 5) + '.png';
                // $('GGGGG_' + t).show();
            }
        }
        frame_it += 1;
    }, 500);
}