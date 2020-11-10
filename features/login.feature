@log_in
Feature: 登录

    @not_login
        Scenario: 未登录
        Given 未登录账号
        When 回到桌面
        Then 应该看到图片账号登录图片

    @login
        Scenario Outline: 登录
        Given 未登录账号
        When 点击按钮账号登录
        When 在账号输入<账号>
        When 在密码输入<密码>
        When 点击按钮登录
        Then 应该看到图片下课图片
        Examples:
        | 账号 | 密码 |
        | 18659131313 | 123456 |

    # Scenario Outline: 登录成功提示
    #   Given 未登录账号
    #   When 点击 账号登录
    #   When 在账号输入<账号>
    #   When 在密码输入<密码>
    #   When 点击 登录
    #   Then 应该看到"登录成功提示"
    #   Examples:
    #     | 账号 | 密码 |
    #     | 18659131313 | 123456 |
    @mistake_account_password
    Scenario Outline: 输入错误的账号密码
        Given 未登录账号
        When 点击按钮账号登录
        When 在账号输入<账号>
        When 在密码输入<密码>
        When 点击按钮登录
        Then 应该看到图片账号密码错误提示
        Examples:
        | 账号 | 密码 |
        | 11223344556 | 123456 |

    @allow_quick_login
    Scenario Outline: 允许快捷登录
        Given 未登录账号
        When 点击按钮账号登录
        When 在账号输入<账号>
        When 在密码输入<密码>
        When 勾选允许快捷登录
        When 点击按钮登录
        Then 应该看到图片下课图片
        When 点击按钮下课
        Then 应该看到图片<登录头像>
        Examples:
        | 账号 | 密码 | 登录头像 |
        | 18659131313 | 123456 | 深蓝色头像 |
        | 18659132323 | 123456 | 浅蓝色头像 |
        | 18659132313 | 123456 | 中蓝色头像 |

    @click_head_portrait_login
    Scenario: 点击头像登录
        Given 未登录账号
        When 点击按钮登录头像
        # Then 应该看到"登录成功提示"
        # When 点击"快速登录图片"
        Then 应该看到图片下课图片

    @click_account_list_login
    Scenario Outline: 点击账号列表
        Given 未登录账号
        When 点击按钮账号登录
        When 点击按钮登录历史
        When 点击坐标
        | x | y |
        | 500 | 475 |
        When 在密码输入<密码>
        When 点击按钮登录
        Then 应该看到图片下课图片
        Examples:
        | 密码 |
        | 123456 |

    @remove_quick_login-001
    Scenario: 删除快捷登录1
        Given 未登录账号
        When 删除登录头像
        Then 不存在登录头像

    @remove_quick_login-002
    Scenario Outline: 删除快捷登录2
        Given 未登录账号
        When 点击按钮账号登录
        When 在账号输入<账号>
        When 在密码输入<密码>
        When 勾选允许快捷登录
        When 点击按钮登录
        Then 应该看到图片下课图片
        When 点击按钮下课
        When 点击按钮账号登录
        When 点击按钮登录历史
        When 点击图片移除账号
        When 回到桌面
        Then 不存在登录头像
        # Then 不应该看到"需要登录账号"
        Examples:
        | 账号 | 密码 |
        | 18659132323 | 123456 |

    @head_portrait_swipe_order
    Scenario Outline: 登录头像按登录时间排序/可左右滑动
        Given 未登录账号
        When 登录5个账号
        When 未登录账号
        When 点击按钮账号登录
        When 在账号输入<账号>
        When 在密码输入<密码>
        When 勾选允许快捷登录
        When 点击按钮登录
        Then 应该看到图片下课图片
        Examples:
        | 账号 | 密码 |
        | 18304307622 | 123456 |
        And 点击按钮下课
        And 划动头像到最右边
        Then 应该看到图片h的登录头像

    @not_login_open_app-001
    Scenario Outline: 未登录打开应用
    # Scenario: 云资料夹登录
        Given 未登录账号
        When 点击按钮<app>
        When 等待0.5秒
        When 点击按钮账号登录
        When 在账号输入<账号>
        When 在密码输入<密码>
        When 点击按钮登录
        When 回到桌面
        Then 应该看到图片下课图片
        Examples:
        | app | 账号 | 密码 |
        | 云资料夹 | 18659131313 | 123456 |
        | 云白板 | 18659132323 | 123456 |

    @not_login_open_app-002
    Scenario Outline: 未登录打开应用2
    # Scenario: 云资料夹登录
        Given 未登录账号
        When 点击按钮<app>
        When 等待0.5秒
        Then 存在取消按钮
        When 点击按钮取消按钮
        Then 存在时间
        Examples:
        | app |
        | 云资料夹 |
        | 云白板 |

    @login_open_cloud_file_app
    Scenario Outline: 已登录打开云资料夹
    # Scenario: 未登录打开应用
        Given 登录账号18659131313
        When 点击按钮<app>
        Then 不存在账号登录
        Then 应该看到图片<个人信息>
        Examples:
        | app | 个人信息 |
        | 云资料夹 | ppt图片 |

    @login_open_cloud_whiteboard
    Scenario Outline: 已登录打开云白板
    # Scenario: 未登录打开应用
        Given 登录账号18659131313
        When 点击按钮<app>
        When 回到云白板主页
        Then 不存在账号登录
        Then 应该看到图片<个人信息>
        Examples:
        | app | 个人信息 |
        | 云白板 | 宝可梦图片 |
    
    @logout
    Scenario: 登出账号
    # Scenario: 未登录打开应用
        Given 登录账号18659131313
        When 打开软件云白板
        When 打开软件云资料夹
        When 打开软件浏览器
        When 回到桌面
        When 点击按钮下课
        When 底部上划唤出运行应用
        Then 不应该看到图片正在运行应用

    @save_20_account_at_most
    Scenario Outline: 保存不超过20个老师的登录信息
        Given 未登录账号
        When 点击按钮账号登录
        When 在账号输入<账号>
        When 在密码输入<密码>
        When 勾选允许快捷登录
        When 点击按钮登录
        Then 应该看到图片下课图片
        Examples:
        | 账号 | 密码 |
        | 18304307622 | 123456 |
        When 登录20个账号
        And 点击按钮下课
        And 划动头像到最左边
        Then 不应该看到图片hjw的登录头像
