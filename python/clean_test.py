import re
import polars as pl
from clean_names import clean_names

# this is a unit test

# Example usage and testing
def test_clean_names():
    """Test the clean_names function with various column name scenarios"""
    # Create a test dataframe with problematic column names
    df = pl.DataFrame({
        " Name": [1, 2, 3],
        "First.Name": [4, 5, 6],
        "last-name": [7, 8, 9],
        "%_increase": [10, 11, 12],
        "123count": [13, 14, 15],
        "camelCase": [16, 17, 18],
        "PascalCase": [19, 20, 21],
        "  multiple    spaces  ": [22, 23, 24],
        "duplicate": [25, 26, 27],
        "duplicate": [28, 29, 30],  # Intentional duplicate
    })

    # Apply clean_names function
    cleaned_df = clean_names(df)

    # Print before and after
    print("Original column names:")
    print(df.columns)
    print("\nCleaned column names:")
    print(cleaned_df.columns)

    # Test different case types
    print("\nCamelCase:")
    print(clean_names(df, case_type="lower_camel").columns)

    print("\nPascalCase:")
    print(clean_names(df, case_type="upper_camel").columns)

    print("\nSCREAMING_SNAKE_CASE:")
    print(clean_names(df, case_type="screaming_snake").columns)

    return cleaned_df

if __name__ == "__main__":
    cleaned_df = test_clean_names()
    print("\nFinal DataFrame:")
    print(cleaned_df)