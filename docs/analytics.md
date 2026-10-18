# Microsoft Clarity 接入

配置文件：`claude-code-session-viewer/analytics.json`。

```json
{
  "projectId": "yzkymu6lyt",
  "allowedHosts": ["ccviewer.top", "www.ccviewer.top"]
}
```

线上域名的 HTTPS 页面直接异步加载站点所有者提供的 Clarity 标签代码，无同意弹窗、统计设置、额外遮蔽或导入会话时暂停录制逻辑。不发送自定义同意信号，Cookie 和录制行为由 Clarity SDK 与项目设置处理。

localhost、预览域名和离线文件不加载统计，避免开发和离线使用产生数据。带查询参数或片段的线上页面正常加载。

保留入口事件：`file_picker_open`、`folder_picker_open`、`paste_open`、`help_open`、`github_open`。

运行 `python3 claude-code-session-viewer/build.py`，通过现有部署流程发布全部 60 个生成页面。将 `projectId` 清空并重新构建发布可关闭统计。

验证命令：`node tests/analytics.cjs`、`python3 tests/check_pages.py`。线上打开页面应直接请求 `https://www.clarity.ms/tag/yzkymu6lyt`，无须点击任何同意按钮。录屏、热力图和事件入库需在 Clarity 仪表盘确认。
