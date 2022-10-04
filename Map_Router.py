import pygame as pg
import Maths as M
import sys
pg.init()

W = 1920
H = 1080

display = pg.display.set_mode((0,0), pg.FULLSCREEN)
pg.display.set_caption(' ')

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
magenta = (255,0,255)

scale = 1
scalep = 2**scale

zoom = 1.1
y_min = 0
y_max = 1
x_min = 0.5*(1-W/H)
x_max = 0.5*(1+W/H)
rangx = x_max-x_min
rangy = y_max-y_min

pan = False

extra = 2

def disp(pnt):
    return((round((pnt[0]-x_min)*(W/rangx)), H-round((pnt[1]-y_min)*(H/rangy))))

def coor(pnt):
    return((round((rangx/W)*pnt[0]+x_min,5), round((rangy/H)*(H-pnt[1])+y_min,5)))

# def Blit(Mp,size,Pos):
#     MW,MH = Mp.get_width(), Mp.get_height()
#     if 2*size/MW < rangx < size:
#         xpx,ypx = MW*rangx/size+extra, MW*rangy/size+extra
#         pxW = (size*W)/(rangx*MW)
#         xv,yv = MW*(x_min-Pos[0])/size, MW*(Pos[1]-y_max)/size
        
#         surf = pg.Surface((int(xpx),int(ypx)), pg.SRCALPHA)
            
#         surf.blit(Mp, (0,0), (int(xv), int(yv), int(xpx), int(ypx)))
#         display.blit(pg.transform.scale(surf,(int((W+extra*pxW)*(int(xpx)/xpx)),int((H+extra*pxW)*(int(ypx)/ypx)))), (int(pxW*(int(xv)-xv)),int(pxW*(int(yv)-yv))))
#     elif 2*size/MW >= rangx:
#         xv,yv = int(MW*(x_min+rangx/2-Pos[0])/size), int(MW*(Pos[1]-y_max+rangy/2)/size)
#         if 0 <= xv < MW and 0 <= yv < MH:
#             col = Mp.get_at((xv,yv))
#         else:
#             col = black
#         display.fill(col)
#     else:
#         display.blit(pg.transform.scale(Mp,(int(W*size/rangx),int(W*size*(MH/MW)/rangx))), disp(Pos))

def Blit(Mp,size,Pos):
    display.blit(pg.transform.scale(Mp,(int(W*size/rangx)+1,int(W*size*(Mp.get_height()/Mp.get_width())/rangx)+1)), disp(Pos))

def Quit():
    pg.quit()

    with open('Maps/Points.txt', 'w') as file:    
        for p in P:
            file.write(str(p[0])+','+str(p[1])+':')

    with open('Maps/Lines.txt', 'w') as file:
        for l in L:
            file.write(str(l[0])+','+str(l[1])+':')
    
    sys.exit()

with open('Maps/Points.txt', 'r') as file:  
    P = [tuple([float(x) for x in s.split(',')]) for s in file.read().split(':')[:-1]]

with open('Maps/Lines.txt', 'r') as file:
    L = [tuple([int(x) for x in s.split(',')]) for s in file.read().split(':')[:-1]]

