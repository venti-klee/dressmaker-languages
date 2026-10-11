"""Stable error codes keep dynamic UI messages independent of the target game language."""
import urllib.error
import socket

ERROR_CODES = {
    "无效的词典筛选条件": "error_filter",
    "目标语言已更改，请刷新列表后保存": "error_save_language",
    "译文破坏了标签或变量，已拒绝写入": "error_format",
    "译文中的格式标签或变量与原文不一致": "error_format",
    "译文为空或过长": "error_value",
    "翻译服务返回了错误提示": "error_service",
    "接口返回内容过大": "error_response",
    "开关必须为布尔值": "error_setting",
    "暂不支持此语言": "error_language",
    "未知翻译服务": "error_setting",
    "LibreTranslate 地址必须为 HTTPS，不能包含账号密码": "error_libre",
    "每日预算必须在 0 到 50000 字节之间": "error_budget_value",
    "请填写游戏目录": "error_game",
    "未知设置": "error_setting",
    "此目录未找到 Yuuma ModLoader，请先安装其 Mac 版": "error_loader",
    "请先安装 Yuuma ModLoader 的 Mac 版": "error_loader",
    "单条超过免费接口的 500 字节限制，请安装离线模型或手动翻译": "error_length",
    "今日免费接口预算已用完；离线词典和缓存仍然可用": "error_budget",
    "请填写你可使用的 LibreTranslate HTTPS 地址": "error_libre",
    "免费接口限额或暂不可用": "error_service",
    "必应网页接口已变化或暂不可用": "error_bing",
    "Google 网页接口已变化或暂不可用": "error_google",
    "缺少已编译的游戏插件": "error_plugin",
    "请使用启动助手打开的链接": "error_session",
    "会话无效": "error_session",
    "未找到页面": "error_request",
    "禁止跨站请求": "error_session",
    "请求内容过大": "error_request",
    "请选择要安装模型的目标语言": "error_model_language",
    "已有模型正在安装": "error_model_busy",
    "未知操作": "error_request",
}

def error_info(error):
    message = str(error)
    if not message:
        return None
    if isinstance(error, PermissionError) or "Permission denied" in message or "Operation not permitted" in message:
        return {"key": "error_permission", "params": {}}
    if isinstance(error, urllib.error.HTTPError) and error.code == 429:
        return {"key": "error_rate_limit", "params": {}}
    if isinstance(error, (TimeoutError, socket.timeout)) or isinstance(error, urllib.error.URLError) and isinstance(error.reason, (TimeoutError, socket.timeout)):
        return {"key": "error_timeout", "params": {}}
    if isinstance(error, (urllib.error.URLError, TimeoutError)) or message.startswith("<urlopen error"):
        return {"key": "error_network", "params": {}}
    prefix = "离线模型未能翻译此条文本："
    if message.startswith(prefix):
        return {"key": "error_offline", "params": {"detail": message[len(prefix):]}}
    key = ERROR_CODES.get(message, "error_generic")
    return {"key": key, "params": {"detail": message} if key == "error_generic" else {}}
