@Third_Party_App
Feature: 第三方应用

    @Third_Party_Setup
    Scenario Outline:应用安装
        Given 安装<app>
        Then <app1>已安装
        Examples:
            | app | app1 |
            | RG_WhiteBoard_Screen.apk  | 云白板  |
            | RG-CloudFile-Screen.apk  | 云资料夹 |
            | com.viaton.wyt.apk  | 外研通 |

    @Third_Party_Permission
    Scenario Outline: 应用权限授予
        Given 授予<app>权限
        When 打开软件<app1>
        Then 不应该看到图片授权图片
        Examples:
            | app | app1 |
            | 云资料夹  | 云资料夹  |
            | 云白板  | 云白板  |
            | WPS  | WPS |
    
    @Force_Landscape
    Scenario Outline:强制横屏
        Given <app>已安装
        When 打开软件<app1>
        Then 不应该看到图片<pic>
        Examples:
            | app | app1 | pic |
            | 外研通  | 外研通  | 未横屏图片  |
