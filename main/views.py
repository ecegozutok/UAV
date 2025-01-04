from django.shortcuts import render, redirect, get_object_or_404
from . forms import RegistrationForm , WingForm, FuselageForm, TailForm, AvionicsForm, AssemblyForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .decorators import check_wing_permissions,check_fuselage_permissions, check_tail_permissions, check_avionics_permissions,check_assembly_permissions
from .models import Wing, Fuselage, Tail, Avionics, Aircraft, UsedWing, UsedFuselage, UsedTail, UsedAvionics
from .serializers import PartAvailabilitySerializer
# Create your views here.
@login_required(login_url="/login")
def home(request):
    """
    Handles operations and renders the unified home page.
    Supports deletion of Wing, Fuselage, Tail, Avionics, and Aircraft objects.
    Ensures Aircraft deletion also cleans up related used parts and resets parts availability.
    """
    if request.method == "POST":
        item_id = request.POST.get('item-id')
        item_type = request.POST.get('item-type')
        print(f"Item ID: {item_id}, Item Type: {item_type}")
        if item_id and item_type:
            # Handle Wing Deletion
            if item_type == "wing" and (request.user.has_perm('main.delete_wing') or request.user.is_staff):
                item = get_object_or_404(Wing, id=item_id)
                item.delete()
                messages.success(request, "Wing deleted successfully!")

            # Handle Fuselage Deletion
            elif item_type == "fuselage" and (request.user.has_perm('main.delete_fuselage') or request.user.is_staff):
                item = get_object_or_404(Fuselage, id=item_id)
                item.delete()
                messages.success(request, "Fuselage deleted successfully!")

            # Handle Tail Deletion
            elif item_type == "tail" and (request.user.has_perm('main.delete_tail') or request.user.is_staff):
                item = get_object_or_404(Tail, id=item_id)
                item.delete()
                messages.success(request, "Tail deleted successfully!")

            # Handle Avionics Deletion
            elif item_type == "avionics" and (request.user.has_perm('main.delete_avionics') or request.user.is_staff):
                item = get_object_or_404(Avionics, id=item_id)
                item.delete()
                messages.success(request, "Avionics deleted successfully!")

            # Handle Aircraft Deletion
            elif item_type == "aircraft" and (request.user.has_perm('main.delete_aircraft') or request.user.is_staff):
                item = get_object_or_404(Aircraft, id=item_id)

                # Step 1: Delete associated entries from Used tables
                UsedWing.objects.filter(aircraft=item).delete()
                UsedFuselage.objects.filter(aircraft=item).delete()
                UsedTail.objects.filter(aircraft=item).delete()
                UsedAvionics.objects.filter(aircraft=item).delete()

                # Step 2: Reset original parts' author field (mark them as available)
                if item.wing_id:
                    item.wing_id.author = item.author
                    item.wing_id.save()
                if item.fuselage_id:
                    item.fuselage_id.author = item.author
                    item.fuselage_id.save()
                if item.tail_id:
                    item.tail_id.author = item.author
                    item.tail_id.save()
                if item.avionics_id:
                    item.avionics_id.author = item.author
                    item.avionics_id.save()

                # Step 3: Delete the Aircraft
                item.delete()

                messages.success(request, "Aircraft disassembled successfully! Associated parts are now available for reuse.")

        return redirect('home')

    context = {
        'wings': Wing.objects.all(),
        'wing_types': Wing.WingType.choices,
        'can_view_wing_page': request.user.has_perm('main.view_create_wing_page'),

        'fuselages': Fuselage.objects.all(),
        'fuselage_types': Fuselage.FuselageType.choices,
        'can_view_fuselage_page': request.user.has_perm('main.view_create_fuselage_page'),

        'tails': Tail.objects.all(),
        'tail_types': Tail.TailType.choices,
        'can_view_tail_page': request.user.has_perm('main.view_create_tail_page'),

        'avionics': Avionics.objects.all(),
        'avionics_types': Avionics.AvionicsType.choices,
        'can_view_avionics_page': request.user.has_perm('main.view_create_avionics_page'),

        'aircraft': Aircraft.objects.all(),
        'aircraft_types': Aircraft.AircraftType.choices,
        'can_view_aircraft_page': request.user.has_perm('main.view_create_aircraft_page'),
    }

    return render(request, 'main/home.html', context)


