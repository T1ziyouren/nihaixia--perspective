#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 紫微斗数排盘 v2.7
import sys; from datetime import date
HE='甲乙丙丁戊己庚辛壬癸'; EB='子丑寅卯辰巳午未申酉戌亥'
PN=['命宫','父母宫','福德宫','田宅宫','官禄宫','交友宫','迁移宫','疾厄宫','财帛宫','子女宫','夫妻宫','兄弟宫']
ALL_MAIN=['紫微','天机','太阳','武曲','天同','廉贞','天府','太阴','贪狼','巨门','天相','天梁','七杀','破军']
ZW=['紫微','天机','','太阳','武曲','天同','','','廉贞']
TF=['天府','太阴','贪狼','巨门','天相','天梁','七杀','','','','破军']
TIGER={'甲':'丙','乙':'戊','丙':'庚','丁':'壬','戊':'甲','己':'丙','庚':'戊','辛':'庚','壬':'壬','癸':'甲'}
MUT={'甲':'廉贞破军武曲太阳','乙':'天机天梁紫微太阴','丙':'天同天机文昌廉贞','丁':'太阴天同天机巨门',
      '戊':'贪狼太阴右弼天机','己':'武曲贪狼天梁文曲','庚':'太阳武曲太阴天同','辛':'巨门太阳文曲文昌',
      '壬':'天梁紫微左辅武曲','癸':'破军巨门太阴贪狼'}
LU={'甲':'寅','乙':'卯','丙':'巳','丁':'午','戊':'巳','己':'午','庚':'申','辛':'酉','壬':'亥','癸':'子'}
KUI={'甲':'丑','乙':'子','丙':'亥','丁':'亥','戊':'丑','己':'子','庚':'丑','辛':'午','壬':'卯','癸':'卯'}
YUE={'甲':'未','乙':'申','丙':'酉','丁':'酉','戊':'未','己':'申','庚':'未','辛':'寅','壬':'巳','癸':'巳'}
MA={'寅':'申','午':'申','戌':'申','申':'寅','子':'寅','辰':'寅','巳':'亥','酉':'亥','丑':'亥','亥':'巳','卯':'巳','未':'巳'}
CS12=['长生','沐浴','冠带','临官','帝旺','衰','病','死','墓','绝','胎','养']
BS12=['博士','力士','青龙','小耗','将军','奏书','飞廉','喜神','病符','大耗','伏兵','官府']
WUHE={'甲':'己','乙':'庚','丙':'辛','丁':'壬','戊':'癸','己':'甲','庚':'乙','辛':'丙','壬':'丁','癸':'戊'}
def fx(i,m=12): return((i%m)+m)%m
def e2i(e): return(EB.index(e)-2)%12

