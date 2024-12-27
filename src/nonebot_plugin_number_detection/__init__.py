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

    if (await_ban := max_member_count - member_count) >= plugin_config.headcount:
        group_user_list = [int(i["user_id"]) for i in await bot.get_group_member_list(group_id= group_id)]
        user_last_sent_time = []
        
        for i in group_user_list:
            last_sent_time = await bot.get_group_member_info(group_id= group_id, user_id= i)
            user_last_sent_time.append([i, last_sent_time["last_sent_time"]])

        user_last_sent_time.sort(key=lambda x: x[1])
        await_user_ban_list = [i[0] for i in user_last_sent_time]
        print(await_user_ban_list)

        for i in range(await_ban):
            await bot.set_group_kick(group_id= group_id, user_id= await_user_ban_list[0], reject_add_request= False)
            await_user_ban_list.remove(await_user_ban_list[0])
    
    else:
        return f"需要群人数到达{max_member_count - plugin_config.headcount}"


@group_ban.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent):

    if plugin_config.is_automatic:
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