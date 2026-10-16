import sys; sys.path.insert(0, sys.argv[2]); from core import *
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, networkx as nx, random
from matplotlib.patches import Ellipse
from matplotlib.lines import Line2D
plt.rcParams["font.family"] = "Liberation Sans"
D, OUT = sys.argv[1], sys.argv[3]
FS = 10
g, nm = load(D); W = wmat(g, "2026-06-30"); idf = sim(W, "idf"); CUT = 0.10
G = nx.Graph(); G.add_nodes_from(W.index)
for a, b, s in edges(idf, CUT).itertuples(index=False): G.add_edge(a, b, w=float(s))
iso = sorted(n for n in G if G.degree(n) == 0)
comps_ = sorted([c for c in nx.connected_components(G) if len(c) > 1], key=len, reverse=True)
core = G.subgraph(comps_[0]).copy(); pairs_ = [sorted(c) for c in comps_[1:]]
def crossings(pos):
    E = list(core.edges()); n = 0
    def ccw(a, b, c): return (c[1]-a[1])*(b[0]-a[0]) > (b[1]-a[1])*(c[0]-a[0])
    for i in range(len(E)):
        for j in range(i+1, len(E)):
            if set(E[i]) & set(E[j]): continue
            a, b = pos[E[i][0]], pos[E[i][1]]; c, d = pos[E[j][0]], pos[E[j][1]]
            if ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d): n += 1
    return n
Q = None
FW, FH = 7.09, 2.2
fig = plt.figure(figsize=(FW, FH), dpi=300); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, FW); ax.set_ylim(0, FH); ax.axis("off")
P = {"D1": (0.45, 1.62), "Coatue": (1.45, 2.12), "Appaloosa": (1.45, 1.12), "Tiger Global": (2.45, 1.62), "Third Point": (2.45, 2.42),
     "Bridgewater": (3.65, 2.12), "Maverick": (3.65, 1.12), "Soros": (2.75, 0.95), "Point72": (4.65, 1.62), "Viking": (4.75, 2.40), "Lone Pine": (4.85, 0.98), "Duquesne": (3.65, 0.70)}
ty = lambda y: 0.70 + (y - 0.70) * 0.74
for _n in list(P): P[_n] = (P[_n][0], ty(P[_n][1]))
P["Berkshire"], P["Daily Journal"] = (5.75, 1.86), (6.65, 1.86)
P["Gates Fdn"], P["Himalaya"] = (5.75, 1.36), (6.65, 1.36)
LAB = {"D1": ("center", 0, .19), "Coatue": ("center", -.05, .19), "Appaloosa": ("center", 0, -.20), "Tiger Global": ("right", -.17, 0), "Third Point": ("left", .13, .0),
       "Bridgewater": ("center", .15, .19), "Maverick": ("left", .12, 0), "Soros": ("center", 0, -.20), "Point72": ("left", .13, .0), "Viking": ("center", 0, .19), "Lone Pine": ("left", .13, 0), "Duquesne": ("left", .13, 0),
       "Berkshire": ("center", 0, .19), "Daily Journal": ("center", 0, .19), "Gates Fdn": ("center", 0, .19), "Himalaya": ("center", 0, .19)}
follow = {"Tiger Global", "Baupost", "Akre", "Icahn"}; drop = {"Coatue", "Bridgewater", "Appaloosa", "Maverick"}
col = lambda n: "#E69F00" if n in follow else ("#D55E00" if n in drop else "#0072B2")
def tier(w): return 2 if w >= .25 else (1 if w >= .15 else 0)
sty = [dict(lw=.6, c="#C9C9C9", a=.7, z=1), dict(lw=1.4, c="#8C8C8C", a=.8, z=1.5), dict(lw=2.6, c="#3A3A3A", a=.9, z=2)]
for a, b, d in sorted(G.edges(data=True), key=lambda e: e[2]["w"]):
    s = sty[tier(d["w"])]; ax.plot([P[a][0], P[b][0]], [P[a][1], P[b][1]], color=s["c"], lw=s["lw"], alpha=s["a"], zorder=s["z"], solid_capstyle="round")
