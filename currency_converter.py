"""
Currency conversion module for the financial analysis system.
Handles real-time currency conversion with caching and fallback mechanisms.
"""

import requests
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging

from config import CURRENCY_CONFIG


class CurrencyConverter:
    """Handles currency conversion with real-time rates and caching."""
    
    def __init__(self):
        self.base_currency = CURRENCY_CONFIG['base_currency']
        self.api_url = CURRENCY_CONFIG['api_url']
        self.cache_duration = CURRENCY_CONFIG['cache_duration']
        self.fallback_rates = CURRENCY_CONFIG['fallback_rates']
        self.supported_currencies = CURRENCY_CONFIG['supported_currencies']
        self.currency_symbols = CURRENCY_CONFIG['currency_symbols']
        
        # Cache file for storing exchange rates
        self.cache_file = Path("currency_cache.json")
        self.rates_cache = {}
        self.cache_timestamp = None
        
        # Load cached rates if available
        self._load_cache()
    
    def _load_cache(self):
        """Load cached exchange rates from file."""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                    self.rates_cache = cache_data.get('rates', {})
                    cache_time_str = cache_data.get('timestamp')
                    if cache_time_str:
                        self.cache_timestamp = datetime.fromisoformat(cache_time_str)
        except Exception as e:
            print(f"⚠️  Warning: Could not load currency cache: {e}")
            self.rates_cache = {}
            self.cache_timestamp = None
    
    def _save_cache(self):
        """Save current exchange rates to cache file."""
        try:
            cache_data = {
                'rates': self.rates_cache,
                'timestamp': self.cache_timestamp.isoformat() if self.cache_timestamp else None
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f)
        except Exception as e:
            print(f"⚠️  Warning: Could not save currency cache: {e}")
    
    def _is_cache_valid(self):
        """Check if the cached rates are still valid."""
        if not self.cache_timestamp or not self.rates_cache:
            return False
        
        time_diff = datetime.now() - self.cache_timestamp
        return time_diff.total_seconds() < self.cache_duration
    
    def _fetch_rates_from_api(self):
        """Fetch current exchange rates from API."""
        try:
            print(f"🌐 Fetching current exchange rates for {self.base_currency}...")
            response = requests.get(f"{self.api_url}{self.base_currency}", timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rates = data.get('rates', {})
            
            if rates:
                self.rates_cache = rates
                self.cache_timestamp = datetime.now()
                self._save_cache()
                print(f"✅ Successfully updated exchange rates (cached for {self.cache_duration/3600:.1f} hours)")
                return True
            else:
                print("⚠️  API response does not contain rates data")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Network error fetching exchange rates: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"⚠️  Error parsing exchange rate data: {e}")
            return False
        except Exception as e:
            print(f"⚠️  Unexpected error fetching exchange rates: {e}")
            return False
    
    def _get_exchange_rate(self, from_currency, to_currency):
        """Get exchange rate between two currencies."""
        if from_currency == to_currency:
            return 1.0
        
        # Try to get rates from cache or API
        if not self._is_cache_valid():
            self._fetch_rates_from_api()
        
        # If we have cached rates, use them
        if self.rates_cache:
            try:
                if to_currency == self.base_currency:
                    # Converting to base currency
                    return 1.0 / self.rates_cache.get(from_currency, 1.0)
                elif from_currency == self.base_currency:
                    # Converting from base currency
                    return self.rates_cache.get(to_currency, 1.0)
                else:
                    # Converting between two non-base currencies
                    # Convert through base currency
                    to_base = 1.0 / self.rates_cache.get(from_currency, 1.0)
                    to_target = self.rates_cache.get(to_currency, 1.0)
                    return to_base * to_target
            except (KeyError, ZeroDivisionError):
                pass
        
        # Fall back to hardcoded rates
        print(f"⚠️  Using fallback exchange rates for {from_currency} to {to_currency}")
        
        if to_currency == self.base_currency:
            return 1.0 / self.fallback_rates.get(from_currency, 1.0)
        elif from_currency == self.base_currency:
            return self.fallback_rates.get(to_currency, 1.0)
        else:
            # Convert through USD
            to_usd = 1.0 / self.fallback_rates.get(from_currency, 1.0)
            to_target = self.fallback_rates.get(to_currency, 1.0)
            return to_usd * to_target
    
    def convert_amount(self, amount, from_currency, to_currency=None):
        """Convert an amount from one currency to another."""
        if to_currency is None:
            to_currency = self.base_currency
        
        if from_currency == to_currency:
            return amount
        
        try:
            rate = self._get_exchange_rate(from_currency, to_currency)
            converted_amount = amount * rate
            return round(converted_amount, 2)
        except Exception as e:
            print(f"⚠️  Error converting {amount} {from_currency} to {to_currency}: {e}")
            return amount  # Return original amount if conversion fails
    
    def detect_currency_from_text(self, text):
        """Detect currency from text or symbols."""
        text = str(text).upper().strip()
        
        # Check for currency codes
        for currency in self.supported_currencies:
            if currency in text:
                return currency
        
        # Check for currency symbols
        for currency, symbol in self.currency_symbols.items():
            if symbol in str(text):
                return currency
        
        # Default to base currency
        return self.base_currency
    
    def format_amount(self, amount, currency=None):
        """Format amount with appropriate currency symbol."""
        if currency is None:
            currency = self.base_currency
        
        symbol = self.currency_symbols.get(currency, currency)
        
        # Handle different currency formatting conventions
        if currency in ['EUR', 'INR', 'BRL']:
            return f"{amount:,.2f} {symbol}"
        else:
            return f"{symbol}{amount:,.2f}"
    
    def get_conversion_summary(self):
        """Get a summary of available conversion rates."""
        if not self._is_cache_valid():
            self._fetch_rates_from_api()
        
        summary = {
            'base_currency': self.base_currency,
            'last_updated': self.cache_timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.cache_timestamp else 'Never',
            'cache_valid': self._is_cache_valid(),
            'available_rates': len(self.rates_cache),
            'supported_currencies': self.supported_currencies
        }
        
        return summary
    
    def refresh_rates(self):
        """Manually refresh exchange rates."""
        success = self._fetch_rates_from_api()
        return success


# Global converter instance
currency_converter = CurrencyConverter()
