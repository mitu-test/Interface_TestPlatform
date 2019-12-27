from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from projects.models import Projects, Modules
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
@login_required(login_url='/users/login')
def project_list(request):
    """
    项目列表
    """
    nums_list = [5, 10, 15, 20]
    project_all = Projects.objects.all()
    counts = project_all.count()
    nums = request.GET.get('nums',None)
    if nums:
        page_num = int(nums)
    else:
        page_num = 5
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(project_all, page_num, request=request)
    start = (int(page) - 1) * page_num + 1
    end = int(page) * page_num
    if end >= counts:
        end = counts
    pro_list = p.page(page)
    return render(request, "projects/project_list.html", {"projects": project_all, "pro_list": pro_list,
                                                          "nums_list": nums_list, "counts": counts,
                                                          "start": start,"end": end,"page_num":page_num})


@login_required(login_url='/users/login')
def project_search(request):
    """
    项目搜索
    """
    keyword = request.GET.get('input1-group2', None)
    project_all = Projects.objects.filter(Q(name__icontains=keyword)
                                          | Q(describe__icontains=keyword)).order_by("-create_time")
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(project_all, 5, request=request)
    pro_list = p.page(page)
    return render(request, "projects/project_list.html", {"projects": project_all, "pro_list": pro_list})


@login_required(login_url='/users/login')
def project_add(request):
    """
    项目添加
    """
    project_name = request.POST["project_name"]
    project_describe = request.POST["project_describe"]
    if request.POST["project_status"] == "开启":
        project_status = True
    else:
        project_status = False
    try:
        project = Projects(name=project_name, describe=project_describe, status=project_status)
        project.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')
    except:
        return HttpResponse('{"status":"fail"}', content_type='application/json')


@login_required(login_url='/users/login')
def project_edit(request):
    """
    项目编辑
    """
    project_id = request.POST["project_id"]
    project_name = request.POST["project_name"]
    project_describe = request.POST["project_describe"]
    if request.POST["project_status"] == "开启":
        project_status = True
    else:
        project_status = False
    try:
        project = Projects.objects.get(id=project_id)
        project.name = project_name
        project.describe = project_describe
        project.status = project_status
        project.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')
    except:
        return HttpResponse('{"status":"fail"}', content_type='application/json')


@login_required(login_url='/users/login')
def project_delete(request):
    """
    项目删除
    """
    project_name = request.POST["project_name"]
    project = Projects.objects.get(name=project_name)
    project.delete()
    return HttpResponse('{"status":"success"}', content_type='application/json')


@login_required(login_url='/users/login')
def project_batch_delete(request):
    """
    项目批量删除
    """
    if request.method == "POST":
        ids = request.POST.getlist('ids')
        for i in ids:
            project = Projects.objects.get(id=i)
            project.delete()
    return HttpResponse('{"status":"success"}', content_type='application/json')


@login_required(login_url='/users/login')
def module_list(request):
    """
    模块列表
    """
    projects_list = []
    nums_list = [5, 10, 15, 20]
    project_all = Projects.objects.all()
    for project in project_all:
        projects_list.append(project.name)

    module_all = Modules.objects.all()
    counts = module_all.count()
    nums = request.GET.get('nums', None)
    if nums:
        page_num = int(nums)
    else:
        page_num = 5

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(module_all, page_num, request=request)
    start = (int(page) - 1)*page_num + 1
    end = int(page)*page_num
    if end >= counts:
        end = counts
    mod_list = p.page(page)
    return render(request, "projects/module_list.html", {"modules": module_all,
                                                         "mod_list": mod_list,
                                                         "projects_list": projects_list,
                                                         "counts": counts,"nums_list":nums_list,
                                                         "start": start, "end": end, "page_num":page_num})


@login_required(login_url='/users/login')
def module_search(request):
    """
    模块搜索
    """
    keyword = request.GET.get('input1', None)
    module_all = Modules.objects.filter(Q(name__icontains=keyword)
                                        | Q(tester__contains=keyword)).order_by("-create_time")
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(module_all, 3, request=request)
    mod_list = p.page(page)
    return render(request, "projects/module_list.html", {"modules": module_all, "mod_list": mod_list})


@login_required(login_url='/users/login')
def module_add(request):
    """
    模块添加
    """
    module_name = request.POST["module_name"]
    module_describe = request.POST["module_describe"]
    module_project = request.POST["module_project"]
    module_tester = request.POST["module_tester"]
    try:
        project = Projects.objects.get(name=module_project)
        module = Modules(name=module_name, describe=module_describe, project_id=project.id,
                         tester=module_tester)
        module.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')
    except:
        return HttpResponse('{"status":"fail"}', content_type='application/json')


@login_required(login_url='/users/login')
def module_edit(request):
    """
    模块编辑
    """
    module_id = request.POST["module_id"]
    module_name = request.POST["module_name"]
    module_describe = request.POST["module_describe"]
    module_project = request.POST["module_project"]
    module_tester = request.POST["module_tester"]
    try:
        module = Modules.objects.get(id=module_id)
        project = Projects.objects.get(name=module_project)
        module.name = module_name
        module.describe = module_describe
        module.project_id = project.id
        module.tester = module_tester
        module.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')
    except:
        return HttpResponse('{"status":"fail"}', content_type='application/json')


@login_required(login_url='/users/login')
def module_delete(request):
    """
    模块删除
    """
    module_name = request.POST["module_name"]
    module = Modules.objects.get(name=module_name)
    module.delete()
    return HttpResponse('{"status":"success"}', content_type='application/json')


@login_required(login_url='/users/login')
def module_batch_delete(request):
    """
    模块批量删除
    """
    if request.method == "POST":
        ids = request.POST.getlist('ids')
        for i in ids:
            module = Modules.objects.get(id=i)
            module.delete()
    return HttpResponse('{"status":"success"}', content_type='application/json')
