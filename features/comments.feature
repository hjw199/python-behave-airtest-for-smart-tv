@comments
Feature: 批注书写

    @comments_write
    Scenario Outline:批注书写
        Given 回到桌面
        When 点击图片侧边栏
        And 点击图片批注图标
        When 点击按钮批注画笔
        And 点击按钮<size>
        And 画正方形
        Then 应该看到图片<pic>
        Examples:
            | size | pic |
            | 批注细笔 | 批注细笔正方形 |
            | 批注中笔 | 批注中笔正方形 |
            | 批注粗笔 | 批注粗笔正方形 |

    @comments_move
    Scenario:批注移动
        Given 回到桌面
        When 点击图片侧边栏
        And 点击图片批注图标
        And 等待0.5秒
        When 移动批注到任意位置
        Then 批注移动到对应位置

    @comments_rubber
    Scenario Outline:批注擦除
        Given 回到桌面
        When 点击图片侧边栏
        And 点击图片批注图标
        When 点击按钮批注画笔
        And 点击按钮批注细笔
        And 画正方形
        Then 应该看到图片批注细笔正方形
        When 点击按钮批注橡皮
        When 点击按钮批注橡皮
        And 点击按钮<size>
        And 画正方形
        Then 不应该看到图片<pic>
        Examples:
            | size | pic |
            | 批注小橡皮 | 批注细笔正方形 |
            | 批注中橡皮 | 批注细笔正方形 |
            | 批注大橡皮 | 批注细笔正方形 |
    
    @comments_swipe_rubber
    Scenario:批注一键清除
        Given 回到桌面
        When 点击图片侧边栏
        And 点击图片批注图标
        When 点击按钮批注画笔
        And 点击按钮批注细笔
        And 画正方形
        Then 应该看到图片批注细笔正方形
        When 点击按钮批注橡皮
        When 点击按钮批注橡皮
        And 滑动擦除
        Then 不应该看到图片批注细笔正方形

    # @comments_save
    # Scenario:批注保存
    #     Given 回到桌面
    #     When 点击图片侧边栏
    #     And 点击图片批注图标
    #     When 点击按钮批注画笔
    #     And 点击按钮批注细笔
    #     And 画正方形
    #     Then 应该看到图片批注细笔正方形
    #     When 点击按钮批注保存
    #     Then 目录下存在文件

    @comments_close
    Scenario:批注关闭
        Given 回到桌面
        When 点击图片侧边栏
        And 点击图片批注图标
        Then 等待0.5秒
        # Then 应该看到"批注图片"
        Then 存在批注画笔
        When 点击按钮批注关闭
        # Then 不应该看到"批注图片"
        Then 不存在批注画笔
