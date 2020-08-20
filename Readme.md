1.Python 版本3.7(不可使用3.8),否则安装airtest时会有问题

2.使用run.bat运行脚本，目录为程序所在目录

3.config路径features/config/config.ini，配置大屏IP/摄像头IP/存储路径等

4.behave执行过程：(其中before/after为environment.py中函数)
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

5.
