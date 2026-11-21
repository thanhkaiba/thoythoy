# Tách khung hình từ sprite sheet nền đen (và cắt chân dung) thành atlas nền trong suốt cho game.
# Dùng: python3 build_art.py <thư mục ảnh gốc>/ <thư mục web/art>/
import sys, json, numpy as np
from collections import deque
from PIL import Image, ImageFilter
SRC=sys.argv[1]; OUT=sys.argv[2]
N={'sam_side':'4e6b0803-e9b5-4b65-9e70-cc64c3517c0b.webp','gan':'736fd146-9545-400a-9f67-9fbc76c3a913.webp','rai':'73b36457-38b8-4316-a9ed-e2c01a1aefaa.webp','yae':'f7c3a9ad-9afb-486b-8e6d-3e156f7ce583.webp','sam_map':'image.jpg'}
def comps(mask):
    H,W=mask.shape; lab=np.zeros((H,W),np.int32); n=0; sizes=[0]
    for y0,x0 in zip(*np.where(mask)):
        if lab[y0,x0]: continue
        n+=1; lab[y0,x0]=n; dq=deque([(y0,x0)]); c=0
        while dq:
            y,x=dq.popleft(); c+=1
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=y+dy,x+dx
                if 0<=yy<H and 0<=xx<W and mask[yy,xx] and not lab[yy,xx]:
                    lab[yy,xx]=n; dq.append((yy,xx))
        sizes.append(c)
    return lab,np.array(sizes)
def keyed(name, thr=16, scale=1, holes=0):
    im=Image.open(SRC+N[name]).convert('RGB')
    if scale!=1: im=im.resize((im.width*scale,im.height*scale),Image.NEAREST)
    a=np.asarray(im).astype(np.uint8)
    dark=a.max(axis=2)<thr
    H,W=dark.shape
    bg=np.zeros((H,W),bool)
    dq=deque()
    for x in range(W):
        for y in (0,H-1):
            if dark[y,x] and not bg[y,x]: bg[y,x]=True; dq.append((y,x))
    for y in range(H):
        for x in (0,W-1):
            if dark[y,x] and not bg[y,x]: bg[y,x]=True; dq.append((y,x))
    while dq:
        y,x=dq.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and dark[yy,xx] and not bg[yy,xx]:
                bg[yy,xx]=True; dq.append((yy,xx))
    fg=~bg
    if holes:
        hole=(a.max(axis=2)<9)&fg
        lab,sz=comps(hole)
        fg&=~(sz[lab]>=holes)
    # drop specks
    m=Image.fromarray((fg*255).astype(np.uint8))
    m=m.filter(ImageFilter.MedianFilter(3))
    core=np.asarray(m)>0
    # dilate 2px to keep a dark outline
    out=np.asarray(m.filter(ImageFilter.MaxFilter(5)))>0
    rgba=np.dstack([a,(out*255).astype(np.uint8)])
    rgba[~core & out,:3]=(18,12,20)
    return rgba,core
def bands(mask,minlen=4,gap=3):
    out=[];s=None;l=None
    for i,v in enumerate(mask):
        if v:
            if s is None:s=i
            l=i
        elif s is not None and i-l>gap:
            if l-s+1>=minlen:out.append((s,l))
            s=None
    if s is not None:out.append((s,l))
    return out
def split(core,r0,r1,c0,c1,n):
    # split a merged band into n frames at density minima near even cut points
    prof=core[r0:r1+1,c0:c1+1].sum(axis=0)
    cuts=[c0]
    for i in range(1,n):
        mid=int((c1-c0)*i/n); w=int((c1-c0)/n*0.3)
        seg=prof[mid-w:mid+w]; cuts.append(c0+mid-w+int(seg.argmin()))
    cuts.append(c1+1)
    return [(cuts[i],cuts[i+1]-1) for i in range(n)]
