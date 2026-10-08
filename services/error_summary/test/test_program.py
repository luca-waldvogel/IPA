import pytest

from jobfit.services.error_summary.program import ErrorSummaryProgram
from jobfit.testutils.env import is_ci

from .helpers import EMPTY_ERROR_PATTERN_INPUT, INPUT


@pytest.fixture
def program():
    return ErrorSummaryProgram()


def test_program_empty_error_patterns(context, program):
    """
    Validates that the program is skipped when no error patterns are provided.
    Run through settings.env to test.
    """
    with context:
        output = program.run(
            input=EMPTY_ERROR_PATTERN_INPUT, llm_client=context.openai_client
        )
        result = output.result
        assert result is not None
        assert "No errors found (besides HTTP errors)" in result


@pytest.mark.skipif(
    is_ci(), reason="Test is not deterministic & only for manual testing"
)
def test_program(context, program):
    """
    Exclude openai_api_key and llm from AppConfig in conftest.py and run through settings.env to test.
    """
    with context:
        output = program.run(input=INPUT, llm_client=context.openai_client)
        result = output.result
        print(result)
        assert result is not None
