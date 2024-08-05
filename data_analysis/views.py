# data_analysis/views.py

import pandas as pd
import numpy as np  # Add this import
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.conf import settings
import os
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from django.urls import reverse

def home(request):
    return redirect(reverse('upload_file'))

def handle_uploaded_file(f):
    # Ensure the media directory exists
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    file_path = os.path.join(settings.MEDIA_ROOT, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = handle_uploaded_file(request.FILES['file'])
            return analyze_file(request, file_path)
    else:
        form = UploadFileForm()
    return render(request, 'data_analysis/upload.html', {'form': form})

def analyze_file(request, file_path):
    df = pd.read_csv(file_path)

    # Display the first few rows
    first_rows = df.head()

    # Summary statistics
    summary_stats = df.describe()

    # Handling missing values
    missing_values = df.isnull().sum()

    # Data visualization
    plt.figure(figsize=(10, 6))
    histograms = {}
    for column in df.select_dtypes(include=[np.number]).columns:
        plt.figure()
        sns.histplot(df[column].dropna(), kde=True)
        plt.title(f'Histogram for {column}')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        histograms[column] = base64.b64encode(buf.getvalue()).decode('utf-8')

    context = {
        'first_rows': first_rows.to_html(),
        'summary_stats': summary_stats.to_html(),
        'missing_values': missing_values.to_string(),
        'histograms': histograms
    }
    return render(request, 'data_analysis/results.html', context)
