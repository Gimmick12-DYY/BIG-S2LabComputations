# Disease Type Matrix Web Application

A Flask-based web application for visualizing disease type information as interactive matrices from Excel files.

## Features

- **File Upload**: Upload Excel (.xlsx, .xls) or CSV files with disease data
- **Interactive Visualizations**: Generate heatmap matrices showing relationships between disease types and various attributes
- **Sample Data Generation**: Create and analyze sample disease data for demonstration
- **Template Download**: Download Excel template for proper data formatting
- **Responsive Design**: Modern, mobile-friendly web interface
- **Real-time Processing**: Instant visualization of uploaded data

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python run_web_app.py
```

Or directly:

```bash
python web_app.py
```

### 3. Access the Application

Open your web browser and navigate to: `http://localhost:5000`

## Expected Data Format

Your Excel file should contain the following columns:

| Column Name | Description | Example Values |
|-------------|-------------|----------------|
| `Patient_ID` | Unique patient identifier | P001, P002, P003 |
| `Disease_Type` | Type of disease | Alzheimer's Disease, Parkinson's Disease |
| `Severity` | Disease severity level | Mild, Moderate, Severe |
| `Gender` | Patient gender | Male, Female |
| `Age` | Patient age | 25, 45, 67 |
| `Family_History` | Family history of disease | Yes, No |
| `Treatment_Status` | Current treatment status | Active, Inactive, Unknown |

## Web Application Features

### Upload Interface
- Drag & drop file upload
- Support for Excel (.xlsx, .xls) and CSV files
- File validation and error handling
- Maximum file size: 16MB

### Visualization Features
- **Disease Type Distribution**: Bar chart showing frequency of each disease type
- **Matrix Heatmaps**: Cross-tabulation matrices showing relationships between:
  - Disease types vs. severity levels
  - Disease types vs. gender
  - Disease types vs. family history
  - Disease types vs. treatment status
- **Age Statistics**: Summary statistics for patient ages
- **Data Tables**: Detailed tabular view of all matrices

### Sample Data
- Generate sample disease data for testing
- Download Excel template for proper formatting
- Pre-configured with realistic disease types and attributes

## API Endpoints

- `GET /` - Main application interface
- `POST /upload` - Upload and process Excel file
- `GET /sample_data` - Generate and process sample data
- `GET /download_sample` - Download Excel template
- `GET /health` - Health check endpoint

## File Structure

```
ADRD_KG/
├── web_app.py                 # Main Flask application
├── run_web_app.py            # Simple startup script
├── disease_type_info_matrix_demo.py  # Core analysis module
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Main web interface
├── uploads/                 # Temporary file storage (auto-created)
└── WEB_APP_README.md        # This file
```

## Configuration

### Environment Variables
- `FLASK_ENV`: Set to 'development' for debug mode
- `UPLOAD_FOLDER`: Directory for temporary file storage (default: 'uploads')
- `MAX_CONTENT_LENGTH`: Maximum file size in bytes (default: 16MB)

### Security Notes
- Change the `app.secret_key` in production
- Consider using environment variables for sensitive configuration
- Implement proper file validation and sanitization for production use

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **File Upload Issues**: Check file format and size limits
   - Supported formats: .xlsx, .xls, .csv
   - Maximum size: 16MB

3. **Port Already in Use**: Change the port in `web_app.py`
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
   ```

4. **Template Not Found**: Ensure the `templates/` directory exists and contains `index.html`

### Performance Tips

- For large datasets (>10,000 rows), consider implementing pagination
- Use production WSGI server (like Gunicorn) for deployment
- Implement caching for frequently accessed data

## Development

### Adding New Features

1. **New Matrix Types**: Modify `create_disease_matrix()` in `disease_type_info_matrix_demo.py`
2. **Additional Visualizations**: Extend `create_web_visualizations()` in `web_app.py`
3. **UI Enhancements**: Update `templates/index.html` and add new CSS/JavaScript

### Testing

Test the application with:
- Sample data generation
- Various Excel file formats
- Different data sizes
- Error conditions (invalid files, missing columns)

## Deployment

For production deployment:

1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up proper logging
3. Configure reverse proxy (Nginx)
4. Use environment variables for configuration
5. Implement proper security measures

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

## License

This project is part of the BIG-S2LabComputations repository.
