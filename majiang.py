'''
我们先做不带赖子的麻将胡牌计算。

把手牌中某一个花色的牌整理成一个字符串，规则如下，比如万字
000000000	=>	没有万字
100000000	=>	一万*1
200000000	=>	一万*2
210000000	=>	一万*2 二万*1
...

手牌中任意一种花色的总张数，要么是3的倍数，要么是3的倍数+2，并且所有的花色加起来只能有一个3的倍数+2。

第一步：这种花色有3张，这里就有9+7中可能，9的意思是3个1|3个2|...|3个9，7的意思是123|234|...|789。我们把这16种形状转换成str，用上面说的方法，保存到cardlist3_n这个字典中，key就是那个str，value等会儿再说(***)。
第二步：这种花色有6张牌，无非就是cardlist3_n里面的16种可能*16种可能，最多256种。但是我们要排除一下，排除3个1+3个1，这种肯定是不行的，哪有6个1，而且还要去重。最终的结果保存到cardlist6_n中。
第三步：这种花色有9张牌，那就是两重循环，cardlist6_n套上cardlist3_n，保存到cardlist9_n。
第四步：这种花色有12张牌，实际上不可能，不开口不能胡，忽略了。

第五步：这种花色有2张牌，这个就有歧义了，如果是屁胡，那就要258将，如果是大胡就不要，所以我们需要准备两个字典，一个叫cardlist2_a用来放大胡的str，一个叫cardlist2_b用来放屁胡的str。
第六步：这种花色有5张牌，cardlist2_a(b)套上cardlist3_n，保存到cardlist5_a(b)。
第七步：这种花色有8张牌，cardlist2_a(b)套上cardlist6_n，保存到cardlist8_a(b)。
第八步：这种花色有11张牌，cardlist2_a(b)套上cardlist9_n，保存到cardlist11_a(b)。
第九步：这种花色有14张牌，不开口不能胡，忽略了。

现在我们就拿到了，不带赖子的，所有花色允许的牌型(str)。我们把玩家的手牌，每种花色根据张数也整理出一个(几个)str，分别丢到对应的字典中查找，全部都找得到，代表可以匹配上。然后就是什么大胡屁胡之类的了，注意有且只有一个需要到5678步中匹配，其余的都要去123步中匹配。

(***)还有一个屁胡的判断，吃的牌另算，手牌，我们在生成cardlist3_n的时候，我们的value是有含义的，在3个1|...|3个9的时候，value是0，123|...|789的时候，values是1，后面的234678步的时候，当我们合并两组牌，都需要将value相加，如果相加的结果还是0，代表都是碰，大于0代表至少有一个吃。


现在我们加上赖子。赖子最多有四个赖子，那么我们就去生成一个类似上面的str
laizi1的意思是一个赖子的时候，可能替换的手牌，无非就是100000000|010000000|...|000000001。类似生成laizi2,laizi3,laizi4。

第一步，我们对cardlist3_n这个字典需要改动，生成两个新的字典，一个叫l1_cardlist2_n(意思是带1个赖子+牌数量2+不分大小胡)，一个叫l2_cardlist1_n(意思是带2个赖子+牌数量1+不分大小胡)。我们将cardlist3_n循环减去laizi1，结果放到l1_cardlist2_n中，注意，每一个位置都不能减成负的。我们将cardlist3_n循环减去laizi2，结果放到l2_cardlist1_n中。
第二步，我们对cardlist6_n这个字典循环生成l1_cardlist5_n|l2_cardlist4_n|l3_cardlist3_n|l4_cardlist2_n。
第三步，我们对cardlist9_n这个字典循环生成l1_cardlist8_n|l2_cardlist7_n|l3_cardlist6_n|l4_cardlist3_n。
第四步，不开口不能胡，忽略。

第五步，我们对cardlist2_a(b)这个字典循环生成l1_cardlist1_a(b)。
第六步，我们对cardlist5_a(b)这个字典循环生成l1_cardlist4_a(b)|l2_cardlist3_a(b)|l3_cardlist2_a(b)|l4_cardlist1_a(b)。
第七步，我们对cardlist8_a(b)这个字典循环生成l1_cardlist7_a(b)|l2_cardlist6_a(b)|l3_cardlist5_a(b)|l4_cardlist4_a(b)。
第八步，我们对cardlist11_a(b)这个字典循环生成l1_cardlist10_a(b)|l2_cardlist9_a(b)|l3_cardlist8_a(b)|l4_cardlist7_a(b)。
第九步，不开口不能胡，忽略。

剩下的就是保存了
第一层：0个赖子|1个赖子|2个赖子|3个赖子|4个赖子。
第二层：n(3的倍数) a(3的倍数+2并且是大胡) b(3的倍数+2并且是屁胡)
第三层：str=>value(大于0代表是屁胡)
'''


import json

class ListCard :
	def __init__(self, _k = '000000000', _v = 0):
		self.key = _k
		self.value = _v

	def setcard(self, pos, num = 1):
		if pos >= 1 and pos <= 9:
			self.key = self.key[0: pos - 1] +  str(int(self.key[pos - 1 : pos]) + num) + self.key[pos : 9]

	def plus(self, c1, c2):
		self.key = ''
		for i in range(1, 10):
			n = int(c1.key[i - 1 : i]) + int(c2.key[i - 1 : i])
			if n > 4:
				self.key = '000000000'
				return False
			self.key += str(n)
		self.value = c1.value + c2.value
		return True

	def minus(self, c1, c2):
		self.key = ''
		for i in range(1, 10):
			n = int(c1.key[i - 1 : i]) - int(c2.key[i - 1 : i])
			if n < 0:
				self.key = '000000000'
				return False
			self.key += str(n)
		self.value = c1.value + c2.value
		return True


# 2张牌=>大
cardlist2_a = {}
for i in range(1, 10):
	l2 = ListCard()
	l2.setcard(i, 2)
	cardlist2_a[l2.key] = l2.value
# 2张牌=>小
cardlist2_b = {}
l2 = ListCard()
l2.setcard(2, 2)
cardlist2_b[l2.key] = l2.value
l5 = ListCard()
l5.setcard(5, 2)
cardlist2_b[l5.key] = l5.value
l8 = ListCard()
l8.setcard(8, 2)
cardlist2_b[l8.key] = l8.value
# 2张牌=>风
cardlist2_f = {}
for i in range(1, 8):
	l2 = ListCard()
	l2.setcard(i, 2)
	cardlist2_f[l2.key] = l2.value

# 3张牌=>无
cardlist3_n = {}
cardlist3_f = {}
for i in range(1, 10):
	l3 = ListCard()
	l3.setcard(i, 3)
	l3.value = 0
	cardlist3_n[l3.key] = l3.value
for i in range(1, 8):
	l3 = ListCard()
	l3.setcard(i, 1)
	l3.setcard(i + 1, 1)
	l3.setcard(i + 2, 1)
	if i == 4:
		l3.value = 100
	else:
		l3.value = 1
	cardlist3_n[l3.key] = l3.value
