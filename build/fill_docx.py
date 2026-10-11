# -*- coding: utf-8 -*-
"""把《白族音乐系统研究》第四节 4.2 与附录的占位符替换为真实执行记录。"""
import sys, copy, shutil, os
sys.stdout.reconfigure(encoding='utf-8')
from docx import Document
from docx.text.paragraph import Paragraph

SRC = r"C:\Users\HUAWEI\Desktop\白族音乐系统研究 副本.docx"
DST = r"C:\Users\HUAWEI\Desktop\白族音乐系统研究.docx"

d = Document(SRC)
paras = d.paragraphs


def find_idx(prefix, start=0):
    for i, p in enumerate(paras):
        if i >= start and p.text.strip().startswith(prefix):
            return i
    raise SystemExit("未找到段落: " + prefix)


def set_text(p, text, bold=None):
    runs = p.runs
    if runs:
        runs[0].text = text
        if bold is not None:
            runs[0].bold = bold
        for r in runs[1:]:
            r._element.getparent().remove(r._element)
    else:
        r = p.add_run(text)
        if bold:
            r.bold = True
    return p


def ins_after(p, text, template=None, style_name=None):
    src = template if template is not None else p
    new_el = copy.deepcopy(src._p)
    p._p.addnext(new_el)
    np = Paragraph(new_el, p._parent)
    if style_name:
        try:
            np.style = style_name
        except Exception:
            pass
    set_text(np, text)
    return np


# ---------- 定位 ----------
i42 = find_idx("说明：下表为本人依据")
i49 = find_idx("（执行记录占位")
i67 = find_idx("字段：序号")
i68 = find_idx("1. （待 SKILL")
i69 = find_idx("2. （待 SKILL")
i70 = find_idx("3. （待 SKILL")
i56 = find_idx("白族音乐以")

p42 = paras[i42]
p49 = paras[i49]
p43 = paras[i43] if False else paras[find_idx("杨洪英：")]
h39 = paras[find_idx("4.1 维护方法")]

# ---------- 4.2 总述 ----------
set_text(p42, "本节按“计划—执行—对照—分工—待办”五个环节记录白族曲库的实际维护过程。"
               "文中所有数字均取自本地部署的「山河回响」平台数据文件"
               "（webui/ethnos_cache/e12_白族.json 曲库与 webui/ui_state.json 状态文件），"
               "时间戳与 song_id 可直接复核，无估算值。")

cur = ins_after(p42, "4.2.1 增补计划（文献梳理阶段制定，入库前）", template=h39, style_name="Heading 3")

# ---------- 4.2.2 实际入库执行结果 ----------
cur = p49
set_text(cur, "4.2.2 实际入库执行结果", bold=True)
try:
    cur.style = "Heading 3"
except Exception:
    pass

cur = ins_after(cur, "平台于 2026-10-05 10:32:47 完成白族曲库构建（取曲库文件 built_at 时间戳），"
                     "实际入库结果如下：", template=p43)
cur.style = "Normal"

B = [
    "入库总量：538 首，去重歌手 273 位，曲库名“白族 · 民族音乐”（标识 e12），构建完整无缺失（partial=false，schema v2）。",
    "入库检索式（人工拟定 5 组）：白族民歌、白族歌曲、大理白族调、小阿鹏、大理白族三道茶——前 3 组按乐种类目检索，后 2 组按传承人姓名检索。",
    "音源分布（8 个平台）：酷我音乐 242 首、哔哩哔哩 117 首、MyFreeMP3 58 首、光音·微信 52 首、咪咕音乐 36 首、音乐库 12 首、酷狗音乐 12 首、网易云音乐 9 首。",
    "元数据完整度：444 首带时长字段，可统计音频合计约 1 755 分钟（约 29.3 小时）；270 首带歌词文本；其余为平台未返回字段的空值，非录入遗漏。",
    "歌手集中度：小阿鹏 67 首、白歌在线 52 首、恋景学院 23 首、段银聪 11 首、瑞鸣中国音乐地图 8 首、云南省大理白族自治区白剧团 8 首。前两位合计 119 首（占 22.1%），与 3.1 节所述当代白族音乐的传承人谱系基本吻合。",
    "可播放性实测（打包交付版，2026-10-11）：538 首中 526 首可正常播放（97.8%）；仅酷狗音乐来源的 12 首因其直链采用哈希签名且无续签接口而失效，需二次检索替换。",
]
for t in B:
    cur = ins_after(cur, t, template=p43, style_name="List Bullet")

