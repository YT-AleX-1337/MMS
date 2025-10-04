# Mutant Matrix System (Python Implementation)
MMS implementation in Python. Original code in JavaScript by HypCos (https://github.com/hypcos/notation-explorer/blob/master/MM3.js)<br/>
First version released on October 7th, 2024.<br/>
**Update:** on October 2nd, 2025 (nearly a year after the first release...) **I finally implemented MMS sequence to MMS conversion!**

## What's MMS
[Mutant Matrix System (MMS)](https://googology.miraheze.org/wiki/Mutant_Matrix_System) is an ordinal notation (that is, a way of notating transfinite ordinals) developed by Aarex and HypCos. It's basically the most powerful well defined notation, being more powerful than [Bashicu Matrix System (BMS)](https://googology.miraheze.org/wiki/Bashicu_matrix_system), [Y sequence](https://googology.miraheze.org/wiki/Y_sequence) and [ω-Y sequence](https://googology.miraheze.org/wiki/%5C(%5Comega%5C)-Y_sequence) (the previous most powerful notation).<br/><br/>
Examples:<br/>
<br/>
Empty matrix corresponds to 0<br/>
(0) corresponds to 1<br/>
(0)(0) corresponds to 2<br/>
(0)(0)(0) corresponds to 3<br/>
(0)(0)(0)(0) corresponds to 4<br/>
(0)(0)(0)(0)(0) corresponds to 5<br/>
(0)(1) corresponds to [ω](https://googology.miraheze.org/wiki/%5C(%5Comega%5C)) (ω is the lowercase greek letter omega and it represents the first infinite ordinal)<br/>
(0)(1)(0) corresponds to ω+1<br/>
(0)(1)(0)(0) corresponds to ω+2<br/>
(0)(1)(0)(0)(0) corresponds to ω+3<br/>
(0)(1)(0)(1) corresponds to ω\*2<br/>
(0)(1)(0)(1)(0)(1) corresponds to ω\*3<br/>
(0)(1)(1) corresponds to ω\^2<br/>
(0)(1)(1)(0) corresponds to ω\^2+1<br/>
(0)(1)(1)(0)(1) corresponds to ω\^2+ω<br/>
(0)(1)(1)(0)(1)(1) corresponds to ω\^2\*2<br/>
(0)(1)(1)(1) corresponds to ω\^3<br/>
(0)(1)(1)(1)(1) corresponds to ω\^4<br/>
(0)(1)(2) corresponds to ω\^ω<br/>
(0)(1)(2)(0) corresponds to ω\^ω<br/>
(0)(1)(2)(0)(1)(2) corresponds to ω\^ω\*2<br/>
(0)(1)(2)(1) corresponds to ω\^(ω+1)<br/>
(0)(1)(2)(1)(2) corresponds to ω\^(ω\*2)<br/>
(0)(1)(2)(2) corresponds to ω\^ω\^2<br/>
(0)(1)(2)(2)(2) corresponds to ω\^ω\^3<br/>
(0)(1)(2)(3) corresponds to ω\^ω\^ω<br/>
(0)(1)(2)(3)(4) corresponds to ω\^ω\^ω\^ω<br/>
(0)(1)(2,1) corresponds to [ε_0](https://googology.miraheze.org/wiki/%CE%95%E2%82%80) (ε is the greek letter epsilon, and ε_0 represents an ω-long power tower of ω, that is, ω\^ω\^ω\^ω\^ω\^ω\^ω\^...)<br/>

I'll now speed up significantly (maybe some day I will post a more detailed analysis)<br/>

(0)(1)(2,1)(2,1) corresponds to ε_1<br/>
(0)(1)(2,1)(3) corresponds to ε_ω<br/>
(0)(1)(2,1)(3)(4,1) corresponds to ε_ε_0<br/>
(0)(1)(2,1)(3,1) corresponds to [ζ_0](https://googology.miraheze.org/wiki/Cantor%27s_ordinal)<br/>
(0)(1)(2,1)(3,1)(3,1) corresponds to ϕ(4,0)<br/>
(0)(1)(2,1)(3,1)(4) corresponds to ϕ(ω,0)<br/>
(0)(1)(2,1)(3,1)(4)(5,1) corresponds to ϕ(ε_0,0)<br/>
(0)(1)(2,1)(3,1)(4)(5,1)(6,1) corresponds to ϕ(ζ_0,0)<br/>
(0)(1)(2,1)(3,1)(4,1) corresponds to [Γ_0](https://googology.miraheze.org/wiki/Feferman%E2%80%93Sch%C3%BCtte_ordinal) = ϕ(1,0,0) = ψ(Ω^Ω)<br/>
(0)(1)(2,1)(3,1)(4,1)(4) corresponds to ϕ(ω,0,0) = ψ(Ω^(Ω\*ω))<br/>
(0)(1)(2,1)(3,1)(4,1)(4,1) corresponds to [ϕ(1,0,0,0)](https://googology.miraheze.org/wiki/Ackermann_ordinal) = ψ(Ω^Ω^2)<br/>
(0)(1)(2,1)(3,1)(4,1)(5) corresponds to ψ(Ω^Ω^ω) ([the Small Veblen Ordinal (SVO)](https://googology.miraheze.org/wiki/Small_Veblen_ordinal))<br/>
(0)(1)(2,1)(3,1)(4,1)(5,1) corresponds to ψ(Ω^Ω^Ω) ([the Large Veblen Ordinal (LVO)](https://googology.miraheze.org/wiki/Large_Veblen_ordinal))<br/>
(0)(1)(2,1)(3,1)(4,1)(5,1)(6,1) corresponds to ψ(Ω^Ω^Ω^Ω)<br/>
(0)(1)(2,1)(3,2) corresponds to ψ(ε_(Ω+1)) ([the Bachmann-Howard Ordinal (BHO)](https://googology.miraheze.org/wiki/Bachmann-Howard_ordinal))<br/>

Now skipping to only the most important milestone ordinals:<br/>

(0)(1)(2,1)(3,2,1) is the [Buchholz Ordinal](https://googology.miraheze.org/wiki/%CE%A8_0(%CE%A9_%CF%89))<br/>
(0)(1)(2,1)(3,2,1)(4,2)(5,2,1) is the [Takeuti-Feferman-Buchholz Ordinal](https://googology.miraheze.org/wiki/Takeuti-Feferman-Buchholz_ordinal)<br/>
(0)(1)(2,1)(3,2,1)(4,2,1)(5,1) is the limit of [Bird's Array Notation (BAN)](https://googology.miraheze.org/wiki/Bird%27s_array_notation)<br/>
(0)(1)(2,1)(3,2,1)(4,2,1)(5,2)(4) is the [Extended Buchholz Ordinal (EBO)](https://googology.miraheze.org/wiki/Extended_Buchholz%27s_ordinal)<br/>
(0)(1)(2,1)(3,2,1)(4,3) is the limit of [Primary Dropping Array Notation (pDAN)](https://googology.miraheze.org/wiki/Primary_dropping_array_notation)<br/>
(0)(1)(2,1)(3,2,1)(4,3,1)(4,2,1)(5,2,1)(5) is the limit of Secondary Dropping Array Notation (sDAN)<br/>
(0)(1)(2,1)(3,2,1)(4,3,1)(5) is the limit of Dropping Array Notation (DAN) (and therefore [Strong Array Notation (SAN)](https://googology.miraheze.org/wiki/Strong_array_notation) as a whole)<br/>

(0)(1)(2,1)(3,2,1)(4,3,2,1) is the limit of Trio Sequence System (TSS)<br/>
(0)(1)(2,1)(3,2,1)(4,3,2,1)(5,4,3,2,1) is the limit of Quad Sequence System (QSS)<br/>
(0)(1,1) is the limit of [Bashicu Matrix System (BMS)](https://googology.miraheze.org/wiki/Bashicu_matrix_system) as a whole<br/>
(0)(1,1)(2) is Y(1,3,4)<br/>
(0)(1,1)(2)(1,1) is Y(1,3,4,3)<br/>
(0)(1,1)(2,1) is Y(1,3,5)<br/>
(0)(1,1)(2,1)(3,2) is Y(1,3,6)<br/>
(0)(1,1)(2,1,1) is Y(1,3,7)<br/>
(0)(1,1)(2,2) is Y(1,3,8)<br/>
(0)(1,1)(2,2,1) is Y(1,3,9)<br/>
(0)(1,1)(2,2,1)(3,3,2,1) is Y(1,3,9,27)<br/>
(0)(1,1)(2,2,1)(3,3,2,1,1) is Y(1,4)<br/>
(0)(1,1)(2,2,1)(3,3,2,1,1)(4,4,3,2,2,1) is Y(1,4,16)<br/>
(0)(1,1)(2,2,1)(3,3,2,1,1)(4,4,3,2,2,1)(5,5,4,3,3,2,1,1) is Y(1,5)<br/>
(0)(1,1)(2,2,1,1) is the limit of [Y sequence](https://googology.miraheze.org/wiki/Y_sequence) = ω-Y(1,4)<br/>
(0)(1,1)(2,2,1,1)(3,3,2,2,1)(4,4,3,3,2,1,1)(5,5,4,4,3,2,2,1,1) is ω-Y(1,4,20)<br/>
(0)(1,1)(2,2,1,1)(3,3,2,2,1,1) is ω-Y(1,5)<br/>
(0)(1,1)(2,2,1,1)(3,3,2,2,1,1)(4,4,3,3,2,2,1,1) is ω-Y(1,6)<br/>
(0)(1,1,1) is the limit of [ω-Y sequence](https://googology.miraheze.org/wiki/%5C(%5Comega%5C)-Y_sequence)<br/>

From there, the notation stays unrivaled.

## ~~Currently working on~~ should work on:
- More advanced MMS matrix study
