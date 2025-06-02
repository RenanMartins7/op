from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.metrics import get_meter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased


import os




from opentelemetry.sdk.trace.sampling import Sampler, SamplingResult, Decision

class ListSizeZeroSampler(Sampler):
    def should_sample(
        self,
        parent_context,
        trace_id,
        name,
        kind,
        attributes,
        links
    ) -> SamplingResult:

        decision = Decision.RECORD_AND_SAMPLE
        list_size = attributes.get("List Size") if attributes else None

        

        # Só amostra se "List Size" existir e for igual a 1
        # if list_size == 1:
        #     decision = Decision.RECORD_AND_SAMPLE
        #     print(list_size)
        # else:
        #     decision = Decision.RECORD_AND_SAMPLE

        #decision = Decision.RECORD_AND_SAMPLE
        return SamplingResult(
            decision=decision,
            attributes={}
        )

    def get_description(self) -> str:
        return "Sampler that samples only if attribute 'List Size' == 0"


def traces_provider(resource):

    traces_endpoint = os.getenv("TRACES_ENDPOINT", "http://collector:4321/v1/traces")
    
    provider = TracerProvider(resource=resource, sampler=TraceIdRatioBased(1.0))
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint = traces_endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    return trace.get_tracer("api.tracer")

    
def metrics_provider(resource):
    metrics_endpoint = os.getenv("METRICS_ENDPOINT", "http://collector:4321/v1/metrics")

    reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=metrics_endpoint), export_interval_millis=1000)
    meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meterProvider)

    return metrics.get_meter("api.metrics")