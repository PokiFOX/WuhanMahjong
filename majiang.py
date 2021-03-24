'''
我们先做不带赖子的麻将胡牌计算。

把手牌中某一个花色的牌整理成一个数字，规则如下，比如万字。
0x000000000	=>	没有万字
0x100000000	=>	一万*1
0x200000000	=>	一万*2
0x210000000	=>	一万*2 二万*1
...

手牌中任意一种花色的总张数，要么是3的倍数，要么是3的倍数+2，并且所有的花色加起来只能有一个3的倍数+2。

第一步：这种花色有3张，这里就有9+7中可能，9的意思是3个1|3个2|...|3个9，7的意思是123|234|...|789。我们把这16种形状转换成int，用上面说的方法，保存到cardlist3_n这个字典中，key就是那个int，value等会儿再说(***)。
第二步：这种花色有6张牌，无非就是cardlist3_n里面的16种可能*16种可能，最多256种。但是我们要排除一下，排除3个1+3个1，这种肯定是不行的，哪有6个1，而且还要去重。最终的结果保存到cardlist6_n中。
第三步：这种花色有9张牌，那就是两重循环，cardlist6_n套上cardlist3_n，保存到cardlist9_n。
第四步：这种花色有12张牌，实际上不可能，不开口不能胡，忽略了。

第五步：这种花色有2张牌，这个就有歧义了，如果是屁胡，那就要258将，如果是大胡就不要，所以我们需要准备两个字典，一个叫cardlist2_a用来放大胡的int，一个叫cardlist2_b用来放屁胡的int。
第六步：这种花色有5张牌，cardlist2_a(b)套上cardlist3_n，保存到cardlist5_a(b)。
第七步：这种花色有8张牌，cardlist2_a(b)套上cardlist6_n，保存到cardlist8_a(b)。
第八步：这种花色有11张牌，cardlist2_a(b)套上cardlist9_n，保存到cardlist11_a(b)。
第九步：这种花色有14张牌，不开口不能胡，忽略了。

现在我们就拿到了，不带赖子的，所有花色允许的牌型(int)。我们把玩家的手牌，每种花色根据张数也整理出一个(几个)int，分别丢到对应的字典中查找，全部都找得到，代表可以匹配上。然后就是什么大胡屁胡之类的了，注意有且只有一个需要到5678步中匹配，其余的都要去123步中匹配。

(***)还有一个屁胡的判断，吃的牌另算，手牌，我们在生成cardlist3_n的时候，我们的value是有含义的，在3个1|...|3个9的时候，value是0，123|...|789的时候，values是1，后面的234678步的时候，当我们合并两组牌，都需要将value相加，如果相加的结果还是0，代表都是碰，大于0代表至少有一个吃。


现在我们加上赖子。赖子最多有四个赖子，那么我们就去生成一个类似上面的int
laizi1的意思是一个赖子的时候，可能替换的手牌，无非就是0x100000000|0x010000000|...|0x000000001。类似生成laizi2,laizi3,laizi4。

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
第二层：张数
第三层：n(3的倍数) a(3的倍数+2并且是大胡) b(3的倍数+2并且是屁胡)
第四层：int=>value(大于0代表是屁胡)
'''


import json

class ListCard :
	def __init__(self, _k = 0x000000000, _v = 0x00):
		self.key = _k
		self.value = _v

	def addcard(self, pos, num=1):
		if pos >= 1 and pos <= 9:
			self.key += num << ((pos - 1) * 4)

	def initfrom(self, c1, c2):
		nk = c1.key + c2.key
		nv = c1.value + c2.value
		for i in range(1, 10):
			n = (nk & (0xF << (i - 1) * 4)) >> ((i - 1) * 4)
			if n > 4:
				return False
		self.key = nk
		self.value = nv
		return True

	def minus(self, laizi):
		nd = 0
		for i in range(1, 10):
			n1 = (self.key & (0xF << (i - 1) * 4)) >> ((i - 1) * 4)
			n2 = (laizi.key & (0xF << (i - 1) * 4)) >> ((i - 1) * 4)
			if n1 < n2:
				return False
			nd += (n1 - n2) << ((i - 1) * 4)
		self.key = nd
		return True


