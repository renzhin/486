from django.shortcuts import render


def index(request):
    template_name = 'cpus/index.html'
    return render(request, template_name)


def about(request):
    template_name = 'cpus/about.html'
    return render(request, template_name)


def cpus_list(request):
    template_name = 'cpus/cpus_list.html'
    return render(request, template_name)


def cpu_detail(request, pk):
    template_name = 'cpus/cpu_detail.html'
    return render(request, template_name)
