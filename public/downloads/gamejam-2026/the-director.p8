pico-8 cartridge // http://www.pico-8.com
version 43
__lua__
-- 00_boot: init and mode dispatch
function _init()
 st="title"
 sel=1
 lvn=1
 t=0
 lock=15
 endn=0
 msg,mt="",0
 flagx=114
 objs={}
 sol={}
 pl={}
 pts=0
 ph=""
 icd=0
 cue=0
 win=false
 s100=-1
 h={x=6,y=86,v=0,s="ready",tm=0,blk=0,lx=6,cau=""}
 pmusic(MUS_B)
end

function _update()
 t+=1
 if lock>0 then
  lock-=1
  return
 end
 if mt>0 then mt-=1 end
 if icd>0 then icd-=1 end
 if st=="title" then
  if btnp(4) then
   st="sel"
   sel=min(dget(0)>=1 and dget(0) or 1,14)
   lock=10
   psfx(SND_UI)
  end
  return
 end
 if st=="sel" then
  upd_select()
  return
 end
 if st=="story" then
  if btnp(4) then
   tolv(sel)
   lock=10
   psfx(SND_UI)
  end
  if btnp(5) then st="sel" lock=10 end
  return
 end
 if st=="play" then
  upd_play()
  return
 end
 if st=="res" then
  if btnp(4) and btn(5) then
   s100=sim100()
   psfx(SND_UI)
   return
  end
  if btnp(4) then
   if win and lvn==14 then
    st="end"
    endn=1
    lock=15
   else
    tolv(lvn)
    lock=10
   end
  end
  if btnp(5) then
   st="sel"
   lock=10
  end
  return
 end
 if st=="end" then
  if btnp(4) then
   endn+=1
   lock=12
   if endn>6 then
    st="title"
    lock=15
   end
  end
  return
 end
end

function upd_select()
 if btnp(0) then
  sel=max(1,sel-1)
  psfx(SND_UI)
 end
 if btnp(1) then
  sel=min(dget(0)>=1 and dget(0) or 1,14)
  psfx(SND_UI)
 end
 if btnp(2) then sel=max(1,sel-7) psfx(SND_UI) end
 if btnp(3) then sel=min(dget(0)>=1 and dget(0) or 1,14) sel=min(14,sel+7) psfx(SND_UI) end
 if btnp(4) then
  if sel<=(dget(0)>=1 and dget(0) or 1) then
   st="story"
   lock=10
   psfx(SND_UI)
  else
   psfx(SND_UI)
  end
 end
 if btnp(5) then st="title" lock=10 end
end

function upd_play()
 for o in all(objs) do
  if o.f>0 and o.f<25 then o.f-=1 end
 end
 if ph=="build" then
  if btn(0) then cx-=1.5 end
  if btn(1) then cx+=1.5 end
  if btn(2) then cy-=1.5 end
  if btn(3) then cy+=1.5 end
  cx=mid(1,cx,127)
  cy=mid(17,cy,111)
  if btnp(4) and btn(5) and icd==0 then
   ph="cue"
   cue=45
   psfx(SND_CUE)
   pmusic(MUS_S)
  elseif btnp(5) and icd==0 then
   ercyc()
  elseif btnp(4) and icd==0 then
   place()
  end
 end
 if ph=="run" and btnp(5) then
  ph="pause"
  psfx(SND_UI)
 elseif ph=="pause" and btnp(5) then
  ph="run"
  psfx(SND_UI)
 elseif ph~="build" and ph~="pause" then
  simstep()
 end
end

function _draw()
 cls(0)
 if st=="title" then
  dtitle()
  return
 end
 if st=="sel" then
  dselect()
  return
 end
 if st=="story" then
  dstorycard()
  return
 end
 if st=="end" then
  dending()
  return
 end
 dstage()
 if ph~="build" then
  dhero()
 end
 dcur()
 dcurtain()
 dhud()
 if st=="res" then dres() end
end
-- 10_data: constants, 14 levels, story
-- measured canon: 2-gap jump safe, 3+ gap deadly; 1 spike dodged, landing cell kills
COST={1,1,2,2,2,2}
TN={"plank","spike","beast","rock","swch","brdg"}
MUS_B,MUS_S,MUS_W,MUS_L=0,4,8,11
SND_PLACE,SND_DEL,SND_TRIG,SND_THUD=1,2,3,4
SND_SW,SND_BR,SND_WIN,SND_L,SND_UI=5,6,7,8,9
SND_DENY,SND_JUMP,SND_SLASH,SND_BDIE=11,12,14,15
SND_FLAG,SND_CUE,SND_HDIE=17,18,21
snd=true

LV={
-- l1 black: spike the landing cell beyond a safe 2-gap
{p=0,pts=1,tools="2",sx=0,sr=10,fx=14,
 goal="spike the cell he lands on",
 story="he runs. you only bend the stage.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","................",
 "#####..#########","#####..#########"}},
-- l2 black: one spike dodged, a field of spikes not
{p=0,pts=2,tools="2",sx=0,sr=10,fx=14,
 goal="one spike he dodges. two he cannot",
 story="he can read one threat. not a field.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","................",
 "################","################"}},
