#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 八字排盘 v1.4 — 身强弱判定+喜用+流年流月+地支关系
import sys; from datetime import date, datetime

HE='甲乙丙丁戊己庚辛壬癸'; EB='子丑寅卯辰巳午未申酉戌亥'
TERMS=[(2,4,'寅'),(3,6,'卯'),(4,5,'辰'),(5,6,'巳'),(6,6,'午'),(7,7,'未'),
       (8,7,'申'),(9,8,'酉'),(10,8,'戌'),(11,7,'亥'),(12,7,'子'),(1,6,'丑')]
TIGER={'甲':'丙','乙':'戊','丙':'庚','丁':'壬','戊':'甲','己':'丙','庚':'戊','辛':'庚','壬':'壬','癸':'甲'}
RAT={'甲':'甲','乙':'丙','丙':'戊','丁':'庚','戊':'壬','己':'甲','庚':'丙','辛':'戊','壬':'庚','癸':'壬'}
CG={'子':'癸','丑':'己癸辛','寅':'甲丙戊','卯':'乙','辰':'戊乙癸','巳':'丙庚戊','午':'丁己','未':'己丁乙','申':'庚壬戊','酉':'辛','戌':'戊辛丁','亥':'壬甲'}
WX={'甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水'}
KE={'木':'土','土':'水','水':'火','火':'金','金':'木'}; SH={'木':'火','火':'土','土':'金','金':'水','水':'木'}
# 地支关系
LIUHE={'子':'丑','丑':'子','寅':'亥','卯':'戌','辰':'酉','巳':'申','午':'未','未':'午','申':'巳','酉':'辰','戌':'卯','亥':'寅'}
SANHE={'申子辰':'水','亥卯未':'木','寅午戌':'火','巳酉丑':'金'}
CHONG={'子':'午','丑':'未','寅':'申','卯':'酉','辰':'戌','巳':'亥','午':'子','未':'丑','申':'寅','酉':'卯','戌':'辰','亥':'巳'}
HAI={'子':'未','丑':'午','寅':'巳','卯':'辰','申':'亥','酉':'戌','巳':'寅','午':'丑','未':'子','辰':'卯','戌':'酉','亥':'申'}
XING={'寅巳申':'无恩之刑','丑戌未':'恃势之刑','子卯':'无礼之刑','辰午酉亥':'自刑'}
BANHE={'申子':'水','亥卯':'木','寅午':'火','巳酉':'金','子辰':'水','卯未':'木','午戌':'火','酉丑':'金'}

def month_zhi(y,m,d):
    if m==1 and d<6: return '子'
    for i,(tm,tj,tz) in enumerate(TERMS):
        if (m==tm and d>=tj) or (m>tm and not tm==1): continue
        return TERMS[(i-1)%12][2]
    return TERMS[-1][2]

def fx(i,m=12): return((i%m)+m)%m