for i in range(1, 8):
	l3 = ListCard()
	l3.setcard(i, 3)
	l3.value = 0
	cardlist3_f[l3.key] = l3.value

# 5张牌=>大
cardlist5_a = {}
for k1, v1 in cardlist2_a.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_n.items():
		c2 = ListCard(k2, v2)
		l5 = ListCard()
		if l5.plus(c1, c2) == True:
			if l5.key not in cardlist5_a:
				cardlist5_a[l5.key] = l5.value
			else:
				cardlist5_a[l5.key] *= l5.value
				if cardlist5_a[l5.key] >= 100:
					cardlist5_a[l5.key] = 100
				elif cardlist5_a[l5.key] > 0:
					cardlist5_a[l5.key] = 1
# 5张牌=>小
cardlist5_b = {}
for k1, v1 in cardlist2_b.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_n.items():
		c2 = ListCard(k2, v2)
		l5 = ListCard()
		if l5.plus(c1, c2) == True:
			if l5.key not in cardlist5_b:
				cardlist5_b[l5.key] = l5.value
			else:
				cardlist5_b[l5.key] *= l5.value
				if cardlist5_b[l5.key] > 0:
					cardlist5_b[l5.key] = 1
# 5张牌=>风
cardlist5_f = {}
for k1, v1 in cardlist2_f.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_f.items():
		c2 = ListCard(k2, v2)
		l5 = ListCard()
		if l5.plus(c1, c2) == True:
			if l5.key not in cardlist5_f:
				cardlist5_f[l5.key] = l5.value
			else:
				cardlist5_f[l5.key] *= l5.value
				if cardlist5_f[l5.key] > 0:
					cardlist5_f[l5.key] = 1


# 6张牌=>无
cardlist6_n = {}
for k1, v1 in cardlist3_n.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_n.items():
		c2 = ListCard(k2, v2)
		l6 = ListCard()
		if l6.plus(c1, c2) == True:
			if l6.key not in cardlist6_n:
				cardlist6_n[l6.key] = l6.value
			else:
				cardlist6_n[l6.key] *= l6.value
				if cardlist6_n[l6.key] >= 100:
					cardlist6_n[l6.key] = 100
				elif cardlist6_n[l6.key] > 0:
					cardlist6_n[l6.key] = 1
# 6张牌=>风
cardlist6_f = {}
for k1, v1 in cardlist3_f.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_f.items():
		c2 = ListCard(k2, v2)
		l6 = ListCard()
		if l6.plus(c1, c2) == True:
			if l6.key not in cardlist6_f:
				cardlist6_f[l6.key] = l6.value
			else:
				cardlist6_f[l6.key] *= l6.value
				if cardlist6_f[l6.key] > 0:
					cardlist6_f[l6.key] = 1


# 8张牌=>大
cardlist8_a = {}
for k1, v1 in cardlist2_a.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist6_n.items():
		c2 = ListCard(k2, v2)
		l8 = ListCard()
		if l8.plus(c1, c2) == True:
			if l8.key not in cardlist8_a:
				cardlist8_a[l8.key] = l8.value
			else:
				cardlist8_a[l8.key] *= l8.value
				if cardlist8_a[l8.key] >= 100:
					cardlist8_a[l8.key] = 100
				elif cardlist8_a[l8.key] > 0:
					cardlist8_a[l8.key] = 1
# 8张牌=>小
cardlist8_b = {}
for k1, v1 in cardlist2_b.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist6_n.items():
		c2 = ListCard(k2, v2)
		l8 = ListCard()
		if l8.plus(c1, c2) == True:
			if l8.key not in cardlist8_b:
				cardlist8_b[l8.key] = l8.value
			else:
				cardlist8_b[l8.key] *= l8.value
				if cardlist8_b[l8.key] > 0:
					cardlist8_b[l8.key] = 1
# 8张牌=>风
cardlist8_f = {}
for k1, v1 in cardlist2_f.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist6_f.items():
		c2 = ListCard(k2, v2)
		l8 = ListCard()
		if l8.plus(c1, c2) == True:
			if l8.key not in cardlist8_f:
				cardlist8_f[l8.key] = l8.value
			else:
				cardlist8_f[l8.key] *= l8.value
				if cardlist8_f[l8.key] > 0:
					cardlist8_f[l8.key] = 1


# 9张牌=>无
cardlist9_n = {}
for k1, v1 in cardlist6_n.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_n.items():
		c2 = ListCard(k2, v2)
		l9 = ListCard()
		if l9.plus(c1, c2) == True:
			if l9.key not in cardlist9_n:
				cardlist9_n[l9.key] = l9.value
			else:
				cardlist9_n[l9.key] *= l9.value
				if cardlist9_n[l9.key] >= 100:
					cardlist9_n[l9.key] = 100
				elif cardlist9_n[l9.key] > 0:
					cardlist9_n[l9.key] = 1
# 9张牌=>风
cardlist9_f = {}
for k1, v1 in cardlist6_f.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_f.items():
		c2 = ListCard(k2, v2)
		l9 = ListCard()
		if l9.plus(c1, c2) == True:
			if l9.key not in cardlist9_f:
				cardlist9_f[l9.key] = l9.value
			else:
				cardlist9_f[l9.key] *= l9.value
				if cardlist9_f[l9.key] > 0:
					cardlist9_f[l9.key] = 1

# 11张牌=>大
cardlist11_a = {}
for k1, v1 in cardlist2_a.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist9_n.items():
		c2 = ListCard(k2, v2)
		l11 = ListCard()
		if l11.plus(c1, c2) == True:
			if l11.key not in cardlist11_a:
				cardlist11_a[l11.key] = l11.value
			else:
				cardlist11_a[l11.key] *= l11.value
				if cardlist11_a[l11.key] >= 100:
					cardlist11_a[l11.key] = 100
				elif cardlist11_a[l11.key] > 0:
					cardlist11_a[l11.key] = 1
# 11张牌=>小
cardlist11_b = {}
for k1, v1 in cardlist2_b.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist9_n.items():
		c2 = ListCard(k2, v2)
		l11 = ListCard()
		if l11.plus(c1, c2) == True:
			if l11.key not in cardlist11_b:
				cardlist11_b[l11.key] = l11.value
			else:
				cardlist11_b[l11.key] *= l11.value
				if cardlist11_b[l11.key] > 0:
					cardlist11_b[l11.key] = 1
# 11张牌=>风
cardlist11_f = {}
for k1, v1 in cardlist2_f.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist9_f.items():
		c2 = ListCard(k2, v2)
		l11 = ListCard()
		if l11.plus(c1, c2) == True:
			if l11.key not in cardlist11_f:
				cardlist11_f[l11.key] = l11.value
			else:
				cardlist11_f[l11.key] *= l11.value
				if cardlist11_f[l11.key] > 0:
					cardlist11_f[l11.key] = 1

