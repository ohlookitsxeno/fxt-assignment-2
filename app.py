from flask import Flask, render_template, request, redirect, jsonify, url_for, send_file
import plotly.graph_objs as go
import plotly
import io
import json
import kmeans as km
import matplotlib.pyplot as plt
import matplotlib.colors as mcol

app = Flask(__name__)

points = km.generate_dataset(128)

centroids = km.init_random(points, 4)
manual = False

def colors(col):
    maxcol = float(max(col))
    
    cmap = plt.cm.get_cmap('gist_rainbow')

    newcol = []
    for c in col:
        if c == -1:
            newcol.append('black')
        elif maxcol == 0:
            newcol.append(mcol.to_hex(cmap(0)))
        else:
            newcol.append(mcol.to_hex(cmap(c/maxcol)))
    return newcol

def plotter():
    px, py, pcol = zip(*points)

    cols = colors(pcol)

    points_trace = go.Scatter(
        x=px,
        y=py,
        mode='markers',
        marker=dict(color=cols, size=8, line=dict(width=2, color='#444444')),
        name='Points'
    )
    data = [points_trace]

    if len(centroids) > 0:
        ccols = colors(range(len(centroids)))

        centroids_trace = go.Scatter(
            x=[c[0] for c in centroids],
            y=[c[1] for c in centroids],
            mode='markers',
            marker=dict(color=ccols, size=16, symbol='x', line=dict(width=2, color='#444444')),
            name='Centroids'
        )
    
    
        data = [points_trace, centroids_trace]

    layout = go.Layout(
        title="KMeans Clusturing",
        xaxis=dict(range=[-10, 10], title='X-axis'),
        yaxis=dict(range=[-10, 10], title='Y-axis'),
        showlegend=True
    )

    return jsonify({'data': [trace.to_plotly_json() for trace in data], 'layout': layout.to_plotly_json()})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initialize/<method>', methods=['POST'])
def init(method):
    global centroids, manual
    print("meow")
    manual = False
    data = request.get_json()
    k = int(data.get('value', 4))
    if method == 'initrandom':
        centroids = km.init_random(points, k)
    if method == 'initfarthest':
        centroids = km.init_far(points, k)
    if method == 'initkmeans':
        centroids = km.init_kmeans(points, k)
    if method == 'initmanual':
        manual = True
        centroids = []
    return jsonify({'status': 'success'})

@app.route('/km_step', methods=['POST'])
def step():
    global points
    global centroids
    points = km.step_points(points, centroids)
    centroids = km.step_centroids(points, centroids)
    print("meo3")
    return jsonify({'status': 'success'})

@app.route('/km_conv', methods=['POST'])
def conv():
    step()
    global points, centroids
    verg = False
    while not verg:
        newpoints = km.step_points(points, centroids)
        newcentroids = km.step_centroids(points, centroids)
        pverg = cverg = True
        for p in range(len(newpoints)):
            if newpoints[p][2] != points[p][2]:
                pverg = False 
        for c in range(len(newcentroids)):
            if newcentroids[c][0] != centroids[c][0] or newcentroids[c][1] != centroids[c][1]:
                cverg = False
        points = newpoints
        centroids = newcentroids
        if pverg and cverg:
            verg = True
    return jsonify({'status': 'success'})

@app.route('/km_rest', methods=['POST'])
def rest():
    global points
    points = km.reset_points(points)
    return jsonify({'status': 'success'})

@app.route('/get_plot')
def plotimg():
    print("meow")
    return plotter()

@app.route('/new_centroid', methods=['POST'])
def new_cent():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    if manual:
        centroids.append((x,y,-1))
    return jsonify({'status': 'success'})

@app.route('/gen_data', methods=['POST'])
def regen_data():
    global points
    try:
        data = request.get_json()
        numpoints = int(data['num_points'])
        if numpoints < 1:
            raise ValueError
    except (ValueError, KeyError):
        return jsonify({'status': 'error', 'message': 'Invalid point count!'})
    
    points = km.generate_dataset(numpoints)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(port=3000, debug=True)