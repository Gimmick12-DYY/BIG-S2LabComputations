#!/usr/bin/env python3
"""
Test script for ADRD data analysis (without Flask)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

def test_data_loading():
    print("Testing ADRD data loading...")
    
    # Check if file exists
    file_path = 'templates/ADRD_Metadata_YuyangD.xlsx'
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        # Load data
        df = pd.read_excel(file_path)
        print(f"✅ Data loaded successfully")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {len(df.columns)}")
        
        # Test basic analysis
        print("\nTesting basic analysis...")
        
        # Disease type analysis
        disease_col = 'Disease Type (e.g., AD, LBD, FTD, VaD, Mixed) (Text)'
        if disease_col in df.columns:
            disease_counts = df[disease_col].value_counts()
            print(f"✅ Disease types found: {len(disease_counts)}")
            print(f"   Top disease types: {dict(disease_counts.head(3))}")
        
        # Sample size analysis
        sample_col = 'Sample Size (Observations) (Integer)'
        if sample_col in df.columns:
            sample_sizes = df[sample_col].dropna()
            if len(sample_sizes) > 0:
                print(f"✅ Sample size analysis: {len(sample_sizes)} datasets with size data")
                print(f"   Total observations: {sample_sizes.sum():,}")
                print(f"   Average size: {sample_sizes.mean():.0f}")
        
        # Data availability analysis
        data_columns = [
            'EHR Data Available (Text)',
            'Imaging Data Types Available (Text)',
            'SNP Genotyping Data Available (Text)',
            'Proteomics Data Available (Text)',
            'Clinical Cognitive Tests Available (Text)'
        ]
        
        available_data = 0
        for col in data_columns:
            if col in df.columns:
                available_count = (df[col].notna() & (df[col] != '') & (df[col] != 'No')).sum()
                available_data += available_count
        
        print(f"✅ Data availability analysis: {available_data} data points available")
        
        print("\n🎉 All tests passed! The data is ready for web application.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    test_data_loading()
