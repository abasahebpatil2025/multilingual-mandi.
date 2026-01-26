"""
CropRate data model for the Multilingual Mandi application.

This module defines the data structure for crop pricing information
including current rates, market location, and trend data.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class CropRate:
    """Data model for crop market rate information."""
    
    crop_name: str
    current_price: float
    unit: str
    market_location: str
    last_updated: datetime
    trend: str  # "up", "down", "stable"
    historical_data: Optional[List[float]] = None
    
    def __post_init__(self):
        """Validate data after initialization."""
        if self.current_price < 0:
            raise ValueError("Current price cannot be negative")
        
        if self.trend not in ["up", "down", "stable"]:
            raise ValueError("Trend must be 'up', 'down', or 'stable'")
        
        if not self.crop_name.strip():
            raise ValueError("Crop name cannot be empty")
        
        if not self.unit.strip():
            raise ValueError("Unit cannot be empty")
        
        if not self.market_location.strip():
            raise ValueError("Market location cannot be empty")
    
    def get_price_per_unit(self) -> str:
        """
        Get formatted price per unit string.
        
        Returns:
            str: Formatted price string
        """
        return f"₹{self.current_price:.2f} per {self.unit}"
    
    def get_trend_indicator(self) -> str:
        """
        Get trend indicator symbol.
        
        Returns:
            str: Trend symbol (↑, ↓, →)
        """
        trend_symbols = {
            "up": "↑",
            "down": "↓", 
            "stable": "→"
        }
        return trend_symbols.get(self.trend, "→")
    
    def is_data_fresh(self, max_age_hours: int = 24) -> bool:
        """
        Check if the rate data is fresh (within specified hours).
        
        Args:
            max_age_hours (int): Maximum age in hours for fresh data
            
        Returns:
            bool: True if data is fresh, False otherwise
        """
        age = datetime.now() - self.last_updated
        return age.total_seconds() < (max_age_hours * 3600)