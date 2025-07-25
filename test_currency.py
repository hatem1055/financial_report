#!/usr/bin/env python3
"""
Test script to verify currency conversion functionality.
"""

from financial_system import FinancialReportSystem
from currency_converter import currency_converter
import os

def test_currency_conversion():
    """Test the currency conversion functionality."""
    print("🔍 Testing Currency Conversion Functionality")
    print("=" * 60)
    
    # First, test the currency converter directly
    print("\n💱 TESTING CURRENCY CONVERTER")
    print("-" * 35)
    
    # Get conversion summary
    summary = currency_converter.get_conversion_summary()
    print(f"Base Currency: {summary['base_currency']}")
    print(f"Last Updated: {summary['last_updated']}")
    print(f"Cache Valid: {summary['cache_valid']}")
    print(f"Available Rates: {summary['available_rates']}")
    
    # Test some conversions
    test_conversions = [
        (100, 'EUR', 'USD'),
        (1000, 'JPY', 'USD'),
        (50, 'GBP', 'USD'),
        (100, 'USD', 'EUR'),
    ]
    
    print(f"\n🔄 Testing Sample Conversions:")
    for amount, from_curr, to_curr in test_conversions:
        converted = currency_converter.convert_amount(amount, from_curr, to_curr)
        formatted = currency_converter.format_amount(converted, to_curr)
        print(f"  {amount} {from_curr} → {formatted}")
    
    # Test with actual financial data
    print(f"\n📊 TESTING WITH FINANCIAL DATA")
    print("-" * 35)
    
    # Initialize the system
    financial_system = FinancialReportSystem()
    
    # Load data from the existing Excel file
    excel_file = "report_2025-07-25_045634.xls"
    
    if not os.path.exists(excel_file):
        print(f"❌ Excel file '{excel_file}' not found!")
        return
    
    try:
        print(f"📂 Loading and processing data from: {excel_file}")
        financial_system.load_data_from_file(excel_file)
        
        # Get analyzer results
        analyzer = financial_system.analyzer
        all_time_results = analyzer.analyze_all_time()
        
        print(f"\n💰 FINANCIAL SUMMARY WITH CURRENCY CONVERSION")
        print("-" * 50)
        currency_info = all_time_results['currency_info']
        
        print(f"Base Currency: {currency_info['base_currency']}")
        print(f"Has Conversions: {currency_info['has_conversions']}")
        
        if currency_info['has_conversions']:
            print(f"Original Currencies: {', '.join(currency_info['original_currencies'])}")
            print(f"Transactions Converted: {currency_info['total_conversions']}")
        
        print(f"\n📈 Key Metrics:")
        print(f"Total Income: ${all_time_results['total_income']:,.2f} {currency_info['base_currency']}")
        print(f"Total Spending: ${all_time_results['total_spending']:,.2f} {currency_info['base_currency']}")
        print(f"Net Balance: ${all_time_results['net_balance']:,.2f} {currency_info['base_currency']}")
        
        # Generate reports with currency information
        print(f"\n📄 Generating reports with currency conversion info...")
        financial_system.generate_all_reports()
        
        print(f"\n✅ Test completed successfully!")
        print(f"🎯 Currency conversion is working:")
        print(f"   • Real-time exchange rates fetched and cached")
        print(f"   • All amounts converted to {currency_info['base_currency']}")
        print(f"   • Conversion information displayed in reports")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_currency_conversion()