def Draw():
    display.fill(black)

    if sel != -1:
        P[sel] = coor(pos)

    for y in range(max(0,int(y_min*scalep)),min(scalep,int(y_max*scalep)+1)):
        for x in range(max(0,int(x_min*scalep)),min(scalep,int(x_max*scalep)+1)):
            Blit(pg.image.load('Maps/'+str(scale-1)+'/'+str(x)+'_'+str(y)+'.jpg'), 1/scalep, (x/scalep,(y+1)/scalep))

    if draw != -1:
        pg.draw.line(display, black, disp(P[draw]), pos, 2)

    if connect:
        for l in L:
            if l[0] in INC or l[1] in INC:
                col = black
            else:
                col = red
            pg.draw.line(display, col, disp(P[l[0]]), disp(P[l[1]]), 2)
        for p in P:
            if P.index(p) in INC:
                col = black
            else:
                col = red
            pg.draw.circle(display, col, disp(p), 5)

    else:
        if show:
            for l in L:
                col = black
                if l[0] in path and l[1] in path:
                    col = red
                pg.draw.line(display, col, disp(P[l[0]]), disp(P[l[1]]), 2)
            for i,p in enumerate(P):
                col = black
                if i in path:
                    col = red
                if i in end_points:
                    col = green
                pg.draw.circle(display, col, disp(p), 5)
        else:
            for i in range(len(path)-1):
                pg.draw.line(display, red, disp(P[path[i]]), disp(P[path[i+1]]), 2)
            for i in path:
                pg.draw.circle(display, red, disp(P[i]), 5)
            hov_ind = sorted(zip([M.Dist(disp(p),pos) for p in P], [i for i in range(len(P))]))[0][1]
            pg.draw.circle(display, black, disp(P[hov_ind]), 5)
            for i in end_points:
                pg.draw.circle(display, green, disp(P[i]), 5)

    if cntrl and mark != -1:
        p1 = disp(mark)
        pg.draw.circle(display, red, p1, 6)
        pg.draw.circle(display, red, pos, 6)
        pg.draw.line(display, red, disp(mark), pos, 3)
        pg.draw.rect(display, white, [0,0,350,50])
        display.blit(font.render(str(round(4085*M.Dist(mark,coor(pos)),8)),True,black),(20,8))

    if alt and CPL:
        display.blit(font.render(str(CPL[0]),True,black),disp(P[CPL[0]]))

    # for y in range(scalep+1):
    #     pg.draw.line(display, white, disp((0,y/scalep)), disp((1,y/scalep)), 2)
    # for x in range(scalep+1):
    #     pg.draw.line(display, white, disp((x/scalep,0)), disp((x/scalep,1)), 2)
                
    pg.display.update()

sel = -1
draw = -1

shift = False
cntrl = False
mark = -1
connect = False
alt = False
INC = []
end_points = []
path = []
show = False

font = pg.font.SysFont('Arial', 30)

