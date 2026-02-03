import pytest
import math
from app.calculations import (
    calculate_factored_load,
    check_safety_factor,
    calculate_section_utilization,
    calculate_moment_capacity,
    check_deflection_serviceability,
    calculate_shear_capacity,
    get_material_properties,
    perform_complete_analysis
)
from app.validators import ValidationError
from app.config import GAMMA_DL, GAMMA_LL, GAMMA_M0


# =============================================================================
# Test Class: Factored Load Calculations
# =============================================================================

class TestFactoredLoadCalculations:
    """Tests for calculate_factored_load function."""
    
    def test_normal_combination_basic(self):
        """Test normal load combination with typical values."""
        result = calculate_factored_load(100, 50)
        # 1.5*100 + 1.5*50 = 150 + 75 = 225
        assert result['factored_load'] == 225.0
        assert result['combination_type'] == 'normal'
    
    def test_normal_combination_zero_live_load(self):
        """Test normal combination with zero live load."""
        result = calculate_factored_load(100, 0)
        # 1.5*100 + 1.5*0 = 150
        assert result['factored_load'] == 150.0
    
    def test_wind_combination(self):
        """Test wind load combination."""
        result = calculate_factored_load(100, 50, wind_load=30, combination_type='wind')
        # 1.2*(100 + 50 + 30) = 1.2*180 = 216
        assert result['factored_load'] == 216.0
        assert result['combination_type'] == 'wind'
    
    def test_seismic_combination(self):
        """Test seismic load combination."""
        result = calculate_factored_load(100, 50, earthquake_load=40, combination_type='seismic')
        # 1.2*(100 + 50 + 40) = 1.2*190 = 228
        assert result['factored_load'] == 228.0
        assert result['combination_type'] == 'seismic'
    
    def test_all_zero_loads(self):
        """Test with all zero loads."""
        result = calculate_factored_load(0, 0)
        assert result['factored_load'] == 0.0
    
    def test_result_contains_unit(self):
        """Test that result includes unit information."""
        result = calculate_factored_load(100, 50)
        assert 'unit' in result
        assert result['unit'] == 'kN'
    
    def test_result_contains_components(self):
        """Test that result includes component breakdown."""
        result = calculate_factored_load(100, 50)
        assert 'components' in result
        assert 'factored_dead_load' in result['components']
        assert 'factored_live_load' in result['components']
    
    def test_invalid_combination_type_raises_error(self):
        """Test that invalid combination type raises ValidationError."""
        with pytest.raises(ValidationError):
            calculate_factored_load(100, 50, combination_type='invalid')
    
    def test_negative_dead_load_raises_error(self):
        """Test that negative dead load raises ValidationError."""
        with pytest.raises(ValidationError):
            calculate_factored_load(-100, 50)
    
    def test_negative_live_load_raises_error(self):
        """Test that negative live load raises ValidationError."""
        with pytest.raises(ValidationError):
            calculate_factored_load(100, -50)


# =============================================================================
# Test Class: Safety Factor Calculations
# =============================================================================

class TestSafetyFactorCalculations:
    """Tests for check_safety_factor function."""
    
    def test_safe_design_basic(self):
        """Test basic safe design with adequate safety factor."""
        result = check_safety_factor(100, 165)
        assert result['safety_factor'] == 1.65
        assert result['is_safe'] is True
        assert result['status'] == 'SAFE'
    
    def test_unsafe_design(self):
        """Test unsafe design where safety factor is insufficient."""
        result = check_safety_factor(200, 150, min_safety_factor=1.0)
        # 150/200 = 0.75 < 1.0
        assert result['safety_factor'] == 0.75
        assert result['is_safe'] is False
        assert result['status'] == 'UNSAFE'
    
    def test_safety_factor_exactly_minimum(self):
        """Test when safety factor exactly equals minimum."""
        result = check_safety_factor(100, 100, min_safety_factor=1.0)
        assert result['safety_factor'] == 1.0
        assert result['is_safe'] is True
    
    def test_custom_minimum_safety_factor(self):
        """Test with custom minimum safety factor."""
        result = check_safety_factor(100, 150, min_safety_factor=1.5)
        # 150/100 = 1.5 = 1.5 (exactly at limit)
        assert result['is_safe'] is True
    
    def test_margin_calculation_positive(self):
        """Test positive margin calculation."""
        result = check_safety_factor(100, 150, min_safety_factor=1.0)
        # margin = ((1.5 - 1.0) / 1.0) * 100 = 50%
        assert result['margin'] == 50.0
    
    def test_margin_calculation_negative(self):
        """Test negative margin calculation for unsafe design."""
        result = check_safety_factor(200, 100, min_safety_factor=1.0)
        # margin = ((0.5 - 1.0) / 1.0) * 100 = -50%
        assert result['margin'] == -50.0
    
    def test_zero_applied_stress_raises_error(self):
        """Test that zero applied stress raises error."""
        with pytest.raises(ValidationError):
            check_safety_factor(0, 165)
    
    def test_negative_allowable_stress_raises_error(self):
        """Test that negative allowable stress raises error."""
        with pytest.raises(ValidationError):
            check_safety_factor(100, -165)


