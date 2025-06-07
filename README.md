# Modal 部署指南

1. 注册网站：[https://modal.com](https://modal.com)

2. 在个人资料页–>API Tokens，创建token,例如：modal token set –token-id ak-XVbmGM9PF3TLwiu52 –token-secret as-Wo9a4CUsfGHkFu8q

3. 在 GitHub 仓库的 Settings → Secrets and variables → Actions 中，设置以下两个变量：

- `MODAL_TOKEN_ID`  
  这是你的 Modal Token ID，上一步以 `ak-` 开头的一串字符，比如 `ak-XVbmGM9PF3TLwiu52`。

- `MODAL_TOKEN_SECRET`  
  这是你的 Modal Token Secret，上面以 `as-` 开头的一串字符，比如 `as-Wo9a4CUsfGHkFu8q`。

4. 节点获取说明： 支持上传订阅服务器，上传TG，手搓节点，进入哪吒查看list.log四种方式

---

## 项目说明

本项目目前处于可用状态，仅供凑合使用。

特别感谢上游项目作者 eooce 的 py-argo 项目。
