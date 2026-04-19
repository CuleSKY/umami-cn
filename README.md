# Umami CN Builder Template

这是一套用于 **自动跟进官方 Umami 上游版本并构建大陆展示友好镜像** 的 GitHub Actions 模板。

它做的事情：

- 每天检查官方 `umami-software/umami` 最新 tag
- 拉取上游源码
- 自动应用一层极小的中国大陆展示补丁
- 构建并推送 GHCR 镜像
- 不长期依赖第三方 fork

## 这套模板修改了什么

仅做 **前端展示层本地化覆盖**：

- `zh-CN` 下把 `TW` 的名称显示改为 `中国台湾`
- 把 `TW` 对应的国旗图片映射为 `CN`
- 保留底层国家代码不变，统计数据本身仍然来自 Umami 原始国家代码


