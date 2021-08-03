#! /usr/bin/env python3
# plot show growth of NAAN registry

tlogdir = "/apps/n2t/tlog"
naans_infile = tlogdir + '/naan_dates'
naans_image_file = 'naan_growth.png'

import numpy as np
import matplotlib
import matplotlib.font_manager as font_manager
from matplotlib import pyplot as plt

# To get font to take, you may have to clear cache first (per stackoverflow):
#    fc-cache -fv
#    rm -fr ~/.cache/matplotlib/
#fontpath = '/apps/n2t/sv/cur/apache2/htdocs/e/fonts'
#fontpath = '/apps/n2t/sv/cur/apache2/htdocs/e/fonts/Humor-Sans.ttf'
#prop = font_manager.FontProperties(fname=fontpath)
#matplotlib.rcParams['font.family'] = prop.get_name()

import datetime

#plt.xkcd()

#with open(tlogdir + "/naandates", encoding="utf-8") as infile:
with open(naans_infile, encoding="utf-8") as infile:
    x = []
    y = []
    i = 0
    for line in infile:
        i += 1
        # yyy wait, some dates (x-coord) repeat -- what does that do to plot?
        #     so date D will show with N, and show again with N+1 ...
        dt_obj = datetime.datetime.strptime(line, '%Y.%m.%d\n')
        x.append(dt_obj)
        #print('Date:', dt_obj.date())
        y.append(i)

#    'Growth in number of\nNAANS (ARK-assigning\norganizations) since 2001.'
#    '\n - marketing budget: $600.',
#    u'\n\u2013 marketing budget $600.', size=14,
plt.annotate(
    'Numbers of ARK-assigning\norganizations since 2001.', size=15,
    xy=(datetime.datetime(2003, 1, 1, 0, 0), 450))
#print("nd", x)

#x = np.array([datetime.datetime(2013, 9, 28, i, 0) for i in range(24)])
##x = np.array([datetime.datetime(2013, 9, 28, i, 0) for i in range(24)])
#y = np.random.randint(100, size=x.shape)

plt.plot(x,y)

plt.savefig(naans_image_file)


#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#ax.spines['right'].set_color('none')
#ax.spines['top'].set_color('none')
#plt.xticks([])
#plt.yticks([])
#ax.set_ylim([-30, 10])
#
#data = np.ones(100)
#data[70:] -= np.arange(30)
#
#plt.annotate(
#    'THE DAY I REALIZED\nI COULD COOK BACON\nWHENEVER I WANTED',
#    xy=(70, 1), arrowprops=dict(arrowstyle='->'), xytext=(15, -10))
#
#plt.plot(data)
#
#plt.xlabel('time')
#plt.ylabel('my overall health')
#
#plt.savefig('foo.png')
#plt.show()

#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#ax.bar([-0.125, 1.0-0.125], [0, 100], 0.25)
#ax.spines['right'].set_color('none')
#ax.spines['top'].set_color('none')
#ax.xaxis.set_ticks_position('bottom')
#ax.set_xticks([0, 1])
#ax.set_xlim([-0.5, 1.5])
#ax.set_ylim([0, 110])
#ax.set_xticklabels(['CONFIRMED BY\nEXPERIMENT', 'REFUTED BY\nEXPERIMENT'])
#plt.yticks([])
#
#plt.title("CLAIMS OF SUPERNATURAL POWERS")
#
#plt.show()