while True:
    pos = pg.mouse.get_pos()
    CPL = [tpp[1] for tpp in sorted([tp for tp in zip([M.Dist(disp(p),pos) for p in P], [i for i in range(len(P))]) if tp[0] < 25])]
    for event in pg.event.get():
        CLLP = []
        cpos = coor(pos)
        for l in L:
            c = ((cpos[0]-P[l[0]][0])*(P[l[1]][0]-P[l[0]][0]) + (cpos[1]-P[l[0]][1])*(P[l[1]][1]-P[l[0]][1])) / ((P[l[1]][0]-P[l[0]][0])**2 + (P[l[1]][1]-P[l[0]][1])**2)
            if 0 < c < 1:
                CLLP.append((P[l[0]][0]+c*(P[l[1]][0]-P[l[0]][0]), P[l[0]][1]+c*(P[l[1]][1]-P[l[0]][1])))
            else:
                CLLP.append((-1,-1))
        CLL = [i for i in range(len(L)) if M.Dist(disp(CLLP[i]),pos) < 15]
        
        if event.type == pg.QUIT:
            Quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                Quit()
            elif event.key == pg.K_LSHIFT:
                shift = True
            elif event.key == pg.K_LCTRL:
                cntrl = True
            elif event.key == pg.K_LALT:
                alt = True
            elif event.key == pg.K_s:
                show = not show
            elif event.key == pg.K_c and CPL:
                connect = True
                layer = INC = [CPL[0]]
                while True:
                    new = []
                    for l in L:
                        if l[0] in layer and l[1] not in INC:
                            new.append(l[1])
                            INC.append(l[1])
                        elif l[1] in layer and l[0] not in INC:
                            new.append(l[0])
                            INC.append(l[0])
                    if new == []:
                        break
                    layer = [i for i in new]
            elif event.key == pg.K_RETURN and len(end_points) == 2:
                if path and path[-1] == end_points[1]:
                    path = []
                    end_points = []
                else:
                    out = [[10**9,-1] for i in range(len(P))]
                    inn = [[] for i in range(len(P))]
                    cur = end_points[0]
                    out[cur][0] = 0
                    cons = [[] for i in range(len(P))]
                    for l in L:
                        cons[l[0]].append(l[1])
                        cons[l[1]].append(l[0])
                    while cur != end_points[1]:
                        for con in cons[cur]:
                            if out[con]:
                                new_d = out[cur][0]+M.Dist(P[cur], P[con])
                                if new_d < out[con][0]:
                                    out[con] = [new_d, cur]
                        inn[cur] = out[cur]
                        out[cur] = []
                        cur = out.index(min([x for x in out if x]))

                    path.append(cur)
                    cur = out[cur][1]
                    while cur != -1:
                        path.append(cur)
                        cur = inn[cur][1]
                    path = path[::-1]
                            
            elif event.key == pg.K_TAB:
                draw = -1
            elif event.key == pg.K_SPACE:
                if CPL:
                    del P[CPL[0]]
                    L = [(l[0]-int(l[0]>CPL[0]), l[1]-int(l[1]>CPL[0])) for l in L if CPL[0] not in l]
                    if CPL[0] == draw:
                        draw = -1
                elif CLL:
                    del L[CLL[0]]
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LSHIFT:
                shift = False
            elif event.key == pg.K_LCTRL:
                cntrl = False
                mark = -1
            elif event.key == pg.K_LALT:
                alt = False
            elif event.key == pg.K_RETURN:
                connect = False
                INC = []
        elif event.type == pg.MOUSEBUTTONDOWN:
            but = event.dict['button']
            if but == 1 and shift:
                but = 3
                
            if but == 1:
                if CPL == [] or (not show and not alt):
                    pan = True
                    rel = pg.mouse.get_rel()
                elif alt:
                    if len(end_points) == 2:
                        end_points = [CPL[0]]
                        path = []
                    else:
                        end_points.append(CPL[0])
                else:
                    sel = CPL[0]
            elif but == 2 and CPL:
                del P[CPL[0]]
                L = [(l[0]-int(l[0]>CPL[0]), l[1]-int(l[1]>CPL[0])) for l in L if CPL[0] not in l]
            elif but == 3:
                if cntrl:
                    mark = coor(pos)
                elif CPL == []:
                    if CLL == []:
                        P.append(coor(pos))
                    else:
                        P.append(tuple([round(x,5) for x in CLLP[CLL[0]]]))
                        L.append((L[CLL[0]][0],len(P)-1))
                        L.append((L[CLL[0]][1],len(P)-1))
                        if draw != -1:
                            L.append((draw,len(P)-1))
                        del L[CLL[0]]
                        draw = len(P)-1
                    if draw != -1:
                        new = sorted((draw,len(P)-1))
                        if new not in L and new[0] != new[1]:
                            L.append(new)
                        draw = len(P)-1
                else:
                    if draw != -1:
                        new = sorted((draw,CPL[0]))
                        if new not in L and new[0] != new[1]:
                            L.append(new)
                    draw = CPL[0]
            elif but in [4,5]:
                z = zoom**(but*2-9)
                xp = (event.pos[0]/W)*rangx+x_min
                yp = ((H-event.pos[1])/H)*rangy+y_min
                x_min = x_min+(1-z)*(xp-x_min)
                x_max = x_max-(1-z)*(x_max-xp)
                y_min = y_min+(1-z)*(yp-y_min)
                y_max = y_max-(1-z)*(y_max-yp)
                rangx = x_max-x_min
                rangy = y_max-y_min
                scale = int(max(1,min(7,2.5-M.Log(rangx,2))))
                scalep = 2**scale
            elif but == 7:
                draw = -1
        elif event.type == pg.MOUSEBUTTONUP:
            sel = -1
            but = event.dict['button']
            if but == 1:
                pan = False
        elif event.type == pg.MOUSEMOTION:
            if pan:
                rel = pg.mouse.get_rel()
                dx = rel[0]*(rangx/W)
                dy = rel[1]*(rangy/H)
                x_min -= dx
                x_max -= dx
                y_min += dy
                y_max += dy
                

    Draw()
