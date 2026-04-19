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

## 重要说明

这不是法律意见，也不能保证你的站点因此一定满足所有中国大陆监管要求或一定不会被屏蔽。

它只能帮助你把 Umami 的相关 UI 显示调整为更符合你当前站点面向大陆用户的展示方式。最终是否合规，还取决于：

- 你的网站整体内容
- 你的备案 / 业务性质 / 地区服务策略
- 其他第三方脚本与页面文案
- 你自己的法律审查

## 使用方法

1. 在 GitHub 新建一个仓库，例如 `umami-cn-builder`
2. 把本模板全部文件上传进去
3. 到仓库 Settings -> Actions -> General，确认允许 Actions 运行
4. 到仓库 Settings -> Packages，确认允许发布 GHCR 包
5. 首次手动运行 `Build CN Umami` 工作流
6. 构建完成后，镜像会发布到：

```text
ghcr.io/<你的 GitHub 用户名小写>/umami-cn:<上游版本号>
ghcr.io/<你的 GitHub 用户名小写>/umami-cn:latest
```

## 部署示例

Umami v3 使用 PostgreSQL。

```yaml
services:
  umami:
    image: ghcr.io/<你的 GitHub 用户名小写>/umami-cn:latest
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://umami:umami_password@postgres:5432/umami
      APP_SECRET: change-this-to-a-long-random-string
    depends_on:
      - postgres

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: umami
      POSTGRES_USER: umami
      POSTGRES_PASSWORD: umami_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 你可以继续自定义的地方

- 改镜像名：编辑工作流中的 `IMAGE_NAME`
- 改检查频率：编辑 cron
- 改标签策略：编辑 docker build 的 tags
- 增加更多大陆展示层覆盖：在 `scripts/apply_cn_patch.py` 中追加规则
