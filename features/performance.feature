@Performance
Feature: 性能测试

    @Monkey_test
    Scenario Outline:Monkey测试
        Given 未运行应用
        When 登录账号18659132313
        Then 对<app>进行mokey测试
        Examples:
        | app |
        | 云白板 |
        | 云资料夹 |
        | 桌面程序 |
    
    @start_time
    Scenario Outline: 启动时间
        Given 未运行应用
        When 登录账号18659132313
        And 等待0.5秒
        #冷启动
        Then 对<app>进行启动时间测试
        When 回到桌面
        #热启动
        Then 对<app>进行启动时间测试
        Examples:
        | app |
        | 云白板ac |
        | 云资料夹ac |
        | 桌面程序 |
    
    @UI_Performance
    Scenario Outline: UI性能
        #目前测试验证条件不确定，用丢帧率确定
        When 登录账号18659132313
        Then 对<app>进行UI性能测试
        Examples:
        | app |
        | 云白板 |
        | 云资料夹 |
        | 桌面程序 |
    
    @lose_package
    Scenario: 丢包率
        Then 连续ping丢包率为0
    
    @reboot
    Scenario: 开关机时间
        Given 登录账号18659132313
        When 打开软件云白板
        And 打开软件云资料夹
        And 打开软件浏览器
        When 重启大屏
        Then 重启大屏，关机时间不超过30秒，开机时间不超过90秒
        When 等待60秒

    # @sys_idle
    # Scenario: 系统空转占用资源情况
    #     Given 登录账号18659132313
    #     When 点击 下课
    #     And 重启并等待大屏重启成功
    #     Then CPU占用不超过0.2,内存占用不超过0.2