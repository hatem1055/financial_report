"""
Main system orchestrating the entire financial reporting process.
This is the main entry point for the financial analysis system.
"""

import os
import webbrowser
from datetime import datetime

from data_loader import DataLoader
from financial_analyzer import FinancialAnalyzer
from report_generators import HTMLReportGenerator, CSVReportGenerator


class FinancialReportSystem:
    """Main system orchestrating the entire financial reporting process."""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.analyzer = None
        self.html_report_generator = HTMLReportGenerator()
        self.csv_report_generator = CSVReportGenerator()
    
    def load_data_interactive(self):
        """Interactive data loading with user input."""
        excel_path = input("📁 Please enter the path to your Excel file: ").strip()
        
        # Remove quotes if user included them
        if excel_path.startswith('"') and excel_path.endswith('"'):
            excel_path = excel_path[1:-1]
        elif excel_path.startswith("'") and excel_path.endswith("'"):
            excel_path = excel_path[1:-1]
        
        try:
            # Load data using ref_currency_amount
            df = self.data_loader.load_data(excel_path)
            
            # Initialize analyzer with loaded data
            self.analyzer = FinancialAnalyzer(df)
            print("🎯 Data loaded and ready for analysis!")
            return df
            
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            raise
    
    def load_data_from_file(self, file_path, file_type='excel'):
        """Load data from specified file path using ref_currency_amount."""
        try:
            df = self.data_loader.load_data(file_path)
            self.analyzer = FinancialAnalyzer(df)
            return df
            
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            raise
    
    def generate_html_report(self, output_path=None):
        """Generate HTML report."""
        if not self.analyzer:
            raise ValueError("❌ No data loaded. Please load data first.")
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"financial_report_{timestamp}.html"
        
        report_path = self.html_report_generator.generate(self.analyzer, output_path)
        
        # Open report in browser
        try:
            webbrowser.open(f'file://{os.path.abspath(report_path)}')
            print("🌐 Report opened in your default browser!")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"📍 You can manually open: {os.path.abspath(report_path)}")
        
        return report_path
    
    def generate_csv_report(self, output_path=None):
        """Generate CSV report."""
        if not self.analyzer:
            raise ValueError("❌ No data loaded. Please load data first.")
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"financial_analysis_{timestamp}.csv"
        
        return self.csv_report_generator.generate(self.analyzer, output_path)
    
    def generate_all_reports(self, base_name=None):
        """Generate both HTML and CSV reports."""
        if not base_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = f"financial_report_{timestamp}"
        
        html_path = self.generate_html_report(f"{base_name}.html")
        csv_path = self.generate_csv_report(f"{base_name}.csv")
        
        return {
            'html': html_path,
            'csv': csv_path
        }
    
    def get_quick_summary(self):
        """Get a quick summary of the financial data."""
        if not self.analyzer:
            raise ValueError("❌ No data loaded. Please load data first.")
        
        results = self.analyzer.analyze_all_time()
        
        print("\n" + "="*50)
        print("💰 QUICK FINANCIAL SUMMARY")
        print("="*50)
        print(f"💵 Total Income:      ${results['total_income']:,.2f}")
        print(f"💸 Total Spending:    ${results['total_spending']:,.2f}")
        print(f"📊 Net Balance:       ${results['net_balance']:,.2f}")
        print(f"📈 Transaction Count: {results['transaction_count']:,}")
        print(f"🎯 Avg Transaction:   ${results['avg_transaction']:,.2f}")
        print("="*50)
        
        return results
