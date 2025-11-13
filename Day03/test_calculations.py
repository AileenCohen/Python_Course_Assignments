import pandas as pd
import numpy as np
from Basic_code_Assignment2 import calculate_pool_concentrations_from_qubit_data

# Define common constants for the tests
POOL_DICT = {'A': 5.0, 'B': 30.0, 'C': 100.0}
PLACES = 6 # Tolerance for floating point comparisons

def create_mock_dataframe(samples, concentrations):
    """Helper to create a mock input DataFrame."""
    return pd.DataFrame({
        "Sample Name": samples,
        "Original Sample Conc.": concentrations
    })

def test_basic_pooling():
    """Test samples that require the calculation to choose the next highest pool target."""
    
    input_samples = ["S1_low", "S2_mid", "S3_high"]
    input_concentrations = [1.0, 15.0, 50.0]
    
    # Expected results: 5.0/1.0=5.0, 30.0/15.0=2.0, 100.0/50.0=2.0
    expected_results = [5.0, 2.0, 2.0]

    df = create_mock_dataframe(input_samples, input_concentrations)
    result_df = calculate_pool_concentrations_from_qubit_data(df, POOL_DICT)
    
    assert len(result_df) == len(input_samples)

    for i, expected in enumerate(expected_results):
        actual = result_df.iloc[i]["Amount_to_Take"]
        sample_name = input_samples[i]
        sample_conc = input_concentrations[i]
        
        failure_msg = (
            f"Test Failed for Sample: {sample_name} (Input Conc: {sample_conc}). "
            f"Expected Amount_to_Take: {expected}, but got: {actual}. "
            f"Rule Check: Should have used pool target {expected * sample_conc}."
        )
        
        # Use simple assert and round() for precision comparison
        assert round(actual, PLACES) == round(expected, PLACES), failure_msg


def test_high_concentration_edge_case():
    """Test sample concentration greater than the highest pool target (should use max pool)."""
    
    input_sample = "S_TooHigh"
    input_conc = 200.0
    max_pool = 100.0
    
    df = create_mock_dataframe(samples=[input_sample], concentrations=[input_conc])
    # Expected: max pool / conc -> 100.0 / 200.0 = 0.5
    expected = max_pool / input_conc
    
    result_df = calculate_pool_concentrations_from_qubit_data(df, POOL_DICT)
    actual = result_df.iloc[0]["Amount_to_Take"]
    
    failure_msg = (
        f"Test Failed for Sample: {input_sample} (Conc: {input_conc}). "
        f"Expected Amount_to_Take (Max Pool/{input_conc}): {expected}, but got: {actual}. "
        f"Rule Check: Must use the largest pool ({max_pool}) when concentration exceeds it."
    )
    
    assert round(actual, PLACES) == round(expected, PLACES), failure_msg


def test_concentration_equal_to_pool_value():
    """Test samples where concentration is exactly equal to a pool target (should go to the *next* pool due to the '<' operator)."""
    
    input_samples = ["SEqual5", "SEqual30"]
    input_concentrations = [5.0, 30.0]
    
    # Expected results:
    # 5.0 is NOT < 5.0, so it uses 30.0 -> 30.0 / 5.0 = 6.0
    # 30.0 is NOT < 30.0, so it uses 100.0 -> 100.0 / 30.0 = 3.333333...
    expected_results = [6.0, 100.0 / 30.0]
    
    df = create_mock_dataframe(input_samples, input_concentrations)
    result_df = calculate_pool_concentrations_from_qubit_data(df, POOL_DICT)
    
    for i, expected in enumerate(expected_results):
        actual = result_df.iloc[i]["Amount_to_Take"]
        sample_name = input_samples[i]
        sample_conc = input_concentrations[i]
        
        failure_msg = (
            f"Test Failed for Sample: {sample_name} (Conc: {sample_conc}). "
            f"Expected: {expected}, but got: {actual}. "
            f"Rule Check: The concentration must be strictly LESS THAN the pool target (i.e., 5.0 must use 30.0 pool)."
        )
        
        assert round(actual, PLACES) == round(expected, PLACES), failure_msg


def test_invalid_or_zero_concentrations():
    """Test handling of NaN, zero, non-numeric strings, and negative concentrations (all should ideally result in NaN or the intended behavior)."""
    
    input_samples = ["S_NaN", "S_Zero", "S_String", "S_Negative"]
    input_concentrations = [np.nan, 0.0, "N/A", -10.0]
    
    df = create_mock_dataframe(input_samples, input_concentrations)
    result_df = calculate_pool_concentrations_from_qubit_data(df, POOL_DICT)
    
    for i in range(len(df)):
        sample_name = input_samples[i]
        actual = result_df.iloc[i]["Amount_to_Take"]
        
        # Check that explicit NaN, 0, or non-numeric entries result in NaN
        if sample_name in ["S_NaN", "S_Zero", "S_String"]:
            
            failure_msg = (
                f"Test Failed for Exclusion Case: {sample_name}. "
                f"Expected NaN (Excluded), but got: {actual}. "
                f"Rule Check: The logic must handle NaN or 0 concentration inputs."
            )
            assert np.isnan(actual), failure_msg
            
        # Check the negative concentration case (which currently calculates a ratio)
        elif sample_name == "S_Negative":
            # The current function calculates the ratio using the smallest pool target (5.0 / -10.0 = -0.5)
            expected = POOL_DICT['A'] / input_concentrations[i]
            
            failure_msg = (
                f"Test Failed for Negative Concentration Case: {sample_name}."
                f"Expected the calculated ratio: {expected}, but got: {actual}. "
                f"Note: For real-world robustness, this case should ideally be excluded (result in NaN)."
            )
            # Assert the calculated ratio to ensure code didn't crash
            assert round(actual, PLACES) == round(expected, PLACES), failure_msg