@login_required(login_url='/login')
def create_page(request):
    if request.user.has_perm('main.create_tail'):
        return redirect('create_tail')  # Redirect to Tail creation page

    if request.user.has_perm('main.create_wing'):
        return redirect('create_wing')  # Redirect to Wing creation page

    if request.user.has_perm('main.create_fuselage'):
        return redirect('create_fuselage')  # Redirect to Fuselage creation page

    if request.user.has_perm('main.create_avionics'):
        return redirect('create_avionics')  # Redirect to Avionics creation page

    if request.user.has_perm('main.create_aircraft'):
        return redirect("create_aircraft")

    # If no permissions match, redirect to home or show an error page
    return redirect('/home')  # Default fallback

@login_required(login_url="/login")
@check_wing_permissions
def create_wing(request):
    if request.method == 'POST':
        form = WingForm(request.POST)
        if form.is_valid():
            wing = form.save(commit=False)
            wing.author = request.user
            wing.save()
            return redirect("/home")
    else:
        form = WingForm()

    return render(request, "main/create_wing.html", {"form": form})

@login_required(login_url="/login")
@check_fuselage_permissions
def create_fuselage(request):
    if request.method == 'POST':
        form = FuselageForm(request.POST)
        if form.is_valid():
            fuselage = form.save(commit=False)
            fuselage.author = request.user
            fuselage.save()
            return redirect("/home")
    else:
        form = FuselageForm()

    return render(request, "main/create_fuselage.html", {"form": form})

@login_required(login_url="/login")
@check_tail_permissions
def create_tail(request):
    if request.method == 'POST':
        form = TailForm(request.POST)
        if form.is_valid():
            tail = form.save(commit=False)
            tail.author = request.user
            tail.save()
            return redirect("/home")
    else:
        form = TailForm()

    return render(request, "main/create_tail.html", {"form": form})

@login_required(login_url="/login")
@check_avionics_permissions
def create_avionics(request):
    if request.method == 'POST':
        form = AvionicsForm(request.POST)
        if form.is_valid():
            avionics = form.save(commit=False)
            avionics.author = request.user
            avionics.save()
            return redirect("/home")
    else:
        form = AvionicsForm()

    return render(request, "main/create_avionics.html", {"form": form})


