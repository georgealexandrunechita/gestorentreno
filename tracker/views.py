from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Avg
from .models import Athlete, Workout, Session
from .forms import AthleteForm, WorkoutForm, SessionForm


@login_required
def athlete_list(request):
    queryset = Athlete.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    contexto = {
        'page_obj': page_obj,
        'athletes': page_obj.object_list,
    }
    return render(request, 'tracker/athlete_list.html', contexto)


@login_required
def athlete_detail(request, athlete_id):
    athlete = get_object_or_404(Athlete, id=athlete_id)
    contexto = {'athlete': athlete}
    return render(request, 'tracker/athlete_detail.html', contexto)


@login_required
def athlete_create(request):
    if request.method == 'POST':
        form = AthleteForm(request.POST)
        if form.is_valid():
            athlete = form.save(commit=False)
            athlete.user = request.user
            athlete.save()
            return redirect('athlete_detail', athlete_id=athlete.id)
    else:
        form = AthleteForm()
    return render(request, 'tracker/athlete_form.html', {'form': form})


@login_required
def athlete_update(request, athlete_id):
    athlete = get_object_or_404(Athlete, id=athlete_id, user=request.user)
    if request.method == 'POST':
        form = AthleteForm(request.POST, instance=athlete)
        if form.is_valid():
            form.save()
            return redirect('athlete_detail', athlete_id=athlete.id)
    else:
        form = AthleteForm(instance=athlete)
    return render(request, 'tracker/athlete_form.html', {'form': form, 'athlete': athlete})


@login_required
def workout_list(request):
    athlete = Athlete.objects.filter(user=request.user).first()
    queryset = Workout.objects.filter(atleta=athlete).order_by('-fecha')
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    contexto = {
        'page_obj': page_obj,
        'workouts': page_obj.object_list,
    }
    return render(request, 'tracker/workout_list.html', contexto)


@login_required
def workout_detail(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, atleta__user=request.user)
    sesiones = Session.objects.filter(workout=workout)
    contexto = {
        'workout': workout,
        'sesiones': sesiones,
    }
    return render(request, 'tracker/workout_detail.html', contexto)


@login_required
def workout_create(request):
    athlete = Athlete.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.atleta = athlete
            workout.save()
            return redirect('workout_detail', workout_id=workout.id)
    else:
        form = WorkoutForm()
    return render(request, 'tracker/workout_form.html', {'form': form})


@login_required
def workout_update(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, atleta__user=request.user)
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return redirect('workout_detail', workout_id=workout.id)
    else:
        form = WorkoutForm(instance=workout)
    return render(request, 'tracker/workout_form.html', {'form': form, 'workout': workout})


@login_required
def workout_delete(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, atleta__user=request.user)
    if request.method == 'POST':
        workout.delete()
        return redirect('workout_list')
    return render(request, 'tracker/workout_confirm_delete.html', {'workout': workout})


@login_required
def session_list(request):
    athlete = Athlete.objects.filter(user=request.user).first()
    queryset = Session.objects.filter(workout__atleta=athlete)

    tipo = request.GET.get('tipo')
    if tipo:
        queryset = queryset.filter(workout__tipo=tipo)

    order = request.GET.get('order')
    if order:
        queryset = queryset.order_by(order)
    else:
        queryset = queryset.order_by('-id')

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tipos_disponibles = Workout.TIPO_CHOICES

    contexto = {
        'page_obj': page_obj,
        'sessions': page_obj.object_list,
        'tipo_filtrado': tipo,
        'order': order,
        'tipos_disponibles': tipos_disponibles,
    }
    return render(request, 'tracker/session_list.html', contexto)


@login_required
def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id, workout__atleta__user=request.user)
    contexto = {'session': session}
    return render(request, 'tracker/session_detail.html', contexto)


@login_required
def session_create(request):
    athlete = Athlete.objects.filter(user=request.user).first()
    workouts_usuario = Workout.objects.filter(atleta=athlete)
    if request.method == 'POST':
        form = SessionForm(request.POST)
        workout_id = request.POST.get('workout_id')
        if form.is_valid() and workout_id:
            workout = get_object_or_404(Workout, id=workout_id, atleta=athlete)
            session = form.save(commit=False)
            session.workout = workout
            session.save()
            return redirect('session_detail', session_id=session.id)
    else:
        form = SessionForm()
    contexto = {
        'form': form,
        'workouts': workouts_usuario,
    }
    return render(request, 'tracker/session_form.html', contexto)


@login_required
def session_delete(request, session_id):
    session = get_object_or_404(Session, id=session_id, workout__atleta__user=request.user)
    if request.method == 'POST':
        session.delete()
        return redirect('session_list')
    return render(request, 'tracker/session_confirm_delete.html', {'session': session})


@login_required
def statistics(request):
    athlete = Athlete.objects.filter(user=request.user).first()
    workouts = Workout.objects.filter(atleta=athlete)
    sessions = Session.objects.filter(workout__atleta=athlete)

    # 1) Distancia total por tipo
    dist_por_tipo = workouts.values('tipo').annotate(total_dist=Sum('distancia_km'))
    labels1 = [d['tipo'] for d in dist_por_tipo]
    data1 = [float(d['total_dist'] or 0) for d in dist_por_tipo]

    # 2) Número de entrenos por mes
    entrenos_por_mes = workouts.values('fecha__month').annotate(total=Count('id')).order_by('fecha__month')
    labels2 = [str(e['fecha__month']) for e in entrenos_por_mes]
    data2 = [e['total'] for e in entrenos_por_mes]

    # 3) Duración total por mes (horas)
    duracion_por_mes = workouts.values('fecha__month').annotate(total_dur=Sum('duracion')).order_by('fecha__month')
    labels3 = [str(d['fecha__month']) for d in duracion_por_mes]
    data3 = [(d['total_dur'].total_seconds() / 3600) if d['total_dur'] else 0 for d in duracion_por_mes]

    # 4) FC media por tipo
    fc_media_por_tipo = sessions.values('workout__tipo').annotate(media_fc=Avg('fc_media'))
    labels4 = [f['workout__tipo'] for f in fc_media_por_tipo]
    data4 = [float(f['media_fc'] or 0) for f in fc_media_por_tipo]

    # 5) Calorías totales por tipo
    calorias_por_tipo = sessions.values('workout__tipo').annotate(total_cal=Sum('calorias')).order_by('workout__tipo')
    labels5 = [c['workout__tipo'] for c in calorias_por_tipo]
    data5 = [c['total_cal'] or 0 for c in calorias_por_tipo]

    contexto = {
        'labels1': labels1, 'data1': data1,
        'labels2': labels2, 'data2': data2,
        'labels3': labels3, 'data3': data3,
        'labels4': labels4, 'data4': data4,
        'labels5': labels5, 'data5': data5,
    }
    return render(request, 'tracker/statistics.html', contexto)
