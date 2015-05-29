

elig = dw['eligibilitystatus'].dropna().str[0].astype(int).le(5)
local = dw['respcounty'].dropna().eq('01')
cover = dw['full'].dropna().eq(1)

dw['mcrank'] = ((dw['aidcode'].notnull()) & (dw['ffp'] >= 1)).map({True:13}.)reindex(
                index = dw.index)
dw['mcrank'] = dw['ffp'][elig].map({100:10, 65:11, 50:12}).reindex(index = dw.index)
dw['mcrank'] = dw['ffp'][elig & local].map({100:7, 65:8, 50:9}).reindex(index = dw.index)
dw['mcrank'] = dw['ffp'][elig & cover].map({100:4, 65:5, 50:6}).reindex(index = dw.index)
dw['mcrank'] = dw['ffp'][elig & local & cover].map({100:1, 65:2, 50:3}).reindex(index = dw.index)





