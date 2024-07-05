import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2
import numpy as np
import pytesseract
import os
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# You can choose other styles like "darkgrid", "white", "ticks"
sns.set(style="whitegrid")

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'],verbose = False)

# Streamlit app title
st.title("Document Information Extraction Using OCR")


# File uploader for refrence image
refrence_image = st.file_uploader(
    "Choose refrence image", type=["jpg", "jpeg", "png"])

# File uploader for data extraction
uploaded_files = st.file_uploader("Choose images for data extraction", type=[
                                  "jpg", "jpeg", "png"], accept_multiple_files=True)


# Sidebar heading
st.sidebar.title("Data Visualization Tools")


# Checkbox to control plot display
show_plot = st.sidebar.checkbox("Add Plot")
# Checkbox to control CSV file display
hide_csv = st.sidebar.checkbox("Hide csv")
# Checkbox to control refrence image display
display_refrence = st.sidebar.checkbox("Display refrence image")


# Function to generate plot
def generate_plot(plot_type, data):
    if plot_type == "Bar Plot":
        column = st.sidebar.selectbox(
            "Select column for Bar Plot", data.columns)
        fig, ax = plt.subplots()
        sns.barplot(x=data[column].value_counts(
        ).index, y=data[column].value_counts().values, palette="viridis", ax=ax)
        ax.set_title(f"{column}", fontsize=16)
        ax.set_xlabel(column, fontsize=14)
        ax.set_ylabel('Count', fontsize=14)
        plot_placeholder.pyplot(fig)
        return fig
    elif plot_type == "Histogram":
        column = st.sidebar.selectbox(
            "Select column for Histogram", data.columns)
        fig, ax = plt.subplots()
        sns.histplot(data[column], bins=20, kde=True, color="skyblue", ax=ax)
        ax.set_title(f"{column}", fontsize=16)
        ax.set_xlabel(column, fontsize=14)
        ax.set_ylabel('Frequency', fontsize=14)
        plot_placeholder.pyplot(fig)
        return fig
    elif plot_type == "Pie Chart":
        column = st.sidebar.selectbox(
            "Select column for Pie Chart", data.columns)
        fig, ax = plt.subplots()
        data[column].value_counts().plot(kind='pie', autopct='%1.1f%%',
                                         colors=sns.color_palette("viridis"), ax=ax)
        ax.set_title(f"{column}", fontsize=16)
        ax.set_ylabel('')
        plot_placeholder.pyplot(fig)
        return fig
    else:
        return None


def save_plot(fig):
    bytes_io = io.BytesIO()
    fig.savefig(bytes_io, format='png')
    return bytes_io


# Sidebar options for plot selection
plot_type = st.sidebar.selectbox(
    "Select plot type", ["Bar Plot", "Histogram", "Pie Chart"])

# Placeholder for the plots
plot_placeholder = st.empty()


# Function to process images and extract data
def process_images(files, refrence_image):
    per = 25
    pixelThreshold = 500
    roi = [[(300, 265), (590, 308), 'text', 'Name'],
           [(593, 315), (823, 372), 'text', 'Date of Birth'],
           [(277, 494), (769, 590), 'text', 'Aadhar Number'],
           [(288, 373), (421, 427), 'text', 'Gender']]

    # path_TO_Main = refrence_image
    # imgQ = cv2.imread(path_TO_Main)

    # Convert the BytesIO object to a numpy array
    file_bytes = np.asarray(bytearray(refrence_image.read()), dtype=np.uint8)

    # Read the image using OpenCV
    imgQ = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    h, w, c = imgQ.shape

    akaze = cv2.AKAZE_create(threshold=0.001)
    kp1, des1 = akaze.detectAndCompute(imgQ, None)  

    myData = []

    for j, file in enumerate(files):
        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), 1)
        kp2, des2 = akaze.detectAndCompute(img, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.match(des2, des1)
        matches = sorted(matches,key=lambda x : x.distance)
        good = matches[:int(len(matches)*(per/100))]
        srcPoints = np.float32(
            [kp2[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dstPoints = np.float32(
            [kp1[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)
        imgScan = cv2.warpPerspective(img, M, (w, h))

        imgShow = imgScan.copy()
        imgMask = np.zeros_like(imgShow)

        data_dict = {}
        print(f'Extracting data from form {j}')
        for x, r in enumerate(roi):
            cv2.rectangle(imgMask, (r[0][0], r[0][1]),
                          (r[1][0], r[1][1]), (0, 255, 0), cv2.FILLED)
            imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 0.1, 0)
            imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]

            if r[2] == 'text':
                results = reader.readtext(imgCrop)
                extracted_text = " ".join([result[1] for result in results])
                print(extracted_text)
                data_dict[r[3]] = extracted_text
            if r[2] == 'box':
                imgGray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)
                imgThresh = cv2.threshold(
                    imgGray, 170, 255, cv2.THRESH_BINARY_INV)[1]
                totalPixels = cv2.countNonZero(imgThresh)
                totalPixels = 1 if totalPixels > pixelThreshold else 0
                print(f'{r[3]} : {totalPixels}')
                data_dict[r[3]] = totalPixels

        myData.append(data_dict)

    return myData


if uploaded_files and refrence_image:
    st.write(f"Uploaded {len(uploaded_files)} files.")

    # Process images and extract data
    data = process_images(uploaded_files, refrence_image)

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    if not hide_csv:
        st.markdown(
            "<h2 style='text-align: center; color: white; font-size: 24px;'>Extracted data</h2>", unsafe_allow_html=True)
        # Display the DataFrame
        st.dataframe(df, width=1000)  # Adjust the width as per your preference

    # Save DataFrame to CSV
    csv = df.to_csv(index=False)

    # Download link for CSV
    st.download_button(label="Download data as CSV", data=csv,
                       file_name='extracted_data.csv', mime='text/csv')


    #Conditional check for displaying refrence image
    if display_refrence:
      st.markdown("<h2 style='text-align: center; color: white; font-size: 24px;'>Refrence Image</h2>", unsafe_allow_html=True)
      # Use PIL to open the image
      image = Image.open(refrence_image)
      # Convert image to numpy array for display (optional)
      img_array = np.array(image)
      # Display the image
      st.image(image, caption='Uploaded Image', use_column_width=True)
    # Conditional plot display based on checkbox
    if show_plot:
        st.markdown(
            "<h2 style='text-align: center; color: white; font-size: 24px;'>Generated Plot</h2>", unsafe_allow_html=True)
        # Plot placeholder
        plot_placeholder = st.empty()
        # Generate the selected plot
        fig = generate_plot(plot_type, df)

        # Save plot as bytes and provide download button
        plot_bytes = save_plot(fig)
        # Download button for plot
        st.download_button(label="Download Plot", data=plot_bytes.getvalue(
        ), file_name='plot.png', mime='image/png')