# 2张牌=>大
cardlist2_a = {}
for i in range(1, 10):
	l2 = ListCard()
	l2.addcard(i, 2)
	cardlist2_a[l2.key] = l2.value
# 2张牌=>小
cardlist2_b = {}
l2 = ListCard()
l2.addcard(2, 2)
cardlist2_b[l2.key] = l2.value
l5 = ListCard()
l5.addcard(5, 2)
cardlist2_b[l5.key] = l5.value
l8 = ListCard()
l8.addcard(8, 2)
cardlist2_b[l8.key] = l8.value

# 3张牌=>无
cardlist3_n = {}
for i in range(1, 10):
	l3 = ListCard()
	l3.addcard(i, 3)
	l3.value = 0
	cardlist3_n[l3.key] = l3.value
for i in range(1, 8):
	l3 = ListCard()
	l3.addcard(i, 1)
	l3.addcard(i + 1, 1)
	l3.addcard(i + 2, 1)
	l3.value = 1
	cardlist3_n[l3.key] = l3.value

# 5张牌=>大
cardlist5_a = {}
for k1, v1 in cardlist2_a.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_n.items():
		c2 = ListCard(k2, v2)
		l5 = ListCard()
		if l5.initfrom(c1, c2) == True:
			cardlist5_a[l5.key] = l5.value
# 5张牌=>小
cardlist5_b = {}
for k1, v1 in cardlist2_b.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_n.items():
		c2 = ListCard(k2, v2)
		l5 = ListCard()
		if l5.initfrom(c1, c2) == True:
			cardlist5_b[l5.key] = l5.value

# 6张牌=>无
cardlist6_n = {}
for k1, v1 in cardlist3_n.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_n.items():
		c2 = ListCard(k2, v2)
		l6 = ListCard()
		if l6.initfrom(c1, c2) == True:
			cardlist6_n[l6.key] = l6.value

# 8张牌=>大
cardlist8_a = {}
for k1, v1 in cardlist2_a.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist6_n.items():
		c2 = ListCard(k2, v2)
		l8 = ListCard()
		if l8.initfrom(c1, c2) == True:
			cardlist8_a[l8.key] = l8.value
# 8张牌=>小
cardlist8_b = {}
for k1, v1 in cardlist2_b.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist6_n.items():
		c2 = ListCard(k2, v2)
		l8 = ListCard()
		if l8.initfrom(c1, c2) == True:
			cardlist8_b[l8.key] = l8.value

# 9张牌=>无
cardlist9_n = {}
for k1, v1 in cardlist6_n.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist3_n.items():
		c2 = ListCard(k2, v2)
		l9 = ListCard()
		if l9.initfrom(c1, c2) == True:
			cardlist9_n[l9.key] = l9.value

# 11张牌=>大
cardlist11_a = {}
for k1, v1 in cardlist2_a.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist9_n.items():
		c2 = ListCard(k2, v2)
		l11 = ListCard()
		if l11.initfrom(c1, c2) == True:
			cardlist11_a[l11.key] = l11.value
# 11张牌=>小
cardlist11_b = {}
for k1, v1 in cardlist2_b.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in cardlist9_n.items():
		c2 = ListCard(k2, v2)
		l11 = ListCard()
		if l11.initfrom(c1, c2) == True:
			cardlist11_b[l11.key] = l11.value

"""
# 12张牌=>无
card12list_n = {}
for k1, v1 in card9list_n.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in card3list_n.items():
		c2 = ListCard(k2, v2)

		l12 = ListCard()
		if l12.initfrom(c1, c2) == True:
			card12list_n[l12.key] = l12.value

# 14张牌=>大
card14list_a = {}
for k1, v1 in card2list_a.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in card12list_n.items():
		c2 = ListCard(k2, v2)

		l14 = ListCard()
		if l14.initfrom(c1, c2) == True:
			card14list_a[l14.key] = l14.value
# 14张牌=>小
card14list_b = {}
for k1, v1 in card2list_b.items():
	c1 = ListCard(k1, v1)
	for k2, v2 in card12list_n.items():
		c2 = ListCard(k2, v2)

		l14 = ListCard()
		if l14.initfrom(c1, c2) == True:
			card14list_b[l14.key] = l14.value
"""


