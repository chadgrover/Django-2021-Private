from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag


def search_projects(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query)
        | Q(description__icontains=search_query)
        | Q(owner__name__icontains=search_query)
        | Q(tags__in=tags)
    )

    return projects, search_query


def paginate_projects(request, queryset, result=3):
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