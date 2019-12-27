from django.shortcuts import render
from apitest.models import InterfaceCase, TestTask, TestResult
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from projects.models import Projects, Modules
import json
from Interface_TestPlatform import settings
from apitest.task_thread import TaskThread, CaseThread

BASE_PATH = settings.BASE_DIR.replace("\\", "/")
EXTEND_DIR = BASE_PATH + "/apps/apitest/"


# Create your views here.
@login_required(login_url='/users/login')
def case_list(request):
    """接口列表"""
    projects_list = []
    modules_list1 = []
    modules_all = Modules.objects.all()
    for module in modules_all:
        modules_list1.append(module.name)
    project_all = Projects.objects.all()
    for project in project_all:
        projects_list.append(project.name)
    modules_names1 = []
    if projects_list:
        project1 = Projects.objects.get(name=projects_list[0])
        project_module1 = project1.modules_set.all()
        for module1 in project_module1:
            modules_names1.append(module1.name)
    nums_list = [5, 10, 15, 20]
    case_all = InterfaceCase.objects.all()
    counts = case_all.count()
    nums = request.GET.get('nums', None)
    if nums:
        page_num = int(nums)
    else:
        page_num = 5
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(case_all, page_num, request=request)
    start = (int(page) - 1) * page_num + 1
    end = int(page) * page_num
    if end >= counts:
        end = counts
    case_list = p.page(page)
    return render(request, "apitest/case_list.html", {"cases": case_all, "case_list": case_list,
                                                      "projects_list": projects_list,
                                                      "module_list": modules_names1,
                                                      "module_list_all": modules_list1,
                                                      "nums_list": nums_list, "counts": counts,
                                                      "start": start, "end": end, "page_num": page_num
                                                      })


@login_required(login_url='/users/login')
def case_search(request):
    """
    接口搜索
    """
    keyword = request.GET.get('input2', None)
    case_all = InterfaceCase.objects.filter(Q(name__icontains=keyword)
                                            | Q(maker__icontains=keyword)).order_by("-create_time")
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(case_all, 10, request=request)
    case_list = p.page(page)
    return render(request, "apitest/case_list.html", {"cases": case_all, "case_list": case_list})


@login_required(login_url='/users/login')
def case_delete(request):
    """
    接口删除
    """
    case_name = request.POST["case_name"]
    case = InterfaceCase.objects.get(name=case_name)
    case.delete()
    return HttpResponse('{"status":"success"}', content_type='application/json')


@login_required(login_url='/users/login')
def case_batch_delete(request):
    """
    用例批量删除
    """
    if request.method == "POST":
        ids = request.POST.getlist('ids')
        for i in ids:
            case = InterfaceCase.objects.get(id=i)
            case.delete()
    return HttpResponse('{"status":"success"}', content_type='application/json')


def get_modules_name(request):
    """
    在接口添加或者编辑时，根据项目名查找项目下的所有模块
    """
    if request.method == "GET":
        project_name = request.GET.get("project_name")
        modules_names = []
        project = Projects.objects.get(name=project_name)
        project_module = project.modules_set.all()
        for module in project_module:
            modules_names.append(module.name)

        return JsonResponse({"status": 10200, "message": "success", "data": modules_names})

    else:
        return JsonResponse({"status": 10100, "message": "请求方法错误"})


def get_case_message(request):
    """
    在接口添加或者编辑时，根据项目名查找项目下的所有模块
    """
    if request.method == "GET":
        case_name = request.GET.get("case_name")
        case_message = []
        case = InterfaceCase.objects.get(name=case_name)
        if case.method == "0":
            case.method = "GET"
        elif case.method == "1":
            case.method = "POST"
        elif case.method == "2":
            case.method = "PUT"
        else:
            case.method = "DELETE"

        if case.param_type == "0":
            case.param_type = "form-data"
        elif case.param_type == "1":
            case.param_type = "json"
        else:
            case.param_type = "param"

        if case.assert_type == "0":
            case.assert_type = "包含"
        else:
            case.assert_type = "匹配"
        case_message.append(case.method)
        case_message.append(case.api)
        case_message.append(case.header)
        case_message.append(case.param_type)
        case_message.append(case.param_body)
        case_message.append(case.assert_type)
        case_message.append(case.assert_body)
        return JsonResponse({"status": 10200, "message": "success", "data": case_message})

    else:
        return JsonResponse({"status": 10100, "message": "请求方法错误"})


