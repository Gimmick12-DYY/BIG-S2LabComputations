"""
Alzheimer's Disease Research Platform - Enhanced Web Application

This Flask application provides a comprehensive platform for managing,
analyzing, and visualizing Alzheimer's disease datasets with specialized
features for AD research.

Author: Generated for BIG-S2LabComputations
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import io
import base64
import os
import json
from pathlib import Path
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import our disease analyzer
from disease_type_info_matrix_demo import DiseaseTypeMatrixAnalyzer

app = Flask(__name__)
app.secret_key = 'alzheimers-research-platform-2024'  # Change in production

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

class AlzheimersDataAnalyzer(DiseaseTypeMatrixAnalyzer):
    """Enhanced analyzer specifically for Alzheimer's disease data."""
    
    def __init__(self, excel_file_path=None):
        super().__init__(excel_file_path)
        self.ad_specific_columns = {
            'mmse_score': ['MMSE', 'mmse', 'MMSE_Score', 'Mini_Mental_State'],
            'cdr_score': ['CDR', 'cdr', 'CDR_Score', 'Clinical_Dementia_Rating'],
            'adas_cog': ['ADAS_Cog', 'adas_cog', 'ADAS_Cognitive'],
            'age': ['Age', 'age', 'AGE', 'Patient_Age'],
            'gender': ['Gender', 'gender', 'Sex', 'sex'],
            'education': ['Education', 'education', 'Years_Education', 'Edu_Years'],
            'apoe_genotype': ['APOE', 'apoe', 'APOE_Genotype', 'ApoE'],
            'csf_abeta': ['CSF_ABeta', 'csf_abeta', 'ABeta42', 'Aβ42'],
            'csf_tau': ['CSF_Tau', 'csf_tau', 'Total_Tau', 't-tau'],
            'csf_ptau': ['CSF_PTau', 'csf_ptau', 'Phospho_Tau', 'p-tau'],
            'diagnosis': ['Diagnosis', 'diagnosis', 'DX', 'Clinical_Diagnosis']
        }
    
    def create_ad_sample_data(self, output_file="ad_sample_data.xlsx"):
        """Create sample Alzheimer's disease data."""
        print("Creating sample Alzheimer's disease data...")
        
        np.random.seed(42)  # For reproducible results
        
        # Sample AD data with realistic distributions
        n_patients = 200
        
        # Generate realistic AD data
        sample_data = {
            'Patient_ID': [f'AD{i:04d}' for i in range(1, n_patients + 1)],
            'Age': np.random.normal(75, 8, n_patients).astype(int),
            'Gender': np.random.choice(['Male', 'Female'], n_patients, p=[0.4, 0.6]),
            'Education_Years': np.random.normal(14, 3, n_patients).astype(int),
            'MMSE_Score': np.random.normal(20, 8, n_patients).astype(int),
            'CDR_Score': np.random.choice([0, 0.5, 1, 2, 3], n_patients, p=[0.1, 0.2, 0.3, 0.3, 0.1]),
            'ADAS_Cog_Score': np.random.normal(15, 8, n_patients).astype(int),
            'APOE_Genotype': np.random.choice(['ε3/ε3', 'ε3/ε4', 'ε4/ε4', 'ε2/ε3', 'ε2/ε4'], 
                                            n_patients, p=[0.6, 0.25, 0.1, 0.03, 0.02]),
            'CSF_ABeta42': np.random.normal(600, 200, n_patients).astype(int),
            'CSF_Total_Tau': np.random.normal(400, 150, n_patients).astype(int),
            'CSF_Phospho_Tau': np.random.normal(60, 25, n_patients).astype(int),
            'Clinical_Diagnosis': np.random.choice(['CN', 'MCI', 'AD'], n_patients, p=[0.3, 0.4, 0.3]),
            'Disease_Stage': np.random.choice(['Preclinical', 'MCI', 'Mild_AD', 'Moderate_AD', 'Severe_AD'], 
                                            n_patients, p=[0.1, 0.3, 0.3, 0.2, 0.1]),
            'Family_History': np.random.choice(['Yes', 'No'], n_patients, p=[0.4, 0.6]),
            'Onset_Age': np.random.normal(70, 10, n_patients).astype(int),
            'Disease_Duration': np.random.normal(5, 3, n_patients).astype(int),
            'Medication': np.random.choice(['Donepezil', 'Rivastigmine', 'Galantamine', 'Memantine', 'None'], 
                                         n_patients, p=[0.3, 0.2, 0.1, 0.2, 0.2]),
            'Visit_Date': [(datetime.now() - timedelta(days=np.random.randint(0, 365*3))).strftime('%Y-%m-%d') 
                          for _ in range(n_patients)]
        }
        
        # Ensure realistic ranges
        sample_data['MMSE_Score'] = np.clip(sample_data['MMSE_Score'], 0, 30)
        sample_data['ADAS_Cog_Score'] = np.clip(sample_data['ADAS_Cog_Score'], 0, 70)
        sample_data['Age'] = np.clip(sample_data['Age'], 50, 95)
        sample_data['Education_Years'] = np.clip(sample_data['Education_Years'], 0, 25)
        
        self.df = pd.DataFrame(sample_data)
        
        # Save to Excel
        output_path = Path(self.excel_file_path).parent / output_file if self.excel_file_path else output_file
        self.df.to_excel(output_path, index=False)
        print(f"Sample AD data saved to: {output_path}")
        
        return output_path
    
    def analyze_ad_biomarkers(self):
        """Analyze Alzheimer's disease biomarkers."""
        if self.df is None:
            return None
        
        biomarker_analysis = {}
        
        # CSF Biomarker Analysis
        if 'CSF_ABeta42' in self.df.columns:
            biomarker_analysis['CSF_ABeta42'] = {
                'mean': self.df['CSF_ABeta42'].mean(),
                'std': self.df['CSF_ABeta42'].std(),
                'cutoff_192': (self.df['CSF_ABeta42'] < 192).sum(),
                'cutoff_500': (self.df['CSF_ABeta42'] < 500).sum()
            }
        
        if 'CSF_Total_Tau' in self.df.columns:
            biomarker_analysis['CSF_Total_Tau'] = {
                'mean': self.df['CSF_Total_Tau'].mean(),
                'std': self.df['CSF_Total_Tau'].std(),
                'cutoff_375': (self.df['CSF_Total_Tau'] > 375).sum()
            }
        
        # APOE Analysis
        if 'APOE_Genotype' in self.df.columns:
            apoe_counts = self.df['APOE_Genotype'].value_counts()
            biomarker_analysis['APOE_Distribution'] = apoe_counts.to_dict()
            biomarker_analysis['APOE4_Carriers'] = (self.df['APOE_Genotype'].str.contains('ε4')).sum()
        
        return biomarker_analysis
    
    def create_ad_visualizations(self):
        """Create Alzheimer's-specific visualizations."""
        if self.df is None:
            return {}
        
        plots = {}
        
        # MMSE Score Distribution
        if 'MMSE_Score' in self.df.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(self.df['MMSE_Score'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            ax.axvline(24, color='red', linestyle='--', label='Normal (≥24)')
            ax.axvline(18, color='orange', linestyle='--', label='Mild Dementia (18-23)')
            ax.axvline(12, color='red', linestyle='--', label='Moderate Dementia (12-17)')
            ax.set_xlabel('MMSE Score')
            ax.set_ylabel('Frequency')
            ax.set_title('MMSE Score Distribution')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plots['mmse_distribution'] = self._fig_to_base64(fig)
        
        # CDR Score Distribution
        if 'CDR_Score' in self.df.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            cdr_counts = self.df['CDR_Score'].value_counts().sort_index()
            bars = ax.bar(cdr_counts.index, cdr_counts.values, color=['green', 'yellow', 'orange', 'red', 'darkred'])
            ax.set_xlabel('CDR Score')
            ax.set_ylabel('Number of Patients')
            ax.set_title('Clinical Dementia Rating (CDR) Distribution')
            ax.set_xticks([0, 0.5, 1, 2, 3])
            ax.set_xticklabels(['0 (Normal)', '0.5 (Questionable)', '1 (Mild)', '2 (Moderate)', '3 (Severe)'])
            ax.grid(True, alpha=0.3)
            plots['cdr_distribution'] = self._fig_to_base64(fig)
        
        # Biomarker Scatter Plot
        if 'CSF_ABeta42' in self.df.columns and 'CSF_Total_Tau' in self.df.columns:
            fig, ax = plt.subplots(figsize=(10, 8))
            scatter = ax.scatter(self.df['CSF_ABeta42'], self.df['CSF_Total_Tau'], 
                               c=self.df['MMSE_Score'] if 'MMSE_Score' in self.df.columns else 'blue',
                               cmap='viridis', alpha=0.6)
            ax.axvline(192, color='red', linestyle='--', alpha=0.7, label='Aβ42 cutoff (192 pg/mL)')
            ax.axhline(375, color='red', linestyle='--', alpha=0.7, label='Tau cutoff (375 pg/mL)')
            ax.set_xlabel('CSF Aβ42 (pg/mL)')
            ax.set_ylabel('CSF Total Tau (pg/mL)')
            ax.set_title('CSF Biomarkers: Aβ42 vs Total Tau')
            ax.legend()
            ax.grid(True, alpha=0.3)
            if 'MMSE_Score' in self.df.columns:
                plt.colorbar(scatter, label='MMSE Score')
            plots['biomarker_scatter'] = self._fig_to_base64(fig)
        
        # Disease Stage Progression
        if 'Disease_Stage' in self.df.columns and 'Age' in self.df.columns:
            fig, ax = plt.subplots(figsize=(12, 6))
            stage_order = ['Preclinical', 'MCI', 'Mild_AD', 'Moderate_AD', 'Severe_AD']
            stage_data = [self.df[self.df['Disease_Stage'] == stage]['Age'] for stage in stage_order]
            box_plot = ax.boxplot(stage_data, labels=stage_order, patch_artist=True)
            colors = ['lightgreen', 'yellow', 'orange', 'red', 'darkred']
            for patch, color in zip(box_plot['boxes'], colors):
                patch.set_facecolor(color)
            ax.set_xlabel('Disease Stage')
            ax.set_ylabel('Age (years)')
            ax.set_title('Age Distribution by Disease Stage')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plots['stage_age_boxplot'] = self._fig_to_base64(fig)
        
        return plots
    
    def _fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 string."""
        img = io.BytesIO()
        fig.savefig(img, format='png', dpi=300, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close(fig)
        return plot_url

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with AD-specific interface."""
    return render_template('alzheimers_index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process AD data."""
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
            # Process with AD-specific analyzer
            analyzer = AlzheimersDataAnalyzer(filepath)
            if analyzer.load_data():
                # Analyze AD-specific data
                disease_counts = analyzer.analyze_disease_types()
                matrices = analyzer.create_disease_matrix()
                biomarker_analysis = analyzer.analyze_ad_biomarkers()
                ad_plots = analyzer.create_ad_visualizations()
                
                # Prepare comprehensive result data
                result_data = {
                    'success': True,
                    'filename': filename,
                    'disease_counts': disease_counts.to_dict() if disease_counts is not None else {},
                    'matrices': {name: matrix.to_dict() for name, matrix in matrices.items()} if matrices else {},
                    'biomarker_analysis': biomarker_analysis,
                    'ad_visualizations': ad_plots,
                    'summary': get_ad_data_summary(analyzer.df)
                }
                
                return jsonify(result_data)
            else:
                return jsonify({'success': False, 'error': 'Failed to load data from file'})
                
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        return jsonify({'success': False, 'error': 'Invalid file type. Please upload Excel (.xlsx, .xls), CSV, or JSON files.'})

@app.route('/sample_data')
def generate_ad_sample_data():
    """Generate and process AD sample data."""
    try:
        analyzer = AlzheimersDataAnalyzer()
        sample_file = analyzer.create_ad_sample_data("ad_sample_data.xlsx")
        
        if analyzer.load_data(sample_file):
            disease_counts = analyzer.analyze_disease_types()
            matrices = analyzer.create_disease_matrix()
            biomarker_analysis = analyzer.analyze_ad_biomarkers()
            ad_plots = analyzer.create_ad_visualizations()
            
            result_data = {
                'success': True,
                'filename': 'ad_sample_data.xlsx',
                'disease_counts': disease_counts.to_dict() if disease_counts is not None else {},
                'matrices': {name: matrix.to_dict() for name, matrix in matrices.items()} if matrices else {},
                'biomarker_analysis': biomarker_analysis,
                'ad_visualizations': ad_plots,
                'summary': get_ad_data_summary(analyzer.df)
            }
            
            return jsonify(result_data)
        else:
            return jsonify({'success': False, 'error': 'Failed to generate AD sample data'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def get_ad_data_summary(df):
    """Get AD-specific summary statistics."""
    if df is None:
        return {}
    
    summary = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns)
    }
    
    # AD-specific statistics
    if 'MMSE_Score' in df.columns:
        mmse_stats = df['MMSE_Score'].describe()
        summary['mmse_stats'] = {
            'mean': round(mmse_stats['mean'], 2),
            'std': round(mmse_stats['std'], 2),
            'min': int(mmse_stats['min']),
            'max': int(mmse_stats['max']),
            'normal_count': int((df['MMSE_Score'] >= 24).sum()),
            'mild_dementia_count': int(((df['MMSE_Score'] >= 18) & (df['MMSE_Score'] < 24)).sum()),
            'moderate_dementia_count': int(((df['MMSE_Score'] >= 12) & (df['MMSE_Score'] < 18)).sum()),
            'severe_dementia_count': int((df['MMSE_Score'] < 12).sum())
        }
    
    if 'CDR_Score' in df.columns:
        cdr_dist = df['CDR_Score'].value_counts().to_dict()
        summary['cdr_distribution'] = cdr_dist
    
    if 'APOE_Genotype' in df.columns:
        apoe_dist = df['APOE_Genotype'].value_counts().to_dict()
        summary['apoe_distribution'] = apoe_dist
        summary['apoe4_carriers'] = int((df['APOE_Genotype'].str.contains('ε4', na=False)).sum())
    
    if 'Clinical_Diagnosis' in df.columns:
        diagnosis_dist = df['Clinical_Diagnosis'].value_counts().to_dict()
        summary['diagnosis_distribution'] = diagnosis_dist
    
    return summary

@app.route('/download_template')
def download_ad_template():
    """Download AD-specific Excel template."""
    try:
        analyzer = AlzheimersDataAnalyzer()
        sample_file = analyzer.create_ad_sample_data("ad_template.xlsx")
        return send_file(sample_file, as_attachment=True, download_name='alzheimers_data_template.xlsx')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/datasets')
def datasets_catalog():
    """Dataset catalog page."""
    return render_template('datasets_catalog.html')

@app.route('/analytics')
def analytics_dashboard():
    """Advanced analytics dashboard."""
    return render_template('analytics_dashboard.html')

@app.route('/research_tools')
def research_tools():
    """Research tools and utilities."""
    return render_template('research_tools.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
