#!/usr/bin/env python3
"""
Quick demo to show currency conversion in the main system.
"""

from financial_system import FinancialReportSystem
import os

def demo_currency_system():
    """Demonstrate the currency conversion system."""
    print("🚀 Financial Analysis System with Currency Conversion")
    print("=" * 60)
    
    # Initialize the system
    financial_system = FinancialReportSystem()
    
    # Use the existing Excel file
    excel_file = "report_2025-07-25_045634.xls"
    
    if os.path.exists(excel_file):
        print(f"📂 Loading data from: {excel_file}")
        
        try:
            # Load and process data
            financial_system.load_data_from_file(excel_file)
            
            # Generate comprehensive reports
            print(f"\n📊 Generating comprehensive reports with currency information...")
            financial_system.generate_all_reports()
            
            print(f"\n🎉 Demo completed successfully!")
            print(f"💡 Features demonstrated:")
            print(f"   ✅ Real-time currency conversion")
            print(f"   ✅ Detailed lending logic")
            print(f"   ✅ Charity breakdown by timeframe")
            print(f"   ✅ Monthly and yearly detailed reports")
            print(f"   ✅ Currency conversion tracking")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"❌ Excel file not found: {excel_file}")

if __name__ == "__main__":
    demo_currency_system()