-- l3 white: one plank bridges a 4-gap grave
{p=1,pts=1,tools="1",sx=0,sr=10,fx=14,
 goal="one plank turns a grave into two steps",
 story="the other face of the job.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","................",
 "####....########","####....########"}},
-- l4 black: beast catches the landing
{p=0,pts=2,tools="23",sx=0,sr=10,fx=14,
 goal="catch him where he lands",
 story="the beast is not the weapon. the landing is.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","................",
 "#####..#########","#####..#########"}},
-- l5 black: combo (shared terrain with l10, spike cast)
{p=0,pts=3,tools="123",sx=0,sr=10,fx=14,
 goal="one threat ruins his answer to the next",
 story="single tricks die on arrival. compose.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","................",
 "######..##^#####","######..########"}},
-- l6 black: he never looks up
{p=0,pts=2,tools="4",sx=0,sr=10,fx=14,
 goal="he never looks up",
 story="you have been thinking on the ground.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","................",
 "################","################"}},
-- l7 white: step over the gate (4-gap)
{p=1,pts=2,tools="1",sx=0,sr=10,fx=14,
 goal="one plank. two graves. choose",
 story="a gate works both ways.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","................",
 "#######....#####","#######....#####"}},
-- l8 black: the ceiling is not
{p=0,pts=3,tools="14",sx=0,sr=10,fx=14,
 goal="the floor is a lie. the ceiling is not",
 story="arrange the ground all you like. look up.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","................",
 "################","################"}},
-- l9 black set piece: switch drops the sky (rocks preset, armless)
{p=0,pts=4,tools="5",sx=0,sr=10,fx=14,
 goal="one click. everything falls",
 story="he trusts the scenery. write the script.",
 rows={
 "....R.......R...","................","................","................",
 "................","................","................","................",
 "................","................",
 "################","################"}},
-- l10 white: same floor as l5, different cast (beast instead of spike)
{p=1,pts=3,tools="123",sx=0,sr=10,fx=14,
 goal="the same floor. the other job",
 story="you know this stage by heart. so does he.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","................",
 "######..##^.Y###","######..########"}},
-- l11 black: the way you bought can be taken back (preset bridge)
{p=0,pts=3,tools="25",sx=0,sr=10,fx=14,
 goal="pull the floor from his plans",
 story="bridges are not roads. they are schedules.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","................",
 "#####xxxx#######","................"}},
-- l12 white: plank the pit, the sky handles the rest
{p=1,pts=3,tools="145",sx=0,sr=10,fx=14,
 goal="plank the pit. mind what waits above",
 story="what you learned to kill with opens the door.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","............Y...",
 "###########...##","###########...##"}},
-- l13 white: escort through everything you rehearsed
{p=1,pts=3,tools="1234",sx=0,sr=10,fx=14,
 goal="escort through every trick you know",
 story="every hazard here was your idea.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","................",
 "####...##^Y#####","####...#########"}},
-- l14 finale white: get him to the flag
{p=1,pts=3,tools="12345",sx=0,sr=10,fx=14,
 goal="bring him to the flag. end act one",
 story="final cue. the world waits.",
 rows={
 "................","................","................","................",
 "................","................","................","................",
 "................","................",
 "####....###Y####","####....########"}}
}

STORY_END={
 "the hero reaches the flag.",
 "the world ends. as planned.",
 "you were never his savior.",
 "you were his stagehand.",
 "he looks back at you.",
 "fin."}

function tolv(n)
 st="play"
 lvn=n
 boot()
end

