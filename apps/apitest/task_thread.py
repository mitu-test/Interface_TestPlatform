import os
import json
import threading
from time import sleep
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Interface_TestPlatform.settings")

django.setup()
from apitest.models import InterfaceCase
from apitest.models import TestTask
from apitest.models import TestResult
from Interface_TestPlatform import settings
from xml.dom.minidom import parse

BASE_PATH = settings.BASE_DIR.replace("\\", "/")
EXTEND_DIR = BASE_PATH + "/apps/apitest/"


class CaseThread:

    def __init__(self, case_id):
        self.tid = case_id

    def run_cases(self):
        # 2. 将用例数据写到 json文件
        test_data = {}
        case = InterfaceCase.objects.get(id=int(self.tid))
        if case.method == "0":
            method = "GET"
        elif case.method == "1":
            method = "POST"
        elif case.method == "2":
            method = "PUT"
        else:
            method = "DELETE"
        if case.param_type == "0":
            param_type = "form-data"
        elif case.param_type == "1":
            param_type = "json"
        else:
            param_type = "param"
        if case.assert_type == "0":
            assert_type = "包含"
        else:
            assert_type = "匹配"
        test_data[case.name] = {
            "url": case.api,
            "method": method,
            "header": case.header,
            'param_type': param_type,
            'param_body': case.param_body,
            'assert_type': assert_type,
            'assert_body': case.assert_body,
        }
        case_data = json.dumps(test_data)
        with (open(EXTEND_DIR + "test_data_list.json", "w")) as f:
            f.write(case_data)

        # 3.执行运行测试用例的文件， 它会生成 result.xml 文件
        run_cmd = "python " + EXTEND_DIR + "run_task.py"
        print("运行的命令", run_cmd)
        os.system(run_cmd)


        # 4. 读取result.xml文件，把这里面的结果放到表里面。
        # self.save_result()
        # 5. 修改任务的状态，执行完成


    # def save_result(self):
    #     # 打开xml文档
    #     dom = parse(EXTEND_DIR + 'results.xml')
    #     # 得到文档元素对象
    #     root = dom.documentElement
    #     # 获取(一组)标签
    #     testsuite = root.getElementsByTagName('testsuite')
    #     errors = testsuite[0].getAttribute("errors")
    #     failures = testsuite[0].getAttribute("failures")
    #     name = testsuite[0].getAttribute("name")
    #     skipped = testsuite[0].getAttribute("skipped")
    #     tests = testsuite[0].getAttribute("tests")
    #     run_time = testsuite[0].getAttribute("time")
    #
    #     print("类型----》", errors, type(errors))
    #     f = open(EXTEND_DIR + "results.xml", "r", encoding="utf-8")
    #     result = f.read()
    #     f.close()
    #
    #     TestResult.objects.create(
    #         task_id=self.tid,
    #         name=name,
    #         error=int(errors),
    #         failure=int(failures),
    #         skipped=int(skipped),
    #         tests=int(tests),
    #         run_time=float(run_time),
    #         result=result
    #     )

    def run_tasks(self):
        print("创建线程任务...")
        sleep(2)
        threads = []
        t1 = threading.Thread(target=self.run_cases)
        threads.append(t1)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def run(self):
        threads = []
        t = threading.Thread(target=self.run_tasks)
        threads.append(t)

        for t in threads:
            t.start()


class TaskThread:

    def __init__(self, task_id):
        self.tid = task_id

    def run_cases(self):
        task = TestTask.objects.get(id=self.tid)
        # 1. 拿到任务对应用例的列表
        case_ids = json.loads(task.cases)
        # 2. 将用例数据写到 json文件
        test_data = {}
        for cid in case_ids:
            case = InterfaceCase.objects.get(id=int(cid))
            if case.method == "0":
                method = "GET"
            elif case.method == "1":
                method = "POST"
            elif case.method == "2":
                method = "PUT"
            else:
                method = "DELETE"
            if case.param_type == "0":
                param_type = "form-data"
            elif case.param_type == "1":
                param_type = "json"
            else:
                param_type = "param"
            if case.assert_type == "0":
                assert_type = "包含"
            else:
                assert_type = "匹配"
            test_data[case.name] = {
                "url": case.api,
                "method": method,
                "header": case.header,
                'param_type': param_type,
                'param_body': case.param_body,
                'assert_type': assert_type,
                'assert_body': case.assert_body,
            }


        case_data = json.dumps(test_data)
        with (open(EXTEND_DIR + "test_data_list2.json", "w")) as f:
            f.write(case_data)

        # 3.执行运行测试用例的文件， 它会生成 result.xml 文件
        run_cmd = "python " + EXTEND_DIR + "run_task2.py"
        print("运行的命令", run_cmd)
        os.system(run_cmd)
        sleep(2)

        # 4. 读取result.xml文件，把这里面的结果放到表里面。
        # self.save_result()
        # 5. 修改任务的状态，执行完成
        task = TestTask.objects.get(id=self.tid)
        task.status = 2
        task.save()

    # def save_result(self):
    #     # 打开xml文档
    #     dom = parse(EXTEND_DIR + 'results.xml')
    #     # 得到文档元素对象
    #     root = dom.documentElement
    #     # 获取(一组)标签
    #     testsuite = root.getElementsByTagName('testsuite')
    #     errors = testsuite[0].getAttribute("errors")
    #     failures = testsuite[0].getAttribute("failures")
    #     name = testsuite[0].getAttribute("name")
    #     skipped = testsuite[0].getAttribute("skipped")
    #     tests = testsuite[0].getAttribute("tests")
    #     run_time = testsuite[0].getAttribute("time")
    #
    #     print("类型----》", errors, type(errors))
    #     f = open(EXTEND_DIR + "results.xml", "r", encoding="utf-8")
    #     result = f.read()
    #     f.close()
    #
    #     TestResult.objects.create(
    #         task_id=self.tid,
    #         name=name,
    #         error=int(errors),
    #         failure=int(failures),
    #         skipped=int(skipped),
    #         tests=int(tests),
    #         run_time=float(run_time),
    #         result=result
    #     )

    def run_tasks(self):
        print("创建线程任务...")
        sleep(2)
        threads = []
        t1 = threading.Thread(target=self.run_cases)
        threads.append(t1)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def run(self):
        threads = []
        t = threading.Thread(target=self.run_tasks)
        threads.append(t)

        for t in threads:
            t.start()
