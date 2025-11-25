import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {                    #練習１
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横方向、縦方向）
    画面内ならTrue,画面外ならFalse
    """
    yoko,tate=True,True
    if rct.left < 0 or WIDTH < rct.right:#横方向判定
        yoko=False
    if rct.top<0 or HEIGHT < rct.bottom:#縦方向判定
        tate=False
    return yoko,tate



def gameover(screen: pg.Surface) -> None:
    """
    画面をブラックアウトし，泣くこうかとん＋Game Overを5秒表示する。
    """
    black = pg.Surface((WIDTH,HEIGHT))
    black.fill((0, 0, 0))
    black.set_alpha(200) # 半透明黒
    screen.blit(black,(0,0))

    font = pg.font.Font(None, 80)#ゲームオーバー表示
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH//2,HEIGHT//2))
    screen.blit(txt,txt_rct)

    cry_img = pg.image.load("fig/8.png")#こうかとん画像
    screen.blit(cry_img,[txt_rct.left-70, txt_rct.top-10])#右こうかとん
    screen.blit(cry_img,[txt_rct.right+20, txt_rct.top-10])#左こうかとん

    pg.display.update()

    time.sleep(5)#5秒間表示


def init_bb_imgs() -> tuple[list[pg.Surface],list[int]]:
    """
    段階的に爆弾が大きくなるsurfaceリストと加速度リストを返す。
    """
    bb_imgs=[]
    for r in range(1,11):
        bb_img=pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs=[a for a in range(1,11)]
    return bb_imgs,bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 半径10の赤い円を描画
    bb_img.set_colorkey((0, 0, 0))  # 黒色を透過色に設定
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾縦座標
    vx, vy = +5, +5  # 爆弾の横速度，縦速度
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs,bb_accs=init_bb_imgs()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):#こうかとんと爆弾が衝突
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=mv[0] #横方向の移動量
                sum_mv[1]+=mv[1] #縦方向の移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct)!=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        yoko, tate =check_bound(bb_rct)
        if not yoko: #横はみだし
            vx *= -1
        if not tate: #縦はみだし
            vy *= -1
        avx=vx*bb_accs[min(tmr//500,9)]
        bb_img=bb_imgs[min(tmr//500,9)]
        avy=vy*bb_accs[min(tmr//500,9)]
        bb_rct.width=bb_img.get_rect().width
        bb_rct.height=bb_img.get_rect().height
        bb_rct.move_ip(avx, avy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