def pai(lm,ld,ti,yg,yz,gender='男'):
    assert yg in TIGER
    shun=(yg in'甲丙戊庚壬' and gender=='男') or (yg in'乙丁己辛癸' and gender=='女')
    mi=(lm-1)%12; s=fx(mi-ti); b=fx(mi+ti)
    pn=[PN[fx(i-s)] for i in range(12)]
    ig=TIGER[yg]; gi=HE.index(ig)
    gs=[HE[(gi+i)%10] for i in range(12)]
    es=[EB[(i+2)%12] for i in range(12)]
    sg=gs[s]; sz=es[s]
    gn={'甲':1,'乙':1,'丙':2,'丁':2,'戊':3,'己':3,'庚':4,'辛':4,'壬':5,'癸':5}[sg]
    zn={'子':1,'丑':1,'寅':2,'卯':2,'辰':3,'巳':3,'午':1,'未':1,'申':2,'酉':2,'戌':3,'亥':3}[sz]
    wi=gn+zn-1
    while wi>4: wi-=5
    wx=['木三局','金四局','水二局','火六局','土五局'][wi]
    wn={'木':3,'金':4,'水':2,'火':6,'土':5}[wx[0]]
    off=0
    while(ld+off)%wn!=0: off+=1
    q=(ld+off)//wn; zi=q-1; zi=fx(zi+(off if off%2==0 else -off)); tf=fx(12-zi)
    st=[[] for _ in range(12)]
    for i,v in enumerate(ZW):
        if v: st[fx(zi-i)].append(v)
    for i,v in enumerate(TF):
        if v: st[fx(tf+i)].append(v)
    hu={}
    if yg in MUT:
        ms=[MUT[yg][i:i+2] for i in range(0,8,2)]
        hu={'禄':ms[0],'权':ms[1],'科':ms[2],'忌':ms[3]}
    st[fx(e2i('戌')-ti)].append('文昌'); st[fx(e2i('辰')+ti)].append('文曲')
    st[fx(e2i('亥')+ti)].append('地劫'); st[fx(e2i('亥')-ti)].append('地空')
    hx={'寅':e2i('丑'),'午':e2i('丑'),'戌':e2i('丑'),'申':e2i('寅'),'子':e2i('寅'),'辰':e2i('寅'),
        '巳':e2i('卯'),'酉':e2i('卯'),'丑':e2i('卯'),'亥':e2i('酉'),'卯':e2i('酉'),'未':e2i('酉')}[yz]
    st[fx(hx+ti)].append('火星')
    lx={'寅':e2i('卯'),'午':e2i('卯'),'戌':e2i('卯'),'申':e2i('戌'),'子':e2i('戌'),'辰':e2i('戌'),
        '巳':e2i('戌'),'酉':e2i('戌'),'丑':e2i('戌'),'亥':e2i('戌'),'卯':e2i('戌'),'未':e2i('戌')}[yz]
    st[fx(lx+ti)].append('铃星')
    li=e2i(LU[yg]); st[li].append('禄存'); st[fx(li+1)].append('擎羊'); st[fx(li-1)].append('陀罗')
    st[e2i(KUI[yg])].append('天魁'); st[e2i(YUE[yg])].append('天钺')
    st[e2i(MA[yz])].append('天马')
    hl=fx(e2i('卯')-EB.index(yz)); st[hl].append('红鸾'); st[fx(hl+6)].append('天喜')
    st[fx(e2i('辰')+lm-1)].append('左辅'); st[fx(e2i('戌')-lm+1)].append('右弼')
    st[fx(e2i('酉')+lm-1)].append('天刑'); st[fx(e2i('丑')+lm-1)].append('天姚')
    zuo=fx(e2i('辰')+lm-1); you=fx(e2i('戌')-lm+1); ch=fx(e2i('戌')-ti); qu=fx(e2i('辰')+ti)
    st[fx(zuo+ld-1)].append('三台'); st[fx(you-ld+1)].append('八座')
    st[fx(ch+ld-2)].append('恩光'); st[fx(qu+ld-2)].append('天贵')
    yzi=EB.index(yz); st[fx(e2i('辰')+yzi)].append('龙池'); st[fx(e2i('戌')-yzi)].append('凤阁')
    st[fx(e2i('午')-yzi)].append('天哭'); st[fx(e2i('午')+yzi)].append('天虚')
    cs_start=e2i({'甲':'亥','乙':'午','丙':'寅','丁':'酉','戊':'寅','己':'酉','庚':'巳','辛':'子','壬':'申','癸':'卯'}[yg])
    for i,v in enumerate(CS12):
        st[fx(cs_start+i if shun else cs_start-i)].append(f"[{v}]")
    for i,v in enumerate(BS12):
        st[fx(li+i if shun else li-i)].append(f"({v})")
    dl=['']*12
    for i in range(12):
        dl[fx(s+i if shun else s-i)]=f"{wn+10*i}-{wn+10*i+9}"
    return {'pn':pn,'gs':gs,'es':es,'bs':b,'wx':wx,'st':st,'hu':hu,'dl':dl}