for n in G:
    if n in iso: continue
    ax.scatter(*P[n], s=210 if n == "Tiger Global" else 70, color=col(n), ec="white", lw=1, zorder=4)
fig.canvas.draw(); R = fig.canvas.get_renderer()
def box(t): bb = t.get_window_extent(R); inv = ax.transData.inverted(); (x0, y0), (x1, y1) = inv.transform((bb.x0, bb.y0)), inv.transform((bb.x1, bb.y1)); return x0, y0, x1, y1
for n in G:
    if n in iso: continue
    ha, dx, dy = LAB[n]
    ax.text(P[n][0]+dx, P[n][1]+dy, n, fontsize=FS, ha=ha, va="center", zorder=6, fontweight="bold" if n == "Tiger Global" else "normal", bbox=dict(fc="white", ec="none", pad=0.6, alpha=.8))
# edge value labels
for (a, b, dx, dy) in [("Coatue", "Tiger Global", 0, 0), ("Bridgewater", "Tiger Global", 0, 0), ("Appaloosa", "Tiger Global", 0, 0), ("Maverick", "Tiger Global", 0, 0)]:
    if G.has_edge(a, b):
        mx, my = (P[a][0]+P[b][0])/2, (P[a][1]+P[b][1])/2
        ax.text(mx+dx, my+dy, f"{idf.loc[a, b]:.2f}", fontsize=FS, fontweight="bold", ha="center", va="center", zorder=7, bbox=dict(fc="white", ec="#3A3A3A", lw=.6, pad=1.2, boxstyle="round,pad=0.15"))
ax.text(0.04, 2.02, "drop = link to", fontsize=FS, color="#D55E00", ha="left", va="center", style="italic", zorder=6)
ax.text(0.04, 1.86, "Tiger \u2265 0.25", fontsize=FS, color="#D55E00", ha="left", va="center", style="italic", zorder=6)
ax.text(6.2, 2.62, "linked pairs", fontsize=FS, color="#666", ha="center", va="center") if False else None
# independent strip
ax.add_patch(plt.Rectangle((0.02, 0.03), FW-0.04, 0.50, fc="#F3F4F8", ec="none", zorder=0))
ax.text(0.10, 0.45, "No link at or above 0.10: 8 independent books", fontsize=FS, color="#333", va="center", fontweight="bold")
xs_i = [0.10, 1.33, 2.30, 3.40, 4.52, 5.40, 6.05, 6.55]
order = ["Baupost", "Akre", "Icahn", "Dalal St", "Elliott", "Fairholme", "Robotti", "Trian"]
x = 0.12
for n in order:
    ax.scatter(x, 0.17, s=60, color=col(n), ec="white", lw=1, zorder=3)
    t = ax.text(x+0.1, 0.17, n, fontsize=FS, va="center", zorder=3); bx = box(t); x = bx[2] + 0.2
leg = [Line2D([], [], marker="o", ls="", color="#E69F00", ms=7, label="follow"), Line2D([], [], marker="o", ls="", color="#D55E00", ms=7, label="drop (\u22650.25 to Tiger)"), Line2D([], [], marker="o", ls="", color="#0072B2", ms=7, label="not selected")]
ax.legend(handles=leg, loc="center right", bbox_to_anchor=(0.995, 0.167), ncol=3, fontsize=FS, frameon=False, handletextpad=0.1, columnspacing=0.9, borderpad=0.1)
# line key (right column)
ax.text(5.74, 1.10, "line = similarity", fontsize=FS, color="#333", va="center", fontweight="bold")
for i, (t_, st_) in enumerate([("0.25+", sty[2]), ("0.15\u20130.25", sty[1]), ("0.10\u20130.15", sty[0])]):
    yy = 0.91 - 0.15*i
    ax.plot([5.77, 6.07], [yy, yy], color=st_["c"], lw=st_["lw"], alpha=st_["a"], solid_capstyle="round")
    ax.text(6.17, yy, t_, fontsize=FS, color="#333", va="center")
fig.savefig(f"{OUT}/network.png", dpi=300); print("ok", G.number_of_edges(), iso)
