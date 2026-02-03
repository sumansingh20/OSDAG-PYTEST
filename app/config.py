# Partial Safety Factors for Loads
GAMMA_DL = 1.5      # Dead load factor
GAMMA_LL = 1.5      # Live load factor  
GAMMA_WL = 1.5      # Wind load factor
GAMMA_EQ = 1.5      # Earthquake load factor

# Partial Safety Factors for Material
GAMMA_M0 = 1.10     # For yielding and buckling
GAMMA_M1 = 1.25     # For ultimate stress

# Material Properties
ELASTIC_MODULUS = 200000  # MPa (Steel)

# =============================================================================
# Load Combination Types
# =============================================================================

LOAD_COMBINATIONS = {
    'normal': {
        'description': 'Dead Load + Live Load',
        'dl_factor': GAMMA_DL,
        'll_factor': GAMMA_LL
    },
    'wind': {
        'description': 'Dead Load + Live Load + Wind Load',
        'combined_factor': 1.2
    },
    'seismic': {
        'description': 'Dead Load + Live Load + Earthquake Load',
        'combined_factor': 1.2
    }
}

# =============================================================================
# Steel Grade Database (as per IS 2062)
# =============================================================================

STEEL_GRADES = {
    'E250': {
        'yield_strength': 250,      # MPa
        'ultimate_strength': 410,   # MPa
        'elongation': 23,           # %
        'description': 'Mild Steel (Standard)'
    },
    'E275': {
        'yield_strength': 275,
        'ultimate_strength': 430,
        'elongation': 22,
        'description': 'Medium Carbon Steel'
    },
    'E300': {
        'yield_strength': 300,
        'ultimate_strength': 440,
        'elongation': 22,
        'description': 'Medium Strength Steel'
    },
    'E350': {
        'yield_strength': 350,
        'ultimate_strength': 490,
        'elongation': 22,
        'description': 'High Strength Steel'
    },
    'E410': {
        'yield_strength': 410,
        'ultimate_strength': 540,
        'elongation': 20,
        'description': 'High Strength Low Alloy'
    },
    'E450': {
        'yield_strength': 450,
        'ultimate_strength': 570,
        'elongation': 20,
        'description': 'Extra High Strength'
    },
    'FE410': {
        'yield_strength': 250,
        'ultimate_strength': 410,
        'elongation': 23,
        'description': 'Fe410 Grade (Legacy)'
    },
    'FE490': {
        'yield_strength': 350,
        'ultimate_strength': 490,
        'elongation': 22,
        'description': 'Fe490 Grade (Legacy)'
    }
}

# =============================================================================
# Deflection Limits
# =============================================================================

DEFLECTION_LIMITS = {
    'industrial': 240,      # L/240 for industrial buildings
    'normal': 300,          # L/300 for normal buildings
    'sensitive': 360,       # L/360 for sensitive finishes
    'cantilever': 150       # L/150 for cantilevers
}

# =============================================================================
# Application Configuration Classes
# =============================================================================

class BaseConfig:
    """Base configuration class."""
    SECRET_KEY = 'osdag-structural-dashboard-secret-key'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
