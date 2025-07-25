"""
Example usage and testing for the Financial Analysis System
"""

from financial_system import FinancialReportSystem


def demo_with_sample_data():
    """Demonstrate the system with programmatic data loading."""
    
    # Initialize system
    system = FinancialReportSystem()
    
    # For demo purposes, you could load data programmatically:
    # system.load_data_from_file("your_file.xlsx", "excel")
    
    print("🔍 Demo mode - please run main.py for interactive usage")
    print("📋 Available methods:")
    print("  - load_data_interactive()")
    print("  - load_data_from_file(path, type)")
    print("  - generate_html_report()")
    print("  - generate_csv_report()")
    print("  - generate_all_reports()")
    print("  - get_quick_summary()")


def test_individual_components():
    """Test individual components of the system."""
    
    print("🧪 Testing individual components...")
    
    # Test data loader
    from data_loader import DataLoader
    print("✅ DataLoader imported successfully")
    
    # Test analyzer
    from financial_analyzer import FinancialAnalyzer
    print("✅ FinancialAnalyzer imported successfully")
    
    # Test visualization
    from visualization import VisualizationEngine
    print("✅ VisualizationEngine imported successfully")
    
    # Test report generators
    from report_generators import HTMLReportGenerator, CSVReportGenerator
    print("✅ Report generators imported successfully")
    
    # Test main system
    from financial_system import FinancialReportSystem
    print("✅ FinancialReportSystem imported successfully")
    
    print("🎉 All components loaded successfully!")


if __name__ == "__main__":
    print("🚀 Financial Analysis System - Demo Mode")
    print("=" * 50)
    
    test_individual_components()
    print()
    demo_with_sample_data()
    
    print("\n💡 To use the full system, run: python main.py")
