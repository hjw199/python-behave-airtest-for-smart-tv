Feature: 底部上划

'''常用工具栏'''

   Scenario:常用工具栏
      When 底部上划唤出常用应用
      Then 应该看到"常用应用栏"

   Scenario Outline:已登录点击常用工具栏应用
      Given 已登录账号
      When 底部上划唤出常用应用
      When 点击<图标>
      Then 应该看到<验证图片>
      Examples:
      | 图标 | 验证图片 |
      | "常用应用云白板图标" | "宝可梦图片" |
      | "常用应用云资料夹图标" | "ppt图片" |
   '''底边图标与桌面图标类似，图像识别出错'''

  Scenario Outline:未登录点击常用工具栏应用
      Given 未登录账号
      When 底部上划唤出常用应用
      When 点击<图标>
      When 点击 账号登录
      When 在账号输入<账号>
      When 在密码输入<密码>
      When 点击 登录
      Then 应该看到<验证图片>
      Examples:
      | 图标 | 账号 | 密码 | 验证图片 |
      |  "常用应用云白板图标"  | 18659131313  | 123456 | "宝可梦图片" |
      | "常用应用云资料夹图标" | 18659131313  | 123456 | "ppt图片" |

   Scenario Outline:点击常用工具栏外围
      Given 已登录账号
      Given 打开<应用>
      When 底部上划唤出常用应用
      Then 应该看到"常用应用栏"
      When 点击常用应用栏外围
      Then 不应该看到"常用应用栏"
      Then 应该看到<验证图片>
      | 应用 | 验证图片 |
      | "云白板" | "宝可梦图片" |
      | "云资料夹" | "ppt图片" |
      | "NB物理实验" |
      | "NB化学实验" |
      | "浏览器" |
      | "视频播放器" |
      | "WPS" |

   '''正在运行应用'''

   Scenario:未运行应用唤出运行应用列表
      Given 未运行应用
      When 底部上划唤出运行应用
      Then 不应该看到"正在运行应用"

   Scenario Outline:运行应用唤出正在运行应用
      Given 未运行应用
      When 回到桌面
      When 打开<应用>
      When 回到桌面
      When 底部上划唤出运行应用
      Then 应该看到<验证图片>
      Examples:
      | 应用 | 验证图片 |
      | "云白板" | "正在运行云白板图标" |
      | "云资料夹" | "正在运行云资料夹图标" |

   Scenario Outline:点击打开正在运行应用1
      Given 已登录账号
      Given 未运行应用
      When 打开<应用>
      When 回到桌面
      When 底部上划唤出运行应用
      When 点击<正在运行应用>
      Then 应该看到<验证图片>
      Examples:
      | 应用 | 正在运行应用 | 验证图片 |
      | "云白板" | "正在运行云白板图标" | "宝可梦图片" |
      | "云资料夹" | "正在运行云资料夹图标" | "ppt图片" |

  Scenario Outline:点击打开正在运行应用2
      Given 未登录账号
      Given 未运行应用
      When 打开<应用>
      When 回到桌面
      When 底部上划唤出运行应用
      When 点击<正在运行应用>
      When 等待1秒
      Then 存在 账号登录
      Examples:
      | 应用 | 正在运行应用 |
      | "云白板" | "正在运行云白板图标" |
      | "云资料夹" | "正在运行云资料夹图标" |

   Scenario Outline:点击关闭正在运行应用
      Given 已登录账号
      Given 未运行应用
      When 打开<应用>
      When 回到桌面
      When 底部上划唤出运行应用
      When 点击"关闭正在运行应用"
      Then 不应该看到"正在运行应用"
      Examples:
      | 应用 |
      | "云白板" |
      | "云资料夹" |

   Scenario Outline:点击正在运行应用外围
      Given 已登录账号
      Given 打开<应用>
      When 底部上划唤出运行应用
      Then 应该看到<验证图片>
      When 点击运行应用外围
      Then 不应该看到<验证图片>
      Then 应该看到<app验证图片>
      | 应用 | 验证图片 | app验证图片 |
      | "云白板" |  "正在运行云白板图标" | "宝可梦图片" |
      | "云资料夹" | "正在运行云资料夹图标" | "ppt图片" |
      | "NB物理实验" |
      | "NB化学实验" |
      | "浏览器" |
      | "视频播放器" |
      | "WPS" |

 '''底部上划回到桌面'''

   Scenario Outline:已登录底部上划回到桌面
      Given 已登录账号
      When 打开<应用>
      When 底部上划回到桌面
      Then 存在 时间
      Examples:
      | 应用 |
      | "云白板" |
      | "云资料夹" |

   Scenario Outline:未登录底部上划
      Given 未登录账号
      When 打开<应用>
      When 底部上划回到桌面
      Then 存在 时间
      Examples:
      | 应用 |
      | "云白板" |
      | "云资料夹" |
