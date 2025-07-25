"""
Financial Analysis System Package

A comprehensive, object-oriented financial analysis system that transforms 
Excel financial data into beautiful, interactive reports with visualizations.

Modules:
    - data_loader: Handles data import from various sources
    - financial_analyzer: Core analysis engine
    - visualization: Chart generation and visualization
    - report_generators: Different report output formats
    - financial_system: Main system orchestrator
    - config: Configuration settings

Usage:
    from financial_system import FinancialReportSystem
    
    system = FinancialReportSystem()
    system.load_data_interactive()
    system.generate_all_reports()
"""

__version__ = "1.0.0"
__author__ = "Financial Analysis System"

# Import main classes for easy access
from .financial_system import FinancialReportSystem
from .data_loader import DataLoader
from .financial_analyzer import FinancialAnalyzer
from .visualization import VisualizationEngine
from .report_generators import HTMLReportGenerator, CSVReportGenerator

__all__ = [
    'FinancialReportSystem',
    'DataLoader', 
    'FinancialAnalyzer',
    'VisualizationEngine',
    'HTMLReportGenerator',
    'CSVReportGenerator'
]
