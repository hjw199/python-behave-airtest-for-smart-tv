@launcher
Feature: 桌面

    @desktop_icon
    Scenario Outline: 桌面图标检查
        Given 回到首页
        Then 不应该看到图片<图标>
        When 向左滑动切到下一页
        Then 不应该看到图片<图标>
        When 向左滑动切到下一页
        Then 不应该看到图片<图标>
        Examples:
        | 图标 |
        # | 'WPS桌面图标' |
        # | '系统音频播放工具桌面图标' |
        | 系统视频播放工具桌面图标 |
        | 系统图片播放工具桌面图标 |

    @adte_time
    Scenario: 日期与时间
        Given 回到桌面
        Given 回到首页
        Then 存在日期
        Then 存在时间
        Then 日期时间准确
