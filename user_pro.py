"""
User profile management system with risk tolerance assessment.
Stores and retrieves user profiles from Firebase Firestore.
"""
import uuid
from datetime import datetime
from typing import Dict, List, Optional, TypedDict
from enum import Enum
import logging
from dataclasses import dataclass, asdict
import numpy as np

from firebase_config import firebase_manager

logger = logging.getLogger(__name__)

class RiskToleranceLevel(Enum):
    """Risk tolerance classification"""
    CONSERVATIVE = 1
    MODERATE = 2
    AGGRESSIVE = 3
    SPECULATIVE = 4

class InvestmentGoal(Enum):
    """Investment goal categories"""
    CAPITAL_PRESERVATION = "capital_preservation"
    INCOME_GENERATION = "income_generation"
    CAPITAL_GROWTH = "capital_growth"
    SPECULATIVE_GAINS = "speculative_gains"

class TradingExperience(Enum):
    """User trading experience levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PROFESSIONAL = "professional"

@dataclass
class RiskAssessment:
    """Risk assessment metrics"""
    max_drawdown_tolerance: float  # Percentage (0-100)
    volatility_tolerance: float    # Annualized volatility percentage
    loss_aversion_score: float     # 0-1 scale
    time_horizon_years: int
    liquidity_needs: float         # Monthly liquidity requirement

@dataclass
class UserProfile:
    """Complete user profile for trading personalization"""
    user_id: str
    email: str
    risk_tolerance: Risk