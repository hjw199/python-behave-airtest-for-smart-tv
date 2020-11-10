@touch
Feature: 触控

    @white_small_character
    Scenario: 写小字
        Given 登录账号18659132313
        When 打开软件云白板
        And 新建白板
        And 关闭提笔即写模式
        And 点击按钮画笔
        And 写小正字
        And 截图保存小正字
        Then 应该看到图片小正字

    @touchdown_and_swipe
    Scenario: 一指点击一指划线
        Given 登录账号18659132313
        When 打开软件云白板
        And 新建白板
        And 关闭提笔即写模式
        And 点击按钮画笔
        And 一指点击一指划线
        And 截图保存一指点击一指划线
        Then 应该看到图片点线不相连

    @fullswipe
    Scenario: 全屏划线
        Given 登录账号18659132313
        When 打开软件云白板
        And 新建白板
        And 关闭提笔即写模式
        And 点击按钮画笔
        And 全屏划线
        And 截图保存全屏划线
        Then 应该看到图片全屏划线
    
    @close_brower_page
    Scenario: 关闭浏览器页面
        Given 登录账号18659132313
        And 打开软件浏览器
        When 点击按钮浏览器新建页
        And 点击按钮关闭浏览器页
        And 点击按钮关闭浏览器页
        Then 存在下课

    @PPT_turn_page
    Scenario: PPT翻页
        Given 登录账号18659132313
        When 打开软件云资料夹
        And 点击按钮PPT
        And 等待5秒
        # And 点击 播放PPT
        And 向后翻10页
        Then 应该看到图片第11页
        When 向后翻90页
        Then 应该看到图片第101页
