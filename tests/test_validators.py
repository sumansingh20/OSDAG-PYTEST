import pytest
from app.validators import (
    ValidationError,
    validate_numeric,
    validate_positive,
    validate_non_negative,
    validate_load_inputs,
    validate_combination_type,
    validate_steel_grade,
    validate_deflection_category,
    validate_safety_factor_inputs,
    validate_utilization_inputs,
    validate_moment_inputs,
    validate_deflection_inputs,
    validate_shear_inputs,
    validate_form_data
)


# =============================================================================
# Test Class: Basic Numeric Validation
# =============================================================================

class TestValidateNumeric:
    """Tests for validate_numeric function."""
    
    def test_valid_integer(self):
        """Test validation of valid integer."""
        result = validate_numeric(100, "Test Value", allow_zero=False)
        assert result == 100.0
    
    def test_valid_float(self):
        """Test validation of valid float."""
        result = validate_numeric(100.5, "Test Value", allow_zero=False)
        assert result == 100.5
    
    def test_string_numeric_conversion(self):
        """Test conversion of numeric string."""
        result = validate_numeric("100", "Test Value", allow_zero=False)
        assert result == 100.0
    
    def test_invalid_string_raises_error(self):
        """Test that non-numeric string raises error."""
        with pytest.raises(ValidationError) as excinfo:
            validate_numeric("abc", "Test Value")
        assert "must be a numeric value" in str(excinfo.value)
    
    def test_none_raises_error(self):
        """Test that None raises error."""
        with pytest.raises(ValidationError):
            validate_numeric(None, "Test Value")
    
    def test_zero_not_allowed_by_default(self):
        """Test that zero raises error when not allowed."""
        with pytest.raises(ValidationError) as excinfo:
            validate_numeric(0, "Test Value", allow_zero=False)
        assert "cannot be zero" in str(excinfo.value)
    
    def test_zero_allowed_when_specified(self):
        """Test that zero is allowed when specified."""
        result = validate_numeric(0, "Test Value", allow_zero=True)
        assert result == 0.0
    
    def test_negative_not_allowed_by_default(self):
        """Test that negative raises error when not allowed."""
        with pytest.raises(ValidationError) as excinfo:
            validate_numeric(-10, "Test Value", allow_negative=False)
        assert "cannot be negative" in str(excinfo.value)
    
    def test_negative_allowed_when_specified(self):
        """Test that negative is allowed when specified."""
        result = validate_numeric(-10, "Test Value", allow_negative=True, allow_zero=True)
        assert result == -10.0


# =============================================================================
# Test Class: Positive and Non-Negative Validation
# =============================================================================

class TestPositiveNonNegativeValidation:
    """Tests for validate_positive and validate_non_negative functions."""
    
    def test_validate_positive_with_positive(self):
        """Test validate_positive with positive value."""
        result = validate_positive(100, "Test")
        assert result == 100.0
    
    def test_validate_positive_with_zero_raises_error(self):
        """Test validate_positive with zero raises error."""
        with pytest.raises(ValidationError):
            validate_positive(0, "Test")
    
    def test_validate_positive_with_negative_raises_error(self):
        """Test validate_positive with negative raises error."""
        with pytest.raises(ValidationError):
            validate_positive(-10, "Test")
    
    def test_validate_non_negative_with_positive(self):
        """Test validate_non_negative with positive value."""
        result = validate_non_negative(100, "Test")
        assert result == 100.0
    
    def test_validate_non_negative_with_zero(self):
        """Test validate_non_negative with zero."""
        result = validate_non_negative(0, "Test")
        assert result == 0.0
    
    def test_validate_non_negative_with_negative_raises_error(self):
        """Test validate_non_negative with negative raises error."""
        with pytest.raises(ValidationError):
            validate_non_negative(-10, "Test")


# =============================================================================
# Test Class: Load Input Validation
# =============================================================================

