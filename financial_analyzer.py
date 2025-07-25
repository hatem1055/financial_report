"""
Financial analysis module.
Contains the core analysis logic for financial data with simplified categories.
"""

import pandas as pd
from config import ANALYSIS_CONFIG, REPORT_CONFIG


class FinancialAnalyzer:
    """Core financial analysis engine."""
    
    def __init__(self, df):
        """Initialize with financial data."""
        self.raw_data = df.copy()
        self.processed_data = self._prepare_data(df.copy())
        self.base_currency = REPORT_CONFIG['base_currency']
        
    def _prepare_data(self, df):
        """Clean and prepare financial data."""
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract time periods
        df['month'] = df['date'].dt.to_period('M')
        df['year'] = df['date'].dt.year
        df['quarter'] = df['date'].dt.to_period('Q')
        
        # Ensure amount is numeric
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Create spending and income flags
        df['is_expense'] = df['amount'] < 0
        df['is_income'] = df['amount'] > 0
        
        return df
    
    def _categorize_spending(self, spending_by_category):
        """Categorize spending into simplified categories: charity, lending, normal."""
        categories = ANALYSIS_CONFIG['spending_categories']
        
        charity_amount = 0
        lending_amount = 0
        normal_amount = 0
        
        for category, amount in spending_by_category.items():
            if category in categories['charity']:
                charity_amount += amount
            elif category in categories['lending']:
                lending_amount += amount
            else:
                normal_amount += amount
        
        return {
            'charity': charity_amount,
            'lending': lending_amount,
            'normal': normal_amount
        }
    
    def _calculate_metrics(self, data):
        """Calculate comprehensive financial metrics with simplified categories."""
        # Spending by category (raw)
        expenses = data[data['is_expense']].copy()
        spending_by_category = abs(expenses.groupby('category')['amount'].sum())
        
        # Income by category (raw)
        income_data = data[data['is_income']]
        income_by_category = income_data.groupby('category')['amount'].sum()
        
        # Handle lending logic - exclude lending from spending if it was repaid
        loan_expenses = abs(expenses[expenses['category'] == 'Loan, interests']['amount'].sum())
        loan_income = income_data[income_data['category'] == 'Lending, renting']['amount'].sum()
        
        # Net lending (only count as spending if not repaid)
        net_loan_spending = loan_expenses - loan_income
        outstanding_lending = max(0, net_loan_spending)
        excess_repayment = max(0, -net_loan_spending)
        
        # Adjust spending categories based on lending logic
        adjusted_spending_by_category = spending_by_category.copy()
        adjusted_income_by_category = income_by_category.copy()
        
        if net_loan_spending > 0:
            # There's unpaid lending - count only the unpaid portion as spending
            adjusted_spending_by_category['Loan, interests'] = net_loan_spending
        else:
            # All lending was repaid or we have excess repayments
            # Remove lending from spending entirely
            adjusted_spending_by_category = adjusted_spending_by_category.drop('Loan, interests', errors='ignore')
        
        # Remove lending repayments from income (since they're not real income)
        adjusted_income_by_category = adjusted_income_by_category.drop('Lending, renting', errors='ignore')
        
        # Calculate totals with adjustments
        total_spending_adjusted = adjusted_spending_by_category.sum()
        total_income_adjusted = adjusted_income_by_category.sum()
        
        # Charity calculations
        charity_spending = abs(expenses[expenses['category'] == 'Charity']['amount'].sum())
        spending_excluding_charity = total_spending_adjusted - charity_spending
        
        # Simplified spending categories
        simplified_categories = self._categorize_spending(adjusted_spending_by_category.to_dict())
        
        # Raw totals (without lending adjustments) for reference
        total_spending_raw = spending_by_category.sum()
        total_income_raw = income_by_category.sum()
        
        return {
            'spending_by_category': adjusted_spending_by_category.to_dict(),
            'income_by_category': adjusted_income_by_category.to_dict(),
            'total_spending': total_spending_adjusted,
            'total_income': total_income_adjusted,
            'net_balance': total_income_adjusted - total_spending_adjusted,
            'charity_spending': charity_spending,
            'spending_excluding_charity': spending_excluding_charity,
            'transaction_count': len(data),
            'avg_transaction': data['amount'].mean(),
            # Simplified spending categories
            'simplified_spending': simplified_categories,
            # Lending details with outstanding and excess
            'total_lending': loan_expenses,
            'repaid_lending': loan_income,
            'outstanding_lending': outstanding_lending,
            'excess_repayment': excess_repayment,
            'charity_percentage': (charity_spending / total_spending_adjusted * 100) if total_spending_adjusted > 0 else 0,
            # Currency information
            'currency': self.base_currency,
            # Raw totals for transparency
            'raw_totals': {
                'total_spending_raw': total_spending_raw,
                'total_income_raw': total_income_raw,
                'spending_by_category_raw': spending_by_category.to_dict(),
                'income_by_category_raw': income_by_category.to_dict()
            }
        }
    
    def analyze_all_time(self):
        """Analyze entire dataset."""
        return self._calculate_metrics(self.processed_data)
    
    def analyze_by_period(self, period='month'):
        """Analyze data by time period."""
        results = {}
        for period_value, period_data in self.processed_data.groupby(period):
            results[str(period_value)] = self._calculate_metrics(period_data)
        return results
    
    def get_top_spending_categories(self, n=5):
        """Get top N spending categories."""
        all_time_data = self.analyze_all_time()
        spending = all_time_data['spending_by_category']
        return dict(sorted(spending.items(), key=lambda x: x[1], reverse=True)[:n])
    
    def get_monthly_summary(self):
        """Get a summary of monthly trends."""
        monthly_data = self.analyze_by_period('month')
        
        summary = {
            'months': list(monthly_data.keys()),
            'total_income': [data['total_income'] for data in monthly_data.values()],
            'total_spending': [data['total_spending'] for data in monthly_data.values()],
            'net_balance': [data['net_balance'] for data in monthly_data.values()]
        }
        
        return summary
    
    def get_lending_summary(self):
        """Get a comprehensive summary of lending activities."""
        all_time_data = self.analyze_all_time()
        monthly_data = self.analyze_by_period('month')
        
        lending_summary = {
            'overall': {
                'total_lending': all_time_data['total_lending'],
                'repaid_lending': all_time_data['repaid_lending'],
                'outstanding_lending': all_time_data['outstanding_lending'],
                'excess_repayment': all_time_data['excess_repayment']
            },
            'by_month': {}
        }
        
        for month, data in monthly_data.items():
            lending_summary['by_month'][month] = {
                'total_lending': data['total_lending'],
                'repaid_lending': data['repaid_lending'],
                'outstanding_lending': data['outstanding_lending'],
                'excess_repayment': data['excess_repayment']
            }
        
        return lending_summary
    
    def get_charity_analysis(self):
        """Get detailed charity spending analysis."""
        all_time_data = self.analyze_all_time()
        monthly_data = self.analyze_by_period('month')
        
        charity_analysis = {
            'total_charity': all_time_data['charity_spending'],
            'percentage_of_spending': (all_time_data['charity_spending'] / all_time_data['total_spending'] * 100) if all_time_data['total_spending'] > 0 else 0,
            'by_month': {}
        }
        
        for month, data in monthly_data.items():
            charity_analysis['by_month'][month] = {
                'charity_amount': data['charity_spending'],
                'percentage_of_monthly_spending': (data['charity_spending'] / data['total_spending'] * 100) if data['total_spending'] > 0 else 0
            }
        
        return charity_analysis
    
    def analyze_all_time(self):
        """Analyze entire dataset."""
        return self._calculate_metrics(self.processed_data)
    
    def analyze_by_period(self, period='month'):
        """Analyze data by time period."""
        results = {}
        for period_value, period_data in self.processed_data.groupby(period):
            results[str(period_value)] = self._calculate_metrics(period_data)
        return results
    
    def get_top_spending_categories(self, n=5):
        """Get top N spending categories."""
        all_time_data = self.analyze_all_time()
        spending = all_time_data['spending_by_category']
        return dict(sorted(spending.items(), key=lambda x: x[1], reverse=True)[:n])
    
    def get_monthly_summary(self):
        """Get a summary of monthly trends."""
        monthly_data = self.analyze_by_period('month')
        
        summary = {
            'months': list(monthly_data.keys()),
            'total_income': [data['total_income'] for data in monthly_data.values()],
            'total_spending': [data['total_spending'] for data in monthly_data.values()],
            'net_balance': [data['net_balance'] for data in monthly_data.values()]
        }
        
        return summary
    
    def get_lending_summary(self):
        """Get a comprehensive summary of lending activities."""
        all_time_data = self.analyze_all_time()
        monthly_data = self.analyze_by_period('month')
        
        lending_summary = {
            'overall': all_time_data['lending_details'],
            'by_month': {}
        }
        
        for month, data in monthly_data.items():
            lending_summary['by_month'][month] = data['lending_details']
        
        return lending_summary
    
    def get_charity_analysis(self):
        """Get detailed charity spending analysis."""
        all_time_data = self.analyze_all_time()
        monthly_data = self.analyze_by_period('month')
        
        charity_analysis = {
            'total_charity': all_time_data['charity_spending'],
            'percentage_of_spending': (all_time_data['charity_spending'] / all_time_data['total_spending'] * 100) if all_time_data['total_spending'] > 0 else 0,
            'by_month': {}
        }
        
        for month, data in monthly_data.items():
            charity_analysis['by_month'][month] = {
                'charity_amount': data['charity_spending'],
                'percentage_of_monthly_spending': (data['charity_spending'] / data['total_spending'] * 100) if data['total_spending'] > 0 else 0
            }
        
        return charity_analysis
