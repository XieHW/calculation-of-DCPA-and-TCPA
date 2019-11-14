'''
author:xhw
time:2019.11.6
theme:calculation of Distance ,true bearing ,dcpa,tcpa between two ships
'''

from math import *
class tarship():
    def __init__(self,lat,lon,cog,sog):
        self.lat=lat
        self.lon=lon
        self.cog=cog
        self.sog=sog
class refship():
    def __init__(self,lat,lon,cog,sog):
        self.lat=lat
        self.lon=lon
        self.cog=cog
        self.sog=sog

class Cal():
    def __init__(self,tar_ship,ref_ship):
        self.tar_lat=tar_ship.lat
        self.tar_lon=tar_ship.lon
        self.tar_cog=tar_ship.cog
        self.tar_sog=tar_ship.sog
        self.ref_lat=ref_ship.lat
        self.ref_lon=ref_ship.lon
        self.ref_cog=ref_ship.cog
        self.ref_sog=ref_ship.sog
        self.differ_lon=self.tar_lon-self.ref_lon#经差
        self.differ_cog=self.ref_cog-self.tar_cog
        self.differ_lon2=self.tar_lon-self.ref_lon
        self.ref_lat2=ref_ship.lat#存储本船纬度的正负号



    def dist(self):
        if self.ref_lat>=0 and self.ref_lat*self.tar_lat>=0:#本船纬度无论南北都是正值，他船与我船同名时为正值，异名时为负值
            self.ref_lat=self.ref_lat
            self.tar_lat=self.tar_lat
        elif self.ref_lat>=0 and self.ref_lat*self.tar_lat<0:#在这里把ref_lat的正负号都弄成了正值！error:这也是导致一开始算数不对的原因
            self.ref_lat=self.ref_lat
            self.tar_lat=self.tar_lat
        elif self.ref_lat<0 and self.ref_lat*self.tar_lat>=0:
            self.tar_lat=-self.tar_lat
            self.ref_lat=-self.ref_lat
        elif self.ref_lat<0 and self.ref_lat*self.tar_lat<0:
            self.tar_lat=-self.tar_lat
            self.ref_lat=-self.ref_lat
        if fabs(self.differ_lon)>=180:                           #经差超过180°时，用360°减去它
            self.differ_lon=360-fabs(self.differ_lon)
        D=acos(sin(radians(self.tar_lat))*sin(radians(self.ref_lat))+cos(radians(self.tar_lat))*cos(radians(self.ref_lat))*cos(radians(fabs(self.differ_lon))))#边的余弦公式
        #print("距离为：%s"%float(D*180/pi*60))                        #算两船距离
        return D*180/pi*60


    def true_bearing(self):
        #differ_lon=self.tar_lon-self.ref_lon                       #它船与本船的经差。注意：经差无论东西，一律正值
        if self.ref_lat >= 0 and self.ref_lat * self.tar_lat >= 0:  # 本船纬度无论南北都是正值，他船与我船同名时为正值，异名时为负值
            self.ref_lat = self.ref_lat
            self.tar_lat = self.tar_lat
        elif self.ref_lat >= 0 and self.ref_lat * self.tar_lat < 0:
            self.ref_lat = self.ref_lat
            self.tar_lat = self.tar_lat
        elif self.ref_lat < 0 and self.ref_lat * self.tar_lat >= 0:
            self.tar_lat = -self.tar_lat
            self.ref_lat = -self.ref_lat
        elif self.ref_lat < 0 and self.ref_lat * self.tar_lat < 0:
            self.tar_lat = -self.tar_lat
            self.ref_lat = -self.ref_lat
        if fabs(self.differ_lon) >= 180:  # 经差超过180°时，用360°减去它
            self.differ_lon = 360 - fabs(self.differ_lon)
            #这里的经差不能为0
        #d=self.dist()*pi/180
        #a2=cos(radians(self.tar_lat))*sin(radians(self.differ_lon))/sin(d)
       # print("方位角2：",asin(a2)*180/pi)
        TB=0
        if self.differ_lon==0 or self.differ_lon==180:#在同一条经线上时
            if self.ref_lat>self.tar_lat:
                p=180
            else:
                p=0
        else:
            a = tan(radians(self.tar_lat)) * cos(radians(self.ref_lat)) * 1 / sin(radians(fabs(self.differ_lon))) - sin(radians(self.ref_lat)) * 1 / tan(       #四联公式
                radians(fabs(self.differ_lon)))
            #a=(cos(radians(self.ref_lat))*tan(radians(self.tar_lat))-sin(radians(self.ref_lat))*cos(fabs(radians(self.differ_lon))))/sin(fabs(radians(self.differ_lon)))
            if a==0:
                a=0.00001
            p = (atan(1/a))*180/pi
           # print("p:%s"%p)#算的这个数没有问题,这个是半圆周法
         #求算经差，这个是为了后面的单位转换
        if self.differ_lon2>180:#求取经差的正负号
            self.differ_lon2=-(360-self.differ_lon2)
        elif self.differ_lon2<-180:
            self.differ_lon2=(360+self.differ_lon2)
        if self.ref_lat2>=0:                 #转换为圆周法
            if self.differ_lon2 >=0:
                if p > 0:
                    TB = p
                elif p<0:
                    TB = 180 + p
            elif self.differ_lon2 < 0:
                if p > 0:
                    TB = 360 - p
                elif p<0:
                    TB = 180 - p
        elif self.ref_lat2<0:
            if self.differ_lon2>=0:
                if p>0:
                    TB=180-p
                elif p<0:
                    TB=-p
            elif self.differ_lon2<0:
                if p>0:
                    TB=180-p
                else:
                    TB=360-fabs(p)
        #print("TB:%s"%TB)
        #print("方位角为：%s" % (TB))
        return TB

    def cal_dcpa(self):
        if self.differ_cog>=0:
            b=self.differ_cog
        else:
            b=360+self.differ_cog
        #print("b:%s"%b)
        a=self.tar_sog*self.tar_sog+pow(self.ref_sog,2)-2*self.ref_sog*self.tar_sog*cos(radians(b))
        TB=self.true_bearing()
        d=fabs(TB-self.ref_cog)
        if d<=180:
            Q=d
        elif d>180:
            Q=360-d
        vx=sqrt(a)
        if self.ref_sog==0 or self.tar_sog==0:#避免船速为0
            self.ref_sog=0.001
            self.tar_sog=0.001
        if vx <0.00001:#避免相对速度为0，导致程序出错
            vx = 0.0000001
        f=(pow(vx,2)+pow(self.ref_sog,2)-pow(self.tar_sog,2))/(2*self.ref_sog*vx)

        alpha=acos(f)*180/pi                  #求相对速度的角
        #print("alpha:",alpha)
        D=self.dist()

        if b==0:                              #如果他们相对航向为0
            dcpa=D/60
            tcpa=0
        elif b<=180:
            dcpa=D*sin(radians(fabs(Q-alpha)))
            tcpa=D*cos(radians(Q-alpha))/vx
        else:
            dcpa=D*sin(radians(fabs(Q+alpha)))
            tcpa=D*cos(radians(Q+alpha))/vx

        if vx<0.000001:
            tcpa=0                     #如果两船相对静止，让他们的最近会遇时间为0
        elif vx<0.000001 and self.ref_sog<0.0001:
            tcpa=10000000
        #print("dcpa:%s,tcpa:%s"%(fabs(dcpa*60),tcpa*60*60))#dcpa的单位为分，也就是海里，tcpa的单位是分钟（先从度转化成分，再转成分钟）
        return dcpa,tcpa*60

#分别输入：纬度、经度、航向角、航速
#ownship=refship(-(8+6/60),-(112+30.5/60),180,15)                 #综上所述，距离和方位角的计算都是按照球面三角形的方法来计算。随着维度的升高，两点间的长度会变小，这也是
#targetship=tarship(19+13/60,138+46.5/60,0,15)                    #00的时候距离很正常，随着纬度的上升而减少；
#验证距离方位
#ownship=refship(17+15/60,108+26/60,0,10)
#targetship=tarship(23+20/60,134+47/60,0,10)

#验证dcpa,tcpa
ownship=refship(45,44,270,15)
targetship=tarship(45,43,90,15)


d=Cal(targetship,ownship)
distance=d.dist()       #海里
TB=d.true_bearing()     #圆周法，单位为：度
DCPA,TCPA=d.cal_dcpa()  #单位分别是：海里，分钟

print("距离：%s"%distance)
print("方位：%s"%TB)
print("DCPA:%s,TCPA:%s"%(DCPA,TCPA))
