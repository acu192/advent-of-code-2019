# My Thoughts on this Challenge

### Ways to Think About It

I personally figured it out by reminding myself of the (Modular Arithmetic)[https://en.wikipedia.org/wiki/Modular_arithmetic] properties and then experimenting with different theories to find which were actually true (many things I thought might work did not actually work). I did this by comparing results with my original brute-force solution from Part 1. I eventually go the modular arithmetic stuff working where I could "reverse shuffle" the deck -- that was a big win. I then did more experiments to "exponentiate" the reverse shuffle and eventually got an algorithm working that did a "binary exponentiation" or "fast exponentiation" or "exponentiation by repeated squaring" (it goes by many names it seems), and that was finally the last piece and I got a working solution with these things combined (and with a lot of experiments along the way). See my Jupyter notebook for more detail on how I did it.

BTW, here is a great [review of modular arithmetic](https://math.libretexts.org/Bookshelves/Combinatorics_and_Discrete_Mathematics/Book%3A_A_Spiral_Workbook_for_Discrete_Mathematics_(Kwong)/05%3A_Basic_Number_Theory/5.07%3A_Modular_Arithmetic).

However, there are other ways to think about it (there is of course a lot of overlap in these different way, but they are different enough I wanted to write a bit of notes about them). I found these other ideas on Reddit (after I solved it on my own).

This post:
 - https://www.reddit.com/r/adventofcode/comments/eeb40v/day_22_part_2/

Correctly points out that a "shuffle" is just the application of a Linear Congruential Generator (LCG), which is a nice way to look at this. In fact, each of the operations individually is seen as an LCG, and to get the whole shuffle you combine the LCGs together into a "super LCG". Then there are clever modular arithmetic ways to "fast-forward" the LCG so you can get an equivalent LCG which applies the original one X times.

Indeed, when I read this I realized I had implemented this "fast-forward" LCG thing before!!! OMG, I had forgotten until now. [Here's a link to my old code.](https://github.com/acu192/archive-2011/blob/febad3454fb147ce8d6c3b66d238651ff2957ba9/challenge_24/EC/solutions/D.cpp#L44)

*ALTERNITIVLY*

This post:
 - https://www.reddit.com/r/adventofcode/comments/ee56wh/2019_day_22_part_2_so_whats_the_purpose_of_this/fbqctrr/?utm_source=share&utm_medium=web2x

Argues that this challenge _was_ easy enough to solve without a math background. He described a divide-and-conquer recursive idea for doing the exponentiation operation, and even posted Python code for it, copied below (which I like how he thought about it). Granted, this guy I guess assumes that expressing the entire shuffle routine in terms of `a` and `b` is a given... which is highly questionable, but anyway:

```python
def run_many(a,b,e):
  if e==1:
    return a,b
  elif e%2==0:
    return run_many((a*a)%LEN, (a*b+b)%LEN, e/2)
  else:
    c,d = run_many(a,b,e-1)
    return (a*c)%LEN,(a*d+b)%LEN
```

*ALTERNITIVLY*

This person has the most concise solution I found. It's tiny...
 - https://github.com/crazymerlyn/adventofcode/blob/master/src/day22.py

I only understand ~25% of their `repeat_mul()` function... but alas. It seems interesting.

### Controversy

While on Reddit (see above), I was surprised to find a ton of controversy about this puzzle. Many people hated it and thought it was unfair to give such a puzzle, while other (less people though) came out and said it was plenty fair, or that they loved it themselves, or both., e.g.:
 - https://www.reddit.com/r/adventofcode/comments/eeeixy/remember_the_challenges_arent_here_for_you_to/
 - https://www.reddit.com/r/adventofcode/comments/ee56wh/2019_day_22_part_2_so_whats_the_purpose_of_this/

To summarize, some people said it wasn't fair because you had to be an expert in mathematics (specifically modular arithmetic) to solve it. One person then said "no I solved it without using any modular arithmetic" -- indeed he did but his solution was very painful (he described it and gave a link). Others argued that they enjoyed it because it forced them to either go learn modular arithmetic (or at least review it (I personally am in this camp)), generally these folks were okay with puzzles forcing them to learn something instead of just quickly implementing something they already know. But the other side then came back and argued that there were no hints about _what_ needed to be learned. E.g. "I didn't even know what to Google!" Anyway, a lot of opinions for sure. Some just took the stance "yeah, AoC has hard puzzles so if you don't like a puzzle, just skip it" while others said "not AoC is supposed to give puzzles that average CS people can solve in 1 hr" while then there would be replies like "oh but you _do_ learn modular arithmetic in CS degrees so this _is_ such a problem" and it goes on and on.

The best defense of the complainers is this:

> When people don't know graph theory, should they complain about the puzzles on days 15, 18, and 20? When they never wrote a VM, should they complain about all the intcode puzzles? When they don't know about boolean algebra, should they complain about day 21?
>
> Modular arithmetic is not that hard, and you could have used this puzzle as an opportunity to learn something.

### Final Summary

I think the following post on Reddit does the best job both summarizing the solution process, and also describing why some people are upset about it:

> I think the main issue OP brings is that there is no "lead-up" to the background knowledge required for this puzzle, and that the word "modulo" appears nowhere in the prose. The insights I required to solve this puzzle are:
>
> 1. Notice that each step can be described as a linear congruential function f(x) = ax + b mod n
>
> 2. Realize that the entire input can be composed into a single linear congruential function
>
> 3. Realize that a linear congruential function can be composed into itself a lot of times using a process similar to exponentiation by squaring (this took me a while, in fact I arrived at it in a roundabout way using matrices. At least I can say that this puzzle taught me something.)
>
> 4. Understand how to invert a linear congruential function, which requires modular multiplicative inverse.
>
> I think the main complaint is that if you can't even see step 1, it's nearly impossible to even understand what research you need to help complete the puzzle.

