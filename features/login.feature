Feature: 登录
   
  Scenario: 未登录
    Given 未登录账号
    When 回到桌面
    Then 应该看到"账号登录图片"
  
  Scenario Outline: 登录
    Given 未登录账号
    When 点击 账号登录
    When 在账号输入<账号>
    When 在密码输入<密码>
    When 点击 登录
    Then 应该看到"下课图片"
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

  Scenario Outline: 输入错误的账号密码
    Given 未登录账号
    When 点击 账号登录
    When 在账号输入<账号>
    When 在密码输入<密码>
    When 点击 登录
    Then 应该看到"账号密码错误提示"
    Examples:
      | 账号 | 密码 |
      | 11223344556 | 123456 |

  Scenario Outline: 允许快捷登录
    Given 未登录账号
    When 点击 账号登录
    When 在账号输入<账号>
    When 在密码输入<密码>
    When 勾选 允许快捷登录
    When 点击 登录
    Then 应该看到"下课图片"
    When 点击 下课
    Then 应该看到<登录头像>
    Examples:
      | 账号 | 密码 | 登录头像 |
      | 18659131313 | 123456 | "深蓝色头像" |
      | 18659132323 | 123456 | "浅蓝色头像" |
      | 18659132313 | 123456 | "中蓝色头像" |

  
  Scenario: 点击头像登录
    Given 未登录账号
    When 点击 登录头像
    # Then 应该看到"登录成功提示"
    # When 点击"快速登录图片"
    Then 应该看到"下课图片"
  
  Scenario Outline: 点击账号列表
    Given 未登录账号
    When 点击 账号登录
    When 点击 登录历史
    When 点击坐标
    | x | y |
    | 500 | 475 |
    When 在密码输入<密码>
    When 点击 登录
    Then 应该看到"下课图片"
    Examples:
      | 密码 |
      | 123456 |

  Scenario: 删除快捷登录1
    Given 未登录账号
    When 删除登录头像
    Then 不存在 登录头像

  Scenario Outline: 删除快捷登录2
    Given 未登录账号
    When 点击 账号登录
    When 在账号输入<账号>
    When 在密码输入<密码>
    When 勾选 允许快捷登录
    When 点击 登录
    Then 应该看到"下课图片"
    When 点击 下课
    When 点击 账号登录
    When 点击 登录历史
    When 点击"移除账号"
    When 回到桌面
    Then 不存在 登录头像
    # Then 不应该看到"需要登录账号"
    Examples:
      | 账号 | 密码 |
      | 18659132323 | 123456 |

  Scenario Outline: 登录头像按登录时间排序/可左右滑动
    Given 未登录账号
    When 登录5个账号
    When 未登录账号
    When 点击 账号登录
    When 在账号输入<账号>
    When 在密码输入<密码>
    When 勾选 允许快捷登录
    When 点击 登录
    Then 应该看到"下课图片"
    Examples:
      | 账号 | 密码 |
      | 18304307622 | 123456 |
    And 点击 下课
    And 划动头像到最右边
    Then 应该看到"hjw的登录头像"
  
  Scenario Outline: 未登录打开应用
    # Scenario: 云资料夹登录
    Given 未登录账号
    When 点击 <app>
    When 等待0.5秒
    When 点击 账号登录
    When 在账号输入<账号>
    When 在密码输入<密码>
    When 点击 登录
    When 回到桌面
    Then 应该看到"下课图片"
    Examples:
      | app | 账号 | 密码 |
      | 云资料夹 | 18659131313 | 123456 |
      | 云白板 | 18659132323 | 123456 |

  Scenario Outline: 未登录打开应用2
    # Scenario: 云资料夹登录
    Given 未登录账号
    When 点击 <app>
    When 等待0.5秒
    Then 存在 取消按钮
    When 点击 取消按钮
    Then 存在 时间
    Examples:
      | app |
      | 云资料夹 |
      | 云白板 |

      
  Scenario Outline: 已登录打开云资料夹
  # Scenario: 未登录打开应用
    Given 登录账号
    When 点击 <app>
    Then 不存在 账号登录
    Then 应该看到<个人信息>
    Examples:
      | app | 个人信息 |
      | 云资料夹 | "ppt图片" |


  Scenario Outline: 已登录打开云白板
  # Scenario: 未登录打开应用
    Given 登录账号
    When 点击 <app>
    When 回到云白板主页
    Then 不存在 账号登录
    Then 应该看到<个人信息>
    Examples:
    | app | 个人信息 |
    | 云白板 | "宝可梦图片" |

  Scenario Outline: 保存不超过20个老师的登录信息
    Given 未登录账号
    When 点击 账号登录
    When 在账号输入<账号>
    When 在密码输入<密码>
    When 勾选 允许快捷登录
    When 点击 登录
    Then 应该看到"下课图片"
    Examples:
      | 账号 | 密码 |
      | 18304307622 | 123456 |
    When 登录20个账号
    And 点击 下课
    And 划动头像到最左边
    Then 不应该看到"hjw的登录头像"
