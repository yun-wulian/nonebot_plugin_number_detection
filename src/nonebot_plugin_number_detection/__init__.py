from nonebot import on_command, on_notice
from .config import plugin_config

from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupIncreaseNoticeEvent,
    GroupMessageEvent
)
from nonebot.permission import SUPERUSER


from nonebot.plugin import PluginMetadata
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="群成员检测 dev版",
    description="检测群人数，当群剩余的空位人数达到设定值，则自动踢出群员",
    usage="发送 /group_ban即可手动触发检测（自动检测默认关闭）",
    config=Config,
    type="application",
    homepage="https://github.com/zhongwen-4/nonebot_plugin_number_detection",
    supported_adapters= {"~onebot.v11"}
)


group_ban = on_notice(block= False)
group_ban_cmd = on_command("group_ban", aliases={"群成员检测"}, permission= SUPERUSER)


async def group_kick(bot: Bot, group_id: int):
    group_info = await bot.get_group_info(group_id= group_id)
    max_member_count = group_info['max_member_count']
    member_count = group_info['member_count']

    remaining = max_member_count - member_count
    #触发条件改为剩余空位小于设定值时触发
    if remaining < plugin_config.detect_headcount:
        #计算实际需要踢出的人数
        need_kick = plugin_config.detect_headcount - remaining
        
        member_list = await bot.get_group_member_list(group_id=group_id)
        user_last_sent_time = [
            (m['user_id'], m['last_sent_time'])
            for m in member_list
            if m['role'] == 'member'
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