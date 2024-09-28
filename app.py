from flask import Flask, render_template, request, jsonify, send_file
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

points = []

def plotter():
    plt.figure(figsize=(8,8))
    
    
    if len(points) > 0:
        x, y = zip(*points)
        plt.scatter(x, y)

    plt.xlim(-10,10)
    plt.ylim(-10,10)
    plt.title("Kmeans Clustering")

    pimg = io.BytesIO()
    plt.savefig(pimg, format='png')
    pimg.seek(0)
    return pimg



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot.png')
def plotimg():
    return send_file(plotter(), mimetype='image/png')

if __name__ == '__main__':
    app.run(port=3000, debug=True)