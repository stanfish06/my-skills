"""
Great Expectations patterns for data pipeline validation.

Targets the GX 1.x Core API. Includes context setup, expectation suite
creation, and validation.
"""

import great_expectations as gx


# =============================================================================
# Context Setup
# =============================================================================

def get_pandas_context(datasource_name: str = "pandas_datasource"):
    """Get GX context with pandas data source configured.

    Args:
        datasource_name: Name for the pandas data source

    Returns:
        Tuple of (context, data_source)
    """
    context = gx.get_context()
    data_source = context.data_sources.add_pandas(name=datasource_name)
    return context, data_source


def add_dataframe_asset(data_source, asset_name: str):
    """Add DataFrame asset and return a whole-dataframe batch definition.

    The DataFrame itself is supplied at run time through
    `batch_parameters={"dataframe": df}`, not here.

    Args:
        data_source: GX pandas data source
        asset_name: Name for the data asset

    Returns:
        Batch definition covering the whole DataFrame
    """
    asset = data_source.add_dataframe_asset(name=asset_name)
    return asset.add_batch_definition_whole_dataframe(f"{asset_name}_batch")


# =============================================================================
# Expectation Suite Builder
# =============================================================================

def create_basic_suite(context, suite_name: str, columns_config: dict):
    """Create expectation suite from column configuration.

    Args:
        context: GX context
        suite_name: Name for the expectation suite
        columns_config: Dict mapping column names to expectation configs
            Example:
            {
                'user_id': {'not_null': True, 'unique': True, 'type': 'int'},
                'age': {'min': 0, 'max': 150},
                'status': {'values': ['active', 'inactive']},
                'email': {'regex': r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'}
            }

    Returns:
        Expectation suite
    """
    suite = context.suites.add(gx.ExpectationSuite(name=suite_name))

    for column, config in columns_config.items():
        # Column existence
        suite.add_expectation(
            gx.expectations.ExpectColumnToExist(column=column)
        )

        # Null check
        if config.get('not_null', False):
            suite.add_expectation(
                gx.expectations.ExpectColumnValuesToNotBeNull(column=column)
            )

        # Uniqueness
        if config.get('unique', False):
            suite.add_expectation(
                gx.expectations.ExpectColumnValuesToBeUnique(column=column)
            )

        # Type check
        if 'type' in config:
            suite.add_expectation(
                gx.expectations.ExpectColumnValuesToBeOfType(
                    column=column,
                    type_=config['type']
                )
            )

        # Range check
        if 'min' in config or 'max' in config:
            suite.add_expectation(
                gx.expectations.ExpectColumnValuesToBeBetween(
                    column=column,
                    min_value=config.get('min'),
                    max_value=config.get('max')
                )
            )

        # Categorical values
        if 'values' in config:
            suite.add_expectation(
                gx.expectations.ExpectColumnValuesToBeInSet(
                    column=column,
                    value_set=config['values']
                )
            )

        # Regex pattern
        if 'regex' in config:
            suite.add_expectation(
                gx.expectations.ExpectColumnValuesToMatchRegex(
                    column=column,
                    regex=config['regex']
                )
            )

    return suite


# =============================================================================
# Validation Runner
# =============================================================================

def run_validation(
    context,
    checkpoint_name: str,
    batch_definition,
    suite,
    df
) -> dict:
    """Run validation checkpoint and return results summary.

    Args:
        context: GX context
        checkpoint_name: Name for the checkpoint
        batch_definition: Batch definition from add_dataframe_asset()
        suite: ExpectationSuite from create_basic_suite()
        df: pandas DataFrame to validate

    Returns:
        Dict with 'success' bool and 'failures' list
    """
    validation_definition = context.validation_definitions.add(
        gx.ValidationDefinition(
            name=f"{checkpoint_name}_validation",
            data=batch_definition,
            suite=suite
        )
    )

    checkpoint = context.checkpoints.add(
        gx.Checkpoint(
            name=checkpoint_name,
            validation_definitions=[validation_definition]
        )
    )

    results = checkpoint.run(batch_parameters={"dataframe": df})

    summary = {
        'success': results.success,
        'failures': []
    }

    if not results.success:
        for result in results.run_results.values():
            for exp_result in result.results:
                if not exp_result.success:
                    summary['failures'].append({
                        'expectation': exp_result.expectation_config.type,
                        'column': exp_result.expectation_config.kwargs.get('column'),
                    })

    return summary