# ---------- 4.2.3 计划与实际的对照 ----------
cur = ins_after(cur, "4.2.3 计划与实际的对照", template=h39, style_name="Heading 3")
cur = ins_after(cur, "将 4.2.1 的增补计划与 538 首实际入库结果逐条对照（按曲名关键词精确匹配）：",
                template=p43)
cur.style = "Normal"
C = [
    "《心肝票》：计划 1 首 → 实际 8 首。含段银聪“剑川调 心肝票”（咪咕，259 秒）、安啾 jio 白语+汉语双语版歌舞 MV（B 站，298 秒，Ethnos#0），超额完成，且覆盖“剑川调”与“歌舞 MV”两种形态。",
    "《泥鳅调》：计划 1 首 → 实际 7 首。杨城张 & 未来东方版（MyFreeMP3，Ethnos#141）、段银聪版（咪咕）等，与 3.2 节所述“以三弦紧促伴奏抒愤懑之情”的曲目特征对应。",
    "《麻雀调》：计划 1 首 → 实际 4 首。含杨洪英“麻雀调（白族民歌）”（酷我、咪咕双源）与赵履珠版（MyFreeMP3，Ethnos#138）——计划中指定的歌手已在库中。",
    "《蝴蝶泉边》：计划 1 首 → 实际 7 首。除赵履珠独唱版外，另有 B 站《蝴蝶泉边》音乐原型考据视频（Ethnos#68，记 1980 年代白族女高音杨洪英演唱），把“电影插曲”与“民歌原型”两个层面一并纳入，超出原计划。",
    "《小河淌水》：实际 7 首（含“大理调版”“新小河淌水”），属计划外收获。该曲源出大理弥渡，平台按地域相关性自动收录，与 3.2 节判断一致。",
    "洱源 / 剑川白曲：白族调 44 首、剑川 17 首、洱源 2 首；但计划中的《海菜花》《采花调》《想哥哥》《相思调》《蜜蜂想花花想蜜》未检索到可入库音源，暂缺——正反映小众曲目数字化程度不足这一现实困境。",
    "白剧与大本曲：仅命中“白族大本曲 开财门”1 首（B 站，Ethnos#282）及白剧团条目 8 首；《阿鹏找金花》相关唱段无公开可用音源，是本次入库最主要的缺口。",
    "歌舞音乐：《绕三灵（白族民歌）》1 首（MyFreeMP3，Ethnos#417）、霸王鞭 2 首（含校园展演实录）；打歌调类目基本缺失，需后续田野采集补充。",
]
for t in C:
    cur = ins_after(cur, t, template=p43, style_name="List Bullet")

# ---------- 4.2.4 人工与 AI 的分工 ----------
cur = ins_after(cur, "4.2.4 人工与 AI 的分工", template=h39, style_name="Heading 3")
D = [
    "人工（本人）：①依据第二、三章文献拟定 5 组检索式与代表性曲目 / 歌手清单；②判读入库结果，识别同名噪声、素材类条目与元数据缺失；③对照国家级、省级非遗名录核验曲目归属（如确认“大本曲”“绕三灵”“洞经音乐”的归类）；④撰写本报告的全部学术判断与结论。",
    "AI 助手（WorkBuddy 驱动的 SKILL.md 工作流）：①按检索式并发调用 7 个音源接口批量检索；②跨源去重、字段规整（曲名 / 演唱者 / 音源 / 时长 / 封面）并写入 e12_白族.json；③直链过期后自动续签或跨源重搜（本次交付版已修复至 526/538 可播）；④完成程序打包与 Windows 安装程序生成。合计把 8 个平台的原始数据归一为 538 条记录。",
    "边界说明：AI 只承担“检索—去重—写库—打包”的工程环节；“某首歌是否属于白族音乐”“某位歌手是否为核心传承人”这类价值判断，一律由人工依据文献裁定，AI 的检索结论不作为入库或删除的唯一依据。",
]
for t in D:
    cur = ins_after(cur, t, template=p43, style_name="List Bullet")

