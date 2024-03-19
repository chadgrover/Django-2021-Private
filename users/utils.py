from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Profile, Skill

# Used to search for profiles in the search bar

def search_profiles(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(bio__icontains=search_query) |
        Q(skill__in=skills)
    )

    return profiles, search_query

def paginate_profiles(request, queryset, result=6):
    selected_page = request.GET.get("page")
    results_per_page = result
    p = Paginator(queryset, results_per_page)

    try:
        projects_list = p.page(selected_page)
    except PageNotAnInteger:
        selected_page = 1
        projects_list = p.page(selected_page)
    except EmptyPage:
        # If there is no page, return the last page in the paginator
        selected_page = p.num_pages
        projects_list = p.page(selected_page)

    left_bound = int(selected_page) - 1

    if left_bound < 1:
        left_bound = 1

    right_bound = int(selected_page) + 2

    if right_bound > p.num_pages:
        right_bound = p.num_pages + 1

    custom_range = range(left_bound, right_bound)

    return custom_range, projects_list