var plotDiv = document.getElementById('plotly-div');

function get_plot(){
    $.getJSON('/get_plot', function(data){
        Plotly.newPlot('plotly-div', data.data, data.layout);
    });
}

$(document).ready(function() {
    get_plot();
});

$('#gen-data').click(function() {
    var numPoints = $('#num_points').val();

    $.ajax({
        type: 'POST',
        url: '/gen_data',
        contentType: 'application/json',
        data: JSON.stringify({ num_points: numPoints }),
        success: function(r){
            console.log('generated dataset!')
        },
        error: function(r) {
            alert('Must be a positive number')
        }
    })
    get_plot();
});

$('#km-step').click(function() {
    $.post('/km_step', function(response) {
        console.log('Stepping called successfully');
    });
    get_plot();
});

$('#km-conv').click(function() {
    $.post('/km_conv', function(response) {
        console.log('Converging called successfully');
    });
    get_plot();
});

$('#km-rest').click(function() {
    $.post('/km_rest', function(response) {
        console.log('Reset called successfully');
    });

    let sel = document.getElementById('init_method').value;
    let k = document.getElementById('num_clusters').value;
    fetch(`/initialize/${sel}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ value: k })
    });

    get_plot();
});

document.getElementById('init_method').addEventListener('change', sendInit);
document.getElementById('num_clusters').addEventListener('change', sendInit);

function sendInit() {
    let sel = document.getElementById('init_method').value;
    let k = document.getElementById('num_clusters').value;

    fetch(`/initialize/${sel}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ value: k })
    });

    get_plot();
}



d3.select('#plotly-div').on('click', function(d, i) {
    console.log("click!!");

    console.log(d3.event);
    var e = d3.event;
    //using solution for finding coordinates from https://discord.com/channels/1281248353752977418/1289750019263696907/1289975646398713947
    var bgrect = document.getElementsByClassName('gridlayer')[0].getBoundingClientRect();
    var xc = ((e.x - bgrect['x']) / (bgrect['width'])) * (plotDiv.layout.xaxis.range[1] - plotDiv.layout.xaxis.range[0]) + plotDiv.layout.xaxis.range[0];
    var yc = ((e.y - bgrect['y']) / (bgrect['height'])) * (plotDiv.layout.yaxis.range[0] - plotDiv.layout.yaxis.range[1]) + plotDiv.layout.yaxis.range[1];

    console.log(xc)
    console.log(yc)
    // Send the coordinates to the backend
    fetch('/new_centroid', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ x: xc, y: yc })
    });
    get_plot();
});