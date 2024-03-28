import datetime

from django.db.models import Count
from django.utils.timezone import make_aware
from django.shortcuts import get_object_or_404, render

from cpus.models import Cpu, ImageCpu, User


def index(request):
    template_name = 'cpus/index.html'
    users_list = User.objects.all().annotate(
        cpu_count=Count('cpus')
    ).order_by(
        '-cpu_count'
    )
    all_cpus = Cpu.objects.all()

    today = datetime.datetime.today()
    aware_today = make_aware(today)  # Присваиваем тайм зону
    month = aware_today - datetime.timedelta(days=30)

    month_cpus = Cpu.objects.filter(
        created_at__range=(month, aware_today)
    )
    interest_cpus = Cpu.objects.filter(
        in_interesting=True
    )

    context = {
        'users_list': users_list,
        'all_cpus': all_cpus,
        'month_cpus': month_cpus,
        'interest_cpus': interest_cpus,
    }
    return render(request, template_name, context)


def about(request):
    template_name = 'cpus/about.html'
    return render(request, template_name)


def cpus_list(request):
    template_name = 'cpus/cpus_list.html'
    cpus_list = Cpu.objects.all()
    for cpu in cpus_list:
        # Ищем изображение по умолчанию для текущего процессора
        default_image = cpu.images.filter(default=True).first()
        # Добавляем найденное изображение
        # как атрибут default_image к текущему объекту Cpu
        cpu.default_image = default_image
    context = {
        'cpus_list': cpus_list,
    }
    return render(request, template_name, context)


def cpu_detail(request, pk):
    cpu = get_object_or_404(
        Cpu,
        id=pk,
    )
    cpu_images = ImageCpu.objects.filter(
        cpu__id=pk
    )
    context = {
        'cpu': cpu,
        'cpu_images': cpu_images,
    }

    template_name = 'cpus/cpu_detail.html'
    return render(request, template_name, context)


def user_cpus(request, pk):
    template_name = 'cpus/user_cpus.html'
    user = User.objects.get(id=pk)
    cpus_list = Cpu.objects.filter(
        user=user.id
    )
    for cpu in cpus_list:
        # Ищем изображение по умолчанию для текущего процессора
        default_image = cpu.images.filter(default=True).first()
        # Добавляем найденное изображение
        # как атрибут default_image к текущему объекту Cpu
        cpu.default_image = default_image
    context = {
        'user': user,
        'cpus_list': cpus_list,
    }
    return render(request, template_name, context)
