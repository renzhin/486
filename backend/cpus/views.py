from django.shortcuts import get_object_or_404, render

from cpus.models import Cpu


def index(request):
    template_name = 'cpus/index.html'
    return render(request, template_name)


def about(request):
    template_name = 'cpus/about.html'
    return render(request, template_name)


def cpus_list(request):
    template_name = 'cpus/cpus_list.html'
    cpus_list = Cpu.objects.all()
    context = {
        'cpus_list': cpus_list,
    }
    return render(request, template_name, context)


def cpu_detail(request, pk):
    cpu = get_object_or_404(
        Cpu,
        id=pk,
    )
    context = {'cpu': cpu}

    template_name = 'cpus/cpu_detail.html'
    return render(request, template_name, context)