class TestLoadInputValidation:
    """Tests for validate_load_inputs function."""
    
    def test_valid_loads(self):
        """Test validation of valid load inputs."""
        result = validate_load_inputs(100, 50, 30, 20)
        assert result == (100.0, 50.0, 30.0, 20.0)
    
    def test_zero_loads_allowed(self):
        """Test that zero loads are allowed."""
        result = validate_load_inputs(0, 0, 0, 0)
        assert result == (0.0, 0.0, 0.0, 0.0)
    
    def test_negative_dead_load_raises_error(self):
        """Test that negative dead load raises error."""
        with pytest.raises(ValidationError) as excinfo:
            validate_load_inputs(-100, 50)
        assert "Dead Load" in str(excinfo.value)
    
    def test_negative_live_load_raises_error(self):
        """Test that negative live load raises error."""
        with pytest.raises(ValidationError) as excinfo:
            validate_load_inputs(100, -50)
        assert "Live Load" in str(excinfo.value)


# =============================================================================
# Test Class: Combination Type Validation
# =============================================================================

class TestCombinationTypeValidation:
    """Tests for validate_combination_type function."""
    
    def test_valid_normal_type(self):
        """Test validation of 'normal' combination type."""
        result = validate_combination_type('normal')
        assert result == 'normal'
    
    def test_valid_wind_type(self):
        """Test validation of 'wind' combination type."""
        result = validate_combination_type('wind')
        assert result == 'wind'
    
    def test_valid_seismic_type(self):
        """Test validation of 'seismic' combination type."""
        result = validate_combination_type('seismic')
        assert result == 'seismic'
    
    def test_case_insensitive(self):
        """Test that combination type is case insensitive."""
        result = validate_combination_type('NORMAL')
        assert result == 'normal'
    
    def test_whitespace_handling(self):
        """Test that whitespace is handled."""
        result = validate_combination_type('  normal  ')
        assert result == 'normal'
    
    def test_invalid_type_raises_error(self):
        """Test that invalid type raises error."""
        with pytest.raises(ValidationError) as excinfo:
            validate_combination_type('invalid')
        assert "Invalid combination type" in str(excinfo.value)
    
    def test_non_string_raises_error(self):
        """Test that non-string raises error."""
        with pytest.raises(ValidationError):
            validate_combination_type(123)


# =============================================================================
# Test Class: Steel Grade Validation
# =============================================================================

class TestSteelGradeValidation:
    """Tests for validate_steel_grade function."""
    
    def test_valid_e250_grade(self):
        """Test validation of E250 grade."""
        result = validate_steel_grade('E250')
        assert result == 'E250'
    
    def test_valid_e350_grade(self):
        """Test validation of E350 grade."""
        result = validate_steel_grade('E350')
        assert result == 'E350'
    
    def test_case_insensitive(self):
        """Test that steel grade is case insensitive."""
        result = validate_steel_grade('e250')
        assert result == 'E250'
    
    def test_legacy_fe410_grade(self):
        """Test validation of legacy Fe410 grade."""
        result = validate_steel_grade('Fe410')
        assert result == 'FE410'
    
    def test_invalid_grade_raises_error(self):
        """Test that invalid grade raises error."""
        with pytest.raises(ValidationError) as excinfo:
            validate_steel_grade('INVALID')
        assert "Unknown steel grade" in str(excinfo.value)
    
    def test_non_string_raises_error(self):
        """Test that non-string raises error."""
        with pytest.raises(ValidationError):
            validate_steel_grade(250)


# =============================================================================
# Test Class: Deflection Category Validation
# =============================================================================

