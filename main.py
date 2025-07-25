"""
Financial Analysis System - Main Entry Point

A comprehensive, object-oriented financial analysis system that transforms 
Excel financial data into beautiful, interactive reports with visualizations.

Usage:
    python main.py

Features:
- Object-oriented design with modular components
- Beautiful HTML reports with embedded charts
- CSV export functionality
- Interactive command-line interface
- Comprehensive error handling
"""

from financial_system import FinancialReportSystem


def main():
    """Main execution function."""
    print("🚀 Financial Analysis System Starting...")
    print("=" * 50)
    
    # Initialize the system
    financial_system = FinancialReportSystem()
    
    try:
        # Load data interactively
        financial_system.load_data_interactive()
        
        # Show quick summary
        financial_system.get_quick_summary()
        
        # Generate comprehensive reports
        print("\n📊 Generating comprehensive financial reports with monthly and yearly breakdowns...")
        reports = financial_system.generate_all_reports()
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"📁 HTML Report: {reports['html']}")
        print(f"   • Overview with key metrics")
        print(f"   • Individual monthly reports")
        print(f"   • Individual yearly reports")
        print(f"   • Detailed category breakdowns")
        print(f"📁 CSV Report: {reports['csv']}")
        print("🎉 Thank you for using the Financial Analysis System!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please check your data file and try again.")


if __name__ == '__main__':
    main()
