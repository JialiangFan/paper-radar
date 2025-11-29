#!/bin/bash
# 定时任务启动脚本

# 激活 conda 环境
source $(conda info --base)/etc/profile.d/conda.sh
conda activate paper_agent

# 进入项目目录
cd "$(dirname "$0")"

# 启动定时任务
python research_agent.py schedule