# =============================================================================
# Test Class: Section Utilization Calculations
# =============================================================================

class TestSectionUtilizationCalculations:
    """Tests for calculate_section_utilization function."""
    
    def test_adequate_section_basic(self):
        """Test adequate section with typical utilization."""
        result = calculate_section_utilization(75, 100)
        assert result['utilization_ratio'] == 0.75
        assert result['is_adequate'] is True
    
    def test_overstressed_section(self):
        """Test overstressed section."""
        result = calculate_section_utilization(120, 100)
        assert result['utilization_ratio'] == 1.2
        assert result['is_adequate'] is False
        assert result['status'] == 'OVERSTRESSED'
    
    def test_full_utilization(self):
        """Test section at full capacity."""
        result = calculate_section_utilization(100, 100)
        assert result['utilization_ratio'] == 1.0
        assert result['is_adequate'] is True
        assert result['status'] == 'ADEQUATE'
    
    def test_under_utilized_section(self):
        """Test under-utilized section."""
        result = calculate_section_utilization(50, 100)
        assert result['utilization_ratio'] == 0.5
        assert result['status'] == 'UNDER-UTILIZED'
    
    def test_reserve_capacity_calculation(self):
        """Test reserve capacity calculation."""
        result = calculate_section_utilization(75, 100)
        assert result['reserve_capacity'] == 25.0
    
    def test_utilization_percent(self):
        """Test utilization percentage calculation."""
        result = calculate_section_utilization(80, 100)
        assert result['utilization_percent'] == 80.0
    
    def test_zero_load_allowed(self):
        """Test that zero load is allowed."""
        result = calculate_section_utilization(0, 100)
        assert result['utilization_ratio'] == 0.0
        assert result['is_adequate'] is True
    
    def test_zero_capacity_raises_error(self):
        """Test that zero capacity raises error."""
        with pytest.raises(ValidationError):
            calculate_section_utilization(75, 0)


# =============================================================================
# Test Class: Moment Capacity Calculations
# =============================================================================

class TestMomentCapacityCalculations:
    """Tests for calculate_moment_capacity function."""
    
    def test_basic_moment_capacity(self):
        """Test basic moment capacity calculation."""
        result = calculate_moment_capacity(250, 500000)
        # (250 * 500000) / (1.10 * 1e6) = 113.636...
        assert result['moment_capacity_knm'] == 113.64
    
    def test_moment_capacity_high_strength_steel(self):
        """Test moment capacity with high strength steel."""
        result = calculate_moment_capacity(350, 500000)
        # (350 * 500000) / (1.10 * 1e6) = 159.09
        assert result['moment_capacity_knm'] == 159.09
    
    def test_moment_capacity_large_section(self):
        """Test moment capacity with large plastic modulus."""
        result = calculate_moment_capacity(250, 1000000)
        # (250 * 1000000) / (1.10 * 1e6) = 227.27
        assert result['moment_capacity_knm'] == 227.27
    
    def test_result_contains_gamma_m0(self):
        """Test that result includes gamma_m0 value."""
        result = calculate_moment_capacity(250, 500000)
        assert result['gamma_m0'] == GAMMA_M0
    
    def test_zero_yield_strength_raises_error(self):
        """Test that zero yield strength raises error."""
        with pytest.raises(ValidationError):
            calculate_moment_capacity(0, 500000)
    
    def test_negative_plastic_modulus_raises_error(self):
        """Test that negative plastic modulus raises error."""
        with pytest.raises(ValidationError):
            calculate_moment_capacity(250, -500000)


