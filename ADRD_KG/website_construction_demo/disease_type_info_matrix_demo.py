"""
Disease Type Information Matrix Demo

This script reads disease information from an Excel file and displays
the types of diseases available as a matrix visualization.

Author: Generated for BIG-S2LabComputations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class DiseaseTypeMatrixAnalyzer:
    """
    A class to analyze and visualize disease type information from Excel files.
    """
    
    def __init__(self, excel_file_path=None):
        """
        Initialize the analyzer with an Excel file path.
        
        Args:
            excel_file_path (str): Path to the Excel file containing disease data
        """
        self.excel_file_path = excel_file_path
        self.df = None
        self.disease_matrix = None
        
    def create_sample_data(self, output_file="sample_disease_data.xlsx"):
        """
        Create sample disease data for demonstration purposes.
        
        Args:
            output_file (str): Name of the output Excel file
        """
        print("Creating sample disease data...")
        
        # Sample disease data
        sample_data = {
            'Patient_ID': [f'P{i:03d}' for i in range(1, 101)],
            'Age': np.random.randint(20, 90, 100),
            'Gender': np.random.choice(['Male', 'Female'], 100),
            'Disease_Type': np.random.choice([
                'Alzheimer\'s Disease', 'Parkinson\'s Disease', 'Dementia', 
                'Multiple Sclerosis', 'Epilepsy', 'Migraine', 'Stroke',
                'Huntington\'s Disease', 'ALS', 'Depression'
            ], 100),
            'Severity': np.random.choice(['Mild', 'Moderate', 'Severe'], 100),
            'Onset_Age': np.random.randint(30, 80, 100),
            'Family_History': np.random.choice(['Yes', 'No'], 100),
            'Treatment_Status': np.random.choice(['Active', 'Inactive', 'Unknown'], 100)
        }
        
        # Create DataFrame
        self.df = pd.DataFrame(sample_data)
        
        # Save to Excel
        output_path = Path(self.excel_file_path).parent / output_file if self.excel_file_path else output_file
        self.df.to_excel(output_path, index=False)
        print(f"Sample data saved to: {output_path}")
        
        return output_path
    
    def load_data(self, excel_file_path=None):
        """
        Load disease data from Excel file.
        
        Args:
            excel_file_path (str): Path to the Excel file
        """
        if excel_file_path:
            self.excel_file_path = excel_file_path
            
        if not self.excel_file_path:
            raise ValueError("No Excel file path provided")
            
        try:
            print(f"Loading data from: {self.excel_file_path}")
            self.df = pd.read_excel(self.excel_file_path)
            print(f"Data loaded successfully. Shape: {self.df.shape}")
            print(f"Columns: {list(self.df.columns)}")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def analyze_disease_types(self):
        """
        Analyze the disease types in the dataset and create a matrix.
        """
        if self.df is None:
            print("No data loaded. Please load data first.")
            return None
            
        print("\n=== Disease Type Analysis ===")
        
        # Basic statistics
        if 'Disease_Type' in self.df.columns:
            disease_counts = self.df['Disease_Type'].value_counts()
            print(f"\nDisease Type Distribution:")
            print(disease_counts)
            
            # Create disease type matrix
            self.create_disease_matrix()
            
            return disease_counts
        else:
            print("No 'Disease_Type' column found in the data.")
            return None
    
    def create_disease_matrix(self):
        """
        Create a matrix showing relationships between different disease attributes.
        """
        if self.df is None:
            return None
            
        print("\n=== Creating Disease Type Matrix ===")
        
        # Create cross-tabulation matrices
        matrices = {}
        
        # Disease Type vs Severity
        if 'Disease_Type' in self.df.columns and 'Severity' in self.df.columns:
            matrices['Disease_vs_Severity'] = pd.crosstab(
                self.df['Disease_Type'], 
                self.df['Severity'], 
                margins=True
            )
        
        # Disease Type vs Gender
        if 'Disease_Type' in self.df.columns and 'Gender' in self.df.columns:
            matrices['Disease_vs_Gender'] = pd.crosstab(
                self.df['Disease_Type'], 
                self.df['Gender'], 
                margins=True
            )
        
        # Disease Type vs Family History
        if 'Disease_Type' in self.df.columns and 'Family_History' in self.df.columns:
            matrices['Disease_vs_Family_History'] = pd.crosstab(
                self.df['Disease_Type'], 
                self.df['Family_History'], 
                margins=True
            )
        
        # Disease Type vs Treatment Status
        if 'Disease_Type' in self.df.columns and 'Treatment_Status' in self.df.columns:
            matrices['Disease_vs_Treatment'] = pd.crosstab(
                self.df['Disease_Type'], 
                self.df['Treatment_Status'], 
                margins=True
            )
        
        self.disease_matrix = matrices
        return matrices
    
    def display_matrices(self):
        """
        Display all created matrices in a formatted way.
        """
        if not self.disease_matrix:
            print("No matrices created. Run create_disease_matrix() first.")
            return
            
        print("\n" + "="*60)
        print("DISEASE TYPE INFORMATION MATRICES")
        print("="*60)
        
        for matrix_name, matrix in self.disease_matrix.items():
            print(f"\n{'-'*40}")
            print(f"Matrix: {matrix_name.replace('_', ' ').title()}")
            print(f"{'-'*40}")
            print(matrix)
            print()
    
    def visualize_matrices(self, save_plots=True):
        """
        Create visualizations of the disease type matrices.
        
        Args:
            save_plots (bool): Whether to save plots to files
        """
        if not self.disease_matrix:
            print("No matrices created. Run create_disease_matrix() first.")
            return
            
        print("\n=== Creating Visualizations ===")
        
        # Set up the plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Calculate number of subplots needed
        num_matrices = len(self.disease_matrix)
        cols = 2
        rows = (num_matrices + 1) // 2
        
        fig, axes = plt.subplots(rows, cols, figsize=(15, 5*rows))
        if num_matrices == 1:
            axes = [axes]
        elif rows == 1:
            axes = axes.reshape(1, -1)
        
        # Flatten axes for easier indexing
        axes_flat = axes.flatten() if num_matrices > 1 else [axes]
        
        for idx, (matrix_name, matrix) in enumerate(self.disease_matrix.items()):
            if idx >= len(axes_flat):
                break
                
            ax = axes_flat[idx]
            
            # Remove 'All' row and column for cleaner visualization
            plot_matrix = matrix.drop('All', axis=0, errors='ignore').drop('All', axis=1, errors='ignore')
            
            # Create heatmap
            sns.heatmap(plot_matrix, annot=True, fmt='d', cmap='Blues', ax=ax)
            ax.set_title(f'{matrix_name.replace("_", " ").title()}', fontsize=12, fontweight='bold')
            ax.set_xlabel('')
            ax.set_ylabel('')
            
            # Rotate x-axis labels for better readability
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            plt.setp(ax.get_yticklabels(), rotation=0)
        
        # Hide unused subplots
        for idx in range(num_matrices, len(axes_flat)):
            axes_flat[idx].set_visible(False)
        
        plt.tight_layout()
        
        if save_plots:
            output_path = Path(self.excel_file_path).parent / "disease_type_matrices.png" if self.excel_file_path else "disease_type_matrices.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to: {output_path}")
        
        plt.show()
    
    def generate_summary_report(self):
        """
        Generate a comprehensive summary report of the disease type analysis.
        """
        if self.df is None:
            print("No data loaded. Please load data first.")
            return
            
        print("\n" + "="*80)
        print("DISEASE TYPE INFORMATION SUMMARY REPORT")
        print("="*80)
        
        # Dataset overview
        print(f"\nDataset Overview:")
        print(f"- Total records: {len(self.df)}")
        print(f"- Total columns: {len(self.df.columns)}")
        print(f"- Columns: {', '.join(self.df.columns)}")
        
        # Disease type summary
        if 'Disease_Type' in self.df.columns:
            print(f"\nDisease Type Summary:")
            disease_summary = self.df['Disease_Type'].describe()
            print(f"- Unique disease types: {disease_summary['unique']}")
            print(f"- Most common disease: {disease_summary['top']} ({disease_summary['freq']} cases)")
            
            # Age statistics by disease type
            if 'Age' in self.df.columns:
                print(f"\nAge Statistics by Disease Type:")
                age_by_disease = self.df.groupby('Disease_Type')['Age'].agg(['count', 'mean', 'std', 'min', 'max'])
                print(age_by_disease.round(2))
        
        # Matrix summary
        if self.disease_matrix:
            print(f"\nMatrix Analysis Summary:")
            for matrix_name, matrix in self.disease_matrix.items():
                print(f"- {matrix_name.replace('_', ' ').title()}: {matrix.shape[0]-1} diseases × {matrix.shape[1]-1} categories")
        
        print("\n" + "="*80)


def main():
    """
    Main function to demonstrate the DiseaseTypeMatrixAnalyzer.
    """
    print("Disease Type Information Matrix Demo")
    print("="*50)
    
    # Initialize analyzer
    analyzer = DiseaseTypeMatrixAnalyzer()
    
    # Check if sample data exists, if not create it
    sample_file = "sample_disease_data.xlsx"
    if not Path(sample_file).exists():
        print("Sample data not found. Creating sample data...")
        sample_file = analyzer.create_sample_data()
    
    # Load data
    if analyzer.load_data(sample_file):
        # Analyze disease types
        analyzer.analyze_disease_types()
        
        # Display matrices
        analyzer.display_matrices()
        
        # Create visualizations
        analyzer.visualize_matrices()
        
        # Generate summary report
        analyzer.generate_summary_report()
        
        print("\nAnalysis complete!")
    else:
        print("Failed to load data. Please check the file path and format.")


if __name__ == "__main__":
    main()
