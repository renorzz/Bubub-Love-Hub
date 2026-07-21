import pygame, pygame.gfxdraw, math, random, sys
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
W, H = screen.get_size()
pygame.display.set_caption("Garden for Salsa")
clock = pygame.time.Clock()
PI2 = math.pi * 2

def lerp(a,b,t): return a+(b-a)*t
def clamp(v,a,b): return max(a,min(b,v))
def rand(a,b): return a+random.random()*(b-a)
def lift(c,a): return tuple(min(255,x+a) for x in c[:3])
def drop(c,a): return tuple(max(0,x-a) for x in c[:3])

PALS=[
    {'p':(255,107,171),'c':(255,230,60),'g':(220,20,120)},
    {'p':(200, 80,255),'c':(255,230,60),'g':(150, 0,230)},
    {'p':(255, 70, 70),'c':(255,180, 0),'g':(210, 0, 20)},
    {'p':(255,155, 40),'c':(255,230,60),'g':(210, 80,  0)},
    {'p':( 60,210,255),'c':(255,255,255),'g':(  0,140,230)},
    {'p':(255,255,255),'c':(255,230,60),'g':(170,200,255)},
    {'p':(130,255,150),'c':(255,230,60),'g':(  0,210, 80)},
    {'p':(255,215, 50),'c':(255,255,255),'g':(230,130,  0)},
]

def bezier(p0,p1,p2,p3,n=18):
    pts=[]
    for i in range(n+1):
        t=i/n; mt=1-t
        pts.append((mt**3*p0[0]+3*mt**2*t*p1[0]+3*mt*t**2*p2[0]+t**3*p3[0],
                    mt**3*p0[1]+3*mt**2*t*p1[1]+3*mt*t**2*p2[1]+t**3*p3[1]))
    return pts

def xform(pts,cx,cy,ang):
    ca,sa=math.cos(ang),math.sin(ang)
    return [(int(cx+p[0]*ca-p[1]*sa), int(cy+p[0]*sa+p[1]*ca)) for p in pts]

def aa_poly(surf,pts,col,alpha=255):
    if len(pts)<3: return
    c=(*col[:3],alpha)
    try:
        pygame.gfxdraw.filled_polygon(surf,pts,c)
        pygame.gfxdraw.aapolygon(surf,pts,c)
    except:
        pygame.draw.polygon(surf,col[:3],pts)

def fcircle(surf,x,y,r,col):
    """filled circle with alpha directly on surface"""
    r=max(1,int(r)); x,y=int(x),int(y)
    c3=tuple(clamp(int(v),0,255) for v in col[:3])
    a=clamp(int(col[3]),0,255) if len(col)>3 else 255
    try:
        pygame.gfxdraw.filled_circle(surf, x, y, r, (*c3, a))
    except:
        pygame.draw.circle(surf, c3, (x, y), r)

