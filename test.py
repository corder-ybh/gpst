# -*- coding: utf-8 -*- 
from math import *
print sqrt(9)
a = [1,2,3] + [4,5,6]
print a
b = list('hello')
print b
b[2:4] = list('yy')
print b
a = list('hello')
a.insert(2, 't')
print a
a.append('q')
print a

def square(x):
  return x*x
print square(9)

a = [1,2,3,4,5,6]
for i in a:
  print i
  
class boy:
  gender = 'male'
  interest='girl'
  def say(self):
    return 'I Love you'
peter = boy()
print peter.gender
print peter.say()

import numpy as np
print np.version.full_version
a = np.arange(20)
print a
a = a.reshape(4,5)
print a
d = (4,5)
np.zeros(d, dtype=int)
print d
a = np.array([[1.0,2],[2,4]])
print 'a:'
print a
b = np.array([[3.2,1.5],[2.5,4]])
print "b:"
print b
print "a+b:"
print a+b

a = np.arange(20).reshape(4,5)
print a;
a = np.asmatrix(a)
print type(a)
b = np.arange(2,45,3).reshape(5,3) #2-45 buchang3
print b
b = np.mat(b)
print b
c = np.linspace(0,2,9)
print c

d = a * b
print d

a = np.array([[3.2, 1.5], [2.5,4]])
print a[0][1]
print a[0,1]

import scipy.stats as stats
import scipy.optimize as opt
print 'scipy:'
rv_unif = stats.uniform.rvs(size=10)
print rv_unif
rv_beta = stats.beta.rvs(size=10,a=4,b=2)
print rv_beta

print '随机数种子'
np.random.seed(seed=2015)
rv_beta = stats.beta.rvs(size=10,a=4,b=2)
print "methon 1:"
print rv_beta

np.random.seed(seed=2015)
beta=stats.beta(a=4,b=2)
print "method 2:"
print beta.rvs(size=10)

norm_dist = stats.norm(loc = 0.5, scale=2)

print "pandas"
import pandas as pd
print pd.__version__

from pandas import Series, DataFrame
a = np.random.randn(5)
print "a is an array"
print a
s = Series(a)
print "s is a Series:"
print s

s = Series(np.random.randn(5), index=['a','b','c','d','e'])
print s
print s.index

s = Series(np.random.randn(5), index=['a','b','c','d','e'], name='my_series')
print s
print s.name

d = {'a':0.,'b':1,'c':2}
print "d is a dict:"
print d
s = Series(d)
print "s is a Series"
print s

s = Series(d, index=['b','c','d','a'])
print s

s = Series(4., index=['b','c','a','d','e'])
print s

s = Series(np.random.randn(10), index=['a','b','c','d','e','f','g','h','i','j'])
print s
print s[0]
print s[:2]
print s[[2,0,4]]
print s[['e','i']]

d = {'one':Series([1.,2.,3.],index=['a','b','c']), 'two':Series([1.,2.,3.,4.], index=['a','b','c','d'])}
df = DataFrame(d)
print df

df = DataFrame(d, index=['r','d','a'], columns=['two','three'])
print df

print "DataFrame index:"
print df.index
print "DataFrame columns:"
print df.columns
print "DataFrame values:"
print df.values

d = {'one':[1.,2.,3.,4.], 'two':[4.,3.,2.,1.]}
df = DataFrame(d, index=['a','b','c','d'])
print df

df = DataFrame()
index = ['alpha','beta','game','delta','eta']
for i in range(5):
  a = DataFrame([np.linspace(i, 5*i, 5)], index=[index[i]])
  df = pd.concat([df,a],axis=0)
print df

print df[1]
print type(df[1])
df.columns = ['a','b','c','d','e']

print "df['b']"
print df['b']
print "type(df['b'])"
print type(df['b'])
print "df.b"
print df.b

