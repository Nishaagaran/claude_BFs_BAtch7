import pytest
from read_patients import categorize_patient_health


class TestCategorizePatientHealth:
    """Test suite for categorize_patient_health function"""

    # Healthy category tests
    def test_healthy_all_normal_metrics(self):
        """Test patient with all normal metrics"""
        result = categorize_patient_health(bmi=22.5, blood_pressure="118/76", glucose_level=95)
        assert result == "Healthy"

    def test_healthy_normal_bmi_low_bp_low_glucose(self):
        """Test patient with normal BMI, low BP, and low glucose"""
        result = categorize_patient_health(bmi=23.0, blood_pressure="110/70", glucose_level=88)
        assert result == "Healthy"

    def test_healthy_borderline_normal_bmi(self):
        """Test patient with BMI just below overweight threshold"""
        result = categorize_patient_health(bmi=24.9, blood_pressure="120/75", glucose_level=99)
        assert result == "Healthy"

    def test_healthy_borderline_normal_bp(self):
        """Test patient with BP just below elevated threshold"""
        result = categorize_patient_health(bmi=23.5, blood_pressure="129/79", glucose_level=95)
        assert result == "Healthy"

    def test_healthy_borderline_normal_glucose(self):
        """Test patient with glucose just below prediabetic threshold"""
        result = categorize_patient_health(bmi=24.0, blood_pressure="120/75", glucose_level=99)
        assert result == "Healthy"

    # AtRisk category tests
    def test_atrisk_overweight_bmi(self):
        """Test patient with overweight BMI (25-29.9)"""
        result = categorize_patient_health(bmi=26.5, blood_pressure="118/76", glucose_level=95)
        assert result == "AtRisk"

    def test_atrisk_elevated_blood_pressure_systolic(self):
        """Test patient with elevated systolic BP"""
        result = categorize_patient_health(bmi=23.0, blood_pressure="135/78", glucose_level=92)
        assert result == "AtRisk"

    def test_atrisk_elevated_blood_pressure_diastolic(self):
        """Test patient with elevated diastolic BP"""
        result = categorize_patient_health(bmi=23.0, blood_pressure="125/82", glucose_level=92)
        assert result == "AtRisk"

    def test_atrisk_prediabetic_glucose(self):
        """Test patient with prediabetic glucose level (100-125)"""
        result = categorize_patient_health(bmi=23.0, blood_pressure="120/75", glucose_level=110)
        assert result == "AtRisk"

    def test_atrisk_multiple_elevated_metrics(self):
        """Test patient with multiple slightly elevated metrics"""
        result = categorize_patient_health(bmi=26.0, blood_pressure="135/82", glucose_level=108)
        assert result == "AtRisk"

    def test_atrisk_bmi_lower_bound(self):
        """Test patient at lower boundary of overweight (25.0)"""
        result = categorize_patient_health(bmi=25.0, blood_pressure="120/75", glucose_level=95)
        assert result == "AtRisk"

    def test_atrisk_glucose_lower_bound(self):
        """Test patient at lower boundary of prediabetic (100)"""
        result = categorize_patient_health(bmi=23.0, blood_pressure="120/75", glucose_level=100)
        assert result == "AtRisk"

    # Critical category tests
    def test_critical_obese_bmi(self):
        """Test patient with obese BMI (≥30)"""
        result = categorize_patient_health(bmi=31.0, blood_pressure="125/80", glucose_level=95)
        assert result == "Critical"

    def test_critical_high_blood_pressure_systolic(self):
        """Test patient with hypertension stage 2 systolic BP (≥180)"""
        result = categorize_patient_health(bmi=23.0, blood_pressure="185/90", glucose_level=95)
        assert result == "Critical"

    def test_critical_high_blood_pressure_diastolic(self):
        """Test patient with hypertension stage 2 diastolic BP (≥120)"""
        result = categorize_patient_health(bmi=23.0, blood_pressure="140/125", glucose_level=95)
        assert result == "Critical"

    def test_critical_diabetic_glucose(self):
        """Test patient with diabetic glucose level (≥126)"""
        result = categorize_patient_health(bmi=23.0, blood_pressure="120/75", glucose_level=140)
        assert result == "Critical"

    def test_critical_bmi_at_threshold(self):
        """Test patient with BMI exactly at obesity threshold (30.0)"""
        result = categorize_patient_health(bmi=30.0, blood_pressure="120/75", glucose_level=95)
        assert result == "Critical"

    def test_critical_glucose_at_threshold(self):
        """Test patient with glucose exactly at diabetic threshold (126)"""
        result = categorize_patient_health(bmi=23.0, blood_pressure="120/75", glucose_level=126)
        assert result == "Critical"

    def test_critical_bp_systolic_at_threshold(self):
        """Test patient with systolic BP exactly at threshold (180)"""
        result = categorize_patient_health(bmi=23.0, blood_pressure="180/90", glucose_level=95)
        assert result == "Critical"

    def test_critical_bp_diastolic_at_threshold(self):
        """Test patient with diastolic BP exactly at threshold (120)"""
        result = categorize_patient_health(bmi=23.0, blood_pressure="140/120", glucose_level=95)
        assert result == "Critical"

    def test_critical_all_metrics_dangerous(self):
        """Test patient with all critical metrics"""
        result = categorize_patient_health(bmi=32.5, blood_pressure="160/100", glucose_level=170)
        assert result == "Critical"

    def test_critical_multiple_critical_metrics(self):
        """Test patient with multiple critical metrics"""
        result = categorize_patient_health(bmi=31.5, blood_pressure="155/95", glucose_level=145)
        assert result == "Critical"

    # Edge case tests
    def test_very_low_bmi(self):
        """Test patient with very low BMI (underweight)"""
        result = categorize_patient_health(bmi=18.5, blood_pressure="110/70", glucose_level=85)
        assert result == "Healthy"

    def test_very_high_bmi(self):
        """Test patient with very high BMI"""
        result = categorize_patient_health(bmi=40.0, blood_pressure="130/85", glucose_level=100)
        assert result == "Critical"

    def test_very_high_glucose(self):
        """Test patient with very high glucose level"""
        result = categorize_patient_health(bmi=25.0, blood_pressure="120/75", glucose_level=250)
        assert result == "Critical"

    def test_very_high_blood_pressure(self):
        """Test patient with very high blood pressure (hypertensive crisis)"""
        result = categorize_patient_health(bmi=24.0, blood_pressure="200/130", glucose_level=95)
        assert result == "Critical"

    def test_borderline_atrisk_to_critical_bmi(self):
        """Test transition from AtRisk to Critical on BMI"""
        atrisk = categorize_patient_health(bmi=29.9, blood_pressure="120/75", glucose_level=95)
        critical = categorize_patient_health(bmi=30.0, blood_pressure="120/75", glucose_level=95)
        assert atrisk == "AtRisk"
        assert critical == "Critical"

    def test_borderline_healthy_to_atrisk_glucose(self):
        """Test transition from Healthy to AtRisk on glucose"""
        healthy = categorize_patient_health(bmi=23.0, blood_pressure="120/75", glucose_level=99)
        atrisk = categorize_patient_health(bmi=23.0, blood_pressure="120/75", glucose_level=100)
        assert healthy == "Healthy"
        assert atrisk == "AtRisk"

    # Real-world scenarios from sample data
    def test_sample_patient_john_smith(self):
        """Test categorization for John Smith from sample data"""
        result = categorize_patient_health(bmi=26.5, blood_pressure="130/85", glucose_level=105)
        assert result == "AtRisk"

    def test_sample_patient_sarah_johnson(self):
        """Test categorization for Sarah Johnson from sample data"""
        result = categorize_patient_health(bmi=23.2, blood_pressure="118/76", glucose_level=92)
        assert result == "Healthy"

    def test_sample_patient_michael_brown(self):
        """Test categorization for Michael Brown from sample data"""
        result = categorize_patient_health(bmi=29.8, blood_pressure="145/92", glucose_level=148)
        assert result == "Critical"

    def test_sample_patient_robert_wilson(self):
        """Test categorization for Robert Wilson from sample data"""
        result = categorize_patient_health(bmi=31.5, blood_pressure="155/98", glucose_level=165)
        assert result == "Critical"

    def test_sample_patient_jessica_martinez(self):
        """Test categorization for Jessica Martinez from sample data"""
        result = categorize_patient_health(bmi=22.7, blood_pressure="115/74", glucose_level=88)
        assert result == "Healthy"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