@login_required(login_url='/users/login')
def case_add(request):
    """
    接口添加
    """
    case_name = request.POST['case_name']
    case_describe = request.POST['case_describe']
    case_module = request.POST['case_module']
    case_api = request.POST['case_api']
    case_status = request.POST['case_status']
    case_method = request.POST['case_method']
    case_maker = request.POST['case_maker']
    case_header = request.POST['case_header']
    case_param_type = request.POST['case_param_type']
    case_param_body = request.POST['case_param_body']
    case_assert_type = request.POST['case_assert_type']
    case_assert_body = request.POST['case_assert_body']
    if case_status == "开启":
        case_status = True
    else:
        case_status = False

    if case_method == "GET":
        case_method = 0
    elif case_method == "POST":
        case_method = 1
    elif case_method == "PUT":
        case_method = 2
    else:
        case_method = 3

    if case_param_type == "form-data":
        case_param_type = 0
    elif case_param_type == "json":
        case_param_type = 1
    else:
        case_param_type = 2

    if case_assert_type == "包含":
        case_assert_type = 0
    else:
        case_assert_type = 1

    try:
        module = Modules.objects.get(name=case_module)
        module_id = module.id
        case = InterfaceCase(name=case_name, describe=case_describe, status=case_status,
                             api=case_api, module_id=module_id, method=case_method, maker=case_maker,
                             header=case_header, param_type=case_param_type, param_body=case_param_body,
                             assert_type=case_assert_type, assert_body=case_assert_body)
        case.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')
    except:
        return HttpResponse('{"status":"fail"}', content_type='application/json')


@login_required(login_url='/users/login')
def case_edit(request):
    """
    接口编辑
    """
    case_id = request.POST['case_id']
    case_name = request.POST['case_name']
    case_describe = request.POST['case_describe']
    case_module = request.POST['case_module']
    case_api = request.POST['case_api']
    case_status = request.POST['case_status']
    case_method = request.POST['case_method']
    case_maker = request.POST['case_maker']
    case_header = request.POST['case_header']
    case_param_type = request.POST['case_param_type']
    case_param_body = request.POST['case_param_body']
    case_assert_type = request.POST['case_assert_type']
    case_assert_body = request.POST['case_assert_body']
    if case_status == "开启":
        case_status = True
    else:
        case_status = False

    if case_method == "GET":
        case_method = 0
    elif case_method == "POST":
        case_method = 1
    elif case_method == "PUT":
        case_method = 2
    else:
        case_method = 3

    if case_param_type == "form-data":
        case_param_type = 0
    elif case_param_type == "json":
        case_param_type = 1
    else:
        case_param_type = 2

    if case_assert_type == "包含":
        case_assert_type = 0
    else:
        case_assert_type = 1
    try:
        case = InterfaceCase.objects.get(id=case_id)
        case.name = case_name
        module = Modules.objects.get(name=case_module)
        case.module_id = module.id
        case.describe = case_describe
        case.api = case_api
        case.status = case_status
        case.header = case_header
        case.method = case_method
        case.param_type = case_param_type
        case.param_body = case_param_body
        case.assert_type = case_assert_type
        case.assert_body = case_assert_body
        case.maker = case_maker
        case.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')
    except:
        return HttpResponse('{"status":"fail"}', content_type='application/json')


@login_required(login_url='/users/login')
def case_run(request):
    """ 运行单个测试用例 """
    if request.method == "POST":
        case_id = request.POST["case_id"]
        # 通过多线程运行测试任务
        CaseThread(case_id).run()

        return JsonResponse({"status": 10200, "message": "任务开始执行！", "case_id": case_id})

    else:
        return JsonResponse({"status": 10101, "message": "请求方法错误"})


@login_required(login_url='/users/login')
def task_list(request):
    """任务列表"""
    nums_list = [5, 10, 15, 20]
    task_all = TestTask.objects.all()
    counts = task_all.count()
    nums = request.GET.get('nums', None)
    if nums:
        page_num = int(nums)
    else:
        page_num = 5
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(task_all, page_num, request=request)
    start = (int(page) - 1) * page_num + 1
    end = int(page) * page_num
    if end >= counts:
        end = counts
    task_list = p.page(page)
    return render(request, "apitest/task_list.html", {"tasks": task_all, "task_list": task_list,
                                                      "nums_list": nums_list, "counts": counts,
                                                      "start": start, "end": end, "page_num": page_num
                                                      })


@login_required(login_url='/users/login')
def task_search(request):
    """
    接口搜索
    """
    keyword = request.GET.get('task', None)
    task_all = TestTask.objects.filter(Q(name__icontains=keyword)).order_by("-create_time")
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(task_all, 10, request=request)
    task_list = p.page(page)
    return render(request, "apitest/task_list.html", {"tasks": task_all, "task_list": task_list})


@login_required(login_url='/users/login')
def task_add(request):
    """任务添加"""

    task_name = request.POST['task_name']
    task_describe = request.POST['task_describe']
    task_case = request.POST['task_case']
    task_status = request.POST['task_status']
    if task_status == "未执行":
        task_status = "0"
    elif task_status == "未执行":
        task_status = "1"
    else:
        task_status = "2"
    try:
        task = TestTask(name=task_name, describe=task_describe, status=task_status,
                        cases=task_case)
        task.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')
    except:
        return HttpResponse('{"status":"fail"}', content_type='application/json')


