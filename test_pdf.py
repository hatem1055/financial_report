"""
Test script to verify PDF generation works
"""

from financial_system import FinancialReportSystem
from financial_analyzer import FinancialAnalyzer

def test_pdf_generation():
    print("🧪 Testing PDF generation...")
    
    # Initialize system
    system = FinancialReportSystem()
    
    # Load the existing Excel file
    try:
        df = system.data_loader.load_data("report_2025-07-25_045634.xls")
        system.analyzer = FinancialAnalyzer(df)
        
        print("✅ Data loaded successfully")
        
        # Test PDF generation only
        pdf_path = system.generate_pdf_report("test_report.pdf")
        print(f"✅ PDF generated successfully: {pdf_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_generation()