#12张牌=>无
cardlist12_n = {}
for k1, v1 in cardlist9_n.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_n.items():
		c2 = ListCard(k2, v2)
		l12 = ListCard()
		if l12.plus(c1, c2) == True:
			if l12.key not in cardlist12_n:
				cardlist12_n[l12.key] = l12.value
			else:
				cardlist12_n[l12.key] *= l12.value
				if cardlist12_n[l12.key] >= 100:
					cardlist12_n[l12.key] = 100
				elif cardlist12_n[l12.key] > 0:
					cardlist12_n[l12.key] = 1
#12张牌=>风
cardlist12_f = {}
for k1, v1 in cardlist9_f.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_f.items():
		c2 = ListCard(k2, v2)
		l12 = ListCard()
		if l12.plus(c1, c2) == True:
			if l12.key not in cardlist12_f:
				cardlist12_f[l12.key] = l12.value
			else:
				cardlist12_f[l12.key] *= l12.value
				if cardlist12_f[l12.key] > 0:
					cardlist12_f[l12.key] = 1

# 14张牌=>大
cardlist14_a = {}
for k1, v1 in cardlist2_a.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist12_n.items():
		c2 = ListCard(k2, v2)
		l14 = ListCard()
		if l14.plus(c1, c2) == True:
			if l14.key not in cardlist14_a:
				cardlist14_a[l14.key] = l14.value
			else:
				cardlist14_a[l14.key] *= l14.value
				if cardlist14_a[l14.key] >= 100:
					cardlist14_a[l14.key] = 100
				elif cardlist14_a[l14.key] > 0:
					cardlist14_a[l14.key] = 1
# 14张牌=>小
cardlist14_b = {}
for k1, v1 in cardlist2_b.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist12_n.items():
		c2 = ListCard(k2, v2)
		l14 = ListCard()
		if l14.plus(c1, c2) == True:
			if l14.key not in cardlist14_b:
				cardlist14_b[l14.key] = l14.value
			else:
				cardlist14_b[l14.key] *= l14.value
				if cardlist14_b[l14.key] > 0:
					cardlist14_b[l14.key] = 1
# 14张牌=>风
cardlist14_f = {}
for k1, v1 in cardlist2_f.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist12_f.items():
		c2 = ListCard(k2, v2)
		l14 = ListCard()
		if l14.plus(c1, c2) == True:
			if l14.key not in cardlist14_f:
				cardlist14_f[l14.key] = l14.value
			else:
				cardlist14_f[l14.key] *= l14.value
				if cardlist14_f[l14.key] > 0:
					cardlist14_f[l14.key] = 1



laizi1 = {}
for i in range(1, 10):
	l = ListCard()
	l.setcard(i)
	laizi1[l.key] = l.value

laizi2 = {}
for i in range(1, 10):
	l = ListCard()
	l.setcard(i, 2)
	laizi2[l.key] = l.value
for k1, v1 in laizi1.items():
	l1 = ListCard(k1, v1)
	for k2, v2 in laizi1.items():
		l2 = ListCard(k2, v2)
		l = ListCard()
		l.plus(l1, l2)
		laizi2[l.key] = l.value

laizi3 = {}
for i in range(1, 10):
	l = ListCard()
	l.setcard(i, 3)
	laizi3[l.key] = l.value
for k1, v1 in laizi2.items():
	l1 = ListCard(k1, v1)
	for k2, v2 in laizi1.items():
		l2 = ListCard(k2, v2)
		l = ListCard()
		l.plus(l1, l2)
		laizi3[l.key] = l.value

laizi4 = {}
for i in range(1, 10):
	l = ListCard()
	l.setcard(i, 4)
	laizi4[l.key] = l.value
for k1, v1 in laizi3.items():
	l1 = ListCard(k1, v1)
	for k2, v2 in laizi1.items():
		l2 = ListCard(k2, v2)
		l = ListCard()
		l.plus(l1, l2)
		laizi4[l.key] = l.value

claizi0 = {}
claizi1 = {}
claizi2 = {}
claizi3 = {}
claizi4 = {}

for i in range(1, 15):
	claizi0[i] = {}
	claizi1[i] = {}
	claizi2[i] = {}
	claizi3[i] = {}
	claizi4[i] = {}

# 2张牌=>大				===>			1赖子+1张牌=>大
l1_cardlist1_a = {}
# 2张牌=>大				===>			1赖子+1张牌=>小
l1_cardlist1_b = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist2_a.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist1_a:
				l1_cardlist1_a[l1.key] *= c2.value
				if l1_cardlist1_a[l1.key] > 0:
					l1_cardlist1_a[l1.key] = 1
			else:
				l1_cardlist1_a[l1.key] = c2.value
	for ck, cv in cardlist2_b.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist1_b:
				l1_cardlist1_b[l1.key] *= c2.value
				if l1_cardlist1_b[l1.key] > 0:
					l1_cardlist1_b[l1.key] = 1
			else:
				l1_cardlist1_b[l1.key] = c2.value
# 2张牌=>风				===>			1赖子+1张牌=>风
l1_cardlist1_f = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist2_f.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist1_f:
				l1_cardlist1_f[l1.key] *= c2.value
				if l1_cardlist1_f[l1.key] > 0:
					l1_cardlist1_f[l1.key] = 1
			else:
				l1_cardlist1_f[l1.key] = c2.value

# 3张牌=>无				===>			1赖子+2张牌=>无
l1_cardlist2_n = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist3_n.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist2_n:
				l1_cardlist2_n[l1.key] *= c2.value
				if l1_cardlist2_n[l1.key] > 0:
					l1_cardlist2_n[l1.key] = 1
			else:
				l1_cardlist2_n[l1.key] = c2.value
# 3张牌=>无				===>			2赖子+1张牌=>无
l2_cardlist1_n = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist3_n.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist1_n:
				l2_cardlist1_n[l2.key] *= c2.value
				if l2_cardlist1_n[l2.key] > 0:
					l2_cardlist1_n[l2.key] = 1
			else:
				l2_cardlist1_n[l2.key] = c2.value
# 3张牌=>风				===>			1赖子+2张牌=>风
l1_cardlist2_f = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist3_f.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist2_f:
				l1_cardlist2_f[l1.key] *= c2.value
				if l1_cardlist2_f[l1.key] > 0:
					l1_cardlist2_f[l1.key] = 1
			else:
				l1_cardlist2_f[l1.key] = c2.value
# 3张牌=>风				===>			2赖子+1张牌=>风
l2_cardlist1_f = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist3_f.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist1_f:
				l2_cardlist1_f[l2.key] *= c2.value
				if l2_cardlist1_f[l2.key] > 0:
					l2_cardlist1_f[l2.key] = 1
			else:
				l2_cardlist1_f[l2.key] = c2.value