laizi1 = {}
for i in range(1, 10):
	l = ListCard()
	l.addcard(i)
	laizi1[l.key] = l.value

laizi2 = {}
for i in range(1, 10):
	l = ListCard()
	l.addcard(i, 2)
	laizi2[l.key] = l.value
for k1, v1 in laizi1.items():
	l1 = ListCard(k1, v1)
	for k2, v2 in laizi1.items():
		l2 = ListCard(k2, v2)
		l = ListCard()
		l.initfrom(l1, l2)
		laizi2[l.key] = l.value

laizi3 = {}
for i in range(1, 10):
	l = ListCard()
	l.addcard(i, 3)
	laizi3[l.key] = l.value
for k1, v1 in laizi2.items():
	l1 = ListCard(k1, v1)
	for k2, v2 in laizi1.items():
		l2 = ListCard(k2, v2)
		l = ListCard()
		l.initfrom(l1, l2)
		laizi3[l.key] = l.value

laizi4 = {}
for i in range(1, 10):
	l = ListCard()
	l.addcard(i, 4)
	laizi4[l.key] = l.value
for k1, v1 in laizi3.items():
	l1 = ListCard(k1, v1)
	for k2, v2 in laizi1.items():
		l2 = ListCard(k2, v2)
		l = ListCard()
		l.initfrom(l1, l2)
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
		if c2.minus(c1) == True:
			l1_cardlist1_a[c2.key] = c2.value
	for ck, cv in cardlist2_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist1_b[c2.key] = c2.value

# 3张牌=>无				===>			1赖子+2张牌=>无
l1_cardlist2_n = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist3_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist2_n[c2.key] = c2.value
# 3张牌=>无				===>			2赖子+1张牌=>无
l2_cardlist1_n = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist3_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l2_cardlist1_n[c2.key] = c2.value


# 5张牌=>大				===>			1赖子+4张牌=>大
l1_cardlist4_a = {}
# 5张牌=>小				===>			1赖子+4张牌=>小
l1_cardlist4_b = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist5_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist4_a[c2.key] = c2.value
	for ck, cv in cardlist5_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist4_b[c2.key] = c2.value
# 5张牌=>大				===>			2赖子+3张牌=>大
l2_cardlist3_a = {}
# 5张牌=>小				===>			2赖子+3张牌=>小
l2_cardlist3_b = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist5_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l2_cardlist3_a[c2.key] = c2.value
	for ck, cv in cardlist5_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l2_cardlist3_b[c2.key] = c2.value
# 5张牌=>大				===>			3赖子+2张牌=>大
l3_cardlist2_a = {}
# 5张牌=>小				===>			3赖子+2张牌=>小
l3_cardlist2_b = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist5_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l3_cardlist2_a[c2.key] = c2.value
	for ck, cv in cardlist5_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l3_cardlist2_b[c2.key] = c2.value
# 5张牌=>大				===>			4赖子+1张牌=>大
l4_cardlist1_a = {}
# 5张牌=>小				===>			4赖子+1张牌=>小
l4_cardlist1_b = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist5_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l4_cardlist1_a[c2.key] = c2.value
	for ck, cv in cardlist5_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l4_cardlist1_b[c2.key] = c2.value


# 6张牌=>无				===>			1赖子+5张牌=>无
l1_cardlist5_n = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist6_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist5_n[c2.key] = c2.value
# 6张牌=>无				===>			2赖子+4张牌=>无
l2_cardlist4_n = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist6_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l2_cardlist4_n[c2.key] = c2.value
# 6张牌=>无				===>			3赖子+3张牌=>无
l3_cardlist3_n = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist6_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l3_cardlist3_n[c2.key] = c2.value
# 6张牌=>无				===>			4赖子+2张牌=>无
l4_cardlist2_n = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist6_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l4_cardlist2_n[c2.key] = c2.value


# 8张牌=>大				===>			1赖子+7张牌=>大
l1_cardlist7_a = {}
# 8张牌=>小				===>			1赖子+7张牌=>小
l1_cardlist7_b = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist8_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist7_a[c2.key] = c2.value
	for ck, cv in cardlist8_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist7_b[c2.key] = c2.value
