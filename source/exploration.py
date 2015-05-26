df.ffpsp0[df.fullsp0[df.respcountysp0[df.eligibilitystatussp0.dropna().str[0].astype(int).le(5)].eq('01')].eq('1')].dropna().astype(int).eq(50).map({True:3})

