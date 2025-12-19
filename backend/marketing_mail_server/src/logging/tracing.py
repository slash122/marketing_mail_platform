import functools
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from src.app_settings import app_settings
from src.logging.logger import logger

tracer: trace.Tracer = trace.get_tracer(app_settings.TRACER_NAME)

# Tracing decorator
def trace_async(func):
    """
    Decorator that automatically creates a Span for the function execution.
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        if not app_settings.AZURE_LOGGING or tracer is None:
            return await func(*args, **kwargs)
        
        with tracer.start_as_current_span(func.__name__) as span:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                raise

    return async_wrapper

# ... existing logging code (get_logger) ...