# 8张牌=>大				===>			2赖子+6张牌=>大
l2_cardlist6_a = {}
# 8张牌=>小				===>			2赖子+6张牌=>小
l2_cardlist6_b = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist8_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l2_cardlist6_a[c2.key] = c2.value
	for ck, cv in cardlist8_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l2_cardlist6_b[c2.key] = c2.value
# 8张牌=>大				===>			3赖子+5张牌=>大
l3_cardlist5_a = {}
# 8张牌=>小				===>			3赖子+5张牌=>小
l3_cardlist5_b = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist8_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l3_cardlist5_a[c2.key] = c2.value
	for ck, cv in cardlist8_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l3_cardlist5_b[c2.key] = c2.value
# 8张牌=>大				===>			4赖子+4张牌=>大
l4_cardlist4_a = {}
# 8张牌=>小				===>			4赖子+4张牌=>小
l4_cardlist4_b = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist8_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l4_cardlist4_a[c2.key] = c2.value
	for ck, cv in cardlist8_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l4_cardlist4_b[c2.key] = c2.value


# 9张牌=>无				===>			1赖子+8张牌=>无
l1_cardlist8_n = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist9_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist8_n[c2.key] = c2.value
# 9张牌=>无				===>			2赖子+7张牌=>无
l2_cardlist7_n = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist9_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l2_cardlist7_n[c2.key] = c2.value
# 9张牌=>无				===>			3赖子+6张牌=>无
l3_cardlist6_n = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist9_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l3_cardlist6_n[c2.key] = c2.value
# 9张牌=>无				===>			4赖子+5张牌=>无
l4_cardlist5_n = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist9_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l4_cardlist5_n[c2.key] = c2.value


# 11张牌=>大			===>			1赖子+10张牌=>大
l1_cardlist10_a = {}
# 11张牌=>小			===>			1赖子+10张牌=>小
l1_cardlist10_b = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist11_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist10_a[c2.key] = c2.value
	for ck, cv in cardlist11_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist10_b[c2.key] = c2.value
# 11张牌=>大			===>			2赖子+9张牌=>大
l2_cardlist9_a = {}
# 11张牌=>小			===>			2赖子+9张牌=>小
l2_cardlist9_b = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist11_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l2_cardlist9_a[c2.key] = c2.value
	for ck, cv in cardlist11_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l2_cardlist9_b[c2.key] = c2.value
# 11张牌=>大			===>			3赖子+8张牌=>大
l3_cardlist8_a = {}
# 11张牌=>小			===>			3赖子+8张牌=>小
l3_cardlist8_b = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist11_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l3_cardlist8_a[c2.key] = c2.value
	for ck, cv in cardlist11_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l3_cardlist8_b[c2.key] = c2.value
# 11张牌=>大			===>			4赖子+7张牌=>大
l4_cardlist7_a = {}
# 11张牌=>小			===>			4赖子+7张牌=>小
l4_cardlist7_b = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist11_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l4_cardlist7_a[c2.key] = c2.value
	for ck, cv in cardlist11_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l4_cardlist7_b[c2.key] = c2.value