# =============================================================================
# Test Class: Deflection Serviceability Calculations
# =============================================================================

class TestDeflectionServiceabilityCalculations:
    """Tests for check_deflection_serviceability function."""
    
    def test_serviceable_deflection(self):
        """Test serviceable deflection within limits."""
        result = check_deflection_serviceability(15, 6000, 300)
        # Allowable = 6000/300 = 20mm, Actual = 15mm
        assert result['is_serviceable'] is True
        assert result['allowable_deflection'] == 20.0
    
    def test_exceeds_deflection_limit(self):
        """Test deflection exceeding limits."""
        result = check_deflection_serviceability(25, 6000, 300)
        # Allowable = 20mm, Actual = 25mm
        assert result['is_serviceable'] is False
        assert result['status'] == 'EXCEEDS LIMITS'
    
    def test_well_within_limits(self):
        """Test deflection well within limits."""
        result = check_deflection_serviceability(10, 6000, 300)
        # Utilization = 10/20 = 0.5 (50%)
        assert result['status'] == 'WELL WITHIN LIMITS'
    
    def test_industrial_deflection_limit(self):
        """Test with industrial deflection limit (L/240)."""
        result = check_deflection_serviceability(20, 6000, 240)
        # Allowable = 6000/240 = 25mm
        assert result['allowable_deflection'] == 25.0
    
    def test_sensitive_deflection_limit(self):
        """Test with sensitive finishes limit (L/360)."""
        result = check_deflection_serviceability(15, 6000, 360)
        # Allowable = 6000/360 = 16.67mm
        assert result['allowable_deflection'] == 16.67
    
    def test_utilization_calculation(self):
        """Test deflection utilization calculation."""
        result = check_deflection_serviceability(15, 6000, 300)
        # Utilization = 15/20 = 0.75
        assert result['utilization'] == 0.75
    
    def test_zero_deflection_allowed(self):
        """Test that zero deflection is allowed."""
        result = check_deflection_serviceability(0, 6000, 300)
        assert result['is_serviceable'] is True
    
    def test_zero_span_raises_error(self):
        """Test that zero span length raises error."""
        with pytest.raises(ValidationError):
            check_deflection_serviceability(15, 0, 300)


# =============================================================================
# Test Class: Shear Capacity Calculations
# =============================================================================

class TestShearCapacityCalculations:
    """Tests for calculate_shear_capacity function."""
    
    def test_basic_shear_capacity(self):
        """Test basic shear capacity calculation."""
        result = calculate_shear_capacity(250, 2000)
        # (250 * 2000) / (sqrt(3) * 1.10 * 1000) = 262.43
        expected = (250 * 2000) / (math.sqrt(3) * 1.10 * 1000)
        assert result['shear_capacity_kn'] == round(expected, 2)
    
    def test_shear_capacity_high_strength(self):
        """Test shear capacity with high strength steel."""
        result = calculate_shear_capacity(350, 2000)
        expected = (350 * 2000) / (math.sqrt(3) * 1.10 * 1000)
        assert result['shear_capacity_kn'] == round(expected, 2)
    
    def test_shear_capacity_large_area(self):
        """Test shear capacity with large shear area."""
        result = calculate_shear_capacity(250, 5000)
        expected = (250 * 5000) / (math.sqrt(3) * 1.10 * 1000)
        assert result['shear_capacity_kn'] == round(expected, 2)
    
    def test_result_unit(self):
        """Test that result includes correct unit."""
        result = calculate_shear_capacity(250, 2000)
        assert result['unit'] == 'kN'
    
    def test_zero_yield_strength_raises_error(self):
        """Test that zero yield strength raises error."""
        with pytest.raises(ValidationError):
            calculate_shear_capacity(0, 2000)
    
    def test_zero_shear_area_raises_error(self):
        """Test that zero shear area raises error."""
        with pytest.raises(ValidationError):
            calculate_shear_capacity(250, 0)


