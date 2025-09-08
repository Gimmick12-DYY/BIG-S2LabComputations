"""
ADRD Metadata Analysis Platform - Web Application

This Flask application provides analysis and visualization of ADRD metadata
using the local ADRD_Metadata_YuyangD.xlsx dataset.
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
import json
from pathlib import Path
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
app.secret_key = 'adrd-research-platform-2024'  # Change in production

# Configuration
UPLOAD_FOLDER = 'uploads'
DATASETS_FOLDER = 'datasets'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv', 'json'}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATASETS_FOLDER'] = DATASETS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create directories
for folder in [UPLOAD_FOLDER, DATASETS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

class ADRDMetadataAnalyzer:
    """Analyzer for ADRD metadata dataset."""
    
    def __init__(self, excel_file_path=None):
        self.excel_file_path = excel_file_path or 'templates/ADRD_Metadata_YuyangD.xlsx'
        self.df = None
        self.analysis_results = {}
        
    def load_data(self):
        """Load the ADRD metadata from Excel file."""
        try:
            print(f"Loading ADRD metadata from: {self.excel_file_path}")
            self.df = pd.read_excel(self.excel_file_path)
            print(f"Data loaded successfully. Shape: {self.df.shape}")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def analyze_dataset_overview(self):
        """Analyze overall dataset characteristics."""
        if self.df is None:
            return None
            
        overview = {
            'total_datasets': len(self.df),
            'total_columns': len(self.df.columns),
            'columns': list(self.df.columns)
        }
        
        # Disease type analysis
        if 'Disease Type (e.g., AD, LBD, FTD, VaD, Mixed) (Text)' in self.df.columns:
            disease_types = self.df['Disease Type (e.g., AD, LBD, FTD, VaD, Mixed) (Text)'].value_counts()
            overview['disease_types'] = disease_types.to_dict()
        
        # Sample size analysis
        if 'Sample Size (Observations) (Integer)' in self.df.columns:
            sample_sizes = self.df['Sample Size (Observations) (Integer)'].dropna()
            overview['sample_size_stats'] = {
                'total_observations': sample_sizes.sum() if len(sample_sizes) > 0 else 0,
                'average_size': sample_sizes.mean() if len(sample_sizes) > 0 else 0,
                'min_size': sample_sizes.min() if len(sample_sizes) > 0 else 0,
                'max_size': sample_sizes.max() if len(sample_sizes) > 0 else 0
            }
        
        # Data availability analysis
        data_types = [
            'EHR Data Available (Text)',
            'Imaging Data Types Available (Text)',
            'SNP Genotyping Data Available (Text)',
            'WGS Data Available (Text)',
            'WES Data Available (Text)',
            'RNA-seq Data Available (Text)',
            'Proteomics Data Available (Text)',
            'Metabolomics Data Available (Text)',
            'Clinical Cognitive Tests Available (Text)',
            'Amyloid-beta Data Available (Text)',
            'Tau Data Available (Text)'
        ]
        
        data_availability = {}
        for col in data_types:
            if col in self.df.columns:
                available_count = (self.df[col].notna() & (self.df[col] != '') & (self.df[col] != 'No')).sum()
                data_availability[col.replace(' (Text)', '').replace(' Available', '')] = {
                    'available': int(available_count),
                    'total': len(self.df),
                    'percentage': round(available_count / len(self.df) * 100, 1)
                }
        
        overview['data_availability'] = data_availability
        
        return overview
    
    def analyze_disease_types(self):
        """Analyze disease type distribution."""
        if self.df is None:
            return None
            
        disease_col = 'Disease Type (e.g., AD, LBD, FTD, VaD, Mixed) (Text)'
        if disease_col not in self.df.columns:
            return None
            
        disease_analysis = {}
        disease_counts = self.df[disease_col].value_counts()
        disease_analysis['distribution'] = disease_counts.to_dict()
        
        # Analyze sample sizes by disease type
        sample_col = 'Sample Size (Observations) (Integer)'
        if sample_col in self.df.columns:
            disease_sample_sizes = {}
            for disease in disease_counts.index:
                disease_data = self.df[self.df[disease_col] == disease]
                sample_sizes = disease_data[sample_col].dropna()
                if len(sample_sizes) > 0:
                    disease_sample_sizes[disease] = {
                        'total_samples': int(sample_sizes.sum()),
                        'average_size': round(sample_sizes.mean(), 1),
                        'datasets_count': len(sample_sizes)
                    }
            disease_analysis['sample_sizes_by_disease'] = disease_sample_sizes
        
        return disease_analysis
    
    def analyze_data_types(self):
        """Analyze available data types across datasets."""
        if self.df is None:
            return None
            
        data_type_columns = {
            'Genomics': ['SNP Genotyping Data Available (Text)', 'WGS Data Available (Text)', 'WES Data Available (Text)'],
            'Transcriptomics': ['RNA-seq Data Available (Text)'],
            'Proteomics': ['Proteomics Data Available (Text)'],
            'Metabolomics': ['Metabolomics Data Available (Text)'],
            'Imaging': ['Imaging Data Types Available (Text)'],
            'Clinical': ['EHR Data Available (Text)', 'Clinical Cognitive Tests Available (Text)'],
            'Biomarkers': ['Amyloid-beta Data Available (Text)', 'Tau Data Available (Text)'],
            'Epigenomics': ['Epigenomic Data Available (Text)']
        }
        
        data_type_analysis = {}
        for category, columns in data_type_columns.items():
            available_datasets = set()
            for col in columns:
                if col in self.df.columns:
                    available = self.df[self.df[col].notna() & (self.df[col] != '') & (self.df[col] != 'No')]
                    available_datasets.update(available.index)
            
            data_type_analysis[category] = {
                'available_datasets': len(available_datasets),
                'total_datasets': len(self.df),
                'percentage': round(len(available_datasets) / len(self.df) * 100, 1)
            }
        
        return data_type_analysis
    
    def create_visualizations(self):
        """Create visualizations for the ADRD metadata."""
        if self.df is None:
            return {}
            
        plots = {}
        
        # Disease type distribution
        disease_col = 'Disease Type (e.g., AD, LBD, FTD, VaD, Mixed) (Text)'
        if disease_col in self.df.columns:
            fig, ax = plt.subplots(figsize=(12, 8))
            disease_counts = self.df[disease_col].value_counts()
            colors = plt.cm.Set3(np.linspace(0, 1, len(disease_counts)))
            bars = ax.bar(disease_counts.index, disease_counts.values, color=colors)
            ax.set_title('ADRD Dataset Distribution by Disease Type', fontsize=16, fontweight='bold')
            ax.set_xlabel('Disease Type', fontsize=12)
            ax.set_ylabel('Number of Datasets', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{int(height)}', ha='center', va='bottom')
            
            plt.tight_layout()
            plots['disease_distribution'] = self._fig_to_base64(fig)
        
        # Data availability heatmap
        data_columns = [
            'EHR Data Available (Text)',
            'Imaging Data Types Available (Text)',
            'SNP Genotyping Data Available (Text)',
            'WGS Data Available (Text)',
            'WES Data Available (Text)',
            'RNA-seq Data Available (Text)',
            'Proteomics Data Available (Text)',
            'Metabolomics Data Available (Text)',
            'Clinical Cognitive Tests Available (Text)',
            'Amyloid-beta Data Available (Text)',
            'Tau Data Available (Text)'
        ]
        
        # Create availability matrix
        availability_matrix = []
        dataset_names = []
        data_type_names = []
        
        for idx, row in self.df.iterrows():
            dataset_name = row.get('Dataset Name (Text)', f'Dataset {idx+1}')
            dataset_names.append(dataset_name)
            row_availability = []
            
            for col in data_columns:
                if col in self.df.columns:
                    value = row[col]
                    available = 1 if (pd.notna(value) and value != '' and value != 'No') else 0
                    row_availability.append(available)
                else:
                    row_availability.append(0)
            
            availability_matrix.append(row_availability)
        
        # Create data type names
        data_type_names = [col.replace(' (Text)', '').replace(' Available', '') for col in data_columns]
        
        if availability_matrix:
            fig, ax = plt.subplots(figsize=(15, 10))
            im = ax.imshow(availability_matrix, cmap='RdYlGn', aspect='auto')
            
            # Set ticks and labels
            ax.set_xticks(range(len(data_type_names)))
            ax.set_yticks(range(len(dataset_names)))
            ax.set_xticklabels(data_type_names, rotation=45, ha='right')
            ax.set_yticklabels(dataset_names)
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax)
            cbar.set_label('Data Available', rotation=270, labelpad=20)
            
            ax.set_title('Data Availability Across ADRD Datasets', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plots['data_availability_heatmap'] = self._fig_to_base64(fig)
        
        # Sample size distribution
        sample_col = 'Sample Size (Observations) (Integer)'
        if sample_col in self.df.columns:
            sample_sizes = self.df[sample_col].dropna()
            if len(sample_sizes) > 0:
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.hist(sample_sizes, bins=15, alpha=0.7, color='skyblue', edgecolor='black')
                ax.set_title('Distribution of Dataset Sample Sizes', fontsize=16, fontweight='bold')
                ax.set_xlabel('Sample Size (Observations)', fontsize=12)
                ax.set_ylabel('Number of Datasets', fontsize=12)
                ax.grid(True, alpha=0.3)
                
                # Add statistics
                mean_size = sample_sizes.mean()
                median_size = sample_sizes.median()
                ax.axvline(mean_size, color='red', linestyle='--', label=f'Mean: {mean_size:.0f}')
                ax.axvline(median_size, color='orange', linestyle='--', label=f'Median: {median_size:.0f}')
                ax.legend()
                
                plt.tight_layout()
                plots['sample_size_distribution'] = self._fig_to_base64(fig)
        
        return plots
    
    def _fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 string."""
        img = io.BytesIO()
        fig.savefig(img, format='png', dpi=300, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close(fig)
        return plot_url
    
    def get_dataset_details(self, dataset_name=None):
        """Get detailed information about specific datasets."""
        if self.df is None:
            return None
            
        if dataset_name:
            dataset_info = self.df[self.df['Dataset Name (Text)'] == dataset_name]
            if len(dataset_info) > 0:
                return dataset_info.iloc[0].to_dict()
        else:
            # Return all datasets with key information
            key_columns = [
                'Dataset Name (Text)',
                'Disease Type (e.g., AD, LBD, FTD, VaD, Mixed) (Text)',
                'Sample Size (Observations) (Integer)',
                'Sample Size (ADRD Cases, Observations) (Integer)',
                'Data Accessibility (Text)',
                'Team Member (Text)'
            ]
            
            available_columns = [col for col in key_columns if col in self.df.columns]
            return self.df[available_columns].to_dict('records')
        
        return None

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with ADRD metadata analysis interface."""
    return render_template('adrd_index.html')

@app.route('/load_data')
def load_adrd_data():
    """Load and analyze the ADRD metadata dataset."""
    try:
        analyzer = ADRDMetadataAnalyzer()
        if analyzer.load_data():
            # Perform comprehensive analysis
            overview = analyzer.analyze_dataset_overview()
            disease_analysis = analyzer.analyze_disease_types()
            data_type_analysis = analyzer.analyze_data_types()
            visualizations = analyzer.create_visualizations()
            dataset_details = analyzer.get_dataset_details()
            
            result_data = {
                'success': True,
                'overview': overview,
                'disease_analysis': disease_analysis,
                'data_type_analysis': data_type_analysis,
                'visualizations': visualizations,
                'dataset_details': dataset_details
            }
            
            return jsonify(result_data)
        else:
            return jsonify({'success': False, 'error': 'Failed to load ADRD metadata'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/dataset/<dataset_name>')
def get_dataset_info(dataset_name):
    """Get detailed information about a specific dataset."""
    try:
        analyzer = ADRDMetadataAnalyzer()
        if analyzer.load_data():
            dataset_info = analyzer.get_dataset_details(dataset_name)
            if dataset_info:
                return jsonify({'success': True, 'dataset_info': dataset_info})
            else:
                return jsonify({'success': False, 'error': 'Dataset not found'})
        else:
            return jsonify({'success': False, 'error': 'Failed to load data'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload for additional datasets."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file selected'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process uploaded file
            df = pd.read_excel(filepath)
            result_data = {
                'success': True,
                'filename': filename,
                'shape': df.shape,
                'columns': list(df.columns),
                'preview': df.head().to_dict('records')
            }
            return jsonify(result_data)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        return jsonify({'success': False, 'error': 'Invalid file type'})

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'ADRD Metadata Platform is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
