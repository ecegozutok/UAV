from django.core.exceptions import PermissionDenied

def check_wing_permissions(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.has_perm('main.view_create_wing_page'):
            raise PermissionDenied("You do not have permission to view this page.")
        if request.method == 'POST' and not request.user.has_perm('main.create_wing'):
            raise PermissionDenied("You do not have permission to create a wing.")
        return view_func(request, *args, **kwargs)
    return wrapper

def check_fuselage_permissions(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.has_perm('main.view_create_fuselage_page'):
            raise PermissionDenied("You do not have permission to view this page.")
        if request.method == 'POST' and not request.user.has_perm('main.create_fuselage'):
            raise PermissionDenied("You do not have permission to create a fuselage.")
        return view_func(request, *args, **kwargs)
    return wrapper

def check_tail_permissions(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.has_perm('main.view_create_tail_page'):
            raise PermissionDenied("You do not have permission to view this page.")
        if request.method == 'POST' and not request.user.has_perm('main.create_tail'):
            raise PermissionDenied("You do not have permission to create a tail.")
        return view_func(request, *args, **kwargs)
    return wrapper

def check_avionics_permissions(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.has_perm('main.view_create_avionics_page'):
            raise PermissionDenied("You do not have permission to view this page.")
        if request.method == 'POST' and not request.user.has_perm('main.create_avionics'):
            raise PermissionDenied("You do not have permission to create avionics.")
        return view_func(request, *args, **kwargs)
    return wrapper

def check_assembly_permissions(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.has_perm('main.view_create_aircraft_page'):
            raise PermissionDenied("You do not have permission to view this page.")
        if request.method == 'POST' and not request.user.has_perm('main.create_aircraft'):
            raise PermissionDenied("You do not have permission to create avionics.")
        return view_func(request, *args, **kwargs)
    return wrapper