# 5张牌=>大				===>			1赖子+4张牌=>大
l1_cardlist4_a = {}
# 5张牌=>小				===>			1赖子+4张牌=>小
l1_cardlist4_b = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist5_a.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist4_a:
				l1_cardlist4_a[l1.key] *= c2.value
				if l1_cardlist4_a[l1.key] > 0:
					l1_cardlist4_a[l1.key] = 1
			else:
				l1_cardlist4_a[l1.key] = c2.value
	for ck, cv in cardlist5_b.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist4_b:
				l1_cardlist4_b[l1.key] *= c2.value
				if l1_cardlist4_b[l1.key] > 0:
					l1_cardlist4_b[l1.key] = 1
			else:
				l1_cardlist4_b[l1.key] = c2.value
# 5张牌=>大				===>			2赖子+3张牌=>大
l2_cardlist3_a = {}
# 5张牌=>小				===>			2赖子+3张牌=>小
l2_cardlist3_b = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist5_a.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist3_a:
				l2_cardlist3_a[l2.key] *= c2.value
				if l2_cardlist3_a[l2.key] > 0:
					l2_cardlist3_a[l2.key] = 1
			else:
				l2_cardlist3_a[l2.key] = c2.value
	for ck, cv in cardlist5_b.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key[1] != '0' or l2.key[4] != '0' or l2.key[7] != '0':
				if l2.key in l2_cardlist3_b:
					l2_cardlist3_b[l2.key] *= c2.value
					if l2_cardlist3_b[l2.key] > 0:
						l2_cardlist3_b[l2.key] = 1
				else:
					l2_cardlist3_b[l2.key] = c2.value
# 5张牌=>大				===>			3赖子+2张牌=>大
l3_cardlist2_a = {}
# 5张牌=>小				===>			3赖子+2张牌=>小
l3_cardlist2_b = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist5_a.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist2_a:
				l3_cardlist2_a[l3.key] *= c2.value
				if l3_cardlist2_a[l3.key] > 0:
					l3_cardlist2_a[l3.key] = 1
			else:
				l3_cardlist2_a[l3.key] = c2.value
	for ck, cv in cardlist5_b.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key[1] != '0' or l3.key[4] != '0' or l3.key[7] != '0':
				if l3.key in l3_cardlist2_b:
					l3_cardlist2_b[l3.key] *= c2.value
					if l3_cardlist2_b[l3.key] > 0:
						l3_cardlist2_b[l3.key] = 1
				else:
					l3_cardlist2_b[l3.key] = c2.value
# 5张牌=>大				===>			4赖子+1张牌=>大
l4_cardlist1_a = {}
# 5张牌=>小				===>			4赖子+1张牌=>小
l4_cardlist1_b = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist5_a.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist1_a:
				l4_cardlist1_a[l4.key] *= c2.value
				if l4_cardlist1_a[l4.key] > 0:
					l4_cardlist1_a[l4.key] = 1
			else:
				l4_cardlist1_a[l4.key] = c2.value
	for ck, cv in cardlist5_b.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key[1] != '0' or l4.key[4] != '0' or l4.key[7] != '0':
				if l4.key in l4_cardlist1_b:
					l4_cardlist1_b[l4.key] *= c2.value
					if l4_cardlist1_b[l4.key] > 0:
						l4_cardlist1_b[l4.key] = 1
				else:
					l4_cardlist1_b[l4.key] = c2.value
# 5张牌=>风				===>			1赖子+4张牌=>风
l1_cardlist4_f = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist5_f.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist4_f:
				l1_cardlist4_f[l1.key] *= c2.value
				if l1_cardlist4_f[l1.key] > 0:
					l1_cardlist4_f[l1.key] = 1
			else:
				l1_cardlist4_f[l1.key] = c2.value
# 5张牌=>风				===>			2赖子+3张牌=>风
l2_cardlist3_f = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist5_f.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist3_f:
				l2_cardlist3_f[l2.key] *= c2.value
				if l2_cardlist3_f[l2.key] > 0:
					l2_cardlist3_f[l2.key] = 1
			else:
				l2_cardlist3_f[l2.key] = c2.value
# 5张牌=>风				===>			3赖子+2张牌=>风
l3_cardlist2_f = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist5_f.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist2_f:
				l3_cardlist2_f[l3.key] *= c2.value
				if l3_cardlist2_f[l3.key] > 0:
					l3_cardlist2_f[l3.key] = 1
			else:
				l3_cardlist2_f[l3.key] = c2.value
# 5张牌=>风				===>			4赖子+1张牌=>风
l4_cardlist1_f = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist5_f.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist1_f:
				l4_cardlist1_f[l4.key] *= c2.value
				if l4_cardlist1_f[l4.key] > 0:
					l4_cardlist1_f[l4.key] = 1
			else:
				l4_cardlist1_f[l4.key] = c2.value

# 6张牌=>无				===>			1赖子+5张牌=>无
l1_cardlist5_n = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist6_n.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist5_n:
				l1_cardlist5_n[l1.key] *= c2.value
				if l1_cardlist5_n[l1.key] > 0:
					l1_cardlist5_n[l1.key] = 1
			else:
				l1_cardlist5_n[l1.key] = c2.value
# 6张牌=>无				===>			2赖子+4张牌=>无
l2_cardlist4_n = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist6_n.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist4_n:
				l2_cardlist4_n[l2.key] *= c2.value
				if l2_cardlist4_n[l2.key] > 0:
					l2_cardlist4_n[l2.key] = 1
			else:
				l2_cardlist4_n[l2.key] = c2.value
# 6张牌=>无				===>			3赖子+3张牌=>无
l3_cardlist3_n = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist6_n.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist3_n:
				l3_cardlist3_n[l3.key] *= c2.value
				if l3_cardlist3_n[l3.key] > 0:
					l3_cardlist3_n[l3.key] = 1
			else:
				l3_cardlist3_n[l3.key] = c2.value
# 6张牌=>无				===>			4赖子+2张牌=>无
l4_cardlist2_n = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist6_n.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist2_n:
				l4_cardlist2_n[l4.key] *= c2.value
				if l4_cardlist2_n[l4.key] > 0:
					l4_cardlist2_n[l4.key] = 1
			else:
				l4_cardlist2_n[l4.key] = c2.value
# 6张牌=>风				===>			1赖子+5张牌=>风
l1_cardlist5_f = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist6_f.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist5_f:
				l1_cardlist5_f[l1.key] *= c2.value
				if l1_cardlist5_f[l1.key] > 0:
					l1_cardlist5_f[l1.key] = 1
			else:
				l1_cardlist5_f[l1.key] = c2.value
# 6张牌=>风				===>			2赖子+4张牌=>风
l2_cardlist4_f = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist6_f.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist4_f:
				l2_cardlist4_f[l2.key] *= c2.value
				if l2_cardlist4_f[l2.key] > 0:
					l2_cardlist4_f[l2.key] = 1
			else:
				l2_cardlist4_f[l2.key] = c2.value
