<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-number-detection

之前在某群看到群成员一直满t都t不赢，所以我~~根据黑产的插件的功能~~写了个自动踢人的插件。

</div>

> [!warning] 
> **该插件未经测试，请谨慎使用**


## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-number-detection

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-number-detection
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-number-detection
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-number-detection
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-number-detection
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-plugin-number-detection"]

</details>


## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| is_automatic | 否 | false | 是否启用自动踢人 |
| headcount | 否 | 10 | 群最大人数 - 当前人数 大于这个值时执行踢人操作，否则不执行 |

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| group_ban | 主人 | 否 | all | 手动模式时的踢人命令 |