@login_required(login_url="/login")
@check_assembly_permissions
def create_aircraft(request):
    """
    Handles the creation of an aircraft, ensuring all required parts are available and not already used.
    """
    aircraft_types = [
        ('TB2', 'TB2'),
        ('TB3', 'TB3'),
        ('AKINCI', 'AKINCI'),
        ('KIZILELMA', 'KIZILELMA')
    ]

    # Fetch current parts availability dynamically
    parts_data = {
        type_code: {
            'wings': Wing.objects.filter(
                wing_type=type_code
            ).exclude(
                id__in=UsedWing.objects.values_list('wing_id', flat=True)
            ).count(),

            'fuselages': Fuselage.objects.filter(
                fuselage_type=type_code
            ).exclude(
                id__in=UsedFuselage.objects.values_list('fuselage_id', flat=True)
            ).count(),

            'tails': Tail.objects.filter(
                tail_type=type_code
            ).exclude(
                id__in=UsedTail.objects.values_list('tail_id', flat=True)
            ).count(),

            'avionics': Avionics.objects.filter(
                avionics_type=type_code
            ).exclude(
                id__in=UsedAvionics.objects.values_list('avionics_id', flat=True)
            ).count()
        }
        for type_code, _ in aircraft_types
    }

    if request.method == "POST":
        form = AssemblyForm(request.POST)
        if form.is_valid():
            aircraft = form.save(commit=False)
            aircraft_type = aircraft.aircraft_type

            # Fetch required parts, ensuring they are not already used
            required_parts = {
                'wing': Wing.objects.filter(
                    wing_type=aircraft_type
                ).exclude(id__in=UsedWing.objects.values_list('wing_id', flat=True)).first(),

                'fuselage': Fuselage.objects.filter(
                    fuselage_type=aircraft_type
                ).exclude(id__in=UsedFuselage.objects.values_list('fuselage_id', flat=True)).first(),

                'tail': Tail.objects.filter(
                    tail_type=aircraft_type
                ).exclude(id__in=UsedTail.objects.values_list('tail_id', flat=True)).first(),

                'avionics': Avionics.objects.filter(
                    avionics_type=aircraft_type
                ).exclude(id__in=UsedAvionics.objects.values_list('avionics_id', flat=True)).first(),
            }

            # Check availability
            missing_parts = [part for part, obj in required_parts.items() if obj is None]

            if missing_parts:
                messages.error(
                    request,
                    f"Cannot create aircraft. Missing or already used parts: {', '.join(missing_parts)}"
                )
                return redirect('create_aircraft')

            # Reserve parts
            aircraft.wing_id = required_parts['wing']
            aircraft.fuselage_id = required_parts['fuselage']
            aircraft.tail_id = required_parts['tail']
            aircraft.avionics_id = required_parts['avionics']

            # Save the aircraft
            aircraft.author = request.user
            aircraft.save()

            # Move parts info to Used tables
            UsedWing.objects.create(
                aircraft=aircraft,
                wing=required_parts['wing'],
                aircraft_type=aircraft.aircraft_type
            )
            UsedFuselage.objects.create(
                aircraft=aircraft,
                fuselage=required_parts['fuselage'],
                aircraft_type=aircraft.aircraft_type
            )
            UsedTail.objects.create(
                aircraft=aircraft,
                tail=required_parts['tail'],
                aircraft_type=aircraft.aircraft_type
            )
            UsedAvionics.objects.create(
                aircraft=aircraft,
                avionics=required_parts['avionics'],
                aircraft_type=aircraft.aircraft_type
            )

            # Mark parts as reserved
            for part in required_parts.values():
                part.author = request.user
                part.save()

            messages.success(request, "Aircraft created successfully with all parts recorded as used!")
            return redirect('home')

        else:
            messages.error(request, "Invalid form submission. Please check the inputs.")

    else:
        form = AssemblyForm()

    return render(request, 'main/create_aircraft.html', {
        'form': form,
        'aircraft_types': aircraft_types,
        'parts_data': parts_data,
    })


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            group_name = form.cleaned_data['team']

            group, created = Group.objects.get_or_create(name=group_name)
            assign_permissions_to_group(group, group_name)
            user.groups.add(group)
            messages.success(request, f'Account created successfully and added to group: {group.name}')
            return redirect('/home')
    else :
        form = RegistrationForm()
    return  render(request, 'registration/sign_up.html', {"form" : form})

def assign_permissions_to_group(group, group_name):
    """Dynamically assign permissions to groups."""
    if group_name == 'wing':
        content_type = ContentType.objects.get_for_model(Wing)
        permissions = Permission.objects.filter(content_type=content_type)
        group.permissions.add(*permissions)
    elif group_name == 'fuselage':
        content_type = ContentType.objects.get_for_model(Fuselage)
        permissions = Permission.objects.filter(content_type=content_type)
        group.permissions.add(*permissions)
    elif group_name == 'tail':
        content_type = ContentType.objects.get_for_model(Tail)
        permissions = Permission.objects.filter(content_type=content_type)
        group.permissions.add(*permissions)
    elif group_name == 'avionics':
        content_type = ContentType.objects.get_for_model(Avionics)
        permissions = Permission.objects.filter(content_type=content_type)
        group.permissions.add(*permissions)
    elif group_name == 'assembly':
        content_type = ContentType.objects.get_for_model(Aircraft)
        permissions = Permission.objects.filter(content_type=content_type)
        group.permissions.add(*permissions)