# 6张牌=>风				===>			3赖子+3张牌=>风
l3_cardlist3_f = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist6_f.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist3_f:
				l3_cardlist3_f[l3.key] *= c2.value
				if l3_cardlist3_f[l3.key] > 0:
					l3_cardlist3_f[l3.key] = 1
			else:
				l3_cardlist3_f[l3.key] = c2.value
# 6张牌=>风				===>			4赖子+2张牌=>风
l4_cardlist2_f = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist6_f.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist2_f:
				l4_cardlist2_f[l4.key] *= c2.value
				if l4_cardlist2_f[l4.key] > 0:
					l4_cardlist2_f[l4.key] = 1
			else:
				l4_cardlist2_f[l4.key] = c2.value

# 8张牌=>大				===>			1赖子+7张牌=>大
l1_cardlist7_a = {}
# 8张牌=>小				===>			1赖子+7张牌=>小
l1_cardlist7_b = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist8_a.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist7_a:
				l1_cardlist7_a[l1.key] *= c2.value
				if l1_cardlist7_a[l1.key] > 0:
					l1_cardlist7_a[l1.key] = 1
			else:
				l1_cardlist7_a[l1.key] = c2.value
	for ck, cv in cardlist8_b.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist7_b:
				l1_cardlist7_b[l1.key] *= c2.value
				if l1_cardlist7_b[l1.key] > 0:
					l1_cardlist7_b[l1.key] = 1
			else:
				l1_cardlist7_b[l1.key] = c2.value
# 8张牌=>大				===>			2赖子+6张牌=>大
l2_cardlist6_a = {}
# 8张牌=>小				===>			2赖子+6张牌=>小
l2_cardlist6_b = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist8_a.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist6_a:
				l2_cardlist6_a[l2.key] *= c2.value
				if l2_cardlist6_a[l2.key] > 0:
					l2_cardlist6_a[l2.key] = 1
			else:
				l2_cardlist6_a[l2.key] = c2.value
	for ck, cv in cardlist8_b.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key[1] != '0' or l2.key[4] != '0' or l2.key[7] != '0':
				if l2.key in l2_cardlist6_b:
					l2_cardlist6_b[l2.key] *= c2.value
					if l2_cardlist6_b[l2.key] > 0:
						l2_cardlist6_b[l2.key] = 1
				else:
					l2_cardlist6_b[l2.key] = c2.value
# 8张牌=>大				===>			3赖子+5张牌=>大
l3_cardlist5_a = {}
# 8张牌=>小				===>			3赖子+5张牌=>小
l3_cardlist5_b = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist8_a.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist5_a:
				l3_cardlist5_a[l3.key] *= c2.value
				if l3_cardlist5_a[l3.key] > 0:
					l3_cardlist5_a[l3.key] = 1
			else:
				l3_cardlist5_a[l3.key] = c2.value
	for ck, cv in cardlist8_b.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key[1] != '0' or l3.key[4] != '0' or l3.key[7] != '0':
				if l3.key in l3_cardlist5_b:
					l3_cardlist5_b[l3.key] *= c2.value
					if l3_cardlist5_b[l3.key] > 0:
						l3_cardlist5_b[l3.key] = 1
				else:
					l3_cardlist5_b[l3.key] = c2.value
# 8张牌=>大				===>			4赖子+4张牌=>大
l4_cardlist4_a = {}
# 8张牌=>小				===>			4赖子+4张牌=>小
l4_cardlist4_b = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist8_a.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist4_a:
				l4_cardlist4_a[l4.key] *= c2.value
				if l4_cardlist4_a[l4.key] > 0:
					l4_cardlist4_a[l4.key] = 1
			else:
				l4_cardlist4_a[l4.key] = c2.value
	for ck, cv in cardlist8_b.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key[1] != '0' or l4.key[4] != '0' or l4.key[7] != '0':
				if l4.key in l4_cardlist4_b:
					l4_cardlist4_b[l4.key] *= c2.value
					if l4_cardlist4_b[l4.key] > 0:
						l4_cardlist4_b[l4.key] = 1
				else:
					l4_cardlist4_b[l4.key] = c2.value
# 8张牌=>风				===>			1赖子+7张牌=>风
l1_cardlist7_f = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist8_f.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist7_f:
				l1_cardlist7_f[l1.key] *= c2.value
				if l1_cardlist7_f[l1.key] > 0:
					l1_cardlist7_f[l1.key] = 1
			else:
				l1_cardlist7_f[l1.key] = c2.value
# 8张牌=>风				===>			2赖子+6张牌=>风
l2_cardlist6_f = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist8_f.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist6_f:
				l2_cardlist6_f[l2.key] *= c2.value
				if l2_cardlist6_f[l2.key] > 0:
					l2_cardlist6_f[l2.key] = 1
			else:
				l2_cardlist6_f[l2.key] = c2.value
# 8张牌=>风				===>			3赖子+5张牌=>风
l3_cardlist5_f = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist8_f.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist5_f:
				l3_cardlist5_f[l3.key] *= c2.value
				if l3_cardlist5_f[l3.key] > 0:
					l3_cardlist5_f[l3.key] = 1
			else:
				l3_cardlist5_f[l3.key] = c2.value
# 8张牌=>风				===>			4赖子+4张牌=>风
l4_cardlist4_f = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist8_f.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist4_f:
				l4_cardlist4_f[l4.key] *= c2.value
				if l4_cardlist4_f[l4.key] > 0:
					l4_cardlist4_f[l4.key] = 1
			else:
				l4_cardlist4_f[l4.key] = c2.value

# 9张牌=>无				===>			1赖子+8张牌=>无
l1_cardlist8_n = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist9_n.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist8_n:
				l1_cardlist8_n[l1.key] *= c2.value
				if l1_cardlist8_n[l1.key] > 0:
					l1_cardlist8_n[l1.key] = 1
			else:
				l1_cardlist8_n[l1.key] = c2.value
# 9张牌=>无				===>			2赖子+7张牌=>无
l2_cardlist7_n = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist9_n.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist7_n:
				l2_cardlist7_n[l2.key] *= c2.value
				if l2_cardlist7_n[l2.key] > 0:
					l2_cardlist7_n[l2.key] = 1
			else:
				l2_cardlist7_n[l2.key] = c2.value
# 9张牌=>无				===>			3赖子+6张牌=>无
l3_cardlist6_n = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist9_n.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist6_n:
				l3_cardlist6_n[l3.key] *= c2.value
				if l3_cardlist6_n[l3.key] > 0:
					l3_cardlist6_n[l3.key] = 1
			else:
				l3_cardlist6_n[l3.key] = c2.value
# 9张牌=>无				===>			4赖子+5张牌=>无
l4_cardlist5_n = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist9_n.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist5_n:
				l4_cardlist5_n[l4.key] *= c2.value
				if l4_cardlist5_n[l4.key] > 0:
					l4_cardlist5_n[l4.key] = 1
			else:
				l4_cardlist5_n[l4.key] = c2.value
