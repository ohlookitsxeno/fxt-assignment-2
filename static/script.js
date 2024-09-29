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
        console.log('Converging called successfully');
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