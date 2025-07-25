"""
Configuration settings for the financial analysis system.
"""

# Chart settings
CHART_CONFIG = {
    'figure_size_pie': (10, 8),
    'figure_size_bar': (10, 6),
    'figure_size_trend': (12, 8),
    'dpi': 300,
    'colors': {
        'income': 'green',
        'spending': 'red',
        'balance_positive': 'blue',
        'balance_negative': 'red'
    }
}

# Report settings
REPORT_CONFIG = {
    'charts_folder': 'charts',
    'base_currency': 'EGP',
    'currency_symbol': 'EGP',
    'date_format': '%Y-%m-%d at %H:%M:%S'
}

# Analysis settings
ANALYSIS_CONFIG = {
    'small_category_threshold': 0.02,  # 2% threshold for pie chart filtering
    'max_categories_display': 10,
    'loan_category': 'Loan, interests',
    'lending_category': 'Lending, renting',
    'charity_category': 'Charity',
    # Simplified spending categories for reports
    'spending_categories': {
        'charity': ['Charity'],
        'lending': ['Loan, interests', 'Lending, renting'],
        'normal': 'all_others'  # Everything else
    }
}

# File settings
FILE_CONFIG = {
    'supported_excel_formats': ['.xlsx', '.xls'],
    'supported_csv_formats': ['.csv'],
    'encoding': 'utf-8'
}
