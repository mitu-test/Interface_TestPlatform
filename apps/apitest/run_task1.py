import sys
sys.path.append('C:\\Users\\guo\\Envs\\autotestplat\\Lib\\site-packages')
sys.path.append('E:\\Interface_TestPlatform')
from Interface_TestPlatform import settings
from ddt import ddt, data, file_data, unpack
import json
import unittest
import requests
import xmlrunner

BASE_PATH = settings.BASE_DIR.replace("\\", "/")
EXTEND_DIR = BASE_PATH + "/apps/apitest/"


@ddt
class InterfaceTest(unittest.TestCase):
    @unpack
    @file_data("test_data_list.json")
    def test_run_cases(self, url, method, header, param_type, param_body, assert_type, assert_body):

        if header == "{}":
            header_dict = {}
        else:
            header_dict = json.loads(header.replace("\'", "\""))

        if param_body == "{}":
            parameter_dict = {}
        else:
            parameter_dict = json.loads(param_body.replace("\'", "\""))

        if method == "get":
            if param_type == "from":
                r = requests.get(url, headers=header_dict, params=parameter_dict)
                if assert_type == "contains":
                    self.assertIn(assert_body, r.text)
                else:
                    self.assertEqual(assert_body, r.text)

        if method == "post":
            if param_type == "from":
                r = requests.post(url, headers=header_dict, data=parameter_dict)
                if assert_type == "contains":
                    self.assertIn(assert_body, r.text)
                else:
                    self.assertEqual(assert_body, r.text)

            elif assert_type == "json":
                r = requests.post(url, headers=header_dict, json=parameter_dict)
                if assert_type == "contains":
                    self.assertIn(assert_body, r.text)
                else:
                    self.assertEqual(assert_body, r.text)
            else:
                raise NameError("参数类型错误")


# 运行测试用例
def run_cases():
    with open(EXTEND_DIR + 'results.xml', 'w') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False
        )


if __name__ == '__main__':
    run_cases()
