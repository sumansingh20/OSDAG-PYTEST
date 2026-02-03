import math
from .config import (
    GAMMA_DL, GAMMA_LL, GAMMA_WL, GAMMA_EQ,
    GAMMA_M0, GAMMA_M1, ELASTIC_MODULUS,
    STEEL_GRADES, DEFLECTION_LIMITS
)
from .validators import (
    validate_load_inputs, validate_combination_type,
    validate_safety_factor_inputs, validate_utilization_inputs,
    validate_moment_inputs, validate_deflection_inputs,
    validate_shear_inputs, validate_steel_grade,
    ValidationError
)


# =============================================================================
# Load Combination Functions
# =============================================================================

def calculate_factored_load(dead_load, live_load, wind_load=0.0, 
                            earthquake_load=0.0, combination_type="normal"):
    # Validate inputs
    dl, ll, wl, eq = validate_load_inputs(dead_load, live_load, wind_load, earthquake_load)
    combo = validate_combination_type(combination_type)
    
    # Calculate based on combination type
    if combo == "normal":
        factored_dl = GAMMA_DL * dl
        factored_ll = GAMMA_LL * ll
        factored_load = factored_dl + factored_ll
        components = {
            'factored_dead_load': round(factored_dl, 2),
            'factored_live_load': round(factored_ll, 2)
        }
    
    elif combo == "wind":
        factored_load = 1.2 * (dl + ll + wl)
        components = {
            'combined_load': round(dl + ll + wl, 2),
            'factor_applied': 1.2
        }
    
    elif combo == "seismic":
        factored_load = 1.2 * (dl + ll + eq)
        components = {
            'combined_load': round(dl + ll + eq, 2),
            'factor_applied': 1.2
        }
    
    return {
        'factored_load': round(factored_load, 2),
        'combination_type': combo,
        'components': components,
        'unit': 'kN'
    }


# =============================================================================
# Safety Factor Functions
# =============================================================================

def check_safety_factor(applied_stress, allowable_stress, min_safety_factor=1.0):
    # Validate inputs
    app_stress, allow_stress, min_sf = validate_safety_factor_inputs(
        applied_stress, allowable_stress, min_safety_factor
    )
    
    # Calculate safety factor
    safety_factor = allow_stress / app_stress
    is_safe = safety_factor >= min_sf
    margin = ((safety_factor - min_sf) / min_sf) * 100
    
    return {
        'safety_factor': round(safety_factor, 3),
        'is_safe': is_safe,
        'margin': round(margin, 2),
        'status': 'SAFE' if is_safe else 'UNSAFE',
        'applied_stress': app_stress,
        'allowable_stress': allow_stress,
        'minimum_required': min_sf
    }


# =============================================================================
# Section Capacity Functions
# =============================================================================

def calculate_section_utilization(applied_load, section_capacity):
    # Validate inputs
    load, capacity = validate_utilization_inputs(applied_load, section_capacity)
    
    # Calculate utilization
    utilization_ratio = load / capacity
    is_adequate = utilization_ratio <= 1.0
    reserve_capacity = max(0, (1.0 - utilization_ratio) * 100)
    
    # Determine status
    if utilization_ratio <= 0.7:
        status = 'UNDER-UTILIZED'
    elif utilization_ratio <= 1.0:
        status = 'ADEQUATE'
    elif utilization_ratio <= 1.1:
        status = 'MARGINALLY OVERSTRESSED'
    else:
        status = 'OVERSTRESSED'
    
    return {
        'utilization_ratio': round(utilization_ratio, 4),
        'utilization_percent': round(utilization_ratio * 100, 2),
        'is_adequate': is_adequate,
        'reserve_capacity': round(reserve_capacity, 2),
        'status': status,
        'applied_load': load,
        'section_capacity': capacity
    }


def calculate_moment_capacity(yield_strength, plastic_modulus):
    # Validate inputs
    fy, zpz = validate_moment_inputs(yield_strength, plastic_modulus)
    
    # Calculate moment capacity
    moment_nmm = (fy * zpz) / GAMMA_M0  # N-mm
    moment_knm = moment_nmm / 1e6  # Convert to kN-m
    
    return {
        'moment_capacity_nmm': round(moment_nmm, 2),
        'moment_capacity_knm': round(moment_knm, 2),
        'yield_strength': fy,
        'plastic_modulus': zpz,
        'gamma_m0': GAMMA_M0,
        'unit': 'kN-m'
    }


# =============================================================================
# Serviceability Functions
# =============================================================================

def check_deflection_serviceability(actual_deflection, span_length, 
                                     deflection_limit_ratio=300):
    # Validate inputs
    deflection, span, limit_ratio = validate_deflection_inputs(
        actual_deflection, span_length, deflection_limit_ratio
    )
    
    # Calculate allowable deflection
    allowable = span / limit_ratio
    is_serviceable = deflection <= allowable
    utilization = deflection / allowable if allowable > 0 else 0
    
    # Determine status
    if is_serviceable:
        if utilization <= 0.8:
            status = 'WELL WITHIN LIMITS'
        else:
            status = 'WITHIN LIMITS'
    else:
        status = 'EXCEEDS LIMITS'
    
    return {
        'allowable_deflection': round(allowable, 2),
        'actual_deflection': deflection,
        'is_serviceable': is_serviceable,
        'utilization': round(utilization, 4),
        'utilization_percent': round(utilization * 100, 2),
        'status': status,
        'span_length': span,
        'limit_ratio': f'L/{limit_ratio}',
        'unit': 'mm'
    }


# =============================================================================
# Shear Capacity Functions
# =============================================================================

def calculate_shear_capacity(yield_strength, shear_area):
    # Validate inputs
    fy, av = validate_shear_inputs(yield_strength, shear_area)
    
    # Calculate shear capacity
    shear_n = (fy * av) / (math.sqrt(3) * GAMMA_M0)  # Newtons
    shear_kn = shear_n / 1000  # Convert to kN
    
    return {
        'shear_capacity_n': round(shear_n, 2),
        'shear_capacity_kn': round(shear_kn, 2),
        'yield_strength': fy,
        'shear_area': av,
        'gamma_m0': GAMMA_M0,
        'unit': 'kN'
    }


# =============================================================================
# Material Property Functions
# =============================================================================

def get_material_properties(steel_grade):
    # Validate input
    grade = validate_steel_grade(steel_grade)
    
    # Get properties from database
    properties = STEEL_GRADES[grade].copy()
    properties['grade'] = grade
    properties['elastic_modulus'] = ELASTIC_MODULUS
    
    return properties


# =============================================================================
# Combined Analysis Functions
# =============================================================================

def perform_complete_analysis(dead_load, live_load, applied_stress, 
                               allowable_stress, section_capacity,
                               combination_type='normal'):
    # Calculate factored load
    factored = calculate_factored_load(dead_load, live_load, 
                                       combination_type=combination_type)
    
    # Check safety factor
    safety = check_safety_factor(applied_stress, allowable_stress)
    
    # Check utilization
    utilization = calculate_section_utilization(
        factored['factored_load'], section_capacity
    )
    
    # Overall assessment
    is_acceptable = safety['is_safe'] and utilization['is_adequate']
    
    return {
        'factored_load_analysis': factored,
        'safety_factor_analysis': safety,
        'utilization_analysis': utilization,
        'overall_status': 'ACCEPTABLE' if is_acceptable else 'REVIEW REQUIRED',
        'is_acceptable': is_acceptable
    }
