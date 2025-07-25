"""
Data loading module for financial analysis system.
Handles loading financial data from various sources using ref_currency_amount.
"""

import pandas as pd
from pathlib import Path
from config import REPORT_CONFIG


class DataLoader:
    """Handles loading financial data from various sources."""
    
    def __init__(self):
        self.data = None
        self.file_path = None
        self.base_currency = REPORT_CONFIG['base_currency']
    
    def load_data(self, file_path):
        """Load and process data from Excel or CSV file using ref_currency_amount."""
        self.file_path = Path(file_path)
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"❌ File '{file_path}' not found. Please check the path.")
        
        try:
            # Load based on file extension
            if self.file_path.suffix.lower() in ['.xlsx', '.xls']:
                self.data = pd.read_excel(file_path)
            elif self.file_path.suffix.lower() == '.csv':
                self.data = pd.read_csv(file_path)
            else:
                raise ValueError(f"Unsupported file format: {self.file_path.suffix}")
            
            print(f"✅ Successfully loaded data from: {file_path}")
            print(f"📊 Data shape: {self.data.shape[0]} rows, {self.data.shape[1]} columns")
            
            # Process and clean the data
            self._clean_data()
            
            return self.data
            
        except Exception as e:
            raise Exception(f"❌ Error loading data: {str(e)}")
    
    def _clean_data(self):
        """Clean and prepare the loaded data using ref_currency_amount."""
        # Convert column names to lowercase for consistency
        self.data.columns = self.data.columns.str.lower().str.strip()
        
        # Check for required columns
        required_columns = ['date', 'category']
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Use ref_currency_amount if available, otherwise fall back to amount
        if 'ref_currency_amount' in self.data.columns:
            print(f"📊 Using ref_currency_amount column (currency: {self.base_currency})")
            self.data['amount'] = pd.to_numeric(self.data['ref_currency_amount'], errors='coerce')
        elif 'amount' in self.data.columns:
            print(f"⚠️  ref_currency_amount not found, using amount column")
            # Clean amount column if it contains currency symbols
            amount_str = self.data['amount'].astype(str)
            amount_cleaned = (amount_str
                             .str.replace('$', '', regex=False)
                             .str.replace('€', '', regex=False)
                             .str.replace('£', '', regex=False)
                             .str.replace('EGP', '', regex=False)
                             .str.replace(',', '', regex=False)
                             .str.strip())
            self.data['amount'] = pd.to_numeric(amount_cleaned, errors='coerce')
        else:
            raise ValueError("Neither 'ref_currency_amount' nor 'amount' column found")
        
        # Convert date to datetime
        self.data['date'] = pd.to_datetime(self.data['date'])
        
        # Remove rows with invalid amounts
        invalid_amounts = self.data['amount'].isna()
        if invalid_amounts.any():
            print(f"⚠️  Removed {invalid_amounts.sum()} rows with invalid amounts")
            self.data = self.data[~invalid_amounts]
        
        # Fill missing descriptions
        if 'description' not in self.data.columns:
            self.data['description'] = 'No description'
        else:
            self.data['description'] = self.data['description'].fillna('No description')
        
        # Set currency to base currency for all transactions
        self.data['currency'] = self.base_currency
        
        print(f"📊 All amounts processed in {self.base_currency}")
    
    @staticmethod
    def load_excel(file_path):
        """Legacy method for backward compatibility."""
        loader = DataLoader()
        return loader.load_data(file_path)
    
    @staticmethod
    def load_csv(file_path, **kwargs):
        """Legacy method for backward compatibility."""
        loader = DataLoader()
        return loader.load_data(file_path)
