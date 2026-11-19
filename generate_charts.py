"""Regenerates the README charts in images/ (same cleaning logic as main.ipynb).
Run from the repo root:  python generate_charts.py"""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
from matplotlib.ticker import FuncFormatter
import os
os.makedirs("images",exist_ok=True)
df=pd.read_csv("retail_orders_raw.csv").drop_duplicates().copy()
tc=["product","category","region","sales_channel","payment_method","order_status"]
for c in tc: df[c]=df[c].astype("string").str.strip().str.title()
df["order_date"]=pd.to_datetime(df["order_date"],errors="coerce")
for c in ["quantity","unit_price","discount_pct","customer_rating"]: df[c]=pd.to_numeric(df[c],errors="coerce")
bad=df.quantity.isna()|df.unit_price.isna()|(df.quantity<=0)|(df.unit_price<=0)
df=df[~bad].copy()
df=df[~(df.discount_pct.notna()&~df.discount_pct.between(0,1))].copy()
df["discount_pct"]=df.discount_pct.fillna(0)
for c in tc: df[c]=df[c].fillna("Unknown")
df["sales_amount"]=(df.quantity*df.unit_price*(1-df.discount_pct)).round(2)
df["ym"]=df.order_date.dt.to_period("M").astype(str)
BLUE="#2563eb";GREY="#94a3b8";DARK="#0f172a"
plt.rcParams.update({"font.family":"DejaVu Sans","axes.spines.top":False,"axes.spines.right":False,
 "axes.titleweight":"bold","axes.titlesize":13,"axes.titlelocation":"left","figure.dpi":100,"axes.edgecolor":"#cbd5e1","axes.labelcolor":"#334155","xtick.color":"#334155","ytick.color":"#334155"})
sns.set_style("whitegrid",{"grid.color":"#e2e8f0","axes.spines.top":False,"axes.spines.right":False})
lakh=FuncFormatter(lambda v,_:f"₹{v/1e5:.0f}L" if v<1e7 else f"₹{v/1e7:.1f}Cr")
def save(n): plt.tight_layout(); plt.savefig("images/"+n,dpi=160); plt.close()
# 1 monthly
m=df.dropna(subset=["order_date"]).groupby("ym").sales_amount.sum()
fig,ax=plt.subplots(figsize=(10,4.5)); ax.plot(m.index,m.values,marker="o",color=BLUE,lw=2.2)
ax.fill_between(m.index,m.values,alpha=.08,color=BLUE)
for k,col in [(m.idxmax(),"#16a34a"),(m.idxmin(),"#dc2626")]:
    ax.annotate(f"{k}\n₹{m[k]/1e3:,.0f}K",(k,m[k]),textcoords="offset points",xytext=(0,12 if k==m.idxmax() else -32),ha="center",color=col,fontsize=9,fontweight="bold")
ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f"₹{v/1e3:,.0f}K")); ax.set_title("Monthly Sales Trend"); ax.set_xlabel(""); ax.set_ylabel("Sales")
plt.xticks(rotation=45,ha="right"); ax.set_ylim(0,m.max()*1.2); save("01_monthly_sales_trend.png")
# 2 region
r=df.groupby("region").sales_amount.sum().sort_values()
fig,ax=plt.subplots(figsize=(8,4.5)); cols=[BLUE if v==r.max() else GREY for v in r.values]
ax.barh(r.index,r.values,color=cols)
for i,v in enumerate(r.values): ax.text(v,i,f" ₹{v/1e6:.2f}M",va="center",fontsize=9,color=DARK)
ax.set_title("Sales by Region"); ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_:f"₹{v/1e6:.1f}M")); ax.set_xlim(0,r.max()*1.15); ax.grid(axis="y",visible=False); save("02_sales_by_region.png")
# 3 AOV category
oc=df.groupby(["order_id","category"]).sales_amount.sum().reset_index()
a=oc.groupby("category").sales_amount.mean().sort_values()
fig,ax=plt.subplots(figsize=(8,4.5)); ax.barh(a.index,a.values,color=[BLUE if v==a.max() else GREY for v in a.values])
for i,v in enumerate(a.values): ax.text(v,i,f" ₹{v:,.0f}",va="center",fontsize=9,color=DARK)
ax.set_title("Average Order Value by Category"); ax.set_xlim(0,a.max()*1.15); ax.grid(axis="y",visible=False); save("03_avg_order_value_by_category.png")
# 4 category x region
p=df.pivot_table(index="category",columns="region",values="sales_amount",aggfunc="sum",fill_value=0)
fig,ax=plt.subplots(figsize=(9,4.5)); sns.heatmap(p/1e6,annot=True,fmt=".2f",cmap="Blues",cbar_kws={"label":"Sales (₹ million)"},linewidths=.5,ax=ax)
ax.set_title("Sales by Category and Region (₹ million)"); ax.set_xlabel(""); ax.set_ylabel(""); save("04_category_region_heatmap.png")
# 5 channel/payment/status
fig,axs=plt.subplots(1,3,figsize=(13,4))
for ax,col,t in zip(axs,["sales_channel","payment_method","order_status"],["Sales Channel","Payment Method","Order Status"]):
    v=df[col].value_counts().rename(index={"Upi":"UPI"}).sort_values(); ax.barh(v.index,v.values,color=[BLUE if x==v.max() else GREY for x in v.values])
    for i,x in enumerate(v.values): ax.text(x,i,f" {x:,}",va="center",fontsize=9)
    ax.set_title(t); ax.set_xlim(0,v.max()*1.2); ax.grid(axis="y",visible=False)
save("05_channel_payment_status.png")
# 6 ratings
rd=df.dropna(subset=["customer_rating"])
fig,ax=plt.subplots(figsize=(9,4.5)); sns.boxplot(data=rd,x="category",y="customer_rating",color="#bfdbfe",ax=ax,linecolor=BLUE)
ax.set_title("Customer Ratings by Category"); ax.set_xlabel(""); plt.xticks(rotation=20); save("06_ratings_by_category.png")
# 7 distribution
fig,ax=plt.subplots(figsize=(9,4.5)); sns.histplot(df.sales_amount,bins=30,kde=True,color=BLUE,ax=ax)
ax.set_title("Distribution of Order Sales Amount"); ax.set_xlabel("Sales amount (₹)"); save("07_sales_distribution.png")
