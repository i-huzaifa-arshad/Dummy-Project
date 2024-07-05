from datadog import statsd
from ddtrace import tracer
from django.shortcuts import get_object_or_404, render

from .models import Counter

# Localhost
# def index(request):
#     with tracer.trace("localhost-counter", service="localhost_counter_init") as span:
#         span.set_tag("operation", "Counter run localhost")
#         if len(Counter.objects.filter(key="counter")) == 0:
#             counter = Counter(key="counter", value=0)
#             counter.save()
#         else:
#             counter = get_object_or_404(Counter, key="counter")

#     counter.value += 1
#     counter.save()
#     context = {"value": counter.value}
#     statsd.event(
#         "Localhost Counter",
#         "Counter run localhost",
#         alert_type="info",
#         tags=["event:localhost_counter_init"],
#     )
#     return render(request, "counter/index.html", context)

# Docker
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
        "Docker Counter",
        "Counter run docker",
        alert_type="info",
        tags=["event:docker_counter_init"],
    )
    return render(request, "counter/index.html", context)