def show(pan):
    print(f"{'':=^60}"); print(f"五行局: {pan['wx']}")
    if pan['hu']: print(f"四化: {pan['hu']['禄']}化禄 {pan['hu']['权']}化权 {pan['hu']['科']}化科 {pan['hu']['忌']}化忌")
    print(f"{'':=^60}")
    for i in range(12):
        ms=[n for n in pan['st'][i] if n in ALL_MAIN]
        oss=sorted(set(n for n in pan['st'][i] if n not in ALL_MAIN and not n.startswith('[') and not n.startswith('(')))
        cs=[n for n in pan['st'][i] if n.startswith('[')]
        bs=[n for n in pan['st'][i] if n.startswith('(')]
        txt=[]
        for m in ms:
            tag=''
            for hk,hv in pan['hu'].items():
                if m==hv: tag=f"[{hk}]"
            txt.append(f"{m}{tag}")
        dt=' '.join(txt) or '(空)'
        if oss: dt+=' '+' '.join(oss)
        if bs: dt+=' '+' '.join(bs)
        if cs: dt+=' '+' '.join(cs)
        print(f"{pan['es'][i]:<4}{pan['pn'][i]:<6}{pan['gs'][i]+pan['es'][i]:<6}{dt:<50}{pan['dl'][i]}")
    print(f"身宫: {pan['es'][pan['bs']]}({pan['pn'][pan['bs']]})"); print(f"{'':=^60}")

ALL_MAIN_SET=set(ALL_MAIN)
if len(sys.argv)>1 and sys.argv[1]=='-a':
    lm=int(sys.argv[2]); ld=int(sys.argv[3]); ti=int(sys.argv[4])
    yg=sys.argv[5] if len(sys.argv)>5 else'甲'; yz=sys.argv[6] if len(sys.argv)>6 else'子'
    gen=sys.argv[7] if len(sys.argv)>7 else'男'
    pan=pai(lm,ld,ti,yg,yz,gen)
    show(pan)
    st=pan['st']
    lucky=['天魁','天钺','左辅','右弼','文昌','文曲','禄存','天马','龙池','凤阁','三台','八座','恩光','天贵','天喜','红鸾']
    sha=['擎羊','陀罗','火星','铃星','地空','地劫','天刑','天哭','天虚','天姚']
    lucky_in=[]; sha_in=[]; mains=[]
    for i in range(12):
        for s in st[i]:
            if s in ALL_MAIN_SET: mains.append(s+'('+pan['pn'][i]+')')
            elif s in lucky: lucky_in.append(s+'('+pan['pn'][i]+')')
            elif s in sha: sha_in.append(s+'('+pan['pn'][i]+')')
    print(f"\n{'='*40}\n[星曜统计]")
    print(f"  主星({len(mains)}): {', '.join(mains)}")
    print(f"  吉星({len(lucky_in)}): {', '.join(lucky_in)}")
    print(f"  煞星({len(sha_in)}): {', '.join(sha_in)}")
    if pan['hu']:
        print(f"\n[四化]")
        for k,v in pan['hu'].items():
            for i in range(12):
                if v in st[i]: print(f"  {v}化{k}在{pan['pn'][i]}")
    empty=[pan['pn'][i] for i in range(12) if not any(s in ALL_MAIN_SET for s in st[i])]
    if empty: print(f"\n[空宫]: {', '.join(empty)}")
    sys.exit(0)

