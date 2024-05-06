import datetime

from django.db.models import Count, Prefetch
from django.utils.timezone import make_aware
from django.shortcuts import get_object_or_404, render, redirect

from cpus.models import Cpu, ImageCpu, User
from cpus.forms import CpuForm, ImageCpuFormSet
from carousel.models import Carousel
from cpu_backend.constants import (
    DAYS_INTERVAL,
)


def suffiks(obj_count):
    """Подстановка суффиксов согласно числу"""
    if obj_count == 1:
        suff = ''
    elif 1 < obj_count < 5:
        suff = 'а'
    else:
        suff = 'ов'
    return suff


def interval_cpus(days):
    """
    Вычисление даты интервала
    и соответствующие ей добавленных процессоров
    """
    today = datetime.datetime.today()
    aware_today = make_aware(today)  # Присваиваем тайм зону
    interval_date = aware_today - datetime.timedelta(days=days)
    interval_cpus = Cpu.objects.filter(
        created_at__range=(interval_date, aware_today)
    )
    return [interval_cpus, interval_date]


def index(request):
    banners = Carousel.objects.all()
    users_list = User.objects.all().annotate(
        cpu_count=Count('cpus')
    ).order_by(
        '-cpu_count', '-registrated_at'
    )[0:3]
    cpu_count = Cpu.objects.count()
    cpu_count_suff = suffiks(cpu_count)
    user_count_suff = suffiks(users_list.count())
    all_cpus = Cpu.objects.all()
    month_cpus = interval_cpus(DAYS_INTERVAL)[0]
    interest_cpus = Cpu.objects.filter(
        in_interesting=True
    )

    context = {
        'cpu_count_suff': cpu_count_suff,
        'user_count_suff': user_count_suff,
        'banners': banners,
        'users_list': users_list,
        'all_cpus': all_cpus,
        'month_cpus': month_cpus,
        'interest_cpus': interest_cpus,
        'days_interval': DAYS_INTERVAL,
    }

    template_name = 'cpus/index.html'
    return render(request, template_name, context)


def about(request):
    banners = Carousel.objects.all()
    context = {
        'banners': banners,
    }

    template_name = 'cpus/about.html'
    return render(request, template_name, context)


def cpus_list(request):
    month_cpus = interval_cpus(DAYS_INTERVAL)[0]

    # cpus_list = Cpu.objects.all()
    # for cpu in cpus_list:
    #     # Ищем изображение по умолчанию для текущего процессора
    #     default_image = cpu.images.filter(default=True).first()
    #     # Добавляем найденное изображение
    #     # как атрибут default_image к текущему объекту Cpu
    #     = default_image

    # Получаем все процессоры с выбранными полями и связанными изображениями
    cpus_list = Cpu.objects.all().prefetch_related(
        Prefetch(
            'images',
            queryset=ImageCpu.objects.filter(default=True),
            to_attr='default_image'
        )
    )
    for cpu in cpus_list:
        if cpu in month_cpus:
            cpu.month_cpus = True

    context = {
        'cpus_list': cpus_list,
    }

    template_name = 'cpus/cpus_list.html'
    return render(request, template_name, context)


def cpu_detail(request, pk):
    interval_date = interval_cpus(DAYS_INTERVAL)[1]

    cpu = get_object_or_404(
        Cpu,
        id=pk,
    )
    cpu_images = ImageCpu.objects.filter(
        cpu__id=pk
    )

    if cpu.created_at >= interval_date:
        cpu.month_cpus = True

    context = {
        'cpu': cpu,
        'cpu_images': cpu_images,
    }

    template_name = 'cpus/cpu_detail.html'
    return render(request, template_name, context)


def user_cpus(request, pk):
    today = datetime.datetime.today()
    aware_today = make_aware(today)  # Присваиваем тайм зону
    month = aware_today - datetime.timedelta(days=3)
    month_cpus = Cpu.objects.filter(
        created_at__range=(month, aware_today)
    )

    user = User.objects.get(id=pk)
    cpus_list = Cpu.objects.filter(
        user=user.id
    ).prefetch_related(
        Prefetch(
            'images',
            queryset=ImageCpu.objects.filter(default=True),
            to_attr='default_image'
        )
    )
    for cpu in cpus_list:
        if cpu in month_cpus:
            cpu.month_cpus = True

    context = {
        'user': user,
        'cpus_list': cpus_list,
    }

    template_name = 'cpus/user_cpus.html'
    return render(request, template_name, context)


# def cpu_add_edit(request, pk=None):
#     if pk is not None:
#         instance = get_object_or_404(Cpu, id=pk)
#     else:
#         instance = None
#     form = CpuForm(request.POST or None, instance=instance)
#     context = {'form': form}
#     if form.is_valid():
#         form.save()
#     return render(request, 'cpus/cpu_add_edit.html', context)


# def cpu_delete(request, pk):
#     instance = get_object_or_404(Cpu, id=pk)
#     cpu_images = ImageCpu.objects.filter(
#         cpu__id=pk, default=True
#     ).first()
#     form = CpuForm(instance=instance)
#     context = {
#         'form': form,
#         'cpu_images': cpu_images,
#     }
#     if request.method == 'POST':
#         instance.delete()
#         return redirect('cpus:index')
#     return render(request, 'cpus/cpu_add_edit.html', context)

def cpu_add_edit(request, pk=None):
    if pk is not None:
        cpu_instance = get_object_or_404(Cpu, id=pk)
    else:
        cpu_instance = None

    if request.method == 'POST':
        cpu_form = CpuForm(request.POST, request.FILES, instance=cpu_instance)
        image_formset = ImageCpuFormSet(
            request.POST,
            request.FILES,
            instance=cpu_instance
        )
        if cpu_form.is_valid() and image_formset.is_valid():
            cpu_instance = cpu_form.save()
            image_formset.instance = cpu_instance
            image_formset.save()
            # Перенаправляем на страницу с деталями процессора
            return redirect('cpus:cpu_detail', pk=cpu_instance.pk)
    else:
        cpu_form = CpuForm(instance=cpu_instance)
        image_formset = ImageCpuFormSet(instance=cpu_instance)

    context = {'cpu_form': cpu_form, 'image_formset': image_formset}
    return render(request, 'cpus/cpu_add_edit.html', context)


def cpu_delete(request, pk):
    cpu_instance = get_object_or_404(Cpu, id=pk)
    # Получаем изображения процессора
    cpu_images = cpu_instance.images.filter(default=True).first()
    if request.method == 'POST':
        cpu_instance.delete()
        return redirect('cpus:index')
    return render(
        request,
        'cpus/cpu_add_edit.html',
        {'cpu_instance': cpu_instance, 'cpu_images': cpu_images}
    )