# 9张牌=>风				===>			1赖子+8张牌=>风
l1_cardlist8_f = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist9_f.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist8_f:
				l1_cardlist8_f[l1.key] *= c2.value
				if l1_cardlist8_f[l1.key] > 0:
					l1_cardlist8_f[l1.key] = 1
			else:
				l1_cardlist8_f[l1.key] = c2.value
# 9张牌=>风				===>			2赖子+7张牌=>风
l2_cardlist7_f = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist9_f.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist7_f:
				l2_cardlist7_f[l2.key] *= c2.value
				if l2_cardlist7_f[l2.key] > 0:
					l2_cardlist7_f[l2.key] = 1
			else:
				l2_cardlist7_f[l2.key] = c2.value
# 9张牌=>风				===>			3赖子+6张牌=>风
l3_cardlist6_f = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist9_f.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist6_f:
				l3_cardlist6_f[l3.key] *= c2.value
				if l3_cardlist6_f[l3.key] > 0:
					l3_cardlist6_f[l3.key] = 1
			else:
				l3_cardlist6_f[l3.key] = c2.value
# 9张牌=>风				===>			4赖子+5张牌=>风
l4_cardlist5_f = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist9_f.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist5_f:
				l4_cardlist5_f[l4.key] *= c2.value
				if l4_cardlist5_f[l4.key] > 0:
					l4_cardlist5_f[l4.key] = 1
			else:
				l4_cardlist5_f[l4.key] = c2.value

# 11张牌=>大			===>			1赖子+10张牌=>大
l1_cardlist10_a = {}
# 11张牌=>小			===>			1赖子+10张牌=>小
l1_cardlist10_b = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist11_a.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist10_a:
				l1_cardlist10_a[l1.key] *= c2.value
				if l1_cardlist10_a[l1.key] > 0:
					l1_cardlist10_a[l1.key] = 1
			else:
				l1_cardlist10_a[l1.key] = c2.value
	for ck, cv in cardlist11_b.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist10_b:
				l1_cardlist10_b[l1.key] *= c2.value
				if l1_cardlist10_b[l1.key] > 0:
					l1_cardlist10_b[l1.key] = 1
			else:
				l1_cardlist10_b[l1.key] = c2.value
# 11张牌=>大			===>			2赖子+9张牌=>大
l2_cardlist9_a = {}
# 11张牌=>小			===>			2赖子+9张牌=>小
l2_cardlist9_b = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist11_a.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist9_a:
				l2_cardlist9_a[l2.key] *= c2.value
				if l2_cardlist9_a[l2.key] > 0:
					l2_cardlist9_a[l2.key] = 1
			else:
				l2_cardlist9_a[l2.key] = c2.value
	for ck, cv in cardlist11_b.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key[1] != '0' or l2.key[4] != '0' or l2.key[7] != '0':
				if l2.key in l2_cardlist9_b:
					l2_cardlist9_b[l2.key] *= c2.value
					if l2_cardlist9_b[l2.key] > 0:
						l2_cardlist9_b[l2.key] = 1
				else:
					l2_cardlist9_b[l2.key] = c2.value
# 11张牌=>大			===>			3赖子+8张牌=>大
l3_cardlist8_a = {}
# 11张牌=>小			===>			3赖子+8张牌=>小
l3_cardlist8_b = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist11_a.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist8_a:
				l3_cardlist8_a[l3.key] *= c2.value
				if l3_cardlist8_a[l3.key] > 0:
					l3_cardlist8_a[l3.key] = 1
			else:
				l3_cardlist8_a[l3.key] = c2.value
	for ck, cv in cardlist11_b.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key[1] != '0' or l3.key[4] != '0' or l3.key[7] != '0':
				if l3.key in l3_cardlist8_b:
					l3_cardlist8_b[l3.key] *= c2.value
					if l3_cardlist8_b[l3.key] > 0:
						l3_cardlist8_b[l3.key] = 1
				else:
					l3_cardlist8_b[l3.key] = c2.value
# 11张牌=>大			===>			4赖子+7张牌=>大
l4_cardlist7_a = {}
# 11张牌=>小			===>			4赖子+7张牌=>小
l4_cardlist7_b = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist11_a.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist7_a:
				l4_cardlist7_a[l4.key] *= c2.value
				if l4_cardlist7_a[l4.key] > 0:
					l4_cardlist7_a[l4.key] = 1
			else:
				l4_cardlist7_a[l4.key] = c2.value
	for ck, cv in cardlist11_b.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key[1] != '0' or l4.key[4] != '0' or l4.key[7] != '0':
				if l4.key in l4_cardlist7_b:
					l4_cardlist7_b[l4.key] *= c2.value
					if l4_cardlist7_b[l4.key] > 0:
						l4_cardlist7_b[l4.key] = 1
				else:
					l4_cardlist7_b[l4.key] = c2.value
# 11张牌=>风			===>			1赖子+10张牌=>风
l1_cardlist10_f = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist11_f.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist10_f:
				l1_cardlist10_f[l1.key] *= c2.value
				if l1_cardlist10_f[l1.key] > 0:
					l1_cardlist10_f[l1.key] = 1
			else:
				l1_cardlist10_f[l1.key] = c2.value
# 11张牌=>风			===>			2赖子+9张牌=>风
l2_cardlist9_f = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist11_f.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist9_f:
				l2_cardlist9_f[l2.key] *= c2.value
				if l2_cardlist9_f[l2.key] > 0:
					l2_cardlist9_f[l2.key] = 1
			else:
				l2_cardlist9_f[l2.key] = c2.value
# 11张牌=>风			===>			3赖子+8张牌=>风
l3_cardlist8_f = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist11_f.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist8_f:
				l3_cardlist8_f[l3.key] *= c2.value
				if l3_cardlist8_f[l3.key] > 0:
					l3_cardlist8_f[l3.key] = 1
			else:
				l3_cardlist8_f[l3.key] = c2.value
# 11张牌=>风			===>			4赖子+7张牌=>风
l4_cardlist7_f = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist11_f.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist7_f:
				l4_cardlist7_f[l4.key] *= c2.value
				if l4_cardlist7_f[l4.key] > 0:
					l4_cardlist7_f[l4.key] = 1
			else:
				l4_cardlist7_f[l4.key] = c2.value

# 12张牌=>无			===>			1赖子+11张牌=>无
l1_cardlist11_n = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist12_n.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist11_n:
				l1_cardlist11_n[l1.key] *= c2.value
				if l1_cardlist11_n[l1.key] > 0:
					l1_cardlist11_n[l1.key] = 1
			else:
				l1_cardlist11_n[l1.key] = c2.value
