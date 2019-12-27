import sys

sys.path.append('C:\\Users\\guo\\Envs\\autotestplat\\Lib\\site-packages')
sys.path.append('E:\\Interface_TestPlatform')
sys.path.append('C:\\Users\\guo\\Envs\\autotestplat\\Lib')
from Interface_TestPlatform import settings
from ddt import ddt, data, file_data, unpack
import json
import unittest
import requests
from ExtentHTMLTestRunner import HTMLTestRunner
import time

BASE_PATH = settings.BASE_DIR.replace("\\", "/")
EXTEND_DIR = BASE_PATH + "/apps/apitest/"


@ddt
class InterfaceTest(unittest.TestCase):
    @unpack
    @file_data(EXTEND_DIR + "test_data_list.json")
    def test_run_cases(self, url, method, header, param_type, param_body, assert_type, assert_body):
        if header == '{}':
            header_dict = {}
        else:
            header_dict = json.loads(header.replace("\'", "\""))

        if param_body == '{}':
            parameter_dict = {}
        else:
            parameter_dict = json.loads(param_body.replace("\'", "\""))

        if method == 'GET':
            if param_type == 'param':
                r = requests.get(url, headers=header_dict, params=parameter_dict)
                if assert_type == '包含':
                    self.assertIn(assert_body, r.text)
                else:
                    self.assertEqual(assert_body, r.text)

        if method == 'POST':
            if param_type == 'form-data':
                r = requests.post(url, headers=header_dict, data=parameter_dict)
                if assert_type == '包含':
                    self.assertIn(assert_body, r.text)
                else:
                    self.assertEqual(assert_body, r.text)
            elif param_type == 'json':

                r = requests.post(url, headers=header_dict, json=parameter_dict)

                if assert_type == '包含':
                    self.assertEqual(assert_body, r.json()['name'])

                else:
                    assert_body = json.loads(assert_body.replace("\'", "\""))
                    for key in assert_body:
                        self.assertEqual(assert_body[key], r.json()[key])

            else:
                raise NameError("参数类型错误")


# 运行测试用例
# def run_cases(): A
#     with open(EXTEND_DIR + 'results.xml', 'w') as output:
#         unittest.main(
#             testRunner=xmlrunner.XMLTestRunner(output=output),
#             failfast=False, buffer=False, catchbreak=False
#         )


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InterfaceTest))
    filePath = r'E:\Interface_TestPlatform\apps\apitest\templates\apitest\report.html'
    fp = open(filePath, 'wb')
    runner = HTMLTestRunner(
        stream=fp,
        title='',
        # description='详细测试用例结果',
    )
    runner.run(suite)  # 执行测试用例
    fp.close()

