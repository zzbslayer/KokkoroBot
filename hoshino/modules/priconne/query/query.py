import itertools, re
from hoshino import util, R, CommandSession
from nonebot import permission as perm
from . import sv

tw_rank = R.img('priconne/quick/r16-4.jpg').cqcode
p4 = R.img('priconne/quick/r17-3-jp-1.png').cqcode
p5 = R.img('priconne/quick/r17-3-jp-2.png').cqcode
p6 = R.img('priconne/quick/r17-3-jp-3.png').cqcode

cn_rank = R.img('priconne/quick/r9-3.jpg').cqcode

@sv.on_rex(r'^(\*?([日台国b])服?([前中后]*)卫?)?rank(表|推荐|指南)?$', normalize=True)
async def rank_sheet(bot, ctx, match):
    is_jp = match.group(2) == '日'
    is_tw = match.group(2) == '台'
    is_cn = match.group(2) == '国' or match.group(2) == 'b'
    if not is_jp and not is_tw and not is_cn:
        await bot.send(ctx, '\n请问您要查询哪个服务器的rank表？\n*日rank表\n*台rank表\n*B服rank表\n', at_sender=True)
        return
    msg = [
        '\n※表格仅供参考，升r有风险，强化需谨慎',
    ]
    if is_jp:
        msg.append('※不定期搬运自图中群号\n※图中广告为原作者推广，与本bot无关\nR17-3 rank表：')
        pos = match.group(3)
        if not pos or '前' in pos:
            msg.append(str(p4))
        if not pos or '中' in pos:
            msg.append(str(p5))
        if not pos or '后' in pos:
            msg.append(str(p6))
        await bot.send(ctx, '\n'.join(msg), at_sender=True)
    elif is_tw:
        msg.append(str(tw_rank))
        await bot.send(ctx, '\n'.join(msg), at_sender=True)
    elif is_cn:
        msg.append(str(cn_rank))
        await bot.send(ctx, '\n'.join(msg), at_sender=True)

rank_pattern = r'^r[1-2]?[0-9]-[1-6]'
@sv.on_command('cn-rank-update', aliases=('国服rank更新', '国服RANK更新'), permission=perm.SUPERUSER, only_to_me=False)
async def rank_update(session):
    print(session.current_arg_text)
    args = session.current_arg_text.strip()
    rank = args[0]
    if re.match(rank_pattern, rank) == None:
        await session.send('※rank名称不符合规则\n※示例:r9-3')
        return
    global cn_rank
    cn_rank = R.img(f'priconne/quick/{rank}.jpg').cqcode
    await session.send(f'成功将rank更新为{rank}')

@sv.on_command('arena-database', aliases=('jjc', 'JJC', 'JJC作业', 'JJC作业网', 'JJC数据库', 'jjc作业', 'jjc作业网', 'jjc数据库', 'JJC作業', 'JJC作業網', 'JJC數據庫', 'jjc作業', 'jjc作業網', 'jjc數據庫'), only_to_me=False)
async def say_arina_database(session):
    await session.send('公主连接Re:Dive 竞技场编成数据库\n日文：https://nomae.net/arenadb \n中文：https://pcrdfans.com/battle')


OTHER_KEYWORDS = '【日rank】【台rank】【b服rank】【jjc作业网】【黄骑充电表】【一个顶俩】'
PCR_SITES = f'''
【繁中wiki/兰德索尔图书馆】pcredivewiki.tw
【日文wiki/GameWith】gamewith.jp/pricone-re
【日文wiki/AppMedia】appmedia.jp/priconne-redive
【竞技场作业库(中文)】pcrdfans.com/battle
【竞技场作业库(日文)】nomae.net/arenadb
【论坛/NGA社区】bbs.nga.cn/thread.php?fid=-10308342
【iOS实用工具/初音笔记】bbs.nga.cn/read.php?tid=14878762
【安卓实用工具/静流笔记】bbs.nga.cn/read.php?tid=20499613
【台服卡池千里眼】bbs.nga.cn/read.php?tid=16986067
【日官网】priconne-redive.jp
【台官网】www.princessconnect.so-net.tw

===其他查询关键词===
{OTHER_KEYWORDS}
※B服速查请输入【bcr速查】'''

BCR_SITES = f'''
【妈宝骑士攻略(懒人攻略合集)】bbs.nga.cn/read.php?tid=20980776
【机制详解】bbs.nga.cn/read.php?tid=19104807
【初始推荐】bbs.nga.cn/read.php?tid=20789582
【术语黑话】bbs.nga.cn/read.php?tid=18422680
【角色点评】bbs.nga.cn/read.php?tid=20804052
【秘石规划】bbs.nga.cn/read.php?tid=20101864
【卡池亿里眼】bbs.nga.cn/read.php?tid=20816796
【为何卡R卡星】bbs.nga.cn/read.php?tid=20732035
【推图阵容推荐】bbs.nga.cn/read.php?tid=21010038

===其他查询关键词===
{OTHER_KEYWORDS}
※日台服速查请输入【pcr速查】'''

@sv.on_command('pcr-sites', aliases=('pcr速查', 'pcr图书馆', 'pcr圖書館', '图书馆', '圖書館'))
async def pcr_sites(session:CommandSession):
    await session.send(PCR_SITES, at_sender=True)
@sv.on_command('bcr-sites', aliases=('bcr速查', 'bcr攻略'))
async def bcr_sites(session:CommandSession):
    await session.send(BCR_SITES, at_sender=True)


YUKARI_SHEET_ALIAS = map(lambda x: ''.join(x), itertools.product(('黄骑', '酒鬼', '黃騎'), ('充电', '充电表', '充能', '充能表')))
YUKARI_SHEET = f'''
{R.img('priconne/quick/黄骑充电.jpg').cqcode}
※大圈是1动充电对象 PvP测试
※黄骑四号位例外较多
※对面羊驼或中后卫坦 有可能歪
※我方羊驼算一号位
※图片搬运自漪夢奈特'''
@sv.on_command('yukari-sheet', aliases=YUKARI_SHEET_ALIAS)
async def yukari_sheet(session:CommandSession):
    await session.send(YUKARI_SHEET, at_sender=True)


DRAGON_TOOL = f'''
拼音对照表：{R.img('priconne/KyaruMiniGame/注音文字.jpg').cqcode}{R.img('priconne/KyaruMiniGame/接龙.jpg').cqcode}
龍的探索者們小遊戲單字表 https://hanshino.nctu.me/online/KyaruMiniGame
镜像 https://hoshino.monster/KyaruMiniGame
网站内有全词条和搜索，或需科学上网'''
@sv.on_command('拼音接龙', aliases=('一个顶俩', '韵母接龙'))
async def dragon(session:CommandSession):
    await session.send(DRAGON_TOOL, at_sender=True)

NORMAL_MAP_PREFIX='刷图指南'
@sv.on_command('刷图指南', aliases=('刷图', '刷装备', '装备掉落', '刷图攻略'))
async def normal_map(session:CommandSession):
    try:
        number = int(session.current_arg_text)
    except Exception as e:
        await session.send('参数必须为数字。示例：`刷图 10`')
        return
    img = f'{NORMAL_MAP_PREFIX}-{number}.jpg'
    img = R.img(f'priconne/quick/{img}')
    if not img.exist:
        await session.send(f'{number} 图刷图攻略未找到呜呜呜 ┭┮﹏┭┮')
    else:
        await session.send(f'{number} 图刷图攻略：{img.cqcode}')


    