@api_view(['GET'])
def wing_counts(request):
    """
    API endpoint to return counts of different types of wings.
    """
    wing_counts = Wing.objects.values('wing_type').annotate(count=Count('id'))
    return Response(wing_counts)

@api_view(['GET'])
def fuselage_counts(request):
    """
    API endpoint to return counts of different types of fuselages.
    """
    fuselage_counts = Fuselage.objects.values('fuselage_type').annotate(count=Count('id'))
    return Response(fuselage_counts)

@api_view(['GET'])
def tail_counts(request):
    """
    API endpoint to return counts of different types of tails.
    """
    tail_counts = Tail.objects.values('tail_type').annotate(count=Count('id'))
    return Response(tail_counts)
@api_view(['GET'])
def avionics_counts(request):
    """
    API endpoint to return counts of different types of avionics.
    """
    avionics_counts = Avionics.objects.values('avionics_type').annotate(count=Count('id'))
    return Response(avionics_counts)

@api_view(['GET'])
def used_wing_counts(request):
    """
    API endpoint to return counts of different types of used wings.
    """
    used_wing_counts = UsedWing.objects.values('wing__wing_type').annotate(count=Count('id'))
    formatted_counts = [
        {'wing_type': item['wing__wing_type'], 'count': item['count']}
        for item in used_wing_counts
    ]
    return Response(formatted_counts)


@api_view(['GET'])
def used_fuselage_counts(request):
    """
    API endpoint to return counts of different types of used fuselages.
    """
    used_fuselage_counts = UsedFuselage.objects.values('fuselage__fuselage_type').annotate(count=Count('id'))
    formatted_counts = [
        {'fuselage_type': item['fuselage__fuselage_type'], 'count': item['count']}
        for item in used_fuselage_counts
    ]
    return Response(formatted_counts)


@api_view(['GET'])
def used_tail_counts(request):
    """
    API endpoint to return counts of different types of used tails.
    """
    used_tail_counts = UsedTail.objects.values('tail__tail_type').annotate(count=Count('id'))
    formatted_counts = [
        {'tail_type': item['tail__tail_type'], 'count': item['count']}
        for item in used_tail_counts
    ]
    return Response(formatted_counts)


@api_view(['GET'])
def used_avionics_counts(request):
    """
    API endpoint to return counts of different types of used avionics.
    """
    used_avionics_counts = UsedAvionics.objects.values('avionics__avionics_type').annotate(count=Count('id'))
    formatted_counts = [
        {'avionics_type': item['avionics__avionics_type'], 'count': item['count']}
        for item in used_avionics_counts
    ]
    return Response(formatted_counts)


