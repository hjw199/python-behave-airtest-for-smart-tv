@four_finger_down
Feature: 四指下滑进入小屏模式
    @four_finger_down_less-than-60%
    Scenario Outline:在桌面进行四指下滑，下滑距离小于60%
    Given 回到桌面
    When 四指下划缩小屏幕至<ratio1>
    Then <pic>成比例缩小至<ratio2>
    Examples:
    | ratio1 | pic | ratio2 |
    # | 0.9 | 云白板图标 | 0.9 |
    | 0.85 | 云白板图标 | 0.85 |
    # | 0.8 | 云白板图标 | 0.8 |
    # | 0.75 | 云白板图标 | 0.75 |
    # # | 0.7 | 云白板图标 | 0.7 |
    # | 0.65 | 云白板图标 | 0.65 |
    # | 0.6 | 云白板图标 | 0.6 |

    @four_finger_down_more-than-60%
    Scenario Outline:在桌面进行四指下滑，下滑距离大于60%
        Given 回到桌面
        When 四指下划缩小屏幕至<ratio1>
        Then <pic>成比例缩小至<ratio2>
        Examples:
        | ratio1 | pic | ratio2 |
        | 0.5 | 云白板图标 | 0.6 |

    @four_finger_down_click-black-recover
    Scenario Outline:点击周围黑色部分复原
        Given 回到桌面
        When 登录账号18659131313
        When 四指下划缩小屏幕至<ratio1>
        Then <pic>成比例缩小至<ratio2>
        #云白板坐标,测试不透传
        When 点击坐标
        | x | y |
        | 1000 | 380 |
        Then 应该看到图片云白板图标
        Then 不应该看到图片宝可梦图片
        Examples:
        | ratio1 | pic | ratio2 |
        | 0.5 | 云白板图标 | 0.6 |

    @four_finger_down_cloud_whiteboard
    Scenario Outline:测试四指下划不透传
        Given 未登录账号
        When 点击按钮账号登录
        And 在账号输入<账号>
        And 在密码输入<密码>
        And 勾选允许快捷登录
        And 点击按钮登录
        And 打开软件云白板
        And 新建白板
        And 关闭提笔即写模式
        And 点击按钮画笔
        And 四指下划缩小屏幕至0.5
        Then 应该看到图片干净的白板
        Examples:
        | 账号 | 密码 |
        | 18659132313 | 123456 |

    @four_finger_down_no_login_openapp
    Scenario Outline:未登录账号打开应用进行四指下滑
        Given 未登录账号
        When 打开软件<app>
        When 四指下划缩小屏幕至<ratio1>
        When 等待0.5秒
        Then 存在取消按钮
        Then <pic>成比例缩小至<ratio2>
        Examples:
        | app |ratio1 | pic | ratio2 |
        | "云白板" | 0.5 | 账号登录图标 | 0.6 |
        # | "云资料夹" | 0.5 | 账号登录图标 | 0.6 |

    @four_finger_down_login_openapp
    Scenario Outline:已登录账号打开应用进行四指下滑
        Given 登录账号18659131313
        When 打开软件<app>
        When 四指下划缩小屏幕至<ratio1>
        When 等待0.5秒
        Then <pic>成比例缩小至<ratio2>
        Examples:
        | app | ratio1 | pic | ratio2 |
        | 云白板 | 0.5 | 宝可梦图片 | 0.6 |
        | 云资料夹 | 0.5 | ppt图片 | 0.6 |