# =============================================================================
# Test Class: Material Properties
# =============================================================================

class TestMaterialProperties:
    """Tests for get_material_properties function."""
    
    def test_e250_properties(self):
        """Test E250 steel grade properties."""
        result = get_material_properties('E250')
        assert result['yield_strength'] == 250
        assert result['ultimate_strength'] == 410
        assert result['elongation'] == 23
    
    def test_e350_properties(self):
        """Test E350 steel grade properties."""
        result = get_material_properties('E350')
        assert result['yield_strength'] == 350
        assert result['ultimate_strength'] == 490
    
    def test_case_insensitive_grade(self):
        """Test that steel grade lookup is case insensitive."""
        result = get_material_properties('e250')
        assert result['yield_strength'] == 250
    
    def test_grade_with_whitespace(self):
        """Test that whitespace in grade is handled."""
        result = get_material_properties('  E250  ')
        assert result['yield_strength'] == 250
    
    def test_elastic_modulus_included(self):
        """Test that elastic modulus is included in result."""
        result = get_material_properties('E250')
        assert result['elastic_modulus'] == 200000
    
    def test_legacy_fe410_grade(self):
        """Test legacy Fe410 grade."""
        result = get_material_properties('Fe410')
        assert result['yield_strength'] == 250
    
    def test_invalid_grade_raises_error(self):
        """Test that invalid grade raises ValidationError."""
        with pytest.raises(ValidationError):
            get_material_properties('INVALID')


# =============================================================================
# Test Class: Complete Analysis
# =============================================================================

class TestCompleteAnalysis:
    """Tests for perform_complete_analysis function."""
    
    def test_acceptable_design(self):
        """Test analysis with acceptable design."""
        result = perform_complete_analysis(
            dead_load=100,
            live_load=50,
            applied_stress=100,
            allowable_stress=165,
            section_capacity=300
        )
        assert result['is_acceptable'] is True
        assert result['overall_status'] == 'ACCEPTABLE'
    
    def test_unacceptable_design_unsafe_safety(self):
        """Test analysis with unsafe safety factor."""
        result = perform_complete_analysis(
            dead_load=100,
            live_load=50,
            applied_stress=200,
            allowable_stress=150,
            section_capacity=300
        )
        assert result['is_acceptable'] is False
        assert result['overall_status'] == 'REVIEW REQUIRED'
    
    def test_result_contains_all_analyses(self):
        """Test that result contains all three analyses."""
        result = perform_complete_analysis(
            dead_load=100,
            live_load=50,
            applied_stress=100,
            allowable_stress=165,
            section_capacity=300
        )
        assert 'factored_load_analysis' in result
        assert 'safety_factor_analysis' in result
        assert 'utilization_analysis' in result


# =============================================================================
# Test Class: Edge Cases and Boundary Conditions
# =============================================================================

class TestEdgeCasesAndBoundary:
    """Tests for edge cases and boundary conditions."""
    
    def test_very_small_load_values(self):
        """Test with very small load values."""
        result = calculate_factored_load(0.001, 0.001)
        assert result['factored_load'] == 0.0  # Rounded to 2 decimal places
    
    def test_very_large_load_values(self):
        """Test with very large load values."""
        result = calculate_factored_load(1000000, 500000)
        # 1.5*1000000 + 1.5*500000 = 2,250,000
        assert result['factored_load'] == 2250000.0
    
    def test_floating_point_precision(self):
        """Test floating point precision handling."""
        result = calculate_section_utilization(1, 3)
        # 1/3 = 0.3333...
        assert result['utilization_ratio'] == 0.3333
    
    def test_marginally_overstressed(self):
        """Test marginally overstressed section status."""
        result = calculate_section_utilization(105, 100)
        assert result['status'] == 'MARGINALLY OVERSTRESSED'
    
    def test_deflection_at_exact_limit(self):
        """Test deflection exactly at allowable limit."""
        result = check_deflection_serviceability(20, 6000, 300)
        # Allowable = 20mm, Actual = 20mm
        assert result['is_serviceable'] is True
        assert result['utilization'] == 1.0
