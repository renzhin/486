import datetime

from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Prefetch
from django.utils.timezone import make_aware
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.shortcuts import get_object_or_404, render
# from django.shortcuts import redirect

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
    users = User.objects.all()
    users_list = users.annotate(
        cpu_count=Count('cpus')
    ).order_by(
        '-cpu_count', '-registrated_at'
    )[0:3]
    cpu_count = Cpu.objects.count()
    cpu_count_suff = suffiks(cpu_count)
    user_count_suff = suffiks(users.count())
    all_cpus = Cpu.objects.all()
    month_cpus = interval_cpus(DAYS_INTERVAL)[0]
    interest_cpus = Cpu.objects.filter(
        in_interesting=True
    )

    context = {
        'cpu_count_suff': cpu_count_suff,
        'user_count_suff': user_count_suff,
        'banners': banners,
        'users': users,
        'users_list': users_list,
        'all_cpus': all_cpus,
        'month_cpus': month_cpus,
        'interest_cpus': interest_cpus,
        'days_interval': DAYS_INTERVAL,
    }

    template_name = 'cpus/index.html'
    return render(request, template_name, context)


def cpus_list(request):
    month_cpus = interval_cpus(DAYS_INTERVAL)[0]

    # Получаем все процессоры с выбранными полями и связанными изображениями
    cpus_list = Cpu.objects.all().prefetch_related(
        Prefetch(
            'images',
            queryset=ImageCpu.objects.filter(default=True),
            to_attr='default_image'
        )
    )
    paginator = Paginator(cpus_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for cpu in page_obj:
        if cpu in month_cpus:
            cpu.month_cpus = True

    context = {
        'page_obj': page_obj,
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


class About(TemplateView):
    """
    Вью для страницы «О проекте»
    """
    template_name = 'cpus/about.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['banners'] = Carousel.objects.all()
        return data


class CpuCreateView(LoginRequiredMixin, CreateView):
    """
    Вью для создания процессора
    """
    model = Cpu
    form_class = CpuForm
    template_name = 'cpus/cpu_add_edit.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['image_formset'] = ImageCpuFormSet(
                self.request.POST,
                self.request.FILES
            )
        else:
            data['image_formset'] = ImageCpuFormSet()
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user

        context = self.get_context_data()
        image_formset = context['image_formset']

        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()

            # Отправка письма после успешного сохранения формы и формсета
            part_number = self.object.part_number
            user = self.object.user
            send_mail(
                subject='Добавление процессора на сайт 486.renzhin.ru',
                message=f'{user} добавил процессор {part_number}',
                from_email='noreplay@486.renzhin.ru',
                recipient_list=['admin@486.renzhin.ru'],
                fail_silently=True,
            )

            return super().form_valid(form)

        else:
            return self.form_invalid(form)


class CpuUpdateView(LoginRequiredMixin, UpdateView):
    """
    Вью для редактирования процессора
    """
    model = Cpu
    form_class = CpuForm
    template_name = 'cpus/cpu_add_edit.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['image_formset'] = ImageCpuFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            data['image_formset'] = ImageCpuFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Cpu, pk=kwargs['pk'])
        if instance.user != request.user:
            # Здесь вызов ошибки, или редирект на нужную страницу.
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CpuDeleteView(LoginRequiredMixin, DeleteView):
    """
    Вью для удаления процессора
    """
    model = Cpu
    template_name = 'cpus/cpu_add_edit.html'
    success_url = reverse_lazy('cpus:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['cpu_images'] = data['cpu'].images.filter(default=True).first()
        return data

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Cpu, pk=kwargs['pk'])
        if instance.user != request.user:
            # Здесь вызов ошибки, или редирект на нужную страницу.
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
