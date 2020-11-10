@buttomup
Feature: 底部上划

    @buttomup_normal_toolbar-normal
    Scenario:常用工具栏
        When 回到桌面
        When 底部上划唤出常用应用
        Then 应该看到图片常用应用栏

    @buttomup_normal_toolbar-1/3
    Scenario:底部上划小于常用应用栏三分之一
        When 回到桌面
        When 底部上划小于应用栏三分之一
        #   When 截图保存
        #   When 松开手指
        #   Then 截图与"小于三分之一常用应用栏"一致
        Then 不应该看到图片常用应用栏

    @buttomup_normal_toolbar-inapp001
    Scenario Outline:应用内唤出常用工具栏2
        Given 未登录账号
        # Given 等待3秒
        Given 打开软件<应用>
        When 等待1秒
        When 底部上划唤出常用应用
        Then 应该看到图片常用应用栏
        Examples:
        | 应用 |
        | 云资料夹 |
        | 云白板 |

    @buttomup_normal_toolbar-inapp002
    Scenario Outline:应用内唤出常用工具栏1
        Given 已登录账号
        # Given 等待3秒
        Given 打开软件<应用>
        When 底部上划唤出常用应用
        Then 应该看到图片常用应用栏
        Examples:
        | 应用 |
        | 云资料夹 |
        | 云白板 |

    @buttomup_normal_toolbar-inapp_1/3-002
    Scenario Outline:应用内底部上划小于常用应用栏三分之一2
        Given 未登录账号
        # Given 等待5秒
        Given 打开软件<应用>
        When 底部上划小于应用栏三分之一
        # When 截图保存
        # When 松开手指
        # Then 截图与"小于三分之一常用应用栏"一致
        Then 不应该看到图片常用应用栏
        Examples:
        | 应用 |
        | 云资料夹 |
        | 云白板 |

    @buttomup_normal_toolbar-inapp_1/3-001
    Scenario Outline:应用内底部上划小于常用应用栏三分之一1
        Given 已登录账号
        # Given 等待3秒
        Given 打开软件<应用>
        When 等待1秒
        When 底部上划小于应用栏三分之一
        # When 截图保存
        # When 松开手指
        # Then 截图与"小于三分之一常用应用栏"一致
        Then 不应该看到图片常用应用栏
        Examples:
        | 应用 |
        | 云资料夹 |
        | 云白板 |

    @buttomup_normal_toolbar-login-click
    Scenario Outline:已登录点击常用工具栏应用
        Given 登录账号18659131313
        When 底部上划唤出常用应用
        When 点击图片<图标>
        Then 应该看到图片<验证图片>
        Examples:
        | 图标 | 验证图片 |
        | 常用应用云资料夹图标 | ppt图片 |
        | 常用应用云白板图标 | 宝可梦图片 |

    @buttomup_normal_toolbar-nologin-click
    Scenario Outline:未登录点击常用工具栏应用
        Given 未登录账号
        # Given 等待3秒
        When 底部上划唤出常用应用
        When 点击图片<图标>
        When 等待1秒
        When 点击按钮账号登录
        When 在账号输入<账号>
        When 在密码输入<密码>
        When 点击按钮登录
        Then 应该看到图片<验证图片>
        Examples:
        | 图标 | 账号 | 密码 | 验证图片 |
        | 常用应用云资料夹图标 | 18659131313  | 123456 | ppt图片 |
        |  常用应用云白板图标  | 18659131313  | 123456 | 宝可梦图片 |

    @buttomup_normal_toolbar-click-outside
    Scenario Outline:点击常用工具栏外围
        Given 登录账号18659131313
        Given 打开软件<应用>
        When 底部上划唤出常用应用
        Then 应该看到图片常用应用栏
        When 点击常用应用栏外围
        When 等待0.5秒
        Then 不应该看到图片常用应用栏
        Then 应该看到图片<验证图片>
        Examples:
        | 应用 | 验证图片 |
        | 云资料夹 | ppt图片 |
        | 云白板 | 宝可梦图片 |

    @buttomup_running_app-norunning-app
    Scenario:未运行应用唤出运行应用列表
        Given 未运行应用
        When 底部上划唤出运行应用
        Then 不应该看到图片正在运行应用

    @buttomup_running_app-running-app-002
    Scenario Outline:运行应用唤出正在运行应用2
        Given 登录账号18659131313
        Given 未运行应用
        # When 回到桌面
        When 打开软件<应用>
        When 回到桌面
        When 底部上划唤出运行应用
        Then 应该看到图片<验证图片1>
        Then 应该看到图片<验证图片2>
        Examples:
        | 应用 | 验证图片1 | 验证图片2 |
        | 云资料夹 | 正在运行云资料夹图标 | 正在运行云资料夹缩略图2 |
        | 云白板 | 正在运行云白板图标 | 正在运行云白板缩略图2 |

    @buttomup_running_app-running-app-001
    Scenario Outline:运行应用唤出正在运行应用1
        Given 未登录账号
        Given 未运行应用
        # When 回到桌面
        When 打开软件<应用>
        When 回到桌面
        When 底部上划唤出运行应用
        Then 应该看到图片<验证图片1>
        Then 应该看到图片<验证图片2>
        Examples:
        | 应用 | 验证图片1 | 验证图片2 |
        | 云资料夹 | 正在运行云资料夹图标 | 正在运行云资料夹缩略图1 |
        | 云白板 | 正在运行云白板图标 | 正在运行云白板缩略图1 |

    @buttomup_running_app-running-app-click-001
    Scenario Outline:点击打开正在运行应用1
        Given 登录账号18659131313
        Given 未运行应用
        When 打开软件<应用>
        When 回到桌面
        When 底部上划唤出运行应用
        When 点击图片<正在运行应用>
        Then 应该看到图片<验证图片>
        Examples:
        | 应用 | 正在运行应用 | 验证图片 |
        | 云资料夹 | 正在运行云资料夹图标 | ppt图片 |
        | 云白板 | 正在运行云白板图标 | 宝可梦图片 |

    @buttomup_running_app-running-app-click-002
    Scenario Outline:点击打开正在运行应用2
        Given 未登录账号
        Given 未运行应用
        When 打开软件<应用>
        When 回到桌面
        When 底部上划唤出运行应用
        When 点击图片<正在运行应用>
        When 等待1秒
        Then 存在账号登录
        Examples:
        | 应用 | 正在运行应用 |
        | 云资料夹 | 正在运行云资料夹图标 |

    @buttomup_running_app-running-app-close
    Scenario Outline:点击关闭正在运行应用
        Given 已登录账号
        Given 未运行应用
        When 打开软件<应用>
        When 回到桌面
        When 未运行应用
        Then 不应该看到图片正在运行应用
        Examples:
        | 应用 |
        | 云资料夹 |
        | 云白板 |

    @buttomup_running_app-running-app-outside-001
    Scenario Outline:点击正在运行应用外围1
        Given 登录账号18659131313
        Given 未运行应用
        Given 打开软件<应用>
        When 底部上划唤出运行应用
        Then 应该看到图片<验证图片>
        When 点击运行应用外围
        When 等待0.5秒
        Then 不应该看到图片<验证图片>
        Then 应该看到图片<app图片>
        Examples:
        | 应用 | 验证图片 | app图片 |
        | 云资料夹 | 正在运行云资料夹图标 | ppt图片 |
        | 云白板 |  正在运行云白板图标 | 宝可梦图片 |

    @buttomup_running_app-running-app-outside-002
    Scenario Outline:点击正在运行应用外围2
        Given 登录账号18659131313
        Given 未运行应用
        When 打开软件<应用1>
        And 回到桌面
        When 打开软件<应用2>
        When 底部上划唤出运行应用
        Then 应该看到图片<验证图片1>
        Then 应该看到图片<验证图片2>
        When 点击运行应用之间
        When 等待0.5秒
        Then 不应该看到图片<验证图片1>
        Then 应该看到图片<app图片>
        Examples:
        | 应用1 | 应用2 | 验证图片1 | 验证图片2 | app图片 |
        | 云资料夹 | 云白板 | 正在运行云资料夹图标 | 正在运行云白板图标 | 宝可梦图片 |

    @buttomup_running_app-running-app-outside-003
    Scenario Outline:点击正在运行应用外围3
        Given 登录账号18659131313
        Given 未运行应用
        When 打开软件<应用1>
        And 回到桌面
        When 打开软件<应用2>
        And 回到桌面
        When 打开软件<应用3>
        And 回到桌面
        When 打开软件<应用4>
        When 底部上划唤出运行应用
        Then 应该看到图片<验证图片1>
        Then 应该看到图片<验证图片2>
        Then 应该看到图片<验证图片3>
        Then 应该看到图片<验证图片4>
        When 点击运行应用空白区域
        When 等待0.5秒
        Then 不应该看到图片<验证图片1>
        Then 应该看到图片<app图片>
        Examples:
        | 应用1 | 应用2 | 应用3 | 应用4 | 验证图片1 | 验证图片2 | 验证图片3 | 验证图片4 | app图片 |
        | 云资料夹 | 浏览器 | 文件 | 云白板 | 正在运行云资料夹图标 | 正在运行浏览器图标 | 正在运行文件图标 | 正在运行云白板图标 | 宝可梦图片 |

    @buttomup_gohome-001
    Scenario Outline:已登录底部上划回到桌面1
        Given 已登录账号
        When 打开软件<应用>
        When 等待1秒
        When 底部上划回到桌面
        Then 存在时间
        Examples:
        | 应用 |
        | 云资料夹 |
        | 云白板 |

    @buttomup_gohome-002
    Scenario Outline:已登录底部上划回到桌面2
        Given 已登录账号
        When 打开软件<应用>
        And 底部上划唤出运行应用
        When 等待1秒
        When 底部上划回到桌面
        Then 存在时间
        Examples:
        | 应用 |
        | 云资料夹 |
        | 云白板 |

    @buttomup_gohome-003
    Scenario Outline:已登录底部上划回到桌面3
        Given 已登录账号
        When 打开软件<应用>
        And 底部上划唤出常用应用
        When 等待1秒
        When 底部上划回到桌面
        Then 存在时间
        Examples:
        | 应用 |
        | 云资料夹 |
        | 云白板 |

    @buttomup_gohome-004
    Scenario Outline:未登录底部上划回到桌面
        Given 未登录账号
        When 打开软件<应用>
        When 底部上划回到桌面
        When 等待0.5秒
        Then 存在时间
        Examples:
        | 应用 |
        | 云资料夹 |
        | 云白板 |