# 12张牌=>无			===>			2赖子+10张牌=>无
l2_cardlist10_n = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist12_n.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist10_n:
				l2_cardlist10_n[l2.key] *= c2.value
				if l2_cardlist10_n[l2.key] > 0:
					l2_cardlist10_n[l2.key] = 1
			else:
				l2_cardlist10_n[l2.key] = c2.value
# 12张牌=>无			===>			3赖子+9张牌=>无
l3_cardlist9_n = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist12_n.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist9_n:
				l3_cardlist9_n[l3.key] *= c2.value
				if l3_cardlist9_n[l3.key] > 0:
					l3_cardlist9_n[l3.key] = 1
			else:
				l3_cardlist9_n[l3.key] = c2.value
# 12张牌=>无			===>			4赖子+8张牌=>无
l4_cardlist8_n = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist12_n.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist8_n:
				l4_cardlist8_n[l4.key] *= c2.value
				if l4_cardlist8_n[l4.key] > 0:
					l4_cardlist8_n[l4.key] = 1
			else:
				l4_cardlist8_n[l4.key] = c2.value
# 12张牌=>风			===>			1赖子+11张牌=>风
l1_cardlist11_f = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist12_f.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist11_f:
				l1_cardlist11_f[l1.key] *= c2.value
				if l1_cardlist11_f[l1.key] > 0:
					l1_cardlist11_f[l1.key] = 1
			else:
				l1_cardlist11_f[l1.key] = c2.value
# 12张牌=>风			===>			2赖子+10张牌=>风
l2_cardlist10_f = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist12_f.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist10_f:
				l2_cardlist10_f[l2.key] *= c2.value
				if l2_cardlist10_f[l2.key] > 0:
					l2_cardlist10_f[l2.key] = 1
			else:
				l2_cardlist10_f[l2.key] = c2.value
# 12张牌=>风			===>			3赖子+9张牌=>风
l3_cardlist9_f = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist12_f.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist9_f:
				l3_cardlist9_f[l3.key] *= c2.value
				if l3_cardlist9_f[l3.key] > 0:
					l3_cardlist9_f[l3.key] = 1
			else:
				l3_cardlist9_f[l3.key] = c2.value
# 12张牌=>风			===>			4赖子+8张牌=>风
l4_cardlist8_f = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist12_f.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist8_f:
				l4_cardlist8_f[l4.key] *= c2.value
				if l4_cardlist8_f[l4.key] > 0:
					l4_cardlist8_f[l4.key] = 1
			else:
				l4_cardlist8_f[l4.key] = c2.value

# 14张牌=>大			===>			1赖子+13张牌=>大
l1_cardlist13_a = {}
# 14张牌=>小			===>			1赖子+13张牌=>小
l1_cardlist13_b = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist14_a.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist13_a:
				l1_cardlist13_a[l1.key] *= c2.value
				if l1_cardlist13_a[l1.key] > 0:
					l1_cardlist13_a[l1.key] = 1
			else:
				l1_cardlist13_a[l1.key] = c2.value
	for ck, cv in cardlist14_b.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist13_b:
				l1_cardlist13_b[l1.key] *= c2.value
				if l1_cardlist13_b[l1.key] > 0:
					l1_cardlist13_b[l1.key] = 1
			else:
				l1_cardlist13_b[l1.key] = c2.value
# 14张牌=>大			===>			2赖子+12张牌=>大
l2_cardlist12_a = {}
# 14张牌=>小			===>			2赖子+12张牌=>小
l2_cardlist12_b = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist14_a.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist12_a:
				l2_cardlist12_a[l2.key] *= c2.value
				if l2_cardlist12_a[l2.key] > 0:
					l2_cardlist12_a[l2.key] = 1
			else:
				l2_cardlist12_a[l2.key] = c2.value
	for ck, cv in cardlist14_b.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key[1] != '0' or l2.key[4] != '0' or l2.key[7] != '0':
				if l2.key in l2_cardlist12_b:
					l2_cardlist12_b[l2.key] *= c2.value
					if l2_cardlist12_b[l2.key] > 0:
						l2_cardlist12_b[l2.key] = 1
				else:
					l2_cardlist12_b[l2.key] = c2.value
# 14张牌=>大			===>			3赖子+11张牌=>大
l3_cardlist11_a = {}
# 14张牌=>小			===>			3赖子+11张牌=>小
l3_cardlist11_b = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist14_a.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist11_a:
				l3_cardlist11_a[l3.key] *= c2.value
				if l3_cardlist11_a[l3.key] > 0:
					l3_cardlist11_a[l3.key] = 1
			else:
				l3_cardlist11_a[l3.key] = c2.value
	for ck, cv in cardlist14_b.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key[1] != '0' or l3.key[4] != '0' or l3.key[7] != '0':
				if l3.key in l3_cardlist11_b:
					l3_cardlist11_b[l3.key] *= c2.value
					if l3_cardlist11_b[l3.key] > 0:
						l3_cardlist11_b[l3.key] = 1
				else:
					l3_cardlist11_b[l3.key] = c2.value
# 14张牌=>大			===>			4赖子+10张牌=>大
l4_cardlist10_a = {}
# 14张牌=>小			===>			4赖子+10张牌=>小
l4_cardlist10_b = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist14_a.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist10_a:
				l4_cardlist10_a[l4.key] *= c2.value
				if l4_cardlist10_a[l4.key] > 0:
					l4_cardlist10_a[l4.key] = 1
			else:
				l4_cardlist10_a[l4.key] = c2.value
	for ck, cv in cardlist14_b.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key[1] != '0' or l4.key[4] != '0' or l4.key[7] != '0':
				if l4.key in l4_cardlist10_b:
					l4_cardlist10_b[l4.key] *= c2.value
					if l4_cardlist10_b[l4.key] > 0:
						l4_cardlist10_b[l4.key] = 1
				else:
					l4_cardlist10_b[l4.key] = c2.value
# 14张牌=>风			===>			1赖子+13张牌=>风
l1_cardlist13_f = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist14_f.items():
		c2 = ListCard(ck, cv)
		l1 = ListCard()
		if l1.minus(c2, c1) == True:
			if l1.key in l1_cardlist13_f:
				l1_cardlist13_f[l1.key] *= c2.value
				if l1_cardlist13_f[l1.key] > 0:
					l1_cardlist13_f[l1.key] = 1
			else:
				l1_cardlist13_f[l1.key] = c2.value
# 14张牌=>风			===>			2赖子+12张牌=>风
l2_cardlist12_f = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist14_f.items():
		c2 = ListCard(ck, cv)
		l2 = ListCard()
		if l2.minus(c2, c1) == True:
			if l2.key in l2_cardlist12_f:
				l2_cardlist12_f[l2.key] *= c2.value
				if l2_cardlist12_f[l2.key] > 0:
					l2_cardlist12_f[l2.key] = 1
			else:
				l2_cardlist12_f[l2.key] = c2.value