@login_required(login_url='/users/login')
def task_edit(request):
    """
    任务编辑
    """
    task_id = request.POST['task_id']
    task_name = request.POST['task_name']
    task_describe = request.POST['task_describe']
    task_case = request.POST['task_case']
    task_status = request.POST['task_status']
    if task_status == "未执行":
        task_status = "0"
    elif task_status == "执行中":
        task_status = "1"
    else:
        task_status = "2"
    try:
        task = TestTask.objects.get(id=task_id)
        task.name = task_name
        task.status = task_status
        task.describe = task_describe
        task.cases = task_case
        task.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')
    except:
        return HttpResponse('{"status":"fail"}', content_type='application/json')


@login_required(login_url='/users/login')
def task_delete(request):
    """
    任务删除
    """
    task_name = request.POST["task_name"]
    task = TestTask.objects.get(name=task_name)
    task.delete()
    return HttpResponse('{"status":"success"}', content_type='application/json')


@login_required(login_url='/users/login')
def task_batch_delete(request):
    """
    任务批量删除
    """
    if request.method == "POST":
        ids = request.POST.getlist('ids')
        for i in ids:
            task = TestTask.objects.get(id=i)
            task.delete()
    return HttpResponse('{"status":"success"}', content_type='application/json')


@login_required(login_url='/users/login')
def get_case_tree(request):
    """
    获得用例树形结构
    """
    if request.method == "GET":
        projects = Projects.objects.all()
        data_list = []
        for project in projects:
            project_dict = {
                "name": project.name,
                "isParent": True
            }

            modules = Modules.objects.filter(project_id=project.id)
            module_list = []
            for module in modules:
                module_dict = {
                    "name": module.name,
                    "isParent": True
                }

                cases = InterfaceCase.objects.filter(module_id=module.id)
                case_list = []
                for case in cases:
                    case_dict = {
                        "name": case.name,
                        "isParent": False,
                        "id": case.id,
                    }
                    case_list.append(case_dict)

                module_dict["children"] = case_list
                module_list.append(module_dict)

            project_dict["children"] = module_list
            data_list.append(project_dict)

        return JsonResponse({"status": 10200, "message": "success", "data": data_list})

    if request.method == "POST":
        task_id = request.POST["task_id"]

        task = TestTask.objects.get(id=task_id)
        casesList = json.loads(task.cases)
        projects = Projects.objects.all()
        data_list = []
        for project in projects:
            project_dict = {
                "name": project.name,
                "isParent": True
            }

            modules = Modules.objects.filter(project_id=project.id)
            module_list = []
            for module in modules:
                module_dict = {
                    "name": module.name,
                    "isParent": True
                }
                cases = InterfaceCase.objects.filter(module_id=module.id)
                case_list = []
                for case in cases:
                    if case.id in casesList:
                        case_dict = {
                            "name": case.name,
                            "isParent": False,
                            "id": case.id,
                            "checked": True,
                        }
                    else:
                        case_dict = {
                            "name": case.name,
                            "isParent": False,
                            "id": case.id,
                            "checked": False,
                        }
                    case_list.append(case_dict)

                module_dict["children"] = case_list
                module_list.append(module_dict)

            project_dict["children"] = module_list
            data_list.append(project_dict)
        return JsonResponse({"status": 10200, "message": "success", "data": data_list})


@login_required(login_url='/users/login')
def task_run(request):
    """ 运行任务 """
    if request.method == "POST":
        task_id = request.POST["task_id"]
        # 1、在执行线程之前，判断当前有没有任务在执行？
        tasks = TestTask.objects.all()
        for t in tasks:
            if t.status == 1:
                return JsonResponse({"status": 10200, "message": "当前有任务正在执行！"})

        # 2. 修改任务的状态为：1-执行中
        task = TestTask.objects.get(id=task_id)
        task.status = 1
        task.save()
        # 通过多线程运行测试任务
        TaskThread(task_id).run()

        return JsonResponse({"status": 10200, "message": "任务开始执行！"})

    else:
        return JsonResponse({"status": 10101, "message": "请求方法错误"})


@login_required(login_url='/users/login')
def show_case_report(request, case_id):
    """
    显示html报告
    """
    case = InterfaceCase.objects.get(id=case_id)

    return render(request, 'apitest/report.html', {"case": case})


@login_required(login_url='/users/login')
def show_task_report(request, task_id):
    """
    显示html报告
    """
    task = TestTask.objects.get(id=task_id)

    return render(request, 'apitest/report1.html', {"task": task})