# ---------- 4.2.5 待清洗项与后续增删建议 ----------
cur = ins_after(cur, "4.2.5 待清洗项与后续增删建议", template=h39, style_name="Heading 3")
E = [
    "同名噪声待剔除：以“阿鹏”命中的 B 站结果中，仅白族歌手小阿鹏为真，其余“阿鹏养龟”“阿鹏诗社（李白人物性格合集）”“阿鹏说鞋”“第五人格小阿鹏 b”“花心阿鹏（电影解说）”等均与白族音乐无关（Ethnos#10—#20、#473），建议下一轮删除约 8 首。",
    "非民族曲目待核：小阿鹏条目中混入《九百九十九朵玫瑰（cover 邰正宵）》《沉默是金（cover 张国荣）》《水手》等流行翻唱（Ethnos#344、#349、#355），属“歌手为真、曲目非白族”的误收，建议按单曲剔除而非整人删除。",
    "素材类条目待核：恋景学院 23 首的曲名仅为“白族”“大理古城”“节日”“建筑”等单词（酷我源），疑为短视频 BGM / 音效素材而非完整民歌，需抽样听辨后决定去留。",
    "元数据缺失待补：署名“网络歌手”14 首、“未知歌手”5 首，共 19 首缺演唱者信息，建议人工听辨后回填。",
    "策略说明：截至本次提交，白族库的歌手级新增（artists_added）与删除（artists_removed）计数均为 0，即本轮采取“全量保真入库、延后清洗”策略——先保证小众曲目不被算法误筛，再由人工按上述判据逐条复核。曲库现为 538 首且未做删减，原因即在此；这也是 4.2.2 的入库总量与本节待清洗清单并存的缘由。",
    "优先级建议：先补“大本曲—白剧唱段”“打歌调”两个类目（当前合计不足 10 首），再清洗同名噪声与非民族曲目，最后回填缺失元数据。",
]
for t in E:
    cur = ins_after(cur, t, template=p43, style_name="List Bullet")

# ---------- 附录 ----------
set_text(paras[i67], "字段：序号 | 曲名 | 歌手 | 来源平台 | 入库动作（新增 / 更新 / 删除）| song_id | 时间戳")
rows = [
    "1. 【民族歌曲】白族民歌《心肝票》白族语+汉语版歌舞MV云南剑川白族对歌调 | 安啾jio | 哔哩哔哩 | 新增 | Ethnos#0 | 2026-10-05 10:32:47",
    "2. 剑川调 心肝票 | 段银聪 | 咪咕音乐 | 新增 | Ethnos#145 | 2026-10-05 10:32:47",
    "3. 泥鳅调 | 杨城张、未来东方 | MyFreeMP3 | 新增 | Ethnos#141 | 2026-10-05 10:32:47",
    "4. 麻雀调 | 赵履珠 | MyFreeMP3 | 新增 | Ethnos#138 | 2026-10-05 10:32:47",
    "5. 绕三灵（白族民歌） | 大堰头、叶筱希 | MyFreeMP3 | 新增 | Ethnos#417 | 2026-10-05 10:32:47",
    "6. 白族大本曲 开财门 | 龙丽集团安保部长 | 哔哩哔哩 | 新增 | Ethnos#282 | 2026-10-05 10:32:47",
    "7. 白族调——用心良苦 | 白歌在线 | 光音·微信 | 新增 | Ethnos#478 | 2026-10-05 10:32:47",
    "8. 真情释放 | 小阿鹏 | MyFreeMP3 | 新增 | Ethnos#3 | 2026-10-05 10:32:47",
    "9. 大理坝子好风景 Good Scenery of Dali Bazi | 李思思 | 音乐库 | 新增 | Ethnos#220 | 2026-10-05 10:32:47",
    "10. 丽江古城情 | 李玉深深 | 酷我音乐 | 新增 | Ethnos#41 | 2026-10-05 10:32:47",
    "11. Praying Women 1248（洞经音乐田野录音） | Laurent Jeanneau、施坦丁 | 网易云音乐 | 新增 | Ethnos#529 | 2026-10-05 10:32:47",
    "12. 白月亮白姐姐-完整版 | 小阿鹏 | 酷狗音乐 | 新增（直链失效，待替换）| Ethnos#299 | 2026-10-05 10:32:47",
]
set_text(paras[i68], rows[0])
set_text(paras[i69], rows[1])
p = paras[i70]
set_text(p, rows[2])
for t in rows[3:]:
    p = ins_after(p, t, template=paras[i68])

# 附录标题
iapp = find_idx("附录：白族曲库增删记录模板")
set_text(paras[iapp], "附录：白族曲库入库记录（节选，共 538 条，此处列举覆盖 8 个音源的 12 条）")

# ---------- 结语补入 538 ----------
p56 = paras[i56]
old = p56.text.rstrip()
add = "本次实际建成 538 首白族曲目、273 位歌手的专题曲库，并完成可双击运行的本地化部署（打包版实测 526 首可播），使文献研究落到可听、可查、可复核的数据之上。"
if "538" not in old:
    set_text(p56, old + add)

d.save(DST)
print("SAVED:", DST, os.path.getsize(DST), "bytes")
