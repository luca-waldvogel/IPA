import datetime

from pydantic_core import TzInfo

from jobfit.model.error_summary import ErrorCount, LogInsights, LogInsightsPattern
from jobfit.services.error_summary.program import ErrorSummaryRequest

EMPTY_ERROR_PATTERN_INPUT = ErrorSummaryRequest(
    error_patterns=[],
    http_errors=[
        ErrorCount(field="HTTP 400", value=0),
        ErrorCount(field="HTTP 401", value=1746),
        ErrorCount(field="HTTP 403", value=0),
        ErrorCount(field="HTTP 404", value=36073),
        ErrorCount(field="HTTP 405", value=0),
        ErrorCount(field="HTTP 409", value=0),
        ErrorCount(field="HTTP 500", value=0),
        ErrorCount(field="Unexpected", value=0),
    ],
)

INPUT = ErrorSummaryRequest(
    error_patterns=[
        LogInsightsPattern(
            pattern='<*>:/ecs/jobfit-api-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": "jobfit/api/auth/dependencies.py", "line": <*>, "message": "JWT has expired", "extra": {"otelSpanID": <*>, "otelTraceID": <*>, "otelTraceSampled": <*>, "otelServiceName": "jobfit-api"}}',
            log_groups=["/ecs/jobfit-api-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 19, 13, 24, 28, 309210, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="jobfit/api/auth/dependencies.py",
                line=137,
                message="JWT has expired",
                extra={
                    "otelSpanID": "c25acb870265fdd8",
                    "otelTraceID": "69bbf90cca8fc66ffcd2cd4032f8f2b6",
                    "otelTraceSampled": True,
                    "otelServiceName": "jobfit-api",
                },
            ),
            sample_count=1706,
        ),
        LogInsightsPattern(
            pattern='<*>:/aws/lambda/jobfit-extraction-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": "jobfit/services/extract/runner.py:<*>, "message": "Processing failed: ExtractionError: Failed to extract candidate information: <*> validation error for GptOutput\\n  Invalid JSON: EOF while parsing a value at line <*> column <*> [type=json_invalid, input_value=\'\', input_type=str]\\n    For further information visit https:<*>',
            log_groups=["/aws/lambda/jobfit-extraction-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 19, 14, 20, 41, 188132, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="jobfit/services/extract/runner.py:77",
                line=None,
                message="Processing failed: ExtractionError: Failed to extract candidate information: 1 validation error for GptOutput\n  Invalid JSON: EOF while parsing a value at line 1 column 0 [type=json_invalid, input_value='', input_type=str]\n    For further information visit https://errors.pydantic.dev/2.12/v/json_invalid",
                extra={"silent": False},
            ),
            sample_count=11,
        ),
        LogInsightsPattern(
            pattern='<*>:/aws/lambda/jobfit-elaboration-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": "jobfit/services/elaboration/main.py:<*>, "message": "Elaboration <*> (<*>) failed: <*> validation error for GptOutput\\n  Invalid JSON: EOF while parsing a value at line <*> column <*> [type=json_invalid, input_value=\'\', input_type=str]\\n    For further information visit https:<*>, "awsRequestId": <*>}\n',
            log_groups=["/aws/lambda/jobfit-elaboration-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 19, 14, 21, 38, 444520, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="jobfit/services/elaboration/main.py:65",
                line=None,
                message="Elaboration J_35cf7cc2-9f32-4ddf-aea6-3f0f0e5ea818:C_054e0de8-88e0-4bcf-95aa-9a1523e5ac05 (JobfitVariant.B2C_1) failed: 1 validation error for GptOutput\n  Invalid JSON: EOF while parsing a value at line 1 column 0 [type=json_invalid, input_value='', input_type=str]\n    For further information visit https://errors.pydantic.dev/2.12/v/json_invalid",
                extra=None,
            ),
            sample_count=5,
        ),
        LogInsightsPattern(
            pattern='<*>:/aws/lambda/jobfit-extraction-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": "jobfit/services/extract/runner.py:<*>, "message": "Processing failed: ExtractionError: Failed to extract candidate information: Content filter error (jailbreak): The response was filtered due to the prompt triggering Azure OpenAI\'s content management policy. Please modify your prompt and retry. To learn more about our content filtering policies ',
            log_groups=["/aws/lambda/jobfit-extraction-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 18, 19, 52, 48, 146898, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="jobfit/services/extract/runner.py:77",
                line=None,
                message="Processing failed: ExtractionError: Failed to extract candidate information: Content filter error (jailbreak): The response was filtered due to the prompt triggering Azure OpenAI's content management policy. Please modify your prompt and retry. To learn more about our content filtering policies please read our documentation: https://go.microsoft.com/fwlink/?linkid=2198766",
                extra={"silent": False},
            ),
            sample_count=5,
        ),
        LogInsightsPattern(
            pattern='<*>:/aws/lambda/jobfit-extraction-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": "jobfit/services/extract/emit.py:<*>, "message": "Maximum retry attempts exceeded for request <*>, "awsRequestId": <*>}\n',
            log_groups=["/aws/lambda/jobfit-extraction-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 19, 14, 12, 24, 745202, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="jobfit/services/extract/emit.py:36",
                line=None,
                message="Maximum retry attempts exceeded for request A_d037f66b-0961-4e72-b2cd-d7921ea7f9b8",
                extra=None,
            ),
            sample_count=4,
        ),
        LogInsightsPattern(
            pattern='<*>:/aws/lambda/jobfit-ingestion-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": <*>, "message": "An error occurred: HTTPError: <*> Client Error: Not Found for url: https:<*>:\\n[\'Traceback (most recent call last):\', \'  File \\"/var/task/jobfit/services/ingestion/extraction_request.py\\", line <*>, in build_extraction_request\', \'    document = ats.get_document(str(document_id))\', \'  File',
            log_groups=["/aws/lambda/jobfit-ingestion-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 19, 8, 36, 55, 439071, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="../lang/lib/python3.14/site-packages/jobfit/app/utils.py:30",
                line=None,
                message="An error occurred: HTTPError: 404 Client Error: Not Found for url: https://ats.jobcloud.ai//document/7896ae64-2bf3-40bd-a95d-f5515d64e53b\nTraceback:\n['Traceback (most recent call last):', '  File \"/var/task/jobfit/services/ingestion/extraction_request.py\", line 63, in build_extraction_request', '    document = ats.get_document(str(document_id))', '  File \"/var/lang/lib/python3.14/site-packages/jobfit/observability/logging_decorator.py\", line 33, in wrapper', '    result = original_func(*args, **kwargs)', '  File \"/var/lang/lib/python3.14/site-packages/jobfit/jc_client/marketplace_api_client.py\", line 51, in get_document', '    response.raise_for_status()', '    ~~~~~~~~~~~~~~~~~~~~~~~~~^^', '  File \"/var/lang/lib/python3.14/site-packages/requests/models.py\", line 1026, in raise_for_status', '    raise HTTPError(http_error_msg, response=self)', 'requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://ats.jobcloud.ai//document/7896ae64-2bf3-40bd-a95d-f5515d64e53b', '', 'During handling of the above exception, another exception occurred:', '', 'Traceback (most recent call last):', '  File \"/var/lang/lib/python3.14/site-packages/jobfit/app/aws_lambda.py\", line 28, in wrapper', '    response_data = fn(event, context)', '  File \"/var/task/jobfit/services/ingestion/lambda.py\", line 9, in handler', '    return handle(event)', '  File \"/var/lang/lib/python3.14/site-packages/jobfit/observability/tracing/decorator.py\", line 105, in wrapper', '    result = try_call_with_trace(original_func, *args, **kwargs)', '  File \"/var/lang/lib/python3.14/site-packages/jobfit/observability/tracing/decorator.py\", line 79, in try_call_with_trace', '    return func(*args, **kwargs, trace=trace)', '  File \"/var/task/jobfit/services/ingestion/main.py\", line 35, in handle', '    return _process(message, trace)', '  File \"/var/task/jobfit/services/ingestion/main.py\", line 41, in _process', '    result = runner.run(_processing_flow, message)', '  File \"/var/lang/lib/python3.14/site-packages/jobfit/app/flow/runner.py\", line 34, in run', '    return flow.get_result(Proceed(args), self._on_step)', '           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^', '  File \"/var/lang/lib/python3.14/site-packages/jobfit/app/flow/flow.py\", line 201, in wrapped_get_result', '    match self.get_result(parent_result, on_step):', '          ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^', '  File \"/var/lang/lib/python3.14/site-packages/jobfit/app/flow/flow.py\", line 160, in wrapped_get_result', '    return successor.get_result(self_proceed, on_step)', '           ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^', '  File \"/var/lang/lib/python3.14/site-packages/jobfit/app/flow/flow.py\", line 87, in wrapper', '    self_result = func(*arg_tuple)', '  File \"/var/lang/lib/python3.14/site-packages/jobfit/app/flow/flow.py\", line 178, in wrapped_func', '    return func(FlowControl[ROut, EOut](), *args)', '  File \"/var/task/jobfit/services/ingestion/extraction_request.py\", line 66, in build_extraction_request', '    raise SafeError(e)', 'jobfit.model.error.SafeError: HTTPError: 404 Client Error: Not Found for url: https://ats.jobcloud.ai//document/7896ae64-2bf3-40bd-a95d-f5515d64e53b']",
                extra=None,
            ),
            sample_count=2,
        ),
        LogInsightsPattern(
            pattern='<*>:/aws/lambda/jobfit-extraction-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": "jobfit/services/extract/runner.py:<*>, "message": "Processing failed: ExtractionIntermittentError: Failed to connect or connection lost", "awsRequestId": <*>, "extra": {"silent": <*>}}\n',
            log_groups=["/aws/lambda/jobfit-extraction-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 18, 23, 36, 36, 498927, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="jobfit/services/extract/runner.py:77",
                line=None,
                message="Processing failed: ExtractionIntermittentError: Failed to connect or connection lost",
                extra={"silent": False},
            ),
            sample_count=2,
        ),
        LogInsightsPattern(
            pattern='<*>:/aws/lambda/jobfit-extraction-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": "jobfit/services/extract/runner.py:<*>, "message": "Processing failed: ExtractionError: Failed to extract candidate information: <*> validation error for <*>  Field required [type=missing, input_value={\'annotations\': [], \'refu...ne, \'role\': \'assistant\'}, input_type=dict]\\n    For further information visit https:<*>, "awsRequestId": <*>',
            log_groups=["/aws/lambda/jobfit-extraction-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 19, 13, 43, 47, 715202, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="jobfit/services/extract/runner.py:77",
                line=None,
                message="Processing failed: ExtractionError: Failed to extract candidate information: 1 validation error for GptOutput\nchoices.0.message.content\n  Field required [type=missing, input_value={'annotations': [], 'refu...ne, 'role': 'assistant'}, input_type=dict]\n    For further information visit https://errors.pydantic.dev/2.12/v/missing",
                extra={"silent": False},
            ),
            sample_count=1,
        ),
        LogInsightsPattern(
            pattern='<*>:/aws/lambda/jobfit-extraction-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": "jobfit/services/extract/runner.py:<*>, "message": "Processing failed: ExtractionError: Failed to extract job information", "awsRequestId": <*>, "extra": {"silent": <*>}}\n',
            log_groups=["/aws/lambda/jobfit-extraction-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 19, 9, 53, 3, 446250, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="jobfit/services/extract/runner.py:77",
                line=None,
                message="Processing failed: ExtractionError: Failed to extract job information",
                extra={"silent": False},
            ),
            sample_count=1,
        ),
        LogInsightsPattern(
            pattern='<*>:/aws/lambda/jobfit-extraction-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": "jobfit/services/extract/runner.py:<*>, "message": "Processing failed: ExtractionError: Failed to extract candidate information: The server had an error while processing your request. Sorry about that!", "awsRequestId": <*>, "extra": {"silent": <*>}}\n',
            log_groups=["/aws/lambda/jobfit-extraction-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 19, 9, 40, 18, 764200, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="jobfit/services/extract/runner.py:77",
                line=None,
                message="Processing failed: ExtractionError: Failed to extract candidate information: The server had an error while processing your request. Sorry about that!",
                extra={"silent": False},
            ),
            sample_count=1,
        ),
        LogInsightsPattern(
            pattern='<*>:/aws/lambda/jobfit-extraction-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": "jobfit/services/extract/runner.py:<*>, "message": "Processing failed: TextractException: AWS Textract Error InvalidParameterException: Request has invalid parameters (HTTP <*>)", "awsRequestId": <*>, "extra": {"silent": <*>}}\n',
            log_groups=["/aws/lambda/jobfit-extraction-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 18, 20, 26, 46, 922228, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="jobfit/services/extract/runner.py:77",
                line=None,
                message="Processing failed: TextractException: AWS Textract Error InvalidParameterException: Request has invalid parameters (HTTP 400)",
                extra={"silent": False},
            ),
            sample_count=1,
        ),
        LogInsightsPattern(
            pattern='<*>:/aws/lambda/jobfit-extraction-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": "jobfit/services/extract/runner.py:<*>, "message": "Processing failed: ExtractionError: Failed to extract candidate information: Token limit reached. Input tokens: <*> Output tokens: <*>, "awsRequestId": <*>, "extra": {"silent": <*>}}\n',
            log_groups=["/aws/lambda/jobfit-extraction-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 19, 5, 36, 20, 870085, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="jobfit/services/extract/runner.py:77",
                line=None,
                message="Processing failed: ExtractionError: Failed to extract candidate information: Token limit reached. Input tokens: 3274. Output tokens: 5000.",
                extra={"silent": False},
            ),
            sample_count=1,
        ),
        LogInsightsPattern(
            pattern='<*>:/aws/lambda/jobfit-extraction-prod {"timestamp": <*>, "level": "ERROR", "logger": "root", "file": "jobfit/services/extract/runner.py:<*>, "message": "Processing failed: HTTPError: <*> Server Error: Internal Server Error for url: https:<*>=<*>, "awsRequestId": <*>, "extra": {"silent": <*>}}\n',
            log_groups=["/aws/lambda/jobfit-extraction-prod"],
            log_sample=LogInsights(
                timestamp=datetime.datetime(
                    2026, 3, 18, 16, 7, 26, 925764, tzinfo=TzInfo(0)
                ),
                level="ERROR",
                logger="root",
                file="jobfit/services/extract/runner.py:77",
                line=None,
                message="Processing failed: HTTPError: 500 Server Error: Internal Server Error for url: https://media.jobs.ch//media/93418976-13ee-4805-95b5-89f1e242f562?token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzcG90dGVkLmpvYnMuY2giLCJleHAiOjE3NzM4NTAxMDYsIm1lZGlhIjpbIjkzNDE4OTc2LTEzZWUtNDgwNS05NWI1LTg5ZjFlMjQyZjU2MiJdfQ.wG0HaGBeIQCgeuC2N56ZDgNX7uJKccJiP1sJk9YVXUvzQcrswlHC83jP6xikAraJAXFMVHy4TSzV9dFhKuFjxQ",
                extra={"silent": False},
            ),
            sample_count=1,
        ),
    ],
    http_errors=[
        ErrorCount(field="HTTP 400", value=0),
        ErrorCount(field="HTTP 401", value=1746),
        ErrorCount(field="HTTP 403", value=0),
        ErrorCount(field="HTTP 404", value=36073),
        ErrorCount(field="HTTP 405", value=0),
        ErrorCount(field="HTTP 409", value=0),
        ErrorCount(field="HTTP 500", value=0),
        ErrorCount(field="Unexpected", value=0),
    ],
)