# 14张牌=>风			===>			3赖子+11张牌=>风
l3_cardlist11_f = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist14_f.items():
		c2 = ListCard(ck, cv)
		l3 = ListCard()
		if l3.minus(c2, c1) == True:
			if l3.key in l3_cardlist11_f:
				l3_cardlist11_f[l3.key] *= c2.value
				if l3_cardlist11_f[l3.key] > 0:
					l3_cardlist11_f[l3.key] = 1
			else:
				l3_cardlist11_f[l3.key] = c2.value
# 14张牌=>风			===>			4赖子+10张牌=>风
l4_cardlist10_f = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist14_f.items():
		c2 = ListCard(ck, cv)
		l4 = ListCard()
		if l4.minus(c2, c1) == True:
			if l4.key in l4_cardlist10_f:
				l4_cardlist10_f[l4.key] *= c2.value
				if l4_cardlist10_f[l4.key] > 0:
					l4_cardlist10_f[l4.key] = 1
			else:
				l4_cardlist10_f[l4.key] = c2.value


claizi0[2]['a'] = cardlist2_a
claizi0[2]['b'] = cardlist2_b
claizi0[2]['f'] = cardlist2_f
claizi0[3]['n'] = cardlist3_n
claizi0[3]['f'] = cardlist3_f
claizi0[5]['a'] = cardlist5_a
claizi0[5]['b'] = cardlist5_b
claizi0[5]['f'] = cardlist5_f
claizi0[6]['n'] = cardlist6_n
claizi0[6]['f'] = cardlist6_f
claizi0[8]['a'] = cardlist8_a
claizi0[8]['b'] = cardlist8_b
claizi0[8]['f'] = cardlist8_f
claizi0[9]['n'] = cardlist9_n
claizi0[9]['f'] = cardlist9_f
claizi0[11]['a'] = cardlist11_a
claizi0[11]['b'] = cardlist11_b
claizi0[11]['f'] = cardlist11_f
claizi0[12]['n'] = cardlist12_n
claizi0[12]['f'] = cardlist12_f
claizi0[14]['a'] = cardlist14_a
claizi0[14]['b'] = cardlist14_b
claizi0[14]['f'] = cardlist14_f

claizi1[1]['a'] = l1_cardlist1_a
claizi1[1]['b'] = l1_cardlist1_b
claizi1[1]['f'] = l1_cardlist1_f

claizi1[2]['n'] = l1_cardlist2_n
claizi2[1]['n'] = l2_cardlist1_n
claizi1[2]['f'] = l1_cardlist2_f
claizi2[1]['f'] = l2_cardlist1_f

claizi1[4]['a'] = l1_cardlist4_a
claizi1[4]['b'] = l1_cardlist4_b
claizi2[3]['a'] = l2_cardlist3_a
claizi2[3]['b'] = l2_cardlist3_b
claizi3[2]['a'] = l3_cardlist2_a
claizi3[2]['b'] = l3_cardlist2_b
claizi4[1]['a'] = l4_cardlist1_a
claizi4[1]['b'] = l4_cardlist1_b
claizi1[4]['f'] = l1_cardlist4_f
claizi2[3]['f'] = l2_cardlist3_f
claizi3[2]['f'] = l3_cardlist2_f
claizi4[1]['f'] = l4_cardlist1_f

claizi1[5]['n'] = l1_cardlist5_n
claizi2[4]['n'] = l2_cardlist4_n
claizi3[3]['n'] = l3_cardlist3_n
claizi4[2]['n'] = l4_cardlist2_n
claizi1[5]['f'] = l1_cardlist5_f
claizi2[4]['f'] = l2_cardlist4_f
claizi3[3]['f'] = l3_cardlist3_f
claizi4[2]['f'] = l4_cardlist2_f

claizi1[7]['a'] = l1_cardlist7_a
claizi1[7]['b'] = l1_cardlist7_b
claizi2[6]['a'] = l2_cardlist6_a
claizi2[6]['b'] = l2_cardlist6_b
claizi3[5]['a'] = l3_cardlist5_a
claizi3[5]['b'] = l3_cardlist5_b
claizi4[4]['a'] = l4_cardlist4_a
claizi4[4]['b'] = l4_cardlist4_b
claizi1[7]['f'] = l1_cardlist7_f
claizi2[6]['f'] = l2_cardlist6_f
claizi3[5]['f'] = l3_cardlist5_f
claizi4[4]['f'] = l4_cardlist4_f

claizi1[8]['n'] = l1_cardlist8_n
claizi2[7]['n'] = l2_cardlist7_n
claizi3[6]['n'] = l3_cardlist6_n
claizi4[5]['n'] = l4_cardlist5_n
claizi1[8]['f'] = l1_cardlist8_f
claizi2[7]['f'] = l2_cardlist7_f
claizi3[6]['f'] = l3_cardlist6_f
claizi4[5]['f'] = l4_cardlist5_f

claizi1[10]['a'] = l1_cardlist10_a
claizi1[10]['b'] = l1_cardlist10_b
claizi2[9]['a'] = l2_cardlist9_a
claizi2[9]['b'] = l2_cardlist9_b
claizi3[8]['a'] = l3_cardlist8_a
claizi3[8]['b'] = l3_cardlist8_b
claizi4[7]['a'] = l4_cardlist7_a
claizi4[7]['b'] = l4_cardlist7_b
claizi1[10]['f'] = l1_cardlist10_f
claizi2[9]['f'] = l2_cardlist9_f
claizi3[8]['f'] = l3_cardlist8_f
claizi4[7]['f'] = l4_cardlist7_f

claizi1[11]['n'] = l1_cardlist11_n
claizi2[10]['n'] = l2_cardlist10_n
claizi3[9]['n'] = l3_cardlist9_n
claizi4[8]['n'] = l4_cardlist8_n
claizi1[11]['f'] = l1_cardlist11_f
claizi2[10]['f'] = l2_cardlist10_f
claizi3[9]['f'] = l3_cardlist9_f
claizi4[8]['f'] = l4_cardlist8_f

claizi1[13]['a'] = l1_cardlist13_a
claizi1[13]['b'] = l1_cardlist13_b
claizi2[12]['a'] = l2_cardlist12_a
claizi2[12]['b'] = l2_cardlist12_b
claizi3[11]['a'] = l3_cardlist11_a
claizi3[11]['b'] = l3_cardlist11_b
claizi4[10]['a'] = l4_cardlist10_a
claizi4[10]['b'] = l4_cardlist10_b
claizi1[13]['f'] = l1_cardlist13_f
claizi2[12]['f'] = l2_cardlist12_f
claizi3[11]['f'] = l3_cardlist11_f
claizi4[10]['f'] = l4_cardlist10_f


data = {}
data[0] = claizi0
data[1] = claizi1
data[2] = claizi2
data[3] = claizi3
data[4] = claizi4


with open("majiang.json", 'w', encoding='utf-8') as json_file:
	json.dump(data, json_file, ensure_ascii = False, indent=4)

pass
