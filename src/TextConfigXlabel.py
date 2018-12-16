#-*- coding: utf-8 -*-

######################################
#当X轴的坐标太长，会重叠，此程序用来将x轴的
# 刻度进行一定角度的旋转；#
######################################
from pylab import *

t = arange(-4*pi, 4*pi, 0.01)

y = sin(t)/t
fig = plt.figure(figsize=(10.0, 6.0))
ax = plt.subplot2grid((1,1), (0, 0))
ax.plot( t, y )

plt.title('test')

plt.xlabel(u'\u2103',fontproperties='SimHei')
plt.ylabel(u'幅度',fontproperties='SimHei')#也可以直接显示中文。

plt.setp(ax.xaxis.get_majorticklabels(), rotation=45 )

plt.show()

