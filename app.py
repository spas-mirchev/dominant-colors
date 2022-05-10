import cv2
import numpy as np
from flask import Flask, render_template, redirect, flash, url_for, request 
from forms import FormUpload
import os

SECRET_KEY = os.urandom(32)

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = SECRET_KEY

app.config["IMAGE_UPLOADS"] = "/home/evgeniya/Documents/code/dominant-colors/static/uploads"


@app.route("/", methods=['GET', 'POST'])
def index(): 
    form = FormUpload()
    
    def create_bar(height, width, color):
        bar = np.zeros((height, width, 3), np.uint8)
        bar[:] = color
        red, green, blue = int(color[2]), int(color[1]), int(color[0])
        return bar, (red, green, blue)

    img = cv2.imread('static/uploads/cinema.jpg')
    height, width, _ = np.shape(img)
    print(height, width)

    data = np.reshape(img, (height * width, 3))
    data = np.float32(data)

    number_clusters = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)
    # print(centers)

    font = cv2.FONT_HERSHEY_SIMPLEX
    bars = []
    rgb_values = []

    for row in centers:
        bar, rgb = create_bar(200, 200, row)
        bars.append(bar)
        rgb_values.append(rgb)
    
    return render_template("index.html", form=form, rgb_values=rgb_values)

@app.route("/upload-image", methods=['GET', 'POST'])
def upload_image():
    form = FormUpload()
    image = request.files["image"]
    image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
    filename = f"uploads/{image.filename}"
    num_col = request.form.get('number_of_colors')
    redirect(request.url)
            
    def create_bar(height, width, color):
        bar = np.zeros((height, width, 3), np.uint8)
        bar[:] = color
        red, green, blue = int(color[2]), int(color[1]), int(color[0])
        return bar, (red, green, blue)

    img = cv2.imread('static/uploads/cinema.jpg')
    height, width, _ = np.shape(img)
    print(height, width)

    data = np.reshape(img, (height * width, 3))
    data = np.float32(data)
    
    number_clusters = int(num_col)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)
    # print(centers)

    font = cv2.FONT_HERSHEY_SIMPLEX
    bars = []
    rgb_values = []

    for row in centers:
        bar, rgb = create_bar(200, 200, row)
        bars.append(bar)
        rgb_values.append(rgb)
            
    return render_template("index.html", form=form, filename=filename, rgb_values=rgb_values)
    

if __name__ == "__main__":
    app.run(debug=True)