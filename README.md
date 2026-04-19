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

## 你需要开启什么

### 1. 启用 GitHub Actions
仓库创建后，进入 **Actions** 页面，允许工作流运行。

### 2. 允许推送到 GHCR
默认使用 `GITHUB_TOKEN` 推送到 GitHub Container Registry：

- 镜像地址：`ghcr.io/<你的 GitHub 用户名小写>/umami-cn`
- 无需额外 Docker Hub 账号

### 3. 包权限
如果你的 GHCR 包默认是私有的，需要在 GitHub Packages 页面把它改成 public，或者在服务器登录后拉取私有镜像。

## 如何手动触发构建

进入：

- `Actions` → `Build CN Umami` → `Run workflow`

第一次建议手动跑一次，确认镜像已成功推送。

## 自动更新逻辑

工作流会：

- 每天定时检查一次官方最新 tag
- 在 push 到 `main` 时执行一次
- 支持手动执行

生成的镜像标签：

- `ghcr.io/<你的用户名小写>/umami-cn:latest`
- `ghcr.io/<你的用户名小写>/umami-cn:vX.Y.Z`

## 服务器部署示例

Umami v3 仅支持 PostgreSQL。

### docker-compose.yml

```yaml
services:
  umami-db:
    image: postgres:16-alpine
    container_name: umami-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: umami
      POSTGRES_USER: umami
      POSTGRES_PASSWORD: change-this-password
    volumes:
      - umami-db-data:/var/lib/postgresql/data

  umami:
    image: ghcr.io/culesky/umami-cn:latest
    container_name: umami
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://umami:change-this-password@umami-db:5432/umami
      APP_SECRET: change-this-to-a-long-random-string
    depends_on:
      - umami-db

volumes:
  umami-db-data:
```

启动：

```bash
docker compose up -d
```

## 反向代理

把你的域名反代到 Umami 容器的 `3000` 端口即可。

Nginx 最基本示例：

```nginx
server {
    listen 80;
    server_name analytics.example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 目录说明

- `.github/workflows/build-cn.yml`：自动构建与推送镜像
- `scripts/apply_cn_patch.py`：对上游 Umami 自动打补丁

## 重要说明

这套仓库做的是 **展示层本地化调整**，不是法律意见，也不构成任何合规承诺。

它的目标是：

- 不长期依赖第三方魔改分支
- 永远基于官方最新版自动重建
- 把修改范围控制在尽量小的展示层补丁中

## 后续你可以怎么改

如果你还想继续做更强的大陆本地化，可以在 `scripts/apply_cn_patch.py` 里继续追加：

- 默认中文语言
- 去除某些敏感展示字符串
- 自定义 logo / 标题
- 适配你自己的部署品牌
