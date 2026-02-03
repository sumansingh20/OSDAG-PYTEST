from .config import STEEL_GRADES, LOAD_COMBINATIONS, DEFLECTION_LIMITS


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_numeric(value, parameter_name, allow_zero=False, allow_negative=False):
    # Check if numeric
    if not isinstance(value, (int, float)):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValidationError(
                f"{parameter_name} must be a numeric value, got '{value}'"
            )
    
    # Check for negative
    if not allow_negative and value < 0:
        raise ValidationError(
            f"{parameter_name} cannot be negative, got {value}"
        )
    
    # Check for zero
    if not allow_zero and value == 0:
        raise ValidationError(
            f"{parameter_name} cannot be zero"
        )
    
    return float(value)


def validate_positive(value, parameter_name):
    validated = validate_numeric(value, parameter_name, allow_zero=False, allow_negative=False)
    return validated


def validate_non_negative(value, parameter_name):
    validated = validate_numeric(value, parameter_name, allow_zero=True, allow_negative=False)
    return validated


def validate_load_inputs(dead_load, live_load, wind_load=0.0, earthquake_load=0.0):
    dl = validate_non_negative(dead_load, "Dead Load")
    ll = validate_non_negative(live_load, "Live Load")
    wl = validate_non_negative(wind_load, "Wind Load")
    eq = validate_non_negative(earthquake_load, "Earthquake Load")
    
    return (dl, ll, wl, eq)


def validate_combination_type(combination_type):
    if not isinstance(combination_type, str):
        raise ValidationError(
            f"Combination type must be a string, got {type(combination_type).__name__}"
        )
    
    combo_type = combination_type.strip().lower()
    valid_types = list(LOAD_COMBINATIONS.keys())
    
    if combo_type not in valid_types:
        raise ValidationError(
            f"Invalid combination type: '{combination_type}'. "
            f"Must be one of: {', '.join(valid_types)}"
        )
    
    return combo_type


def validate_steel_grade(steel_grade):
    if not isinstance(steel_grade, str):
        raise ValidationError(
            f"Steel grade must be a string, got {type(steel_grade).__name__}"
        )
    
    grade = steel_grade.strip().upper()
    
    if grade not in STEEL_GRADES:
        available = ', '.join(sorted(STEEL_GRADES.keys()))
        raise ValidationError(
            f"Unknown steel grade: '{steel_grade}'. "
            f"Available grades: {available}"
        )
    
    return grade


def validate_deflection_category(category):
    if not isinstance(category, str):
        raise ValidationError(
            f"Deflection category must be a string, got {type(category).__name__}"
        )
    
    cat = category.strip().lower()
    valid_categories = list(DEFLECTION_LIMITS.keys())
    
    if cat not in valid_categories:
        raise ValidationError(
            f"Invalid deflection category: '{category}'. "
            f"Must be one of: {', '.join(valid_categories)}"
        )
    
    return cat


def validate_safety_factor_inputs(applied_stress, allowable_stress, min_safety_factor=1.0):
    if applied_stress == 0:
        raise ValidationError("Applied stress cannot be zero (division by zero)")
    
    app_stress = validate_positive(applied_stress, "Applied Stress")
    allow_stress = validate_positive(allowable_stress, "Allowable Stress")
    min_sf = validate_positive(min_safety_factor, "Minimum Safety Factor")
    
    return (app_stress, allow_stress, min_sf)


def validate_utilization_inputs(applied_load, section_capacity):
    load = validate_non_negative(applied_load, "Applied Load")
    capacity = validate_positive(section_capacity, "Section Capacity")
    
    return (load, capacity)


def validate_moment_inputs(yield_strength, plastic_modulus):
    fy = validate_positive(yield_strength, "Yield Strength")
    zpz = validate_positive(plastic_modulus, "Plastic Modulus")
    
    return (fy, zpz)


def validate_deflection_inputs(actual_deflection, span_length, limit_ratio=300):
    deflection = validate_non_negative(actual_deflection, "Actual Deflection")
    span = validate_positive(span_length, "Span Length")
    ratio = validate_positive(limit_ratio, "Deflection Limit Ratio")
    
    return (deflection, span, int(ratio))


def validate_shear_inputs(yield_strength, shear_area):
    fy = validate_positive(yield_strength, "Yield Strength")
    av = validate_positive(shear_area, "Shear Area")
    
    return (fy, av)


def validate_form_data(form_data, calculation_type):
    validated = {}
    
    if calculation_type == 'factored_load':
        validated['dead_load'] = validate_non_negative(
            form_data.get('dead_load', 0), "Dead Load"
        )
        validated['live_load'] = validate_non_negative(
            form_data.get('live_load', 0), "Live Load"
        )
        validated['wind_load'] = validate_non_negative(
            form_data.get('wind_load', 0), "Wind Load"
        )
        validated['earthquake_load'] = validate_non_negative(
            form_data.get('earthquake_load', 0), "Earthquake Load"
        )
        validated['combination_type'] = validate_combination_type(
            form_data.get('combination_type', 'normal')
        )
    
    elif calculation_type == 'safety_factor':
        validated['applied_stress'] = validate_positive(
            form_data.get('applied_stress', 0), "Applied Stress"
        )
        validated['allowable_stress'] = validate_positive(
            form_data.get('allowable_stress', 0), "Allowable Stress"
        )
        validated['min_safety_factor'] = validate_positive(
            form_data.get('min_safety_factor', 1.0), "Minimum Safety Factor"
        )
    
    elif calculation_type == 'utilization':
        validated['applied_load'] = validate_non_negative(
            form_data.get('applied_load', 0), "Applied Load"
        )
        validated['section_capacity'] = validate_positive(
            form_data.get('section_capacity', 0), "Section Capacity"
        )
    
    elif calculation_type == 'moment_capacity':
        validated['yield_strength'] = validate_positive(
            form_data.get('yield_strength', 0), "Yield Strength"
        )
        validated['plastic_modulus'] = validate_positive(
            form_data.get('plastic_modulus', 0), "Plastic Modulus"
        )
    
    elif calculation_type == 'deflection':
        validated['actual_deflection'] = validate_non_negative(
            form_data.get('actual_deflection', 0), "Actual Deflection"
        )
        validated['span_length'] = validate_positive(
            form_data.get('span_length', 0), "Span Length"
        )
        validated['deflection_limit'] = validate_positive(
            form_data.get('deflection_limit', 300), "Deflection Limit Ratio"
        )
    
    elif calculation_type == 'shear_capacity':
        validated['yield_strength'] = validate_positive(
            form_data.get('yield_strength', 0), "Yield Strength"
        )
        validated['shear_area'] = validate_positive(
            form_data.get('shear_area', 0), "Shear Area"
        )
    
    elif calculation_type == 'material_properties':
        validated['steel_grade'] = validate_steel_grade(
            form_data.get('steel_grade', '')
        )
    
    else:
        raise ValidationError(f"Unknown calculation type: '{calculation_type}'")
    
    return validated
