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
      | 18659132323 | 123456 |
      | 18659132313 | 123456 |

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
    Examples:
      | 账号 | 密码 |
      | 18659131313 | 123456 |
      | 18659132323 | 123456 |
      | 18659132313 | 123456 |

  
  Scenario: 点击头像登录
    Given 未登录账号
    When 点击 登录头像
    # When 点击"快速登录图片"
    Then 应该看到"下课图片"
  
  Scenario: 点击账号登录
    Given 未登录账号
    When 点击 账号登录
    When 点击 登录历史
    When 点击"需要登录账号"  #未识别出图片
    Then 应该看到"下课图片"

  Scenario: 删除快捷登录
    Given 未登录账号
    When 删除登录头像
    Then 不存在 登录头像

#实际未完成，验证过了
  Scenario Outline: 删除快捷登录
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
    Then 不应该看到"需要登录账号"
    Examples:
      | 账号 | 密码 |
      | 18659132323 | 123456 |
  
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

      
  Scenario Outline: 已登录打开云资料夹
  # Scenario: 未登录打开应用
    Given 登录账号
    When 点击 <app>
    Then 不存在 账号登录
    Then 应该看到<个人信息>
    Examples:
      | app | 个人信息 |
      | 云资料夹 | "ppt图片" |
#PPT图片未识别出来

  Scenario Outline: 已登录打开云白板
  # Scenario: 未登录打开应用
    Given 登录账号
    When 点击 <app>
    When 回到云白板主页
    Then 不存在 账号登录
    Then 应该看到<个人信息>
  


  Scenario: 日期与时间
    Given 回到桌面
    Then 存在 日期
    Then 存在 时间
    Then 日期时间准确
