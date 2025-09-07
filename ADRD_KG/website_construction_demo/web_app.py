"""
Flask Web Application for Disease Type Matrix Visualization

This web application provides a user-friendly interface to upload Excel files
and visualize disease type information as interactive matrices.

Author: Generated for BIG-S2LabComputations
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
from pathlib import Path
import json
from werkzeug.utils import secure_filename
import warnings
warnings.filterwarnings('ignore')

# Import our disease analyzer
from disease_type_info_matrix_demo import DiseaseTypeMatrixAnalyzer

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_plot_base64(fig):
    """Convert matplotlib figure to base64 string for web display."""
    img = io.BytesIO()
    fig.savefig(img, format='png', dpi=300, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)  # Close figure to free memory
    return plot_url

@app.route('/')
def index():
    """Main page with upload form."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process disease data."""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process the uploaded file
            analyzer = DiseaseTypeMatrixAnalyzer(filepath)
            if analyzer.load_data():
                # Analyze disease types
                disease_counts = analyzer.analyze_disease_types()
                matrices = analyzer.create_disease_matrix()
                
                # Create visualizations
                plots = create_web_visualizations(analyzer)
                
                # Prepare data for JSON response
                result_data = {
                    'success': True,
                    'filename': filename,
                    'disease_counts': disease_counts.to_dict() if disease_counts is not None else {},
                    'matrices': {name: matrix.to_dict() for name, matrix in matrices.items()} if matrices else {},
                    'plots': plots,
                    'summary': get_data_summary(analyzer.df)
                }
                
                return jsonify(result_data)
            else:
                return jsonify({'success': False, 'error': 'Failed to load data from file'})
                
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        return jsonify({'success': False, 'error': 'Invalid file type. Please upload Excel (.xlsx, .xls) or CSV files.'})

@app.route('/sample_data')
def generate_sample_data():
    """Generate and process sample data for demonstration."""
    try:
        # Create sample data
        analyzer = DiseaseTypeMatrixAnalyzer()
        sample_file = analyzer.create_sample_data("sample_data.xlsx")
        
        # Process the sample data
        if analyzer.load_data(sample_file):
            disease_counts = analyzer.analyze_disease_types()
            matrices = analyzer.create_disease_matrix()
            plots = create_web_visualizations(analyzer)
            
            result_data = {
                'success': True,
                'filename': 'sample_data.xlsx',
                'disease_counts': disease_counts.to_dict() if disease_counts is not None else {},
                'matrices': {name: matrix.to_dict() for name, matrix in matrices.items()} if matrices else {},
                'plots': plots,
                'summary': get_data_summary(analyzer.df)
            }
            
            return jsonify(result_data)
        else:
            return jsonify({'success': False, 'error': 'Failed to generate sample data'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def create_web_visualizations(analyzer):
    """Create visualizations suitable for web display."""
    if not analyzer.disease_matrix:
        return {}
    
    plots = {}
    
    # Set up plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    for matrix_name, matrix in analyzer.disease_matrix.items():
        # Create individual plot for each matrix
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Remove 'All' row and column for cleaner visualization
        plot_matrix = matrix.drop('All', axis=0, errors='ignore').drop('All', axis=1, errors='ignore')
        
        # Create heatmap
        sns.heatmap(plot_matrix, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_title(f'{matrix_name.replace("_", " ").title()}', fontsize=14, fontweight='bold')
        ax.set_xlabel('')
        ax.set_ylabel('')
        
        # Rotate x-axis labels for better readability
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        plt.setp(ax.get_yticklabels(), rotation=0)
        
        # Convert to base64
        plots[matrix_name] = create_plot_base64(fig)
    
    return plots

def get_data_summary(df):
    """Get summary statistics of the dataset."""
    if df is None:
        return {}
    
    summary = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns)
    }
    
    if 'Disease_Type' in df.columns:
        disease_summary = df['Disease_Type'].describe()
        summary['unique_diseases'] = int(disease_summary['unique'])
        summary['most_common_disease'] = disease_summary['top']
        summary['most_common_count'] = int(disease_summary['freq'])
    
    if 'Age' in df.columns:
        age_stats = df['Age'].describe()
        summary['age_stats'] = {
            'mean': round(age_stats['mean'], 2),
            'std': round(age_stats['std'], 2),
            'min': int(age_stats['min']),
            'max': int(age_stats['max'])
        }
    
    return summary

@app.route('/download_sample')
def download_sample():
    """Download sample Excel template."""
    try:
        analyzer = DiseaseTypeMatrixAnalyzer()
        sample_file = analyzer.create_sample_data("sample_template.xlsx")
        return send_file(sample_file, as_attachment=True, download_name='disease_data_template.xlsx')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'Disease Matrix Web App is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
