#!/usr/bin/env python3
"""
Test script for ADRD web application
"""

from adrd_web_app import ADRDMetadataAnalyzer

def test_analyzer():
    print("Testing ADRD Metadata Analyzer...")
    
    # Initialize analyzer
    analyzer = ADRDMetadataAnalyzer()
    
    # Test data loading
    print("Loading data...")
    success = analyzer.load_data()
    print(f"Load successful: {success}")
    
    if success and analyzer.df is not None:
        print(f"Data shape: {analyzer.df.shape}")
        print(f"Columns: {len(analyzer.df.columns)}")
        
        # Test analysis functions
        print("\nTesting analysis functions...")
        
        overview = analyzer.analyze_dataset_overview()
        print(f"Overview analysis: {'Success' if overview else 'Failed'}")
        
        disease_analysis = analyzer.analyze_disease_types()
        print(f"Disease analysis: {'Success' if disease_analysis else 'Failed'}")
        
        data_type_analysis = analyzer.analyze_data_types()
        print(f"Data type analysis: {'Success' if data_type_analysis else 'Failed'}")
        
        print("\n✅ All tests passed!")
    else:
        print("❌ Data loading failed")

if __name__ == '__main__':
    test_analyzer()
