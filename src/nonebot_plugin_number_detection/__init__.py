from nonebot import on_command, on_notice,logger
from .config import plugin_config

from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupIncreaseNoticeEvent,
    GroupMessageEvent
)
from nonebot.permission import SUPERUSER


from nonebot.plugin import PluginMetadata
from .config import Config

import json
from pathlib import Path
from typing import Dict
from nonebot import require
require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import Args, Alconna, on_alconna, Match

__plugin_meta__ = PluginMetadata(
    name="群成员检测 dev版",
    description="检测群人数，当群剩余的空位人数达到设定值，则自动踢出群员",
    usage="发送 /踢人即可手动触发检测（自动检测默认关闭）",
    config=Config,
    type="application",
    homepage="https://github.com/zhongwen-4/nonebot_plugin_number_detection",
    supported_adapters= {"~onebot.v11"}
)

group_settings_path = Path(__file__).parent / "group_settings.json"
group_ban = on_notice(block= False)
group_ban_cmd = on_command("踢人", aliases={"群成员检测"}, permission= SUPERUSER)
set_remain = on_alconna(Alconna("/设置空位", Args["amount", int]), permission= SUPERUSER)
clear_settings = on_command("清空空位", aliases={"清空设置"}, permission= SUPERUSER)
clear_settings_on_group = on_command("删除空位", aliases={"删除空位"}, permission= SUPERUSER)
show_settings_on_group = on_command("查看空位", aliases={"查看空位"}, permission= SUPERUSER)

def load_group_settings() -> Dict[str, int]:
    try:
        with open(group_settings_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_group_settings(settings: Dict[str, int]):
    with open(group_settings_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

def clear_group_settings():
    save_group_settings({})

@clear_settings.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    clear_group_settings()
    await clear_settings.finish("已清空群聊空位信息")

@clear_settings_on_group.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    settings = load_group_settings()
    del settings[str(event.group_id)]
    save_group_settings(settings)
    await clear_settings_on_group.finish(f"群 {event.group_id} 的预留空位设置已清空")

@show_settings_on_group.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    settings = load_group_settings()
    logger.info(settings)
    amount = settings[str(event.group_id)]
    await show_settings_on_group.finish(f"群 {event.group_id} 的预留空位已设置为 {amount}")

@set_remain.handle()
async def handle_set_remain(event: GroupMessageEvent, amount: Match[int]):
    settings = load_group_settings()
    settings[str(event.group_id)] = amount.result
    logger.info(settings)
    save_group_settings(settings)
    await set_remain.finish(f"群 {event.group_id} 的预留空位已设置为 {amount.result}")


async def group_kick(bot: Bot, group_id: int):
    group_settings = load_group_settings()
    # 优先使用群专用配置，不存在则使用全局配置
    threshold = group_settings.get(str(group_id), plugin_config.detect_headcount)
    
    group_info = await bot.get_group_info(group_id=group_id)
    max_member_count = group_info['max_member_count']
    member_count = group_info['member_count']

    remaining = max_member_count - member_count
    if remaining < threshold:
        need_kick = threshold - remaining
        
        # 修正3：一次性获取全部成员信息
        member_list = await bot.get_group_member_list(group_id=group_id)
        user_last_sent_time = [
            (m['user_id'], m['last_sent_time'])
            for m in member_list
            if m['role'] == 'member'  # 过滤普通成员
        ]
        
        # 按最后发言时间排序（从未发言的优先）
        user_last_sent_time.sort(key=lambda x: x[1])
        
        # 踢出需要数量的成员
        for user_id, _ in user_last_sent_time[:need_kick]:
            await bot.set_group_kick(
                group_id=group_id,
                user_id=user_id,
                reject_add_request=False
            )
    
    else:
        return f"当前剩余空位 {remaining} 已满足要求"


@group_ban.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):

    if plugin_config.detect_is_automatic:
        await group_ban.send("群员增加，正在执行群组踢人操作")
        msg = await group_kick(bot, event.group_id)

        if isinstance(msg, str):
            await group_ban.finish(msg)

        await group_ban.finish("群组踢人操作已完成")


@group_ban_cmd.handle()
async def _(bot: Bot, event: GroupMessageEvent):

    await group_ban_cmd.send("正在执行群组踢人操作")
    msg = await group_kick(bot, event.group_id)

    if isinstance(msg, str):
        await group_ban_cmd.finish(msg)

    await group_ban_cmd.finish("群组踢人操作已完成")