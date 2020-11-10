# @Clouds_Background_Downloads
# Feature: 云资料夹后台下载
#     Scenario Outline:云资料夹后台下载
#         Given 删除<user>文件
#         When 登录账号18659131313
#         And 等待2秒
#         And 点击按钮下课
#         And 等待2秒
#         Then 服务<process>存在
#         Examples:
#             | user | process |
#             | "/sdcard/ruijie_white_board_cloud_file/user"  | Value 2  |