"""
Report generation module.
Contains different report generators (HTML, PDF, etc.).
"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt

from visualization import VisualizationEngine


class ReportGenerator(ABC):
    """Abstract base class for report generators."""
    
    @abstractmethod
    def generate(self, analyzer, output_path):
        """Generate report from analysis results."""
        pass


class HTMLReportGenerator(ReportGenerator):
    """Generates comprehensive HTML reports with embedded charts."""
    
    def __init__(self):
        self.viz_engine = VisualizationEngine()
    
    def generate(self, analyzer, output_path="financial_report.html"):
        """Generate comprehensive HTML report with monthly and yearly breakdowns."""
        # Perform analysis
        all_time_results = analyzer.analyze_all_time()
        monthly_results = analyzer.analyze_by_period('month')
        yearly_results = analyzer.analyze_by_period('year')
        
        # Generate charts
        charts_dir = Path(output_path).parent / "charts"
        charts_dir.mkdir(exist_ok=True)
        
        chart_files = []
        
        # Overall spending pie chart
        spending_fig = self.viz_engine.create_spending_pie_chart(
            all_time_results['spending_by_category'], 
            "All-Time Spending by Category"
        )
        if spending_fig:
            spending_path = charts_dir / "spending_pie.png"
            spending_fig.savefig(spending_path, dpi=300, bbox_inches='tight')
            chart_files.append(("spending_pie.png", "Overall Spending Distribution"))
            plt.close(spending_fig)
        
        # Income vs spending bar chart
        income_spending_fig = self.viz_engine.create_income_vs_spending_bar(
            all_time_results['total_income'], 
            all_time_results['total_spending']
        )
        if income_spending_fig:
            income_spending_path = charts_dir / "income_vs_spending.png"
            income_spending_fig.savefig(income_spending_path, dpi=300, bbox_inches='tight')
            chart_files.append(("income_vs_spending.png", "Income vs Spending Overview"))
            plt.close(income_spending_fig)
        
        # Monthly trend chart
        monthly_fig = self.viz_engine.create_monthly_trend(monthly_results)
        if monthly_fig:
            monthly_path = charts_dir / "monthly_trends.png"
            monthly_fig.savefig(monthly_path, dpi=300, bbox_inches='tight')
            chart_files.append(("monthly_trends.png", "Monthly Financial Trends"))
            plt.close(monthly_fig)
        
        # Yearly comparison chart
        yearly_fig = self.viz_engine.create_yearly_comparison(yearly_results)
        if yearly_fig:
            yearly_path = charts_dir / "yearly_comparison.png"
            yearly_fig.savefig(yearly_path, dpi=300, bbox_inches='tight')
            chart_files.append(("yearly_comparison.png", "Yearly Comparison"))
            plt.close(yearly_fig)
        
        # Category breakdown chart
        category_fig = self.viz_engine.create_category_breakdown_bar(
            all_time_results['spending_by_category'],
            "Top Spending Categories"
        )
        if category_fig:
            category_path = charts_dir / "category_breakdown.png"
            category_fig.savefig(category_path, dpi=300, bbox_inches='tight')
            chart_files.append(("category_breakdown.png", "Category Breakdown"))
            plt.close(category_fig)
        
        # Generate new spending analysis charts
        new_chart_files = self._generate_spending_analysis_charts(
            monthly_results, yearly_results, all_time_results, charts_dir
        )
        
        # Generate monthly charts
        monthly_chart_files = self._generate_monthly_charts(monthly_results, charts_dir)
        
        # Generate yearly charts  
        yearly_chart_files = self._generate_yearly_charts(yearly_results, charts_dir)
        
        # Generate HTML report
        html_content = self._generate_html_content(
            all_time_results, monthly_results, yearly_results, 
            chart_files, new_chart_files, monthly_chart_files, yearly_chart_files
        )
        
        # Write HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📊 Comprehensive report generated: {output_path}")
        return output_path
    
    def _generate_monthly_charts(self, monthly_results, charts_dir):
        """Generate individual charts for each month."""
        monthly_chart_files = []
        
        for month, data in monthly_results.items():
            if data['spending_by_category']:  # Only generate if there's data
                # Create spending pie chart for this month
                month_fig = self.viz_engine.create_spending_pie_chart(
                    data['spending_by_category'],
                    f"Spending in {month}"
                )
                if month_fig:
                    month_path = charts_dir / f"monthly_spending_{month.replace('-', '_')}.png"
                    month_fig.savefig(month_path, dpi=300, bbox_inches='tight')
                    monthly_chart_files.append((
                        f"monthly_spending_{month.replace('-', '_')}.png",
                        month,
                        data
                    ))
                    plt.close(month_fig)
        
        return monthly_chart_files
    
    def _generate_yearly_charts(self, yearly_results, charts_dir):
        """Generate individual charts for each year."""
        yearly_chart_files = []
        
        for year, data in yearly_results.items():
            if data['spending_by_category']:  # Only generate if there's data
                # Create spending pie chart for this year
                year_fig = self.viz_engine.create_spending_pie_chart(
                    data['spending_by_category'],
                    f"Spending in {year}"
                )
                if year_fig:
                    year_path = charts_dir / f"yearly_spending_{year}.png"
                    year_fig.savefig(year_path, dpi=300, bbox_inches='tight')
                    yearly_chart_files.append((
                        f"yearly_spending_{year}.png",
                        year,
                        data
                    ))
                    plt.close(year_fig)
        
        return yearly_chart_files
    
    def _generate_spending_analysis_charts(self, monthly_results, yearly_results, all_time_results, charts_dir):
        """Generate comprehensive spending analysis charts."""
        new_chart_files = []
        
        # Normal spending by month
        normal_monthly_fig = self.viz_engine.create_normal_spending_by_month(monthly_results)
        if normal_monthly_fig:
            normal_monthly_path = charts_dir / "normal_spending_monthly.png"
            normal_monthly_fig.savefig(normal_monthly_path, dpi=300, bbox_inches='tight')
            new_chart_files.append(("normal_spending_monthly.png", "Normal Spending by Month"))
            plt.close(normal_monthly_fig)
        
        # Normal spending by year
        normal_yearly_fig = self.viz_engine.create_normal_spending_by_year(yearly_results)
        if normal_yearly_fig:
            normal_yearly_path = charts_dir / "normal_spending_yearly.png"
            normal_yearly_fig.savefig(normal_yearly_path, dpi=300, bbox_inches='tight')
            new_chart_files.append(("normal_spending_yearly.png", "Normal Spending by Year"))
            plt.close(normal_yearly_fig)
        
        # Charity spending by month
        charity_monthly_fig = self.viz_engine.create_charity_spending_by_month(monthly_results)
        if charity_monthly_fig:
            charity_monthly_path = charts_dir / "charity_spending_monthly.png"
            charity_monthly_fig.savefig(charity_monthly_path, dpi=300, bbox_inches='tight')
            new_chart_files.append(("charity_spending_monthly.png", "Charity Spending by Month"))
            plt.close(charity_monthly_fig)
        
        # Charity spending by year
        charity_yearly_fig = self.viz_engine.create_charity_spending_by_year(yearly_results)
        if charity_yearly_fig:
            charity_yearly_path = charts_dir / "charity_spending_yearly.png"
            charity_yearly_fig.savefig(charity_yearly_path, dpi=300, bbox_inches='tight')
            new_chart_files.append(("charity_spending_yearly.png", "Charity Spending by Year"))
            plt.close(charity_yearly_fig)
        
        # Total spending by month
        total_monthly_fig = self.viz_engine.create_total_spending_by_month(monthly_results)
        if total_monthly_fig:
            total_monthly_path = charts_dir / "total_spending_monthly.png"
            total_monthly_fig.savefig(total_monthly_path, dpi=300, bbox_inches='tight')
            new_chart_files.append(("total_spending_monthly.png", "Total Spending by Month"))
            plt.close(total_monthly_fig)
        
        # Total spending by year
        total_yearly_fig = self.viz_engine.create_total_spending_by_year(yearly_results)
        if total_yearly_fig:
            total_yearly_path = charts_dir / "total_spending_yearly.png"
            total_yearly_fig.savefig(total_yearly_path, dpi=300, bbox_inches='tight')
            new_chart_files.append(("total_spending_yearly.png", "Total Spending by Year"))
            plt.close(total_yearly_fig)
        
        # All-time spending categories
        spending_categories_fig = self.viz_engine.create_spending_categories_chart(
            all_time_results['spending_by_category']
        )
        if spending_categories_fig:
            spending_categories_path = charts_dir / "all_time_spending_categories.png"
            spending_categories_fig.savefig(spending_categories_path, dpi=300, bbox_inches='tight')
            new_chart_files.append(("all_time_spending_categories.png", "All-Time Spending Categories"))
            plt.close(spending_categories_fig)
        
        # All-time income categories
        income_categories_fig = self.viz_engine.create_income_categories_chart(
            all_time_results['income_by_category']
        )
        if income_categories_fig:
            income_categories_path = charts_dir / "all_time_income_categories.png"
            income_categories_fig.savefig(income_categories_path, dpi=300, bbox_inches='tight')
            new_chart_files.append(("all_time_income_categories.png", "All-Time Income Categories"))
            plt.close(income_categories_fig)
        
        return new_chart_files
    
    def _generate_html_content(self, all_time_results, monthly_results, yearly_results, 
                             chart_files, new_chart_files, monthly_chart_files, yearly_chart_files):
        """Generate comprehensive HTML content with monthly and yearly breakdowns."""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Financial Analysis Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f8f9fa;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .navigation {{
                    background: white;
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                    text-align: center;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .nav-button {{
                    display: inline-block;
                    margin: 5px;
                    padding: 10px 20px;
                    background: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: background 0.3s;
                }}
                .nav-button:hover {{
                    background: #5a6fd8;
                }}
                .section {{
                    margin-bottom: 40px;
                }}
                .section-title {{
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .summary-cards {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .card {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    text-align: center;
                }}
                .card h3 {{
                    margin-top: 0;
                    color: #667eea;
                }}
                .amount {{
                    font-size: 1.5em;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .positive {{ color: #28a745; }}
                .negative {{ color: #dc3545; }}
                .neutral {{ color: #6c757d; }}
                .charts {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                    gap: 30px;
                    margin-bottom: 30px;
                }}
                .chart {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    text-align: center;
                }}
                .chart img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 5px;
                }}
                .period-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                    gap: 25px;
                    margin: 20px 0;
                }}
                .period-card {{
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .period-header {{
                    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                    color: #333;
                    padding: 15px;
                    font-weight: bold;
                    text-align: center;
                }}
                .period-content {{
                    padding: 20px;
                }}
                .period-summary {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                    gap: 10px;
                    margin-bottom: 15px;
                }}
                .mini-card {{
                    background: #f8f9fa;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: center;
                }}
                .mini-amount {{
                    font-weight: bold;
                    font-size: 0.9em;
                }}
                .details {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }}
                .category-list {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 10px;
                }}
                .category-item {{
                    display: flex;
                    justify-content: space-between;
                    padding: 8px;
                    background: #f8f9fa;
                    border-radius: 5px;
                }}
                .generated-time {{
                    text-align: center;
                    color: #666;
                    font-style: italic;
                    margin-top: 30px;
                }}
                .collapsible {{
                    cursor: pointer;
                    user-select: none;
                }}
                .collapsible:hover {{
                    opacity: 0.8;
                }}
                .collapsed {{
                    display: none;
                }}
            </style>
            <script>
                function toggleSection(sectionId) {{
                    const element = document.getElementById(sectionId);
                    if (element.style.display === 'none') {{
                        element.style.display = 'block';
                    }} else {{
                        element.style.display = 'none';
                    }}
                }}
            </script>
        </head>
        <body>
            <div class="header">
                <h1>💰 Comprehensive Financial Analysis Report</h1>
                <p>Complete overview with monthly and yearly breakdowns</p>
            </div>
            
            <div class="navigation">
                <a href="#overview" class="nav-button">📊 Overview</a>
                <a href="#monthly" class="nav-button">📅 Monthly Reports</a>
                <a href="#yearly" class="nav-button">📆 Yearly Reports</a>
                <a href="#detailed" class="nav-button">📈 Detailed Analysis</a>
            </div>
            
            <!-- Overview Section -->
            <div id="overview" class="section">
                <div class="section-title">
                    <h2>📊 Financial Overview</h2>
                </div>
                
                <div class="summary-cards">
                    <div class="card">
                        <h3>💵 Total Income</h3>
                        <div class="amount positive">{all_time_results['total_income']:,.2f} EGP</div>
                        <small>Excludes loan repayments</small>
                    </div>
                    <div class="card">
                        <h3>💸 Total Spending</h3>
                        <div class="amount negative">{all_time_results['total_spending']:,.2f} EGP</div>
                        <small>Adjusted for lending</small>
                    </div>
                    <div class="card">
                        <h3>📊 Net Balance</h3>
                        <div class="amount {'positive' if all_time_results['net_balance'] >= 0 else 'negative'}">
                            {all_time_results['net_balance']:,.2f} EGP
                        </div>
                    </div>
                    <div class="card">
                        <h3>🎯 Avg Transaction</h3>
                        <div class="amount">{all_time_results['avg_transaction']:,.2f} EGP</div>
                    </div>
                    <div class="card">
                        <h3>❤️ Charity Spending</h3>
                        <div class="amount" style="color: #ff6b6b;">{all_time_results['charity_spending']:,.2f} EGP</div>
                        <small>{all_time_results['charity_percentage']:.1f}% of spending</small>
                    </div>
                    <div class="card">
                        <h3>💼 Spending (No Charity)</h3>
                        <div class="amount negative">{all_time_results['spending_excluding_charity']:,.2f} EGP</div>
                    </div>
                </div>
                
                <div class="charts">"""
        
        # Add main charts
        for chart_file, chart_title in chart_files:
            html += f"""
                    <div class="chart">
                        <h3>{chart_title}</h3>
                        <img src="charts/{chart_file}" alt="{chart_title}">
                    </div>"""
        
        html += """
                </div>
                
                <!-- Spending Analysis Charts Section -->
                <div class="section">
                    <div class="section-title">
                        📊 Spending Analysis Charts
                    </div>
                    <div class="charts">"""
        
        # Add new spending analysis charts
        for chart_file, chart_title in new_chart_files:
            html += f"""
                        <div class="chart">
                            <h3>{chart_title}</h3>
                            <img src="charts/{chart_file}" alt="{chart_title}">
                        </div>"""
        
        html += """
                    </div>
                </div>
            </div>
            
            <!-- Monthly Reports Section -->
            <div id="monthly" class="section">
                <div class="section-title collapsible" onclick="toggleSection('monthly-content')">
                    <h2>📅 Monthly Financial Reports</h2>
                    <p>Click to expand/collapse detailed monthly analysis</p>
                </div>
                
                <div id="monthly-content" class="period-grid">"""
        
        # Add monthly reports
        for chart_file, month, data in monthly_chart_files:
            html += f"""
                    <div class="period-card">
                        <div class="period-header">
                            📅 {month}
                        </div>
                        <div class="period-content">
                            <div class="period-summary">
                                <div class="mini-card">
                                    <div>Income</div>
                                    <div class="mini-amount positive">{data['total_income']:,.0f} EGP</div>
                                </div>
                                <div class="mini-card">
                                    <div>Spending</div>
                                    <div class="mini-amount negative">{data['total_spending']:,.0f} EGP</div>
                                </div>
                                <div class="mini-card">
                                    <div>Balance</div>
                                    <div class="mini-amount {'positive' if data['net_balance'] >= 0 else 'negative'}">{data['net_balance']:,.0f} EGP</div>
                                </div>
                                <div class="mini-card">
                                    <div>Outstanding Lending</div>
                                    <div class="mini-amount neutral">{data.get('outstanding_lending', 0):,.0f} EGP</div>
                                </div>
                                <div class="mini-card">
                                    <div>Excess Repayment</div>
                                    <div class="mini-amount positive">{data.get('excess_repayment', 0):,.0f} EGP</div>
                                </div>
                            </div>
                            <div class="chart">
                                <img src="charts/{chart_file}" alt="Spending in {month}">
                            </div>
                            
                            <!-- Detailed Breakdown for this month -->
                            <div class="details" style="margin-top: 15px;">
                                <h4>� Simplified Spending Categories</h4>
                                <div class="category-list">
                                    <div class="category-item">
                                        <span>💝 Charity</span>
                                        <span style="color: #ff6b6b;">{data.get('simplified_spending', {}).get('charity', 0):,.2f} EGP</span>
                                    </div>
                                    <div class="category-item">
                                        <span>💰 Lending</span>
                                        <span class="neutral">{data.get('simplified_spending', {}).get('lending', 0):,.2f} EGP</span>
                                    </div>
                                    <div class="category-item">
                                        <span>🛍️ Normal Spending</span>
                                        <span class="negative">{data.get('simplified_spending', {}).get('normal', 0):,.2f} EGP</span>
                                    </div>
                                </div>
                                
                                <h4>💰 Lending Details</h4>
                                <div class="category-list">
                                    <div class="category-item">
                                        <span>Outstanding Lending</span>
                                        <span class="negative">{data.get('outstanding_lending', 0):,.2f} EGP</span>
                                    </div>
                                    <div class="category-item">
                                        <span>Excess Repayment</span>
                                        <span class="positive">{data.get('excess_repayment', 0):,.2f} EGP</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>"""
        
        html += """
                </div>
            </div>
            
            <!-- Yearly Reports Section -->
            <div id="yearly" class="section">
                <div class="section-title collapsible" onclick="toggleSection('yearly-content')">
                    <h2>📆 Yearly Financial Reports</h2>
                    <p>Click to expand/collapse detailed yearly analysis</p>
                </div>
                
                <div id="yearly-content" class="period-grid">"""
        
        # Add yearly reports
        for chart_file, year, data in yearly_chart_files:
            html += f"""
                    <div class="period-card">
                        <div class="period-header">
                            📆 {year}
                        </div>
                        <div class="period-content">
                            <div class="period-summary">
                                <div class="mini-card">
                                    <div>Income</div>
                                    <div class="mini-amount positive">{data['total_income']:,.0f} EGP</div>
                                </div>
                                <div class="mini-card">
                                    <div>Spending</div>
                                    <div class="mini-amount negative">{data['total_spending']:,.0f} EGP</div>
                                </div>
                                <div class="mini-card">
                                    <div>Balance</div>
                                    <div class="mini-amount {'positive' if data['net_balance'] >= 0 else 'negative'}">{data['net_balance']:,.0f} EGP</div>
                                </div>
                                <div class="mini-card">
                                    <div>Transactions</div>
                                    <div class="mini-amount">{data['transaction_count']:,}</div>
                                </div>
                                <div class="mini-card">
                                    <div>Outstanding Lending</div>
                                    <div class="mini-amount neutral">{data.get('outstanding_lending', 0):,.0f} EGP</div>
                                </div>
                                <div class="mini-card">
                                    <div>Excess Repayment</div>
                                    <div class="mini-amount positive">{data.get('excess_repayment', 0):,.0f} EGP</div>
                                </div>
                            </div>
                            <div class="chart">
                                <img src="charts/{chart_file}" alt="Spending in {year}">
                            </div>
                            
                            <!-- Detailed Breakdown for this year -->
                            <div class="details" style="margin-top: 15px;">
                                <h4>� Simplified Spending Categories</h4>
                                <div class="category-list">
                                    <div class="category-item">
                                        <span>💝 Charity</span>
                                        <span style="color: #ff6b6b;">{data.get('simplified_spending', {}).get('charity', 0):,.2f} EGP</span>
                                    </div>
                                    <div class="category-item">
                                        <span>💰 Lending</span>
                                        <span class="neutral">{data.get('simplified_spending', {}).get('lending', 0):,.2f} EGP</span>
                                    </div>
                                    <div class="category-item">
                                        <span>🛍️ Normal Spending</span>
                                        <span class="negative">{data.get('simplified_spending', {}).get('normal', 0):,.2f} EGP</span>
                                    </div>
                                </div>
                                
                                <h4>💰 Lending Details</h4>
                                <div class="category-list">
                                    <div class="category-item">
                                        <span>Outstanding Lending</span>
                                        <span class="negative">{data.get('outstanding_lending', 0):,.2f} EGP</span>
                                    </div>
                                    <div class="category-item">
                                        <span>Excess Repayment</span>
                                        <span class="positive">{data.get('excess_repayment', 0):,.2f} EGP</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>"""
        
        html += """
                </div>
            </div>
            
            <!-- Detailed Analysis Section -->
            <div id="detailed" class="section">
                <div class="section-title">
                    <h2>📈 Detailed Breakdown</h2>
                </div>
                
                <div class="details">
                    <h3>Spending by Category</h3>
                    <div class="category-list">"""
        
        # Add spending categories
        for category, amount in sorted(all_time_results['spending_by_category'].items(), 
                                     key=lambda x: x[1], reverse=True):
            html += f"""
                        <div class="category-item">
                            <span>{category}</span>
                            <span class="negative">{amount:,.2f} EGP</span>
                        </div>"""
        
        html += """
                    </div>
                    
                    <h3>Income by Category</h3>
                    <div class="category-list">"""
        
        # Add income categories
        for category, amount in sorted(all_time_results['income_by_category'].items(), 
                                     key=lambda x: x[1], reverse=True):
            html += f"""
                        <div class="category-item">
                            <span>{category}</span>
                            <span class="positive">{amount:,.2f} EGP</span>
                        </div>"""
        
        html += f"""
                    </div>
                    
                    <h3>💰 Lending Summary</h3>
                    <div class="lending-info">
                        <div class="category-item">
                            <span>Total Lending</span>
                            <span class="neutral">{all_time_results.get('total_lending', 0):,.2f} EGP</span>
                        </div>
                        <div class="category-item">
                            <span>Repaid Lending</span>
                            <span class="positive">{all_time_results.get('repaid_lending', 0):,.2f} EGP</span>
                        </div>
                        <div class="category-item">
                            <span>Outstanding Lending</span>
                            <span class="negative">{all_time_results.get('outstanding_lending', 0):,.2f} EGP</span>
                        </div>
                        <div class="category-item">
                            <span>Excess Repayment</span>
                            <span class="positive">{all_time_results.get('excess_repayment', 0):,.2f} EGP</span>
                        </div>
                    </div>
                    
                    <h3>❤️ Charity Breakdown</h3>
                    <div class="charity-info">
                        <div class="category-item">
                            <span>Charity Spending</span>
                            <span style="color: #ff6b6b;">{all_time_results.get('charity_spending', 0):,.2f} EGP</span>
                        </div>
                        <div class="category-item">
                            <span>% of Total Spending</span>
                            <span style="color: #ff6b6b;">{all_time_results.get('charity_percentage', 0):,.1f}%</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="generated-time">
                Report generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
            </div>
        </body>
        </html>
        """
        
        return html


class CSVReportGenerator(ReportGenerator):
    """Generates CSV reports for data export."""
    
    def generate(self, analyzer, output_path="financial_analysis.csv"):
        """Generate CSV report."""
        all_time_results = analyzer.analyze_all_time()
        
        # Create summary data
        import pandas as pd
        
        summary_data = []
        
        # Add spending categories
        for category, amount in all_time_results['spending_by_category'].items():
            summary_data.append({
                'Type': 'Spending',
                'Category': category,
                'Amount': amount
            })
        
        # Add income categories
        for category, amount in all_time_results['income_by_category'].items():
            summary_data.append({
                'Type': 'Income',
                'Category': category,
                'Amount': amount
            })
        
        # Add totals
        summary_data.extend([
            {'Type': 'Total', 'Category': 'Total Income', 'Amount': all_time_results['total_income']},
            {'Type': 'Total', 'Category': 'Total Spending', 'Amount': all_time_results['total_spending']},
            {'Type': 'Total', 'Category': 'Net Balance', 'Amount': all_time_results['net_balance']},
        ])
        
        df = pd.DataFrame(summary_data)
        df.to_csv(output_path, index=False)
        
        print(f"📊 CSV report generated: {output_path}")
        return output_path
