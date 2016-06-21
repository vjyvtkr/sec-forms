# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 17:27:44 2016

@author: Vijay Yevatkar
"""

n = input()
ans = []
for i in range(0,n):
    c = input()
    lc = input()
    #for j in range(0,lc):
    list_is = [int(inp) for inp in raw_input().split()]
    
    pair = False
    for j in range(0,lc):
        for k in range(0,lc):
            if j==k:
                continue
            if list_is[j]+list_is[k]==c:
                ans.append(j+1)
                ans.append(k+1)
                pair = True
                break
        if pair:
            break
i = 0
j = 0
#print "ans is",ans
while True:
    if j>=n:
        break    
    if ans[i]<ans[i+1]:
        print "Case #%s: %s %s"%(j+1, ans[i], ans[i+1])
    else:
        print "Case #%s: %s %s"%(j+1, ans[i+1], ans[i])
    i = i+2
    j = j+1