def soft_glow(surf,col,x,y,R,steps=6,max_a=70):
    R=int(R)
    if R<2: return
    x, y = int(x), int(y)
    c3=tuple(clamp(int(v),0,255) for v in col[:3])
    for i in range(steps,0,-1):
        r=max(1,R*i//steps)
        a=clamp(int(max_a*(1-i/steps)*2.5),0,255)
        try:
            pygame.gfxdraw.filled_circle(surf, x, y, r, (*c3, a))
        except:
            pass

def draw_petal_layered(surf,pts,cx,cy,ang,base,highlight,shadow):
    """Draw petal with 3 color layers for depth"""
    t=xform(pts,cx,cy,ang)
    aa_poly(surf,t,shadow)
    # Shrink toward center for inner highlight
    cx2=sum(p[0] for p in t)//len(t); cy2=sum(p[1] for p in t)//len(t)
    inner=[(int(p[0]*.78+cx2*.22), int(p[1]*.78+cy2*.22)) for p in t]
    aa_poly(surf,inner,base)
    inner2=[(int(p[0]*.5+cx2*.5), int(p[1]*.5+cy2*.5)) for p in t]
    aa_poly(surf,inner2,highlight,160)

def draw_leaf(surf,x,y,side,L,sw):
    if L<4: return
    ang=side*(math.pi/3.5+sw*0.04)
    body=bezier((0,0),(-L*.38,-L*.25),(-L*.22,-L*.7),(0,-L))
    body+=bezier((0,-L),(L*.22,-L*.7),(L*.38,-L*.25),(0,0))[1:]
    t=xform(body,x,y,ang)
    aa_poly(surf,t,(28,80,34))
    cx2=sum(p[0] for p in t)//len(t); cy2=sum(p[1] for p in t)//len(t)
    hi=[(int(p[0]*.65+cx2*.35),int(p[1]*.65+cy2*.35)) for p in t]
    aa_poly(surf,hi,(55,140,62),180)
    # Vein
    tip=xform([(0,-L*0.9)],x,y,ang)[0]
    pygame.draw.line(surf,(150,230,155,60),(int(x),int(y)),tip,1)

def draw_flower(surf,x,y,bt,pal,sc,np,ft):
    b=clamp(bt,0,1); s=sc
    p=pal['p']; c=pal['c']; g=pal['g']
    ph=lift(p,60); pm=lift(p,25); pd=drop(p,30)
    # Big aura
    soft_glow(surf,g,x,y,75*s*b,8,80)

    if ft==0:  # ROSE / PEONY
        pL=lerp(0,38,b)*s; pW=lerp(0,18,b)*s
        for i in range(np):
            ang=(PI2/np)*i+0.3
            body=bezier((-pW*.12,0),(-pW,-pL*.18),(-pW*.92,-pL*.65),(-pW*.22,-pL))
            body+=bezier((-pW*.22,-pL),(0,-pL*1.07),(pW*.22,-pL),(pW*.92,-pL*.65))[1:]
            body+=bezier((pW*.92,-pL*.65),(pW,-pL*.18),(pW*.12,0),(pW*.12,0))[1:]
            draw_petal_layered(surf,body,x,y,ang,pm,ph,pd)
        # 2nd ring smaller
        pL2=pL*.68; pW2=pW*.68
        for i in range(np-1):
            ang=(PI2/(np-1))*i
            body=bezier((-pW2*.1,0),(-pW2*.85,-pL2*.22),(-pW2*.8,-pL2*.68),(-pW2*.18,-pL2))
            body+=bezier((-pW2*.18,-pL2),(0,-pL2*1.05),(pW2*.18,-pL2),(pW2*.8,-pL2*.68))[1:]
            body+=bezier((pW2*.8,-pL2*.68),(pW2*.85,-pL2*.22),(pW2*.1,0),(pW2*.1,0))[1:]
            draw_petal_layered(surf,body,x,y,ang,ph,lift(p,80),pm)

    elif ft==1:  # DAISY
        cnt=np+3; pL=lerp(0,46,b)*s; pW=lerp(0,12,b)*s
        for i in range(cnt):
            ang=(PI2/cnt)*i
            body=bezier((0,0),(-pW*.6,-pL*.28),(-pW*.5,-pL*.72),(0,-pL))
            body+=bezier((0,-pL),(pW*.5,-pL*.72),(pW*.6,-pL*.28),(0,0))[1:]
            draw_petal_layered(surf,body,x,y,ang,pm,ph,pd)

    else:  # POPPY
        pL=lerp(0,42,b)*s; pW=lerp(0,22,b)*s
        for i in range(5):
            ang=(PI2/5)*i
            body=bezier((0,-pW*.07),(-pW*1.05,-pL*.1),(-pW*1.1,-pL*.58),(-pW*.48,-pL))
            body+=bezier((-pW*.48,-pL),(-pW*.16,-pL*1.07),(pW*.16,-pL*1.07),(pW*.48,-pL))[1:]
            body+=bezier((pW*.48,-pL),(pW*1.1,-pL*.58),(pW*1.05,-pL*.1),(0,-pW*.07))[1:]
            base=pm if i%2==0 else p
            hi=ph if i%2==0 else lift(p,40)
            draw_petal_layered(surf,body,x,y,ang,base,hi,pd)

    # Center
    cr=int(lerp(0,13,b)*s); cr2=int(cr*1.6)
    if cr2>1:
        fcircle(surf,x,y,cr2,(*drop(c,60),240))
    soft_glow(surf,c,x,y,cr*2.2,6,130)
    if cr>1:
        fcircle(surf,x,y,cr,(255,255,255,240))
        pygame.gfxdraw.aacircle(surf,int(x),int(y),cr,tuple(c[:3]))
    # Stamen ring
    if b>.55 and cr>0:
        da=clamp((b-.55)/.45,0,1)
        for i in range(8):
            ang2=(PI2/8)*i; dr=cr*1.18
            sx=int(x+math.cos(ang2)*dr); sy=int(y+math.sin(ang2)*dr)
            fcircle(surf,sx,sy,max(1,int(s*1.1)),(255,255,200,int(da*200)))

class Flower:
    def __init__(self,x):
        self.x=float(x); self.pal=random.choice(PALS)
        self.ft=random.randint(0,2); self.np=random.randint(5,8)
        self.sc=rand(.8,1.35); self.targetH=rand(110,min(340,H*.68))*self.sc
        self.stemH=0.; self.growR=rand(1.6,3.0); self.bloomT=0.
        self.phase='growing'
        self.swSpd=rand(.0012,.0028); self.swAmp=rand(5,12); self.swOff=rand(0,PI2); self.sw=0.
        self.leaves=[
            {'t':rand(.22,.42),'side':-1,'mul':rand(.75,1.1),'ot':0.},
            {'t':rand(.42,.62),'side': 1,'mul':rand(.65,1.0),'ot':0.},
            {'t':rand(.60,.78),'side':-1,'mul':rand(.55,.9), 'ot':0.},
        ]
        self.sparks=[]; self.stimer=0; self.age=0
    def update(self,dt):
        self.age+=dt
        self.sw=math.sin(self.age*self.swSpd+self.swOff)*self.swAmp
        if self.phase=='growing':
            self.stemH=min(self.stemH+self.growR*dt*.055,self.targetH)
            for l in self.leaves:
                if self.stemH/self.targetH>l['t']: l['ot']=min(1.,l['ot']+.025)
            if self.stemH>=self.targetH: self.phase='blooming'
        elif self.phase=='blooming':
            self.bloomT=min(1.,self.bloomT+.014)
            if self.bloomT>=1.: self.phase='alive'
        if self.phase=='alive':
            self.stimer+=dt
            if self.stimer>90+rand(0,90):
                self.stimer=0; tx=self.x+self.sw; ty=H-self.stemH
                self.sparks.append({'x':tx+rand(-16,16)*self.sc,'y':ty+rand(-12,12)*self.sc,
                                    'vx':rand(-.6,.6),'vy':rand(-2,-.4),'r':rand(1.5,3.5)*self.sc,'life':1.})
        for sp in self.sparks: sp['x']+=sp['vx'];sp['y']+=sp['vy'];sp['vy']+=.028;sp['life']-=.018
        self.sparks=[sp for sp in self.sparks if sp['life']>0]
    def draw(self,surf):
        tx=int(self.x+self.sw); ty=int(H-self.stemH)
        ix=int(self.x)
        if self.stemH>2:
            w=max(2,int(3*self.sc))
            pygame.draw.line(surf,(35,105,42),(ix,H),(tx,ty),w)
            pygame.draw.line(surf,(60,145,65),(ix-1,H),(tx-1,ty),max(1,w-1))
        for l in self.leaves:
            if l['ot']<=0: continue
            lx=lerp(self.x,tx,l['t']); ly=lerp(H,ty,l['t'])
            draw_leaf(surf,lx,ly,l['side'],40*self.sc*l['mul']*l['ot'],
                      self.sw/self.swAmp if self.swAmp else 0)
        if self.bloomT>0:
            draw_flower(surf,tx,ty,self.bloomT,self.pal,self.sc,self.np,self.ft)
        for sp in self.sparks:
            a=int(sp['life']*.8*220); r=max(1,int(sp['r']))
            fcircle(surf,int(sp['x']),int(sp['y']),r,(*self.pal['p'],a))

# ── Pre-render background ────────────────────────────────────────────────────
bg=pygame.Surface((W,H))
for y in range(H):
    t=y/H
    r=int(lerp(2,10,t)); g=int(lerp(0,2,t)); b=int(lerp(10,5,t))
    pygame.draw.line(bg,(r,g,b),(0,y),(W,y))
# Subtle vignette drawn directly on bg
for i in range(0, min(W,H)//2):
    a=int(i/(min(W,H)/2)*80)
    pygame.gfxdraw.rectangle(bg, pygame.Rect(i,i,W-2*i,H-2*i), (0,0,0,max(0,80-a)))

# Ground glow strip drawn directly on bg
for i in range(100):
    a=int((i/100)**2*50)
    pygame.gfxdraw.box(bg, pygame.Rect(0, H-100+i, W, 1), (0,160,50,a))

# Bokeh
boks=[{'x':rand(0,1),'y':rand(0,1),'r':rand(1.5,4),'a':rand(.04,.16),
       'sp':rand(.00004,.0002),'ph':rand(0,PI2)} for _ in range(22)]

# Fonts
try:
    font_h=pygame.font.SysFont('Georgia,serif',int(H*.072),italic=True)
    font_s=pygame.font.SysFont('Georgia,serif',int(H*.028),italic=True)
except:
    font_h=pygame.font.Font(None,int(H*.072))
    font_s=pygame.font.Font(None,int(H*.028))

flowers=[]
def add_flower(x):
    if len(flowers)>=18: flowers.pop(0)
    flowers.append(Flower(clamp(x,50,W-50)))

show_hint=True; hint_a=0
spawned=set(); t0=pygame.time.get_ticks()
spawn_xs=[rand(W*.1,W*.9) for _ in range(8)]

last_t=pygame.time.get_ticks()
running=True
while running:
    now=pygame.time.get_ticks(); dt=min(now-last_t,50); last_t=now
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT: running=False
        if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE: running=False
        if ev.type==pygame.MOUSEBUTTONDOWN: add_flower(ev.pos[0]); show_hint=False
    for i,xpos in enumerate(spawn_xs):
        if i not in spawned and now-t0>=200+i*450:
            add_flower(xpos); spawned.add(i)

    # Draw BG (now includes vignette and ground glow)
    screen.blit(bg,(0,0))

    # Bokeh
    for bk in boks:
        bk['y']-=bk['sp']
        if bk['y']<0: bk['y']=1.0
        ts=now*.0007
        al=int(bk['a']*(0.45+0.55*math.sin(ts+bk['ph']))*255)
        r=max(1,int(bk['r']))
        fcircle(screen,int(bk['x']*W),int(bk['y']*H),r,(210,175,255,al))

    for f in flowers:
        f.update(dt); f.draw(screen)

    # Hint text with glow
    if show_hint:
        hint_a=min(240,hint_a+4)
        for text,size,col in [("Garden for",int(H*.072),(255,255,255)),("Salsa",int(H*.09),(210,90,255))]:
            try: fnt=pygame.font.SysFont('Georgia,serif',size,italic=True)
            except: fnt=pygame.font.Font(None,size)
            surf=fnt.render(text,True,col)
            surf.set_alpha(hint_a)
            # Glow behind text using gfxdraw
            yp=H//2-90 if text=="Garden for" else H//2-90+int(H*.082)
            try:
                pygame.gfxdraw.filled_ellipse(screen, W//2, yp + surf.get_height()//2, (surf.get_width()+60)//2, (surf.get_height()+40)//2, (*col[:3],40))
            except:
                pass
            screen.blit(surf,(W//2-surf.get_width()//2,yp))
        try: fnt2=pygame.font.SysFont('Georgia,serif',int(H*.024),italic=True)
        except: fnt2=pygame.font.Font(None,int(H*.024))
        hint_surf=fnt2.render("click anywhere to plant a flower  ✦",True,(180,180,220))
        hint_surf.set_alpha(max(0,hint_a-80))
        screen.blit(hint_surf,(W//2-hint_surf.get_width()//2,H//2+int(H*.04)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit(); sys.exit()