if len(sys.argv)>1 and sys.argv[1]=='-q':
    q=sys.argv[2]; a=sys.argv[3] if len(sys.argv)>3 else ''
    D={'wuhe':WUHE,'六合':{'子':'丑','丑':'子','寅':'亥','卯':'戌','辰':'酉','巳':'申','午':'未','未':'午','申':'巳','酉':'辰','戌':'卯','亥':'寅'},
       '冲':{'子':'午','丑':'未','寅':'申','卯':'酉','辰':'戌','巳':'亥','午':'子','未':'丑','申':'寅','酉':'卯','戌':'辰','亥':'巳'},
       '害':{'子':'未','丑':'午','寅':'巳','卯':'辰','申':'亥','酉':'戌','巳':'寅','午':'丑','未':'子','辰':'卯','戌':'酉','亥':'申'},
       '破':{'子':'酉','丑':'辰','寅':'亥','卯':'午','辰':'丑','巳':'申','午':'卯','未':'戌','申':'巳','酉':'子','戌':'未','亥':'寅'},
       '藏干':{'子':'癸','丑':'己癸辛','寅':'甲丙戊','卯':'乙','辰':'戊乙癸','巳':'丙庚戊','午':'丁己','未':'己丁乙','申':'庚壬戊','酉':'辛','戌':'戊辛丁','亥':'壬甲'},
       '长生':{'甲':'亥','乙':'午','丙':'寅','丁':'酉','戊':'寅','己':'酉','庚':'巳','辛':'子','壬':'申','癸':'卯'},
       '三合':{'申子辰':'水','亥卯未':'木','寅午戌':'火','巳酉丑':'金'},
       '刑':{'寅巳申':'无恩','丑戌未':'恃势','子卯':'无礼','辰午酉亥':'自刑'}}
    if q=='rels' and a:
        # 分析多个地支关系: python3 ziweipan.py -q rels 申,卯,子,卯
        zhis=a.split(',')
        labels='年月日时'
        print(f"地支: {' '.join(f'{labels[i]}{z}' for i,z in enumerate(zhis))}")
        for i in range(len(zhis)):
            for j in range(i+1,len(zhis)):
                r=[]
                x,y=zhis[i],zhis[j]
                if D['六合'].get(x)==y: r.append('六合')
                if D['冲'].get(x)==y: r.append('冲')
                if D['害'].get(x)==y: r.append('害')
                if D['破'].get(x)==y: r.append('破')
                for k,v in D['三合'].items():
                    if x in k and y in k:
                        if all(z in zhis for z in k): r.append(f'三合({v})')
                        else: r.append(f'半合({v})')
                for k,v in D['刑'].items():
                    if x in k and y in k and x!=y: r.append(v+'之刑')
                if r: print(f"  {labels[i]}{x}-{labels[j]}{y}: {', '.join(r)}")
    elif q in D:
        if a: print(f"{a}->{D[q].get(a,'?')}")
        else: [print(f"{k}->{v}") for k,v in D[q].items()]
    sys.exit(0)

if len(sys.argv)>1 and sys.argv[1]=='-s':
    m=sys.argv[2]; gs=sys.argv[3:]; wm={'甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水'}
    fe={'木':('土','火'),'火':('金','土'),'土':('水','金'),'金':('木','水'),'水':('火','木')}
    yy=lambda g:'阳' if g in'甲丙戊庚壬'else'阴'; rw=wm[m]
    for g in gs:
        tw=wm[g]; print(f"{m}({yy(m)}{rw})对{g}({yy(g)}{tw}):",end='')
        if rw==tw: print("比肩"if yy(m)==yy(g)else"劫财")
        elif fe[rw][0]==tw: print("偏财"if yy(m)==yy(g)else"正财")
        elif fe[tw][0]==rw: print("七杀"if yy(m)==yy(g)else"正官")
        elif fe[rw][1]==tw: print("食神"if yy(m)==yy(g)else"伤官")
        else: print("偏印"if yy(m)==yy(g)else"正印")
        print(f"五合:{'合'if g in WUHE and WUHE[g]==m else'不合'}")
    sys.exit(0)

if len(sys.argv)>1 and sys.argv[1]=='-l':
    lm=int(sys.argv[2]); ld=int(sys.argv[3]); ti=int(sys.argv[4])
    yg=sys.argv[5] if len(sys.argv)>5 else'甲'; yz=sys.argv[6] if len(sys.argv)>6 else'子'
    gen=sys.argv[7] if len(sys.argv)>7 else'男'
    print(f"农历{lm}月{ld}日{yg}{yz}时{ti} {gen}"); show(pai(lm,ld,ti,yg,yz,gen))
else:
    lm=int(input("月:"));ld=int(input("日:"));ti=int(input("时:"))
    yg=input("年干:");yz=input("年支:");gen=input("性别(男/女):") or'男'
    show(pai(lm,ld,ti,yg,yz,gen))
