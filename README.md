我们先做不带赖子的麻将胡牌计算。

---

把手牌中某一个花色的牌整理成一个数字，规则如下，比如万字。
数值|手牌
---|---:
000000000|没有万字
100000000|一万(1)
200000000|一万(2)
210000000|一万(2) 二万(1)
...|...

---

手牌中任意一种花色的总张数，要么是3的倍数，要么是3的倍数+2，并且所有的花色加起来只能有一个3的倍数+2。
1. 这种花色有3张，这里就有9+7中可能，9的意思是3个1|3个2|...|3个9，7的意思是123|234|...|789。我们把这16种形状转换成str，用上面说的方法，保存到cardlist3_n这个字典中，key就是那个str，value等会儿再说(***)。
2. 这种花色有6张牌，无非就是cardlist3_n里面的16种可能*16种可能，最多256种。但是我们要排除一下，排除3个1+3个1，这种肯定是不行的，哪有6个1，而且还要去重。最终的结果保存到cardlist6_n中。
3. 这种花色有9张牌，那就是两重循环，cardlist6_n套上cardlist3_n，保存到cardlist9_n。
4. 这种花色有12张牌，实际上不可能，不开口不能胡，忽略了。

5. 这种花色有2张牌，这个就有歧义了，如果是屁胡，那就要258将，如果是大胡就不要，所以我们需要准备两个字典，一个叫cardlist2_a用来放大胡的str，一个叫cardlist2_b用来放屁胡的str。
6. 这种花色有5张牌，cardlist2_a(b)套上cardlist3_n，保存到cardlist5_a(b)。
7. 这种花色有8张牌，cardlist2_a(b)套上cardlist6_n，保存到cardlist8_a(b)。
8. 这种花色有11张牌，cardlist2_a(b)套上cardlist9_n，保存到cardlist11_a(b)。
9. 这种花色有14张牌，不开口不能胡，忽略了。

---

现在我们就拿到了，不带赖子的，所有花色允许的牌型(str)。我们把玩家的手牌，每种花色根据张数也整理出一个(几个)str，分别丢到对应的字典中查找，全部都找得到，代表可以匹配上。然后就是什么大胡屁胡之类的了，注意有且只有一个需要到5678步中匹配，其余的都要去123步中匹配。

---

(***)还有一个屁胡的判断，吃的牌另算，手牌，我们在生成cardlist3_n的时候，我们的value是有含义的。在3个1|...|3个9的时候，value是0；123|...|789的时候，values是1。后面的234678步的时候，当我们合并两组牌，都需要将value相加，如果相加的结果还是0，代表都是碰，大于0代表至少有一个吃。

---
---

现在我们加上赖子。赖子最多有四个赖子，那么我们就去生成一个类似上面的str。laizi1的意思是一个赖子的时候，可能替换的手牌，无非就是100000000|010000000|...|000000001。类似生成laizi2,laizi3,laizi4。

---

1. 我们对cardlist3_n这个字典需要改动，生成两个新的字典，一个叫l1_cardlist2_n(意思是带1个赖子+牌数量2+不分大小胡)，一个叫l2_cardlist1_n(意思是带2个赖子+牌数量1+不分大小胡)。我们将cardlist3_n循环减去laizi1，结果放到l1_cardlist2_n中，注意，每一个位置都不能减成负的。我们将cardlist3_n循环减去laizi2，结果放到l2_cardlist1_n中。
2. 我们对cardlist6_n这个字典循环生成l1_cardlist5_n + l2_cardlist4_n + l3_cardlist3_n + l4_cardlist2_n。
3. 我们对cardlist9_n这个字典循环生成l1_cardlist8_n + l2_cardlist7_n + l3_cardlist6_n + l4_cardlist3_n。
4. 不开口不能胡，忽略。
5. 我们对cardlist2_a(b)这个字典循环生成l1_cardlist1_a(b)。
6. 我们对cardlist5_a(b)这个字典循环生成l1_cardlist4_a(b) + l2_cardlist3_a(b) + l3_cardlist2_a(b) + l4_cardlist1_a(b)。
7. 我们对cardlist8_a(b)这个字典循环生成l1_cardlist7_a(b) + l2_cardlist6_a(b) + l3_cardlist5_a(b) + l4_cardlist4_a(b)。
8. 我们对cardlist11_a(b)这个字典循环生成l1_cardlist10_a(b) + l2_cardlist9_a(b) + l3_cardlist8_a(b) + l4_cardlist7_a(b)。
9. 不开口不能胡，忽略。

---
---

剩下的就是保存了。
JSON层数|内容
---|---:
第一层|0个赖子|1个赖子|2个赖子|3个赖子|4个赖子。
第二层|张数
第三层|n(3的倍数)
第三层|a(3的倍数+2并且是大胡)
第三层|b(3的倍数+2并且是屁胡)
第四层|str=>value(大于0代表是屁胡)

---

游戏中加载这个JSON到map结构，将手牌+待计算的牌，生成每种花色对应的str，到对应的层中进行匹配，看能否找到第四层中的key。如果所有花色都可以匹配到，并且符合大胡屁胡规则，赖子数量足够，没有皮子，带赖子有且仅有一个花色数量是3的倍数余2，开口等。

---

没有考虑花色是风的规则，那个太简单，不在考虑范围内。
