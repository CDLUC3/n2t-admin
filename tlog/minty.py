#! /usr/bin/env python3
# almost stateless minter

tlogdir = "/apps/n2t/tlog"
naans_infile = tlogdir + '/naan_dates'
naans_image_file = 'naan_growth.png'

#for n in range(1, 61):
nc = 6   # number of counters
cc = 10  # counter cardinality
cc = 20  # counter cardinality

print(f" v: n= m ")
#for n in range(1, 61):
for n in range(1, nc*cc+1):
    ns = (n + nc//2) % nc
    v = ((n-1) % nc) * cc + ((n-1)//nc) + 1
    v = ((ns-1) % nc) * cc + ((ns-1)//nc) + 1

    #m = (v//c)*c
    #m = ((v-1) % k) * c + ((v-1) % c)
    # XY, Y is number of 1s, X number of 10s
    # n = (XY-1)%10
    #m = ((((v-1)//c) % k) * k) + ((v-1) % k)
    which_counter = (v-1)//cc
    counter_level = ((v-1) % cc)
    m = (counter_level * nc) + which_counter + 1
    #m = counternumber * c
    #m = ((v-1)//c) % c + (v-1)*k
    print(f"{v:2}:{n:2}={m:2} ", end="")
    #print(f"{v:2}:{n:2}t{which_counter:1}o{counter_level:1} ", end="")
    if n % nc == 0:
        print()


# pages.github.com for websites

#with open(naans_infile, encoding="utf-8") as infile:
#    x = []
#    y = []
#    i = 0
#    for line in infile:
#        i += 1
#        # yyy wait, some dates (x-coord) repeat -- what does that do to plot?
#        #     so date D will show with N, and show again with N+1 ...
#        dt_obj = datetime.datetime.strptime(line, '%Y.%m.%d\n')
#        x.append(dt_obj)
#        #print('Date:', dt_obj.date())
#        y.append(i)
#
##    'Growth in number of\nNAANS (ARK-assigning\norganizations) since 2001.'
##    '\n - marketing budget: $600.',
##    u'\n\u2013 marketing budget $600.', size=14,
#plt.annotate(
#    'Numbers of ARK-assigning\norganizations since 2001.', size=15,
#    xy=(datetime.datetime(2003, 1, 1, 0, 0), 450))
##print("nd", x)
#
##x = np.array([datetime.datetime(2013, 9, 28, i, 0) for i in range(24)])
###x = np.array([datetime.datetime(2013, 9, 28, i, 0) for i in range(24)])
##y = np.random.randint(100, size=x.shape)
#
#plt.plot(x,y)
#
#plt.savefig(naans_image_file)
#
