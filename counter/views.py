from django.shortcuts import render, get_object_or_404
from .models import Counter
from datadog import statsd
from ddtrace import tracer

def index(request):
    with tracer.trace("docker-counter", service="docker_counter_init") as span:
        span.set_tag("operation", "Counter run docker")
        if len(Counter.objects.filter(key='counter')) == 0:
            counter = Counter(key='counter', value=0)
            counter.save()
        else:
            counter = get_object_or_404(Counter, key='counter')
    
    counter.value+=1
    counter.save()
    context = {'value': counter.value}
    statsd.event(
                    "Counter",
                    "Counter run docker",
                    alert_type="info",
                    tags=["event:counter_init"],
                )
    return render(request, 'counter/index.html', context)
