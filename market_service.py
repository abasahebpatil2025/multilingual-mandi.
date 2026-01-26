"""
Market Rate Service for Multilingual Mandi
Provides current and historical market pricing data
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

@dataclass
class CropRate:
    """Data model for crop pricing information"""
    crop_name: str
    current_price: float
    unit: str
    market_location: str
    last_updated: datetime
    trend: str  # "up", "down", "stable"
    historical_data: List[float] = None
    
    def __post_init__(self):
        if self.historical_data is None:
            # Generate some mock historical data
            base_price = self.current_price
            self.historical_data = [
                base_price + random.uniform(-200, 200) for _ in range(7)
            ]

class MarketRateService:
    """Service for managing market rate data"""
    
    def __init__(self):
        self.mock_data = self._initialize_mock_data()
    
    def _initialize_mock_data(self) -> Dict[str, CropRate]:
        """Initialize mock data for Indian agricultural markets"""
        current_time = datetime.now()
        
        mock_crops = {
            "wheat": CropRate(
                crop_name="Wheat (गहूं)",
                current_price=2500.0,
                unit="quintal",
                market_location="Pune Mandi",
                last_updated=current_time,
                trend="up"
            ),
            "rice": CropRate(
                crop_name="Rice (चावल)",
                current_price=3200.0,
                unit="quintal", 
                market_location="Mumbai Mandi",
                last_updated=current_time,
                trend="stable"
            ),
            "onion": CropRate(
                crop_name="Onion (कांदा)",
                current_price=1800.0,
                unit="quintal",
                market_location="Nashik Mandi",
                last_updated=current_time,
                trend="down"
            ),
            "tomato": CropRate(
                crop_name="Tomato (टमाटर)",
                current_price=2200.0,
                unit="quintal",
                market_location="Pune Mandi", 
                last_updated=current_time,
                trend="up"
            ),
            "potato": CropRate(
                crop_name="Potato (बटाटा)",
                current_price=1500.0,
                unit="quintal",
                market_location="Delhi Mandi",
                last_updated=current_time,
                trend="stable"
            ),
            "sugarcane": CropRate(
                crop_name="Sugarcane (ऊस)",
                current_price=350.0,
                unit="quintal",
                market_location="Kolhapur Mandi",
                last_updated=current_time,
                trend="up"
            ),
            "cotton": CropRate(
                crop_name="Cotton (कापूस)",
                current_price=5800.0,
                unit="quintal",
                market_location="Nagpur Mandi",
                last_updated=current_time,
                trend="down"
            ),
            "soybean": CropRate(
                crop_name="Soybean (सोयाबीन)",
                current_price=4200.0,
                unit="quintal",
                market_location="Indore Mandi",
                last_updated=current_time,
                trend="stable"
            )
        }
        
        return mock_crops
    
    def get_current_rates(self) -> Dict[str, CropRate]:
        """Get all current market rates"""
        return self.mock_data.copy()
    
    def get_rate_by_crop(self, crop_name: str) -> Optional[CropRate]:
        """
        Get rate for specific crop
        
        Args:
            crop_name: Name of the crop
            
        Returns:
            CropRate object or None if not found
        """
        crop_key = crop_name.lower().replace(" ", "")
        return self.mock_data.get(crop_key)
    
    def get_historical_trends(self, crop_name: str, days: int = 7) -> List[float]:
        """
        Get historical price trends for a crop
        
        Args:
            crop_name: Name of the crop
            days: Number of days of historical data
            
        Returns:
            List of historical prices
        """
        crop = self.get_rate_by_crop(crop_name)
        if crop and crop.historical_data:
            return crop.historical_data[-days:] if len(crop.historical_data) >= days else crop.historical_data
        return []
    
    def update_mock_data(self):
        """Update mock data with slight price variations"""
        for crop_key, crop in self.mock_data.items():
            # Simulate price fluctuations
            variation = random.uniform(-0.05, 0.05)  # ±5% variation
            new_price = crop.current_price * (1 + variation)
            
            # Update price and trend
            if new_price > crop.current_price:
                crop.trend = "up"
            elif new_price < crop.current_price:
                crop.trend = "down"
            else:
                crop.trend = "stable"
                
            crop.current_price = round(new_price, 2)
            crop.last_updated = datetime.now()
            
            # Add to historical data
            if crop.historical_data:
                crop.historical_data.append(new_price)
                # Keep only last 30 days
                if len(crop.historical_data) > 30:
                    crop.historical_data = crop.historical_data[-30:]
    
    def search_crops(self, query: str) -> List[CropRate]:
        """
        Search crops by name
        
        Args:
            query: Search query
            
        Returns:
            List of matching crops
        """
        query = query.lower()
        results = []
        
        for crop in self.mock_data.values():
            if query in crop.crop_name.lower():
                results.append(crop)
                
        return results
    
    def get_trending_crops(self, trend_type: str = "up") -> List[CropRate]:
        """
        Get crops with specific trend
        
        Args:
            trend_type: "up", "down", or "stable"
            
        Returns:
            List of crops with the specified trend
        """
        return [crop for crop in self.mock_data.values() if crop.trend == trend_type]