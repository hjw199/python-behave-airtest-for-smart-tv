1.Python 版本3.7(不可使用3.8),否则安装airtest时会有问题

2.adb版本使用1.0.41以上版本，否则swipe会有延时

3.使用run.bat运行脚本，目录为程序所在目录

4.使用allure serve reports_path查看报告，需安装allure并加入环境变量，也可集成入Jenkins/gitlab直接查看

5.config路径config/config.ini，配置大屏IP/摄像头IP/存储路径等

6.behave执行过程：(其中before/after为environment.py中函数)
before_all
for feature in all_features:
    before_feature
    for outline in feature.scenarios:
        for scenario in outline.scenarios:
            before_scenario
            for step in scenario.steps:
                before_step
                    step.run()
                after_step
            after_scenario
    after_feature
after_all

7.