def frames(name,rowsel,merge=None,thr=16,scale=1,skiprows=40,rows=None,colsx=None,holes=0):
    rgba,core=keyed(name,thr,scale,holes)
    rows=rows or [r for r in bands(core.sum(axis=1)>2,gap=3*scale) if r[1]-r[0]>skiprows*scale]
    res=[]
    for ri in rowsel:
        r0,r1=rows[ri]
        cols=bands(core[r0:r1+1].sum(axis=0)>0,gap=3*scale)
        cols=[c for c in cols if c[1]-c[0]>20*scale]
        if colsx and ri in colsx: cols=colsx[ri]
        fl=[]
        for ci,(c0,c1) in enumerate(cols):
            n=(merge or {}).get((ri,ci),1)
            fl+= split(core,r0,r1,c0,c1,n) if n>1 else [(c0,c1)]
        row=[]
        for (c0,c1) in fl:
            sub=core[r0:r1+1,c0:c1+1]
            ys=np.where(sub.any(axis=1))[0]; xs=np.where(sub.any(axis=0))[0]
            y0,y1=r0+ys[0],r0+ys[-1]; x0,x1=c0+xs[0],c0+xs[-1]
            f=rgba[max(0,y0-3):y1+4,max(0,x0-3):x1+4].copy(); c=core[max(0,y0-3):y1+4,max(0,x0-3):x1+4]
            lab,sz=comps(f[:,:,3]>0)
            for l in set(lab[:,0])|set(lab[:,-1]):
                if l and sz[l]<400: f[lab==l]=0; c=c&(lab!=l)
            row.append((f,c))
        res.append(row)
    return res
def anchor(core):
    # feet centre: centroid of the bottom 10% rows
    h=core.shape[0]; b=core[int(h*0.62):]
    return int(np.median(np.where(b)[1])) if b.any() else core.shape[1]//2
def atlas(fr,fname,anch=None):
    # fr: list of (rgba,core); cell is uniform, feet centred, bottom aligned
    A=[anchor(c) if not anch or anch[i] is None else anch[i] for i,(_,c) in enumerate(fr)]
    L=max(A); R=max(f.shape[1]-a for (f,_),a in zip(fr,A)); Hh=max(f.shape[0] for f,_ in fr)
    half=max(L,R); cw=half*2; 
    sheet=Image.new('RGBA',(cw*len(fr),Hh),(0,0,0,0))
    for i,((f,_),a) in enumerate(zip(fr,A)):
        im=Image.fromarray(f,'RGBA')
        sheet.paste(im,(i*cw+half-a,Hh-f.shape[0]))
    sheet.save(OUT+fname,lossless=True,method=6)
    return {'file':fname,'n':len(fr),'w':cw,'h':Hh}
meta={}
s=frames('sam_side',[0,1],rows=[(45,222),(300,472)])
print('sam',[len(r) for r in s])
meta['sam_atk']=atlas(s[0],'sam_atk.webp'); meta['sam_skill']=atlas(s[1],'sam_skill.webp')
sm=frames('sam_map',[0,1],thr=30,scale=2)
print('sam_map',[len(r) for r in sm])
meta['sam_front']=atlas(sm[0],'sam_front.webp'); 
g=frames('gan',[0,1],holes=60); print('gan',[len(r) for r in g])
meta['gan_atk']=atlas(g[0],'gan_atk.webp')
r=frames('rai',[0,1],merge={(1,0):3},rows=[(48,224),(300,468)],colsx={0:[(55,216),(249,425),(427,598),(624,797),(803,938)],1:[(27,617),(628,806),(815,1011)]},holes=60); print('rai',[len(x) for x in r])
meta['rai_atk']=atlas(r[0],'rai_atk.webp'); meta['rai_skill']=atlas(r[1],'rai_skill.webp')
y=frames('yae',[0,1],holes=60); print('yae',[len(x) for x in y])
meta['yae_atk']=atlas(y[0],'yae_atk.webp')
json.dump(meta,open(OUT+'meta.json','w'),indent=1); print(meta)
# chân dung
def crop(f,box,name,size=192):
    Image.open(SRC+f).convert('RGB').crop(box).resize((size,size),Image.LANCZOS).save(OUT+name,quality=88)
crop('5be0b7ec-6e97-4a45-8af1-073e6e7b984f.webp',(150,125,450,425),'p_gan.jpg')
crop('a8599763-545b-4811-bc0f-365cafe93ab0.webp',(185,150,425,390),'p_rai.jpg')
crop('e7abd892-8ccb-447b-acc2-5d2d11900486.webp',(150,185,450,485),'p_yae.jpg')
crop('71744ce5-f90b-4d8c-a959-b9a3784539d4.webp',(560,95,740,275),'p_sage.jpg')
# chân dung kiếm khách: phóng to đầu sprite trên nền giấy
f0=Image.fromarray(sm[0][0][0],'RGBA'); w=f0.width
head=f0.crop((max(0,w//2-58),0,max(0,w//2-58)+116,116)).resize((192,192),Image.NEAREST)
bg=Image.new('RGB',(192,192),(236,222,190)); bg.paste(head,(0,0),head); bg.save(OUT+'p_sam.jpg',quality=90)