@api_view(['GET'])
def wing_availability(request, type_code=None):
    """
    API endpoint to return total, used, and available counts of wings.
    Supports optional filtering by `type_code`.
    """
    query = Wing.objects.all()
    if type_code:
        query = query.filter(wing_type=type_code)

    # Total count (all wings of this type)
    total_counts = query.values('wing_type').annotate(total=Count('id'))

    # Used count (wings that are currently in use)
    used_counts = UsedWing.objects.filter(
        wing__wing_type=type_code if type_code else query.values('wing_type')
    ).values('wing__wing_type').annotate(used=Count('id'))

    # Available count (excluding used wings explicitly)
    available_counts = query.exclude(
        id__in=UsedWing.objects.values_list('wing_id', flat=True)
    ).values('wing_type').annotate(available=Count('id'))

    availability_data = []

    total_dict = {item['wing_type']: item['total'] for item in total_counts}
    used_dict = {item['wing__wing_type']: item['used'] for item in used_counts}
    available_dict = {item['wing_type']: item['available'] for item in available_counts}

    for wing_type, total in total_dict.items():
        used = used_dict.get(wing_type, 0)
        available = available_dict.get(wing_type, total - used)
        availability_data.append({
            'part_type': wing_type,
            'total': total,
            'used': used,
            'available': available
        })

    serializer = PartAvailabilitySerializer(availability_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def fuselage_availability(request, type_code=None):
    """
    API endpoint to return total, used, and available counts of fuselages.
    """
    query = Fuselage.objects.all()
    if type_code:
        query = query.filter(fuselage_type=type_code)

    total_counts = query.values('fuselage_type').annotate(total=Count('id'))
    used_counts = UsedFuselage.objects.filter(
        fuselage__fuselage_type=type_code if type_code else query.values('fuselage_type')
    ).values('fuselage__fuselage_type').annotate(used=Count('id'))
    available_counts = query.exclude(
        id__in=UsedFuselage.objects.values_list('fuselage_id', flat=True)
    ).values('fuselage_type').annotate(available=Count('id'))

    availability_data = []

    total_dict = {item['fuselage_type']: item['total'] for item in total_counts}
    used_dict = {item['fuselage__fuselage_type']: item['used'] for item in used_counts}
    available_dict = {item['fuselage_type']: item['available'] for item in available_counts}

    for fuselage_type, total in total_dict.items():
        used = used_dict.get(fuselage_type, 0)
        available = available_dict.get(fuselage_type, total - used)
        availability_data.append({
            'part_type': fuselage_type,
            'total': total,
            'used': used,
            'available': available
        })

    serializer = PartAvailabilitySerializer(availability_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def tail_availability(request, type_code=None):
    """
    API endpoint to return total, used, and available counts of tails.
    Supports optional filtering by `type_code`.
    """
    query = Tail.objects.all()
    if type_code:
        query = query.filter(tail_type=type_code)

    # Total count (all tails of this type)
    total_counts = query.values('tail_type').annotate(total=Count('id'))

    # Used count (tails that are currently in use)
    used_counts = UsedTail.objects.filter(
        tail__tail_type=type_code if type_code else query.values('tail_type')
    ).values('tail__tail_type').annotate(used=Count('id'))

    # Available count (excluding used tails explicitly)
    available_counts = query.exclude(
        id__in=UsedTail.objects.values_list('tail_id', flat=True)
    ).values('tail_type').annotate(available=Count('id'))

    availability_data = []

    total_dict = {item['tail_type']: item['total'] for item in total_counts}
    used_dict = {item['tail__tail_type']: item['used'] for item in used_counts}
    available_dict = {item['tail_type']: item['available'] for item in available_counts}

    for tail_type, total in total_dict.items():
        used = used_dict.get(tail_type, 0)
        available = available_dict.get(tail_type, total - used)
        availability_data.append({
            'part_type': tail_type,
            'total': total,
            'used': used,
            'available': available
        })

    serializer = PartAvailabilitySerializer(availability_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def avionics_availability(request, type_code=None):
    """
    API endpoint to return total, used, and available counts of avionics.
    Supports optional filtering by `type_code`.
    """
    query = Avionics.objects.all()
    if type_code:
        query = query.filter(avionics_type=type_code)

    # Total count (all avionics of this type)
    total_counts = query.values('avionics_type').annotate(total=Count('id'))

    # Used count (avionics that are currently in use)
    used_counts = UsedAvionics.objects.filter(
        avionics__avionics_type=type_code if type_code else query.values('avionics_type')
    ).values('avionics__avionics_type').annotate(used=Count('id'))

    # Available count (excluding used avionics explicitly)
    available_counts = query.exclude(
        id__in=UsedAvionics.objects.values_list('avionics_id', flat=True)
    ).values('avionics_type').annotate(available=Count('id'))

    availability_data = []

    total_dict = {item['avionics_type']: item['total'] for item in total_counts}
    used_dict = {item['avionics__avionics_type']: item['used'] for item in used_counts}
    available_dict = {item['avionics_type']: item['available'] for item in available_counts}

    for avionics_type, total in total_dict.items():
        used = used_dict.get(avionics_type, 0)
        available = available_dict.get(avionics_type, total - used)
        availability_data.append({
            'part_type': avionics_type,
            'total': total,
            'used': used,
            'available': available
        })

    serializer = PartAvailabilitySerializer(availability_data, many=True)
    return Response(serializer.data)
