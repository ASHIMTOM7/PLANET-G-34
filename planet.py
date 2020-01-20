import pygame
pygame.init()

sw=600
win = pygame.display.set_mode((sw,480))

pygame.display.set_caption("PLANET G-34")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')


clock = pygame.time.Clock()


class player(object):
    def __init__(self,x,y,width,height,left,right):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = left
        self.right = right
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.visible=True
        self.health=10
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0

            if not(self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                    self.walkCount +=1
            else:
                if self.left:
                    win.blit(walkLeft[0], (self.x, self.y))
                else:
                    win.blit(walkRight[0], (self.x, self.y))
            self.hitbox=(self.x+17,self.y+11,29,52)
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def hit(self):
        if self.health>0:
            self.health-=1
        else:
            self.visible=False


class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 12 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)



def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    man2.draw(win)
    for bullet in bullets2:
        bullet.draw(win)
    pygame.display.update()


#mainloop
man = player(50, 410, 64,64,True,False)
man2=player(sw-50-man.vel,410,64,64,False,True)
bullets = []
bullets2=[]
run = True
while run:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    

#bullets of 1st man
    if man.visible:       
        for bullet in bullets:
            if bullet.y-bullet.radius<man2.hitbox[1]+man2.hitbox[3] and bullet.radius+bullet.y>man2.hitbox[1]:
                if bullet.x+bullet.radius>man2.hitbox[0] and bullet.x-bullet.radius<man2.hitbox[0]+man2.hitbox[2]:
                    man2.hit()
                    bullets.pop(bullets.index(bullet))

            if bullet.x < sw and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))


#bullets of 2nd man
    if man2.visible:
        for bullet2 in bullets2:
            if bullet2.y-bullet2.radius<man.hitbox[1]+man.hitbox[3] and bullet2.radius+bullet2.y>man.hitbox[1]:
                if bullet2.x+bullet2.radius>man.hitbox[0] and bullet2.x-bullet2.radius<man.hitbox[0]+man.hitbox[2]:
                    man.hit()
                    bullets2.pop(bullets2.index(bullet2))

            if bullet2.x < sw and bullet2.x > 0:
                bullet2.x += bullet2.vel
            else:
                bullets2.pop(bullets2.index(bullet2))


    keys = pygame.key.get_pressed()


#1stman movement codes starts from here
    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 1:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 4, (255,20,147), facing))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < sw - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

#2ndman movement codes starts from here


    if keys[pygame.K_f]:
        if man2.left:
            facing2 = -1
        else:
            facing2 = 1
            
        if len(bullets2) < 1:
            bullets2.append(projectile(round(man2.x + man2.width //2), round(man2.y + man2.height//2), 4, (255,20,147), facing2))

    if keys[pygame.K_a] and man2.x > man2.vel:
        man2.x -= man2.vel
        man2.left = True
        man2.right = False
        man2.standing = False
    elif keys[pygame.K_d] and man2.x < sw - man2.width - man2.vel:
        man2.x += man2.vel
        man2.right = True
        man2.left = False
        man2.standing = False
    else:
        man2.standing = True
        man2.walkCount = 0
        
    if not(man2.isJump):
        if keys[pygame.K_w]:
            man2.isJump = True
            man2.walkCount = 0
    else:
        if man2.jumpCount >= -10:
            neg = 1
            if man2.jumpCount < 0:
                neg = -1
            man2.y -= (man2.jumpCount ** 2) * 0.5 * neg
            man2.jumpCount -= 1
        else:
            man2.isJump = False
            man2.jumpCount = 10
            

            
    redrawGameWindow()

pygame.quit()


