from datadog import statsd
from ddtrace import tracer
from django.shortcuts import get_object_or_404, render

from .models import Counter


def index(request):
    with tracer.trace("docker-counter", service="docker_counter_init") as span:
        span.set_tag("operation", "Counter run docker")
        if len(Counter.objects.filter(key="counter")) == 0:
            counter = Counter(key="counter", value=0)
            counter.save()
        else:
            counter = get_object_or_404(Counter, key="counter")

    counter.value += 1
    counter.save()
    context = {"value": counter.value}
    statsd.event(
        "Counter",
        "Counter run docker",
        alert_type="info",
        tags=["event:counter_init"],
    )
    return render(request, "counter/index.html", context)
