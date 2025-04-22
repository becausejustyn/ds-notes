import re
import polars as pl

def clean_names(df, case_type="snake", replace_with_underscore=r"[^a-zA-Z0-9_]"):
    """
    Clean dataframe column names similar to janitor::clean_names() in R.

    Parameters:
    -----------
    df : polars.DataFrame
        The dataframe with column names to clean
    case_type : str, default "snake"
        The case to convert column names to. Options: "snake", "lower_camel", "upper_camel", "screaming_snake"
    replace_with_underscore : str, default r"[^a-zA-Z0-9_]"
        Regex pattern of characters to be replaced with underscores

    Returns:
    --------
    polars.DataFrame
        Dataframe with cleaned column names
    """
    # Get current column names
    original_cols = df.columns
    new_cols = []

    for col in original_cols:
        # Step 1: Trim leading/trailing whitespace
        name = col.strip()

        # Step 2: Ensure name starts with a letter or underscore by adding 'x' if needed
        if name and not re.match(r'^[a-zA-Z_]', name):
            name = 'x' + name

        # Step 3: Replace all special characters with underscores
        name = re.sub(replace_with_underscore, '_', name)

        # Step 4: Replace multiple consecutive underscores with a single underscore
        name = re.sub(r'_{2,}', '_', name)

        # Step 5: Remove leading/trailing underscores
        name = name.strip('_')

        # Step 6: Handle empty string (should be rare after all processing)
        if not name:
            name = 'x'

        # Step 7: Apply case transformation - convert to snake_case first for consistency
        # Convert camelCase or PascalCase to snake_case
        name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
        name = name.lower()

        # Then transform to the requested case type
        case_transformations = {
            "snake": lambda x: x,  # already in snake_case
            "lower_camel": lambda x: x.split('_')[0] + ''.join(part.capitalize() for part in x.split('_')[1:]),
            "upper_camel": lambda x: ''.join(part.capitalize() for part in x.split('_')),
            "screaming_snake": lambda x: x.upper()
        }

        # Apply the appropriate transformation function
        transform_func = case_transformations.get(case_type, case_transformations["snake"])
        name = transform_func(name)

        new_cols.append(name)

    # Step 8: Handle duplicate names by adding numbers
    seen = {}
    for i, name in enumerate(new_cols):
        if name in seen:
            counter = seen[name]
            seen[name] += 1
            new_cols[i] = f"{name}_{counter}"
        else:
            seen[name] = 1

    # Create a new dataframe with renamed columns
    return df.select([
        df.get_column(original_cols[i]).alias(new_cols[i])
        for i in range(len(original_cols))
    ])