function boot()
 local L=LV[lvn]
 ph="build"
 cue=0
 pts=L.pts
 pl={}
 for i=1,#L.tools do
  pl[#pl+1]=sub(L.tools,i,i)+0
 end
 tool=pl[1]
 objs={}
 sol={}
 for r=0,11 do
  local row=sub(L.rows[r+1],1,16)
  local run=0
  local rx=0
  for c=0,15 do
   local ch=sub(row,c+1,c+1)
   if ch=="#" or ch=="=" then
    if run==0 then rx=c end
    run+=1
   else
    if run>0 then
     add(sol,{rx*8,16+r*8,run*8,8})
     run=0
    end
    if ch=="^" then add(objs,{k=2,x=c*8,y=16+r*8,c=0,f=0}) end
    if ch=="B" then add(objs,{k=3,x=c*8,y=16+r*8,c=0,f=0,hp=1}) end
    if ch=="Y" then add(objs,{k=3,x=c*8,y=16+r*8,c=0,f=0,hp=2}) end
    if ch=="R" then add(objs,{k=4,x=c*8,y=16+r*8,c=0,f=0,st="hang",vy=0,arm=false}) end
    if ch=="K" then add(objs,{k=5,x=c*8,y=16+r*8,c=0,f=0,on=false}) end
    if ch=="x" then add(objs,{k=6,x=c*8,y=16+r*8,c=0,f=0,tr=-1}) end
   end
  end
  if run>0 then add(sol,{rx*8,16+r*8,run*8,8}) end
 end
 flagx=L.fx*8+2
 s100=-1
 h={x=L.sx*8,y=16+L.sr*8-10,v=0,s="ready",tm=0,blk=0,lx=L.sx*8,cau=""}
 cx,cy=48,80
 msg,mt="",0
 icd=0
 t=0
 lock=12
 win=false
end
-- 20_sim: canon physics, hero fsm, verb runtime
function solidat(px,py)
 for r in all(sol) do
  if px>=r[1] and px<r[1]+r[3] and py>=r[2] and py<r[2]+r[4] then
   return true
  end
 end
 for o in all(objs) do
  if o.k==1 and px>=o.x and px<o.x+16 and py>=o.y and py<o.y+8 then
   return true
  end
  if o.k==6 and o.tr~=99 and px>=o.x and px<o.x+16 and py>=o.y and py<o.y+4 then
   return true
  end
 end
 return false
end

function ov(a,b,w,hh,c,d,w2,h2)
 return a<c+w2 and a+w>c and b<d+h2 and b+hh>d
end

function kill(c)
 h.s="die"
 h.tm=0
 h.cau=c or ""
 if c~="stall" then
  dset(100+lvn,flr(h.x/8))
  dset(200+lvn,flr(h.y/8))
 end
 psfx(SND_HDIE)
end

-- tier-4 memory: he hesitates at the spot a past attempt died
function wary()
 local mx=dget(100+lvn)
 if mx<=0 then return false end
 return h.y>80 and abs(h.x-mx*8)<9
end

function sim100()
 local w=0
 local plist={}
 for o in all(objs) do plist[#plist+1]={o.k,o.x,o.y,o.c} end
 for i=1,100 do
  for n in all(plist) do
   add(objs,{k=n[1],x=n[2],y=n[3],c=n[4],f=0,hp=(n[1]==3) and 1 or nil,
    st=(n[1]==4) and "hang" or nil,vy=0,arm=(n[1]==4) or nil,
    on=(n[1]==5) and false or nil,tr=(n[1]==6) and -1 or nil})
  end
  h.x=LV[lvn].sx*8
  h.y=16+LV[lvn].sr*8-10
  h.v=0
  h.s="run"
  h.tm=0
  h.blk=0
  h.lx=h.x
  ph="run"
  for f=1,900 do
   simstep()
   if st=="res" then break end
  end
  if win then w+=1 end
  st="res"
  -- rebuild objs for next run
  objs={}
  boot_presets()
 end
 objs={}
 boot_presets()
 st="res"
 return w
end

function boot_presets()
 local L=LV[lvn]
 for r=0,11 do
  local row=sub(L.rows[r+1],1,16)
  for c=0,15 do
   local ch=sub(row,c+1,c+1)
   local oy=16+r*8
   if ch=="^" then add(objs,{k=2,x=c*8,y=oy,c=0,f=0}) end
   if ch=="B" then add(objs,{k=3,x=c*8,y=oy,c=0,f=0,hp=1}) end
   if ch=="Y" then add(objs,{k=3,x=c*8,y=oy,c=0,f=0,hp=2}) end
   if ch=="R" then add(objs,{k=4,x=c*8,y=oy,c=0,f=0,st="hang",vy=0,arm=false}) end
   if ch=="K" then add(objs,{k=5,x=c*8,y=oy,c=0,f=0,on=false}) end
   if ch=="x" then add(objs,{k=6,x=c*8,y=oy,c=0,f=0,tr=-1}) end
  end
 end
end

function fin()
 st="res"
 local L=LV[lvn]
 if L.p==0 then
  win=(h.s=="die")
 else
  win=(h.s=="win")
 end
 if win then
  dset(lvn,1)
  if lvn>dget(0) then dset(0,lvn) end
  psfx(SND_WIN)
  pmusic(MUS_W)
 else
  psfx(SND_L)
  pmusic(MUS_L)
 end
end

function atksc()
 for o in all(objs) do
  if o.k==3 then
   local dx=o.x-(h.x+7)
   if dx>=-4 and dx<=16 and abs(o.y-h.y)<=12 then
    return true
   end
  end
 end
 return false
end

function hazsc()
 local px=h.x+16
 if not solidat(px,h.y+11) then return true end
 if solidat(px,h.y+6) or solidat(px,h.y+9) then return true end
 for o in all(objs) do
  if o.k==2 and px>=o.x and px<o.x+8 and h.y+2<o.y+8 and h.y+10>o.y then
   return true
  end
 end
 return false
end

function trigsw()
 local first=false
 for o in all(objs) do
  if o.k==5 and not o.on then
   o.on=true
   first=true
  end
 end
 if first then
  psfx(SND_SW)
  for o in all(objs) do
   if o.k==4 and o.st=="hang" then o.st="fall" o.vy=1 end
   if o.k==6 and o.tr~=99 and o.tr<0 then
    o.tr=12
   end
  end
 end
end

function updobj(o)
 if o.f>0 then o.f-=1 end
 if o.k==4 then
  if o.st=="hang" then
   if o.arm and h.s~="die" and h.s~="win" and abs((h.x+4)-(o.x+4))<10 then
    o.st="fall"
    o.vy=1
    psfx(SND_TRIG)
   end
  elseif o.st=="fall" then
   o.vy+=0.25
   if o.vy>4 then o.vy=4 end
   o.y+=o.vy
   if h.s~="die" and h.s~="win" and ov(o.x,o.y,8,8,h.x,h.y,7,10) then
    kill("crush")
    o.st="smash"
    o.f=20
    psfx(SND_THUD)
   end
   for b in all(objs) do
    if b~=o and b.k==3 and ov(o.x,o.y,8,8,b.x,b.y,8,8) then
     del(objs,b)
     o.st="smash"
     o.f=20
     psfx(SND_THUD)
     break
    end
   end
   if o.st=="fall" then
    for b in all(objs) do
     if b~=o and (b.k==1 or b.k==6) and ov(o.x,o.y,8,8,b.x,b.y,16,8) then
      del(objs,b)
      o.st="smash"
      o.f=20
      psfx(SND_THUD)
      break
     end
    end
   end
   if o.st=="fall" and (solidat(o.x+4,o.y+8) or o.y>108) then
    o.st="smash"
    o.f=20
    psfx(SND_THUD)
    for m in all(objs) do
     if m.k==5 and ov(o.x,o.y,8,8,m.x,m.y,8,8) then trigsw() end
    end
   end
  end
 elseif o.k==5 then
  if not o.on and h.s~="die" and h.s~="win" and ov(h.x,h.y,7,10,o.x,o.y,8,8) then
   trigsw()
  end
 elseif o.k==6 then
  if o.tr>=0 and o.tr<99 then
   o.tr-=1
   if o.tr<=0 then
    o.tr=99
    psfx(SND_BR)
   end
  end
 end
end

function updhero()
 if h.s=="die" or h.s=="win" then
  h.tm+=1
  if h.tm>40 then fin() end
  return
 end
 if h.s=="atk" then
  h.tm+=1
  if h.tm==8 then
   for i=#objs,1,-1 do
    local o=objs[i]
    if o.k==3 and o.x<h.x+24 and o.x+8>h.x-4 and abs(o.y-h.y)<14 then
     o.hp-=1
     if o.hp<=0 then
      del(objs,o)
      psfx(SND_BDIE)
     else
      psfx(SND_TRIG)
     end
    end
   end
  end
  if h.tm>14 then h.s="run" end
  return
 end
 if h.s=="run" and atksc() then
  h.s="atk"
  h.tm=0
  psfx(SND_SLASH)
  return
 end
 if h.s=="run" and wary() then
  h.s="wary"
  h.tm=0
  psfx(SND_UI)
  return
 end
 if h.s=="wary" then
  h.tm+=1
  if h.tm>45 then h.s="run" end
  return
 end
 if h.s=="run" and hazsc() then
  h.v=-3.8
  h.s="jump"
  psfx(SND_JUMP)
 end
 h.x+=0.75
 if solidat(h.x+7,h.y+6) or solidat(h.x+7,h.y+9) then
  if not solidat(h.x+7,h.y+1) and not solidat(h.x+7,h.y-6) and h.y>26 then
   h.y-=8
  else
   h.x=flr((h.x+7)/8)*8-7
  end
 end
 h.v+=0.2
 if h.v>4 then h.v=4 end
 h.y+=h.v
 if h.v>=0 and (solidat(h.x+1,h.y+10) or solidat(h.x+6,h.y+10)) then
  h.y=flr((h.y+10)/8)*8-10
  h.v=0
  h.s="run"
 elseif h.v>0.2 then
  h.s="fall"
 elseif h.v<-0.2 then
  h.s="jump"
 end
 if h.x<=h.lx+0.05 then
  h.blk+=1
  if h.blk>90 then kill("stall") return end
 else
  h.blk=0
 end
 h.lx=h.x
 if h.y>106 then kill("fall") return end
 for o in all(objs) do
  if o.k==2 and ov(h.x,h.y,7,10,o.x,o.y,8,8) then kill("spike") return end
  if o.k==3 and h.s~="atk" and ov(h.x,h.y,7,10,o.x,o.y,8,8) then kill("beast") return end
 end
 for o in all(objs) do
  if o.k==6 and o.tr<99 and h.s~="jump" and h.s~="fall"
   and ov(h.x,h.y+8,7,3,o.x,o.y,16,4) then
   if o.tr<30 then o.tr=30 end
  end
 end
 if h.x>=flagx then
  h.x=flagx
  h.s="win"
  h.v=0
  h.tm=0
  psfx(SND_FLAG)
 end
end

function simstep()
 for o in all(objs) do updobj(o) end
 for i=#objs,1,-1 do
  local o=objs[i]
  if o.k==4 and o.st=="smash" and o.f<=0 then
   deli(objs,i)
  end
 end
 if ph=="cue" then
  cue-=1
  if cue<=0 then
   ph="run"
   h.s="run"
  end
 else
  updhero()
 end
end
-- 30_build: cursor placement rules
function ow_of(k)
 if k==1 or k==6 then return 16 end
 return 8
end

function place()
 local L=LV[lvn]
 local cost=COST[tool]
 local w=ow_of(tool)
 local x=flr(cx/8)*8
 local y=flr(cy/8)*8
 if tool==4 then y=16 end
 if tool==5 and y>96 then y=96 end
 local ok=true
 local why="blocked"
 if pts<cost then
  ok=false
  why="need more pts"
 elseif y<16 or y>96 or x+w>128 then
  ok=false
  why="off stage"
 elseif not has_tool(tool) then
  ok=false
  why="not in this scene"
 elseif ov(x,y,w,8,h.x-2,h.y-2,11,14) then
  ok=false
  why="not the hero!"
 else
  for o in all(objs) do
   local ow=ow_of(o.k)
   local oy=o.k==6 and o.y or o.y
   if ov(x,y,w,8,o.x,oy,ow,8) then
    ok=false
    why="occupied"
    break
   end
  end
 end
 if ok then
  local o={k=tool,x=x,y=y,c=cost,f=25}
  if tool==3 then o.hp=1 end
  if tool==4 then o.st="hang" o.vy=0 o.arm=true end
  if tool==5 then o.on=false end
  if tool==6 then o.tr=-1 end
  add(objs,o)
  pts-=cost
  icd=6
  psfx(SND_PLACE)
 else
  msg=why
  mt=30
  psfx(SND_DENY)
 end
end

function has_tool(k)
 return find(pl,k)
end

function find(t,v)
 for x in all(t) do
  if x==v then return true end
 end
 return false
end

function ercyc()
 icd=6
 for i=#objs,1,-1 do
  local o=objs[i]
  if o.c>0 then
   local ow=ow_of(o.k)
   if cx>=o.x and cx<o.x+ow and cy>=o.y and cy<o.y+8 then
    pts+=o.c
    del(objs,o)
    psfx(SND_DEL)
    return
   end
  end
 end
 local idx=1
 for i=1,#pl do
  if pl[i]==tool then idx=i end
 end
 tool=pl[idx%#pl+1]
 psfx(SND_UI)
end
-- 40_draw: stage, hero, objects, cursor, hud
function dash(x,y,w,h,c)
 for i=x,x+w-1,3 do
  pset(i,y,c)
  pset(i,y+h-1,c)
 end
 for i=y,y+h-1,3 do
  pset(x,i,c)
  pset(x+w-1,i,c)
 end
end

function dstage()
 for y=16,111,2 do
  local hw=8+(y-16)*0.62
  rectfill(64-hw,y,64+hw,y+1,1)
 end
 for y=16,95,2 do
  local hw=(8+(y-16)*0.62)*0.45
  rectfill(64-hw,y,64+hw,y+1,5)
 end
 for r in all(sol) do
  rectfill(r[1],r[2],r[1]+r[3]-1,r[2]+r[4]-1,4)
  rectfill(r[1],r[2],r[1]+r[3]-1,r[2],9)
  local x=r[1]
  while x<r[1]+r[3] do
   rectfill(x,r[2]+1,x,r[2]+r[4]-1,2)
   x+=8
  end
 end
 local L=LV[lvn]
 local c=L.p==0 and 8 or 11
 pal(12,c)
 spr(42,flagx-2,56,1,2)
 spr(43,flagx-2,72,1,2)
 pal()
 rectfill(flagx-4,94,flagx+3,96,5)
 for o in all(objs) do
  dobj(o)
 end
end

function dobj(o)
 local hot=(o.f>0 and o.f<25)
 if st=="play" and ph=="build" and flr(cx/8)*8==o.x and flr((cy-16)/8)*8+16==o.y then
  hot=true
 end
 if o.k==1 then
  spr(32,o.x,o.y,2,1)
  if hot then dash(o.x,o.y,16,8,10) end
 elseif o.k==2 then
  spr(36,o.x,o.y)
  if hot then dash(o.x,o.y,8,8,10) end
 elseif o.k==3 then
  spr(38+flr(t/8)%4,o.x,o.y)
  if hot then dash(o.x,o.y,8,8,10) end
 elseif o.k==4 then
  if o.st=="hang" then
   spr(64,o.x,o.y)
   if hot then dash(o.x,o.y,8,8,10) end
  elseif o.st=="fall" then
   spr(65,o.x,o.y)
  else
   spr(66,o.x,o.y)
  end
 elseif o.k==5 then
  spr(o.on and 68 or 67,o.x,o.y)
  if hot then dash(o.x,o.y,8,8,10) end
 elseif o.k==6 then
  if o.tr==99 then return end
  local n=o.tr>=0 and 70 or 69
  spr(n,o.x,o.y,2,1)
  if o.tr>=0 then
   pset(o.x+4,o.y-2,8)
   pset(o.x+11,o.y-2,8)
  end
  if hot then dash(o.x,o.y-2,16,6,10) end
 end
end

function dhero()
 local x=h.x
 local y=h.y
 local n
 if h.s=="die" then
  spr(h.cau=="crush" and 10 or 7,x,y,1,2)
  return
 end
 if h.s=="win" then
  n=8+flr(t/10)%2
 elseif h.s=="atk" then
  n=h.tm<6 and 4 or 5
 elseif h.s=="jump" then
  n=2
 elseif h.s=="fall" then
  n=3
 elseif h.s=="ready" or h.s=="wary" then
  n=6
 else
  n=flr(t/6)%2
 end
 spr(n,x,y,1,2)
end

function dcur()
 if st~="play" or ph~="build" then return end
 local w=ow_of(tool)
 local x=flr(cx/8)*8
 local y=flr(cy/8)*8
 if tool==4 then y=16 end
 local c=10
 if pts<COST[tool] then c=8 end
 if ov(x,y,w,8,h.x-2,h.y-2,11,14) then c=8 end
 dash(x,y,w,8,c)
 local mx=flr(cx)
 local my=flr(cy)
 pset(mx-3,my,c)
 pset(mx+3,my,c)
 pset(mx,my-3,c)
 pset(mx,my+3,c)
end

function dcurtain()
 rectfill(0,0,127,15,8)
 rectfill(0,112,127,127,8)
 for x=0,127,8 do
  rectfill(x,0,x+3,15,4)
  rectfill(x,112,x+3,127,4)
 end
 rectfill(0,15,127,15,10)
 rectfill(0,112,127,112,10)
end

function dhud()
 local L=LV[lvn]
 local nm=L.p==0 and "black: he must die" or "white: he must live"
 print(nm,2,2,L.p==0 and 8 or 7)
 local px=127-L.pts*5
 print("pts",px-14,2,6)
 for i=1,L.pts do
  spr(i<=pts and 56 or 57,px+(i-1)*5,2)
 end
 local ix=2
 for k in all(pl) do
  spr(57+k,ix,9)
  print(COST[k],ix+9,11,6)
  ix+=15
 end
 print(">"..TN[tool],ix+2,10,10)
 if ph=="cue" then
  local s=cue>20 and "stand by..." or "action!"
  pc(s,44,10)
 end
 if ph=="pause" then
  pc("paused - x resume",58,10)
 end
 if mt>0 then
  pc(msg,60,8)
 end
end

function pc(s,y,c)
 print(s,64-#s*2,y,c)
end

function pc2(s,x,y,c)
 print(s,x-#s*2,y,c)
end
-- 50_screens: title, select, story, result, ending
function dtitle()
 dstage()
 spr(52,72,30)
 spr(6,58,34,1,2)
 dcurtain()
 print("the director",64-23,20,8)
 print("the director",64-24,20,10)
 pc("you never control the hero",28,6)
 pc("14 scenes  6 tools  1 script",40,5)
 rectfill(24,56,104,92,0)
 rect(24,56,104,92,10)
 pc("press o to begin",70,7)
 print("you never control the hero",2,114,7)
 print("the curtain rises on you",2,121,6)
end

function dfig(x,y)
 rectfill(x-2,y+3,x-1,y+7,13)
 rectfill(x,y+4,x+6,y+7,7)
 rectfill(x,y,x+6,y+3,7)
 rectfill(x,y+2,x+6,y+2,12)
 rectfill(x+1,y+8,x+2,y+9,13)
 rectfill(x+4,y+8,x+5,y+9,13)
end

function dselect()
 dcurtain()
 print("scene select",40,3,10)
 local unlocked=dget(0)
 if unlocked<1 then unlocked=1 end
 for i=1,14 do
  local col=(i-1)%7
  local row=flr((i-1)/7)
  local x=8+col*17
  local y=30+row*30
  local L=LV[i]
  local open=i<=unlocked
  local clr=dget(i)==1
  rectfill(x,y,x+13,y+18,open and (L.p==0 and 2 or 1) or 0)
  rect(x,y,x+13,y+18,open and (L.p==0 and 8 or 11) or 5)
  if open then
   print(i,x+5,y+5,clr and 10 or 7)
   if clr then pset(x+10,y+15,10) end
  else
   print("x",x+5,y+5,5)
  end
  if sel==i then
   dash(x-1,y-1,16,21,10)
  end
 end
 pc("arrows pick   o read   x title",100,6)
end

function dstorycard()
 dcurtain()
 rectfill(8,40,119,80,0)
 rect(8,40,119,80,10)
 local L=LV[lvn]
 pc2("scene "..lvn.." / 14",14,46,6)
 pc2(L.p==0 and "black: he must die" or "white: he must live",14,54,L.p==0 and 8 or 11)
 -- wrap goal
 print(L.goal,14,64,7)
 print(L.story,14,72,6)
 pc("o: places, please",90,10)
end

function dres()
 rectfill(8,40,119,92,0)
 rect(8,40,119,92,10)
 local L=LV[lvn]
 local l1,l2,l3
 if win then
  l1=L.p==0 and "the hero falls" or "the hero lives"
  l2=L.p==0 and "black scene: clear" or "white scene: clear"
 else
  l1=L.p==0 and "he reached the flag" or "the hero dies"
  l2=L.p==0 and "black scene: failed" or "white scene: failed"
 end
 l3=attrib()
 pc(l1,48,win and 10 or 8)
 pc(l2,58,7)
 print(l3,12,68,6)
 print(cause_line(),12,76,5)
 if win and lvn==14 then
  pc("o: the finale",88,10)
 else
  pc("o: again   x: scenes",88,6)
 if s100>=0 then
  pc("100 runs: "..s100.."% clear",78,10)
 end
 end
end

function attrib()
 if h.cau~="" and h.cau~="win" then
  return "his end: "..h.cau
 end
 if #placed()==0 then
  return "the stage stood still"
 end
 return "stagecraft pieces: "..#placed()
end

function placed()
 local r={}
 for o in all(objs) do
  if o.c>0 then r[#r+1]=o end
 end
 return r
end

function cause_line()
 if not win and h.cau~="" then
  local near=""
  local bx=h.x
  local by=h.y
  for o in all(placed()) do
   if abs(o.x-bx)<24 and abs(o.y-by)<24 then
    near=TN[o.k]
    break
   end
  end
  if near~="" then return "your "..near.." was there" end
  return "the script needed no help"
 elseif not win then
  return "he outran your imagination"
 end
 return ""
end

function dending()
 dcurtain()
 local n=endn
 if n<=4 then
  rectfill(8,44,119,84,0)
  rect(8,44,119,84,8)
  pc(STORY_END[n],60,7)
 elseif n==5 then
  dstage()
  -- hero looks back at the player
  local x,y=60,70
  rectfill(x-2,y+3,x-1,y+7,13)
  rectfill(x,y+4,x+6,y+7,7)
  rectfill(x,y,x+6,y+3,7)
  rectfill(x,y+2,x+6,y+2,12)
  pset(x+1,y+1,0)
  pset(x+5,y+1,0)
  rectfill(x+1,y+8,x+2,y+9,13)
  rectfill(x+4,y+8,x+5,y+9,13)
  pc("he is looking at you",40,7)
 else
  pc("the director",54,8)
  pc("fin",70,10)
  pc("o: title",86,6)
 end
end
-- 70_audio: guarded hooks (ids matched to assets/ASSETS.md)
function psfx(id)
 if snd and id then sfx(id) end
end

function pmusic(id)
 if snd and id then music(id) end
end
__gfx__
00077000000770000007700000077000000770000007700000077000000000000007700000077000000000000000000000000000000000000000000000000000
00777c0000777c0000777c0000777c0000777c0000777c0000777c000000000000777c0000777c00000000000000000000000000000000000000000000000000
00077700000777000007770000077700000777000007776000077700000000000007770000077700000000000000000000000000000000000000000000000000
00d7770000d7770000d7770070d7770760d7770000d7776000d777000000000070d7770770d77707000000000000000000000000000000000000000000000000
0dd777000dd777000dd777000dd7770066d777000dd777660dd77700000000000dd77707ddd77707000000000000000000000000000000000000000000000000
0dd777000dd777000dd777000dd777000dd777000dd777600dd77700000000000dd77770d0d77770000000000000000000000000000000000000000000000000
0dd777000dd777000dd777000dd777000dd777000dd777000dd77700000000000dd777000dd77700000000000000000000000000000000000000000000000000
007777000077770000777700007777000dd777000dd777000dd77700000000000dd777000dd77700000000000000000000000000000000000000000000000000
00077000000770000077770000077000007777000077770000777700008880000077770000777700000000000000000000000000000000000000000000000000
00700700007777000770077000700700000770000007700000077000085758000007700000777700000000000000000000000000000000000000000000000000
07000070007007000700007007000070007007000070070000077000877777500007700007700770000000000000000000000000000000000000000000000000
070000700070070007000070070000700070070007000070000770000dd777600070070007000070088888800000000000000000000000000000000000000000
700000700070070000000000700000070070070007000070007007000ddd77000700007070000007877777780000000000000000000000000000000000000000
7700007707700770000000000000000007700770000000000770077000ddd0000700007000000000850705780000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000800000807700007700000000877777780000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000088088000000000000000000088008800000000000000000000000000000000000000000
999999999999999999999999999999990700070008000800000000000000000000000000000ee000006ccccc00600000000a0000aa0000aa0000000000000000
44444444444444444444444444444444067067000680680000eeee0000eeee000000000000e0e0e0006cccc000600000000a0000a000000a0070000000000000
4444224444224444446444644446444606676670066866800e0ee0e00e5ee5e00eeeeee000eeee00006ccccc00600000000a0000000000000707007006000060
444444444444444444444444444444440666666006666660eeeeeeeeeeeeeeeee0eeee0e0eeeee00006cccc000600000a00aa00a000000000070770000606000
224444444444442224444442442442446666666666686666eee0eeeeeee0eeeeeeeeeeeeeeeeeeee006ccccc00600000a00aa00a000000007077770006006060
444444444444444444444444444444446666666666666666eeeeeeeeeeeeeeeeeee0eeeeeee0eeee0060000000600000000a0000000000000077700700606000
4422444444442244464446446444644455555555555855550e0000e00e0000e0eeeeeeeeeeeeeeee0060000000464000000a0000a000000a0700770006000060
55555555555555555555555555555555000000000000000000000000000000000e0000e00e0000e00060000004464400000a0000aa0000aa0070000000000000
888888888888888800000000000000007777777788888888bbbbbbbb000a00000000000000000000000000000000000000000000000000000000000000000000
848484844848484800111100000000006767676781111118b111111b000a000000aaaa0000555500000000000070070000eeee00006666000000000609900990
888888888888888801111110000550007777777781111118b111111b0aaaaa000aaaaaa00555555009999990066066000e0ee0e0066666600000006004400440
848484844848484811111111005555000000000081111118b111111b000a00000aaaaaa0050000500444444006666660eeeeeeee665666660000060004200240
888888888888888811111111005555006666666681111118b111111b0a000a000aaaaaa0050000500422424066666666eee0eeee666666660555555504400440
aaaaaaaaaaaaaaaa01111110000550006766666681111118b111111ba00000a000aaaa00005555000444444055555555eeeeeeee066666605555555505500550
088008808800008800111100000000006667666681111118b111111b00000000000000000000000005555550000000000e0000e0005555000000000000000000
000880000800008000000000000000006666666688888888bbbbbbbb000000000000000000000000000000000000000000000000000000000000000000000000
00040000070000700707070700000000660000000999999000999999070000700999900000000000000000000000000000000000000000000000000000000000
00040000070000700066660000000006006000000444444000444444070000700444004000000000000000000000000000000000000000000000000000000000
00666600006666000666666000000060000600000464464000464464009999990440040400000000000000000000000000000000000000000000000000000000
066666600666666066666666000006000000a0000444444000044444004444440420040400000000000000000000000000000000000000000000000000000000
66566666665666666665666606666666066666660422442000044444004464440440040400000000000000000000000000000000000000000000000000000000
66666666666666660666666005555555055555550444444000044444004444440400040400000000000000000000000000000000000000000000000000000000
06666660066666600055550055555555555555550555555000055555005555550500505000000000000000000000000000000000000000000000000000000000
00666600006666000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
__sfx__
000c0000181501f160241602b15300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000800000c06005040030330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000600001c34018330122230000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000800001636008160040430000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000a00000e37006160020530003300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000400002e24034233000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000c000010141121420f1330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000c000024650286502b6603066300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000c000028150231501e1401813300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000600002823000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00080000282402f243000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0008000012250122400e2500e24300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00060000183201e330242412a23300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000800000a05006033000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00050000343502e340286330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00080000243501c340143300c32300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000c00000815208150071430000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000c00003065034650376503c64300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00080000142600e243000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000a000018131121410c1510815100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000600001e350123400a0330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000a0000261711e161161510e14108133000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000001106000000000000000018040000000000000000160600000000000000001d040000000000000000140600000000000000001b0400000000000000001106000000000000000018043000000000000000
0010000019060000000000000000110400000000000000001806000000000000000010040000000000000000160600000000000000000f0400000000000000001106000000000000000018043000000000000000
0010000000000186401b6401f6300000000000000000000000000186401b6401f6300000000000000000000000000186401b6401f6300000000000000000000000000186401c6401f63000000000000000000000
001000002915000000000000000027150000000000000000241500000000000000002214300000000000000024150000000000000000291500000000000000002b16000000000000000029153000000000000000
000c00000514000000000000513000000000000000000000051400000000000051300000000000000000000005140000000000005130000000000000000000000514000000000000513000000000000000000000
000c0000182301b2201f230222201f2301b2201823000000192301c2202023023220202301c2201923000000182301b2201f230222201f2301b2201823000000192301c2202023023220202301c2201923000000
000c00001234000000000000000000000000000000000000123400000000000000000000000000000000000012340000000000000000000000000000000000001234000000000000000000000000000000000000
000c000024650286502b66000000306630000000000000002b6502f65032660000003767300000000000000024650286502b66000000306630000000000000002b6502f650326600000037673000000000000000
000c00000c050000000000013040000000000000000000000c050000000000013040000000000000000000000c050000000000013040000000000000000000000c05000000000001304000000000000000000000
000c0000000000000000000186401c6401f63000000000000000000000186401c6401f63000000000000000000000186401c6401f63000000000000000000000186401c6401f6300000000000000000000000000
001000000514205140051320513003142031400313203130021420214002132021300015200150001430000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0010000024150000000000000000221500000000000000001f1500000000000000001d1400000000000000001b150000000000000000181400000000000000001314000000000000000011133000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
__music__
01 20222341
00 20222341
00 21222341
02 21222341
01 24252641
00 24252641
00 24252641
02 24252641
00 28292741
00 28292741
04 28292741
00 2a412b41
04 2a412b41