class TestDeflectionCategoryValidation:
    """Tests for validate_deflection_category function."""
    
    def test_valid_industrial_category(self):
        """Test validation of 'industrial' category."""
        result = validate_deflection_category('industrial')
        assert result == 'industrial'
    
    def test_valid_normal_category(self):
        """Test validation of 'normal' category."""
        result = validate_deflection_category('normal')
        assert result == 'normal'
    
    def test_valid_sensitive_category(self):
        """Test validation of 'sensitive' category."""
        result = validate_deflection_category('sensitive')
        assert result == 'sensitive'
    
    def test_case_insensitive(self):
        """Test that category is case insensitive."""
        result = validate_deflection_category('NORMAL')
        assert result == 'normal'
    
    def test_invalid_category_raises_error(self):
        """Test that invalid category raises error."""
        with pytest.raises(ValidationError):
            validate_deflection_category('invalid')


# =============================================================================
# Test Class: Safety Factor Input Validation
# =============================================================================

class TestSafetyFactorInputValidation:
    """Tests for validate_safety_factor_inputs function."""
    
    def test_valid_inputs(self):
        """Test validation of valid safety factor inputs."""
        result = validate_safety_factor_inputs(100, 165, 1.0)
        assert result == (100.0, 165.0, 1.0)
    
    def test_zero_applied_stress_raises_error(self):
        """Test that zero applied stress raises error."""
        with pytest.raises(ValidationError) as excinfo:
            validate_safety_factor_inputs(0, 165, 1.0)
        assert "cannot be zero" in str(excinfo.value)
    
    def test_negative_allowable_stress_raises_error(self):
        """Test that negative allowable stress raises error."""
        with pytest.raises(ValidationError):
            validate_safety_factor_inputs(100, -165, 1.0)


# =============================================================================
# Test Class: Form Data Validation
# =============================================================================

class TestFormDataValidation:
    """Tests for validate_form_data function."""
    
    def test_factored_load_form_data(self):
        """Test validation of factored load form data."""
        form_data = {
            'dead_load': '100',
            'live_load': '50',
            'wind_load': '0',
            'earthquake_load': '0',
            'combination_type': 'normal'
        }
        result = validate_form_data(form_data, 'factored_load')
        assert result['dead_load'] == 100.0
        assert result['combination_type'] == 'normal'
    
    def test_safety_factor_form_data(self):
        """Test validation of safety factor form data."""
        form_data = {
            'applied_stress': '100',
            'allowable_stress': '165',
            'min_safety_factor': '1.0'
        }
        result = validate_form_data(form_data, 'safety_factor')
        assert result['applied_stress'] == 100.0
        assert result['min_safety_factor'] == 1.0
    
    def test_material_properties_form_data(self):
        """Test validation of material properties form data."""
        form_data = {
            'steel_grade': 'E250'
        }
        result = validate_form_data(form_data, 'material_properties')
        assert result['steel_grade'] == 'E250'
    
    def test_unknown_calculation_type_raises_error(self):
        """Test that unknown calculation type raises error."""
        with pytest.raises(ValidationError) as excinfo:
            validate_form_data({}, 'unknown_type')
        assert "Unknown calculation type" in str(excinfo.value)


# =============================================================================
# Test Class: Integration Tests for Validators
# =============================================================================

class TestValidatorIntegration:
    """Integration tests for validation functions."""
    
    def test_complete_load_validation_workflow(self):
        """Test complete workflow for load input validation."""
        # Step 1: Validate individual loads
        dl = validate_non_negative(100, "Dead Load")
        ll = validate_non_negative(50, "Live Load")
        
        # Step 2: Validate combination type
        combo = validate_combination_type("normal")
        
        # Step 3: Verify all values
        assert dl == 100.0
        assert ll == 50.0
        assert combo == "normal"
    
    def test_error_messages_are_descriptive(self):
        """Test that error messages contain useful information."""
        with pytest.raises(ValidationError) as excinfo:
            validate_positive(-10, "Applied Stress")
        
        error_message = str(excinfo.value)
        assert "Applied Stress" in error_message
        assert "negative" in error_message
    
    def test_validation_chain_fails_fast(self):
        """Test that validation chain fails on first error."""
        with pytest.raises(ValidationError):
            validate_load_inputs(-100, 50)  # Should fail on dead load
