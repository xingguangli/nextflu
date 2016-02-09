import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import json

sns.set_style('darkgrid')
plt.ion()

virus = 'Yam'
#virus = 'H1N1pdm'


if virus=='H3N2': ########## H3N2
    freqs = json.load(open('../data/H3N2_3y_frequencies.json'))
    clades = ['3c2.a', '3c3.a', '3c3.b']
    mutations = ['HA1:114T','HA1:142K','HA1:171K', 'HA1:94H']
    mut_legend = {'panel':0, 'loc':3}
elif virus=='H1N1pdm': ########## H1N1pdm
    freqs = json.load(open('../data/H1N1pdm_3y_frequencies.json'))
    clades = ['6c', '6b.1', '6c.2']
    mutations = ['HA1:84N','HA1:162N','HA1:152T', 'HA2:164G'] #these don't add up to one in Asia, probably due to sketchy sampling.
    mut_legend = {'panel':0, 'loc':3}
elif virus=='Vic':
    freqs = json.load(open('../data/Vic_3y_frequencies.json'))
    clades = []
    mutations = ['HA1:129D', 'HA1:117V'] # HA1:56K would be good, but it currently isn't computed -> need to lower the threshold.
    mut_legend = {'panel':1, 'loc':3}
elif virus=='Yam':
    freqs = json.load(open('../data/Yam_3y_frequencies.json'))
    clades = ['3', '2']
    mutations = ['HA1:251V', 'HA1:172Q']
    mut_legend = {'panel':1, 'loc':4}


offset = datetime(2000,1,1).toordinal()
pivots = [offset+(x-2000)*365.25 for x in  freqs['clades']['global']['pivots']]
regions = ['global', 'NA', 'AS', 'EU', 'OC']
cols = sns.color_palette(n_colors=len(regions))

if len(clades):
    fig, axs = plt.subplots(len(clades), 1, sharex=True, figsize=(8, len(clades)*2))
    for clade, ax in zip(clades, axs):
        for c,region in zip(cols, regions):
            try:
                tmp_freq = freqs['clades'][region][clade]
                if tmp_freq is not None:
                    ax.plot_date(pivots, tmp_freq,'-o', label = region, c=c, lw=3 if region=='global' else 1)
            except:
                print "skipping", clade, region
        ax.set_xlim([pivots[-1]-700,pivots[-1]+30])
        ax.set_ylim(0,1)
        ax.text(pivots[-1]-700, 0.9, clade)
    axs[1].legend(loc=1, ncol=2)
    plt.tight_layout(h_pad=0.01)
    plt.savefig('figures/feb-2016/'+virus+'_clades.png')


fig, axs = plt.subplots(len(mutations), 1, sharex=True, figsize=(8, len(mutations)*2))
for mutation, ax in zip(mutations, axs):
    for c,region in zip(cols, regions):
        try:
            tmp_freq = freqs['mutations'][region][mutation]
            if tmp_freq is not None:
                ax.plot_date(pivots, tmp_freq, '-o',label = region, c=c, lw=3 if region=='global' else 1)
        except:
            print "skipping", mutation, region
    ax.set_xlim([pivots[-1]-700,pivots[-1]+30])
    ax.set_ylim(0,1)
    ax.text(pivots[-1]-700, 0.9, mutation)
axs[mut_legend['panel']].legend(loc=mut_legend['loc'], ncol=2)
ax.set_xlabel('time')
plt.tight_layout(h_pad=0.01)
plt.savefig('figures/feb-2016/'+virus+'_mutations.png')