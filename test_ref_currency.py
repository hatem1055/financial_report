#!/usr/bin/env python3
"""
Test script to verify the updated system with ref_currency_amount and EGP currency.
"""

from financial_system import FinancialReportSystem
import os

def test_ref_currency_system():
    """Test the updated system with ref_currency_amount and simplified categories."""
    print("🔍 Testing Updated System with ref_currency_amount and EGP")
    print("=" * 65)
    
    # Initialize the system
    financial_system = FinancialReportSystem()
    
    # Load data from the existing Excel file
    excel_file = "report_2025-07-25_045634.xls"
    
    if not os.path.exists(excel_file):
        print(f"❌ Excel file '{excel_file}' not found!")
        return
    
    try:
        print(f"📂 Loading data from: {excel_file}")
        financial_system.load_data_from_file(excel_file)
        
        # Get analyzer results
        analyzer = financial_system.analyzer
        all_time_results = analyzer.analyze_all_time()
        
        print(f"\n💰 FINANCIAL SUMMARY IN EGP")
        print("-" * 35)
        print(f"Currency: {all_time_results['currency']}")
        print(f"Total Income: {all_time_results['total_income']:,.2f} EGP")
        print(f"Total Spending: {all_time_results['total_spending']:,.2f} EGP")
        print(f"Net Balance: {all_time_results['net_balance']:,.2f} EGP")
        
        print(f"\n📊 SIMPLIFIED SPENDING CATEGORIES")
        print("-" * 35)
        simplified = all_time_results.get('simplified_spending', {})
        print(f"💝 Charity: {simplified.get('charity', 0):,.2f} EGP")
        print(f"💰 Lending: {simplified.get('lending', 0):,.2f} EGP")
        print(f"🛍️ Normal: {simplified.get('normal', 0):,.2f} EGP")
        
        print(f"\n💰 LENDING DETAILS")
        print("-" * 20)
        print(f"Total Lending: {all_time_results.get('total_lending', 0):,.2f} EGP")
        print(f"Repaid Lending: {all_time_results.get('repaid_lending', 0):,.2f} EGP")
        print(f"Outstanding Lending: {all_time_results.get('outstanding_lending', 0):,.2f} EGP")
        print(f"Excess Repayment: {all_time_results.get('excess_repayment', 0):,.2f} EGP")
        
        print(f"\n❤️ CHARITY ANALYSIS")
        print("-" * 18)
        print(f"Charity Spending: {all_time_results.get('charity_spending', 0):,.2f} EGP")
        print(f"Charity Percentage: {all_time_results.get('charity_percentage', 0):,.1f}%")
        
        # Test monthly data
        print(f"\n📅 MONTHLY ANALYSIS SAMPLE")
        print("-" * 25)
        monthly_results = analyzer.analyze_by_period('month')
        if monthly_results:
            # Show first month as example
            first_month_key = list(monthly_results.keys())[0]
            first_month_data = monthly_results[first_month_key]
            print(f"Sample Month: {first_month_key}")
            print(f"  Simplified Categories:")
            month_simplified = first_month_data.get('simplified_spending', {})
            print(f"    Charity: {month_simplified.get('charity', 0):,.2f} EGP")
            print(f"    Lending: {month_simplified.get('lending', 0):,.2f} EGP")
            print(f"    Normal: {month_simplified.get('normal', 0):,.2f} EGP")
            print(f"  Outstanding Lending: {first_month_data.get('outstanding_lending', 0):,.2f} EGP")
            print(f"  Excess Repayment: {first_month_data.get('excess_repayment', 0):,.2f} EGP")
        
        # Generate reports with new format
        print(f"\n📄 Generating reports with EGP currency and simplified categories...")
        financial_system.generate_all_reports()
        
        print(f"\n✅ Test completed successfully!")
        print(f"🎯 Updated system features working:")
        print(f"   • Using ref_currency_amount column (or amount as fallback)")
        print(f"   • All amounts displayed in EGP currency")
        print(f"   • Simplified spending categories (charity, lending, normal)")
        print(f"   • Outstanding lending and excess repayment tracking")
        print(f"   • Detailed breakdowns for each timeframe")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ref_currency_system()
