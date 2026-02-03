from flask import Blueprint, render_template, request, jsonify
from .calculations import (
    calculate_factored_load,
    check_safety_factor,
    calculate_section_utilization,
    calculate_moment_capacity,
    check_deflection_serviceability,
    calculate_shear_capacity,
    get_material_properties,
    perform_complete_analysis
)
from .validators import ValidationError, validate_form_data
from .config import STEEL_GRADES, LOAD_COMBINATIONS, DEFLECTION_LIMITS


# Create Blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html',
                          steel_grades=STEEL_GRADES,
                          load_combinations=LOAD_COMBINATIONS,
                          deflection_limits=DEFLECTION_LIMITS)


@main_bp.route('/calculate', methods=['POST'])
def calculate():
    try:
        calculation_type = request.form.get('calculation_type', '')
        
        if not calculation_type:
            return jsonify({
                'success': False,
                'error': 'Please select a calculation type'
            }), 400
        
        # Validate and extract form data
        form_data = request.form.to_dict()
        validated_data = validate_form_data(form_data, calculation_type)
        
        # Perform calculation based on type
        if calculation_type == 'factored_load':
            result = calculate_factored_load(
                validated_data['dead_load'],
                validated_data['live_load'],
                validated_data['wind_load'],
                validated_data['earthquake_load'],
                validated_data['combination_type']
            )
        
        elif calculation_type == 'safety_factor':
            result = check_safety_factor(
                validated_data['applied_stress'],
                validated_data['allowable_stress'],
                validated_data['min_safety_factor']
            )
        
        elif calculation_type == 'utilization':
            result = calculate_section_utilization(
                validated_data['applied_load'],
                validated_data['section_capacity']
            )
        
        elif calculation_type == 'moment_capacity':
            result = calculate_moment_capacity(
                validated_data['yield_strength'],
                validated_data['plastic_modulus']
            )
        
        elif calculation_type == 'deflection':
            result = check_deflection_serviceability(
                validated_data['actual_deflection'],
                validated_data['span_length'],
                validated_data['deflection_limit']
            )
        
        elif calculation_type == 'shear_capacity':
            result = calculate_shear_capacity(
                validated_data['yield_strength'],
                validated_data['shear_area']
            )
        
        elif calculation_type == 'material_properties':
            result = get_material_properties(
                validated_data['steel_grade']
            )
        
        else:
            return jsonify({
                'success': False,
                'error': f'Unknown calculation type: {calculation_type}'
            }), 400
        
        return jsonify({
            'success': True,
            'calculation_type': calculation_type,
            'result': result
        })
    
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Calculation error: {str(e)}'
        }), 500


@main_bp.route('/complete-analysis', methods=['POST'])
def complete_analysis():
    """
    Perform complete structural analysis with all checks.
    """
    try:
        form_data = request.form.to_dict()
        
        # Extract and convert values
        dead_load = float(form_data.get('dead_load', 0))
        live_load = float(form_data.get('live_load', 0))
        applied_stress = float(form_data.get('applied_stress', 0))
        allowable_stress = float(form_data.get('allowable_stress', 0))
        section_capacity = float(form_data.get('section_capacity', 0))
        combination_type = form_data.get('combination_type', 'normal')
        
        result = perform_complete_analysis(
            dead_load, live_load, applied_stress,
            allowable_stress, section_capacity, combination_type
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis error: {str(e)}'
        }), 500


@main_bp.route('/api/steel-grades')
def get_steel_grades():
    """API endpoint to get available steel grades."""
    return jsonify({
        'success': True,
        'steel_grades': STEEL_GRADES
    })


@main_bp.route('/api/load-combinations')
def get_load_combinations():
    """API endpoint to get available load combinations."""
    return jsonify({
        'success': True,
        'load_combinations': LOAD_COMBINATIONS
    })


# =============================================================================
# Application Entry Point
# =============================================================================

def run_app(debug=True, host='127.0.0.1', port=5000):
    from . import create_app
    app = create_app()
    app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    run_app()
