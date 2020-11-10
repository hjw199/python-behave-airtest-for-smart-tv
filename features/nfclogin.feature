@nfc_log_in
Feature: NFC登录

  @nfc_login-001
    Scenario: NFC登录-01
    Given 未登录账号
    When NFC登录账号18659132313
    When 等待1秒
    Then 存在下课

  @nfc_login-002
    Scenario: NFC登录-02
    Given 未登录账号
    When 删除登录头像
    When NFC登录账号18659132313
    When 等待1秒
    Then 存在下课
    When 点击按钮下课
    Then 存在账号登录
    Then 不存在登录头像

  @nfc_login-003
    Scenario: NFC登录-03
    Given 未登录账号
    When 登录账号18659131313
    When NFC登录账号18304307622
    When 等待1秒
    Then 存在下课
    Then 应该看到图片hjw的登录头像
    When 打开软件云白板
    Then 不应该看到图片宝可梦图片

  