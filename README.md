# 0720
Content: 本次上传代码文件main_0720.py与示例输出google_ai_overview_timeline_full.csv。后者最后一行No AI Overview因为本号今日也已超过limit。但上午测试时稳定运行。

Purpose: 本次代码修改成功实现根据读取csv文件中的sysname列后，在搜索框中搜索'Summarize {sysname} AI Adoption time'并提取AI Overview答案。

Problems: 爬虫不会引起谷歌封号，但目前遇到的最大问题是单个账号问询次数过多后，生成AI Overview（以下简称AO）的概率会大幅缩小。使得稳定的脚本变得不稳定。

What's Next:下次任务重点：1.探索单个账号产生稳定AO的最大问询次数。2.探索除不同地区的显示频率外的其他不稳定因素。完善该脚本让不稳定变稳定。4.拆分Summary文本使按年份分行。
