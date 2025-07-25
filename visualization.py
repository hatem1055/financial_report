"""
Visualization module for financial analysis system.
Handles all chart generation and visualization.
"""

import matplotlib.pyplot as plt
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False
    print("⚠️  Seaborn not available, using matplotlib defaults")


class VisualizationEngine:
    """Handles all chart generation and visualization."""
    
    def __init__(self):
        # Set style for better-looking plots
        try:
            # Try different seaborn styles based on what's available
            available_styles = plt.style.available
            if 'seaborn-v0_8' in available_styles:
                plt.style.use('seaborn-v0_8')
            elif 'seaborn' in available_styles:
                plt.style.use('seaborn')
            elif 'seaborn-whitegrid' in available_styles:
                plt.style.use('seaborn-whitegrid')
            else:
                # Fall back to a built-in style
                plt.style.use('default')
                print("⚠️  Using default matplotlib style (seaborn not available)")
        except Exception as e:
            print(f"⚠️  Style setting warning: {e}")
            plt.style.use('default')
        
        # Set color palette
        try:
            if HAS_SEABORN:
                sns.set_palette("husl")
            else:
                # Use matplotlib's built-in color cycle
                plt.rcParams['axes.prop_cycle'] = plt.cycler(
                    color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
                )
        except Exception:
            print("⚠️  Using default color palette")
    
    def create_normal_spending_by_month(self, monthly_data, title="Normal Spending by Month"):
        """Create a bar chart showing normal spending trends by month."""
        try:
            months = []
            normal_spending = []
            
            for month, data in monthly_data.items():
                months.append(month)
                simplified_spending = data.get('simplified_spending', {})
                normal_spending.append(simplified_spending.get('normal', 0))
            
            if not months:
                return None
            
            fig, ax = plt.subplots(figsize=(12, 6))
            bars = ax.bar(months, normal_spending, color='#3498db', alpha=0.7)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Normal Spending (EGP)', fontsize=12)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:,.0f}', ha='center', va='bottom', fontsize=10)
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"⚠️  Error creating normal spending by month chart: {e}")
            return None
    
    def create_normal_spending_by_year(self, yearly_data, title="Normal Spending by Year"):
        """Create a bar chart showing normal spending trends by year."""
        try:
            years = []
            normal_spending = []
            
            for year, data in yearly_data.items():
                years.append(year)
                simplified_spending = data.get('simplified_spending', {})
                normal_spending.append(simplified_spending.get('normal', 0))
            
            if not years:
                return None
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(years, normal_spending, color='#3498db', alpha=0.7)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Year', fontsize=12)
            ax.set_ylabel('Normal Spending (EGP)', fontsize=12)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:,.0f}', ha='center', va='bottom', fontsize=10)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"⚠️  Error creating normal spending by year chart: {e}")
            return None
    
    def create_charity_spending_by_month(self, monthly_data, title="Charity Spending by Month"):
        """Create a bar chart showing charity spending trends by month."""
        try:
            months = []
            charity_spending = []
            
            for month, data in monthly_data.items():
                months.append(month)
                simplified_spending = data.get('simplified_spending', {})
                charity_spending.append(simplified_spending.get('charity', 0))
            
            if not months:
                return None
            
            fig, ax = plt.subplots(figsize=(12, 6))
            bars = ax.bar(months, charity_spending, color='#e74c3c', alpha=0.7)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Charity Spending (EGP)', fontsize=12)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:,.0f}', ha='center', va='bottom', fontsize=10)
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"⚠️  Error creating charity spending by month chart: {e}")
            return None
    
    def create_charity_spending_by_year(self, yearly_data, title="Charity Spending by Year"):
        """Create a bar chart showing charity spending trends by year."""
        try:
            years = []
            charity_spending = []
            
            for year, data in yearly_data.items():
                years.append(year)
                simplified_spending = data.get('simplified_spending', {})
                charity_spending.append(simplified_spending.get('charity', 0))
            
            if not years:
                return None
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(years, charity_spending, color='#e74c3c', alpha=0.7)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Year', fontsize=12)
            ax.set_ylabel('Charity Spending (EGP)', fontsize=12)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:,.0f}', ha='center', va='bottom', fontsize=10)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"⚠️  Error creating charity spending by year chart: {e}")
            return None
    
    def create_total_spending_by_month(self, monthly_data, title="Total Spending by Month"):
        """Create a bar chart showing total spending trends by month."""
        try:
            months = []
            total_spending = []
            
            for month, data in monthly_data.items():
                months.append(month)
                total_spending.append(data.get('total_spending', 0))
            
            if not months:
                return None
            
            fig, ax = plt.subplots(figsize=(12, 6))
            bars = ax.bar(months, total_spending, color='#9b59b6', alpha=0.7)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Month', fontsize=12)
            ax.set_ylabel('Total Spending (EGP)', fontsize=12)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:,.0f}', ha='center', va='bottom', fontsize=10)
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"⚠️  Error creating total spending by month chart: {e}")
            return None
    
    def create_total_spending_by_year(self, yearly_data, title="Total Spending by Year"):
        """Create a bar chart showing total spending trends by year."""
        try:
            years = []
            total_spending = []
            
            for year, data in yearly_data.items():
                years.append(year)
                total_spending.append(data.get('total_spending', 0))
            
            if not years:
                return None
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(years, total_spending, color='#9b59b6', alpha=0.7)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Year', fontsize=12)
            ax.set_ylabel('Total Spending (EGP)', fontsize=12)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:,.0f}', ha='center', va='bottom', fontsize=10)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"⚠️  Error creating total spending by year chart: {e}")
            return None
    
    def create_spending_categories_chart(self, spending_data, title="All-Time Spending Categories"):
        """Create a horizontal bar chart showing all spending categories."""
        try:
            if not spending_data:
                return None
            
            # Sort categories by amount (descending)
            sorted_categories = sorted(spending_data.items(), key=lambda x: x[1], reverse=True)
            categories = [item[0] for item in sorted_categories]
            amounts = [item[1] for item in sorted_categories]
            
            fig, ax = plt.subplots(figsize=(10, max(8, len(categories) * 0.5)))
            bars = ax.barh(categories, amounts, color='#34495e', alpha=0.7)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Amount (EGP)', fontsize=12)
            ax.set_ylabel('Category', fontsize=12)
            
            # Add value labels on bars
            for i, bar in enumerate(bars):
                width = bar.get_width()
                if width > 0:
                    ax.text(width, bar.get_y() + bar.get_height()/2.,
                           f'{width:,.0f}', ha='left', va='center', fontsize=10, 
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"⚠️  Error creating spending categories chart: {e}")
            return None
    
    def create_income_categories_chart(self, income_data, title="All-Time Income Categories"):
        """Create a horizontal bar chart showing all income categories."""
        try:
            if not income_data:
                return None
            
            # Sort categories by amount (descending)
            sorted_categories = sorted(income_data.items(), key=lambda x: x[1], reverse=True)
            categories = [item[0] for item in sorted_categories]
            amounts = [item[1] for item in sorted_categories]
            
            fig, ax = plt.subplots(figsize=(10, max(8, len(categories) * 0.5)))
            bars = ax.barh(categories, amounts, color='#27ae60', alpha=0.7)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Amount (EGP)', fontsize=12)
            ax.set_ylabel('Category', fontsize=12)
            
            # Add value labels on bars
            for i, bar in enumerate(bars):
                width = bar.get_width()
                if width > 0:
                    ax.text(width, bar.get_y() + bar.get_height()/2.,
                           f'{width:,.0f}', ha='left', va='center', fontsize=10,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            print(f"⚠️  Error creating income categories chart: {e}")
            return None
        
    def create_spending_pie_chart(self, spending_data, title="Spending by Category"):
        """Create pie chart for spending categories."""
        if not spending_data:
            return None
            
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Filter out very small amounts for better readability
        total = sum(spending_data.values())
        filtered_data = {k: v for k, v in spending_data.items() if v / total > 0.02}
        
        # Add "Others" category if needed
        others_sum = total - sum(filtered_data.values())
        if others_sum > 0:
            filtered_data['Others'] = others_sum
        
        wedges, texts, autotexts = ax.pie(
            filtered_data.values(), 
            labels=filtered_data.keys(),
            autopct='%1.1f%%',
            startangle=90,
            explode=[0.05] * len(filtered_data)
        )
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Improve text readability
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        return fig
    
    def create_income_vs_spending_bar(self, total_income, total_spending):
        """Create bar chart comparing income vs spending."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = ['Total Income', 'Total Spending', 'Net Balance']
        values = [total_income, total_spending, total_income - total_spending]
        colors = ['green', 'red', 'blue' if values[2] >= 0 else 'red']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.7)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + (height*0.01),
                   f'${value:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title('Income vs Spending Overview', fontsize=16, fontweight='bold')
        ax.set_ylabel('Amount ($)', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_monthly_trend(self, monthly_results):
        """Create line chart showing monthly trends."""
        if not monthly_results:
            return None
            
        fig, ax = plt.subplots(figsize=(12, 8))
        
        months = list(monthly_results.keys())
        income_trend = [data['total_income'] for data in monthly_results.values()]
        spending_trend = [data['total_spending'] for data in monthly_results.values()]
        balance_trend = [data['net_balance'] for data in monthly_results.values()]
        
        ax.plot(months, income_trend, marker='o', linewidth=2, label='Income', color='green')
        ax.plot(months, spending_trend, marker='s', linewidth=2, label='Spending', color='red')
        ax.plot(months, balance_trend, marker='^', linewidth=2, label='Net Balance', color='blue')
        
        ax.set_title('Monthly Financial Trends', fontsize=16, fontweight='bold')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Amount ($)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    
    def create_category_breakdown_bar(self, category_data, title="Category Breakdown", max_categories=10):
        """Create horizontal bar chart for category breakdown."""
        if not category_data:
            return None
        
        # Sort and limit categories
        sorted_data = dict(sorted(category_data.items(), key=lambda x: x[1], reverse=True)[:max_categories])
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        categories = list(sorted_data.keys())
        values = list(sorted_data.values())
        
        bars = ax.barh(categories, values, alpha=0.7)
        
        # Add value labels
        for bar, value in zip(bars, values):
            width = bar.get_width()
            ax.text(width + (max(values) * 0.01), bar.get_y() + bar.get_height()/2,
                   f'${value:,.0f}', ha='left', va='center', fontweight='bold')
        
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel('Amount ($)', fontsize=12)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_yearly_comparison(self, yearly_results):
        """Create comparison chart for yearly data."""
        if not yearly_results:
            return None
            
        fig, ax = plt.subplots(figsize=(12, 8))
        
        years = list(yearly_results.keys())
        income_data = [data['total_income'] for data in yearly_results.values()]
        spending_data = [data['total_spending'] for data in yearly_results.values()]
        balance_data = [data['net_balance'] for data in yearly_results.values()]
        
        x = range(len(years))
        width = 0.25
        
        # Create grouped bar chart
        ax.bar([i - width for i in x], income_data, width, label='Income', color='green', alpha=0.7)
        ax.bar(x, spending_data, width, label='Spending', color='red', alpha=0.7)
        ax.bar([i + width for i in x], balance_data, width, label='Net Balance', 
               color=['blue' if val >= 0 else 'red' for val in balance_data], alpha=0.7)
        
        # Add value labels on bars
        for i, (income, spending, balance) in enumerate(zip(income_data, spending_data, balance_data)):
            ax.text(i - width, income + (max(income_data) * 0.01), f'${income:,.0f}', 
                   ha='center', va='bottom', fontsize=8, fontweight='bold')
            ax.text(i, spending + (max(spending_data) * 0.01), f'${spending:,.0f}', 
                   ha='center', va='bottom', fontsize=8, fontweight='bold')
            ax.text(i + width, balance + (abs(balance) * 0.05 if balance != 0 else max(income_data) * 0.01), 
                   f'${balance:,.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        ax.set_title('Yearly Financial Comparison', fontsize=16, fontweight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Amount ($)', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(years)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig
