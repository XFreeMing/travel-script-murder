# 第一幕0.2.1原型与检查记录

记录日期：2026-10-13（北京时间）。当前状态见[TODO](../TODO.md)。本轮响应“细化第一幕，包括孩子和家长的角色卡、线索卡和主持引导，看看一家人怎样玩”的要求。

## 已交付内容

- [第一幕主持说明](../pilots/dongfang-weicheng-act1.md)：准备与发卡、四步话语、答案与判定、提示分级、抢答与人数处理、提前追问、虚构设计示例及反馈问题。
- [卡片文稿](../pilots/dongfang-weicheng-act1-cards.md)：两张角色卡、公共委托、家长文字联与收件条、儿童图签、三屋图及制图定义。此文稿供共创，不能整页发给玩家。
- [三页A4玩家包](../../output/pdf/dongfang-weicheng-act1-cards.pdf)：第1页两张角色卡，第2页两份线索分开裁切，第3页公共委托与屋图。
- [空白观察表](../pilots/dongfang-weicheng-act1-feedback.md)：真实行为、提示、先报答案、原因提前披露、用时与下一次改动。
- 卡片生成文件位于 `scripts/build_act1_cards.py`。卡面文字和房屋条件从卡片文稿读取；重建后须重新渲染并检查。

版本仍依托0.2架构，未改主线。0.1独立小样与原图卡保留，不混入新版。故事中的迎归灯统一用三条波纹标记，门上星星只表示存放位置，避免把两类信息混淆。

## 文本与运行检查

- 独立审查角色参与和可试带性：未发现本轮必须修正的问题，非作者可从材料表、四步流程与答疑确定发卡和推进方式。
- 独立审查玩家视角：圆窗单独留下左/右，两星单独留下中/右，交集唯一为右屋；来源和物件对应已说明。默认卡面不透露修棚与防雨。
- 提前追问可获得可靠记录；玩家坚持直接问位置时可提供答案，但只记录后续核验，不计作独立定位。成人抢答后的儿童核验同样分开记录。
- 两孩、两成人均在本幕内分配行动，不只依赖未来换岗。家长兼主持的已知答案状态须单独记录。
- 示例明示为虚构演示；观察表为空白。没有填入家庭实测数据。

## PDF生成与视觉检查

工作目录：`C:\Users\xiaof\workspace\travel-script-murder`。使用已配置的PDF技能和本地依赖，生成前已成功执行一次artifact操作标记；未安装新依赖。

生成命令：

```powershell
& 'C:/Users/xiaof/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'scripts/build_act1_cards.py'
```

渲染与检查命令：

```powershell
New-Item -ItemType Directory -Path 'tmp/pdfs/act1-review' -Force | Out-Null
& 'C:/Users/xiaof/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe' -r 110 -png 'output/pdf/dongfang-weicheng-act1-cards.pdf' 'tmp/pdfs/act1-review/card'
& 'C:/Users/xiaof/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdfinfo.exe' 'output/pdf/dongfang-weicheng-act1-cards.pdf'
```

结果：PDF为3页A4，文字可提取，嵌入中文字体。生成时检查角色页不含定位答案、默认卡面不含搬运原因，均通过；这只检查内容边界，不证明玩家是否理解。

本次交付PDF的SHA256：`93FAEC19D5D0D49786B5A0931EB689ABCFC8889B3B7C4F072AFE69D3312C659C`。后续重建可能改变文件摘要，应重新记录验证版本。

逐页渲染已目视检查：中文完整，无文字截断、重叠或缺字；裁切线与页码清楚；两份线索分开；三间屋子等大同色、窗形与星数正确，无房号或答案高亮；波纹灯标记一致。图案依靠形状和数量，未将颜色作为必要线索。尚未做真实纸张打印或家庭阅读验证。

保留本次渲染证据：[角色页](evidence/2026-10-13-act1/card-1.png)、[线索页](evidence/2026-10-13-act1/card-2.png)、[共用图页](evidence/2026-10-13-act1/card-3.png)。临时PNG已移除，证据副本保留在归档目录。

## 交付前检查与后续

- 13份Markdown中的75处本地链接全部存在，包含PDF、空白观察表及3张渲染证据。
- `git diff --check` 通过；已知的换行转换提示不影响本轮内容检查。新增文件另行读取与渲染检查。
- 重新读取PDF资源确认中文TrueType字体已嵌入；最终文件与3张归档预览均存在。
- README、整体架构与TODO已链接第一幕原型；当前状态明确区分“材料已制作”和“家庭尚未试玩”。既有小样与研究未删除。

本轮没有持续运行任务、软件部署或景区操作。

下一步由真实家庭试玩第一幕，按行为改一个主要问题并复测。第二、三幕完整材料与真实场地适配仍未完成。若家庭觉得像练习题，优先研究情境行动和反馈，不因答对就直接增加题目或宣布成功。