"""
# 12张牌=>无			===>			1赖子+11张牌=>无
l1_cardlist11_n = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist12_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist11_n[c2.key] = c2.value
# 12张牌=>无			===>			2赖子+10张牌=>无
l2_cardlist10_n = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist12_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l2_cardlist10_n[c2.key] = c2.value
# 12张牌=>无			===>			3赖子+9张牌=>无
l3_cardlist9_n = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist12_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l3_cardlist9_n[c2.key] = c2.value
# 12张牌=>无			===>			4赖子+8张牌=>无
l4_cardlist8_n = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist12_n.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l4_cardlist8_n[c2.key] = c2.value


# 14张牌=>大			===>			1赖子+11张牌=>大
l1_cardlist11_a = {}
# 14张牌=>小			===>			1赖子+11张牌=>小
l1_cardlist11_b = {}
for lk1, lv1 in laizi1.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist14_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist11_a[c2.key] = c2.value
	for ck, cv in cardlist14_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l1_cardlist11_b[c2.key] = c2.value
# 11张牌=>大			===>			2赖子+10张牌=>大
l2_cardlist10_a = {}
# 11张牌=>小			===>			2赖子+10张牌=>小
l2_cardlist10_b = {}
for lk1, lv1 in laizi2.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist14_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l2_cardlist10_a[c2.key] = c2.value
	for ck, cv in cardlist14_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l2_cardlist10_b[c2.key] = c2.value
# 11张牌=>大			===>			3赖子+9张牌=>大
l3_cardlist9_a = {}
# 11张牌=>小			===>			3赖子+9张牌=>小
l3_cardlist9_b = {}
for lk1, lv1 in laizi3.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist14_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l3_cardlist9_a[c2.key] = c2.value
	for ck, cv in cardlist14_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l3_cardlist9_b[c2.key] = c2.value
# 11张牌=>大			===>			4赖子+8张牌=>大
l4_cardlist8_a = {}
# 11张牌=>小			===>			4赖子+8张牌=>小
l4_cardlist8_b = {}
for lk1, lv1 in laizi4.items():
	c1 = ListCard(lk1, lv1)
	for ck, cv in cardlist14_a.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l4_cardlist8_a[c2.key] = c2.value
	for ck, cv in cardlist14_b.items():
		c2 = ListCard(ck, cv)
		if c2.minus(c1) == True:
			l4_cardlist8_b[c2.key] = c2.value
"""

claizi0[2]['a'] = cardlist2_a
claizi0[2]['b'] = cardlist2_b
claizi0[3]['n'] = cardlist3_n
claizi0[5]['a'] = cardlist5_a
claizi0[5]['b'] = cardlist5_b
claizi0[6]['n'] = cardlist6_n
claizi0[8]['a'] = cardlist8_a
claizi0[8]['b'] = cardlist8_b
claizi0[9]['n'] = cardlist9_n
claizi0[11]['a'] = cardlist11_a
claizi0[11]['b'] = cardlist11_b

claizi1[1]['a'] = l1_cardlist1_a
claizi1[1]['b'] = l1_cardlist1_b

claizi1[2]['n'] = l1_cardlist2_n
claizi2[1]['n'] = l2_cardlist1_n

claizi1[4]['a'] = l1_cardlist4_a
claizi1[4]['b'] = l1_cardlist4_b
claizi2[3]['a'] = l2_cardlist3_a
claizi2[3]['b'] = l2_cardlist3_b
claizi3[2]['a'] = l3_cardlist2_a
claizi3[2]['b'] = l3_cardlist2_b
claizi4[1]['a'] = l4_cardlist1_a
claizi4[1]['b'] = l4_cardlist1_b

claizi1[5]['n'] = l1_cardlist5_n
claizi2[4]['n'] = l2_cardlist4_n
claizi2[3]['n'] = l3_cardlist3_n
claizi2[2]['n'] = l4_cardlist2_n

claizi1[7]['a'] = l1_cardlist7_a
claizi1[7]['b'] = l1_cardlist7_b
claizi2[6]['a'] = l2_cardlist6_a
claizi2[6]['b'] = l2_cardlist6_b
claizi3[5]['a'] = l3_cardlist5_a
claizi3[5]['b'] = l3_cardlist5_b
claizi4[4]['a'] = l4_cardlist4_a
claizi4[4]['b'] = l4_cardlist4_b

claizi1[8]['n'] = l1_cardlist8_n
claizi2[7]['n'] = l2_cardlist7_n
claizi2[6]['n'] = l3_cardlist6_n
claizi2[5]['n'] = l4_cardlist5_n

claizi1[10]['a'] = l1_cardlist10_a
claizi1[10]['b'] = l1_cardlist10_b
claizi2[9]['a'] = l2_cardlist9_a
claizi2[9]['b'] = l2_cardlist9_b
claizi3[8]['a'] = l3_cardlist8_a
claizi3[8]['b'] = l3_cardlist8_b
claizi4[7]['a'] = l4_cardlist7_a
claizi4[7]['b'] = l4_cardlist7_b

data = {}
data[0] = claizi0
data[1] = claizi1
data[2] = claizi2
data[3] = claizi3
data[4] = claizi4


with open("majiang.json", 'w', encoding='utf-8') as json_file:
	json.dump(data, json_file, ensure_ascii = False, indent=4)

pass