def calc(sd,ti,gender):
    y,m,d=sd.year,sd.month,sd.day
    if ti==12:
        sd2=date.fromordinal(sd.toordinal()+1)
        dt2=(sd2-date(2000,1,1)).days; dg=HE[(4+dt2)%10]; dz=EB[(6+dt2)%12]
    else:
        dt=(sd-date(2000,1,1)).days; dg=HE[(4+dt)%10]; dz=EB[(6+dt)%12]
    yy=y-1 if m<2 or(m==2 and d<4)else y
    yg_idx=(yy-4)%10; yz_idx=(yy-4)%12
    yg=HE[yg_idx]; yz=EB[yz_idx]
    mz_n=month_zhi(y,m,d); mz=EB.index(mz_n)
    yg2=TIGER[yg]; mg=HE[(HE.index(yg2)+mz-2)%10]
    hour_dg=dg
    hg=HE[(HE.index(RAT[hour_dg])+ti)%10]; hz=EB[ti%12]
    rw=WX[dg]
    def ss(g):
        tw=WX[g]; ryy=dg in'甲丙戊庚壬'; tyy=g in'甲丙戊庚壬'
        if rw==tw: return '比肩' if ryy==tyy else '劫财'
        elif KE[rw]==tw: return '偏财' if ryy==tyy else '正财'
        elif KE[tw]==rw: return '七杀' if ryy==tyy else '正官'
        elif SH[rw]==tw: return '食神' if ryy==tyy else '伤官'
        return '偏印' if ryy==tyy else '正印'
    yinyang=0 if yg in'甲丙戊庚壬' else 1
    male=1 if gender=='男' else 0
    shun=(yinyang==0 and male==1) or (yinyang==1 and male==0)
    mgi=HE.index(mg); mzi=EB.index(mz_n); dayuns=[]
    for i in range(8):
        di=i+1 if shun else -(i+1); dayuns.append(HE[(mgi+di)%10]+EB[(mzi+di)%12])
    days=365
    if shun:
        next_ck=None
        for tm,tj,_ in TERMS:
            yr=y+1 if tm==1 and (m>tm or (m==tm and d>=tj)) else y
            ck=date(yr,tm,tj)
            if ck>sd and (next_ck is None or ck<next_ck): next_ck=ck
        if next_ck: days=(next_ck-sd).days
    else:
        prev_ck=None
        for i in range(len(TERMS)-1,-1,-1):
            tm,tj,_=TERMS[i]; yr=y-1 if m<tm or (m==tm and d<tj) else y
            ck=date(yr,tm,tj)
            if ck<sd and (prev_ck is None or ck>prev_ck): prev_ck=ck
        if prev_ck: days=(sd-prev_ck).days
    sa=max(1,days//3)
    five={n:0 for n in'木火土金水'}
    for s in[yg,mg,dg,hg]: five[WX[s]]+=1
    for b in[yz,EB[mz],dz,hz]:
        for c in CG[b]: five[WX[c]]+=0.5
    # 所有十神(含日支藏干)
    all_ss=[]
    for g in[yg,mg,hg]: all_ss.append(ss(g))
    # 地支十神(取藏干主气)
    for b in[yz,mz_n,dz,hz]:
        c=CG[b][0]; all_ss.append(ss(c))
    return{'y':(yg,yz),'m':(mg,mz_n),'d':(dg,dz),'h':(hg,hz),
           'ss':[ss(yg),ss(mg),ss(dg),ss(hg)],'all_ss':all_ss,
           'dy':dayuns,'sa':sa,'shun':shun,'f':five,'dg':dg,
           'dw':WX[dg],'sd':sd,'ti':ti,'gender':gender}

def strength(b):
    """自动判定身强弱: 强/中强/中和/中弱/弱"""
    dw=b['dw']; five=b['f']; dg=b['dg']
    yg,yz=b['y']; mg,mz=b['m']; dg,dz=b['d']; hg,hz=b['h']
    lm={'木':['寅','卯'],'火':['巳','午'],'金':['申','酉'],'水':['亥','子'],'土':['辰','戌','丑','未']}
    ling=mz in lm[dw]
    dc=sum(1 for bb in[yz,mz,dz,hz] for c in CG[bb] if WX.get(c)==dw)
    sc=sum(1 for s in[yg,mg,hg] if WX[s]==dw)
    score=five[dw]
    # 综合评分
    total=score*2 + (2 if ling else 0) + dc*1.5 + sc*2
    ke_ele=KE[dw]  # 克日主的五行
    sheng_ele=SH[dw]  # 日主生的五行
    sheng_w=SH[SH[dw]] if SH[SH[dw]]!=dw else None  # 生我的五行(印)
    op_score=five[ke_ele]*1.5  # 克我的力量
    if total>=10: return '强'
    elif total>=7.5: return '中强'
    elif total>=5: return '中和'
    elif total>=3: return '中弱'
    else: return '弱'

def xiyong(b):
    """判定喜用神和忌神"""
    s=strength(b); dw=b['dw']; five=b['f']
    # ke_w: 克日主的官杀 (如火克金)
    # cai_w: 日主克的财 (如金克木)
    # xie_w: 日主生的食伤 (如金生水)
    # sheng_w: 生日主的印 (如土生金)
    sheng_w=None; ke_w=None
    for w in'木火土金水':
        if SH[w]==dw: sheng_w=w
        if KE[w]==dw: ke_w=w
    cai_w=KE[dw]   # 日主克
    xie_w=SH[dw]   # 日主生

    if s in('强','中强'):
        xi=[ke_w,xie_w,cai_w]
        ji=[dw,sheng_w]
    elif s in('弱','中弱'):
        xi=[sheng_w,dw]
        ji=[ke_w,xie_w,cai_w]
    else:
        xi=[]; ji=[]
        for w in'木火土金水':
            if five[w]>2.5: ji.append(w)
            elif five[w]<1.2: xi.append(w)
    # 去重
    xi=list(dict.fromkeys([x for x in xi if x]))
    ji=list(dict.fromkeys([x for x in ji if x]))
    return xi,ji,s

def dizhi_rels(zhis,labels=None):
    """分析四个地支之间的关系"""
    if labels is None: labels=['年支','月支','日支','时支']
    rels=[]
    for i in range(4):
        for j in range(i+1,4):
            r=[]
            a,b=zhis[i],zhis[j]
            if LIUHE.get(a)==b: r.append('六合')
            if CHONG.get(a)==b: r.append('冲')
            if HAI.get(a)==b: r.append('害')
            for k,v in SANHE.items():
                if a in k and b in k:
                    if all(x in zhis for x in k):
                        r.append(f'三合({v})')
                    else:
                        r.append(f'半合({v})')
            # 刑
            for k,v in XING.items():
                if a in k and b in k and a!=b:
                    r.append(v)
            if r:
                rels.append(f"  {labels[i]}{a} ↔ {labels[j]}{b}: {', '.join(r)}")
    return rels

def liunian(b,year):
    """分析某一流年与原局的交互"""
    # 流年干支
    yg_idx=(year-4)%10; yz_idx=(year-4)%12
    lyg=HE[yg_idx]; lyz=EB[yz_idx]
    gw=WX[lyg]; dw=b['dw']

    # 十神
    rw=WX[b['dg']]
    def ss(g):
        tw=WX[g]; ryy=b['dg'] in'甲丙戊庚壬'; tyy=g in'甲丙戊庚壬'
        if rw==tw: return '比肩' if ryy==tyy else '劫财'
        elif KE[rw]==tw: return '偏财' if ryy==tyy else '正财'
        elif KE[tw]==rw: return '七杀' if ryy==tyy else '正官'
        elif SH[rw]==tw: return '食神' if ryy==tyy else '伤官'
        return '偏印' if ryy==tyy else '正印'

    effects=[]
    lyname=ss(lyg)
    xi,ji,_=xiyong(b)
    se='喜' if gw in xi else ('忌' if gw in ji else '')
    if lyname in('七杀','正官'): effects.append(f'{lyname}克身⚠')
    elif lyname in('正印','偏印'): effects.append(f'{lyname}生身✓')
    elif lyname in('比肩','劫财'): effects.append(f'{lyname}帮身✓')
    elif lyname in('食神','伤官'): effects.append(f'{lyname}泄秀')
    elif lyname in('正财','偏财'): effects.append(f'{lyname}求财')

    # 流年地支与命局关系
    zhis=[b['y'][1],b['m'][1],b['d'][1],b['h'][1]]
    for i,z in enumerate(zhis):
        if CHONG.get(lyz)==z: effects.append(f'冲{["年","月","日","时"][i]}支{z}')
        if lyz==z: effects.append(f'伏吟{["年","月","日","时"][i]}支')
        if HAI.get(lyz)==z: effects.append(f'害{["年","月","日","时"][i]}支')
        if LIUHE.get(lyz)==z: effects.append(f'合{["年","月","日","时"][i]}支')

    # 与大运交互
    sa=b['sa']; age=year-b['sd'].year
    dy_idx=min((age-sa)//10,7)
    if dy_idx>=0:
        dy=b['dy'][dy_idx]
        if CHONG.get(lyz)==dy[1]: effects.append(f'冲大运{dy}')

    strength_effect=''
    xi,ji,_=xiyong(b)
    if gw in xi: strength_effect='喜'
    elif gw in ji: strength_effect='忌'

    return {'yg':lyg,'yz':lyz,'ss':ss(lyg),'effects':effects,'se':strength_effect}

def liumonth(b,year):
    """分析某年12个流月"""
    yg_idx=(year-4)%10
    lyg=HE[yg_idx]
    months=[]
    for i in range(12):
        mz=EB[(i+2)%12]  # 寅=2,卯=3...
        mg=HE[(HE.index(TIGER[lyg])+i)%10]
        months.append((mg,mz))
    return months

# ---- 显示函数 ----
def show(b):
    yg,yz=b['y']; mg,mz=b['m']; dg,dz=b['d']; hg,hz=b['h']; gs=b['ss']
    print(f"\n{'='*60}\n八字: {yg}{yz} {mg}{mz} {dg}{dz} {hg}{hz}\n{'='*60}")
    print(f"{'':<6}{'年柱':<11}{'月柱':<11}{'日柱':<11}{'时柱'}")
    print(f"{'天干':<6}{yg+'('+gs[0]+')':<11}{mg+'('+gs[1]+')':<11}{dg+'(日主)':<11}{hg+'('+gs[3]+')'}")
    # 地支十神(主气)
    dz_ss=[]
    for bz in[yz,mz,dz,hz]:
        c=CG[bz][0]
        rw=WX[dg]; tw=WX[c]; ryy=dg in'甲丙戊庚壬'; tyy=c in'甲丙戊庚壬'
        if rw==tw: dz_ss.append('比肩' if ryy==tyy else '劫财')
        elif KE[rw]==tw: dz_ss.append('偏财' if ryy==tyy else '正财')
        elif KE[tw]==rw: dz_ss.append('七杀' if ryy==tyy else '正官')
        elif SH[rw]==tw: dz_ss.append('食神' if ryy==tyy else '伤官')
        else: dz_ss.append('偏印' if ryy==tyy else '正印')
    print(f"{'地支':<6}{yz+'('+dz_ss[0]+')':<11}{mz+'('+dz_ss[1]+')':<11}{dz+'('+dz_ss[2]+')':<11}{hz+'('+dz_ss[3]+')'}")
    print(f"{'藏干':<6}{CG[yz]:<11}{CG[mz]:<11}{CG[dz]:<11}{CG[hz]}")
    print(f"\n五行:")
    for n in'木火土金水': print(f"  {n}: {b['f'][n]:.1f}")
    dw=b['dw']; lm={'木':['寅','卯'],'火':['巳','午'],'金':['申','酉'],'水':['亥','子'],'土':['辰','戌','丑','未']}
    ling=mz in lm[dw]
    dc=sum(1 for bb in[yz,mz,dz,hz] for c in CG[bb] if WX.get(c)==dw)
    sc=sum(1 for s in[yg,mg,hg] if WX[s]==dw)
    s=strength(b); xi,ji,_=xiyong(b)
    print(f"\n日主: {dg}({dw}) 得令:{'✓'if ling else'✗'} 得地:{dc} 得势:{sc}")
    print(f"身强弱: {s}  |  喜: {'、'.join(xi)}  |  忌: {'、'.join(ji)}")
    print(f"\n大运({'顺'if b['shun']else'逆'},{b['sa']}岁起):")
    for i,d in enumerate(b['dy']):
        age=(b['sa']+10*i, b['sa']+10*i+9)
        now=" ← 当前" if b['sa']+10*i<=2026-b['sd'].year<=b['sa']+10*i+9 else ""
        print(f"  {d}  {age[0]}-{age[1]}岁{now}")

def show_full(b, future_years=10):
    """完整分析模式"""
    show(b)

    # 地支关系
    yg,yz=b['y']; mg,mz_n=b['m']; dg,dz=b['d']; hg,hz=b['h']
    print(f"\n{'—'*40}\n【地支关系】")
    rels=dizhi_rels([yz,mz_n,dz,hz])
    for r in rels: print(r)
    # 补充: 与大运关系(当前大运)
    sa=b['sa']; age=2026-b['sd'].year
    dy_idx=max(0,min((age-sa)//10,7))
    if dy_idx<8:
        dy=b['dy'][dy_idx]
        print(f"\n  当前大运 {dy}:")
        dy_z=dy[1]
        for i,z in enumerate([yz,mz_n,dz,hz]):
            if CHONG.get(dy_z)==z: print(f"    大运{dy_z}冲{['年','月','日','时'][i]}支{z}")
            if LIUHE.get(dy_z)==z: print(f"    大运{dy_z}合{['年','月','日','时'][i]}支{z}")

    # 十神统计
    print(f"\n{'—'*40}\n【十神统计】")
    ss_count={}
    for s in b['all_ss']:
        ss_count[s]=ss_count.get(s,0)+1
    for k,v in sorted(ss_count.items(),key=lambda x:-x[1]):
        bar='█'*v
        print(f"  {k}: {bar} x{v}")

    # 流年分析
    cur_year=2026
    print(f"\n{'—'*40}\n【流年分析 {cur_year}-{cur_year+future_years-1}】")
    for yr in range(cur_year, cur_year+future_years):
        ln=liunian(b,yr)
        se_tag=f"[{ln['se']}]" if ln['se'] else ''
        effects='; '.join(ln['effects']) if ln['effects'] else '—'
        print(f"  {yr} {ln['yg']}{ln['yz']} {ln['ss']:3s} {se_tag:<4s} {effects}")

    # 2026流月
    print(f"\n{'—'*40}\n【{cur_year}年流月】")
    months=liumonth(b,cur_year)
    month_names=['寅','卯','辰','巳','午','未','申','酉','戌','亥','子','丑']
    for i,(mg,mz) in enumerate(months):
        # 流月与命局的关系
        rels=[]
        for j,z in enumerate([yz,mz_n,dz,hz]):
            if CHONG.get(mz)==z: rels.append(f'冲{["年","月","日","时"][j]}')
            if mz==z: rels.append(f'伏吟{["年","月","日","时"][j]}')
            if LIUHE.get(mz)==z: rels.append(f'合{["年","月","日","时"][j]}')
        gw=WX[mg]; xi,ji,_=xiyong(b)
        tag='✓' if gw in xi else ('⚠' if gw in ji else ' ')
        print(f"  {month_names[i]}月 {mg}{mz} {tag} {' | '.join(rels) if rels else '—'}")


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='-a':
        # 完整分析模式
        if len(sys.argv)<4:
            print("用法: python3 bazi_v1.4.py -a 1997-03-22 8 女")
            sys.exit(1)
        sd=datetime.strptime(sys.argv[2],'%Y-%m-%d').date()
        ti=int(sys.argv[3])
        g=sys.argv[4] if len(sys.argv)>4 else '男'
        show_full(calc(sd,ti,g))
    elif len(sys.argv)>2:
        sd=datetime.strptime(sys.argv[1],'%Y-%m-%d').date()
        ti=int(sys.argv[2])
        g=sys.argv[3] if len(sys.argv)>3 else '男'
        show(calc(sd,ti,g))
    else:
        sd=datetime.strptime(input('\xe7\x94\x9f\xe6\x97\xa5(YYYY-MM-DD):'),'%Y-%m-%d').date()
        show(calc(sd,int(input('\xe6\x97\xb6\xe8\xbe\xb0(0-12):')),input('\xe6\x80\xa7\xe5\x88\xab:')))