<!-- 文件说明：源码目录说明文档。用于概览应用代码、数据目录、测试目录和开发约定。 -->

# DeepReproduction

## 知识阶段环境配置

```bash
cd DeepReproduction/source
pdm install
```

## 知识阶段测试方法

当前最稳定的测试入口是：

```bash
pdm run python scripts/run_knowledge.py CVE-2022-28805 --dataset-root Dataset
```

如果外网访问依赖本地代理，使用：

```bash
HTTP_PROXY=http://127.0.0.1:7897 \
HTTPS_PROXY=http://127.0.0.1:7897 \
http_proxy=http://127.0.0.1:7897 \
https_proxy=http://127.0.0.1:7897 \
pdm run python scripts/run_knowledge.py CVE-2022-28805 --dataset-root Dataset
```

测试前如需清空旧产物，可删除对应 CVE 目录：

```bash
rm -rf Dataset/CVE-2022-28805
```

## 运行依赖

- 项目使用 `pdm` 管理依赖
- 运行前需要准备 `.env`
- 知识阶段相关的关键变量包括：
  - `KNOWLEDGE_AGENT_MODEL`
  - `KNOWLEDGE_AGENT_API_KEY`
  - `KNOWLEDGE_AGENT_BASE_URL`
  - `KNOWLEDGE_ENABLE_LLM_CURATION`
  - `KNOWLEDGE_MAX_REFERENCE_DEPTH`
  - `KNOWLEDGE_MAX_FETCH_COUNT`
  - `KNOWLEDGE_FETCH_TIMEOUT_SECONDS`
  - `LLM_TIMEOUT_SECONDS`

## 知识阶段产物位置

以 `CVE-2022-28805` 为例，产物会写到：

- `Dataset/CVE-2022-28805/vuln_yaml/task.yaml`
  - 任务基础信息
  - OSV 引导得到的 `repo_url`、`vulnerable_ref`、`fixed_ref`
  - `reference_details` 中保留了 OSV 的 `type`

- `Dataset/CVE-2022-28805/vuln_yaml/knowledge_sources.yaml`
  - 参考链接筛选结果
  - `seed_references`
  - `selected_references`
  - `skipped_references`
  - `reference_kind`

- `Dataset/CVE-2022-28805/vuln_yaml/knowledge.yaml`
  - 知识阶段最终结构化输出
  - `summary`
  - `vulnerability_type`
  - `affected_files`
  - `reproduction_hints`
  - `expected_error_patterns`
  - `expected_stack_keywords`

- `Dataset/CVE-2022-28805/vuln_yaml/runtime_state.yaml`
  - 阶段最终状态
  - `final_status`
  - `last_error`
  - `llm_status`
  - `llm_error`

- `Dataset/CVE-2022-28805/vuln_data/knowledge_sources/cleaned/`
  - 清洗后的网页和文本证据

- `Dataset/CVE-2022-28805/vuln_data/knowledge_sources/raw/`
  - 下载到本地的原始附件或补丁类文件

- `Dataset/CVE-2022-28805/vuln_data/knowledge_sources/extracted/`
  - 若抓到压缩包并解压，则内容在这里

- `Dataset/CVE-2022-28805/vuln_data/vuln_diffs/patch.diff`
  - 标准化保存的补丁 diff

- `Dataset/CVE-2022-28805/vuln_data/vuln_pocs/`
  - 如果模型识别出明确 PoC，会写到这里

## 如何判断测试成功

最直接的检查项：

1. 命令成功退出，并打印 `Knowledge stage completed`
2. `runtime_state.yaml` 中：
   - `final_status: success`
   - `last_error: null`
3. `task.yaml` 中：
   - `repo_url`、`vulnerable_ref`、`fixed_ref` 不为空
4. `knowledge_sources/cleaned/` 中：
   - 至少存在若干抓取后的清洗文件
5. `vuln_diffs/patch.diff`：
   - 文件非空
6. `knowledge.yaml`：
   - `summary` 不为空
   - `affected_files` 有值时说明补丁解析成功

## 如何判断大模型是否生效

查看：

- `Dataset/<CVE>/vuln_yaml/runtime_state.yaml`

重点字段：

- `llm_status: success`
  - 表示模型成功返回并被系统接受

- `llm_status: failed`
  - 表示模型调用失败，系统回退到规则化知识生成

- `llm_status: unexpected_response`
  - 表示模型返回了非预期 JSON

- `llm_status: disabled`
  - 表示当前关闭了知识阶段大模型整理

当 `llm_status: success` 时，`knowledge.yaml` 中通常会看到更紧凑的：

- `summary`
- `vulnerability_type`
- `reproduction_hints`
- `expected_error_patterns`

## 当前已验证能力

当前知识阶段已经验证可运行的能力包括：

- OSV 引导任务信息
- 保留 OSV `references[].type`
- `FIX` / `EVIDENCE` 参考链接按高优先级抓取
- 网页抓取与清洗
- GitHub commit 和 `.diff` 抓取
- 标准 `patch.diff` 落盘
- LLM JSON 输出解析
- LLM 状态显式记录
- LLM 辅助识别并落盘 PoC
