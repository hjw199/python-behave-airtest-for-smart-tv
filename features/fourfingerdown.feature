# Feature: 四指下滑进入小屏模式

#    Scenario Outline:在桌面进行四指下滑，下滑距离小于60%
#    Given 回到桌面
#    When 四指下划缩小屏幕至<ratio1>
#    Then <pic>成比例缩小至<ratio2>
#    Examples:
#    | ratio1 | pic | ratio2 |
#    | 0.9 | 云白板图标 | 0.9 |
#    | 0.85 | 云白板图标 | 0.85 |
#    | 0.8 | 云白板图标 | 0.8 |
#    | 0.75 | 云白板图标 | 0.75 |
#    | 0.7 | 云白板图标 | 0.7 |
#    | 0.65 | 云白板图标 | 0.65 |
#    | 0.6 | 云白板图标 | 0.6 |

#    Scenario Outline:在桌面进行四指下滑，下滑距离大于60%
#    Given 回到桌面
#    When 四指下划缩小屏幕至<ratio1>
#    Then <pic>成比例缩小至<ratio2>
#    Examples:
#    | 0.5 | 云白板图标 | 0.6 |

#    Scenario Outline:未登录账号打开应用进行四指下滑
#         Given 未登录账号
#         When 打开<app>
#         When 四指下划缩小屏幕至<ratio1>
#         When 等待0.5秒
#         Then <pic>成比例缩小至<ratio2>
#         Examples:
#         | app |ratio1 | pic | ratio2 |
#         | "云白板" | 0.6 | 账号登录图标 | 0.6 |
#         | "云资料夹" | 0.6 | 账号登录图标 | 0.6 |

#    Scenario Outline:已登录账号打开应用进行四指下滑
#         Given 登录账号
#         When 打开<app>
#         When 四指下划缩小屏幕至<ratio1>
#         When 等待0.5秒
#         Then <pic>成比例缩小至<ratio2>
#         Examples:
#         | app |ratio1 | pic | ratio2 |
#         | "云白板" | 0.6 | 宝可梦图片 | 0.6 |
#         | "云资料夹" | 0.6 | ppt图片 | 0.6 |


