from __future__ import division, print_function

import os
import sys
import lzma
import base64

# 将可执行文件依赖压缩进字符串，让脚本鲁棒性更强。
d = {}
d['UnRAR.exe'] = (
'{Wp48S^xk9=GL@E0stWa761SMbT8$j;m$?x{#^hjmX2@$7x(N1yXy4+lmRb9?|kO=6e;>K>%jK7xi3L+`HpJ=>`ZtgmZWseIE3y?a2d+#qjLzCUyf&TJx(29Is5siygv+2v1f1(Fxoe)9C=zv_^m{~LV8n-x!y)MsBVedd#rDTpD`FL5u2P^vs8Zm^{9nx@X)3RH^J9Mw<o=V_5A@-Ln^A(@v~fxI>%x8&6>I|$!psWP^m!%vQVkTyyZg2UTuYlRY;B74ra@N3T1_lFcfXhF_UXqBkLUR{jsZtn^Z-wJ!kV;{pK^sn+OMPIHsSpQ_~7p7uwUt-K^%8wD~1EJ!*&F+*!X2$<|E(+IACi9rO+juG0=1Z}4&hbmd{EjGT7Ppqm^r-kgpx@G{}$HjCT&{*1z5$mR7GhV%Eq*Rc?ya5D(UkaB4wLhr9-$MU<xFe;b4kMlsSu(;1+itGHalfe!6wiZ4265ECeehkwB_lO6-4iq|V+sAdA!;&*}'
'dqzuod747`nMDdKUCQJEmd*qgkU3><0cWKrYuw^o_RL0iAnD4xiLA}NsXSwKYz%s%`b3#X^NeTS?Uy5_WMNDf678cMYmgEL9M8+x;|sGr%aKNMQ)>pa()?ZA*lz<d158|7zN6p{4fqe4BI-cx)f28m^|bQ`ppZTB`NMNywQZWs>riA?(-()Ig;!>lok0(=`>UO>X~xoC8QkX;iYNA&{pv>xQl-Ep2J#URhYDuc&JNvdk)ni5x{<7!1xULCH`SeJaP$_aE3k0l?s<_PhFGq%O8GkuX^UyUH?F`_uo>Ic%6$jfp0=g3y6AiY%*1z&sf*;m&afp^W%*{{#Kkcoj8Z8Nz?wlQ7A5`IRB|B}Re_;6JrPR}Pp=bZ{~C0sRcX@q>fomzxyJewu`_z`+9s7lNyS_#ioo*<tfL7)r~M$PO!9AR;y_R*CQ26AI9%ypalW%v_gHW)MJxw{3X7iU<4sL}41<Q&&O>_1bZTTl`YQ>ZowtvGKR<1JJ+MpS'
'hExT9BqB&7Y)F5N!Yf*|F}`uRO<2A^*PI%hNO=&23|XBT{tB2o%QnmH1lztR5zoMxs96wG&0P%{b)ze5+5Pse_flKfTTtSya4u@DgjqpKjd7QZU>93>jP9@zW??s`D8+s*8mT2%VSzE2XcE>OtFuI4i~Cy1#{hFQCW7wBaDP-vW!^%v$QXyN4?FGykbvPqf#UiqP26E*qmVBzJziAZx+`0RXsa(DUn?isvk;6Y3KO;G-Kzr5UcY3xHk7ij@WW0g1%x$uPQEkzo<Oy&g*`yvGNn=gT4WW=W!FbFmxp!zaPH&H7>leiFv3i*<_))USKl+N%UiO?4$XdG8nONAYbH(WzgP{#C^YlLPmav_>)uZZcMD((wyO+Bo!-kfo;4ER{^zc|8rv|6ddng7J~}P7P2U`!(YukPxJzCWmhCqFO-c%i@mqSWH4LU{QBVo+f-QKK`Gg@xg^ntb4CwQ?#*_!0y4xD`W>38MZYyV>Cnl`##hH!QadcmaA2>}&'
'&6F6pwR4|g{VV`?`!+(xUm-SFcd)FXtP0JUdfycNXK{+hy^lu*RdBh&ILic*Rsngjd34H%dVMu~>sclD%5%Z%Vd!=vrLh4)C#>Hb|8>)Y!ajqjb;m>=y^aO3NEvQ9Cr~jf=+~sNv?ImQ1eR1qP~RR1TNLL`y^E?QW6{NRC*LGDp#O~4ZEK$%2RmkOhYfbo`}i4v8SVSC>Zc^X4n5A&2iq(AUo!(JBJsrftd$_FPkj3VQb??I&>E=d4a6~8&4#4s+wc1wrJL(%Ba!CG(yO%^s0kJ%rM!VuGQb+;tQ*sU>9jZOkJ7#{m0ir>;M-a=YFU^eSj)Qh89r=_ER<<2$u5lH<8q+PTby)i7zg^7h*zV+$vLor<A2A6C118PcWwdhWG_XhyavAyoL_eochbw<Q!pxDI}Q;uH2wcQ+>rFiaH8P<q`vZNl)uUVad`O6e<{1FQoDADz{AC_BeQsTs|C9(4Z1JO_eP;^&E{Vn*_5=Tvf9pHh+%!j-G-XG'
'SMOUTa_T7NNGzp+xS|3IGLptd0`NJEQYV;V_JcIS3MO=Ty(cD~+FW^jt%@#gGNsi5f;6}8IAzzEN3iYjE-e!A>tf(-8k!S>ZlN+|mo?rCZ_e%JQx1%pmneec^Zh9)gPFfM?e!natX*c_ChoOxMn3SLzm>S)Az0k$J?L9CdO~a_B6Lf}Jc#YFMX^Us=vrh{);+=lY#B~b9(OCP-E62ZC8%+j1{Q|59%0EK9Jslri}!n0ddvFGM}*1~E)c$_CzMIpWvHdKrYaP!Co6STw;)VE`=HgzZ()Um;bC+$pE6U(LZ8(oed!X0vq1@U(%3>MU)u{C8kR<qaPmA~bBonxDI9aa3Spgy&*DTRZMyJcmla_dgP*dD%?5m3IE%xJP&b(|%<OwQQejLXXCgjzXlccvo2~v$?LS>!tCi=Uw;X^$Hh0W36d{2wWO>+PA>cBY9Xw0hk>DZ&?f78RC-28*s0WHt`#WTBvO9DUYOoKA{mprJ0sGq)bWNlG=jXMK'
'l>SxJ<k1K|unxe!#@(cwzUq=U1`?g_2DBmYynD$bOKB4kLTIOV!&^3!;iG=)Fn$cGgIAMA`UA^7hyh0G3JP@gI<_Grc{=&^y*cfwgaA?a-VJoeI8KP|nlL(vUU*>ZAA`*Lo*_eZG(F_SoZg}|A$Rp{#P~c;3{O66gx4l~l5dWsiY-wx{|3XgC;y{~%l0KIN>#}4)P~U*!P-p!-gE)#t3-;$_6nr3_yVh{ymw$f#3M*sf4BsQ=jsx_rC6zv7*Qvh__SVM|LL)9a!N%;s^uxXjB^U{z+w>4x)*SF@d2%=={OF%f%L0$1r+KEtTPoP|JShmFs7q0_4gDw;27kHT`mI(I^o^F`J;oqCa30TFad8$z_jh4=S`!kAZC?pqH@p=V9>2#`2hXL!*x*2phbi?`DGq9PzkRKdMx{4{knEIF>B=iR6)IYj}J?!U85J*C#}<gL{$om7%64AE06c8<&*<k@mda(SDli<mqg1&ym?7XNQQXBTa?>dI<E;I'
'j1>zpfQhoXBBnzvw{&rR)&mF6IXB~p@+l&DsB<Le1~_hG8d&3((8?>m*vkA^S@Ft~X|lGbwt|QC^6##X6e;4d%$5$KW9?1@(6>&WEVUQfFB_pK>U`TbOdtD$5Mjzf_W0Kfaj_bKK~X2r%pp_Hv>0$4ofIo`8wXZ{)$&E_yh2m6S0jpht1faNe+l9EdSMKc1kd;X7?MXRSvMeJ`y5+sb}vaDWr^HA|0O8YU=>gFxpAZ!)F_Bj@nwYAq!zwWMpw@OeUBnHY(h*AP{*v{BC>v{N{3<?8{{Zk`va92UPRXVPdK2gZ!ufFzTTQD;ysFnWSXSUve!FUdOw#mBYqS2*}A9W=jf7)SB^yZa{nE?9(mRD5KTh{RtCppO=c1X%Ec`q5eXILf$4Yay?^6i%3jk8IoU$rQXZ{ou*Ic3<-uOKk$Wt$NxXh9mRS2qDGM3;>z*tkUVlJ)AKHAry&P`288~C_(6Sn0w{}YIE4p!{pxuYCURBs)-=#$>AXQ<c'
'pqs0CWhv4~)msArHScsTQmi)803-0cxDwcXe&+%3j?iUt1J=DCO=QC;nMFrSf4oPT@X~3p`S@vI(7MNgSg2pWH{lwZ?0NHxwA+D*RRK8>d`E8{H}{oBJHclDB$OSL2dK8w`@Aa@wiNh&Jnk-nzeQX?^b}0)&5Qx?@EEt}WF^#~+G^%k3Em)Ose3{@JkAJKw7ykGLvMkhq*;#{S6tu}5xJ$A&(zwO^wT2csrqfmWw@rUmwLTIK?ZPd=m+tQUIsl&h93v{pFVO)k#WT%o{o0wuEpK(XY8i-euE5B`3hx<kwlr7K=Mn$<>N4v!R<1=rg-R_`U`o6OFwGN#lK$tA1hUWnN&rO#^Zn}0N6=b-!&=<^DbH|NCi8+A=-r~N?af5#h{emBEX9j`A}7r5WV58!H-mqegX}31F*r>G2tACh~quknXAIc*KqdgKFxRUjWV-5j<oGugh=b#kuAW;g-(Gh+5==yhlEQ*_(1ShN>s9=*oL8a_}!hL4gb{p'
'd&JKL$A-3O`TR6v1U4t0OB{WzEwyz|B@46~#AvZvx{7|Sp^5j`a;}nzQyRqEN4Q@qL~pl9&$rMI=&WWA;Ulpx=R*L{vZ_;|xY&~XV7i8gQQX)c?&*EtlD$wk>=!Odb^dBN+wM#rp%0x#+%j)=>5OX>7O78vpS~|KZAvG&BS6>yTxZ1i=Zk#?gKY0V`t(pdPMz$5<wB7M`kWwCm=I!O_ENo>dqDbrf<%H8e@$<te_`pz6JrD@Cl*w(jqSBqgs(VL^bA`NgkD7fMVP$|@n`j3C;NvPqQR!gA`VmH5qw?g3e{*L9<iMlv<tZCmirE6y;;jfs&iq`yK#|uiw!P5ub2$I`RWv_Mj<bc;kD)Ie}7Y@Ph)v6uD#jMp-^g&)o76KuaazQuda6Qu34kT_69+X*Be?w@W5k6b*{4;K(9J`CCIW)>NOF=M%-lfvj{Pb*RNx$9P&|*3>C(sx~5bS!JUDmTZ@g@d^R?B1%r|7+oK<vB^t3kQWb<Dw%rQe'
'aVY_CY{uys9QYpANcc}m8xX?t3-zsQP&|dUZr-fF71*!DqN<Rwa8k84?p|Fedit;Fi}BpY{N0?jWVk{y3SsjA?=94nsis<GfP~K=e|qO<zJ7z*T+V3AS`Q~{;dKsnBXY|xAOyfn03<`F<~y{wwx}guSH)gv2P_*cbG~(OKwWJq2N>c_35mN@{7#QXrm?(;IWQoLQ4M1dEgvxzYt%YS4IMj6u7lssr)c5&8cV!bai=Xz2k@vnQr?Fsk=)g|a^=0OoZ7`VEqy{>GcBxY6@O8#3~>Qr6$ygQp!WI3o-vKZVF6Tt9E2DOA+0?C^SYM_Eml;19AKJzJte2rxY*z0)H3HcW*bp+u&N+E`48bA;OOIbWE-m>;g}~jzah1;Isk=GK7mKCBeLA>|J~Gkxk4AifztFLBjPyL2%<YxFq&5d#Vq1W(WC&!6F9FzV~!S}@+5Sv$W=X+fJ)9k=zBB>YLDs_0>n}>q*OLObTN(qKUnbn8uTvYkGirjj50#e'
'bx++I%;746REVV7xgu(UbG9z9?vfJVUwy5k+y*#Es&r)scwt!F-eX>qDGMO3HL?<EZmue%?5fud5i$W8lRNz6mM_N12i*TC1zlf#Fo?d^yK}aUm5jv^9DgpuY?dr&h?RSlj({)U>`a6tmU*>xj=A)HYiInXhJ-X@H}-0s!Lp5Er$hfr`~e4_72yT{UttZ*zWzC?!NY&)b-M}9-NKeU_m1vpNNy8?9<U8L5<&{a#t8TSiUhzz@P4v|O-*9a@08l(S^w^(0Em{KWTjA<E#4<WLmHaJ-5TL6klxz;pCEc8rdP303${_O-qUpb+b?{c+FRUhY;P`_+U{?b4A)2!y$u;_&@$+snpa#I%b!kxnig?h>PU#A!L*Y^F7i3pnQ6}RnUEw6t?V6z-bg?3=ey;Qq4{@Jpj3F320^Po|9~A>ne^NzZG&zX(zhioL<Egn!k4c*4s1l|OeKTbv2bNAX|*iW4@qtu>t?||HL1g0Mkt=*lirLYU!5F51t6|U'
'bSI788-pz~$udRj2=Hmvcvp-@b!Z+(@cSRyqLUXmjsO@p35AwA$XN&bP!^Gxa{=-E2&49^AJr0+ufJejD8T)~dec+Q6kPaO`vxmnPrkO$zTw>Jr);HaD5nPM<SL?`hi5TLCYHCV^DC8H$W`gLbJW751^mt&r-Gpf;sp&T(#bIMoKaewaOvYzul)2O<|*A)6o@pi+Y_Q6w9qnnIa)Sf5$6m;aa7=0D~bWl@6R4^dm>Xzp>&w}ceA8Zzw61xc{ofBSV<!KmMygI)S0(w_#9&&=%R<9>EvT!h1-<qI{^pjyL^WW&P2+~mRYwQKE9={IGF3kFDcxpjD5q3*EI-1?>D>))Idm)$)l@>f(tSkQb_~x3&9nzNGQL>_y<s|_-lSJ)ZU&n7|MAo$NGsScNa#Z-VAJkN+lTb#%Aro5JGlGmM_9%)XH!IrNSZJ<iZM>y|By}lNP}6I=(Q)ne$%A&Z}G3qFeU5z}IbhnT~r44gH4)WOf{uc{J)vTbh7;'
'Z`MY@kbeast<S(-03kL|&h0jt$|fb5yB5J~76Dup&JNwvCP)r_NMAACKG=8Dq%S!BfPKwQ@-$|T$<JkyhpQlx9x!>pPKsyA{fue6?88vl+wG~3(P<ucsP@(Mi%7&k>*CFphO`b0qNorHdMCuGW%q_Z!4{%_V5XbYs8#JI2*#Gr#HL<2Ev*6TAT*e?o&8}9bQSxeyyKuu%NujN82TN{rW?(KW=rnY^RX7{-jQ&rIxR;3wBL)OsHfIX%P%O%1aik8pQneq5$bcevVhZ}Nj27|Ol*NVJk`QOPEjIDAJiYmKW=o^67kN*pIgOKCmB+vm56OiIFs{287j}9ZuD3V1wUOTTrU8^zITrBP6pGwEkZ(TBSMs-kTxXvdw;+Tw8btyjc#ROxG2&&4TQuaJ&27ELxe=2OMHbpqCWALTZ8DZ*nX8J(`o@{>hMynw>b9wZuO!*xp6nkg^*obRvPvkbD%F3y0jH-57b`7`k2s<CG!73-8!`SE%4SUkgu(!'
'RQ$RNS76DGi#pmS{S!eFl7T+EFi0DGMU%u#R7w7t#uN;EDt7A)Eg&mG?|e*imc&3FevkFvmQaSmy@hM~KvGDJF}Sp1@H-1!f$@C;eH6($F+nRB^UlS{Wajy~9QbyZKY@|t$Hi;kpaMij05x7|E5UN5ocE!V-nIVuX(TE%<1;oozRuD)^>yhOg?i&q``N!0D*Z0A-!!`$8N9*H?{(%*6X3qB`S1k_3bEeSGg;x!oCLzTF<@(UUYaL^`v&DWQ*nx8&Pm4+YFe^3>7Xkhboat?5S4%D(Mlk2RaBXhPGX~$v%sh7vo$EV*55Wo&?atLX;MGI)#*DRK}a(S22tAVB!AhM8#ms?ZJEY8OGQh+fhBfJbH5C0A?NI3ovf73^IbJa-oW?I%nqu1cz~4VYEiq2o4YNHhmicVVxf&s*QGW|VNWx70_Z)CmIF@FepbD6&jFx}_Or-EZQ_$}`mwV>`;S!}@Se0G0N9qfuUZpipz-&_m+6U8HLm6-=N6`9'
'm{p;Nu49?51d`b&(xtMS)=@XY_lOC>3l2whCP8-~1}ol+-|q=+j2s*gNx9+w65M+Oz(YM`m|KbvVJ6Y~LpfgS##_GHREedtvBxfJw)(ISkj_weEg6(tGW-tv8mXlA`iq94ATn1OLl{we4Pt}kqJ{v$)f#rV0v`sqyOU;<gWu5>kuL)7*r2obnD{I|Ry}gkUseb8Pkm%q-zWvRg*xgJGYpL~&Be`IYE5azxghXcj1q@vP+=p|gkn~P4!y?3JnkkhD%YVA+(2x?8DEXmWc7o(-?v@cluy%dM1qe@kroVBmX^p7oJ`Dj*g3AU74m_|%A+OWmVPiYX&a7~n%Y+QJj5Y&7|klU3rtT$Y5=bm!&7YX%;!U|`L5%+shoHg_J0aWu^}tYZoN*`P7(PI5Ma>J7B@%iT2}8L=t_9wo>8G}x6`0$%o6LVjXT3=xc8~|tLel5K|B!5)DY<DP;Bl}Ut%s&+uTVTW=wFj+Nae|=E@Cb_SV61ZTc|13Ghmp'
'cSZ8X9C|Q;@FNS@i#svq@AGb(%hyOpgDc1BY_@igluLp16kCKp56jGe(1ZUI?5a|~7!5y%9Xjy=H}`W8U1&ieJl?9f@U=+^Buq_iM+S8AJow{6!F4NrE>C~U&eFboNZz|l$Wm?w{!Cc)Yfr96!SZEQV?VfLM%WvV%utzBzCGWmHgm=|>u<RB@MGoS<VF+&fH+3X#A#+q43DCC5gaZykRhAIC=QqnZ1CWYBX`qAq)bc4jPdWx1I)g(H<8ydB0ll5wKn6AtQ}TBV1ASV?hWj9VW!~wSm<LzN1?PBF)@Fl>#2E_vH(I5Zr3szl-v3E66uHdN8;>fvrw?iR^25zVx{HPa!E9VLw;Oqf!Qj^=F$JYV5j`W7-*AX7g?a1Kx<`hlkCL}HDlylLhb)LTwKBAt6#@axPI_bI7EomM|cjCBVLx#boRiQ3pxS|;!Rs2^^Rps5qWV^j^%xRIALan4c<`^217^Fgqdy0^tXlxQ8S0+z}0s@=u!NwkHgVl'
'Ng0(^>nugRo;ni0K4-L551^yJiSVgP<iNT+FxC=nA=6l*M5Ywl%~JF?p=12x;vtv+T{EQ*Kje&w#s?E5nlks*6iP)FnSwSp@ZB3|q8dJui|N4O)y=SxE>Ln2NZY?eb&1ZN>(**0W1QOI++tXowl5_6%^F#^EsbogJ>kZDcli%)ZR8lWwnod7d6QTIy^npnN9tO;`oo>72qzg(l|=ZFgICbMlH#cs>whO%x=?Vca9x%4x{C1zQK^&iZ48kvdxHrvPNrH(lD1&q$JsZ&=yo>rN|^gBR?mM7l!w8B*go4si0vqK@>VdWFBN3xG!`r<VCYKzXc4i85Q+CnoaL7!=V>h3#xU^rP!maQel1A4;N)l+t+wJ&%j?+leCfkJ3_O`gKD0%5w2LIiNCy=o=?f$T2N?0NXCfYjM;7>64a#QdKUv7-;nvKjL<ru{Y+K9qa3?Z<-DtY~r;Igy8Z~R3R<Mu9S|i>jbb)k|BcZDdcvjzGzXLL)$k?vDds5yO'
'&KprWjKO-BBCTzkO(9J34Qk|E%3<}18K#V_Ze{q;PF>Ky>Un`s;@t?A{_`n_`eW^UW<ND$mPLVaOJ7vNCH<2U>qQsQkt5?lb+dxCUG<>`E`?o!ou0uqk1E(k{bBd9!cU=ZgT*QIo5o<T{@*p^)b>*o^nT8@Ze0+S#u~Y7N8)GmbIU$RL@UKp{aQ*<HGySJ{S0(0?hoCIf>JLB?yVbjOZ=oXX`1Y*w+}`(Nl|LbCnm8ss4(|Y!@ehOcN@j47P)jC?86#DkEwWUVTefWVKXb}=<XY3KvzL9=C-4_p_)2g^>Yw9hs~Aban{l!*snj#jo#@BMZ8UVEV<3QMWhEpcF<=QfEoyk1aIrvaK@oi=5)V}Pi1VxsEd+;-~XNip-pp=wwlT^JEB#2P<{9KON4M71qfid6i$6p8GO~HG%nWHMvWU^()*-Kk-^*!WuUml?M39BdJMczZS|0`u7w{+t7WtmUVeB9qtn+x=0xeR?<R6pOg<|o$nQ(<M1s-Z'
'%9()sVDgi(;O+_I9Ji1?&49^jKEk6}XQbyJ|A;v_u?)YU;v)Xpj{>D&6#p-VmeFQ{v1;-)gJj|_R@Iay2dbV?sYC97=7SH+p1NQ3gC_&?>_7TZT~zd9d(y9Dpeg+jv?)EJz9p;?dW~*QPY8MDRTxi5m@|VI=Kw5{SDE+R2Lgg^C-C7s?_o;3wob1zRRaaey)9J5JQ3VdoHe|xSDAmD7gC~SRg{v7L4V+>ZCnybP=bO{Nn#0_?3oCsmgWmZx1Up=YPw^DK3@a7O%X(i8YRGLtW76%M7$h22-IS)Y%nec{I4fSdn?97L#)f5Ir{A?2wdtjAK^@&^&9A_fMY;8U=?(0W=1P#cW^H7i5R2)YuARh!RQpqeK)78=_4iu=I`&?<mt6V6jT|>`!K$?YA4~%K%hTR8u7vzjOgxtoXZz=A0b-GAvre`;tB^oRh|ZY_U4qKF~^|pw)4V)s{<Yt2bH`k<P&WJKCu_CEY_F)69c_9YaW)&=O8RLqWahk'
'0G~I>FSP~dA{=_9wU|x)o@5PY3pgwopBV3A>y2@dH8c8hx6yH_<mP=Io&U>&Z>P6sn`rX7l>dfd);<Y~lkni7aq>tD`2i4C?Z3Ey?5z<;xiJVIGR-*;wm|0;um8CE2h&CiC_O<LXR72_AHDCw7f9>^QG{iktaYNH52qbY2B)2z9NrM!Q0hKk3O%)+IE;QpV)k2!k-FF}H$<}NITvY>=%2@`z+O3@e=M6$umd)>Lf-br%3p$!JH+3H0<&a+0^fgu<N<NTPdN<{nLM{u%M~G?Jtg01$Viv7&C~?fb`rM?f$HP&sc4?9k&Nx#@P8WRJDnhzP;80!CR<n^(%sq;5DrGW<y44f;}l#8MLT-#VjYGT{F{_Sdmht*5aKkT6wSDy8-y2a2N=Cs>TarkC1D-I9P)h*XaxV`8Bi8c-xxmO5M%{G<_;Tu+g5gNTS!TM&-O2*Jj*>B&~}9EV(Tu*Re?iYXgA*Dmwg35#~S_^QpKPsJQ99k&5gMz>+%k{'
'{ppB37Fw#i@r76zKoPILuEmg8HYbe-xOpV;6;63J9^kjPX>LW=@}SVzF1PZ^xOXcJ%!{AU=1@mtm1f$4tpK1d!@1!@K@YKTMY{r1A+?vM_m7Md_mU28AiRL{Zjfk-m=BnNiEHt!whS>LkKqMhdn2uHtV&@&ZccF?T00?a3gwvO(KQ}}16rSu8SOM7qq($fhFPJeK<Fu)p4-!i_lDEZ&*3+@O3~cX-zjzB;3V&d7L7{`#O$Tj2!8d-M??efM@6G=oTP%|xfwWeMGPQci&2R}KFE{{?a{-!E5bVQ#P=LJ4V1I9P~su@w)?eH+G6b&p96$N{(2PfZVtTkANQ<4;A*8?j(Wwag8kD|PbX8yZI|0cC_eCHU8$?G+~L(Hu7X&lDOZcX>Et8R$nvkroJAbHIc?4QEs)Pya+6KZi||%&EVCiJQ2`ZOA4UfP0+##?%5d^lV}+k(sM1fZ7NZ4?#F*cUH~cinWT>Q12zsZuJ`9i>hk5z#k!ALjuEZ2w'
'Yjm8LprTOJp?HM;-PRx84-E^%EC8_8kSrnSdz|(yzE*%Wx=$nMj!Blxv>QVt5~<2%_++3)Dw<M=wbzg5fZf>8ovCSIh);N#wV7@Rn}=H;Rbu*BS_>vDaPLt2WOf+x=W{hkrC&JOc1!`A@i_?_7sO9|r$Z>vu6C_1h*NRiB(cOnXgjjpURJp#Z;_M*5KJqMhTd6#mV_HArDGj6gCB=NKF`*(i2X-*>*aAA*ORePkRo^2x=vWU2xG!FZYS1FkJ5r{dK;l7JC8fd1r7I!HcTZEm+y)?HxKY8z;yF}W*i$d#i6}nZrz5{@Hew%Abu=ktA;IF55G@@$h}%4@OEc8-}^tACns6ZTkyb9x`@}OM9iaqoYm%27A92gmULB>n;uLHa+iJH5$%5_N-UjO?=Ac!^E6i>Zx@6Mv-!3HTK-df#*57fsx{8$mH~g2aXET&$7I`&*5Al0Knpi>G^5b)_13RiE(HsUR67!MBRT$HO2s%C{OQ3f>F^HJ?Vfv4'
'3w%SHT?rl_?Nw!eW&yu+V>m^QS^vw}v+mxAiQT$Kk%x`}`<IT?n3-gnF3AZHQ_iat?o@F6eaX@xVI#j$vr$Z%&lF05UZ0<~+@Nf%GCRWJr{{!n6hGOvqE}E$FCif^`sAE@*uGF^r42JG@jucshcBQP!ZNo&G-s=I+<!WdG|0l=gC4rBxf2TpHNlg4803NK@(6Hx_eMP;zFzs-@7A?b&Pv=T6No~)n;-j+fv9aSV=l?hmyOB)vkd7*lkflPX$hZwgcTa74i20<NPko(+nY;YK(u1af<Z8DXC&+sC1hwmTG9t(eHEmpP;ZRB6==e~Gt33TpiOrLfq_GAV4=&xhQ2Fxtw&G+2*b1GZaS?k!Pu*f{p9p;HmLkLCj~uaIXJv?%MYI3f~h#Q9erH1$(f8J?@yqqavDYDRHK&DCnCwYqsl6|7VDqX=oyji&7Ka+ELuz<Zz(%78xzR^S65X_d$)46+cye`bNQN&9_BtAAbvY*heA4sxwDLiRG+~m'
'26^yC(UL<1<V_%*a<b8Ysso!At_S_aiD?$_?0c+5ZrFk~qkc8|t)FKM2kI(fx@W364;z^Y>(fxdBce(LSx=31IfB4pAbNS6{3h4f8yTA#hKEozN*@4Vr{hz3;`A94Dz&ji0M+>u@F@b0(Lw2IO7Q{AaBwRfZZADmY)hWeb#^hKQ&KzJj=7{Ba>s3#`ekWsY;YKgtMBl%6%JC%(GIZsM=>8y4nuBeOx|NCmcg`i$ziRMEXFCkY@FV@cvPTRyJl?3OQ(O@hzo{cP2#pY?dar?88k}DmL2OIEBfL6+yF+bDNk{AoRzBMz?b#@2=qbW)xi)$oHrx4i)0d=VPGtm-LA7xw>h(5a~1lp+Q$A@-sM<Qc>Qu(#9<2oq6}R<V!QT%g-f9%|1ipcf}2XdNl02V6*hPmM6Go_mrgTRk|5YKqA<kGx`Z@CcS)OX-0VJ%x1G4f#n^M$YUG|d@tpy@2pbUPue&X+^I-X{^THrDI<XfcT#Rh@JyJ(Bx4hP('
'rV4mEDtN_wyPuScjDgG_Wi%^%sSC7b)W-voreU@;6KpuHB4o<(aJRc!w%n@7#jH`Wioa&je3<|pN$=rFO9NdHT5RHN@^6(jidDj$lJ^FEcp+i&O<aK{ENR232NGH0Y(VmveDH2se+Q1ohHt@1JeL<-&X;cWgr<_`%bG1>0R}cdvWWK)H`xzj^Fzn4AK)E+uBPTR7|3uu9cLJ5gf>5AF(`m?<1v$T0AJsbZS7~%l0%_YvcnbW8$S(6ZB4Gy^nR_)Ae|iU4qQ=cSSD@|Pxl#POFG)w9(zUlrz-o{=MM#_S)+ctNhu1j_Hh3QXHnBnbml>U;tjB;pC{YrzH?V)m>6TQSKai%(v^rbUgC3~0gn*UM)(2doG%Vu5G-dJ)s)PUv)5TkOjA?Jc5M3m8P3>sZfo3{5<k`ivll#`tn-8c1LqGT^c8?=Sd&L&fQPUD(=8c_ZOU$TZ325r$uDsh30viLu-7bTIMiG&@-7Xr->esQ1{*XIw0X+N+vcPj'
'kYWQ;FbVT79};<DzqkJ^kRatZw3j3Y*<<OQF$F~Jx;xOH5*@zq$QX(@zP(jX$d*J^D9^yo|MX~TggI(RmbOBDj@&$X8rxvI0oHn-Q8;?HSn8@f*jGpG|9cfLbkXVik{oKD?mR$nFjV7=2_NYk1<GYHM%ZAK*HNZugM0|Qm={`J-xFk}doQ*auMGLBvp#o!I%b-w^R-eHxV3Ov-j_v|?+qG81SQMRm-N+(zFFNU{0~B=@PB{2FpduV-<~(xGSv8vC0(lGNtY{ttV8~Kj4?PF6$gSm$F9R=XBk0#aF~?ccjBQ5KD|hVGB_2=yNuXqpMc?My|U`aSFlk8!#`RWCmu<zw2$)dk1jQB5mLCcO`!;LAc2UikU?wWv~FCcst#>JDN}O55DTaTKulcf7fNocxNcX~<w}$xCrK&QRX-@43-ZG7>k7p~Bb>P72}-)f`mr{uHXmyX)HE<}*#e<9E%<OX_+%3{unuIcKg^hpg*+io%_M(wu*_Ly40|N{'
'(yBQ^bht*1nkI9H8`xEBz>|W>Og~B@5EhItk<4G<r&e`NgO$4%+knbCwC%ZfyEr1=2479JJ9J&DFSe+Z$kC1c8}ly|O<wfa(zVlU%_0}5q`WSj`Tl5f@xOg;8H|?SWeB<k>r<jJc;CmanT;+B0;b2C@Z>-UOAUo}<YVRbJB`S+t7rHv!6ja4AOU(F@B?I4Zo7z^|3XEG!MT=)GJ#jxzIhZN(aW<DPs&^na<B+W5dgHQ@N;HOQaDJZTydo>5uNNhFq7fN*JmlDE^b^?+KgZoi)QCYFJMa#)AMIX{Y0(P;73d5W8L%gA@KZ+Hx6M(;VNYDwAb~+P|c{zQLQ_?&(^<7>vzo({M{6rf4>nx;D=yS&QK3Od&i!?B1J!e%j-eZZO=sr=zT?)q??j+b-yWvRORgx;~T=CPr(V$$tw({Yos+oJjl}9Z);yj<Z?~-!vkOjYvj^bqtV{mW-&+bsbz<(pa~-5kL)u^hiu>Yo?$dN;?eu7T`O4UR0g1z'
'_T|?nB8qAseSZKJ;D<73Cokn|s1g7?BJ$l|NQ8$&mz%|J7mg^WPn-3dyIF{>qKzd;(XwQ+u$B}L>Nne)oDZHeI$OpvA4$^jf#InDRuheAk{uzDs}jUrrA*RRYOTW96@vWsvdy}z6Cs)f$Nn}Si>_HmEby3Ga7X$;3dc4=)E_Kn4h?XVx6M2)Pboi$4cfAE_qjX07uNYpS%RdATmZi!CGQIBsMrgZ0iK;h#v9Cy&X<wi_j!-pNvutnoAzq~x`#>NZQMb@<M5Eq<yw|hl4&APxFh~v1CUVTm}g(wucqZ+zg!7P@Do6a@3w>Ut-opB8D%Hq%s7W6NV8dh?~UTL<GwaJo<IIbA@a^Bp^Ka!$mY)Srv(Q!*~6ERC(l(-_9{k-$*<4`jE-b{FY1zzgxlxCoK$7>JJSCQJ24acC&NT53AuV)@0m>kv)QLE*ok|4nl2R57D<=LW;zE$+*VW3$6e-^;6wLgAS#nQ!&(h~9*zw0;UxOu>x-kxrZ`A`'
'Zhc%ZibFRgokp13T}d%&HU^pnv8Do2aXCvMAXzG*aP3c}FnNYQM<N5Qa|UTO-TL`W37u(k?bUin$Zt9W1U`9ly6Kk!)JR3zSQnqHDX$jp%hc4TVj3Gf=RSIKO=?>W{ASn+3Cy@g3RaCv%(_N%Qc)S<m^c<Gc6LH~naNfL#~`;PO<kb~UGLZr5UQBKcus;{3yEEoebMYCyj{<jUb4;h#LYqIt$@}p>3A~#K<uj|iNxMD__Ky03tkMdJEm(MG|Ke*!81`E4d1zyek>%fYBm)EUG(H&YVfm4so&_G`hP80t2X|glr(m_p)sdb$i&G_fCK=H89qB`Ht94#&5On80vdO+o{7iG*s+qw=m9lWO$Lb%{=3SwdpOi8F}{|R)(h}dc>SUGS-jk*^)9O>4`iI!;!0z9RU|*q=w9~P1Zl^$jGBnQnH}fA5|u%4h49Qn#Y+bnK}{M3JrL~;z)KFleK>46ka=OoCLLf4+TJH#?WP<~q{VgqSs_6^+}1%i'
'65Lv|ljzi)3T<UA%uJ|*zuqTC;C%M}X`ZvXZrf{>Cd*HC<Gm<XgkAXp-W-POPe${|10Ob`%sac@ljdEiqiMH-vmr}&_(2V4vIH+pwgfH4-U5Gped5MRhTveI=@@^SU&~;TXRNhQsOs<;oVz{|F}E`uFhOs82nFFxftO-YZJco5wi}`!3R-bHei-mYCblJAg2@2&gZHMCQ)P+$GYofuMDd|@Ta%qy#IC37<ZsW&Op@@HDFaOG=(H{{9ABSK7d$f7MQGW#1^P4?uFR*bmWR|u0?AcC#JnbU`^Py~PBhwpBq7MQ7-GiPW+`;Kxuwc-a4rR6S2j1e#=NRL*}{vq`-eR3!_Ib|c=e60?o+79QUGcrb>NPgXG}A&lizjlM&vz#!o~m`J})Ev+zOt`Z&7Iy&MB~?J_EHeLFQ)t&i*NJ;kz>rLd2J(mrk=vIe9Nm*dRN1d;o3~cDfdMGP0p-RM8KR>yHt$)cfT9r00Q^C`Ymv<vv?%SyT;NS3VHJ'
'pM_w<B%6sPqr!^a7RFURT;igU?#rYBFk|bIoqL)hac`PQ$E)7ye3t-~4K$Csms@w3?YxF)@4DLiTixRHG;{LK-NDX~F=gFQ15r-mQrY<QGXf?pD}PUOklK5gZ;xQDG^*e^fMTF5kjjeZ15&NXD0C$7<3@Jclb-(<JsJJZdvS>n3w9$k?H_sfG|di*_ESKaD5y@(eBrYl7N8wrKOxiI7sZA!k_}{LJq$;4ijRhZg;|RUb8=mpy?gi5cqyJS?RH7`m+5aOFPpUOBC(qVzrIZ@+NS4dqv4s_Y2&aQp2lCKoPOdK!N`nD33oV`^kCWO3Q$eTS+os~(_)&p8%u%OwEl^A<eI&6Yv8@@lZp*`v!>;id7Z&?abO}kRBA~1^bS6KQ879Z;8?&D;KTpYvk4m<$|BXsQFq|C`2d-E>$NM2UPKfsDaXLXBM~XS!4E~Oo?$i@l~k)liIS*tb97xzf4560?vesa@x3DzqZ2v0o%|@m)~`>XVj7D@5sA?G'
'37e)60y}11n19Ja+{Jk3YZqJ|lD2owPGqW5${W4_+#4bTXQwxLpzeE-Qmsv@*YxETbF&O@sI=N^!ZlW-zrf<odr%DCI>*7c{^CB>gaM4|ov7-lE!5NcXeM43iPHXa-u2QLo<?P}J~~LmX(Y`!2nm-s=#eTsGK_Jx=UflFCye5s!eEAQ{^X?q=w8U@q*9$Tgpms^t=16**@xqO&It35IqJ76lFTU>mj~}!{HL({OOTW6h&q9Y0C^{|QiF;?sJ2v&OH!BEg?EQzl9_=X4PNn{#<V0-NOoEHhAi~YRT{qr<Ttg#CI9Ythn+Q`U7>T4W;ah4!xf?h>uf*@^DVB)P~Rt|wbo@)`<ERs3V$%_8M;v_{*W4ta1j3PshrDRlZ7;=+dr9Y`myjQ$4_8QzL64d0r&U{l$5(nL6|^HkTub$qA}5)x|Dy0$KBus<2~!FUi8EzIk*1!q+lV$;O5zcdEaqUJAk$-aTEQs-&iiUG5yq924sUfi6rSG2XwqJ'
'{>`*OmoL1R(E|B!`5X4k7xV0gQ0zsx_l^pge=2yjmmG><cX(SI@fk{sv^m`sT4<q6_^&uBp)U%;RC^!bsz;U$1=lBz)2~yex(ll82_a9!u|ld<dfF6D_|W)?JnA$JCbaC(_ZNCw1mQ<bj%|};=lfoU3y+oDdT9}`(PPlhN4-B=yn>IwijU;v4gW>i#(8o$ySF8roM<Y7s`D3R5t(`kyv~6CRU{^D5kr=g<Jg7qnx|^)#Apor8haqGJuR1`x}*48j4AQJ74~nE6gyYy-|n0Ur!sp#_CQqrJNLhb4V8X`-bFZrtMD@R>L6FhI|x!M{3XsDB;U%Cx2nF!omb2{AzUUTX@Za?)kMA~j3NZ=ad~d#KL)l+EfVW7&P*2)s;dp>Fm5d%pdWPZ7T>A{n|>Amjb%?<>tV~~#-*?C!sG<y^l1AhG>xrPS3?gTqFIt!r)kP+B5p31?|O?`En7vS3hv?bIs;e-je(A*pv$M;i?}wm|M=33cMA!bBN$&}'
'{@8k)(WQPxd%=I<%ay3BVo^fzQgxWE32c;9c=TWnMhXTiaNucB<Ea713!RnU-I#{F3&!If9LK94CL)=s4C7yOSRjdDJLn;LWpvo(YG2RouYYb!uc+APpqvzN*AM#{Pe<kEl$bZ1a&!bK+e#H!kJ`7+Z~<)^RMdP2q;BQ%z;<2&-^JlHY`bXn){VU9Jz49RS_*SgL@7pF|Hu|#a&Sm#g-t(5TLi1GeS<)Sm(zkf=J61>utS#g4>aym6m`{6tB<rLXx?FRf0dRV<26H3OX1=-=^-NL6YyylHWi(#513K;26+%cUtsR6lZ`W`8HSToQAu%}5@Ey2hZeJoQ9B-BPW6d*iFb#<hh>6_odGz=_XQYeJYs#VLwqr6^Qehbq*#hW3I_0IyUr<3qj2ixGOP};2PsJSrh9@Dn*Q^$lB&j%F2L&t|JBV8nND){M<ZyKIs(psyhPuohkQN8h9c{Cv|0M!_uM?JO+AaBQfLSOh=b3#HJ-Z@KZm(QzC1dc'
'V&n^&`(@N^lnEz(sx{v!VaHB>$sFFY&Jm$UMsDJh<k{T4g^(3%2v#6tCQ|-Sb4{Af1I>$;mFZmdm$QVozd89<M2(ZwZmHB*4`Nw<o8DK13Uz_l{J3q3Y15!NyQPAk_;}?M2|axD%&ovVu`Ak!Z&qIDv`*VQficBsBG&4?AsJ67?~+wmD+c;-gxMz6+>ba9t)nsNXMM+6ABK<jFep-QejqbvWerB>%vx(|O&$;Ay@i)Vqf&=mg!l>w%+i%om$wFDw#x&RbQFj?YGdC%2Utg3ZN!X3C~4t&4sX!<f_7*5ONwF{>H7EBZJ~Y&N2FCPVByFxkRjmzJd&l+ZEf+52?x#0J(H^5<loP{;0bwt_0%`BMST`ogvUZL@}@V=ExfMN*=H<m8geV5iE$Gb38cC>(nphZ&x2T@45ZCSBJV*#&kP4ZU70e$1=IOyyPXIe_x_Wtdb-ty9l|Tm6UwS<19g8p&?d&Mm=-c!Jt+MTP6sM$rbgKaSB5~EvVV4q'
'9g#i{hHzQHU?8sO{Y?Qs(e$p9rmb9nQ<2<76|JW&R^8GwMeJM79KP)tBN$-}QRLoH%HJj!aMaG-WGdpk7|2H;aH~0XH&se}PaTM!5t6BvB=D!^sau28f;M896;4G#vBL2-7S21$l1>er+si+d)eC?C)=J0(zC0>%{1ykuqQI`D$h2EvM;$D1-Y~RCIZM{;f);pEpLUTCa$;9Y&+KOCUs75^0P-}Lb>QQL*c(8S>AS4ZY#R*NX}%*#TpZ0YrE}x`A+=CQz`PvFiP%S^$+Rr7$)_;?7F(UnF+I;UpvgR4e&M<Pz*8U$L;SP->HXbF*SjIO%7!;|@2g={sDf!q?m(xGhPQ^@gCBd3xw@AXOy19P3W3}O>)Rggx(q4`<({FW>LkUXfI`ZC!5O&3qX3;|rdN;+jTZ?@MSa;9p>+6OWS`${YzU~+g+PReeqU*?-c?6KgX=jxZ?e8pTsga8td(GQlFMY3QS8S$+v@*_esUAb%66~-H8dWqUWhMp'
'9E>(igNfrmY0VS-_UD;KMb?&MGuayVWcpVA6?vji4$%u;A=k?Q#*oA9{}L)rSIQ7Zbu#KX`pbd0H54%w^O$=Y7Dp0|&(0T2oU{Sow!?3=mBT|*dT22+e^hJ|UD_CC#@<0dS?H5>B5p};@39kRzO6Jn9JtbQfCHb%O6>!A5LX=)n(0@GHddl(Vc-GOpO{=Sj}qi8)tn*}0mhggSs|(Kd{yB^T1+qGOS3iaL&`Wl0s*Rd;@BsBfC5ksy6#z3hBDX_xeRdNYRZ^afK<2U;AYUp2*vkOOy6&Kyy`v|9;PolI|iVctP(W4Cv|r6ZysOM376U6JcA3y6q8xY#q&oe-KkT<rhSvH7Bn0D_zS6qoFokcM<e4|SF4dcfONe|GeOYjAJy&^^!5pne=1Qu=UH#V0Iv3$BX}5-29lxfU84_ZAMj0I>6ql1te4xOAPhSsD<{KGQPbwUN25k5;O<4h#i*;JJEHR=usb#-XWY09LwKMm(=o|M4HF-+%?HKF'
'v6%sTZ)HW0Z(BVmf70n;4I$qaggM6Z_~IoNO@e<Ik$oXX{3Vy%nSycX4r;aRb0J!3NrGYb4Qa|7Zf8*|7~X3DW5$|v^skB)^k&-79XrK6G5$D!=e5N)CN)6EvNfty6Gy0zRAzdu?F`@^;8&ZCGrCDmJ+XZ2b{WNF(Po*sT$Y79g`5vae&mr3!3OD8c*;QyNAok@SosJ<zpfp>-!s7loP0s>vodVI2zm$-pl9L=kLv5%D0TMBEPUqoa4MtKAjM~q<+14iQZnFG+5=si<6!<^s;$^y=IEV}!GP`J7xK;Yh_#SX-Z#YELQCNa-L&tNP06!w+801puV`P4UaH`WN;c3$8pW+WU!1}o5GCE)kKsN&=9;YR`C=n3F~bPY@*BT#x07jFB-w(;2-05^S(G(dCAnYuy&mEdT`n#cdvCf8v`xiibkWdcd^!bJg`;>urFdvLc&;sqUjbH6|DQ9Ai!@TOoYdR&7x)65TsjU*&T`)GBy?2#vg0v7z?_$l'
'^JM$#<t9N*yS9#By`O|zz;6AP&X5VEE^%*|=lkhn=+@4;=z8Eg*;<$7Uy(Cd_!;iP5Q%=ENTP+#wGHO+Mo!}}rH!(DlA5ny<}{*eaXa*0*~HaZ@C>jpvOKlbXd&IoV*=D{B-8KmD4zBM7I!eb%t%Z>GPu~MO4=`=Js*uS_WtY11E+95YQw8WinD^G=4^v<;vh7(gso7StBUdC&hx&jETM@9lp#=zo~Z0<TOKvH1QNc|LLAso3sXaM5!v(4GB_+-2IXz`ke-khP$gC+2F>}fWg3rS$g|(B8jZg=@$CmqxUKVO_1<Uc%RhN$pj@I~1=QwUyC7sq?~4Sk%q*BCAYGSO+11-v6T6<BsPo8m*x2<GzRErW<+=(w2;O*w7inJBrx;URyDro#RW;)7Z-p5>7?%q7E$-Y}`dn<n`+5q;l-2T?2#?5Ssb6~|&5`O#!@m1Gj|7$i$6h_uoISHfH2bD)A_q;qHG(~rH{hoGcEj0p7FXe3EyRI^8zxDI'
'H1}JXO5NU~$8m3b&s1e`V$dpq9kDrnmbULW*5y^Z;ZY_7O8n@}pHOCEu-v5*5<98aPoq}@yUi*A_|>d2ad@2VS46sJg7n*j40B8!@FWFtYG5+=2cFsv`S#iM-)63ma-0amlGu!n6v+?XB$pc}GJx)glqsj8E%ND7swgo{0yd_IzsaMuHY@gbjc-?PS7n(rRapg=Q9|2}ISd-D&PXMsMSAdxe!bHA?D$Fp9O|Uwo_Z8biSRLs6fF9P0=wGl;Y3~kjiV&H>=yg5Y#L!7pH+oC6%ofk$|22P&aGJ`D7cNbS=GEdd<cbN7i7Z?C$fs$nw;v{;@Qw6E2F_LM5%@FnM_^}C&q%O%3A}TD)Pt{xA?*y+wz>H6XE=zGeUu{7~Hr#lbTRpPD6B4mW959CA1L8rZ@V`b0m0UBKOyLw=QNIVR0v~Rk{>>c1iKJ|80J%DsZfZesa|aB8oGQOCUR%N_03MXGT76OOa*>-}d4I@%UzOy*$Kg95tjESD5B8'
'g1^wh6FdNNg{a_6J@mcXh^*OrK(JH~<L{RJDo$V^i*QS6%ElS4Zm8_}%}=R$&yZMR+xRy1Y5~l?$q3w8X4dn;ZKMpZInMMV-hbZz(fyd>ZsNu*YOascXv~IMf87}(vD4>5NDQXf@3hx;1$uB=&Kn<O1jUhp$irVgr*Kr`3On76x3)b_Pfux;2QO!iHM{9NKp!m9DyN;>ga5)Lq$@}_khZS4cy&qo1b;ZN!%kR5F&k@I_?<*D$MS2lg>J8O$4@~Q*RML?4F@wS$3I_4&umeK=NWf(FL@+jW*{muETHh2SNQx#i8c6x;0nQ6>$2|!U!^|Ve;dNf;Kf35Xv0JfTxB#EWSuj)uHMx9_p=VeB07nLX;9>leQx!*bd+wGq&9Xm?T8U$K{Z9GZ|<^ZSA!`3cdy@<J8hSglK0ikg-6&LWV$oG7Y%?~6Ofqe;&YH)ghfCxN#)a|xnjeIu^m-4*%S8~lsSTR{MzmByPA9r;{*n%nI^Dh6vm8b3@EWC'
'+y6?h5hjY<Bi)HtDii=&TW}nQ|FEdfR+$>1sUPGI=z&x`fJ-yCtq_fZt)+)YFw<bF#hocI-gi>M8$iizJHe4IoN+NBp_iYj#6bg6Yl^_)u@>D6ZgOV^mbm^=a4|1K*5mN@LpX>E-i=tvSGk_Bmq*w7b}^SMEU>)HCMXVkqUW@eQYpuHP<TvN!hip&QzBo~)r?$_HttiIAAT)i?;}E>LXZiMbw?V@UEu=00=*j_VT2CFT8+LP0O=lBn3eL#tJ=oLQzpE0L3P&vwf-hr9p(1<*}ceELme&Ep431y`8!x0%s+YZDOF1T=tH22c!u7Cct@m{CTsit#wK4fk8_6;CY^sVGerf0NaMn-tyz=)rQRcOc0~XyYHx{~8S8NDjuv#G?`ly1d@4-L8(4Lf_`}GI<vV_8xa(C7$r7RvyT9+iv1fMc=K@Yffk#H@8$hKs8-EOjD2jr(F>8bD-NZ$kc{=}MjR&T0-gH>{eib3KJC|%Fbq=zvP?%XAVs?68'
'ZIr$hWNxW_U))T~d43;SPRUP`A>hj*n3nW&e*$#kp9D@9<m%9Ibb`#iVMUCD;DW88p-t95_?w9xgMG0@X$twW^ZZ*AIoBXg83%bLZ7O`;=^w19n)yM~QeC?sOB?lXLruDBp6OnD3O~L)9Y+t(NUI?e><v^K)yqjMgg5Xv5xp_lrc9ufS9T`0li9;Zs^$9nk47NCs=0AMS%<;hR?gyp#$NGM73JqgipB;8*ND9X$|XX&Y%q`~7wuSVW>9>LPQX3v?(vyJ8_XGfE#(aj{ljcA)TPf~q>UxV!(zQbb6dZX9djd)5UY$ph-i*<Pv_r+LW7k5T6;QZn(e8hj6y2QVDOFFp(38W6FH5H<AF0A7LfS0Gy6%G|J%K(Tf+0n4Hw5nuk=f!o$k6HNNd*K7XX3uyOps!dLU686!{ErM+fUJ2N>3)qn@G^L0i4Zr>$}c5Wi*$@urskE;Q-66;S!NMwuz9-#J2^Fa^8r)&q1J1e%A-@G<OwamO3um;zLI'
'g~u2Dt+*4PPR`HKx>Qwk1I=Q|(-0zoIBL&R3EctcxULs7#GsEcyKBL;vUmwb8}R)TN#Rd28!Redwz%wP4F-2PXymDo;!o;*a1B1BEsa*)F`ewc>72Mnn4ije0L`)wG@Z84UIG>Zey;nTEwM&O#0nr;qG$xiO0LVuFhuh&>pz1LAzSx`W&jjpzhAx2WsiyM3$0eXmeHxv&QF?-PUU{~@+q<RaBw=HhF2$tDrJQntKUy?<vay91Garz9H#yTIRWTpuf(j9#8Dlaz%78a$ty_lJGiTwkFNNY%EM1Z$MC^QN|7%Ip83eTeC18eLREj^*NOK-J*dlT!%}aZ-yW;ej&xc`d75cI1~r@`U?}QWH}=;$aF!=S7ZZ3xTEP8!__bT{>OClNCy^wDzT%Gd&lp0EAMS$AU~ZDzi1H%AU`l3K$&VFLC+PJWXxT6%EP&BNJFrPIUi<9fW=!kZk$=U>rX3bm-n4(pjfWF}7F#NaMAK>&$BLQl*y$Ho-1|MA'
'OnuJv=kAN1YU#jMcI#&Gy*iM{i5XCy+eUbiWvEHzLH^M=FP<JtHJkzC3nRI4d>x-J&229c39+XpJ+!y~A*nU#b~zLs*cW5b94Juc7${WW#=(_5Eh+tbG&N(~UPDo|pv>hW(E>TjxnXu5+CrmDB5)?lM6Sd0fT>+Pn!;m57ckaM>bIn)A4<$Aby=Cq(EcMdK>4S5Xs%%x?ZDuZPt{Nv<AZJ=x_W(bPiJJv1rPV6nz>zq0F9x>u0Yg3p!lfN+|Q7$m7o=*%k*cJjf5jCZ}mO7ntbu2CD(SH|JOcLfswFDwM!?FDYh(49w(jakb+0J<78~TC+oiGCS_rX_hIc_6~SVk$9e)Lmk9Q~fWY(C_L~>?i1DEF0aXlwLn$A|S=+S$hPBo-H%z{}0Be8_^^+J(DkuJ(=&D>L?Ok?%@(ZF-FL%FdlKOV0#>mw_BF*>pBB_2KN8!N*PQ{q?LTPKGu+7lerYOufqYM1<(+J=_j-c)V1e-8OJipn+NfTtJ'
'SZ`RF)Bph?PaXbn$#DkfM0sJf`#0MpCUHq=d+)<72Y3v5krJD_G1Z{d5v^xRLk!08VFE-t4c7S#dzb)W)tJ~;<uY!Kl{TZ(#viV10lZ5EEytAZ3?D7kwgY`cbvgLOIM^#6$dSgPw?VScPt;vR7f~)gDVNi6h|Jd_LN8oH&F}=RJGFrE4{lFik1qh08dv!Z#Q+?4Otr3lPTOB(YW1a$d-1Us(<Fp|0Wgk$zgAIZ4g$|qg*zg7mj$eepaL!W4E4cL0L)#A1jRtn_8)pm>{PtY_vetCO-hV(rdU$pU?PP1JFR1tN9*yZh28dssZyvCYm7WiJax6~Bi6&RvzMC8P5sL^YL*>o;mCCh@DjltPBjF%fE7(lj8V(6!$zhA8DO1u^#tWTtWR4+&*i+#4G0@Y=4wbsa`fV+?0B4<H^v*Pt%sk`TLo`Z0AOYH;jr=-SZ~_}102per0tLYO8Y0X1KfVPC~_P~&{5MYSi!JAjvMmI-DZ$uJ2Ml{C+%?D'
'tM=s0`BWHo6%xNKs%`6<Fa2cPVMt(^sBJ9gp>Qk^<n0qefds_Je3V!T5LkKv@jylV;aIEx<4U%-uvsQvF@D;{>3#;0pG}8--kiYz!^Kryt_y@ffVeu<MqkOW$jvDt&sP)aX5SNO19Rp>c_;^{VMcK)Af#=Q?4H*BU%_xiVB>ZX=*L|R&V|vX8|X*1+ypRyB(!3C`aokH2+;<VDo!h?ZOhf)mKmmp6(r7)e*6_~-BfeJu`nxWY{5}z$OGU^<_ws8Hdz@i5rcGO>@g^Dt>B2#7-Elij?0>YWzr55fCJmuaOkzBJuRVW47ps7P40!n>T;Z2i73&60|Q#YT$`W0g4SV%-HfntiY<njH|arSEo{p%Kc)7`GUJlXtIwUUqCwEcF+?d~@pPXt<q&0=Wgz!LV`#K3Ce#xud$4!HPA?9MH)@X0`VwW9;>A?7*RUz4jpYukycCiv0eB7g%^+7i`@2Xf86oon;0nM)J0?Afd{?xL0hnv)2@1#O223UF'
'AKmudOHs5q?^iMFXfaY}Ve~TM1)=AUr?z(oAMOhWS|g>$Nd<&4c4O)k7dZ0VnPh{1V7*L|LHxv+cN18{lomeER+en<<JP_K5%{BiIJEkE852_)D-MX$7x0Wkb>0WsgqJ<~QL3juWf%3%wP;R%5&j|eF!KW!&#`hNtP^#H>kRQ08D@+dALt_(jLds%UXat_&h3@^`D!k0L&UVjY>_%(Q}<F*2v5`s&N$FcGWFo41w0FxQ5>p+A_{bs0HWfIu^Nj(0?tiy18XHu|CucXd}Ai73j`(FFCXcK_l)z<b)Qc-#U)UUw}L#}18cT$aehBh*{weH=wwdYHvyh2MgxvR8}%yMGzb`V6c6L#As}{!3x9+g?SlV;no>Vl;!BXW10y~5pahGB+Bz`c*MYTxxV6OFXU}C^)B+Nj&6=fZN24u?@?b@#tv}0YiLah%Y>^P%e!`jg8TjooGmwH|6soyZM#Oc~(kpyi3d*^6+jl@|3W3hYK<H>990~TMwtQH0'
'!8T8Z##`dq+@_L|m-WpgG3W0!=?AW~Y?mgWjIH8afQh$Bl$hzmhF#i8b?}3MPLAls^ixB&wb5)_8qw6Q5UDA^A?nc%pr(ECP(B0D&3>^7rp}pMaWV-*zSWQa9zIAm8(E9z&-so|2k!HM-z9>ZZr6+7XqKuo+G;p^Fp!&1b&fXcSX;vdh*Z1sd^)vRzA_&Ter_6vr7NiUxEoNDAIQI|&D%!&xc&tPRMi)fKx<N2!@T5)VH)WeHQz@2-fg0CPdNh-Nw{9!DMxdBYIZi|33;S2d2e>}7xC5C(-aLaE%KD;HH5a5i}K&t>zXE#X66U}8DSd5IhlrnXx)0zF%nCb8+uXe|0aE=Y?vEHva<X!Gcw5EKlLOm{>?(EB0PC*+sq<+!nq{m!#reyR1#zyuH2+KJ>Yt1EO*Wnt|OG|f>bO@ZfZ!Ml5q9f_vZ^>JHRIF#kubzlEvDn3v|>fs9Ipge-I)Z>gb?#PVl6kmYkk^LN`W}lKIqPmu)`WtFdwV'
'-DuZ5C=|kDEk&*I2ovqg5GS?Tn78)c-{}h=nUqeD&H;cbs2#HGt|@tO5DIW1@!sRc+Si0zorS_Me@)~>Ni_kU7CAABpal<jC;hjvOI1u>a0fB0$wNs`W*oUE$^eev9pY+0Ai3_9rl7M9_+q0xID+r&h|eHy#`2J+@LIeZI@ses=?X-zQeWe{aDyp+wjqT^@<%u}^Yl4-bomLkY;OInhYyx!Xdx7NUTne3EvPl)6`}S7)F4-#vHI(!sliuIk>2o@3JV9yh{OV*2aRJ$oN~_^4%Ko6R0Ic-`UMv$Oi}56i&JvVR8Ub8fRgkM?$<RNGPRfx^=%1m2K_2pbE$5q%p&K~=}elN2EPPr5{G=#hFtDp(v=M9_&#;tDW%QWxFeqmovy7tXFq|D9JCgz4M(g5I3GD3-Tm3ZsGdh|YE+*z?u4CZI&|<PZjjxXJ@wf<O-B);6DAjo3*vBp5XNGMOv0;a&U{%9plSpuK)F&l_H}!+D@^<*CcHNU&jzn&'
'$2!zV2j}Fd3FCWbJ!C_b=JDSDYo${0zxcQ;R)4#%%0CJ7?2~e2SO045lWR)qH?4K3rIyz=KcQ;BoEA7kT&tujDT*-c2EZpmvQU!qxoq^1Do+kau168d`Cb1Km@0QcboX)zaIEt#JFMKh<}sTUJ@8CzRD|thi@z>TkF3*_kF~*Z0V0e{ZbA-}Np&S?Ot{>er#VJ)GQ=T;k=i(qrW)tg6o}?s$8YM8qJy=%q7mya(tiK0_<WYA4ku*p-a2cHdRi$(0LnmWR&8dzH7SwdIQYv8X%uKC<A2(ElhP9p6xb}Tl80;7QK?PysUt@#R!KZOu|@5Lm7hXnHuQa6|3-U0&WGxQh(3mKIg0wT*^RC@A|)}wIVt#yKZ;zoX^B;<DvvGUd=z^ZjLlAB%LPtrd8(K}8<<1f8+MatJo!wZ7OGtjDd-;MRCB0TJ_(eSMwT*D&ycFJAK{m#-YV8C)`Qs(%v`}{N$>Z(68VRf;7s&j{}qZ6o)B@sBifv)LI<I}'
'B(X=7GL;55HsI~X!kv5D$(EmN!7guEbXX#iK2bRNSa!IBwEHVyy|>dpYq)l#xLe2~K<>;W<1C{u`>q~6Kqp{h_OLZg<NZB1E^ltJ*Vj)spo+F}mcv_YsyOHi&(shtZkw+|yIUl;<l5kid~+lfAuS;w{hD8-1i<KrFS%$!P~*qI!8>l`9tp-R=319a5h$>{t6H-r<zEG-YH1ooD$y}~wt_&d4uL>Y2fS6w#_0aFa&1GA?#_l(@stTITMRFBU?0~J`XhCk$T9ZI%MWQv<{DOqNG-%BPi<cmw?ror$>ZJ#M2)@XJ3e+W5i9vTFU1e5_K9$Z(c8=QJuZ(8v*92MyWsdKe`(K>p)_QyRo$6DsZ*!MiG#e-o7K@0Jw(A+VR(FlTg^%|vd`g!$!#>PJoqF2U!_ZSs_>5$;xX<S@Chw_^?0MsM*iPraiQn0<DE0H&P-44&=a7(Jh|}O>Z`+TL?vY3jz=N=xkevSH*E}GF9(wKmGhSIdCv^zU}0@{'
'kQr&ejUCOguGtA*23}*fkDI}$YI=O5M(dm5S7c-Wpr|1P2SPUGa*&uRT)XC0(8Qxz+cYtK2jW#9i@{4a7`~qfZZ7waI)i<(c$87FgkBZuz6qNXKS&h>UC+p;f~(cFYBy=4isSSWs0eq=wBz>J(C_+JiP6VqS1EfPq@f+{qnI>B)5}Zp`<zQj5bw>6hdFKZ?KqgK1o)L>i#m;r)DdcwF-yLV79OA4<#c8)U9hm`ZJckE%@d|NSB}A8IgTx8l4#<Q4C8n#fGX(5!UV~vf7e>BBf+&ekh9&|OiI@Z<az=+L~K&FGX<T6E^8H`bH02m4)~FajvqTrJ!;yTJcqWt3o6p)zw(@pa<iX{BV;0H7OsNFS|TL3K*Y)Yv7mv<eeQ062-3r4>!3RxperDeakoBOd0PR1_Ciz0+SgXw*>(HFEK*1X^J6?m#Yc+^F6=M`Xv3x4TAxT@Ii?x-)J`{&!&Ry)is0NLdTfF>Ee!t>a(%=h#<#2JcaxjcqVCL)'
'^4=66YHVv6>>}m>&g*r6NPc{~&D^%OIPqsTe!br~%<@tLg6bKl<1hyI6HiVsn~8)<o=;Z|KC3odL+Z7pa_uSRwhzNEtlQB{5+kCmp2s<#JRyI-BV2s{+Y~~Y+~WZ{-7jdn&w_i2PfJWzMd{RA^Iksjdy-*OX8Mz>-_XbIf;EdYaTH2KjDoaUvb&Gf66^Otb@Zpl<y}d-A`lYQguHAfAErmn<UxL;$GF<YVeTCuv586eMk9g{hP6}Rk4X|0=|#r>DxKME4WsrYbc}C(1$|K@g2CHDU2$~X*O^2n=CQ;>(r&RPt39pNFsiyDC{Qs(+@e2R>eh^8Q$fV{uC#$btATR;Z&jTu1ji~AY!9?b^%;H)Pou?9MgaXeaX?L79t=qzyIaqwA1VWQR9rwcQ0~Z!EpU{_<Ai}g=n1+&-ky66GRiKUyPPb8KO$}flAOb($KUE9VJtngUVaq6HM~xib7NH7wQQieCCs9a!H@)Ad3L3s&3|-67$dB<Z{gH$'
'<LV!)vU~6BjZ97}&Re)ooGAB4yaO!@J5Ly+6NtXsw>8tLOkoR=fh}v&`e>LwGefDWDdO2a6<(=WAc)F(IPElk`@X5@EWB;fif*M&7=!R-o<=$}e|msVO12vAajDM+(vSaBbm`;C&PDF0ZV!B?eLj(=hvT<qlszkCrZlE$$U#EYk1{9US4_Fci&cEDUth2wAke}um-Cm$Ud&tB%<a=p0kte0%l2{Ga0XLLIM<KYPHZefQNqr2>2kc5`SHHBGChq26`oV1%oX0PYK-?3wp!o$s%8PDsn|TtY+V0WPs<+YY{Tp7!@<=^wJxO}4Wlj`!ANy(QgAGW@Nxc5KGVODeDJ;D?6t|8Q%?g69uS$oZTUZ1%3*0CX&&D{wTbmz^TWyPUB}h2QtJt;!_lR?Ycn-ejJ5EfV#aG@Os71IbQQw_{l^GnraxwX1<vKvqUtSGQ+Da<T89`Z1V0NT)&salFr69Z5|yN0kw3*oUoCwf<H`~)>unM5p_SVJXJO7i'
'0f+m}eF#5wP13>|7*Tz!7!ctcmH8SxwUAc$&=32}mSSel9x!*R=}k=VRI!{nD!JM=Fn;^Ds10tGeQ_a~O(Ma+3(IE7hOz@Kz_J7;$QttC{9L(qz9Wx@l!8T_G!%gPl&5hQHLh_~tdk4m2u&vE>vOXkWR^`7=DW7jj)_j{K4rMG6AJg0<VtkwC1ukrc?tGS(PUsRZY}+Qkacka)Xqm?4^FnMLmXyNVwBgkcT9~ZVed#>KO}IoT`blKqm20yY7pGwul149rPmlJ!tA0?JiU0Et@o>s!@TSK*_rC3=u0b#R4b}9m~!aEHWj{Uw}p?cEs}tIZ+oQw-BuIZ{tgn^87Q*`^wAv2ZB@1F+Ix|c9SWy8uDl+~!chd<lzllQn9}NRhdY3aS^S5@hYGtOl2Iuy0pHi>KK<lE3t?(8YjIfen!@+Rar%M?wJk{Ku*321Of4)*)rP0A881PNtoJWMRFPJU6H7fy6CNK6!6Kz71$l|QmY{bu2frR|?tcw{'
'J2(;<@3&r?Wm=X>OJ#`(D>Z})TF2h-U21QB*C#Q^bn-|*GB{`;G2-goD#<Z&@=?AOCwcdT$_ucM+_qUH{dt=A%>R5vhU-&Fb@=yyvmi}zTPn!;l&SY*<n_!GWAits<-UaH70g^$_EL`MXm-8$?I~Rol6%`;r>=Hbg(&`RgxzoV&na~YqpOk#s@-0=4+B18%)BS=4W!5(O@;odqGE$@vmHrl>xbVC3m=;H@}d+F3q1@J=|MQedS2AZJ@@LXm;A4Gp=Lg&wSD(ge&v<ruvIm@ZL(RxCbI<m$|iU!ix3n8t2+Zp>=w0k!)8y0T(jy-AO7eFv48SvcgONOw$4WwJx}YWRc^7iFu6(nr3eKkNsLfV@u7_05uryOhH?ON<AbeUZf@J`O8WDvF)VY2ZIAM~vIf~3;=7E<Gjsw8PQIkTKR~m4WI=NECXa;A3WedWGh`X~<5(uP#6$CgWj|aRt`H{xXi(%GUK#mD$e%}|b|qA+R?F_L(4I?;D1&=g'
'rDfO)eAXCURt(;iV0<nobDdL1&0hC5dras-{Wtrp0*dXxF+~sxpb+@$ydNNR{;TuAU>>3=#ijaPk#iGSnD)QjIsDiF^x>hNVv-tEM?)-L{S-at%%5-99Jy&HY-0Iq{|rx>st)(st!1);bEN5a+@OvRGYqdKA5hmZB$z6CKNHx*2=x<+`R-<MzM}e+V_^#fKNGLoIc|AL2kf}3&=Y-a>hnWqSo7bbWv+x1=GadTh0~;IJM8=mleVH<!z6z9<oBj##yRTL8IZ~b5Ek5y=@fj)0~~~s;Zb2avV6q`p?9GhL%8=$+im_t1Kwq@Y$JfZz8YDK4jcycaR_dCWrgq%VA!mN5-=iJ2Fd#vHsz1r+!`U;S0NQu<7rNU-<&t$;Iqre`O>ap?v)QK(0T}wIC`OW)pgILfJz&yIz0SebhWz|+{LS+I=tvd3C}c=_S;_+gP6Ai|5s65pY}U=dQE`2i-dl^;CynNAwRM9(+hS(Wn2dOZj{3xFNVIFqzzMo'
'9+mE(dqYJrd1(AWSTUZ0U+4c|EPDz<Y+FH|^*HKMRj)+u6pQA^twZfiZ&FqJOFk%SMfW*=!i|F6a^huKpNHB$h7+6o3`L8tmQhffQG7(u0STNpWahhP<PX%n|864H6tH=r8eA2Xb;e%^h+MuJAgoo^mKG~W9RaiOJef+BP$GuX-qMO+R>!iUUaL4f@Zq_7^7-X`@4XA!FYEO|c1BhJb*LPEupOnD0?(KSOkE<t!VtnQL@z;x1SxOPqB5LLIksMVpuqczX#Xyy724}AV=nB|#EzfPA%fDHfH(<At2O!|*W)l69U%@=LFBAR%gP3S=H0CP$^zr?!*01d<(V#<S$beW^N`1qfapl+#5->kWszpH2{qwU_Niu<e(=Zx!guMMAKvti^#(QJ*r{@3-xR&N2{<=(*1!O}H*-!e!tt{o)GwOZumRgHTC-HW2;;=yUp)r&_ABcd-a9N4-~l?)yh@P&C`X3=ps3y(y{3QeS%;*9=k<3&F;hFpkcui3'
'#lZ`pCTS`hzs`^CYrJg@zyqwCUfUNx$spdYd)qz>Dvfn|W1ZO-d!yc7Zt3ZlD?O#qxXuS(IpQld-@AG;bNi9yWgh5o;9loTSA=q4(>Oj}!}^0F!QTW0qeldsiUBU%4+GCJmVIs(Y(8>Y?7s1Kw(u#uxj~%g&U3IArke#C=oML~h9*Go+=!3t?v0k+=M+{wbtLkN@1Ie9A!I_^Ta`t-seCa30NdWW&PJb061oU7N^_PnaelEtSoU#uh79jUNbihpdGULcx94cTRken`i55hcmD2#AeMK&OPGHErnt;XyH^Q%H^aOXY6^0*w)`3`MKCT^Y%`TTP4~N)>OJOyp9H<Ju3|tUKQM-~!s*Zvy!E~e|X-I5rE|_Yk$b3u4FH~RPAdh{xUE&FUDk~64r`aj*oR}a$GHXBGi)=3*R-%nlRuS8k=#99>l1Pdu`{bOcYH$V1hh)ZptYYTC6R3J6toZso5<tXNQToR>?(<%V0z!A%1X&zw@AE1)AMV!<'
'<Raj}@Watz0l`GI)vXKvfoU$@{Q8sIW6Eo-z>#Nxc5O4nnQcL<MX(wqJ*>=R5E_6!Uw`jJpclO^2cj|lUO4z_HEP{a0%taHm;PwF)oik~r%m?ZnSFv!@uIA0G&EL7%H{%ZkRt|*al_LHv%{H$MGi&>;jgOmf8tX~Vfb50NN<V7XQzllz;AQ%oHr0(*5rllOGMh{@PM`+4$Ab-jN5BXakX_vn`5TwWPhuQ$p_}EHBpy~kwkq#tNs-sZM0djfWEjyHBnrb>plK0{W&Y!W%ji@MB4rnaEi!)HNRw!8;N+DGBygWhO>57e4{qm6%8$N%iH$|V@LBR8TG(2sn9w|P)uzVnJYzbZUD!VqbHC<j{$i*gIYgsIdxR>(syF=>HxzFWi#NAC6xrE7V8V&rS2|^{sq3{VCW`keG9JfC`e&nB{j@nTYjlz{UwDYN)WE0p@>_RL+VE3OdFrC#T<=vJ6l58-s+2BHtjh-zJ;#h@<plRcSrk6@+RngiF<xr'
'r8+DVVdF?9|LY9$a>OtUn%mK#wkTzCY%j?3B_VpWYV|ydn9J3I6;OXl2I;JDHy&K8IzxwRwOB;rcvZCZ+Qm(mYM$gbkV*Rz;}brcRiP;Y54J)1eima0;2*#EOguFvDLQ%Z=6iarUV)29p%O3GTl&u<o3FIDQnk1MU#y`H$lt<J`hDNlZk<}Df;it4zBjkBEVb!G-``rB9B{S4P{|(i*DIeLnnPiiGQx5p#cOi!2HEE#3Nz(nXOffQ7WF3JI!?SQ0#{Mplq<UNzZM{v7C->v?t<^@pgFO`bJwEU{xrnD5!87Ta~*PN?SNxb%n!P{XrnV+#yA+9-+n3u27XIZ8efJ$-ap2L$o46%lqsBaVP_<g0$yG(ewKcYPMwIzw%kg(m`nuki;{cM>NGwG!mEh82_K270(#%|eGX&y;e{mSa<Uj@zJycX!W6q_!_5;bSidoB<h)$`AcQI;JXo8?Y`BF>yG(sy&hNe@@~oArT{M5rCov-W<?b|w?KDi+'
'pEi|wbpw3VAT3aNauEWNauNW~Gl<M?h;b=1i_Fs`Q-i`^7Q(+VJjBy|*|#{p2$-RaSRsS)Ufiu;_Ur7Z0j>zA9D&)qCJ7Hilu;X*d56jFkdMhg0UH9M^y$+chKhxFpnp?Tgo~RT{bcU2ma89_+xA;NP1_O|P?4#uG~GJp!G-9*cF@Z?nIjpt`ZZ;@*Ws&ND~3Q>RY_N9Zzw+t?@uSa_z;?N48eFI)7@O1t0?|J%_?J^85fbF?i*87)pBGtYz3N<E3QER$2gj*Pv6Ab@O<dZD<)sCVBQ=i4^K;foc=>LH+XnYt3=D`2-N4k@yTuTfhtBwtut#;?vwQZOAk*sON&AGrW~HM{lpg2NE`q3vL0)5T<Cp+z<Fdd4z}l4Bu@P_F3tWN+qJ_<XK;76$Cu1icdYHY>XH@Pp~dPH?~!7t#QMz+`=$<^m6AVX!<?T$`mE-xVe~odncj%S&r#KL99onEo%*$gKj4<d8?)JW-udBs;BtM{u|WzSG@WW#'
'ELyfYP=-P5qCtzxI#zgw;v9$9lTih^Wczv<m_X$2a7u1em%Ih-inNM0F>Zl#JjSnEQBFPXs3;X`OZ->&KvEw%z+jxp+P(9p0S(jkYqiXfg|DIm2iKwSI`4SpnxR(<tWoQmKnlIo*!j)d3KV<<TuS`8LjrHNS)aa+URirn?yX^OFxkaApoI@!Q1ARs9oNDPT>w%jzHiW~budCxPU%n0=U(5J^z`7|oGL#6S>eTIY=FrDhYJ3L5nJhIXA~VKiRum<w0**{uG4?%uUuk6DW7h~G-)qm<%P|sV59kED{yIeYo?0P_NLCzDX2%)|F5{fh=^TeidtkJViO*e5ZlOcBUF$+myAw+1F$*jXz`gIV5y26v3~4D^=0&C3<D93KnA#Wfik%2#5>){a!^gjDdSTO>Jp8H)3Rzf;Om#KO$e+bZY7W9()jUvvPf?E_Sv_+Ur-N5=2QO5i_U{opWEFsobKEu!*p>{xB0pFBJC=kUBG-01jd_@CG<|`vsH0?'
'10V;+zt_Wbn6OfAJ%uoS8c`GJaYJ0l@OgLcOsdxG>zPZ^nR)p<TkY%4HGppD!+HBoK#mFc^u%T6nQtNEhmE1Wh*GH6iTxg2{G!JGXY~jZCu}|8r1JG5I)7+z@#ZWQQr0X^SWC(dw{3mmaLi8kD1SV0?czullUupEjluEEiag8NL~QE8R-ccpeEjVQ$`J}~te*77!Jey66cacH%RxNGSrucDFMw193$=2IAd!UCTWOm^LOeg9FtoQ4V)dA*Fo5w(uqA!_Sid&Z*V?zks_wi+c1cQ7y$&LA-jexh>P-uc2YFFa3B%wSe-22r&5lbGN7TkjIR$SPEHkxp_7QE(JO|UnoEmjG$@KG3DYA5ZPBZO3E6PDO;i06xx(4X1OnmEH?<S=z6RIaeCm>vOWWCsDdXRMPjd{q~aR4D2|Ix^<7LxhqK8>R^Tm_{a&Z`B<8ML2tn%df=aEI{5H=7&nN2RjJJTu)F+%V23bdnpsHKbh0?bxLxdgM9$uIz`1'
'=HC<X?c&HtFaU)-+>Mm9zoS9iTKhN0o8hSVnQQ2iZkLHkYHwD`Di$h#&$eEUb_uYmfqnc(Er1dKF$+O=U9&GXjsN=5AlHgE81ZCMl`=lR7lrU-L?KoK#|&CeDGdWBS=w=jhLV*W+6`1(OX5A49o91@I=+IHv)AunXDJ1-zXfuEkbLk(F)9BeQDKr3SUkm86S8}$hxMSNM~!nB-v4N|0taspF1w2?TH5X_sMXs+5r;~|2~}c!Cc9$=ezl|UUP#3TwsKK4W}Wuu&5fI}pNzW5jeI5u^Gf{mB~Y|ilzoG?;A3}-hqTg$2QC5#KhrW^s~U&1HzutpmBM4aW8d|$0?dLdvyi!WbHi44uD}+aV>-a_|KaJmOv_`1B;>jjXRRtv1(EhTHDeDJAI+!mhN_ECT$j*)#sGi`qg6w8EVXhhv^~iPKd2L*3p7UoYG==#cJ4nG=rX8cyZBuQt<Y9s-%!3<eue?e5Y&bjjR=1O<&`>JUKl!&LoX7W0oKy!'
'H@n``sCJQ4%I>=TG|Ndy-z6cE@wvf6(WG!wQQ>lpQ+-fltS?O)wra%_VxuAb9c}aJJ9vdT*FPXob<%5%eL~T(Atm$x@DF*Z*3Rzv4g6OIJs5%Wsf>Dy{p2T2??Y`Sf%V81i4%0w7#zT4_@7!w)Lp6R__CRp<qwW;GgrPcdNrmPwet;5re>(^U=P`Gvmg;#3TF|TB2e3S2Owei@m8uoTNd92O8P{lQ=#NUL95cq`R%e`DQZeOhWcHrlA#a9X6n)0e5Ml12x6y)kt`R>ETiCfg%*9(Lja<h-7=TQrWc{Y9{_enR31B!GBb<~cZ*3fn=#GkXQjeN%wZJ@JNfoc9UFb>GQ(=9XsSpCJut^9??Lu9nZ%A^*_G`;6Im~i7yKS_Fv<{G8*Ngd7LVm-fGweq3&y3G&|EwB-bUTd3*=uk5Kytpnw$muP$?Hm!1d$b{NU?55rLO0W3RQeGT4i!cXo^PV~(*WI}ukgonTT`(kh{M@T=U#b#t6Mbrj_E'
'!Zwl?v>`EpL$6<!gs7R$StogDO3Y<I*q$vO_yvpwzbVKhZYx=`+stjV4{2dfoPm%NwOH}2TY$<DsGxVt;WL*jebC|0jaA=33mP6AOA6sj17uNWe@g!|xz;c*;;-qW@3-j(N)MHAHw3V%(5Hf~{{-ylTt0*sCsfKGjm<a+J(`5wOf_dfy#IQSPma{_drd#61gINV0J@aH2Fo{%vE{l|{U*rN3W^!F^34BV8^3rU{ewRkquY5|uf9#OewNSnBSrFi$cTUD^H{v-!u^NQ<E*wlUmm6;7_|xCLsyw2p6`v<kbk{+=d>sb=uoO)_4}%3_nCTLlh6xVs<OadHdQ+JJZ=T#u8An!CF%-)<^nf9x$gNS!>c8>Xj?^#gt_Pj%r|~dZx!FR+f8lK2}IoxICD(4s5o@!)S66qhA{$|HxfBCUk91FDrT#KZK99;T<`fK&E4N|s|f|Bn-?<FbyR~Em6&6G9|j&9F1a*Yb9c0z1*w4*dG#1nRbA-jaVa7G'
'{mtqIS*v|CAWs%ONj&eM&o9J~tUk4#&$ki&w}OM^)ZXw)_KkwD2KyGGKb$d=MlnCso7!4Uc2%eh@qv!hdCbr5R*FxP8`j0_)JoAoV6^y#I9xxaNbTwtBhc{!fXAAu$2CtG-zIRc9Hs#^rll+y)RkAQ|0U&@z$(qtN@#|p!dq&bx-?`;(F0aFXb$YT(5$q|*Fi{6hMmM(5Q5f>5}}>zwu3$O_bQ;#Y8s;&;l?pGc~%(U91qLvJ5y8ocWqV>h+IlP-wS-AP7=Oj){s3<k>>D&AF-c|hLhaGY@zo`B^o8@G|o_iZJj?vhm}+dc)v?B_RYABoz1Uq3+AVJZ>POL^YlY#>v`Xi{)GP_^%l{5^z&u#`I`@L)GTM5t4fvzQmDz8aN?1&X=rCHNHO|2dfEn@vZgz$mdzM@ei-JvypN96Vk`i}S2B7M+XB;t#>Y;7B;MvKYz{)|I9^Ni3BgX`6V&jWc@XKNNb2<h@Z8M(-v!n!Q@*t5=daHWU^XCD'
'G93wSVT9w>hY$K_C@qhPR$yI~hjj~}sd;7X(Fnv1Rqm+ypMs#&qH~er^`ibJHMOB&H7o(+Y#rS!S0&Q0heW6$8U4kE>PC*E`eC1~l%9u!n;0|XSnKTEt?*Hn=TNz$o`2Zc^;Ab{lITTn6+>6%NU?t~ChTo8moUb5FkFyETL{p2ZKR;?ph&CASUQ=&(=NB^-SB_O&~M%d8enTw&J`O?ab|Pr9*la6DY&A%L~!R|Vj>=t>1GVl3TB|VKgz}6CF-Y-prm~j2}XsQ?mUC!$&K2D;9>p?LyF^WYzsQ=7JH4MqD|4G566m&Oizq6hMPcf30vHI#aI~{I4T^=#1^lr@!Cm3+F`NNu-A1zKl}x(^1CrAj^tW>cklaAmBx4{({}iAVdfoU=yV6*RFB=22>Iq~z@A2v=fga3;V#7LNPT%hWlbXmlFC9th<^H6(X7#qS)LSFGv*7LGCkcA_XdQhAvEKvoGb^ZoY~%WBoOu_P*#B9c9yK%`l52uMG!c*'
'J>a_(T1A2Y-xh5WD&TjnO(=Ra=rK7V*$IIE)|aXXB?!GmLoNzL?(JA5ZyS8E0XV-oAKo@nDmMiR{GBuT2JsqJJ6pr&O;2@N!WaLJF%ELzJ(97hbmXEcFL|=TjtC*J(+88D=x^OAe^2DCPw_%MiI&iWja5Ly9XUT5x0A?GPMgdXlyqV#XK=cUVD|*$wWi7u88-u^wx@ocV3+3gS#8M*(PnHTB*SD!DnE@pakf}R(;nO~yx;cj_Tv?T45>Kxv&d-%uXJ#48Tn9F*#BYzvCyO+^+kc;%Ds50ch4vUAT9GQ4{LaU(|AR$>qwTZ=wHMs&>xGB6?>Qz)hS1{(o6zL{<{MLr8a@1C|%&nV&vX6a|n(ymIT|pOiol0FfCrEYAv#?>6U$#0;HH~YgNvWeo(jw$};S5+R66e_Uy8Qb6D*GF))ERrXoWnP=0=}9zTe&RoOeeLXnD_DB?*p^A8t>6{=#Hrmw3C@}7cIx>A(q$Z3`qG%i`$jWLsIUj))&'
'p+~hz|D@8r-a$;rgxR5=E?tv!?uKC?6Fo*?wIs!avvqV6#{0;bnwlGGfra_G@2XnVo!3iw&_sLiCBU>TGnV+90jJA+o*8lTa99f%rKoJQUp+LRN-DkbO$j8xYT2vch9XY&P0N&2%VNaU1yaWD`djSPjRF4F5b(I$ykNKxQzP)D*L?s_c+zv7b$>Y~_UdoBuds=6qheA6Ro`JBU}L!L7wG;j>ay|YM;G`uHJ@g9FS!oir&*|2sd+=k%z5*U-68AJ7zkIKEiKB|oscLWM;aw)v}rm%Iy|AWefe?Uy}8n$vqV;%#9F%|1u<R*Ta0r5sIIK&gZ1epgl9Y<uMlU_S_+JYDuY4AyuMF?L_P$J%aIGEQ{U5S5P!1TFohxbZ!ALAMxWg?D(MRN%2GIhPO2!koY0h?SXb!tqRA;{hc@=}p9fzb2G1yQwF!CsG|aC#uYZG`cE3#(xX@|OJ!Zln)wA_2vZG%nxpZIrv``hgTnW&g2n_MZzMEs3kj><X'
'E*yO^#Z%b#cab9u{g#&j%^*$%AxgXGJjQ<>$9JP%F47k|DoU)Z3|~#KA<I7H3p1Wr%7{S1%&S{<HZF{ZA*2?xca}n-Mxjl=N=r?%xx1d^saxRC;+<xHIyxQ5DJ7Ss`K>USEjwW^`zBdgQd%(Bls~aItap0BSS&C$=Cnhvsf~<DtFV)%EwHS|8xw5`5%06>%&0jqZ2Lrj{PIfCB;&}=0~iqI@taeG9d^{LW%`+-G)PZPR$^k!16rCi_^$K2GkFcrVGc&e`WbaT<!{w#j_94nIDf{TbH&LmAfp4AEY0s)I{ist(M!pV1>5pBB*6C^H!JNFXhLbmlKWb2xADycQXw|H_e%~j#hX)^MLl9#_LxgEvB;a81#2@v?wjS0w`)VvitR_^5zRu8;0N6l`E;B!!Do<O+k|E{B8j!K$3^{OsR`0YIklV$LHTzB0;VSsg>Y7LK3J#mKXf;PL_oMI6p|@K>xuzV4uj|I4p6&IQq0@<*QqWvB4AkL-C6x&'
'$X080vyK9<B2ZhXi8wFfY(Ro#a&#v%gx&GX@PmmWI4XMbl_uY<ja{DZqijT^X3rX0!(s9bspq~^Lqm81XDQKJ^wS@I&|I+CSKWwg5Zom(=;{UVG_~6u<aqFAW1>y43j3*s&9uts8w@LzrQt<_eAV3#H#|#zv?8$pWgD474->BlSS<V-11#YQ>P*+~gT7qhn=R1ay|E&<EI$tdTvav11-21N91eO4$7gp;^o;yC_On9b$;zh~OFUze0BCN*JJdm>Um*c^a7SMR@gnmU?ak6~aKqc$q(9(a@v<PjS?Qj=4-dbEx}Jg@J?9}&RPPF4I-i3uAJ*4&UjZk8871}Me>zxD{Nd6N+N`~tDUc)^&X**G2m}2YbU{2b|6LfztPriTJFBu?EIqyr0hLcWxo@DDi;HUZW0Vct8^t9b%)YscMxzeNIFX0N9Q+nF(-9o4G(Dn#%}Sd7dX_`7XNXWd{aW^0z<;nPF+|2?rmH$q24t9&O%h=_$VK4z^m8rL'
'5Gy$Kd;PuhfzuaS?Y`^HlJvHL?em<P{H?LQspGtW43EIhTTZNxrLhBHXYI1Ce9OcZlG?()NO%MKXVptfsx(w9>|BE0LC3Hvzal4raQ@A%C=W8F4`p=RyvKW1>zR|iBx#iUo%o{$S$bz3f<DZd=sM36iIOowAF7hbq24gxV?5b*7&va#uKu8o24E)AZRkaMZ7(2*RkYIjtmwjsBJfl@Hzei;&+ja@I5i!>j9W!Y(4I0F2rhsi-Mj?y>?FQl(%-qfV82)s<(;^K2Mjv-E&*K56|qO&g7IN!ZoM{<9X`1z)Vkja^xUHUt0I*nk9lup-RW+K^#YKMLvSnAe?&|EPFk;<B#X_5O2G*BqC3(n2LBhmYYANsYVwMa(v=p>=Zdd@hG<1|wlI0!WhQ}mzw};PRc;aMY_e|+Y@z&*8mGVs6u@r#c*U6~V?=!N$(7@;{D6G;N~X>z3gx~CAXTZ|z!nSmGPB*XPIYJS(VZ{sd;9;k1RA%EIyHrLKx}{F'
'<gb48A0+oplBYFp6SrRD`CR{j<3u6Q*bLL;Dh<$renug}h8f)eQC^=as|T-bg=iLI3!diFP5u9Biq#h14eH6=`NrJF>*L{us*4^J9%fiB;$gl5iJ*ttx(Kth=y$B_$K;O6N47M3Tx!J&=Gdj!Si?;7Et+D8d6L+w;Ngmj)m`vI;$t#RQCiFE=gS->GZnhc*iWrv<jYS*KGDOhy!D&XizI}QyCmvER4Ylt<8o*_VkGo^q)4L1-$J^3acDe2?u74&>-5z1&?0Yy3Fa^YT@Ex!C!6#fSP-VaRSdhP&-K+!ep$n@FU*S~N|5O{5~|c=MztPoK}3VFwP=d2ECG<#EW2k7!4FLhb8GKHqxVv`VU<(xZ<bobPN(gWbn}~!`e7fwq%YRyM}E5?{M>G7-nqCKT>D1F8i5;$E{WPRAh0#imD5YX<(sHGWhof5x9!XAvFz@*ARV!=!>rbIvkdyTV>-7C){xMjsL+U(0LWQ|1e*46yUHbgqDa;V7)~VK'
'FBs{~QhK<~Zl~E=r$K;TxDM#oBiOs}OE(4ITX&o~%Ea+iwmBtNku<0}7yT$H6w4}LTm~f@5sW}Dkm+GEp!r`fsYY^XpkAMgS>~>&jb(1%WDs*~{B8;V`jDqP|7*hHi5ir5t5mB`VV5U*vX8&*0z*02JuT(<U_<|ajSU@+3&xnq;yvTd&k>L=HK~Flq<`ee4TTn7MWECCfe9S;$?XtF41XUFRxPAmAqwJG*q{^$XxU9K1B?E7Sab3-eQ~C7v(1`9bH8d2EY<2Jil?&ajKd4Lo|c{9nauOI_D?@ad20N<^Rh`X>L=*QPc>l`0Hi3u%+Ri@HUYTADQWo~Lb(T}&(X_yRP!pQI1W^2EXvY{osZd~cOVqRciVRq%E<yKz5d-`^qj!L-m-FZKveRJ9jGId7KqPXuo;s^`ER1QqLPyyv!6bB912jHZe7$f5<d2x)J9##`qZXOZr-emMfgJ)dfYh@zf&6010GwB9JuD{OhMQ(<Ns0z6-gGs*wbS_'
's`w>;&MSaGeYb#Wk}VIkKrq>mw$4>87t?8<u3wi77C4TKN{U2j7{jZHCJXiba4j1{B~@-iHNTWgSvVD)QD@od(4VkjS2y2!>nHC=)N(8`qjKe|o-r}*Y5+v{v_y`3T`R}*M2#GRJ?^iM_|YQJ&^6w+(u`8>MnIEtVF>x>2z+rWxM5^KuUBspUFES9SMQp3#;7w%BKzU#!^~P>NN)a*M98Q<e*_g4RE3?RDW|H~xudsm%f`Pyv^t<hM#U+?OJLrG2T7-IGnx>S8ICK2V$J#*L`x%kfkGN;AX87lpj_q*Vu<+NMY^bY+!T<G(dp$n<ItqIDbAi*3^LU2&rn(XB@&rB_@@(LFw0brO~7O_U;pWIoyZrxxE<lDf$$4&5I}FMn%Tqo`Y5IQ!h{GHdW2FWB@W%HRF|+)Y^CrLWMB@0HEqkssnMS?++GzGES36f9HXTw_*k4TjgHU-cipzDTH7sKjlff=+_Iez<0o2N#B^ru(B+!&&opay@RauP'
'^w?M9&5X_?{6M_aF-hLKvUp2bQ&DffyZ_>ndpx_I3nY(9E48pNal6P{6|F30B>Gq+mS5e7eXywG_HemmGzuU+d+2H>@*9l1%Um*njG6?wx%d<j_+iW7_`wb}0FK^IMW<cquJ1CB<~`JpWHobKOBL0xpb<ogUwin={TBcqmc1%y-HZMyV`+@)ZeZdUJ)z<3ySPIzyg;pK|7+H>`w0epj$myY)BWC^r)P?&gBEZ_;WlCPxK(@Sa~t-L;$1U^ACa$4`23bk!R!o4nkk;KMEMJOLsL8;c>}02h_F4BuK05S^~{Dq<>YY`&iH2m_;YiSuzqs|=bvqK+{kDbz-_R9dXf;6F!<t>ss_etQd{Z@KE7Dp=i;!}&HNa57rtWWPOKt!U{u=Nk}%Dg^pyynNpBP*Ewl<XC+tUfXygY){_!zdmai-|7ol=f#aYb7gcXN&^iy%qifX^j33_y7aE<LbOHm4VN4AQreZYkXU4|6X#m%#0Ew6|9Ydv(ZoM@l9'
'>>j)&sm2>S*pvgM1bT}Eud6=@CUX+&JyCDu`5<j+tk8ZFRNSEyJ>lpOYtnnkmK#2(yga)1BwW%TQZO1KZU-&-cLz?AeOo7Y6i*FXG>lkG$4DcK109wN>g)4Zd<>a9gxL+4eUE76stA{s(o{G8$*Q;E%{8*ie+e)fvr7B!8FPU#)C**@AKFJsbYW9P_DR-B+sLHKIY8zj7fdd|FVZ<-KFAI!p;EIB35?ip+N}Rxa^=r4^Cmm}Kt%$=a5*A58aMYhK3IO@;Oxf$3GZup^PYxjwnIz_Y8>Wv#Z%x((E4axum}k}xgm*b!22;2X>MO1hec;x?saf>d2C)6e!apIM?bs41(xpX_3z1mc=y1u5qNS)LLPees>HGl*G){TkB$sWHXtgPfrTp(mBbY%vz-j&uozRit#F)cYJOVZs?84jTdRFg%T*o_u5$Z>QJchV>SVu<)m+mUBNrjREJMGOK?$<P(D5=${RD5MMzup&e@IoAWiU_UxT##39J-!@'
'rNn_{uWR`Luj|?HzeOp_Q`eu45a%ro=GV*)(3aZI!&xb|P3W!#<aB_oVxwU*fnZP8+yJb!4&FeCy7E4M9SK@)q4L~vC^;4Esx(@xgL6P&Y>7J$mYqe;SVR8)Y$S)AUq0$31tTmOX#*clP$EgTK5C3#_ee*hFk2v8nGC-Rsy0{Q25wdZI!Nuhrk|L;UjNJhBCyKQmxL@$w-2;Qh<D|%-5iYR<x}*V>B<XSs#Fag2v-j=>^g{I601N8(p7@Uq#P31W}$b80f%O?h~&6hFFye@rk$=hX-`gEm|UAEV6x)~<0iP=*YAb}Bi3Yhn!0P~%dfHbG3yuWZo_N7&P*dens57vcae|5=ie=U;PX-0{<z;o1R;S9I|C3AQ<7QPuo~8zj2y|IffQfyyDe(VH!-E47h6`TH=~wP8-*{BjsNWlIePBlZ(m01hq-_ae@y!4MvU=f_Yc3gc@7$b*F*R3;?hI;pK!zDVX52<1tpqqrBq$}ov=-3vyv-(-zq+)'
'Mxs3)8fVRvo5$Y$pFJB@c(xv>+#5LV$Oq(C&iU>+f`NO^Bj0c?xsG_B{(fCl;-m+|t6N2&bmh#sOsD$(X{aGU=RxsS2x{<a6EM|4scnc4uLHTeEXUHssn4jdJpuBoB>Vs@6J1OSsRwqkvl)KsHXMSqCwJ;P4N|EDin)fBn1QfX<%~bqf*wbLWPPemOmH(wn+t*0Y(LJo{XH%);!k%+HaPV9u==+ZeShZH+6N%9_1C2ZvWg+8V>W%}^x~emc$fOeg?y6p+vg-A?KwPB04k3`r8_}x3xMypx}0I!OBj(uPj^4vDKBqwcK^=H!Fv{M^il48u9p|sD+f;>Pu`<wKYcwb80xl$oKX1VU%%v8%(cOmPQqr)gM@+D%Z({qxS|i4UE*Dd)-FY0_6f3sa8TE3TeskJN$JUznR-^Zs*==Bh#+A`@Ut)zTNb!nC3t?u1~F|NVYW}l=OH*Uy?Qz=i9X&qif(yZGU}2^rkhc1Jfb7x9Ay$TI}uunl#SaD'
'DmqWj%pWpg0b`bK1L4<~q4f%388rH`kD>nviL7Xu9VHCQiV=V~k!$KrsA|V&pej;;dA7<<G~^Xna6Om+8|JPF%#4-Bu^h21U3Q*T`nn->@szDL*$cbIc*%;)`?Q{3VYmHoKnKp_+AHwt;;)M7q!bK9qu2^f20iZ2IZa)T@sszIC+<$D5!H&{44W2Kc5#ZTIUPh1Ji|{O3RrvZpC+&vtE=WOGKWPf!emAlw<Y!1Jk8)0U1kvTaT`y?Ed<ch!!C7HE<pk>g-F<}!ARO8ew}S75MS1|N`)uV{nb#@h6s02HT?a)Pku1IK@8I%%(1nIO&KVKPVShb%tEo=b~?$&vPmWy?MjSJ8RP#|+=a~gLms&~7l9o1GyXax6=KX6woWodmJric9jKLqIvC{?pq%w7EFH|Ov3f3avVa1)cB7+9iD^Oyi3w65ywUgWAVAdtLo4+t^eZkm-wXIh)bR!q*8&7*mGfvao?|DPb*e8al3Tv_J&SwA`{3}NFyLI*'
'Ty9>zQO~QUL{L;uBI7iciuD-cO@j6Nmnorat<h<g1pig3WoqCUF2{jje$K^?-yzZj2z9zLF9XV+0XMg*6AJts$O-chgejpjZXyOEBIDz$sRt|tG{Uvu2_Y{mp30O}gY2htO{5@pRvF2B^i<0uWZ&}wtw-dV>+SU4u|m{b*^4CZ-YqL&9ZPg|1XsjewscOYpPrX>R5i9b`4w<tfG2mIC2tAw1d9J&W@)#^k}@49(JA!z;h#FpkpP~6U-1l#o(pG^nCVvjs3Koc5e_uqGY_Aa7YZ<hlFggX6hs#!Iaa65I8JdtFa0`hWH0V{={XM{Xa)<hUvy!l7N(}pBvW?^GbFObjnJQ*P-ts*R9zXF#-}|a%SF)^T1rsf{70u2=8X32qdg}#b%HdORT{42oqZ~v&78~=0%d<+vWm6=f*<eZm?W(M;@F1P5f1T;Ru%?mQ|J7%^9>Iv$PNx#Pu1XWsGvKi=%{Dd*Pq>EgSrNer!o<gsgf(oE0sZvuR1r%'
'P4BLasHUBV(3Ym$vc1s%;>N0KDnk+#rc_JtH$G}QsPREW5Qo&{&4M7A#sy72boMk^4*1Bz{dH!fMZlwDB)QDGJJFo1x<#Egi@9z^_Nqtb&shlu90wwg#c*d%a5`&MINvcieiUx=Q~ozgP1+|5T1|kh5j-~e>G8Ob`BfL(2V{nx-4gonb6mGkdM+WvlP~LhZx;o<XHuPU%8#YIv5Gt(zUjwt{ANHJh~+n^Oj2gW<TjFQqOYN5pQ<UN02WbAxxK=nVmJoYwgGwdkU^I`T@6gGoUKq3oRX{D;6Q>0a=}0pGjy@KO6j!FVwPEOdO5<FYD4H?J*GHDL^co@G8W7aTcWB)R-fb|H!-%PHt`sd9W%H7ML_Rng}YmB8L<iK(wI1w7wvE(kFYSdvPge=1^IkJ|7;aL-VMSJ(WiYQT@w*uoYr#agb96KGbsSgX^}I4C@7j*$9`0{CKzxXuqGsyS8>G}WJwHo+b_ScFukeW&Yez4V&}gl9-pre&sWgB'
'pGevQZMwRiDmpSeTZ2L%jV>T^@Y=XrwLzKm?|%PTz*Lgcx^eM&SmcZF%o0$m$mvFmyZk%lp_J-QAaULcc(S*4;47s>20@@QI_bZ-J6aRmc9M%EHsKe|!BvBQE{xm#Xg7=!j8kEL*P}w->QD`|dZruy=B$2BiHpe6a_`#(+nV^l_74!bO+*Ef;55KtIVcX`BGd%;ukL4WU10_*e3B%OY`|nsmqa|COcm^O|7&FvSv#$gg(JAPD?UN|Ed6udhhWW_zm<mnIw|j$lA}B+oMaHV46B!{);XO$K8}-mt%jYv9lzm}EsQmZIJ^VP00Z}a-jZu-YmK;Y8IpR_RDl?gXrKfpQ<<<t9<!2+9YV--G<@nlx-F)`8KF?u6D0FsvLeo_0bkZb1wbtMve#_N8fGJ8t;`h=|CQ4pi%#lTA@F@N<*dYuw%p8U*g?zjZI8U$bVjG#R{B9$!OB>hO?K4JRh2HV?Ft1G2I<yReuFvohc>i%jb<~Ai1f(;ttd-1'
'TWY@}jJ2Imlhk2)Vu1cPon&b-F+P@>lgzO;Tg<j%EptbA*3D4SN{C^Cswo`T#S&hiW|VXB>#~o^`=Zz*w4ajPs?u{6_TDW%Z=RDYN43hXr-)%|e1*TvNWgXoiQ__qP!=<poUEF+6a4VwprH~g!^m}&D+G*q+ZTjkv`n(F$>hn+Ubsq?aqw<xfQZ$L?*F8u^yWEr8I?F-Cr-T3GC{U(3p2Y&Clq*9LcY$sD*Bl*r0j3qF4*->GNZg7f4ld3orktar}b?Csv0!%H|2IzN5${c^=gcL_j}ZQ;m{wWxB)$ZL>K*w_3LYtwiPgr#)&;8Gvg6grjF;nmi95B2{z=nl2F-{z<mEJFg9aW-hha@`L&Yay6F#X*X}`cNIJ}RggQG*L!K>!md9B8G0hv4gx@@^;365Rg7fMZ49<1OMkqr1>S7Z1E9DmVEUa_G;T4@p2ttmfwwnu@!<fE=I~UnFQFaw!`V)pxWX*?Opm)Bb;5t`j?N^uW)d4>ahXTwT'
'uRQywvbStqcmKRo*G33BWQp~1Du?{IG<|Gf?Xb+1_MP__b(uAnxYI~}wtYJl_grb7o4_F9i6j?k1$vH>yDJ1Y1HO6=Tutq~OMqlls(0-bO5|`ht0M!}?~^G?s4B$8;1F2nk(*TIxyOxsJ6RER(7kv|3!S!bL#upZps&Bq*!f9x#@{!{uc^9lIH+yqN?m>XE0L3ThlICMMDbJg6Yl9-PP}>Dbdsa=Hgs~*jnOV~c~#z<uD$SJK^@4~^~27(92p#q$;`>U08eB0WKV$`<pbjK0s)JBlX(v8S$Y@l`{3`N0p+&2ITGm)!Bi?56VKg(sRs-2^vu^--lD(X&49h@RU}Kgn!CD$-M@W^bt>RS$idMqR#(&!IodRe?xEf6U9TOQt<H%d<6OS<subT?vE-TeTuI{ORFYFxn7&eQa8_+F1y|GMZ7>w)D`<05E<_5Hz#Vr_tlgGu{(Tb~v}@~KtzDB1n@ybxr=f3vJ70wEf4P1hX0q|r#2=Cy``85g'
'xYO9-cVhsoQi*!=!}{Dgz()MX)oi<?bd9WRv{G0&x<*7ww5nPWCIl{f=x4EvX7f*TK5p(dXW@hr_Nk~M6(Uo+J&&C`^UKu_m=BzTyoB3jR*S`Dz}|yz_N88$l5P24!omfU(nT{1SyoNh$W-27am@i}n=3SkSVK9e_q?Fl1B?}=570jZ4W!OG>d1tY)>}w`x3Bw~Ug@ca1~k4h`4=4*YS@{Q%VL9KA+ezT{Qe2j#)Q|G*cv@Aqv>mQs%=<<87p8U+-kn}*kKH2<H0zr`k+s2!aa&2sPI-_)lZhm)Sfgi1*QWqK%<Q<NZo>g&dofAUcOr$)*bX#`AByRsW<cuE$M;4b$;}jbsHb0(pQ{H+sa<XFR{0k?$1BrV}@iTGje7y-#_jH#h;vohk8kc%NBT8X#N0t14|=u@nGv7KdNyWIojCMml}eG#tLvU;dLn~aq(Cl^Th_UmX*&BfV$@!zPGJ)ybe=ZC=MxOs%u$Dd7Dr6eJ;%g<6cG(!A@63'
'>d!ehFr*c964Iv$O$|G4&LGiP42{Y;t-ZS>o<m_3yzgCKnc`<vtB5D7k#_~Lg}uPD>Mv+fTCG$X%znm}>9g2hhzt7@X^m96!;-%cSlKLyHNXIcaE*l$##E*!oN$K&;%iJqU@mP?abPQN0od%j84n?7_p#O0;+ylNi)q(inJ$-*r%#7kN^~=?<WoK5XeE<9`T;7yhNnfT;=rz!iHhigmqLIpKp;NbYxsjBXrdjpob~GxEP!o2=^`8Jv}flvui;O;I7TR+O8rjAGuM}eEQHN?F35$U^o)CN{*W+8{t{2t(&h64oujjOpLx&uOpqzBx8_7ypabb+MLfoVC>665eQj`90k)w$IFv!aGbX`IRpx%G2s^8!$~^j_PxZnZINXud<)FQ}7~$2FbxU~5FUQ=<p4albb9&+wb4f_AC_o|Ir?|#Ux6rDm=<1KbbEm6|oK;<AH;LFuH<c!kK~^!i90-Ia(%ZoW5zxOorXhL1i+Oki4@Q{?PY@VAP~PYs'
'Z^3kp1aWHG9d4!RFj>(Fa7>mLgXx_&dJBy_meUOjg(RHrK{wj$*^fT<Q^AXA8emG6X^ED5gS}CA{KGxMEn2$_+n7U|n%)}HWM=x&Oz~4g)mVYdg&Rk%xJnn~5Z1RT0`2H2LkMWN`zF&y6`@(yz&Dw<Ub|=hGn#^}h!Afp_BbO(e+rW4x{Ffm2K?mVXzv7*@Wyu7?7HjRkoaDG@KcQ85T7D~2%yDND}O{uZc_RH$|&;N`L&dGN4ac^r1}yUvx%TWByACMJp<Jt6x~q;)Fu0wZ4~qno^jWN<OQ(!_Ay96SD#FGW9l#7CTl<e1oeAi78`YPgoiFt=DXVrGs@wcV98bz+TOp&mN1RZ(rDHjxy5rrA~8e@jjbPH3<teA?7w0<Z3+G%fsAI;wnqZ)^cE#tJgk%LWdiAHTd1s<L8B2~3rYD~(-%2?F_JcH%MAZMEwSF<+p!-R#rkJNa^G0EMk8o5Yac!FB1~vx-Bk<);pCfgQY4mFNCN2a(DT&3'
'Q97ms<N1F!Y?A#5xUF8Z?3v=n4+2zo2H55z(=M%Eq7pwpzc2G8u-vYWDn=YiZ3$@V<&9+hCOy!JyqxIEoSMU)rFLKH$%w?H7{GZ^`(MA!yt6>71IB^9*XcvJ5_+C#yD)$V`xPQ*3R&<rFkevB-Mnuh2`uQiQf71f-UUDC5wsSy7KmzN%zk80rSe2l;x3waa&_SN{vc6e?8;_`vR@4bEto<CmpNw(Y`7bG`!59CJieG=vi2kL=(#c%hg}hu?Q3hxe*5+bR|0dJ^i=HBm31J}#A<eZ7Jk*<!ae$rCoN1bBy=HUtk-EMN^aC9HQeV_zyJc1*u^nlR7tcuj#|_A?3bQSgl--M7u=m<<N~P&bEfXS;a3`WTS-b$D5Jc-xlcYKvL;|M@4#4|H7n!kYqwTDRgqD^2R8t|%oHg^l}Dx=xCwIv9K7}=uhq2J;hnM#R*(%q_wRd|j&#O~umbiwG=pq%tC7*qU2B5}e46z8z^BCX^2inZsFIyWyHvh>'
'bq&pG`^atvoZwN_-`ZQ;-Z_QRiY@#zhnc{`fj1NVx2HeIP^^@p^no5|&%oL+Ye~$Sy+&0kpS^cP`x*m+a9Q(cPSML2h)i^aVK%PwvpA%2bVuMh6NnA%S<}y0J!?T?the;P=%!LSazz#io>&bzC_Cd+sf)eH_a7P8n|hW+MLe-32%>y4CqR59^BzYstDh9cKY^}Nh^EB4Nna`xQA`aW0c~`9Nj&qrgR=iD@A6q-md$r|XtmjN0k`hrz~SrR+?#^hlGi3y4U#@lGN4QgF;$OQJ;c*qduqO`p5RMjN>N@lH=%I04%(EL@7b4OuVJ{tbz%Ow)I4n<#aXjaZg2-m2ahUQXO?eg$0Qgi!d3;?;w){sz~sc7KTrAIIbqb33m&4bov(q##JNF1q4pt_=NvPV75K-!II|rp4X83)ppZqF%DslxFqy3kfU$SI9Gz4$rn`&zmJW`}i_cJRra<4h<23-gC5|S6^XWEpja+c*iV)Kk0+R#T_y6tgzI1kL'
'w=So}{Co4F9>j4_j4Q=E+oZuqJ&ETgW5iYtK_OqbAU6w5(_+WJ*hHcWs_<-;E!XVFpYXnL{}A53ihZHbm)Xfk48%=m@{PVpoZ~q1F|bTX1t`GCfg;xMl&E<t5MvUixCNUFNvSdzv9*8$@Gfq%BKG!Iqx+rdulB?7N1OGe8C;27@xJC(J9^5)$96|AeGQ`HctgvK7RJy0JvGg3R2V+aTeGrWKqPhu2-nYb9RUlmu8Ts7z(jw;WbST2?WY$YHyuSnVb$Z%jW?_WG#-{qOYk8;P99otkDxxB!b-gIC3hQxqrAGXe|3r&r=(rl%GF1t5LP#7a~!bJT<E;k_Kg?nT4yXxrLaYpj-C&k2O-cPsWr9eVDM#TVfwmIeJ00?b2+5^s}rNDizpCZ$YOPtlITNG8S-eu;n|>~v<xx-C7_16>c6UjSF)M$p~wxDiXi>TLv>>8iadh|)6P7>nNniW3h%YThq4N=h5Qg0@k<`4rBcn6GxuGfm)#J8k3Ll%'
'mOI#{hr#SE6gL!?**9|}#YM{Nh~j*=N`{;(TpK7~Dg0Gzamc?*IFq~cjLzDOL~Y!E{H64q!l~JE>DCG{M|!Q%4OqXDj@=d5R6j}*F54o(Ud|pQf$Z$tGJygTxa=Hjf__dO0ZbjSD=Dvw`Fe`Fr31*2ki;4zMc^XRV<A}Dk?4q|gz1jh!6vJ3+}=Nyy-U(c=FfG7XT%;S-c+~TH!XA`$Od<cSWSu!)NjH}>aOzd=pLCW4QL1Dk|^;%-?n!XtzX#=6Q3_=5ve^*>08`bM6}ij>lVw$YI~Gbyny_WdZF3E=_RGY$tu8}^uc9KZ@SXmAmd3@#uGh?(R>{%NTGPP!0V%|&A<D#t|ZLB&y=-0&49U07nsNHar||v6R-^f8siW(gIwXuByQRs{>2FslHl52-U%yQ=Um!@mdJ8!6!^dSP-cKGOLR;CCV&Sz@vsP4C?lA78YW~Na3XY@u=tT(vlaJY2VGh%M($*^<*v+sz-Dp%w1PyEw%94VJBL2d'
'u3YxWEpgD)Wh!|h=eS8GpxUf}Z0-KmhKU0n#NPkH!>Xm4>UBF`?k9>yCD$L$vNPwCT~HSp+}3$<M?uR6#b7WcAc=xRRw<gnI|yr11Df+U6Fkr#v=A@k57P^pQ<3wiRk;a9;Sf&<mE-u>=;YNVr?=TxTG!4#=#lI~tR1=8*24AZa6%zJvZ7E)FNI&6NSujBz9RDOI4M+~&9-W{ZdlQfF!Avx!ztiW(fIJ*rei9WI8P*><QKPK*AO^^Xqq4Ytz;BuT3=y2O{R>{e+erR82O&J>l9CREE{Q7tlsJMWYnW&=ZfyEpn9>p;ib?GDazadN?GxG?7FBscXM!~L+UD1Rq(=tT1}aeYV|*xTi2g#u$;`(vV^u_KGjcCC+zXa?_JsZ7w--y54gL{C1Mrc?rU3wkc;x(Xh2V?#J*S65KsfW&&TX{r>zU6X#>p)`Tv1FNK%iO(#|<R!+DU;82kKSXRK!Iz!e8Bj$+7Jr6ymBCEONf|ABW2z|*V)6}SNN'
'0=7vAJ$6lIuGOY2XM6pq-yu;knW8SrE)uosC*8QDVw2wi@3JZl9=N42)->UZ{`}{vKZUP-#aQ^|%hWY!ZFnzp2J*s>n0`STV}UZ)oh7u(M1IL2UiBCtbFf2EAzq@OI%D9>R*Ls%?k$`-uLQo}4j5(VX1_cLXK$>zYSHNEhEq=Tk^K%Iiq&cKT@nR`NQmC(3e{xMD!mczd8EwFiFWT>+wVPl-C5LpS+rbtCd;NtdP}<j`=zAl4s~hL;?<=CSAuP?c&T2uqssgFe0qS$y!4%r-G&o!FK8(tLVI$LqV4$=D(pudZgQo%FBu3XCv#K!2@{1zu>9WBVkMT10IYAjrI8-h_HuQyIF8O{tY1*)<?zKGAlLgxp@6eunPyr8vAxe}<gP+^19m#c!*^XyaVzVm?*&TG19A5FiG7<WwnL3XA;i&ah*A*I`65Yx&S_`jFLYyMsbOwdHi|^`uPm3YFF^zvFY?Ab$TF2+V*J%GS^rF=S2h2?!IAR<@jv&5'
'r-tpq989Ywg+{fC4OPJw$Lvp!_&so9AcTs_FTkCT{;ur`FP)Xxk+cz5uc3+pBV(GNTa5#{P+(NaFvu`YIoro=I-&0R;ZjEO9-COye2Pf_myN3ddrW8S!+Q=8;!CA2K|<ty>*EtEu^Q`%Wm$zlxyX_Wf#tMT8`1yam?kMa8*7@vRU!~SlV@3j0sqa6g5V&Qaenw3Z}3$tKnQ~^Q&dQRgi97eYb<@I=_7I<$ezinLpKp}sJ~|gkx?5M^&=rx!b9db+y5JWW#jg3GDo@qbg-sXl_w)C({ewO?l+HZa<b`C4m~q9AJ=D7w$v9ZDzieR^2#(PbLg`9w+eE?5%WAn!T8oXuBV1iq78mu9k4In1!-DU{-F*HxD4bKrp0TIH0QJ{%vpJxs~2YV(V|_%H@{s<oe4?B*LPk5WVztU005uYH5Llf;X=aB@W+#e6QN$`%p^%`fpp<B7}-%|e8P<ls<45BUJ&mJC7SCIdY(?mEz*L+0E&o5(YXKx4TO}A'
'&18k#z)KHrdwT-&N5S9DpzzhcOuC-n`0zj|+NvD9r|KWyxG!$DX*PJW*lS{{XLWUv+Y3@fNR!$(GY#EU?h{fR8NJbEJ<F>4Ogj<A1@q>$l2!Ln>hY?@U<<x#>XDYA$n}$b)py=DD&>)J>)bRv@MmAxFj~$&^o)mNCvVPH)>AgZFz}r?K$`G_cNTrFEJ}jZ4OQWR7$T%gWu#REQWJW~*JQDhVf@K?@PovB{LSbo!px1_C;m_`Ur|{qGZH?rF_s~<cG^3D7+(k1x5dzR!uKlB6`O(t$tHVM<I{)`|7l7*3!LQ=rIm@D=@OZocSQh&;gDB%m<w?{ASGDQWZA<%C}R9qx>S0HyE?XllEMRM#!@yDgA=MB{8qae+BkU1_Ic+$`6c)UFAQ|9+~QmAdUnWmmZY}c;^iKuDI}wdo9I83>E(=uF>et-B94nTv?$q=5+1hMg~d~<mWh@x)Y@JEeEw#8iVU0vM!ErL4too?60l=%8iIJ)c3UC*hmUKf'
'A!+bypBH?w@wbtYxvd7Bcg3ilfh6evwW1G`gPhOEs&*8ti00>N>q3asr%mY*XO=c%R1e08$oM%emL(L-tC@7f4E9`<!Tguvy=i_b_1FJ{Y8W|5k7VhkErgpwhJy+DB&*<VueQr{rqmIoDyXEyS+I++yFQsxXCDyWc!u+2suwf~cEs#4TiHzCEK}4u>jK6Jl}a`M<WJ1XO4lc{yUzq-Sm`>K#z@{Z2f9Vn;A4hnG|-GSa^K8CNHex-Q2ym3m<joL5kUxIyM|&u!0-9^&NsLupD6*VLuw_fD{?}0B1ASnJd2)YFFq{QLg{w!hJ@S!{7SEaksvgakZlOotGw}s0R0v&0u1?RYWU!5_yhp~r}kUlzN@uNNjJ};=DHYAUYTg%bzvECs?47)m3xdP@RMuDKi!DN62Y6zaK=2|@uSIT0djA{-UzQnF+;a1k~U}(c}sdbjE@&o#RRt>3su@?aEtZH`&>cdqdkY^&-|d%pZbFOX)RCCU!mn!tZ<&?'
'YcCp$R@9JK?F)~VFf@dXNXb|unsV!5aLCBWp5tN2ZnNyW?<)ry?y-s!TR<dh`$4dL=p2z%gK$uGGSFA~!&(&`enp(hTC}arrInc!F_XzQwrOYN#w_${v;kHh;Zpe~K}{f-(V{(a$O!LitWYk!Ct$;51rX+d2k`AmbcJ!79!`FfnY-tAtFM#4l!)Ks*()d|kAr-jp(`u1Gsdj;DRwq56W5O4)NGwkXO<)|i-c$lBf()6qA`~Kn|Hu=I4+$loY|W_Qt>Pio>04zA9A((hC|#5bCr+`FDUin5wu&w+<sEbqd<2EZP>U?el;8eOo^}jKrB8Yq=hq$4kEcdcl9l~`Wv<!dBVOWUrY#t5pd(@iQE$A`X<Sz13`sk`3!rb(H-7n-1Z-b<@rCoY>E<j{fY7`#Gw;zaNIbUMjESDw3qUOb!2LKk~R_{w^QjM$mh1+Q;xt5=(#J3iHjVl^YNF(=wT|@dbj;WL{wIgH0GZ%P*%0^w(2*ePnY*JDf(hM'
'`Y1-0X0;VUpy$pQ;9ZA?fT{+i(~c5wFC-;+&He63{J$t?(;}RQ$mZkc@C#QumE$7Q14Q-L9>sGM#bndpWaL7{@l-cvC%wD>P3hIEtfHUewd1fl<`V2EDuegKJDIh$Q^g@=Z8~BOCqmgEfA51FpVnVRLu?C2O{oRzlNVwX1SXv+kY+^qnACs_PJi&`=I2l3)Nv<uv(5`u_C~1gO%!CO0c567sS!d{mVfbAh{57pUGp`kN6GFlDTJ!T6PwMZ$LNYT6IcIG0e^;Az_?fo!r^os6@i{sT{OAz76J>Bh7ONa@-~!C1R^`8jy}@Pqt-O}&B)?Zs*#=udGNtjoiMylVXTon$yl-S7um<ok5vZm4<OrF4Uz|4O9L0qDc}8jJPS^8xXx9B8+tpwO8K)uAIa;@MwRZryvpE+ys<Xd^6;8-TA%Ao3*7h&)IGoucFv=UGG{=&6aYcfL^lYwEHBplfKu>^<}8JLDQ`?PYUUr@Vi#&B`;5>5kS5Q)pAY`f'
'*krUQT}QaFqq2QXBS=TG-qNG{;C3ES;)x+a1@h1>;)1lfUOC|lbjjc?$Hqjwu-W;~f3(otvKi_N$DChsgFfvD_KmiP4*rA(%#kP8{(j<keR4>>kpXW%Dc!l}<?$^6AkXg$Mc}5E7}Je1Y|07Cc^<@*9m8Ftnhk@<A_?&@TuB^{NA^dLg#@Oq$(FDx4%#I%0-!zs8!3ssOIcBmToj-G=$n@%i2KMo*6nALNy6o*JG!6K9a%-J6ZJc+*QCCFmx^y{dOLi#iJEqcwr{%}FuYFOJ^_%C_^6s8xIPpWOVv9RD_qZ*f&E!?UCc7TVCne#7MOw1pSE;Bq$fsVuE#jER}8ueY))DVrf=R8YQAS}^Xlzzkwa<>*=(spewRRbw&^#L+y3$2UFI^z2+-Ku4NQ9RMiD@h49PNIWl*((G%Uv>9<=s(*8%KEXyO?Bn1!t$viP2^#YS9vvB8%HdYO*$;KiT6kF4xL1|U#T#+Qj21g<eVnH9nxYAjhv&UI;U'
'dXptzj-Oq@gv{N(xH)h*84<h)>g*2JM01gcEI-23V6_UPoJPIDLEKFex~gkGId#*jf-U;3N(>AYwE+4)g5E{;HnJOP;m)y4l4r`Zf%CE5`%R<XG=Sbzu0Jzo)$#;^^)2*&3;}0Ps`Yp%Ls!xq!6i78_lk?s?#%+zs2b2NUx06$Q`s;G6n0RA;*^+nf7!N&2}Nm*CT8&-u*R|3;l2|JM76O4H>e4LD>^JgYYUyC9U;|}Lwtj-=X@iNcHV`vIB%hPsFrmya&(udt#!D3uqs{R_M&KfmIsJcXEz-Fg+F=;>p^)wt{Qm}40UBJ<Bttiog!!{hVD^p=YAeKai%tMznjwqS&(59L?q|tTt*Y&srSiVjDW$#02@4A$j9J&q2riCTP-VMu{mOEkcJEWH=QzoR?ZxMufzZbS6RSajR7~}YaUu9Op{W>qR0b;h^QTIGnX8h<Vl=PEsHT*G8^Waz!z$RNW+mHa+hqA82QfWM?DjQ@6#ASeZ}w&%wTHV'
'4Y;1<NFrj55eB0h^W8$ZY{Ysb3`(Q!T(Rbu)cGSMashv9st^I!%fL2d?2LEc$<+myi?C)ruqfOXsM}b)%4A11*#`1#-D%{dbS5fxh||7D0~aej@Ax#&STc3T`1u3?-NbY<7i=vcx4si_mFzX2i*<Q3J;6lB++*}3HS+<tfD>sOSkduWfIu0NQb7U$68gGHfpr`3eU1@FZjfW{mnvP&7sN;we`oBSoY?FHYfM+3wRt=&<!_N1oB`Vfz7Rb4rJi4YxLsrx>0pKp7r^>=iDm%hatzh2+)2DfAqSSLMZ3;knTPfCDD~1eg*C2It*#X)y}hxVHKszS?UEDQ;Cu7)!BH#%8HUD$F1CW_m0i_}eGL*S&e$8#5!PUa>RZRy8@pL{L4;g#@Xh@WY^UsEkFo8(;0%b5O7W1jBX){fZaX15HBBJ6Sx!%(ArReHEwTNZh7Z_@d{zB4voT|&<vs2Ujepq<+oEJj@jq4>%Us>C=`q;#YKD<vM8|r`YhsVY'
'D`w<!03N2MVu2T7tw-(5&N88x`v_o?AIg6?#jj0T!)|sShYyG3i>=J659Euy6Tmz_=Ld@H*6@(@*V`Tx-xUGI^^D!_d|~J;zm{xo6-ARM!RB8~@XhU97X1992fwos-H_j6d8MF$=nT2`YhG}WQ=1L2S~{S&{_y;w9gUJ?ruQEMgIrPq)fOS8;3X~su9FyPsZb+?$qscNl&xo;N`TIlGLAaymC3qapl(`sK-lq&u`ijG3m*wJec-4J)Lf$qYJ>cq=VrZGppY;R=L+6+=ogmfy6~oV84e+Wp+n7X2BS7-gD!KbIEgP5@gEbg()i7g<32C|)#oyK^FK=4D;&nerCevSNB2DB?;4e-y;#khS=1FLqgBmswKjt0A_0cTiQfWi=eC0mv&DDdg!+MPjP7lCS*ZRE1B{zK5C&^CrR>H@9gv1cDd<6;?F1$D(nt(~KAwM&)e_?<dWd7`{he#|j$aW-`<&N!=siJvA>bO|qQQO#8)8DTC*<kla|=x#'
'Q_*Xe`2Pt6d&+VZM`&AGtu{kIm9M+=A_=aPn!c;IqT8|xobu`+<EwWkXOb8AxzTXq64l^%cIPo}_m<3S3M_o2Xx%Pet=~2tC+ys*eG^Z6Lp8|m4fPifZ!km|*`Dsl^LVES(;P6}mgY4)8o(vWTz?I}wG1L#LbXlj)=NRC7v5c1q3$pL@jbf0f73s{SBzw-xRwnCT_s1{q65}Kq5o9VPA4d?V|+59APJ#LQV1Fd>f9{xbT6?Kj5Tm5+-+(YBp!X1AKn-ZpJ|bH*VWc;(5_U|>jG;j)ECb$2C-fYmGE9`#VZdDz8w;fOx`6Vr+4BoB(IKMent;1O^vT#iP~B8tnVwXD131d4w`zS{bslLt-2jiCvg0J!O!7Lx+foU{$1%=Pe~(LgdY=~8Z`1b19$XBPE{Q`Z^8qg{hKx0CX&PwOOUue4$GPPUjMUK(#DfNmOCSG0uU<>?}=4*JwOQDV4dF^oMEwJ7&p25SoVSaVdoYOC!&Uq`o8Bb*H>^q'
'J6$I(pyCTFc&$94)_0#K0c5umi_6Q!jKs?He^aWT<uC)(BhJUK=|U^G-WC0P2RZHJ)xl)%`YN=)pkAWUzrDY*N0-~aw=V|ks?6*xX1jHEzSw1mc|f1M_{uTtS06C5Uiix5my+bv=bB<AVZhSG4;gZm2OsU%#$@Jns%F$;^0vXz-BU~~<4FD4kn50;3B`j($r3`ez_yK^S<m`fHMP51IPtl7zcZ#xkhM7LEJe}XpjK}&+RAHanN+TUPn*DW7L1)rtjSTJtw0}(G2ZHx0qH-|5|+hqLqTbjuX&vrIn-?8*V7~~N-@_%aKJ5qy_jIHv0jinRdCk#Ug?2h?<rC)ga%+9FtDZeMMZoVB7t$wu!LwO9|d^mJ84u53QNERKsf-3_4GgQ+HH?hmZB0jsa^`C@=dh8I?=2k3L&FYRaBA(JCZ|dmyGHvIkuaNsU)Bgba4!0!VZq3)*2Qzf`bAI>_^e{PJ8R|0+xf;!3-jgQYeG*3A4T8rrOrV`w<oY'
'C<LZ<TeNMo_Nw7k`|sj6xpLWsP(YZ=aA@D5$1BtI0b4j28A<30z29bowUfPy$Pl%zNvRp^T+%NI51NZ1ji&efocD;M>4>R=qBzXDk_bRJzgE%kCnA5kKc`RUB+JYXV|644H87bqwPuOQC3Tu2)}o?dslGodPLx@(7^CpnSGD?yzj|D3qM|McW2zUoRu`42aovq1%$}(#F?>Dvf*U|GbtR6GW(!MCmKEW!y>In5N2f-16lW0KpD8tzTy>}-d!GGAb6s|}-@~Xd?0U6TE^7kC7`jJ5gYU$Befv2)Amv2vJG6J0in%vnO31!RgdRz<$+=+q=>n%pkWmD%d&~>!gsw(t;a2?R=QI|T!ovq7fhI&GV>I3>p_qpQSmX+jU6vkyDQ@sssxQ~S;pKE(q1%NTjBN}P;+wrg$s)6hwK|3gQ$pO_B_`kXnBQc3$b73?ch#=8gB?AwxULOZVZpvr<=#lvwtw;H?5rk=ka@C+P~@Z@Dx@FZBj)e_7dJ(O'
'ZTNp`#wFy&wMG1|Me5BL@AtptEU}>0y7FQ<1>drFRhGGgeJFSVf4-7!%?nprb2fj@XG1GBbp>NLYAH?2JSct$>qTmSSZTuLq=hPk>G$xx8HX`?&MI!y)fAVgpGm1OP}z~ruUh3!(_yy&7kl|7Gnp{X=n6^AGNs@oZDWU{nx;WhRP>x&h$&qq?U-c{aY0`vCc;kT5n<_TA-&t;U=>|sf^E?E`diG;$^Oi~W%X}O`jFtS+fN~*FMRE2nIY?fhw?rl?RWwF4?<5y63T)&Q^$+b1$lWa4L#0wl=%eac;_&#u~tvV9V?e)U`~D{-Hz+T=c|XHSC4+W#7#|I;#@js6IxtU-i`?kMCHWuXJy?gFsmtArkc-wwDR>^_ssZd-K+UDqNh~o@>D4Q8zSGjO^cPl+1YFYj0Wzx_KNWxaXIZK?%xmY>AruN!KvSadX5BVUP_n-`x&Y|nN2Kmt6DvV@~B3H*=Y@vVTSJU<<RZF=AC~LtCkrN4^*1uX-5uK'
'A~Y9ghAJ8ZZwaP9h7nA~dUL8)tdL3@G+Iuh7Olu65g!%oQZ}hC&4DLI)OU^>TPbzQ{&p79ax2pI^(Fw>;R~lHYU5ry^Y952(q>sEQ^}EmreNBpDdG4nLv}<XES*Q~mG~&pFxsy>uA~27=rZEasr3XU1+LU$aB5t22@DMl#Zj%^8}H~dFFf_RD)H|WO=Hd_e@|fV1FnCxjU6#iHdO-_gp>={xbeCvd6l01FRA2a^-ut4EYyKkW#VI-K36Katg`h+4W=XB*X-H|BY>`uyKIuh{uZ+Rq4@M+izG6*>H-Y%vo;UNJl)+UFt*I!;&Ppd<@sub(jk-Hz<t;-Zc)2sgH*(l+7i`c?*vh#75h&kUyJN1tK8H{=`=Mn?XK}%bB9bTEAWwnL^iC7>P^<e3$x2-9pev}b!<GpF1jy`Hcr1A(VC5nxF|IyHplsnj4=wW$35X6d{z?!<;0oU;)-|=nF8YVNw-Gedr)xl-*Kg(_vYHa`TZT$n(5TIm$e*%'
'6=e{v5$^iMz_n}^=E841*%xK1rUF4NKSC#dtWUw25UNb@T<sIW5%7|UfhFaqR``ll%aHM}bS>aPszVdwpzavt{4b3l(w`Z%fpht#|3Snt_>#@Eel;Re0CGxo<u?cIWYBehW*qlce_9ftXSb1%>~$mwQ*vDaNadeKyF)=S6aq#E>d~c+#9S1Q_fPrRqQJfczxrcu3msX<REOD`Pymmk-{f;w(1;I6lDiV1u;pl;?k&exd$<L1VR6zE7abWMmCq+2-=hpcN#D&hH-6-COP9mQ_=wB9(?=vK&L-l<7DYkdH=#|{=T(*$kiO;;B`mo@EnO-M{UiMJhxO#z|J&RO9sM!8RbQ#ij8sf=F*VxYfvm_M1@|{GoS~DR_xxjHkF56Iy48Tzs_2OmeC1thbzoD-L~z?Y=SQ<U(mn0ZAcpyYP8f`Dzvj$@Y<z4&uo9OqH<k3h=#;-7$B?Vt7%jxRIcIbnm*1T5hvh8n%dHDQ`7NpMYfJXSuTs%9|5f;G'
'6PzYjPgY|1QjtrOyMpwOD-q9~!Yo|j@cjl@5T&*Mf%Z=Z!eJ?)rqb5&xwyS4hpVP$@GHWj>AcO2fMXwn52M~9%J^>|dDamodWAe3yr>ih&e@r9eRW@)$KN3FJ;c;E5^2t@laH#NLlgEGa0*F6;H}`#ak3MS+6CNAH`5qNZ-PC#+^)&M2DwlkI`lR>5qwgZ0n-cQ2CYq-1bS=~^Z43!L_q?Ay;VA5RQr@pE(qUn#pd4c@3V%7jWAAR54p1gOqt!3pkp3E@(WC{%30(l%=nuzLg5%FJzCA>*!dVgE*P8lpxpUXyj%ic^1yS<FCFDZT<Ob=A={^3U<!-~V{(#~S@tE*V?+Z4AwA9IMB|8;WTXTqarQH*y2aws!+fVETsb@eO2C97g+@u~B-ZK}=i*Y+;EiFKgQhlQzJ~LjkfKOtc=mxfY$+L_O$P<Vfmh^OAEJspfSgH>mH8+1(FE#fm60x;T?BVCi5OfHB}o^9BY3da7pEl>hA&6E05LR|'
'+L?ys*zTILi?J^hL6{tl2raN95AXr-0xhAHr3!@#vy(~^g%R}P5WB@0e-<<ESsIB2jT7yfVbEf`Y!tuTXq*)YvIVXw9yoP=HlHa2%Z>B+Uyq%d@;d+C-vqP@p8Y%u7^p7T?z=JJIknz$D?@-XlPz=^ugI23JBGCuaXaxQqBgqdU*#;Ww@52HIi+nu9D*Hwmib}DB0xu=d_^w&oS_-`2-}+(dT6e#i9;V>(@fk+R|LkEFSSXE<>TCfiGI3`q3?v?<HjFZkV=S_f6B$ysMN()HV&ss^x@E_6>DVG_zlbTqa=hG&q1Rt)dZsO{O@lK#jF`Ipqm&~VTnsV!X((Wg~o8g$44t~pI7{D4V~!K9xxEkQLb_R;;%8_c1u*X=hHdm0$FZ;?7Xh`mg#G)=O*gL-}=w(h5=gZQ4c?ZzTa*#gLjxs0$8xY(0q4GvYZq&L4$p^jwPy<NpoPWz);Rcl_B&GF?vZFl35K9H{UN=t?+V)ue~wn+qCf*izUuX'
'g;L<ycZPL)cFig{mp_nqb$oer%xbn^mvHJkw~@`*43y5L88TBnd8eaRmLt=BWxwhMzwdt0MUa??U*&qus~d%&DqHg<z`w{$K-av5iOQL78(3l=Vgo!5zZO?pIxj*4V>6H^-q#pu=XmSkxHoy}ym!}Ir`}s^4m6g-edsSn<aiB>x1I*j*2z;$h0(F&Gy(i$q;tFc@=zh>r+;d(#7|6|DO0ULN7z(Q<~JSx_#H-W@s4c2oxjZ6)&4gfY|Iy(W9fT%aiq{SB<6q$B*iTuQNSSU=8dK64?wK=Tte+fE^Td~ZUO%4uiG<u6F^)Xq$9gRLvenb8w>W9;r8qL1J<BIBW4U(&?oM61~3nCJFzx9xk5}j7nOwZmj>QgJFZfV-S=S7argjVG0T&8yAW_><?G9BfdHbCcV~F4IAb)K%rwQ0w>41R1pKk%A`?IAJtaLK_tqQSwo(7Q&zz`X=RZzJDp)oJUtk^EVX3(WZ`~^8!b{>UvogeVIzBilbpU`%'
'gU-Vqc6gHeeR5Fvk(6tJBwA+7p?AwDi_HK~FXDmOJzW*2=0<L!yx1)1&OA`JE$V(XXi?i5*#%F5S#!s#QSNvi#V<b-^4D}|Xx)daU-S#v)P&!SzV_#OCU`RzD_;*Dh9M-FLDQ}KW#E!;D3duaPBT<w9^6!et}mbFxHqxWCfwvjz_kBS&+(;AG(Y&5<OG*S7ZsuPyd1iskcIPTd_0fWj`-jptLkBMw&6|S61Wc7AvN5j_T3HfpRs(cI5tb)7eRkN#K~NacN;>mCEEH_hQ&;ilE^-*a&;H;@qmIFa!oFYK4bT<fQSFW2JZVPo31haq@fe4;>M^&Y9(y06Q*WrXdTpq^?$(VUENsEyqz%qw!KiNHE`Mm5#f6py4(NQ4Oj`vjV0yk0OWW(DDFSX5EFj)gN->Tb6$*=$2{}oJ2l(lWjjF*c@4^5^6Xj+bzyD2j);T;CzbN;QfL_TTy?NELKzr&P;@X6bdq4mSl}u$T|Be#X+5>50ZNvO)IWDy'
'TKYWy_2Nb%Ej+(ucQkFCrU+1m7YFpIgW4z?v|VR^PI6_NI$<VfaEXn@4IVwtf+J!AwxCqqLQq07pgZ^#KZM{>GB11gKY~I@=%BxZQDptHoEIV1Ce4$Vvjf%~iyhe)yT4nv&eBmY!S+at#`Sn)!u53Vc0~Q}rNpKjko4X|N&ubDa1WHGhnxJPBoB!?<`T*und-Qp06w}%$)kC-JBwOVTWh&h{uhzeH}1>icbjI|dRkgZ%Ji9RyT7J67nvpyuRVQ@s8d&gVIii`CEH)1;FU;MwjlEFJtEPI#bwtO^ZEG&%ZOL#t`vLqLaBSCj|4V8(z0E7z|CmhM_i0OJx4N^&Y2SA|1U3o^gy=pa4-8H))qdNPOC@W2OJf+xN$zbm?GUDinq)j@z^Qg2!c_@(XEMvbw}zVH`mWj>TE-k%Xbqj`e8{X2YqIETmGxQ8FjsmKg2R=7Hv3;R3qm)gXJjPE@VVVP(WoJ9)oeCu8H;VeKA3%5|fm(i@~t)I+V~2'
'pHpN#cJIN;l^+3N)6O}e5Pm4{-J&}eMzB>-v<e=zcNFdkXMg$!2=yn}(>I|FQsyRDWHy$CWe#1}>U6m_njJm?65v_xlZj%5;^;(p_yD9)S(hxJ_~Z>9Gie1@4Dwny06@giY{%vtuyWODV|iv2hs-b=`Y*2IHc!awN~IVveh<%OU|6x1!W^2xwUUCmOeRp1jBnb4;jJ>4%^Mj2ZiZ{0A2K9Un)evusoBC4MLd#H9{j;Y9$|>NS6-S*ELRprU6JpY=T&F2=zw8r;aG{HYo|g)*Az1SNfo+9R#=xKRI3nJ0l@u4q62wMOw3?Khe<)DJ#?0e-ht}JpH_IfElnPp%LhC9q?}gyDlXBp=)t*>WR@L-@Y$lISa;{ionk0f#MA?WtUk0V5i4<A=E|kV8!wsS^T~+jt+j|1kUU6QR^djF9A_xsiM|}y|D8*EBiJ0IZr;wynD==nr(mQ@w*<<ODS>Q>!>F}m1n}23c3S9X6a+-E$56U!&>Xw8f8jB5'
'6)QKM2(DI5Q#eSh5~BNU%+^aVssbbpzLF={Fu6n<%-4zR;7kck?2`i6MDwR4#jWu>?8gVQ^ELO8G!svpGX0|-8!|lM58LI0(1=!UByaI=r;<y3k#$2)r>bi@BpzPhtORCi81(2m`fI&w%7uTW+$axecAI|E4}a;2OLoIb@P#vr*UJ+Bn<rF?JRwD&q*K(YA8umX!_2MvT&UeM>a`h?V*NUJ^&JZ)3fwQngTR6r3Rzy12Nxz}IU97uqJOj}a5{W)&iQ%_?_MHB<U6<4_Nj_}Lri$;@>e^`bUHDrcUwa|Ht<ga8fh(&cqXSSOuG=u)eLWRv1Zfx1E|YZ)c>mCw<2RZC=!Eum%zsuOU4GW^xi^aMloDCu!ySq&m5?>GM41R;j)9C^JmJuetKwQzTQ0|@c%RfMM6UQOM_DqlefHO@A6KX)onNHy2~$q768v|>^7A-T9PDckXR8MRJ^1uyBr{_xnNYSCqQ5r4^o@h;|7<b&PShis8BpFm^_QA'
'TENm_VX7D?k_`+?5XU^|J}<*y;Fa@GGO%mE2D+R6lcF`@w)%k)uFLpfLasWYH~ron+tV25RC3;e_+c4G+oZhL=qlJ%eF9C>F~W#S;=?D|o#{c>(|Hn{=!JiPm9lgjuufWhUOXP?FbstcC$#oW8;gtmDcX3hf>>WyD3lh;V&Q5nZeYv+I%CD#HQSAuwd?;8XS2N8f;QIMId8+BL;{-OFoyrpe)fs}MI<5jmehhSo%d|{$dLQh>MlQi#@><$9O!WFe5t^odbeE<wd+|OQIIR#If>XX&g-EyOCDVjg!)OAS(#)F6?u#Vwob!o9*mFm_eHaUeAT{|Eg=Bc%;4-j4!%zrh!IVIb@qYMjmeAd3}?MYyj)K?_X9*Ki~M@puQ5cmC-Yx{;o0n2-{YKZXv=<9ldWDD2!}TKx`BRS)Ax0?wK$(wbA~ij;F%W<r<JyY|7t*qXSr#3fAiW39k?i|97#IqR}2_#Mj!`ZJxX9=aqr<;35JD*Rc$zR3}M0U'
'>;B0w<m0d^HN^`}CW{XP)nCm(Ko(vujiHDaCjDQG9l9Si@p95zu|PdQRvzt?xzzur+nQCukJa|^nwdd^`k-237tdmh_P7S?^l5p$NSvkZtlFO2%mj84Ac<l^#}u^wifQ{I!YA2+Da!cK{e(dJ;Q6ObH1oC!%~h@7WLq-<8Ot=6*=+v}%8SR{#d(zdAbbiRMMestPBlU%u-?#%Oy_KFkFyYPuUlo1%&j-8W|O8=xK!774UXdYHvqfUCoLTAs>BgOixMC3<3SGpv%Ae_SMYX$E_HJ64xt8q$1C<BHs`Q+-n3EX2Rz}&QEVl;k~C19m;+=YbDTC;uobU}*d)Xb8pehjW44kP-|6&0d`IM59nxGlb69v=v-`Utbh3|G-4PsV-j4Drsi<7Kca^EFP}N&wESk4rU#Be*2)jDl(k~~Y!$U=@rea@dTj+luh2+w9O|3&npy01Ywl!M4r|#X$)6s)0T@$>D#z_!43VaQ+QtCtf^TBXcHod$ID!|@O'
'%?vAGyTjQu6Hk;baP<t%rlBf0*g<|1rx!{pT--Of^8BD?v*?N9v+8ZVO;s*?9%zTz@a{-wM&@(Ds)SsXxqO!cXS87MPu!MfwZQ!*i_rjC8-i4i*G9RYr4Lj&x`#sH0Yk@45JO1Qdu(5QNOFpp>mc_2X1ZP{QT~^AZaS@ON-WfXSKyaS!CWL)eEmJ~hNJyUc~q{raaiIy(;RrX20iV|3}}}hE~7}SatIR%Z^5>sD~&j}ZoZz9$$L~CD68kcP_mY61nsYw&w>-HF&dfX>TpCbL-l*Pw6o3Oq=$W{&U5g3^~3UXFlCra9~cnJSf6*A+G<zLHHQD+#wpF`@J7R>juhfjEBlyZT<Z_g<O0gH#MbiYut(mV)_N4!9vEi{*zvBOIq|?yl7eceM<!k?JMUJ8^e0x8v(&S9P=|3F_Q8b2htv`qG}*bST^n=a5us+Zsj`s-G=Naf^*N^X^;gb_LThYie}nk~%%=}};XW%K7nIE5aJ%fnXfsqv*vI;Q'
'g=U2C1Ub&im@)OHQ9)>WYb(i4e}`$fL9jyPygg!Vo<kz<?Gi;)huX93wJ{4O8PL(YwCoC*lpai_;b6J6^-O+YB9xl;@vxlWt7Xewlb=##DR##S!`)N*b8<KhsXQ<20!YoYwvwem8MU?07zA+a#@)c{U5_Q%jhd>Y%c5&<{!L^Ummm7Y<ftz6#8~%#w1|&R9?R$mKTodS95ma&Rn`1NV+tR>w6h^>Sp2tT?}r&Hdxwy=o;9`G#FZ;XBA;M5S795Au??YHv{S0qLiPI%QGhdJfzzo8l{QrHA#kOr2NM4664K?ajo?FN_Cg52X$XI28@L4xec6Hh5!ss6>C6pwKe#9LbJ!zqN5gtOJ0nr^^$uuF-@4;koKLC(8V+aBzk)S0#r^!F8IbLI?e~@jJ$qkZ_!zU7XvO)Zeyjyx-*vFXNTC3aTG+ThAB&FB{F=Vtft3o+kF#F3Nf{kiS_=Htm!5I-F_8!}sueyf#W%(}RTjgye<>s+_W<Oe6j%dU'
'MCenKV<EIACi5uh;iL4RT;S?ih{MtDx9GV7AC2ctK9ATH>KhIB3B#6*BzKY<oGoU)hakSC0_5>YBMVbw3V>d2rfI6UN{tiC7@eUXTZ7B)kIG%ISlbd$ro%hEtxS3`^d$ybsamK4wL$5A^<RBMNwm?#FZ(IwZec*bx@I<L%1PCez(2sTJ)`Amx+hv{RfdX?0)q97H%e*KKmiy|C-X;;`yF;i<<#b;&GhT3^DFOb*VO_EDg{)qhZP{!Q^V<w5Sb{m@en$8J9p6r=vQ1FF4rj<zCf?5$%HgH{e8$H3QQ^%ZbUq!H0QIyYdgto?6kSip*uBC#nM|8j1$kK$<M=QD~kIke&qPAcfulIRUMRMbEFgUZJAb%(*>u+6cl51IJZxsvew=v;_xOmx`Y3Z4cbAO)Ql`f8@z+ygbCw*7rFRb4a-b07gs6H(ho&h32H1Pq8$kLABIG`jTQD2SB~UtIlg5E$;j$lI16ER^<yMZ^`2;vmj6VzPhV$acE8Gv'
'N10$a><MCyh=D)U%iTO(;&PK!U4GI)?0~nDS92ZS#OR^>DX<ZG_y8|NfF3K}*7ctQM??#QLI~&v4RHOaPnZ;tZ7)ev;c`EbdJWh_&)X_@@zGhAxlGU!p!Jfoz&@JtFYV$<sLy`4Ly#NPFx;m{3t_H?Ah<nvjBylVBWcQW#)8cJs=Pk^cDFZ7CYArG_EIro3NM5C-|=e!G<M*SdK?+5MJ2$SG;^#ls_pf&e-HV{TkcE0-pFBi1lwQ8F#De>?*QZu1c$Ig*<MS_7sq_KYYug7nxZAtue=2(50FT;jgv-_@16^5=LPq&%4R4g=R)-TZ9FAhOecXPv6`|sThZQ$NImVl5KF1I7Jtdam<*7n*=Z;}n`aHYp4?;)U3N<XN87NY$M32Di%PsvJ6P)N-OF5r3t18MeUnDz{P%N=S-)q7Au8RefcVu^S<0f=$+e^jjgLhmOlqAoYT!-DO^kt@kg;QYD1EMKHA@8Bm}+XmofKL3tYQz{%1q$UjWpDD'
'93fu<EHI9|mP~PoWFa&i2=QRykG6<bIQnRrGwe+)=A;Yt*6Zkfxx7NV;((z<w3e!?Q<=>buANw>>@9px{_3|$Cl<GlP&Kf_uJRNPBrMh6qRIR5E^fXryJ`wgLt>wGn@UhG7*M_a$@v*WvTWA9SFV=U)Z!a$10W9ZrpIQ|xXC5cjv39joJJgVS)>re^y*MjNt`a34o_V{dC-`${L*Cs@Z#k)ZlGEDH)Khy_sFaLQDOGx25*e9n3?UdQs~mlmdJWL)=EUyggAN&x|Qm5(|cQ2663cF&|XlibKPsbcL)8<Fy*61(s0JUR;%y6!5J7M)k5OcDLKvkvK!87`bGS~B)A^qj=PqpQD=lmgMcA2T#g*8e(vJ$skI!iM0jMDS(UmO{CQnf<k`k|x_;%m(cWrq7$U1UkvKYH+=hn)tnDJcqseugY}yfrOr~CBDj_+Tdf3n3kBL#spz2p<Q@g6eqJsz-(h!td7&rNp#eNSdNCQ-w8yWXt4>*7{*$|%H'
'1KcEtQjmSCOEnPQOH4t-{`vFl)NkD+8bxHHI^|N8P|ltl!J^qo{3*X9(<~P39;(5lnuaxhomqnz8{-%Ap8>fmY(SeQ>i#+eT5pMROzTLQ@f!!`5hN*CF6SzBr^DYvmY?6xhrT1zno)&7Kd&rnb2D+~eIAsbbTWVQ9CI2vj^LI=-f|D-zj<ZS?meBPjSK+VV^2`8_)tgQlfD1LS(*N?!N~-3Q6G?L-3qu>avzKeN3j7%ZA0v?q2eRunp7HgN~bL3-NCA0oi9?bv&@t@K2Y>t4o{)pw2N9r9eQPg+;U8VxHXMeh^;LfuDQYiWoHs=M3*8`xypF0w0nbM?mP>ShdbZi>_9p*Ia%bn!MgNV6+fgt%9O3Oh}fqP>y&23lT$m{gz{{1%`b{nupgc8uy!s(3yjK09hK1?i@rBmisyT8eQ=ll({clCw>9CeEYVx@1@Ux)_2Kr^tpD2sUCdp$q=aQSs-#+3DmpfpV-R31mOUC-+;Fr_Oh1J%`AL^*'
'S&A4{6Sxo7ZsTPEAX#ola}ZOOG1cMvt>7||+*iE%Kg$XxXesfiyO@qYiC0TTji&O9un#3wBl=Nc+#0_5e+_Aj6x!f9<+`F-Owqwt+K`W)06?u}CQ2REMd(`R>1lgF@G76>3mT`>AOFPm<O>X`do{oNEA1qPMe?~t_=bvuaUQz0z`}j>Ll*M10!luvTBU$~0hh`g+MH9A8Tq=&C+Cd3ENQvi-~Ffcncr-q&^ukOprxgfe^t*lBx)h^82AHu)#~xb^dp>;K_<uKm9pz@W>a%ftqpm|at@FQ%)~K4{-26=o1BK><GgxqbhZiF;$<#9Nfnw;;=+d_q5&)30LlttG}WbtKUL)O>hx#Xx<^-T40|+3K8E(DC#Kms)D>VDOTcIT==zbh*o*AKAubbd)0loO-*mCpx=sU|YBtL~jF9ZQO^EtG>G)P!YQL!0ceG$dQOkH1t1$gGrPbOWf4dvu%#>G`<m-0FYPKJf+4e~oJE9!CMM2s^1O6)*LNMx>'
'i=lm{wd+uBq<GNaJBrBkj3nzJ56AM%+<d~L1=lTnpkubW`Db0OEzgQ|kzCFg9W(Nm+FY7oCn9A|i6czw?~RZtJ5DHL&ijmw#^-aIC@a+LZN(>Od}&cBl_W~pF{8C&9JkbIx}%6c3u8wA*!%{wABj(#P+<wt;WYHN*f{XJG2!uD5ffh=sHw5OIyjlWD&AF>w!XgW9_V=wv^H%7lMCHtF+kZy_Mamy86GUmO4R+#SbX5=HKUbzCXp|4Qm%85-m`T@**RLT#s;-4o^;AHehY%Jp=devY*V8bIMxNVFLNs=vStz|^h_^($3lW0Lz=l)?`TjHIvtixC(05FoY;OHT2e07>iepl>!?=M!ww@MW9oUlZErii$?|&06kxwV(h^mnh}NSi!?v7Itio{D1NH6wzXa>}MtrKbdn7~<CtJn{7Gtk%T!Sn!BKfTZ?a0V)7=eEw+E|F@gp<DkfV-rjEG8Tol++71v?o?DY!g7Wa?s*BqO<u+<@>2FPyfn)'
'<4=CC0O!d?fdkxYc_hJZj(|I%xB%|c(bZ{dOD+rT6yKyqD$OY+z*8Q~_)RKs6eNeTR(>(@rSt1m?*y70BbOy=y}BW+n|o-N!}6y=4VQn>H1Y8z195U6mM}SRt<=;fuT)~ionB!?|GGKswHqPcSZcH0$;>G@80Ve;pZIV;|GzdQ6?|g+`4YNhqY3&As9UB}P(PUm`6a%D=O}}kk(yAHUBAr+K^Tsuwjt7$8*wnTWaFx|!-%K02~CCATU@2Xc@pg=oq|%_uo7>5c%tr|k(5xOo8X}hftbM@-)NRn4S}ie_SY9CM3-pjkG;xC2E$)lbnl$i^_68|h4H7^^-rJ=Nxnq0vXOB=FgraF(=9et;dYkZcrgj7;*g$bT@S>x@Sk?YQe!f*Z5oVq*bzf`vixF%v?RmR-Ab_kVtsecM9K<-Enili>a<Q`vWT&(zrxE(rgvcllAP0j9Ai%%s_?vk^KSeDRM(JRC=wzWbuQb&hSVW5Y}DA}cqpFZP|Dzh'
'*#<LznzBuSBfMYKDiNLcPu6Rls4&q%RrzkazSX}x(o^NR3d7@bALU3&4RTd%yj_y*%6v`|v?aso7i6$RmpL}7@$LkoS!JhyX>v-ht73#aW_f_2B2!%AD#Zq9^+)+dVbzix_zvjj;*Zo8oB$@&v0$w1oUV%8#m(#9TuPatAt2>q?q{kv63QigL2JYG00qHs<%l%FflDy~=zEA0obt>wpqwk|2hbJVi#cW3HSpCAi;wEa=|OD(AR9nmvI#nLIJR0dqif7wYpT{T{@J)D2@9-TH%vNiW4hc<nn>c?_>r=BifiPBiIHPQ1|i8~6~}B<JfG2tRZDCB;R6HdWH8upGLiRilPf9QP>)p_l0p(NLy4eW>`c-spCeH?;i<$53XEo$Wz)ebY#WOfH;9}4LLloBhq~X^H+Z=x0~DaItk;~dwMp)8ZfW3+`QHdzmogk*l2zfq=*6~t-8z%0;Qf5vU#czV_au|}v(3>=2-rFfW9OdIHTMyh=mVCH+kaNI'
'uO>J_>l4al)Ym@ZDPg4kZ_L|BOYh=Mvy#DRbd_NME<>AMh2780DDszq^3z26xQiSbf7y3w?_q{PVf63#!V#GSq&Y#KF%lBKK2P30lYVKg4my&nJIi7cbJHX`UHT1xDL+Q=wI66mqz>N>B`A&kN2@zLD3_v40uSsOeK*t~4);s`{8>I}B^&IaBCgRI5_BlG2lT20tkU@<jV?X6t)@&}q0((z?L&%B{T2b?AvGHw@U-iTIxGDrMk!Xf-+_II{FpjNSCgk6-BiG~g!yv?`J74ADv_@Yh**2fdOPr0>#Lh+-yHKpt-$2{!CX#lB%91ii<vevT;T*a(^8d2R%xoW+{F*0XuWkp=kR~_Ar$mmM#qlLugJDw`B&OkwBbtp)oacPN}2=InQH2yrIzx~;yuceF`QRkXWGxm$)yvOWCG+;P*ujZmalA*c*<(2FM(n1YKEoNO}@5BVP`Nu?4@q6d6Qt5b2<0OU=JV#!9=agE5dr+dq58p$xZD&Stb+9'
'gBST|M@?JR;wUW;YfgsWJ2pj#a&@w2OMrFszlPaKCQc=30$<(~AMMMwRPP|fW=$R`w0sN10@+{Kv&%q`0`p+^%n@aDl@OB4v7F+Q783b<gX%u9D!pbyu({Lx>mAc_*1IgnZpJDoOEW2*fH;w>V4}JsvYaw|)KJO_rrJ8eXazUzpp;7wE(+qi(>^`eZzj`bZXRb43NAq7$lmY*bz4<T4j3tQcJ2={l-&Z$7o*|_^zb|dKtsP_;5|&<RPMEtH~Je=)u;P<oqwu%C%fX=_!2CZ`#4$h>6sK%#g4LZ*!vdfDk~vj{?z@0<=*=$Z%e=Tlr;jK^RZg!&rjc8U{0m5Oqpka_XjV)xj712e-01_nC9pvvg~Hf)1|V)JH6TGcaiZEmAJG4G0G?wBhQ+{hmnqtIzqeS0TPHmqT)S%Q5<W-L+Q4Rnaz^dXgtnuQGxpj@2{c%UDg<v_Ob$#>+kY*Z%eG`%Jwrk<?RxPe)>y!$hC1$ac+5FSA;#RdxG_X'
'X@5BYJ2iqwQH82DYoK!7MH^duEjK|?`{vIKRR#zQ7cS6d7#eb@UQUp07Hnq#r^-G<anR^bOORzR{nQ|Ey<1k?2M`B6n-qqhd7qyb6H>1!3R3x(m1zQSzK=V2QmyhKq%Gw%CtPwzNh24pzP=-jj(^0~hp9;5Cc-Z$ivC9Ojg~qIKAH>i(!a7Wbu0K2;4NL;^2Ys4=(h?>N5V35!?1s2=p8^NO{raY_+H_Hyc0O50<0Zcmyfa~GKl=XAP<inUR5bNJ9Ah!Gtk<{2i?s|J_tp#r+rW(A(0aF{Q-?1u+>5?#Ht{}x<XfQQV^~BTdydXEQwV9iT1aUD?Ple1_ZD~L5L2XO{+!et+?uJw7Gp{6C!ZsHfKC?)FH}cpjW^MT(2X)HpiR%0Hq@trI1BD!JYO-GSw<?xqel*&2QDBJj0nI+(bVG$}Ud^svKZg_72p$3R^bGOJpW4lVIL|&0;44qM7u2ZqV<S5BM2y<#WHM`ca7L#`)zH@*C8Wqb@Ex'
'aPih*F~HRK_)?=)a>Z;DBfF2ld99ZrbJz$lk_%S+zy}Ad-L-qRkt(LbC9^=G5KNkat!(i?F2f=}4W+(ZA{ksXi@mErR<?cU>lCjMMy`#xz*t2T&QvOm`6GD4KgI&=WgyOH^=SU*A>)Q8yM|gAH|sl-{Mh$S&}88;4{>=;PWt8HEtMIW^IVN0^TcYRy#l%nDJW}Hd~2YTq#)#Lnz0J%CqxX=wtrfWEbcBdYo2b6F`kd{?+2s_&ros|c?{O(se=6)ABDNjjEs-^o5KD>Ud}TTuR^5EU}~AP*YB8^K5#ERrL1u){No%LLi19xNnvSX8jZm;D&^P&4Ccg+vH6_yQ~eV4<COrgU~Hfs9nj$v3qLFtOAG<plz``h3gpxXqv`lge)BVDXSfIMi>~AK^p)c&p33{RLSJMZv|kJhe}o>EV<5ZlpgllS=HDvs8;1Tkq;8fx>f-(VD6n|0f(N0L&gC&Ck#1f>0Y&odv7-Lth3_V^o?l+uUzX7SPd4p2'
'Q1~U0lVtgQ==_#n4TER6OdxtE*Tol;Fg#w@XB_{QR=jnyJokMe!1jhZyP3HE^Z_YP0f5KB-ztU-K_BG?((z^9Yao!x=oD23l<K)4qG0RYlxq%aYo7FE+L|#K`;74J9xFf0m+smUsYC~OQf`VQvBZjaQP*_sGHFND3+ikH1XeTCP9nNx{*QvU`V{5&+<Y$pylzn=q7d?$K8JIR0BSa4$(B#iQYO#T2i{u&DCWjGH}j8(+|ja<-Z+l07@zede_iemy9EYJpokSA&z_DDMUA~h(u_KVZz6KHFivUdqN8Z2>UH7oKo|-DX##kPGiH}lOF)@ePc34$+#AHzW-<wXi5<QvEmgSWsLiYjK}?NGk`I1xL0uX@I`&u<7MHM~B#wJgK++c>prAkAzl-k?00lgs?orikc*1QBXEyE5c>Jols~TV3P@<LKo)kp<Cn@Yt`hfw;#cm;Cgf$PA+J;+Doch$hF|S4O=T4&fJVto>Q~hCC!HKS)(mY(<f`Aud'
'1E=8krfn$2cOUahE5jE15H;lrJ<IamrN?8F5|^;7;E-lN?8ObL%Qd%)j4b2DLxrWH7r(FK(O31rC><!^Ith*?pB=zhhfYUhP*YRBQR*p2`JMMHM;U=y=ISeIgrH8C&@}Y@xAG@dAND{N(33n~GAEt2>b0PeaxK4gTL}L@3wGyr@wFUOL1=R7<O;9sL}!wggx#nD&F?03@#alGH3ovk3uNny=Y%D!WMb6qInYc&9xt%+y2m)rbk=Jv{5?DCyv`g~6sDk7dC}Zmr6N-i)%Q-8H~_4q(b>K3S0=E^8Pgnaf;iI1y%cJz&u(oGe6@7-_JLY~p?I(#n74OiEpdLP3~u5a#3fV2T@9@ZH`%>2zZ->#%#YTX+AF$_#~}OFpA&X_F6H!%x>2#q=wa_jdOIxXrUEbhL3uaKjRR71^+R@Xt@RyLdJXzv!iAQJLf7TM9nG0w<gr=i=b!-Ay4x>)KyV)W&tb5{<upV%l=4f|={f@X3CT_|;eGO>_Rvf0'
'v$%C?=?(Z^6E=G-u$S&(s@{sL;WQ$bSVF5X3<D1Vt!j;SE1*59*RPJuqn+HbOaR8FC*jr<$J29@qA;@+-+5t2`QG(fVw=-1*}@v-6!q&=&KE*gB!upil7{7nvHCKrW<dX5(+#tlKl7vt2Mc#S(N-Ktng0gUEI6<L>1@?`)?7u&QDx#QM@;hH^VuYg<Jl~TBHlCsi(M&t$*OW(`>s~i^6LR$SN7@}7u8jJkGeKc|F!n-Qd5ZIFJ)LIdCBYr;#S~vH<UfW%Gm7ds8)#TL4<1zd8dDS22zYk>7-^sYYa(|KpNKBtUm|=7kuTmCYR*KMK|yo+eNZ_F2#H6gOsMAs2)IsZhrN%`jF%AQZf;iqZfn}*NwwJro4B)&1x_0WCzucJ8{YFDdWRblXYARtyK%%h`qcgdBO;~v*B|>ch~Wkt%B^r{5S@?(uEKiUyGiQA{*;lik8RKS$7!N^G!)c<q70?>2PiiP<LEzlN%ie<PxSR9en`%jsQd*w+-Mn'
'*}9ZPm_@IYeimwdZIK+or*i8mWO88TT9jT6CAk9QhGhH(fy>!fp>N9`!`LKOv+Cnt525=S$sRx1tPtXC>7={josiA|i>c3j;|d96R@a9Xci^9gyR#4L8r_U>jD>35qlbk%iVZgYoo$4C*@j|g$l!JT++l74@g>2{*c_8hcCK`M)~RlkSSS$KRn2EDmd}%`R(e+<c*Koz^OfV&z25z>w)T!{#@-i;i2N~=M@AXY+vzppcVDxW1*s>1{ptIRyB&Hqsv8c6YfLwcT+<3`nC=pg?40)xw{AwT#;#{mr<@nOEZcWAxNqBN1gFmn@n`;&{$`To2g24nHob9No{+hqN?N$Q>vf@pjurrtf;Xcz3tOM_bqq~N?yW(S4|#SRXdIxj#);2B7_Luo)FKAA*H9?0F!r}V<H~oDDs^V0E-Kz*GO-kVOM)>&MWD)oFy+xG?lW@$(&BQ;4`&&%*7JE9>8BwDVEm_bg(7qrynIV`v9%snBPUFALZlCvQkq|!'
'_yh#B&{s5fCOBRVlUiEc6Of%`PbKF6cQH({6uKAOp4gFL*QO)#j1hE*c-(P|VMksHxzX6;`+&(Z1vtqtzo03RU?}qFrRUI>-|_PKJ38SRe3&~Mf=w-fI3I5JeWGH#@QH9ATi=m=6&WDenKeKjvcNd#ao9|+GpdJ@5VG{$Aw(lyORQfaM%=f<oMR3^=1rBaUD~`FrMTvLj8@%KzB14_dDB5+Z=}2va0leO?{H>rE#r9q2<O@%#psGq*=kUIgr=s^BU%81jm)#!eKomMO}W%l-F^yXAqNPHQ$ZWJ&YAnx4N|UDt#$7uHen5~fL@lYArXe)u&Bp0y}d=14k_s+ls<8!pUXfZd<|e9O{@Bdk+*Y02#4D|>>lEEOH>Uia5FqswEuxAy|1<!L!q_uX-L>B;mB)+E@aS*$r2HHzY+=U=XHeZpd%kzEJ8S(tGy+XKpxZS{)oLEalOXCK(>@{5<Wyr%t>}Z`WtRhmN_Q1ZcdZ-aIK&R(8_}~Zb@#W'
'ze85VI_@(4%3LS<lM|u&zYt((G_1={mCJrqBHTNH-<)vht071%q*LmW=oUXEg`=OG7Et#A+ofx@hB`^SI;0WUDiK}_Iwhb3OyH8>NUg+2EtegEWpBW4Imk8a*KOgf=j5sBS>D{QOE#AvBeYt1f#jy6R2RGuhb=IymeI#n&5BtjO8uUEivLbQ<$_Y76Gi0%Buy&ljFK;;rjhF^vMQ%8=N%H?E^Mp{ag=b}nEx@)Plh38q4tA<g|MXAyCIp^fbH6HG>y4D1dhpewSLcV?8DCYPo+0n^-kPNV1}l=KzqM>D|hGcEaGwkgJo$!`cr$H#U&aD8$paK1AHUI$%MpZyY9EgZx4iy1H`DOLD<{GJ^vo;9iSmiPDAlIiwgI071~duGUCTFg)?ZM*psAy7TGnj&u6UH-G+!DNDmr9&l17+ZaHG;3vX<6gV*$YK2FIjSAP@m$bR!1b-4KILE`AwBW5AQ6*?gX*zMU1`I%CE6(+Q2GLSpKCQ8#BL}tx3'
'+n+k-pg|VAaM*VgLIes4r=^6)Ax`Cfn89Xob{#t}i^@pHZ3Xxcc|y$-uZ2iwd#sOUy{d(;!`rv)V1>Y3J*@OWVq`$}I8rAe5qnhBj#RS`g1WHICa`k2X;s%CpFK^p>OxQYsjs{h`2C1b%1Wy!+>9P{6QY?v){(32Ih;6Uqng|1V8Gu8`O?Cg>;k0}naT{ZM8o|r-y)$B?nPC=8z0vBd3Umv-(O$GGR<v1JeYm}vykN51?iFQPDg=AV#hs}75tZI>-%xr4Np)Wf?)yE7<-P(g(GrcFpB4c{nGdFy&%&XX95scdAdfpx|>7HQC!!_bv+bAC!D&+6>uW%5h=`(qKV%EtE#F(!q}Y<XX5>t()@8eDe2J}#Q<HTK2O>KDf!}jd|k?kpHksFYa|KTIwYuIwjomnv;D&32_>K`<1&&H|IjsB=DjN9-q#{pCaZYPYrEFbE!e5y-(C-G;B#3bS|R|42G|At3bhX@LNlOkO!`5HSeZXkAsBm<4{OX6'
'As^S*D|E^`$M}Xf{PU4AsyZKDE^%W%I~tXWGVvV4x}lPdw>SagKLO4Qzk!9$lzGI(O2g4cJWXM*Bfsv(dattEEP$oN_+4s*WUE^9dclCp*pNOOA{_}l5YtSlm<;Ax))z%YM4E_6gK`4(qK<KlpE3NnlK{shA0a+C(@0)S2bwdypJOPk|C~2{3_Xw&T&pot4QoL4PrFwF&n!LJdXSX75CtTRT$wLjnMfPMASUK>jQSXW=@1zc^l{y6mr$>Ev10j7=CKd2m;e&It%o;gJC^3i1D)W5-C(G+R<<+w5=|gO8q;=NZHZ9YLQ8MoDhc)nepG9!KYOWVU*z;NTi~mgVd6Z5)37j(B2bO;a8?PA!L$Wi=s^HY7`RQfs|c>6&qmk_G4D-y@JDHy%ngR>i2(s)#jFmf#5wxT_w_b9^0p>bv1;P0Cc_4a<4n-buaot}A0jP;y$(7{=TkUgHrMTa@8=kF#Va>YI|#$ydO<0%IMKLh0srB`B)ky%@8fSF'
'b^+tiD|y-uY9C5IZ$!~byU+a{+IRjt%!TZT?Z#r*;JwH5bFt6ANB5|qBKE#eP<ORS9E9X1mx+FuHWrScR`c=&LEZJ64kMjx;u!4^4b?qKuQ~fi*E(gJ0m|5hyMVHBR3irED(bop-Cfe2BjSSWO?F^2VQq)kFp~y!(ON74;oh|T61jQdSJPw^wj>o)%msK23q(!Mxx2#beL^5gp{#MHe~@Y^`Vr)``W)IgU1h1OL0|UI9ZzbNDv;!LE54UB>TAqx2I*;kXg0m=z<?88yQBK;FaMmvH-cG!^Z<7gykiQQq*QaAD?7>&H!oKuvwfHwC>hoild0f?VQ~`EGC0^=CXO+}=!%kiojNTL;3qh9%nfWaCDVP_TM#=1aU&ppPDF_IRTygaV2{(cy0?x49_m%awl853682t&24FE3{6q)0kx+>gQ}}8$ln4?o(%m}0opp$}EFDgDfZg^=8sg=ClYboP!#h+>*@e|7m<`-pl~U;`>@5TA!mSLn0-udY'
'degE}YCM)H)o?V#8o<gx8~l)f`rX=}=#>DsjSlkqQTBkU=jh=Qih%$&2ND#5ttoT8DHxT0+nq}OBcfI)cyPGeEqgHkUb-?{#xOZv<Lh_F47|i$`lxbV+^p${+u0cm&`6^!ELi_PJ6>=EAE{>)qc7YMYCa-pZ1*;B9(uj4K%>KW160B+z@53QhK>03alBC`!*TTwUj&bZ_jnnL=-gUINZ;K&mOk3_W+2|unHo84^e$TK-h@S@Iwp{z`^xLBd5sLM{#!)MiyRWU;VO|X>+5ikwLfBxJ=y9P4Teaf)Lm#ezqpbIXn=u#xU^1WoBb=~3ad8P8+5|sf2lLz9IB}z^s1TP7x!%2+re~);OUCl3?o%{fdUaIWtsNljv9W~<*bYwThNiXai?SUpr8i6Jk07vKEfTAGYVNz1}0oq(zCp8;-fm{(v|Qtae+$#Q6el^+RwoqH?JdpZJ;;_HGT%rWML7`f5GT3>s_x)z_LfAN%_vCQ-8{7qj)5QXaif+'
'vTmeHg!c4XP$k%d&h3}SmYJ+H)m5YnA!b476A2`yv|*>|oiAnt5hrMM4>;KhfiEF#BUlk)(m|~9n~!FeeySgAIHJ87T?~jI#uKp8K^?N%xfX$s+?>iQ&6bXdlFpGE#@r~qVe1miFOU9RaIPVRi}L`%ABrlLtg=SGUd=PJ4r09M+kwI>N&RkQPd>W|zX4Go9=Esp0n;Dc5~nKlZUSD{G%5pSQAwmD?T-0pBsfynh*g(VHmfPT&iSk0yf+zf1^?jI190?T06}HXY}+)ur^zY^dBeIK_An##WU#FAxu+*RFtY)RkC-yD`2rtAklNjW&QX~6md^t}lb80BZs)f{qX6&b*v2*5=h}mr26dx=I*p_1A5a2e_+MK~$&l&!KnwN2E(psDF9fZNfvE}rr^vElCZM8gNYgaD8h(oOu#>F7GOVKI1rzM(iX7MRTWFvUDt73i)GXOc2nVFCsP(l#VMP;L|BkN6mu&AiIgrG6CEAt0GXfRDKM51pwb<yD'
'q^1X5h<uouQxSR&QcsoMmx)Qt5+%SO7%<;R#9ai<I#kYPE0VWDeO$EPJ8O2BdTxR<HlRAhEBXib==&HrO)>=2dXg<ppt{ZqOw7-2ppE<K%4U?TFLsAG&HXr?<>>C3&FEoUs!FYnmW$Qpf3<er`VYJJElO)GmuUm8r(8Pbxc$pVCVPP60%C!dyea>baE9kXZo1(FT|xymR5vfExXmYRE>l!5Qwq;1L2kEW<mKmtua84(e@mB}jzxRi?~8UZTnT7wf=6Y6r>}F0<iy9i8th3Z9r1O|dI&{Ys^i|(ii{P{V<CGP+Ww#>+6Gs^>A>Fta@snqZCjq-SFud2?*Ww3%*V&XJ;Vfn6cm0~#$$NXUuez$icp~ke9YRY7oe$KfB<=w8Ce3z&=%+adBo4!Bh$g_cd2WIytv@9880ZXF{f!N$d?P;<E_t%D}#}p&q)8z<Iz&lo++8|>8+!LgW`u9;3PT7ag}|dV*3OiYSB8TAnU8TlY=$+iwg%5<8Dr;'
'LpTMT{oMUWiDe>7FWDtg4T(Rw&$LG+1)f@34<%}pGE<nyt_XNDDP#{h10eONEIvp^g8oK&(1wqXwv@<%9V6gy?_ps&s&pLq?dJWaHzyl!&)@WG(Tv?$r4_}4%x5<|6kGT&6+-Mm;Ni4<^u<Vq$w)UlS3LF!ZO2~Mrn@5;K^^}%Syu8vJTrQ=&zO<C0rwSIR+4#@9K~yekRHN0iR>Dg5jPY~WqEJH#}Wp@5GJ+>nM9gfHg}_&@q+L?=9iVHVCg%*jx6t8C+-q;*_lS2uZ<Y=CIv`mHma!h`JjMqH*q4!Ir}j5o7;rI#pD*dj4cfrv}L+uD$GMNI3r?7k}bdg6Sai&1MOwgCR=#^@J=ihpvt4_zYdaxte_ez$_*3T-ybBD4;^+e6ZWnhr_UUf5NiVKIuV{tCBKrYOA<9w00h=RNY9DRQ*O~=qC$+$HoQL*N$X*I7e4d7Q4Nzw689sM9uR!8dfDBt!0Wcs_{!smLzS6mh?l4fLzCoqzQ4+?'
'TtSpV=}JLDN}g{_N9$NW%4V?CjfVIArf`^Q;3Vk=p~s0Swahx!q7veRW}e?Ulvy84H8Losn2ajaf`79!7gH4Wy_y?eavDgns}q7?s7q`6qOm+5j`DKInAWluB-u2DDvGtmcR)*3+UL@Um#}Wad_AFA<saP%<2bq)6DDzh=A_6j2Ka2Y%k?7{Bs`I4)To%zQXf<|m<3!kIJDB>7alHX_=EB1gi*d5udV-C)|7~wU9~igm&Y9zl$>>gQj66(ud5v&Z1y)sV(!Dc#}YF=3yvm5vNPSpP>!uX<UP#OlMD`h{NMWAvOVLK+tKbD>)pu_fo%A~K7BhSHK?{R_h{_GbORiN2b=+Salky*XwD$)dB!ghMCxixVEA`3#_?QFoQdM}u9DAX`dJYef35%b@j8!H`JqFpcdpxoEB)qEJ#xHAt;OoT5TWT5a2z2dFZVC*Dg_&Ks*nF<Hdyf=cf^x1SAjETky(jSo*;aA!ZIhj+u^8<E$-&RPet{*sHb3F'
'QR)kSlDFaE#XQs3cYPq{V%)~v%f@?)pi_<05+a}zxCO$A4W$eF;FLzji^*?!pazleae+a>+FtOwe{rkbUJqOIuJO#nW32XyqAL^EhpHj>#I>wJ5?9QZy<$_*+tBw7%#oT@!;Bw0zX1r>9#ZHn{m}77@GiTkDG5m=!|Is8N>UnN0r+@{p(M3tfv@;UwbW0$BLSDOemM9f!|hlvO;;vuFkMKTOlt7PiK>5_RfM^1qArC2j>=4SNVQQ9>leZo@~+|ZQE+fQj1CF2ne-uTjj}aKqbgEx{IK*2K|*`eiPaBPPz*fAG4v_4U|i2#yNN2*rdJ~oB!rj5?yN&=>VJH+#_{ELb+=*w!Vlj`+kvSN?8zZx0wSPd8tZ2xl++=pgMAC_?R1^E9OCi>lu-@p%NtWR(^`rvo+XR6Ow)l22~DC5ouD@?`qEl7wub})G&bsB{>TmfKNIw*gTFj@-4f)Hq&{(jY_3=O6Tx8*LFzb_cV>9TC_BF;x@q|&xsj68'
'ELe(Nmf0<vMiwVl_Qm=MRhC9C_}{!8Ke`|j0s7<7i1K^7i%407d=y0fA2p=eQ(G0)Au}<}|2emD71)I6d^Y#3hPm4VsQ|0agA&I`him17O#F09Q%NqZo<rP))^;hx4G@K7$|{i`=Dt{jr0DIw1?eZ5!n<Qe0i}zjHG;5D@?-Gg<zL4RT~=rWNQTPnI4OuiN8Zao{wQ<P5E2ETaM%ABF9z@#Z8#;;1-_f5i)vE{#y->wg?o7w(()3|dCexFe!)q>15B~r;zbR>$a6+9WCuu)dv1jsc;`V!Q?NR{OXd|F`LKMNQ~&G3Q)7vwe1<q+^_ngmdzhWG*4(BUZGh2)pJv*#5_%Q56*~Hmh+Sr_Qd`x9I9NExaaQm+mUMz!7kI#eH*4IN4F(Hgxd;V<aItumzD8I=9H8uXdMVyP4OPv?E(_rfAiW%bila;((^67yA-$j{(HPWpi*OPLlI8d@7Zdq=p9$AV=Pl~v_Ba~XSz+8)$0_QWz=W1_OM-$$'
'#fOiyc&(S21RsrWM0DA5;$OYt8e0>b$$@z0BqESF&n_W}4xjwVg^y@K%-!zTBN*A_KgvH9o0EVhc(q{jqPmPw6!Dg^g6T$b6jdG;;?p2AcwoW>EHCyBC#|!y9nR-Utv6`cri|?e29-eloG(RSL5@}^Wp_ivPmoP4He~SDO>?q7zK%+9-B-4Nu1r{3+qgM2>a6|Zr5Cu+i0{qrB(wy0+Z&u2H2NX86c<O83CqkW2k<20`o>u76>Hz6{{~AazipT^&`^7HvmE<xaN|q7wOeDX5HzC@lQiFLwp2#HHlkz+Kus5fUh{>A5P*BogN@uZyzI06hFZ@E6vlk#S{hpWjyI$lQtG5U+D#_gJhA@WYolwPrpaiSiKc|i!Q-(<ki<3$RvL7KR&XR-x`h~jBDj?{MlPun!Qcx+ORu#dqkM($+tA3ri=r`V+!QZ;|LqZ8kA^gmv+R4`_rlekUMrlSXp(Qrno|m?Gd&q;n7o$4d{6b^mVhJlNR%g33;XK?'
'qq+zCz}+9M>EOJxk08ZahqTRY&Sd~HqP-_r1@2+EF<PaI8ozYQd5^&uq2;u6qS=fyqy&A>dARDfdERZXRL@7{zuI7r^uhvAszh;w3(6JK)+Px<NywOJiTZ$!Bxh8tH{^*&bOShv<Qv{cvxy$kUtf04rWL~6NXhxbXq=dvPNu(CBLK#R2L5Dy^b+N2A|C_bu{_nPJUf6?7PEbzsQ6F>q4yUQexNhNvn2y@liWlz?ts}Ol;Kl2I#gHiIq3{>04uI+svc1-@Jd|^2os{V4+FQINr;*4^E}ecbWBg0HAN|%L!<rq;92*8VC}w5NWtZ6Z0S^es?5W_3lad`^W#1x-Y>Y$WCDdY6c<N5rEVbJ3;M1cbG8TzErQ1th(CX4%a@1RRnqAhyWckj;XKQS=Ly0Wg^TCw<)8qls?lNRfffm{5wbGXRPV>}lu{?AYd}SeEdk{IFy=E-*_**6*aVd)zt-=N;Xt7)J4q5K`A#xenghc@<?%ryYQY2%d)(2E'
'T)~)X0*~!rBqQoj|3gq)rx&Z$S?zHo<XATvSXEv1dw`ef6%5#`IKOuJzMBM6`Cc2|>rL-#2}uRu8B&_(2NBpKOn=8OovL+Z_#nPLb;(rp+>4yWU$6P9pYb6Y>BBd1pPEY-{#--Le(&=k=>wijIOa*7Bf_T34{&^r*C~O3VXsuK^mDWKc^>@7sA|+7#*;A>uf1#mKMaYHua<xeD&Mjui`I!)y^!9rG%vi?tO@0n-%F4o@I0I9=${b%_b<#GBJEmHH?u7v^9|CO-&*>RWjWqIyp39b6~Sd##u9E2K`$6U=-OkP!vT9whE?cU1+?O*TXempD>!La;km<Hwv0HDp@Ity@BRRTd~P`&a#PRYHID#tpAzkA>+s`TjBjUWIwfkmO5mYPQqfu&f8Eh%I7I@w;lzn_+3~6!y!Zw#zob~V>9*u+JsJauJ<Bqq*MA*(AH>cD14sB<a-S2ypo0847e?Z%^FIfD%6eQEaHt-tEi4Q&3&J%uf_0ND`OE@G'
'VnSI)LH^6CFyL(0A+j)@oVSBd6G9C~%0m)e{}1l`am04j&{vvF;j`9!@c;rwJR1zf@?3B<@bPD%!QFUu%L@lwzv2J+amGp$Av182I?!Vbib$V<2Kud(t$__#Vo(TZpd!3LkXq0mYbU5EH_=cE3-!kTOMtwfyhw13iG)D66(`d~@e8$uk|usQqmnN2O@JW<R#R62qejOoQ=?Ed6uN5**oFA+o=Y^-aH7?<m{tNMJ5pK_jVIa1bL?Z)sy8*G(9sq5(n;%8;tGbZ^Rr(dZ*MI@YYuD_FGbwNGy3i}3fzi>sm_(2t2GWD(w9W7N^6y|CpfmJT}b4fvk_ti=lC<aR|(H<1ZLmPBkvk*y(`}TlXq7B78SoJa*BQ+$Hvd)$g}9rpe+O`5Vcx1C18riYTZBEJ@R6OL@XrV2!-1Pe);8jp;3g2@22+fuw(oa#|}8tSZ++|<%QX;p`om}CN@6pQl#LgoExP~DSaA5eD4{EiZ;iXyMlV$-paG0<NYrl'
'>#0(v_DkLatgK7~!&-uXCkYjcxa20<X2oldqMa41W!7azIhB0J+^md|aBQU+Sp(i=ev+qJ3}8vcNFGzrzNA`&2<Sk~^Auk{KxdHfs8b4iH{~dmdzM-2P8Twi7U)G5ym1a`<|+q=1<uOew<pKAEtRa%v9;&n>k!xEXmnw!kLNJh+m{seUG;NL*-HQ-!k<?&GH$vWNK8%9Z}4zr*EVV9zziY)K1>15C)Wnc_vc?(DP%~gFzm(5_g+lCEMVWde$1oM7XotKwd7hXnvw=yPhbgoCn<w=M>|xtIyGa&m)ST-iv2Z+G~z`cf{>4Kwt$y%V1>_T>XVXQb%Tvks=0t*_ZIy9d;5fpJF(fTNV|nkU_^To_hXYzbEM3dSHlxM2GX|J+gt_n+OjjseQl<d`fJ`MT`NIv{)vwfYpe7E^)!pV4cZ=*5OurheNry=3}nd^XgL9hx3+N|YH<a?SJ#2kkSLAI>o?Mwh+*=l90Dxuk~kr`k7w8U%US8g3}KC?'
'wl;FL3Vq7*e|olc4L`Oa8a=vM6tTJDCEB#p7NccPGIn-N2jkKWNKG$b_1c7+^2Dzlm>3wVGGupf!O5K5+!5S`iOr}W9?zgM$jqQ#NTZRY)S54#lyv)8D;*O);bhXVWuq`$;Ev6##usHvD+#{onZjtGrm7H%hMD_S!LWJ;mA%KUmE!o(q3q`z6_j8{i|rf4f6Lb267Zj|17Y5zv|cZc`l)=wRy0L;ZNw4?hH6iQ<!vl9Yh~HN72O20ml8t48hdm01Lr5B=>wUZ$Yy3~P+gJ@1Y5?W<*Q=lgx4~PA;xD+h)n*5ETUW&u$vp?ia#IZ*ED&|DNsy~DcH=*QnA9Om09{C*|D^@gyC~JB$y6geXd!y&JWumIkk!A^I$$9WC{U@JeJ)l$K5roh=sB2%6^1WLn)Ufi{<ilMK|*`ISujYi-#xZg9ne<O?!#BCX~HwSgour&1<{GO>N<YgtCFgdA#wZ?@E>IxFbx_X6b80x7~+Q9`jQ<!+u~txyqN`'
'6x|tKcG2mHEl2V!#De&RNd|$ml~pIzk4D3`j!r9Gg9wSJQ(}zAMSlCVUX_u~h~2QSfp!IsmX7I}Zw3PD?BxgfJi4*>rYs#cDWOfQzz86#p}4zfA%K>W!d58OaQ~PnC6thQj!J&+gdStnHuX{#+P4dEg?UhUh;ZMiI7?yCqT<BY;P0uK*`TrJ9oChe8`3)z>zLe8Lc+ZL{k#?+R*yo`P{6sGw;tFIx%r6=mMJ=9ZfSuVp$V|+lNN;;0LL=7c~|iIT+XB?;_a25nGzst^s|3cq?chpWxy1d$H0&UrFe+>3gv%=Jzd0v#TVjVu@73zB&fwXBCUB+o-uh%s~<X_VJX~w!Cux{X-L}UzO{)G*#z{UFRE)e#~3qzP%ZbZor9V$%K`~?AjvagJa!YwV>*z;eT;4SV%^rPluug=G{GT!R1H#Hp`0CC8U?&+KSWQW<P49KAKYx_R&nhBN4rxBT-tGLc}b{72YpKw_xlZxx+qXviv>0;<m4#7WsYJ#'
'pc$!iy%r|Aihy$+MrrAV#J30wc(F|2`=N)RPIVZ&7+UB2Ss1JG7V|w9&pr)9Lr7|n(=IejDzjz=)VTRs*Yc#8CQ4jsc!kIk82O7Q{kuz;!NuW=96u)bU>lg*-SU2|JD}##>INg>OD4-2A%o_TV602<wxxnA_UCfF2t_rsOw}=tB_-&0S$>WK{J+>vJYD<J4<lAfM@M!N(bdHCzI=U-mVr&gWkN+kP7oTx$>|c3a31<mz0bF&V0~;$@k^K{lY8pjTS4YX2FS;#)RRB&2Cf`!RraVVXW3M#{d`!6hOhP>URt3~&5SOeudmOA)ta_%^e(CSM~pd6`bH8j8>-*6NgQ8b@iOomlkf)lY=h}71k3T@Du%(fh(Ktns#@FLZb@Z1vll0F+fHO4EekCLkC8c{C<X8!J9QMX-XcVmfvgyOA%E<kI}HPN7-m$wAOs{a%1RPsXOa<wA;|DFnZ@&8+?@VL5`v^YZd=jPjaU$#_8kb%>_+ZaVaz8(88XbP'
'8t|}02V=rWVOQSQq&EYVs0lUG3#wP&O%g0*=hVEtVy^RcW+QnxbRgr4eR+)K9waDnq|Ys&htG*=iSI(n)pDdiNRE_U_S4d#1s!3F6Fu-x@ER3nl`D;p$XWkH+}ea^nj>InTd1HfOEa?dt2oVY)4%U_s&@{T=Pc!gSvnKX2*pXw2HGUB-##1u*AZib6@48V@q@xnn`1=Xlp6>D$gcR{4zrNEC;-wa59Hd^KJ+pP4CQ_4GTb{~&IB+>^*kp*XM5HgNrlIH$OF2jw1E4<Ut1=i82)ffAjC^n*7@L>_sEf0rL02ZZo9PG4??q_1ryzlS<2L`tP~~5K$)W_!zRkaQN!IQ)~sG4lL%61e>r%Wmy#o8?Cl<AdNOSR=Itw{grX6AEUN}@h5*8MJaE7?3Iu%irI7h=X19Z6p^fJU*opP@RgmMvz>mviAh~SW&qN7kk8HwhEs4BLh#$!>{vbu#j1$^8`Y*@0BAN{p0fL6guRnY>BSs#kvu&*)3@ZV%'
'+jp7EE-0PlPnwElOuf<jjziCbjeCl!Jvks{tj82saEjM<L%JJKWjcCZ-B@hR*k-fJS&W&bWz71PvXOdd1u5;M2XgfWSgc`PI^dG1l<!AOdQEtu!9L9*VJ`OsW>_y|23fic<M*NxT73uK^h|9v-RycyL(*lE$~gmkV4W=9PC7=s{i}IX&$9ci2Yew#frSx6nc_s2;qU3@UW{zroL$<^G_=o|_xR9{0J~?}jx{jj>Htbf{-PGl;?~wQ7@-O*C4jojZymw=10?5n%NV~GTx2p`;c1^S9YtvKOrc~~j+S*&RqKeKPYZ3Zk+15PO>5BS8CQEwUYnHZ8lIDLu`kk|$31zzK(&`hR_(S+(P*(@vS-$KUg<I9g5FrV@wF_vsx}6m&>fSwTIGpInZKr4z12rgAC-R*wRq;@BTr~bw3D&UJsKtou0-igun4)mcL5$EOk=Jcpa$IknD){gAJ2=^12jC=-bBLiHWrjn@9_IROeOw%k*ipxuW3N*DN~T8'
'izE}=Y_4@vPPbuTwy;5n8YZtMjQD<(M&l%wJU`_K0KIw0;N<cegC9lR)%cZFWS!joP5EA?SU|MK=17^r0;bD9$5l^9&y#H|GKYQaK$17fAmw|z?#jh^iFi?cULvi4Zg#a}o6doh%^n#g7kc=i^*~IZQKVM;5Uiy~OSf`mqm$YMs(2Nyy?HQf30ZJpXX$pp<i&skope|;ClPIxgWE%<HGJqAP=9#pGd!9~qP)&?q{Oz)l+|u0eyOE+wP?}el*&HSGX!q~KpSiLD&P~9ku(Z$AyXRS6Ut<zH57dCKEq(P$-jYYf#IBtMDCE_H3m!&X>Up{2OY+HMvbA3QGy9~WDip+Mp=gQP-+Ppi<FJAGkdLu%L1gd1w4v#48Iiw&$W6S@?EST;r&mleQq;knqO+xnhq>Z(6o(l3kqla-rM_oUoMUq6%cw8$B71hIlyP>HD?}|SrlAez_SX5!x??KhY3_y`U!YokFMA4P(Zc_wbkkuML!epITcT;p>{*g'
'=f;%DdMCg=A1ZD~%3_Mu7FVg}a}N$LTB6~zHHhC)ud6Upa|@RX8z9KN@Z)E=*a-aQ?)Bj0+nGQCUT{;qh0?claa%)B6aM<ubD(p-t{8;E9kUQDH8yjW*pUcoCNhh2nIEuXs4o853|>f-yKUSV)ZvLazlRI68P+viDfSq&K+#g<#d<65M+evH*PoXGQ%D(U!D-iwbNW$Gu6a^V?HwVgShh7M<7|RdG0Mo}=G%rsC7W$eeiQK+<jFIQpI`$1jCn~*pTYaLE~EcD85G|{CR81lwNG)p4en&%eAMkPVdlb{<I%NJ`W<$|Qqv8074l%B3!hWx*|+|hm4{Tg@Eip?QIj`?dQ$3!t}PF=#r4d#3dS=hgfDFfJ>>LeR$7iZ%C>-_z_IDMbD?IH2SzMPZq$G(FYtkUp>}tK@aGQ)AOUwl8gqU;Let}+c4UipZLoBwTlfx0{HG^BF2-i27ui19Vt{=u7;`%mwB~T<3|-q+@%hr%yS&f^<2>JnvGL79'
'B^wXt$3*n!7gnCQL9^=b4^n5F&~9VranIlPXpYpUA59Q4c|fH+z7A891(@aJ$tdDgNXNc3U--;-kXc>RvoBj>)W|q(LvcJ?`lZSa5|;}_4J#$landKx(*0%Edc#RA$h)pfm5CB4b*{RI!({A!laQLmCFaXSEI?v?dL|KA_E=>O4EL0%sr9r01?&Br{XiLYWNx&v2Z!WEN?(StR`LHBDr!H=#{Z{B0>iUxM0!Te*5q?CgD*KihdORRFJ=eS7+6``3Odc3z6O*P7Cj6b7}!{Rtr~)zqtY;&L0x2qkJbXAsJN4CjHOSTjnYQd-&S~=*v=0L;|q^lCfE8p{Yfd(^&RF^lJRx!>B(^|jL<1@`}KJD=CoSD52A<N@*ygamWwt+p9+<97UW9D{s|-EHli%LHY0-gpMpS-@5YqkcIwIBM$@Ek5RNgUQ+B{EsMHB@LYVY*kEE}iNcbp57nxNsoq~Pa)vh~xk*tvRRT&Q2!=hkIm=weiem!M7%%OiL'
'H<;e^mkSLkKq?lXYUZ8~VtOLixi_)}P?qIfs*R+Pv$2&d=AJ^4=bq`dr5h2vWE=DJdd09`qN*kYU%-w$Zp89YIN%SdPP7MlmcoBuIO^I%$@2i)?>5fZiaz4`&y)rW0n|H2O*Kxga`k4r60Mo`P3U|V1eGf!9Sys~kpFf41!hAv0vV8BZ@6z;;nfRU!X+#XVRbRg4k5h{Z)p~y;6&8g8=fQObFv>c%;$(N4&0A$xlBfbW!EVtZy>{wEOj$bwgqkg%k*D}e{J}c*Fk1Xx?bP;IbFecdp>O|WUO45RbpH9#Uph;Yqf)!FG*$Kw*9Dj34B)!NsCE;*n)o<@b#?tGSPEgWN!B(W{Vx~UrM$H)_bz1c^fm6F84kQPMG(<g86#_(thHM0^l-hJ9!blAs%)6)(o4Z*NIgkk1au(T$}y0`>+W~xD%eIul^fL^pE+>YU#6@p9}*Fqz9{#-TxB+F%%8)r%Pm2G}f(PwwhGRa+#gTY#j+<mewRLb?Lqj'
'c6tZb!;lgYHj06Nwk>kg?i{jtG`VHwo^}w^-minF`9@^AafT}3^xtc-qT{241>Hf|oVD$I?+T>o<O^$#L;7}RG8TE?t1+6A_V14au>rMGcNgz`oxWnN;3nnyr62}>B(amjlT46ZT)ZZ-hu18KLcN}5dXWM@16tw{BLTJ~02eNG^+Kj+9Y7>L^0}P3Vr8I>?eFRuniLL$s?dOj4;@C?FE2G#D`|1+Spm!5e6cS8reO5<<~9>Y9CtRm>X4O%A2@*No;0bAwqqBO5R{bhr}(1!6}z6pDS-K=gUJTo%9Xg9T)~<{&-mgTaVSq4<|g*VIW9z^pBIfS(J~=TlB1Owgf3nvyT@yUM@>BuVE0>!3hAhFgmEE+$D-gKci`Na)5a*jSVEmEaWP-mv2<g1L~-oCyi-aWRBf>C3xG3nT#~@YX^|zm#uL_Bb>+a6WwtbG&2p0xru^awiUqRG=dr!+pw5px7FmL6g|t|Si%3gpH-aTvRjBh8rO!)n6TV6{'
'nhnkvhnT8(+&j;I0wCUre*ng{*6S{^lURZN7J81y2)H)+4^ljPy>kQ9$`>54j$IISsR4Ag9f2}3d^V#u*mFx|PnPlDL<c<#S%#wm3(rUeLl;uu@70eDx@1g{$L(58`HY1axjP&y*h4Tyiw+R0D`7d$X4%<K1~hF{#&u<xG&lm|^Oh#uWbga;Gdg1mcPom%x-`t7>SL*!!9l9fm;3`c<D>m12n3kOYH5b{F&{<aVS47-(!r@7;GTTP<T(f(*HQnDCoEc|F&KvAqeL<yA0RiSK*_i3G>^7!eA#L*GyYq{-7vL6kgP>@JfH;ZlJ~ljKoC~v{X{e`Mlm7v)-RC9q!AyDi-1jZ?YfoDnz|fkSZ#O32Qa2lALR-)3=%koj0g3RB6RkNX~_c&5WSm;i(vehP#O}9@TI)T>NjL`-EkCcoJ=|X-L}c%<L}`C<5w|)$NIIcYluneDtya)CV`u2ZkTN<j?+-#&b1ZS;uW`8Ty~N}j?(tF{-DjB@Q*O#'
'Z_pC$^S^_6KscRAF*V&HR}ovXA58{%{Mcs*6~4;D4HE|Fl`i{0@o^ZY63e3(2>Qgv{(m!|yxmXB0QO9FQDZZm!9mf)BXw=m@CHwasN%yO_<l-fV_ekFJdrs3>aaSp&v+raOt{bE94rHd84r3ef*tF1$z;Cv#VzKck%c&O5EYTr#nPzIrhPu&^G>>AdIsT?emE*ht3LO@Lc2)PkwBi7WWcA*S-ilc)Ap~@_;fErPim!aXOK@^$tKU=tMI$$W5gD=kJPRbay)4{LEPBRy&%D4CD%Na5D%Cmy~izz+?3$?!qFntDi43!-t`=w|6f#3Qe@dAzNuqcbBF1*;FR``A!K@WlwsLpGVAOSBHiK;Qwuytrc5kBkKZLlH{qrj!3|2a({FEL+DDxhx7Mm)A_U*bzzV5ucf<OkRLixU0OLGPpfIZ(zX$*oZA`>cYc=qQ4r%eBW(t?VFT7i-r8Nmw0=se4&?VI(gN8ErjE!?w9dKzUTgpoDHS}hfp0aBY'
'Z(L>$f=U}=waF9IO9yVEja2Ih1LTI;Vi&w@CqQH4<eE_pgjzMJWJ(nY?tUjy+?whu3T(P{e3Wnsi~(5jFuD(L(MlbNci=>*+wI3QfPb8D6k;s1zhVYw32vP1@p4k*{s})H-;5oGDXvSBAuiMhM>Wmm`#`eL`=pv-Lt)!^O-q_>4BN)R8E2WhSz30!iVZVtAF8$;E07I0m`%(D;r9!_S&i;C5JIxgyR(AhuAH~5e9uk)#pG1Zr17&U4y8`<?)V{K2pnm8@#f3vM204oh+W#~qx&(HyQjK^juCG?1d`LjB=zSOE^JrV^R`N>z|^wiN9!B@m2Y34$INLecTO+1c^l89S->s8{nH3Bb{DzoQ1t_T0+%8&oW~qr_T!(|3oD%25IGD3^3;_tFreBdW%<F{6s1W?N)|QpOvRAZl}za@l<x;nV%17o_2wYt$J=Mfl|;g1HXs=L$Eu5hu()gx{%4qq3b_WJX}6rmbnnAra@5kYSd3ijpUhY?aVo}!'
'9|-_9j=Ci1jEc0{vmCEcufp+XI_?a5v#gsB&=}~@{%K~(u=r`_y1!aEZfncBrwB8as(%(KZ9WfZ=?#?B-BEgfD=a9o>WRAcp;zIeY==i04S48E65py%XJ!}~>&*lM@a)S#3m{Mf$p!fu3dJ^V{j%C)l06UjnOfzfOqQCNLP&_>7GI%-&qyb^j5P-J<1AEgBZdUP3hE+l8C6R)5iliKk@ansa=Wr<R5B#Nv$JgPf3r|<$tN5Jm@QbYnjkcL!WxceVHM(A<y*^-_@o$gxL=iWR9A7ydiLOhnv)i4CEi{AW(GUQ)?vj89Ph0z4Ok0t3$v6Dq&rw5Ne_~!djs#wc4kmUw9POTWUFbz`-6LaS^63t3|Zl8V8z&*%#Rz`(Dg6Br7CXIJa~AhFpELlYD+Hbu}#96*!|O7Vl4z8H0q6^Dk@<VDBaAB0W>&KAWG0WkhGscqg7^}T1UjccbkJfOKD+$HJaB~y`as|bD9pd7w62x?n|C`Td-kZm|(Ik'
'Vx=fX?1nPSHUV>v_(>ba@4Awnzd?EBkNJJVf)DUFm=g4yKDh+oW!0nZMU*$H+qGhhYoxY+=dcp=CELJaafst9FBEDrBGjF4=imhhFzI!@G?l=SXPZ~qvr&ss@7_w%?N|{8n5_+jvIR9o<O)Rueu{Ev#tvQxB<5ji`Smr>H?cM#D%+M560MBW|5xhjFm#PAP99|Y9qA(Hn;1Ix#c;JPjfg*K3?4=R+|wDH@RkHUS^6;*q~%Dxe;c!BTH=q?M*9uq^UJ{~5ywZTpt%hWX4xt6q&Rrc_cw33?&2{ro{60l3I8~X(8H0BWazBybIhy_1!m{0{#v-gS?C0d%TK<Zj7apbOEIvRbNcsde!w90K12@Mqbv=(`yd{5$8ry9O|eruwtIY3Bin)8JTDtKL{{pU^>LAzb#)FvavId=!PMeKr(ne6ADx8kAwPJ{9ZZ*;pd472ugd!?&aV6aQQk=9(FlTsp!c5B*@L#vt_-vpqKofO^qiQ2+f7Rr*5S9Q'
'V#}=S1Z4A^Mdf1`2(xA)3g06NFZSyU7=UdTcp@x9_lk_Ee)af;mVKN`uk42x&hJRiBG{3ij%OTEM4_qbda}?;%B>EOp~n%(GK75XUm%GkH?GKiwo*FKh=q(jdv_Gd7dAY@ZuD(z>8oGHV>#+_bhS*l@!2s`1*FeMSsL(e0@IPRYiF&(cm7Qg_oWc>nbjn1%88aI*0!(ap1)+DWttDA)PdBQv{t1q`27D*6YVmXHi_fs=rYq0bux;axjIJaxK5uZo{?c`1?EK-^4Kkfj~@+eoNWDL=L1JQz1UagHhFO*2H&kl*sQWIN8{&-7^7q^xgLSDP~lvoj@Gy=V$JWGV+*j-D!BE0>R`60cYGc*B074xT{P%k^oDR{ZYz~b<=9{-ZChUMnw8B3RDXjP#~%aS#GFA^wC`%Taq*_^FB@Ua5>_*HzkaWX&4c_o$H&KGg)Y8NKfR&MG+ZJgu2rAmCl#=5c4yM6DnR*E#|?kyTgov{x@5uvhnhHqf)M0$'
'#lpaM^dQ$uiVJOI`zp;&1ohbUppd+%B?ss;O7d;+TTU@>cy~*U&OMXvw|ow$y#k(NU!xj63m%uMSl7w5zVMEqukF|Q;>o*8K-v!PJj<s(6rH|!#Gs^}7sW?D4LPtp^(8NO0xlou28E&a2s=TFS%1}*Ng?HfSGyAAUj{2Kt(ll8%q31bQ)d4lqcb8(@ueNma9nCk*fQfHPi9#=rYhBbha*^t{HpQ@BomYc6EQdm!nPzG=ek(}%mwdG5h$)Z=oamO<@tllVjC0E8{UUaLD}eO>qSUvP;OL2hc@k@P5ImJeUN+Jt?muM>&Yyl&ASWYyU+S*chfk#&if@>Dizs|mWp-MVp82>5I5O$TXs0yp1}*d*Q9nTcSHjN>!p<L>}Y1#nI*Y*{uUqslV<MnuN?UFm)aFBSrBKY{#kZ?(!m-w{y@3Vz2pd^jtKfAv5Z6aADE~(1!hSA8y{)ligU5Y9=Jus`Exc*JdJ(h8OA8b;@2;hXf)W<!Ir_1<JNW0'
'QXf~ri4}CVz_y((V4@`_`h8rEtuQotnFxjz8g>)bi<VOsTyc}URpiLI(=DqI+woO`74?bV+kj-tX_;kDSYX9CDLjOr6seWPunMnaa@?fm;SxxlA${oVc#3!`&WE3@T+H!jTk}{eK^0QnI+I+jtF0UU(FZ)*OsR+HmM7*%Jqmip$-M<yot%oCrwh*-9}JN3s-KkJ-A}A1Hh>*@FhLY81Ko<8ZuQnagKVK?&xIj!@a4xvx0F#HYH!Xi;dVZ9)mCZNp9mWEI-MKotsr#4EUBmBI-1u&rm~YUXtkSeq97r?7bPAitd@acLZ!(JwCJc#U5)Tqlbscz?Zfe7fht96@GQ&dDb`ac522`%tYbLdN24leE}_6O7^;u;hc}ZEkc5y`%TT}$x=|X6TC`L)L$pILqf9OL)`%UXO%v<>Z{HSqcq{y{9okKkuE0PkruslDAmYOLiZYaMV5hk74S;z%4xMGhUl@TtLL{&~_yS(`b3mq!q|>4kJDc%WeUK)5'
'&lDs+vyA5-Q5Z~$RAEH|HW4>ffa#0a8_ZkIDO&?xvp*pDZMy)S+abhSTPdZ&C#Y_B=G95_i;e(c3jRvhjlT5D6Q=Z${i}QXuX&?tY<uOng<RryQt<}b-$7YVIr%Nj;CQV+BMS;o<|`4fU+%a;ZKQ^jYqqmZ1}G4CRT3_hgj*z=e`DX(FQt+|P0Y@=Q5_xpud1!0K+Wj@XP@4q&q8e^X2)=h^>%wnnNlf@+DczJ5gVfuHA)$~6t@>>jkC~UpT%m~Sn8hFFbkvC6VK{dAZ;H;m;UdqBwy1rKEPuyKTm#$8I}e_t)v*0mTlX*2l-otHVMe5OwQv{*!n1_{TiyX-RN6U&e>{=lxSebo=hW(<y5>cMfKP-giC>xG)WHJgZ51ma#D}TS1_i%uwEX1qO9l@MA*s`_TJO8D-HgAbg2M?EdYr!Q8l}0iOr(A5s^2h{ue)wHS)xb&Ed9nh95Wqf{-}7m;<>SyqZu84EFRs)#-6|>#XAacQ@9Lw75VB'
'0M8`#2z(oWU|=Y#1}MysEtooU$-u<%R2#9|iW<seXT)0<Hax>Sj&@1;`*L$f<<Fu2q-1(ApRpVxtg3Fo1_f8Jr+cxPM@q6f@z8AIyPW9-x$yizw^PlTIyTki&oG?*H=E=qw@|`01Jnc?$N`mnLp`F)ZgUip4mY_OACJ#WuHXjZ0urkmz!MH$PTsE`Be-x?8Nrm42zC+iJKOrPYsVO5HWx^bp4e8*yH}Qo+>VwiKOYu&HstZfOxW8#6ba+_&2Y3<<d_|O6hp~A)EQMOPS2FUx{&~l%<s!z@{TZWMt{orLJ6@gch_>Dn|mcmuw{%?kf^W5mJ(E3ksW883zTN>9Jjvh@XW0D&R$dZZ7YzwRZT{~1CIPYrgnRp-<f#Z88;*}1MMGcIP9R3lc0bK^(~wlpc8Yqq!z!VSm^V_gylH*KHB!bA&~PG%!nmzu;2HEx{-=S)gm!{MPcFhLeNKo66%!=HAeis3HZ{emkswBHw&?`i4<=``z0E5Y&@>v'
'1CMrO(#b**3<=7i&u|W8yorF(vQ$Sf#WTkG9-N!TF<|)LB6QK;4{nkBy8qLce-e6Sqjt4wLB7cca&9ri;|dChT?AZ(08Ez8gaEDPYRT0g9|G*Bx%5T?NeT+eOoq4d!fZc8Z?VBpj-AT!@c9C}F*pL3ZzligzxqdEugB<B4!6&mv`eFjMlJKFF`tm`eLpZ1rfyi@8@eNK2D*V<MUErGGw^527nis2{R9P(iOnCa$>2!&wm(B^J^pF>U3EZHn4`9N(1A;vf9lc+#k*5Gkcy$V+RG!JGe6Uh@+CZ}fYbw$ncyli&C#=rj?2Qz^9*EC_sSR%HYL}@r2Tg|^Wqir@BF2eke~NC`epon<_2;%slrg(B0hapwNz-VmqnCG>tFP89>*u_Dq=v2?#jdowZx;?X6kc><%s(@@-^|I5?oG6r1N{g`|cXDL6+2*J^^eqGfK}Udgf`Rtq2$pN%k8cQX*+iK2CYvp|=jB0BSsdBN3h_{sp*2Np}Vlz{!_>'
'A&K3A7*vHt=ZhYSIhtXbxm6(~Rq#tGA=%~Fg;f{umA_73nd5Pq`|JbyK*Ao9hVL<Dv1(sH!H$Gtt?F<T{xM&oBY|`Q|Gm3{0`Mniq||m|Kbefr0`i<be$AhM#QzZ}F8MG|CM}FfC>f0D{c#4frYkPH#sstbK^c*Q^_-g{1WPJc?%=9CNtXPATuHSF8MWcBdzbt#at)ne{0({eWW?bMSg;rk%my@#<+$)Xy7U||SB0Y1aVJ$4-qdDMKto%Vk2T`ose!iPrES;*ONL1bOozz!r7u3Hg2PD4a(9QBkfqAsHntD`fQXg<b#Np3WdEU}+fXog8o~CE&X>E9;c!-oWd}#1Q*h{z4D3Vi;8HR*X2uy*8@a!mvf0~-^BxJ_4Xt@p(R-09es3kH_w1!x#kh1(e>d;JRwK@J!C3C?ZcFNbJfNp6Qw05xWTl+bujxJt?a=Z$Au#xEtnVt}@3%G#>8pE2e=h&k^X}?41d>Sw2!Dr7$guIzb*6wAJeY28'
'lJ_XSG|=2>D&6ws)#Sy>k3D-vw$2XY8|z1lJx?q`i7N)wb^yFWPuma)&qDk|=nN-y@xgH2H%n;MN?XlXE|gA;df?}{slqfK-P;%+?SYTRF=uh7&Ol2?%79FMo-W~tAX6S&|5dHE$mbt_-HY9-4YxDV>r8sFUnLM(@uv(@d7hy2eY&lV5H8Q2@s`Zy#+xlp@TUFco`)3tAdf$&ivb;?YgT05=>$AI0O*(Nq4rE${-m%EMDG9Mx1LOgHj=~UtAb{-<xhz3K{SF?=I5&m0r4`@`xUmuG^6+YLfB8FY&`{u;r~NKa2Kj7Ktd|ktAqmCq%>U^5CgiVQx(`P2=o?yO%;)sTFho4&KoRf|K5E|RoPl^)^d)$DQLKjX+V5jh4IX}&TQ{>YuNeMn;{8E9k&~|7~w0&+Rf1enVHA7$mdzhm)2pjq&<2%vn&MCTv`Wnj|Ve$u5j6II)>!WeTO!5pEW>8;N$yKfcg6FHX|3o;^BPS-$EzX^U^KjAY5V{'
'0kZp^F-~zT4v`DACAEB!$a;-B>Xzwz-rb);b{9SA9V`<-cN7pg@(vF&_2`MAf;Y3@u|N6y{pLCdFalUYch{C=T`Cjxi<z_n$)GI_$hXgq6QMXfx+x*vRJq}~wutiqp;+Ascg#k}n@aD_xI9Vg+w6`(=bJYFj80)IVt0>Qg<j`bh=-9LkIRycQrRDv@~2zm?#V6O@=~4S;3+4#h?%@;R{K9XMJY9l2|HV^oZpC3G-SpXJo;Ci{-=e~`+S$~1#5IDhJzL)YJ6yiDWnW*`VA(160Klx@HG!yJ-!O15u8Sg6{<f~s2`XTD8?jgp0zU^eA>zwc_x7jN=%=ut%Z&>rEEpE9natINiUoNL#S4`)d`OZ!F-<&7_Rs1(nser1#oy(4$8Q{V9(`gxY93Au8>uxUl5&LNwvF8+1l`#(?2Dj15~B<Sc&6I8B!8yBF#IT6#UkPL)Sac+MU`1*?FSl{d+9JOg_b^Jr0NimHM7ZzlJ#2(LY&}TCU0NBS%_W'
'+Y4k`8)PxoU&b>=x7>^eCrxm#Y?f-NH#C3<7~aInJ%f`{NU3r>-#cvd5LtSK;Ik78C$TeH^+$sloLMN6Z8U&OaD6L_=^^j$riYi-C2_;pp;t~znbc|BM8QU1?zSehj%WLma%U;+jrgWbcmneXK=?yfCM=MQeSE~r(4J96_+}|b$9JjZN7kdl`km!@_jXdC-v;vAG3>-ESqRV)ds@zQJ&!C4sBD+?-0iqOK(nTaUr1lqLf|L%O-VnP*94gDKwLmzC#S)^yWs0od~zlM6jITjP_Um=`&U+C5`Z2l<w|3gUks%C`_uxNkOAEHqPTN4Ji)hD!~oXoa41ZfyEt#H)8fi6BD_y)x9BW_{*QrrEvC-NU&@bE?QpSKDs3kT0N&AQqosthsG*{hvISt<dRo=3a(eHWEi=(Wlo@*k=zGxS^RppcgBzi9mJ?mUuoJ0pQ80?3OVw0|#G}1`8Y$O${6lEK>>_WrzjtSNd6(RnzdU5T;62K%0d9UhzHh<W'
'mk~O>GR!Z9ECd(~o;f0pj^z$$>Dazy7*$s#P30h(2=PCWBU^!XbJ@dj94a=KOANuYeJkC5L0rWiOG-{g4i8-XNt}h>QTJvlfLIVH#54e#9C?WtWJh42Mlt0`ZOY`i!!vQsn8*PXDSBXqf~?blH6FRb-S5-emcV*v_NL-6%MQ-s?;lk03Ri}ADBdx)i%%LU!yZ?#+b<2`@q&p4rsIrnyrT)^%!(a>=p;6gd=Y@aZR&!KHx&Ob(iKbAyN#0aad?5pDP)#KI1;Bj4IXqmE;44!s?2PxQd^ZdV{*(FFW<<oMFmhMe}|u0w_|XqAPXyPzvqL7FIFZ?YVhB!e3yx5<*!6Mv^0q!&)@KZyFoG`%=<~5q}`)5jWI{tVlfOl?q0Vk?_u$rQD~9WrDe4#BD`Y=csvbd02`_@>L;-N!EvxmPdd~Mks$zrF9j0g*^h|C6Vx;=4)|^v`#rFJ@A$_kWd-m^>3)OD6<01kKRZ3ZI;~f#LPC)@L7Y*`#zf2n'
'4F*jUxp|7TA@1rQ+0WNsZ0OZiu)>reL_RW=g+McS%bp~8S00fL&k^mH?8R4eF+*Hd;&+V+DT74C8Z)BZf5_kvLtQ5@{wb&6SM?OTrt6^}AG5&_*&N1zvkVp=Xh`6*RfWA|HABv|zds|COMJm;55L(T2wFehtkg1*d{<16Pqy+cQOhh9W13r)J}-gF7fb})4;;_{MU>S)x{A+eL(!X}Rpoeh;lP-~tB9oFU>y0_7PJnr5n&;n%QxFnkJImab8ZMBWi*MQ3^5QL7!59#+8PX<FF=onz9?po8=H{@=EOL=rm8IG%yrwB1#*G}cme+5UmTKpT~akM&7K(h@J&92>l7zTLrhu!a?fO%gU-L%dl)MK_?V$%nZ0G>j8Xozl@sZg;{fzOz%Epkf??2V@TxH}l0#U~Ip6qvE6rtzzCRUlnbo@}J#v&dCXp+VW4URKrq}z35)h%483gN5VBZIJ&ow9X2%P~~-HOVBQk80zinuO|dCj4>Cdwsa0<=7s'
'T57;kJJ$zwpzCElSUt8)@HUWYVBV*FrB8@G_OJnjnTx2cR6Rs<CA&$PlX3~i&6!1JIn{6<hc?9cv@Ox@cuF#W%B9xgiVt->ghe{i?nR<PjgX~qFSf)G@|h?Pfd!_m-`qmCkn`wrjEvGp!&H!VQaN|pSA+j}+Kk_$n+Hd9(hN^qE@H8A9$vK#w^tq^;K=POCnKaaXwn&(o@v&I$7oUB?pAj@E_jkxka32HBZA^xU9qr*VcIFG#be_|QB?<SYuk^yq$l;tc~tb-2ZJ>hIiyiC16?0U?t;|q5Q^aL$IA}>wp7_%jSCSk1dQ(UF-{IOW6;;OWc6Orrgs|&Cz`Gq=3zGzQVsv`?5h;+KKze*^W=hrV?+}dyx)m|T4QW_|NNJonR(IqdiZw)m*EPsHT2YV(|AswH?p_{D{_i@>Mj#eJK;=O-en9AwiTq~{+$7p4#?RXz>>JsvYLMEM@WtyMUoOZ*aBPlFohw`D4V|Qnxs6Pcb_GYMwgBVK1*lG'
'){4mJ0SF)FndUJg=Jx~P=fI_?x$0l(r8truj}kpFNX$&<^Di5Jj$@KzeL80gsISoX<QC=jj@;tGB;N^V)(FCNnOq2J!4vmUQbIY)AJT_2MdZ%55t8yJ0Th;i{+vof9zxt;<MLOYCwJKoYu-xM79`f=g+y7QU4TuLlK7cU=a=onf{dRj#9N7D7ciR)4}GOYh>dyF+X+`8IMaAe>USkXcxxnuB??d)K?kBp!YECcLRA)00qRqmu(N*Br)#ihzuR;_izYQ2`3jQHlSkgS`@taRo)Ca?4QX;9N@4Ha`;quN1w}t<VUvLqR?7_6)ZNQE#(<u|<1n$!K9$=W@eV`p-II`>c%5@m=N!-et*CPYqXke!``f;jsz?iE_B_gcBr6Z;L%p=ZIb~#yOT@uWC@Zafiy9uWf5soPH`O)anA(n){i-$$ZfR+SfI3)0qoQ7s|7=X(2QihN)GRJv|J9EDW?9@3LrK!UBTDIkY(?e1ymppXQLnX#uwh{{@-Pfo'
'DJfkGen|!pyy(2^Is&t-Y|nn)lQO<ZObj20Sgh_*VGKUnK)}d{UDVWLc`%$viI_JWmCd?CRKOr```8PE2J{OK5zU4dD67qL>W+_us+<L<*PV^>1Qa=*ae(qxxYWaw1-qeSmlN_+leB3&@pyC-UHn098GGxiJIEi2;YlRWEeUHR3|;Iy@Da)BAf|Z?<S(c%CPs;UC=*jaO3D6bngQO?CDy-ilSQg6N*V9keNkm0U)Cl6Sh{5fuBl4~@qjFys_F~rZ(Bgws5$Tt^deDI2^U22YW6_VF*h`xlW>hVNRY5}2zx8&2H$+IYGg!>+$x40hGBF>zbrrDk^@$`gaj;2gTeX>-gE*P^J76a%~u_Mt;=CqWZ<sOUHmcY1R)b3O%^#YTASXll<ak93tk8|QC5`UkUbDS9}wMzf89nfVi%OoWhcforGUUAfhGYak-$?iuEKSgL-QhbAt%~=+2_4P5+tVn=Lc(LIh=*#W(sTX)I|A!3!}sf<(Nt>?cYBE'
'Y*Jj%kmp)>VB#cqVrmzzoxn!k;fXjpn^3}dceM0Al`@PvEH>{ur151sw!qWwY5*U-d-h|<09}jSFGiUZKrKYJ{{ZaWmkux=sHP*=D;IkPHbGxxRY(KppEzNW(Y7Wa#-T<`3T6Hs7J#mm>ckaU2~dB{ClWbqwTz%(A*6K$$%EGl%*jx9M{EO>In-CLd2^ynRT-oHNWV{GBv{LKK|pn@_0#U2cMT3;aO`|{M%?n$HEW6NXuAL<bAZcH05>i=#sYEX7`f9<><sof_UKx$sZC$+=WfA9y?BQZl}3?xs`_w2?!86#cv>ZD?|OFH`NQms>rqzy(^Jjub(!-3n*wnI=@tw)yq&Vl-z<sm!S35dJ|>R<cgBGxvo7$jnD9xm*NvI*HCRylGm?znrNi)1#=b8TaRNMjnsXL~<kogvWzP&GZPZH&C2x)pn-c}%R_*HvzdM)JeBb9LMPdu@!7L2l$1Ghuu?gk4uDx^p$3V~r5{ex$C0`P;szqCmb-~I+'
'8!=OEX^n=`1YmrN@?z*k0I+L`nR?GWHd#v}qr^GYph(GlWIr6!ash~<dfzPn#ms_605Nz;A;CgC5!K3dE;5K%963dzR48Q!^L2*#QF6L)JH8h!c)@rsLF722h>{awu8Nb!_1wX#*^~6Ab*?DStbYE#7fL~itu6#*4<E3*<guMAy!{qSw!!!X<Z3;CXOMe?O5=-_)CEMT#~V^F>R~eEW-w6lz-N42YHECE1;ZEZ161mIy??}bQ*IQdad*V*^BZ6+*HsgyiRwHme|e!#Zg}66i|J?oV%VFll)BVma$wih3}Xq1-^6YfqN%A|L|0lxLoXSR%E<E?;>jp7kwor4E-E}U5v#X&_CH8FY^EkSe<8oWVMF5v0LjBlGFV4Yk5|_Z2+=1DYg*H)4vN@fI_J_Dm&9MP<$n9}q1wh?zp}9^Fp*<=tuYGZcIo@BQ4k)B!a2ul_^~oBUiC}hYKu3=!m*cEzqk3$8WrJ8d-=<S9|OekZ*3&P6U<i=&=@eJ'
'6U-E5qCdYU5rg8CkR0iC7MHN-UI+I7-1KBWG<u_P4*|08)bVupzRW;B;%)yitBfQVkzk)ZT3~!EN)zxr_Y7?i)B81Z-?u&Li@l0Pn@&|$-EIIBHbxrl`Qt{|%X_8p`l`pkur!_qLC?aXlR}u_SpwW_)@$qoC2PGx@vwI$kUb%JbSkTEgjuaPRu~I*Ci=M^vg=Hp!B9D!V?0TKO9UQrdse|pfK=)CH(J+yh7cYn<(<U;o80$k9u=MTX@snHQMO{;n#Hh6RGM&YXfEchxPh$*ljE=Vu-U$MP-Cjw@B}XylSO>vmUo6#0~7Txk5x=;rsprt7j)O-b|`zG|3dlR`dR3$D$-@8T)>K+$E5{A`%6++DF<E=iwQsnNjEHbOJz*A2ry!YJ5q!NGi1bUAABPZb94YV`GlY5HOCXOC!YKt$cS&n(q8_^r3A}KuZ$itrXq?%ie}r!K3CB^{X}Yk=OA-NToI6W)HsNtC(F<z-nS-p%^u`?PWGjM42>|w'
'>6@n96s}-_V+?vp?aJ~rvlUxodfzYYiHG1s#7*<_0#UTW*P{1o+>#l5)Rb9)-a2}NJgBe$^g4B@*^rt&RkcXGBM1mH0v?drJ46&)(Mrl;m32>*N%;A(TWz}c26+$zcaBQWV>na5MM;PZxP=?%;&??18(ZPDDj;s@TYPCMlWX>*i>R5{#g6&p{y@^Rs_4fuK52b0`ip5uG^euFQ@K4Om1c(q-Lg{Ip3P|8H^Wm=-5+w!5BYbUC<A_bHhmFI*?cwE#|D_mNigBSNrzXh)oQMoN0*E7S14A<0tmB(S&VcfKCnU}ud>KCW^cDgb_<tKk&>5m%pN`1V)x&9mshq=?&&TIIZi`k$~YsIE;;w6Tl{Q>3-OC(D?`U!o)LvH${?4Qq&Hw3FmQT#k|m0;Zir4tND8k!0@Aw-#-+sE4`@8H$~H%mAk^?U1F+kpT}k<X5Es&c@aMw0kYa4aYKkR7pSsq-BJYQ8%e9TO<#QDhnl^}#2{q<lfKWyt+%lts'
'&l`JIgWSitBMlaPDzIK6+E$*mcwWA8R#S53&&P2`sZZ6=eix_+q!E$75g6LaU4IM9l*sSq*|Zvl*4!hl+%@86)N=*T8dl<Mic2{igPA4OGct**8Ljif^YzeG7phTSzpn_1#;eocbOH&T;Mlr6Lf(@GrX?{h)$Gb&o4_`@{#&8`s5NI6*^y8Hi73}I@i0A$_^G!AtR%QSxeq?^pSBiLnoqip^%ZJNMK&Tp(pc9G8_L_Z6AR4gS1FF{;!D76O205+D6B}8?yH!=_u`+s;i!r0I)1Jc%qiOWM_6Abtv#WfU20U6yW;iE`7v;F7WaKkPhbwpqvl&0qdBey5caqr(Z5f3!vWQCeLz`jLt^vkd?GWALr_Q54x%+ofTW+2_p)3{vfj!<yofPn_H4}rtsHlN7S3IKU7XM$sfk%uTDk!hhGPeqWsIWLE>pH*KqytSHz9v@)$g@YTEp(+A66N(;32q>du+WeCwUiqKKq5`tY#CY-o;zqJwIL|0MgT0'
'AK7>&LkX2Q3oL|56I>F93$$@?C9mAwwFV`nj;@9tp?Rj#FzMpX!!C8okRvX9o*oA7c}$JD>U_QPD^r2G5Ri6gyXUS-FM*6XW(B&x(a@G(?9XUr`U#2#lRbvVa*L%S4?-Ho9%OE~MRBvD!PFBLbeaj|N;P$Z`mX)?+Q-L7;Gb`+8rC=5{glk11n~s9(RCWxQ>{@xs1&RLj-ak2IFo>Cse{wCK5yQhIqv+s;9$Nop6k8VU~7PN-r%ko4Z7~0e&$f113Z0c)}rIK<%Do_3kvLJ!cO>%3LE~|Y+QaebhcA<bei_R@{@aclgocwOsa-w&rWYoGA2^0)*#Y8VnGjMgs_iN<2lA^F*=HA)Fh|?>A<`%P4*b*X@AOKx8=!_BX^dc=RY8(_D(l+tb;gfN>6u`wperz7)u!0jzlhh=`o}663`Q}dcZpb!HGicmfp9EsCYWaP;cpe%K}NIo+Z|EX3e9;pv&Q&<BUkdrwGT`Fer06pu|WNeo)6a>Oo5R'
'cNt=YpG_1-07n|N)3d|IN^>t4I(vg{wLifOZDcxSQ0&7}xd&=w^pa?x;1=DNJx1tJN8M-~bmK-DhFij<ay16Y{aiUMHda4P-iv^Y4)MiiX+(+Cmkr7%&i}Fu%X%qB*u1+DmNWTfOU_I-ve^K6nI{n)Hentu;8Vo`&CkSBn<JA_!-)(>U<<;o>%-37-@Gppa7?>ldV>te-GtZBAloh|9K)~`IFG-Xe-)uYl^<Sa>}>fdF;2l!9#;BlJNm;G2bKR;Z8@`|DNSZt0sj)b8pgh(;U<|JSTAU-A`X8hli<k_>zUiE`?9>wbx#i2wijIL@t1KGVN~Ya^qagGM|{ZxtUz?-+Z&xj<cc#D!h%(t+#rzuNlOhHO8C*-p3*N3U?oqwDTXaXh0Htt$hl`j<~h%lhFM-m?R=PX3a!CGLP^~pGl~JbcD!j}u}AX|m$UvcB6Rj}?M;ifluW*LyZIxkvgo_`<kEwqq+=V@+Lv1^0NdJz7B|BhTyxa+70?bs'
')EHx^3d2Shoo%U4DDJtgjIJDqXm`vcYrU@+3b~@jj+gk`Ok%1u1*51FT2@(LbxTU;mw+4EUpD71{y%s3SwozKf?p(R6VoqKpOFcW3IrhBjt0K+(9>f&48;@2*uuo!wt6UQsWH%KH-f*LlZ6FZZWT)-y-{I2>6W6YdoB%qdp#-d9*I2(SK7jdpP`)Ql6a-;DhN2%*R}8K9sCB@9)<Lg$pSKRO33RLKI0zAkB)`dn*?(V%3xVm9Hi>Z{)P5FQ)_yZP!bH`=dn2{7%doSNjxShZulwzYy;vtwMh+E2y7sYi0`&!xbXVhSNL)))fNsHAhYr9fC9;Irze)edLDZ-1vQc<(a*bm<Xk#MlhwWX_bk|GUUECoaL5WzL1^_ei(wrcCgVim1=S`33Xt_#KL|WDRt-x3_prd2Azik@?ZxUhBJnQm&+DoIZhfb(Uk@8G<so_G=!A{w+XdD1X2QoLpA)qjTphC#fbND5_{iN2Md&=$x6)AqZK6y-Hena4'
'RqgZ)jxlD&o=TpY{`X~PRz!Xf<;T66{8f*tcQQL>Zq*(Clg1EB-oSrz`;6HwA)RO=Qd1$M<hxG+Yh;4oA?rn26DLk!>z3;`5gIVDV@iUjcFZhPp<aPg?!C<fzLIJby~Ax4mIh*xDsMxB1M1ejBg7Mel><-Q|0q>>NotvvA9s+jCjzPrX^G5jQJTXs$)NzmR6WXDc$q@6rhz#QKaem%_f3vq;HIwCasZwqh0Xfr&ful(o^nq$qXG(Jp!=JMR6_N4?Inw@3**wx(WH~W4n8laZWJE2H3}y)y_jRKn;&x~b|5gXhr9>p^+n&;meo6KnMb(peXmnd2ah@kM)LN2FX?fem;YR%oLPkg&jRQlMn&JO5Gvb8b+?4^fB6_ZI(a>hwZ^tsseI@KGqfwZpvY$={sb?%#ChR|)QZnDvZPw8k81Z%`2I5%{>y4`7AmEAQ0?(09=q3y(7C@u76g*x{Yyc~+%UWTbQiE(GY(WykI*Nt@6}{1ll^J$n%Z^z'
'uHZhlIrqZI<OUip8c}rF4f=5x2q^<S-BP{QXnLZ!R5x)Lh=Vv>)#d;)WjpM9<x?n==cwG(M_njuFBZWFHp>4}k$9Yi-??IdIxW4t5l<KS7rQ+rfdpi-8pa!_DVbRCh3ok%%kjUC$sCInOQ&2XCKGPk+WV*gE{wk2zLE-_m-1-gLfq>PUEo+q1?>%-eoL2*@~W};`73nV$?%D6q%T&!77jsX?g`a<vR`&}tz%T1k;B@zMNT*iNYNK)b{?k^tv0Ww$ameL+RASp$v{~los{ZeRbX!toadBg{4}bb?}!x~JwsmrI#32RF*qZ(H&l^Lm0T*aqvTetLJH^)pg~8Mo{G&m&oXE6v%<lM(C_8jif|q_w;qlKmJPVOmn_iITa)s0nQa=J=p-r}(j7JRp+M;%P1mhcX~G9KN{F#4&FP=ISuoGNIP1t|VvLZ?<H5z%#)xi2Vn>!GG<d&6qj`@0DcU)x?73ceOkO}piP1n{L4k3EiP``+rI}USZD!Qr'
'>LM4x-5>xc^+0473AT<^6dmqmndn-xa5)F98`^GzSg=s^{VhfR$;Z~O)E!Bavh$Gf!sDXmC4O|$+y--X((n}b1CjjvJi2k8+HrlJY|Wps>QT4UtF}CYFfB;|`XJ|dq~!?}992JQ+_YJ1E&2totFB{@)$w7O0x(}KO-CUE>9qdOj^eCzi21JU<`xV}3+(0ZQX;<x^*8_%<?6M^+xfs>2s4#?8Aj|A7p06wVyObzGo+$E<%!>76qh3{S+vH!92|U3^@z0`{!%(#hFZ&H(|IH_{nz&}Nsyp-AWP;02d#n^OvsI7Xb=RNc9er%dd4M%imiOe3g7|E!D?{8X<aog0!uPy8FT~lNOalH2qi>aR=*aXt&tVQc*h`N5q9s;-rAdL>V|rDAv7nwt`?co9t)yaC;vY^=tGBg^>bUC{%#u0laN}?2Z<XYO>x>*Urc?>SO>MXN=hmJ1Pg?gEa=keWdcvL1Rm&%!JzL-cPD>14~O{Mqp%i!0k4JVW|+%)'
'Lwk)MYpRmkV%VQ%XXt-P(of$in*Q*+FOYdAIt8(UX+HNcCVk9h@)9p9UHNO4?kx^0A@NPcw3%`u3J%To$efQN+`x|Pp5=dn@#_e1A#N3is<5lYtoBB&TqYgu=(H4P`xcrT3?S|)w!9>RT%l<_`+s_!Fh^S5q~>2lwW)wt9U10NkU}wObxkc#r8lq^DbsQ-h5}zJnXt)t;iq_ek&SZHcwR(S>Xiv^qXyqERF*w62;=CY;0rpQkRyvv(!VxpilEX9#kp=(uy!!Pm=vmx1Q*)>sSc_@Ecm!HD_Or(#0}qONr_b<%V6-BS|K6KJU{VPU2rS{+D%ZR#3axqrv@I*Jd?EU$K6@M;sROgK7ocq5lYMn#F5j>x>3hyo-8Q<`o>%4#l(sh%;Hym0!YhYN%iqAs6MoJHxO(OV+=dSj&!Mj-wG*hbnBPS5Ss$XVv>Ycfzq~}$d5ToG5~lzK6HrZF;<h*zJh8!k`=a*F#0KKxu}5%I@)Y_o0~sIhcr@}'
'qo#D7gpk&NuPX*s-B|7Z@GExiccgfcBQ*A>*#$MPTS5Vhw^`C9nfp?vPl<QToB0%9fh9v7@W#KE%Zr8469a&vRP1pT8OYIT#Ni$R=*d-YH5|a>1A(1>06ADKWVH$$5+eCs?ZSa-WBGjpUy$enEI`7)$#Rb%nd+TxG0Lk;5oCv|V7GvUf?ugc@|V3VLU+GR{l74n>r?^;gp?v*%yTJRmzG@%4yvX^h%OWE^v3b`1o7efq2dOGy>{R$drn6l`VeGbYT7DprfUF*JdFp*JM=j<B0%zUCChTB_*<n*udW_5dj3-8kR78k%w}AP{=Bfv;6oRt*I&5Q57zDQY0hyCe?!&&OCB5w^~5*VH<zrh9279sgAJC<oO-r;@0T=}f7%;Hj=gVqARU(_?%03#{(IbkE0;Eg?9wt9Vgx4lgZ3fkH*@3=f|V6eu%DK*^J5VUavq^p4jKm#1BOI+7Fa_CDG0m-G@*I?_dwPT2U0LF=~a00bZQ_ou-fvM7U5yV'
'Q#=OVgCLh~jevxZPq%26Vg0rsz#E3jEh(dLuo;i#9~FVqJ3_46QM;?KY}OdVdZsz}m89b|2k69SOoT>!^RfNNIf(0<Shv!CI;oDY<AI%XmQP187-qBO{JDyfgs2Hq8y#AH%srThInZLwflz%Zf&-_edECJuY9f{^1KP=#BBKGz%#@Vsbk#f!YZo%H?qrv_#%iC_s~u^yvNvMdM}c}H%)3zV(bgh)tUK)ZymuR8n;(BfBNMMf{cxe<9mHw5LN<||S`9ST>AVHfCf~;uOJsRoaz2>MGU?a~;NN1t=Kp^R27>mevUAZ}kQf4a=K+?IIYF<$gDz{%G%?@nSkOgyMJix;I`qcAAH}FnhED0Y4v2mIsMbILXNU~2pOd_c>@Xy7rD5iqqW8k4Z{z>gaj};wS)F7Q4dno0g6)G>*Qu`V&Tt%^UnEw-`lkH+!0>Cm&eZA}`QTelYwRN{Fxgkvn^98fm%~>Nd_Gui&Nr_Cw0J$y?O*0dg-yS)-))qt'
'Ib4N4@Qpy){EWMtr!;$rocK+)r|F-uXTL}f>RGRZe7FmI>U9~wXkj$Dd~g2!sG@{-N}#R`wF}NoWO`UujPR2Ltd~dPcK;o#xHhq=b6TxQ<rv(h{8~^foogz%|C|Xl#vlgtc`Ky*9sX(NFjPh<?w#Iu)Yw}M?qK(#lvan(K=h6$RfMOgp5yjwnM%FudBEPZ^MVdMr(Z&9c+YWs_IOpRq&&X3vjGCKw5{8Ty4IpAB+ExAlVvHjd)eVjbZVqVJyx~Bsbqy+tt0SS#qU8W_#hkoi^GuF_<Z?s4uxX23@F_Daof)|RPp~2+;=|L#J{}35y{QKLIatP@C75iUTH=bYQFE-0V-xHy#uJ3VUD1C*_1>!t^wtIXM=T#pJul}hRhNYfb>SfIN=*(@d@iX;^WMiIB37qbvSc8=n@Kqdf-`~bteCR%wK@M*_<8m6Nk`}th$+v_6{1V$k570fo|WWv|XV)m`@4CyndHsuocWzRdoMB6zcDAp5%o4@SG?s'
's_!*dxmwccvd<x%^wEnKqWGcS92S;I4LdQ>4~s3QM?P0xbR2$mL8jn6*6o~S`_SM6CyIgdEArME@gzS{h_kPSFJ4selUKYp;~pXTJ~{YCKXMKaeIK-YK<hu;{iCy?D&K^dDzYiEyd+EW*Us9r_&O(Eh6^0lh>XOFUZuPQG(;;8w3KioNIz_1Whfo2I|Hi~M#6TVbBA4V9lmVmJp@P=+2RY2Pv`XupHu!KU|^>Pm+5102TcB)YG-S|x{Dp>+vJyN=b<B!lno?n@06`el@dw3rn8Ql`phas<rtU~Zrs|Vx7bxmCOfR@q$?VQHwg7co@E`v-5sJ*DQles_HBBhd>#xmT($SUqjF(k_qxe9!y^tX^|}64iI->^QRl<Z4D%~5_f*^n`U!>M-t!+^d3b#(^fhiWQYe|K=125c#ZFO-wum697-;rG`xzgl>+ZzBnL-ia5bj<QtS4nJ>mL`nVe#@X20S(&4mtppnRcjgJ7Yw-*SBUOpp%jeej{MJ'
'$Y$A+(*s3&X|vTR1sg-GwRkbWM~u-58tgb&gAl^Jy6O_%LZmiVI<Kl&Ts{Yyn~+3+seF5Zq4N_2bxa#LT2=X)3-B!Ac4wvq^fN5fgXbjdU`=68_A_g*d3ry@ve8?!iGQ7EO9wf5@QUCnUtgCc#>%qP?dsG_yLDVPa&SeNW!evGItnuag`Jn^VMudO7IGu*L|uCn?L`6IP%_|S=qLW6EI!;8$*Zw^z+mWp5Mmj5nM_FCcRHKW-0A8|7{Ighbj+3O4Hi6fbOVu^-f7pY{OwgA5+G^!;thuQ3oSkfcZZ%hGSa#6Tn_mKTw|><LGS%ENEXb^@`y4MH;cenTX$*=eZQWLJj?4K5LRrjCF6&`VIP$r#IaL@a~KROV1L~%p<|s;@q;CjxFu?)I>RrKXomxt`Ox9nt4D74w9@uLPEBHD`+w$!1dE10@Nem5t5<ITd-{Q#0K>wbZT?^gq~%iJ7uK@^3JDYAIY<ka!k=%qJhkk@n1*}St#QHppYUi3'
'fRHghiV#V!$jY8Hp1R5?d!AX)&DuhS_^r6}Nq@41L9W@m&7yj(3|q#8!I;M@H-8}{?7hsF-4kpY8(*zQfqm7D-Y~x>xump>EU|gqhGj@@!B~;QG9Lit3n@3CN+l8y_+Yye({rQA6FXWw;D7Q<^7rFS%b%ZUY7c#014-LwBe*Fny-cMp4T(HTR9WROYEP-X1jrR}V>Tf#sEQSn<8JRzKR^R=D9-NW%pMv3Lh@X~Ji;;RcaAH03C2EqJ37&Ai*mAPMFPri{M;EH`UsTiDOD_uCO#Sl<<>XLS)tt!C}&JGV4?!$kfNE?J+?YhM{3f$htAk3Gyy8wP#X=o2t*VyAAe|UY@%{>KumUT?xd({Y&<JyX&jBqU5v)hK8-aFMvxXNe&D`iL*~K4X8_23EnNo$aCsw}Hq-fnfC09O`<UKk$9f%Bp30sqqL;5x27&5Xmld^Uute7g&jUxrQc~ttti1YIKA=(f|4e28Gg4p3RWKrYzQMT!?EiVNwMx3R'
'^+vfOQ2?;oOk+r~d8G(MSrg(Au@XSc>Y>u4;2VF|_vJjLC}PE&tcRx)r04xEjmRvt(%wN_=!sK$CkdXL2}+JV<UHg92Hzv?((3`fjTwG66L;$ep4Hj&40;B+gsYs0|21C-`ln)33JcPGFKOoB(wQ6eavO7uo%yl{BZVF{8VgX0)d>YG92CMBnLhLa4>EqJ@}G9f1fJ2g6yf}_^k$X{U6|od8$Ueq0DDpUU~&+0{!R^yuDXduH&7B2Df6G2%u?BaqubvA2jO-V8WhhL(;`0*BhVHwD>ea59mz#Zb~kb#Qkh6nAD{<mI8QMD?}uS4(R{tqd$OO5OTbhf`v&LD3^nX1+|COH<n3=E&;@0eu6GEQLT)jRcyb&m8?MR-?hQES(Q_mYOXbXn!j|;>9?W!5ekGR#h~Jy%OnG!_W=;<@S@{CvB)=fZ`cG5Gywwq&_3Mq`8WlExv!)_l@@;U~BuObdSV_6~nq85W;Ep5w<RKvRppJcgjR~`Ar(jV8'
'by|Q2^uUPZz|1WM9D6XdRtRx5Dv9;WiV%9dCpNSAF!cDDL!O3k#G_GC#5Gj3OREY<p(L;^_ANET_A)%iOZ4MzNA=e^fi7Cg`za1V@HFJJPvd(c7WwhN-+90vOW0B}SyMl*|9r>|JOymPzG|(Y0EQ5nYY6=wqg9AHd!h^L|6<et%0iB;M#J*c1*a-z3r*~XFFjiL-PhD0llj~JTb(M@v>uv1&O-}E_`V%Id%f8Y&L5Zqa6f&6SGQP<3)m}1*QHtZDu0;L|LdcF^y@3mYew&R1BFqF5g$<&Xsg$dq?X}w0AS3g!EqNMySbIHy5mjE2DdiE&4hAge08Ld7_Xf-FVZNp?V|*Y>kThOZ<W)~6RJ%!A^%?Q(h~ZC?k_bgQ?;?FOwW|qP~4Nie#F%E=Cb%}@wO4ib6@4x0jn}#xiig|zCwEm=Or^|ic8~8m;Y=gK-L*-ZXKhcE4*{OS|+cR5v37N<o##s=y>UtK9ULr&CWCRXd*=9E(H~`pNI5?'
'o#6`dS=k)0JSz-cKF!J>7+A}idyGlsg=F{_M)C`d2QZ12<|IsYmVuYnYDO>oI4z(wP0Elh|5qY3{eBa7fk^&J?T$YmGJ0Ira34ELz~8)~pTw*z87g`FW!=S!2i&ZMQ}@wfG3u}`d1J=|1aVu3>OK_nYni2eB?VMx`dtSgbw)7wvxzi3KDMLgBcK!sA5aMYR|e5iyT=&KHG^ztW?2<Q|7jnr=Gk`^Pt5vLJ3C&l*h=iZl*QU^bHc~1+}(wUold27IV7pg9E9H@jt;afLG+HDO})SzQZ|oAlfbOga8Fpktuux+XK<UNe$WUocac3E(qd9A_vr_sh+|x~O3${7wTLSvzPm1p*WXQA(tCfN6@8EB8&Vwqm-DSJ=+~c3h;AJ6PZ>}-(@k!ceLN1ADEu0RL0PbrZB`Ps_IZV;5T<`IbNb>U)NCCDb-;)M{O8|8IXm~pcdGvLlXa$vWD<n@^Q2f(Iy1x{cK)wCkPyqtlXrGUvQi3$J~<Tq^szt9'
'bJV~NV@zYvJ5w0uTOhLbGK#?&t<(ngr4pC726j^prcfqddOZvb^pbG$3#CxDH66{M!Bi!PqZ@v%e=H770p>G-ln`g4$k8L3+$&#~2KxQ_V#T=l&{3IeEVIyAJ|F&fJ7<zVqn6Inuf5n2JKI=AjY;d+_gS$xrp@ofjy$=iy_5}`vPPhaU-`R+3|X(VJ7oL~St^z1l@tCo?Qio?PzZA6ccPXOpe9L(ndzMi9=OVnF8eJ7+{}}$@xcp;q9atCEca0E0@&Fv^!9)Cl^1aaEbA%(C9o|Z^?`G}X)G*#Ior#wbwG>!w13a0QmkXfiEeC%mF;!F)#L+g{HTXIgUM0df*Rq81$TfGss;2xm@EIn|A{1E5hPP|Sfm&Ah>4CLTASkFsVB&{9&8Ln?FC8UBo3=>svp24BzA!URfC+AFJ>Zqr++WN>p%iang)zg)lLK&QPV^m=N-xxqoUi%5yBkD&!Mv?!r7Ik)GC!2FmRf!SQlYZcp^C#bCIMX74w40'
'jCBBtxvG2_Y(65QAAB#v3eb#bu_5UJj{oCeD?;4V)^hlo=!lF)i{c*Xp3co38={Bxk;3JH&#p%iDX10gy?+<O3@hEeK|_Ok9gdfhx{Q|{D<De~w6*gUclr6m=eZM0?r8@4iRM_y3%=)D)_x)k=xL0wXK)Zl9nvl?%*k+^lq;@9^}Ez1$6uM#We}b+jd}KG-amwiaz(<0uuL=GN{kXZ4ANF_JA;lI&U4{{?Ex9wfJJ}Poldls@g<gUKd2KwR`?Y|tQ9ad7-<x~HTdzRS89`gsz+j0ZwB_pHtV^o<Y*<{x;N4|rq?65B}M1oB*d2>Z$D;>3-qxQ_GRH7TRDn)X{l^1%h{oK@tor5Hpr4lyt(q<^(lLi7p!0h4zIdet7?BXwE{jyV)kUO)Vi#lonsK|C|JCVz<_3H;S(jmf08(m3S;_>Vk&be%*r~6r>pZY@SF<Yo=!==HvM``oL%lL*C|jMfKUDW<^arzT8$(z!_^Ro>HsYSv=d)=C*?ts'
'&;TnE4ETTw4&~{PW+ggMVul`1@%T2nheM%AU3B=-!4-(4v$JGi6%fi;A}r{s(Cdr`lIu!l3zE=ULRyeH<n^V&&a>XAr&ct_<p&@vQ{`3D-Fv`g*E<+Tm3{JYioCW^nN=V0abtSUPAbf5&fyZGBS=T+&t2&mNHL?7?T<&u7c1@-t5T#f@sIUep38ZKn*&p!A@YTF2i(DB1J*|u=_!Kv9i70$Fm0awuRz3Zc7qT!P*t7-pFt0560RZsISQ{loasl)izq~&3veJsiG8!Gg&FxC4kqk)T=odR#=-IZMv3b^0MDQ#?(p(1cxuBYcQLr7s4_%@>L}P965)egU*hSaH~j!+`~;A2wNA90)~3X<;G22eopL6txNY)_NaTgMcqLV=px0tBcdayRtVk7%qm*4;SCI-bc6%0?fXxy25B<?LHXitA`&8fgBzLd#uC4#MDNea+EMI~HtWd~dORJ+bR3WZQ&}T<ep$T5TRi%Q8)FKL-y^Bvrm#CrPI97&C'
'Xe`=V;hn{5K?Kl#ZAr3!80@hxfK)g>=Pr@D#e8}|yMjl{0jM7WF#}Vtax=!ZOX;5qV)yRPak!w-%Li<N-tAV`_d3qQ*rkQ!ePM?q=6z+WAy`G@q~#_uP9&Ao1{R&qM_3E<MWz$ndm+N&0v^w!4C?_Tp>etlafhn3$R@PWbh8{!GBf1maxc?te&y6PP(v?{i%{7ziwpt&96SR^p2v{sCpm|<;FuSV{ub#k+dkqv`h9v1#mSuR3$!w=i;1xhQ*5Q=yAri_bF|XKYL=_G#8)9>v**~JHo1ormN^ImqJ3bq_r{MyE)^tZc7DPS=&`_C9K3|<0h;iN!r+D-6hs6<nQFwpb<`E7!AS(e5LjMX+l0c&jS0)_^#-*XtSVORGX%4@ci412;)l2pQ7o>`l1*@0Hr-dQEOSj{I;A0VIa$GSI?9-5dY=a2&u|!MhQLY+XNU(YmF3h&_QWckHjxpnGX0OAIx-w&wwM4`tfeD&>|u25Y$eQ>leO$jWbhB<'
'iUsCjHx62vzl~cJ@e1hz<R>l26jO`*4I7<a?%H&l7?V%safkVc6M-kb_%t--N1`v+W?s&9A#j$PTpI#vpz~iOI~hMvt*Ro%j^dLf3$0!hr!bLOK_SkrWZYNb`O3$wOee~`Yb;SQnrE<@P}mr1DP8W1`fFIkSH}Op(?Ib2;e7fsB7m@|zCZ3|e}!geXW9tKS|W{cuXbVv8(7+J$PAbekfIUmRB}F{ofdO7*OU(&8bVE+4L#R@nH?CZR3GpmhD>wAPWP@EZGYm+51aMFCXncPSOb}6@A90jG(eY(sp7+0{;NN3Wh?fbrD|sD{_eln1EjMZyo?;$Kt<Dc?_^<8U906x9b&!b{=68`)E<bEPOhO5RwZceFc^4WslTyH+d|2tZSm1!NZww;yyg|nk65OR6|Q{Ah@am`<|{zaVw>YP6-i3@hm{%@6(Z{9gXgmG_XZ1weHkZD!&MjiAe7Q@>-U?$B-8Xt(Dpg_IJtyYU(6|!2MXi&hI~-)qfz%}'
'W&;oF=N+Eh$Q$mGrpx3TUUD^ZNvMSi9F=P;3)N_Yu0oR{4FR%zMW<t*k<=rVnH(E3FGrP3tuPupRIvrTo=nQSFrbd^GgX*EleYMHEZv8`Hh-iBAOf`^LMW%d(y2)GHDUQ4A8A6WizzNS-_2~%iWVy>18SzriBVtKMtNf+Rlj>eFFpUsCf?@TVFf0=5rsZ0Y-<5Bg$7G%ZNFp<co>_2e1*~q*0AgP;whf`T8r7A0A<gAE&nlqhhebEK(~SCq^acxR!y61p?dC*^PU%<@O{$Cq>&}Sz^y>C-3y!3<F$qW$rKtmx#ZPGcuQ>gd6U8^RT$`nBrXiFf_I&Mymb%yp<FQ+&+0mQ%JEK{rb)D#-3H)VjS8v@^bRP8#P>XQ&RgESl*T(+O(slJ>O?7<<6};*gCpvL_IswF&f93Q-2!eLwjOLR!`f;GQCmVd;SOZwF5o?6qdB%ej^1ndF<9mj^1YVh9+X6F(2VC<(Vf&KA#Zhph)V?r?Ejb2lCB#v'
'{dyxffuz}inA;u|@*JBMmye@hFV@F9^V#8O(Wv;ZS0aBHe%6eNN%rwdl;s(q$?^Va^oF#8zkNI&%~o)Ld0_(H4=m&Xd+RCsStFaYVVm+G`Mc6=N<o$+l)iBGYhZJgwuCuZVORa_1L`#8WKi*vSO5)w@%dJs#K{~Fxv-v7>HS3y&G8_2Ce7Jqi@$3%+h%$4Ke`$fLrmV;?98u0GN#Z%J6B?S{w?3v(Ugmh+Jwn4x(zh$>g_v3woZDZ!|LfJZ&V%GK$(n+hWchx_^hkMgwqneZ|~`*yZEUmn(nB4svwxb7~)4AcZH}RiO~^DvD`rfIxNU4Us&1kIWw%04%LV=h=`KS2D(HnX4K5Ee022U$vbD{6}gz$+!1SlGP*J0ZM^#tVLOc-5^dJS1x#<lHbyGIt`=}KUOELaXpGFOjhejm??s~m{?BvbGVzdW1&M{|@la<-!PISbShy8_RC^^FOqo=Koj&36Nm*5(Gy}w4UMu^*v48Wp5Dov9Pq}{J'
'!3lcgJgpKD9Tg6;gLG<NI0b*?6~q2nvyV2fszNN%u1iS}F;UPR)(D+Xa3iC^mRKrIsY*Ce7;#<+G!UlJq7+o(WG}=h^PIK{ye6k+Poi^rEai+Wo1iS&MBr{H4C{j0nV(jL7&EnoaR(5<Au>xo=|h=|4Q+$lENm?-xP@d^fY-H2Ezan*Ei>^z2L^nXIqU64K*|*H8xB#}@y@<q{6rdMx^HKyppKfw1MgN!{^s$E$(qOlY~B@iU$S2obwr_4fG@xDaDN2P(rk<5;`ulZi1VrV-GeT#0)QYrG6_Z7xAI={iN0Es$i*RDFq)=wRhF!4$5_t|R>^hzKl@PNm7p^SSf^lF58shj$2$=855y3BMKn-`*S7^LNR7<+nSs)W7>(&od3)+X7k!v3L&b(uF_FkN`pR!X1MC})BT4g>#b6v?k&LQ~{By0aj$U=3vs3TB)mm10n-!Z5P$um(L*L()9u4zuNcb@8ms#VLNwDWBEBPwfz4|=rU}H2XBOFG6'
'38eZ+&p26V|DPO5m9u6KJ=YyUf1*x79&2=3LaCa;)DJqC%f<4_0??aPba=fr`YZs~puWx6Udr~tSNZy;8S+pTtqv8G3>YqLho5AMP$I+3!Ab@9n$&s0D6l(SH1sMMFDWp>JF~5!&;zn9kZF4Cy6n)>qT}umTQsR(<jZ4i@H%;?`uAf2qU2CJl$D_At#fp7^ohMF7bO(10yN^5a4)_8gK(M?GEGdnyoEUZj*=v-dr&^H;<x4nNw^MmpNvK2PuAOP<b-sn1DT}kTDTk~tY3|RrFnLrteY*m`rM;MjD?s1Z{FBt<8x(>Xc&^h6YlpOiZeq}KdZrXVF%z!2f3@~U<!+H=Jqz}>#~wtPVR?;2I}&mMCn0DuF-N7jqd0XOGU})<Mk$z23Xcu6P!RwOvUhvMh;5Pa7~qaktyPhJRS9}Nj~yJ?X8cTtxv2E#gFDbC#;f8uA~n97bP+tY7uSf`^5I#c`a7ld~Y#r0|clpSCQQKbVO-Jc%4_aT;cqu'
'cjO21G4SgXqe=GAZz~5mInUE$er*ohbC!n<M&KR#vgfN_GJp3u|7eh7w`1{6|5YzZ9xjlJPc;Jq2X(_Ugt6<&PTTF@Y5EL2Qu?5Y&R)AhJFVj4fy-vp(5-p;<0dj_hqv;`8fE9l=*U>xr#AtcDIUL|7%42GZL{A9&q9cQ(qSY0v(_<!m1G$L4EsCnEiKVIH&Rzh|HywOAJqOo9E2oo6*CXYd&rp&Jp$46u{EbsN<q?0xPV)oli}a(CaX=&R!6O1o{ONB*HM(wNUU08Om)^d)c=`Q{%C)9hyxk=P&zd{Jy2V6yLt_+ME<$WvSNc^eS1MP&wn%QbsFZr87~|ukFe3}?eL{-bBpw!^6p^8N~?i}iL-Xyy|#Ou`S7-@#xR~*61Xp$E9&6JsYJy&NO@*Er`9;pEl@7`v4Y5>!lLiC93w9Az+moPFz<;%$v~+rO3O~b(ASuASHs+{M;NQ`IP;_7#U+`QLqBD#5Y%9dXfo>WN=d;AX{&uMQPfM_'
'R(aZ%fs{C%>cp3Bl8SzsG87F+Bn2eXrSKs8a0$^O^n`PR<l%bb-)V6UBhzorBx(S9`)n)(2r?R0I!C+a%G2$9ghH{n@Z5QJOP~{{k8CK}PA^=jr!Uvd*z@>esrb;#@0xvtNTNpD(&`A^{on@|-c3HTyp2%GT#176B$2E*Vk7~INreY(xlEdu4QK$`ne!<PeaM7Rf4CE04${6cG_(<L7%8|-smkEUKxwCBjBhJvL3G41RJ)s7bY2q8=xoA>LrVnY7J%NKI*i}NKLOGR^EOfsbx3+eoViDho=K)xjuAO*=JAszKP$z-$_&ySe0vb^?Q+@}%3XMz#XxdKOnJeI<8Bcxn!(;scX)T@O!Dn#t!m~CV}_Q^dRg}FdIQfqc<BtjDboVQ5*YTCF4FKFbutu6=SJ}(H74!8)jE4%@1AoM`r*O!Oc=Y&zu3rvG9iL%<5>NDZ&=s?h+WN)ke%7^B<mN`(s2<heA2i=wP`Z3K%ewJ8>u<VMo#3ZrqWtz'
'lh&E~NTaoAFP0O59YMNe;wCFj<m_uQU?}coeZ@?or(3FeZK5yU$#SsZ_;H6P&^tGn{hjqMX1uS40_>XUt!_?XV8RY{IjWG$#t=be-epI7&hx)uULbi5+t$jzh2*RYKYcDXqjfkH;%T~UA2ez%U%Wb8yDo<I+*qszsl<J9EWry(N9w|!lw%jF*-&&nE>o`l>i<GM3ErQJE^gJEtRbo+_Z9x7zx$NHP;H&?bsI1|nB-tOP~-#^zP!vK3g}XKTSt34FWOBFD-3v!LMT@9p7b*4a!`I_e|jRpNl-dg?`A?ZcDw0*dW0xyF5<r;{kl8hiR_u?jM=ilOx5CyEfbllQjX>j?Y$J5*@o#0XfWo{m+YSMrEL%TNXs}`%A%`UrOAyjm{j@Y>$iLMN+QF{XA0U$VJbGcJs)!IaU7$*R;Ef+pM7^3j09weHY;A|(jr0v5+3UXw!c4vtd&<+`}=K<q()h^H0q2CpVM2a>~gRbNPc2kK%Q6j@lFl1VT$9r'
'4h2B}1D5Sgz*0m>z&AlZziRUxfMN=!=KUUR&LA|o3;hXZ{A>q23ddB8kFrRH$N$Q+(_V}pQ<fdPKie-ZO;OJ7(3Xcwq3Aj(#KY^Aa}?D9&^^<_;LT9kzQ1nVS#_lGnBL7RabVlnXm#f0RZvk_4D+IFtuMk%%(7(uB8u8LrkD<EdJUl;yR&J8<`*8;C%hX&f38}me0x<BAj1R3Ep;wu=&j(($*bbRYq8CX4#Tz(Oo|dY5%Fsax<8=aa)#|<?EdQ{bWQLc@Q3|`62L;>cC5(g_4rP35;8f)^zC4>4a!YeCi3|6>MLvG(}K+!IdjW2`mJIda-7MI8wWnfG|@_V%B{>bo@1z=#I=?TD^%r3D{Y=#+N6ei!fTCyxMW|XfOzv=ASJo-SZSMnEtsQGYjjF6nwa^Ee%wZbnk;}Gf`j>ZO=5`&j5+DKA0J@wr$NwlMj-^>_x;)xOOss_?Y~0X5oQh;mkJZDSpTQkDD8{U8d#$8gfiv|#Nuhkk<PIC'
'&%h0wrb#qdfLxsg#QYPwd{tZ8KAKLZ5~^zk?5UlENBZWDs0=M&8<#(k1ZW55H^M~OeNsJz;JWri3`j^h^X;M1YQvDECNZTV{Ylb+e!dOf^54T0%u>FezJ@|AEA`7iw-*&rU7Fz3N;z8=+<EFt;R_WoH#^%a$zK!oT4E%FSB_sHzBqe-n41C}BiE8@l6fA{qc({>pfy|zKO;P`)f9x-d72MYw8t|EMU3Juk^B!Tl)GMs70N^L*YOZ9=V%o2$Dh$$+n{euNJ#c08kpK4dYo7Z*{jHuf8WPMF6kAwJ^075h!jIQYK-FnP0vzZN*j};6|;vQ-t(4N^bCdkydsM(p+iy;N^k?Ybl*i+6;=kiS97kb39%8aG~Ac$HW!(VUC9oB03?%wIM;<~V@%3P-W{L0Hk#Vm*51l&or)p@7ZdG1{O8J1*bA-xuePsAWd(#fb!%<koIP9A&G`vU2zxR=R)V1JMrffom#{E)bhP)<!9k_~1JQ#iJTPC%%VmOR'
'|M}Qi=L31`Ji|X1-RQXyRVhp_DWt681G3CyYTS*q_`?S@W0@3QJZNj4JCH>&I9P;Uts&&EoFy|`Je@n$UWSi-qzhgUAzjIxx;W+3$q%!=M@;R-xdfwSfT<<M*)hGmad6k;yfV|pc1T*>MB0mrGMF~?c&~|wJ-m&kmu-NUk>E`n8Bs0B3JMxNBTlIVkGR%u`ZP(ccIiMX!50pUsYHLjmw>=NwP&eB<25c7I}O*BK*NZ8QuxvC10b50XeY$0=!3_}2%!?&F->%8)Ni_?o3F%jqp-;%WiZulQ088}3UmD=-(sWO<x_j&VtF-^EpfPxEf6*Ae@n43Iz?OdrB!PgIjDxZkx5Q+mQ9Zv)Q4WDn>9R&dzW3^6+``MOTrgie&RY#efGNY^88X9rqugtk;Br;Dd16=HTyZ?8#i9-62N-6AQG8jTu<W8r$){SXG>dg%z;o!*t-R$Jp}3itdfSOHPP%XkdhP`3cdC3Gd#DJ>&1TUAyqb=clmxhPLqw<'
'n2a7PhE9<y%;2_;dNa^3v$0_%k6v$#7UXpUHzu?MYmHo{W^6!{)B)pYnVP6zn&sp?eC+egzIG+7NBJig?1*zof<6)@O<o+Ql94HYn7?K_W-46aX^n6Vf8CuSd3IS{5UXcw<l(|<1?Gj(_r2C!05DLgWMT<59hU@3hl1X<Z_Uvvb#0|${)hm&a+zfTa%`}1-O!0SbZWNS=*o>42UO7%i{Z|gU<KoW1;td#*&TeyvK2Uu+3K@!k3g0n=tYLx=1>dv?AGRM5fnIn^LMxt$+-<RgU;V%J(vu<_A{6d1Jk2wUlw}|I(N|iQJPK$p?ZtGvks{DP$m8c1j3DeNXhM4>jMP#p^TeiH?&kljzu_|R^~E%%A`dA#+8)wJceE*%O}a>vV~Vu*I+_=Q*mnx<8({BeM=hG{+*+P+#Vo!FeYY%f01GvT*U7bsLWiY`B60X1GD7>4;WHG(npX*;FQUIqm^r6!zB(H#WCXQ>2Yyk>c;^X73z#(1S~9th&_Uy'
'7~<$hi&G=}6fGCL{W>pERgCU-3A?K9<=_I>myp82;W*i|ra)bjHN`C3D<>9#`;7qBAxGEJln*99VH@0ThHS_m_Vb9K*sPCD%&}SMv99{xhpsQ<F8z~9OI1M}C5?uT=#2s&+ac3k=|v{9ZVkB%@x*M51+V<BQtCGE%`TW@>#opd7%E0bp5vs2a_8*WoXrnEK)N$c$hS3odL6Yc$YPQTavsw5DaSwp603K{G2Ls>7vd~uoTYWcPTq=Lh3EKm+13&?tOlckH;FMrd&j10jMb1K=K2q>Y^$S5^2AJ><Zt%01L65Ud%H~HTU=k3S_%{!Xho<3_t!X??&rB4Fvgt=1k@Z+m@U?oJQU%IG8A*2RwS+amJ3-mVXYAmQWEsnn<MK78;ZCgtmgFV6dAk<J=B02_V9w;Be*UTx<r{|!^K^499Po2sM+|^;?dTR_<@>1!%Gc#c+{Q|U&9xLveLuP^Av225Tzw`6{K%7q}4XXwM_PUQitg15BJ9Q;g&ym'
'QJ>rOfKp>6tij#6w`0!fL+E6u1{c9{3TS#k@&;v=Y&x0<u-@sKuE2mxa1j{r0;q{nF+`h1(VGBp(o(OPif7qIbD+V<%klf7;F+twnxwYH!_r+tZg9{4-EXFnXKlD6gV+rchvUYk<M))+QK`-3T8T*4m=;B<rK7Wo0|9@k(?3nJ(2t7yGGyAoN9BV|VjEla0RGP)XrBE{Z90-uU1l5DVD#XA+pf{{V#vcRWud`|OR>#0teFKZ{kGJwq76udnmS^>Uf=bp5DoR<?w>l?;@T!V-rRLA>NXzl-Z2tn4Qz`(_O2+IEkS(YOzIC|KdFRu|81x-lpk}hq-PbLnL$%x8sSl$9_%?mMqR2(+1e00Bg?a7^$;V@Y-O2sJ;1z(AU!0&2xH!cyvSt&F206daIupuxb)*DLgV7cvpLq^%e)S&dr+3~P{ePXY*y*JU7f$<f`4Ck^1Ex_M>by5`;TQOUp~8I45h^!1MdQ)F?$9K=a5^E+1@#r-q9!vZ)9zX'
'#<Q-zm*(ZwWH2>~5{=iX%Sd^5?_&{*LN20L-Fvk&3PQj8hc_{c_ANfcRD_>ZH-eOMgc56FYU|`YHg+FKkcHpe9J+z~Buh1lf-Zt{HP%#)x0}g0e@!M_Dl$3yj#cTQdNc;PW?LB{mO`6!Mb9RYO1d3Z0+nI`v|Kco`<y1PN!45;Zk**K-1a7>W6egdXh{hWGj@3uf+`^VIC}GAsO26z4w)2h5(Kkt_e5?eQt}#9`^@3wc;osdT(k+k&S^Nc?+f%&A7$%s6<>>7??fKQ1ewf7P57db`h~IMu>PKleZ?6^;H3TK8J50iL`w^=t84|?Wq~H#cZ5oi3e!xm&hZt2K1o;7Ia$NVhh~=&0reo;Uyfoz%IsZA;d0zN<F|Lp6Il;*5UFDpcVZUYIFL?u1Wc&D9bJ(}P~FE!(mw`UN&s0`T0|va@)i9FJ)aHnT>nz2D|h%3l`^?@xR6_%M}L-EP9F&IR7JPS)8qTQ1-&{gokQNJzs)OeueL+5((d+g'
'np@6yDLHI(DN-F-z_D-oYlOS1!hSx|Q{h2@8~+fu0QQ!Qf=HJ$DE<cIZV~)p4-C*18<ZGG`*wPbt|g)?R(GT{JdIRmkl+1u7!h^@U}s)vsOJRRgdFyvm7b|^VRSqh8q9FzXitY}Yei)-z~&hK7f{242SKGbn*{8Kgv|Yts9JyWOiJ)gV6a1?;a#sn2Eq3lzS+t|#KZ|Hyk~Kwb`4_#nrAzM>T9HbD%Mu!UbhnkZ~2r-@A6Ika>Axizw&!;;8ta@OIZ8O5&Bc|F*L5>J9IBSrBOC&;)koHotD8C;FMmd)WRpSf)prw0i)s0Q9ZqmHP+~QzW_ANh|9vQHGa&zK0A>6&7*hHHR0%v?wqp#arQDxnm*;=3<qjl+v3fT>k2Exxo=%n;W1AFeq6tCghSgcf&y;LThIZO+=>+03SRSQO>`cImNd&r<x&j;#MqIt37unRo;bdOr=oek_lX+`R-K{uOwDbiR}1pwqNHTgTNC!rk13X@9S>7L511#6'
'r8x<*??D^BkXf$=p$P~7gn$qBN`G9d;0gMez1sW9h6`tY0E=Y?E5RZGJ~PTu=#*D&!f_a-?r+K+uavM3n@D94gq9K`@s}nE8|&I?ZFRoQna2%}Q4g7o=|ZoFX5T$oboX!uzU9kUI`Y!HdNX~HYHAWdF&CY^o*`X{s+$hNZtTB@Lmq$;Ns6BJ#jhYoPL<LB6c=cfOA|n_cwOkr{)`9_2gLKW6>0-g+M!z$o@O05+alXj9<KZ`X8LYwVa~nbzhE}GZ6ZZcwJ6_h(SLL4qRQC0<i83gjJ*$&*-r|ARwCk`(aBe}v6VBVcwWVobl(e95&pH*3ua08Q5zOc!eRqmP570(s}I$wxzHk_gg$A&({;-hI37Bh&g7#`C6o*#GRigJhr8e7<x^<>#u}KdR`6|cRWb$@snQnUM{RQkCTLH7o@u+bc{Gvam?@SMh<B&6IXY@|$m5@?$tB}!og0jO!E~ZfrA%9rP>?k|?AYD5jbQ-&82}N2;8s%}lVgM<'
'8>Dcg!B9~H)ckdC^dTZ+;~K;6S+Zo!v<3|EE}HjA<7;v4^7!Ttq|2;96A%abSQOs$0rEN3soy>4!V;a?MEtHIS%A5qaHgGO^Vf~YI|gw6xhojn#%n|kql2<#DD0s0)G6yAhgc?^LxZxBY-V&819}+R8D`(T!6iEv?G-rs2bZD}8LumW@JtX|?5uN|58ucf?>OPQLLPSX3o40;I>s<J{gv}Eyn5;@8d_&_l^ye-P1r3j4t}SJYb9-md#AVE8%nAZ)PAp)s=en&P;$jpico)G*B{0iSghYzzokxUD>ZGv8+WU8p04wuhD;0#og3#2GszIw2UeuO9Xiqe?D<{sE)NqkcMvnaVn5TW0ut?9=$+R%m5T;J$*Ej#3pNf)j2W^!bVnLsfzzEU7LDhMG;ZSTWgRNQj(zQ0;62LCsb(5nYgJRQeYcr0h;w5rHXHS+M;@%ApXMUvh}QbAjIxS->Z&+PTa(F_sm65YZ*(RO@pWHNE7(o4YtraUQ$fal'
';yX6s@C$lpkXykQL^i&ZG~eWtJ^n*7B=$DYUFd!y>77`0Odv*>9Dk4UJiD~2Ar&<?Uuwm7tPi#J#6YEBMH+X%mP)nv2xsW#)%7usp0COM%K{~eNbqFH{u82&Ym#%_>Ju`2JrQ7-%BT6*X&z9n-6!V=Y*D_!Pwc4MJW&Y?%Y<o!j2CA9DnzRV%_{KeD_eq#Yc2_5D7ljt<)$$RGuQBV59V<o`|Z7ahL+mABr%Cs>(YDd@YELLv7bC8S9bZl>%bNE3IhY}*8mk)wgP3BFTXU^cMB&C+wmc@P+gX5D%}En^~iaOkC-`dpnxNf_9yj#c->Kp`n%(0LN`Ddp--gT!JO}&hMYPw9N-r^w1_m>1C?v<>^3M%{Pv!;Ga5Xke_Y!ZAT3<R6TYe7a<a6JDs2qQM1z7`c~RUCTna_tdsBBjWxN#v4Cbi;eq`~W?&Pzb*OXNo^}0$+p&|)gk=gGLjOjEhn^2XkM5m@?A-Ub`doeOG#)s&^?6{1a2#M}N'
'K3C<Uz#X>>1)j_>JZDBWf?rNkq?m{LDU<Y7zc%<U(OH^EZ*Hb}rC;9NSe?JTBKOaVimYU2!f8yDaS^w@bMq>7aK(Kg?YV#s``-AEMI@D6Pty?LFE5Jph356_y)(i7J4A7b+jKpUJy+8jQZDXiWd`5Sg1rMjG*7p#&GIJ;3lJ@@OFTSNe}!;EEGf++4QlNO23uv9wF8Z@!8{qB+_I{+F_z%gO1U8H@|q8#`g6k1PQ?zQ7ch8VsGiQ;+PaOEgJ>KJUl$tl#%m)CUyWMt2$IZLCi3?P5KtlasNI7zIw>{8K32kkn8s(jPiS#7PUAc(9(L)#Q%F2p_!h5x{U!rA-IA@Xi!UGbRVJhDwU_F4vmPw_5D}Tbr{caCp$vF0`R~xs4naYz3a`kUYPN4ZT|Q9HH@+wh&8(-7py9qBPFB{2A#xlj$kPU4{qcH5+SQ59>DlRil7Rv}qxptx>aZ51S5?eaTtY87`W{h+C})cae-|vdcnB8QWDZE;DM{wm'
'8A<{*xe}|kHHkM>4>>-IHJa5dI-XFpGJD=m1Vi6lRw&D4RrYdxZJzOw+&@**!XiCfHn}lI09#)bA`T$qD>j!v;s8Bb<R=m9X59~f9dZhbIp6a{HSZkXqRp+7J!$2)7<f<cK0XD&pIfZg5J5F4Icz{9XZ8emQbGSX@DK=8_j9^kxv39<xG|ak53UW##@1tHMASVI_=-J<V94`K$q$z!%6?q$B&v}l=JnBYUG#)4btybj{@6U;U`Q&c=5Ew1BjOA)ZT8Vo%dwzm{!Pv-ULPiiw1V_dc_%lkN0DWg&o~g!bg+~<UiK-%w<J<^W;y$ryd|Rj1Na8!Q{OJgB`zF4SNWVY)9h`I^-Njy=|t<<R7cuzMcNp&7-yb7#`Be{bi&z6wX7;oeh9jkyWBtfHLTAYvwL>F-Bqu?hau3@>c9>(aOI+jZ&POeF?8;x^LbLNYI@2;!!!$yx08u+l+aE15<$TfAQ%u%FHRi_$)4|d`NWX^O!YdDvz_2{Wb96R'
'dEXybj!CU@XtT&~k%t$~F?+`*yhX*3EH(MN8|bmf=ckkhEbeMJ4eDnVtv9{Q+PK9>QjU?xgik%nCq5ZpwQ$FG^>WNQ(q&Zm9d9GC3|b-{67xKmZ{xId3zd)u1fU7S4^<HUvb6F`%!2LTOq9j~Pv{Mh(+bgLW1g~hTl$I|kt2S%MwQC+poKP_?n&3G<B9E+R)x2!R7K)tAj!cewkkY%rX`(oORjyK_UL^&cKvQ$h#fDMPbBr7G{#{JO@9NGKl7n8p-fwpheVMgnXlMRSl>p0*UB8*V+IICE_-Tyq*HIQh8J$C(DB_NfPp$OPobvZk=1|z1t1@g2NEZswH}UF#qv(uwxAhm<dIT&)^tZoX7rnCe%J;k<WLxrM<RBThRBe!D6CdZprJW1Yb3umye&Xp^WSQlBH9%>e{VyHne1F*)|V-0TTxCO)I2Ltucip3u)`e$X!G~Fv*I9OCsd~$Q{o%VYM=Ahel!Hf)F7R)C-JgWGoRw)=r-g}6-ac`'
'Wuj{BR;vkxti?Pb2f))d)22c{IRG8s>Q(_r#Rrzk&>1L~VmBfOB$f3^1)z`+M(+8hf|i4qO_I}NMfsVLpe!Fl6L4*o;&@}Asgv)pf9L-1J)q_R=YCi*SY*>H8(Ko5%6$Qq7(z^&i<2M;bx+0Emu!j5Y#w4k7C@J6IR$6~h1Qc`ud+2v?+lFp<ja*z*{Q3iRx*USsv12JeLZF1ZkKB=@wL%URxQ$KVlbuT4MSy|@S&Gxq1J(Z5jzrv;~E(ZiD0q8d-(TwbnSo6aC#{#&WnppNArs`>!mM-g~Xz#e`nG?#VaMaa&75sex+&c1Jb4<kcdCBEuc<T(9l(|i@q7B=qXzRAYyZuJid@`B#NdeI3EQl>W?Up^}pjSZL;G%-Ulo72r?tma9%?nnSAA3fJ|81rHIzS-^;Xth#t1yay2B-f{Vl#2>-j0KDCWPyDfxQ&(*47>8+pvs8`VfjzIs~CQzd6D2&ym+EMOmW$sbo;l8Q8wQS>P7C_yBhI-j9'
'31@99tIp)mzadDWwz<HX@qrMTmFP7$pDg-iS>2hkf|Oa`%PI;iJqvsn&A_~4;F3nYngf?fUf_t0eA&>a!gMG5k6c~iiU-LkbHw41ig7TwXrnm~?b?)}xf9oRtLxV&UB`fkg%`4eD#OjFsnzAB+hHKv8AlbAZLSw2=63)P+YG(aZ+ZI7Gk!&!3dT<=L^Mfqd}^)R0ZC22=oZ_moe!swXpR-5g}V08wDox$!y)k+g$I-}O6!EC54>D>AN>D@aic+&U$-^LY(Amusvr{&yAGr_?S$U#+L(zL)(K_%3fwlo&?7?HPj4)na(R1nZf$Qc8a^~ZC#xT>KwP`ee!TpR04Ub2d$;-7u@&c!Rr}N<(N$+VLCLrt8o)E`EAwZ^rh&qEH(??v#uPNGl+%$*zoR$(&sPI{S>^_f`Q3F68l=W>hmd^1wXcsrUI1xTs=p%&(jzda^0wLnB;)jOR-@uG36v=J>HFrg&H<lh_?#2&jY~p>K6k{6IdiGo!?yIQ'
'g;_`U8NrwQ6i(eGN@&Y=Z>I%w>BSsNilU|}DLO2+b_F;|5+rlkM)o&{I<u-CZ4$vJ2=&?kC4?YH+XBlrkV0Sx9kwxQ7W8xrdEh#T=-LL+$paQNLW2)u%v>6?S>cP9(Bz|BR^_7$&BDjaCXr^=+e$oEt+r$?b;2_|WEvdgffke?Gm|RKlsMzCdACvvBOknK6|184NApk^F<<Ish}cOgku1U*1pyx7mGaXHcAHCxJ((Xi(lk+Y+DvkPi}iNo(2{$O1i{XRS8i86y~m$Kk}}3U;?$Nrrt&sBxhs7m;YtR9Be~`qgmarI?ZZ-MWmjd~TR5h(Mox+%$@ylHZkOze*%dBu^@*;@#d*_?50^E*%;1E}GdEo|)}%|qQnCiuZWOKbUB#TR-dpuM<dNtw_G-T8air?EH@c@)6zPnavkSnr3j`-+{!4xRqKde@xH9yi2_S)E8Q0obn`+M^fTy{+Y~2`+rdlnjZ^IGYUI*8l8~eM^;EsH5oWouNy64hr'
'3gPYu?^-hY7xi1>8Pejdh%qTmKqf{#_ncC&C}Z;HQnErn$oBVu(Y{Uv0TLkEKo1CxE_QOj?CCXFJV#~B*N^$?gkdB|Hvd)7ta}7bjrgxP9?bdRtDApBvHJ<{j3ToP2~z!WPSgmD_egJ?e|^ldX)M~LhpiUB*i<m}@b!_hn0@nf%t*uLHhh`2IZ`E*#i;n6?^z(AL~)DvBhvD#8C&P&C?Ja8Hsslew8hab#XLOwX))B?J^oK;8;1{2(+q3_QvE$@0j^Pcgt{8i>lp|h58#8F9n&oD^{}OE3m?)POV{_Y>Wu^~?DKv8S2xC1BmtnSO#J^})IP;%HW6|oOe(K)py&La9<A7Psg46s2fSr;Y*+QdwHXBFUUi}}bvhV98GKu`EETfVAJ4Ckc&ECwj#hO8;7{WzJc?8q->pdQ?rb>uiy`(!POhcS5cX#d30YTvS{Fd5Z;X@>Dj=!}b66sM+oalvIWLfI=QM4SZ4kHipE@fTImfP`32?_nu-DVj'
'(|RaMX6wKpzRpGI?3MSv>DDcTrin>_J`z5JHlpC%BaP61HyOj5a(}-3hLtLuuM!cEe@R@-S?61T_PvzPe(;z&_-z>-%dKyr!d)$ut%PW=s4SZ3g|r))3sUPted8_Z&T-fy92due9@fYxjoyV+4(#}X*WYKdiV7g8jCewOMrssirYnk#rUm<jFX%UjBfQV}yrF<M#7Gr}ajs5!5$i!n_CW3MQ?g<V;$KiQW%QWmqdk|QmIYrVn*VPlBJ4YcKYYZ@(12K;B4&Jl$ew7uJ5dj7MNnFisn#s^Zhi)(|EZcx->DpEk1JnZ-SDW)UJPnDAx%0m(>@u^K{FQt2Px96O!(G0bW4B3lXJPH3H{;d$fk?4=e-%YsGkyH<L^R=Z4F~e4-9`SOGSb5HRi<>fFFnL{rTH^zU5k;M@^hBaw6H854S6OiNUbBm_mC>ZvRgHcQ7n?$i)I_DhaA8OTGHmZM`>&9QTStZr_zZhpzrx*akme4bU@5WH#`aevb4K'
'?YuTNNqY)j4a500+aYkX9TnxsrC3C>GJ3FkYP9mY=l1@4+aHjV9ocbYwyvWIqHx+eN&YT7kD>Zf=Oig&8*;9_k-7g%v90fzWudI0Xwc-hIU8(!>9EDLo)L^QIUfH-m+6?lG*I~{e()oxwD~U~JrnrS2=`dB<Y=RN(%C&#8)D)bnZ6xH$Ipv6jZ5T){1g5sq+-z|?hNFbilI7>nuxn@!oDg@L!ijuHkGSuDwascln6Sa^-y3567XK$?UCRH4$UJFl>$noN*^Mm*Rv6f03mOE4`|<K<O^9HK3c8JO6_Z^gfuzr{a3z@M5-LB@pA+Nb>m^LXH!)z-+bZj$qG5LVKVlQU6&W;SA^2m$;(i7`B4JlF5|NwJC`r?Q;M)WwXC(rWui!t3>f|0DO8S+O-s9UsG?<4E>;cOA|D{pX1})R_RW03fsIw?sp^oMMlEUQ%&xIlNQcd5|2n!VLK_ceewts%0+f<T7=QZt6%8l=y=RCZA{U`FcrvqdH?4|Q'
'kS#GI`sm)U<$DM&UNEl08*`mf+ucs9q=0FmQ*G89V^(-SQXjZNE{DnqooGr!+7GV$3|&t$9=qRb?I}X>Mv68byLzR1I^Gt`Uxfrm9P26mOp5HWdMHKFZ)o%)_aN&W*HLKLi4~HQojS%_(R{%#eEZ^O3)3=WTbr0}e3NST-u?N7WFk&95c+7DH8@^<jP2O*ZgU>A!5PV-RMz^dj`|!h#FV!&#wd)tJZ-JDM-|k`B+W1MKDGaSr#h`-#2*}rF4U6)#fv-s`ePv2S1ia`7<H-U#yM<-@oXjuj(G~EeG?#*z6$4^z7Alw(TjYVw~>OaG%Aa;lsNQ4!jfpGgzr4)Hx<&>ChFaxWe9N^ALTT0k?N3-L!VrN3#db%n*I}fNy~lYs+u2#j#67v=QJT~kQG<44aa719Nch(!tek^Aj%XZwX*ORa1MGp4Oi*+v9fk+F73k(dE2%w@)L7ClK)3OyTljuatkU6xy1)Tf4pFUq?~FVI4K1;@Y~)B{dXP#'
'yrn6Jrn1TR_VS-K9(efgAf;PndpeLOh3Ob_lRzcMEt*05l6%(|u4plCcfjTtPu#v*Ruz(8E8{3o5SQ0n(pt`chD~3)>YUf9)~!uDjWR|g%-rEoRv!N!mn69v^ttlhmB0oQGT8DeN~c!$=x(kyy_j;94pYYcY3y@yOG=u&Wd9`k0ndS$k!maB`R2!Iz9&~t(a(H04E3{Z2k^%LAeA=t!Wv=3`aPjs%J<K}S8tAK{#w**^3h121Q3`mkBRCE23BnHCPfpnIFl$^pw}0WwpXhyG#ut7b9p?M<U0nQYligUUIQ_g<>8?tDSLO*Gln!1^Fd{v9|p`rMf)&+1<Zcz8r6gcB0F5IXZ8o%QBNwCCW+rz!a-^Jt@xvw{kfw6$^IZb;j(C;!vpprQiv^Nz#0RwGYh8V+c0-#H{WQIG#HlTu;1{aVU%TbPBWKA(*B4HP(5XLez4);I1LZ5OoluHzAyjLaLFKXhuvjSPU^7mdP4_1jNZriBna70*rH<$'
'EiXmu^m1DdS_+w{b+7-$iEh}OS}_YUD?(@)W@fS~o@Go2eTa-yxm88Ulu-V@>RJB==+TX&i)|DOz@|eH)J2~Cg_ctW#)VM8mViF7jc=0DzYd+`7=X(2HIgx^302$Ew3BITNkXl0wCvck&B~>=1h=<KR_QHxfi|S{Sw2}_(G%$B!4a16fhO=qhhR*_f5@_A(S0lmQx&N~y`-<XePR_b@$W>+&ISeeT==%;QJ-DWj(uM(#SLfLI~)<6_N=Hgv45%eP`sh@XR(z*^`s83Fs%0-h2F6i7+>JLlDZoX?ahY3^wa~ztW1+%MByTaJ?z|JW^)y-by}+o#Q+x@J^L!=<0;Uv#+h&x$ZS$%q+`!~?O7z*1(8&8w|-B_7=~`>nnZYCKcy1<PI61a&vJ!1G@R(g>r3AwQh)N4`5Ee<8wm)PXDRD+lM*`u(mTrkSpH?q6jDQtR17T&k_5D*X9)u?h>33)+Pamy_rAnE1_}cb9s+-?_F`;c)vju{WTQA>'
'NM0NSb_OD7yZk?%@Cb6n#f|z6iS5oWHKVz%VKqnviT^+Fe8Z2ESF#pk+avsLx}Y5KYJdhuGfn8izvuU}Vv2!tIVHoC^DMI{KA!*0-xZhLRIO4tWLVt99RmcpY{C~2G>Ud<ZHU_}j+`i}Fu`k=^qIFTJNS}EI&0Y%e_tZDDn5h1_QG=dD^@oy5i~_{{(E80hvTnWzVT0VG&S2ruIsB8s_%g*z@OFJ*o~G0X(NS9T|a}Rk?E=*MxKyKb-w$2w7n;N<nn4UKYv*I)mNjuuJ2DXVFfdqtD_@>)2GTf-upz;-u8cePhg=4&={GTMurFj>g@&E>N^Q4pvzt<0kY0vbH|pw7avKG1t?*GB=Mf6DyTn=t>{(C$sN*K`40HGX2aQ0!$mAMVyhQi_V)fZyXijULB8gZavif<?_^SVq^?+Zm!NphU$3N%KU;ha3hvLgawo(w$|}cr4ZCmazPQ9Z^vikdD->|8>hr?xKUu_JR-7a|vx;l!6=7iVcm#`R'
'0MLqZ4u_Op37IXhXlYuM#9J1Lrh+eMwIQt+-&o*ey_x9j4glOb&$4rd?Nxm{9aA#03O6^Oq`|ywv9hTM*B8n|krBOfDIJ|X>N7#0A+M+zZ{JN%;O{ix3z`n-W4c&3G|FABKKBZ|c$kc#7!>KNm&7rXivFJP>AbqrQF@ViU^si)($&hRV-&?bbfiVoqhkp``p3k~2))@Jp0&vrcvOoxfBlTO8nV<;!Al7bbGXm_A#t49xWYquI2R?qiPz2O6Wr(~X=u6&fhmuTE^CkPbX~@HUbL)+a@h((6e?9e`$Fe)Rbkk5lz~DyFA_hT*tV&0X77g-06CD%b^Gd}j3IdRtK2+>PwyE3u<Dgb=$(y20}JJ(eyP+Rq$wY|l^LW|^$i@upx%r}reyq^$Oy~Zd@DDFKs0_&zR@^AoX_6E8Q)iK{0Anxw+@36B7UWmkzWbj5ns2QA}bu*UPmo)QuLi{nukfC+hNIXHyh$|<1bCys&AmoCl>|te0+AsVqGAC'
'5zhcar_HeOdoY{;!3*HKSZdoAyCpmdl`>4tVY3@O<MI0An0<nz9X!ELM4A1@M)vqy^gYK9gGKTFFWAs6B(^5TF0aRWI^>2Yl0!+Zo*eUbm2?e7dxT0il;IN7ABn*((+?BkeE$KrREm|g96sKQ9&%Rf3-I0nD$3aOVWIRD1<}eAh*ahxEUeDv#*+R-Hprh2;Hjg;Z^FDBbXcVrMv54NAZLaod~5-uO}yG-YOJxI8RY<H*;x&@sAh8cD-qmQiK0cLWIz08>guvw*+N1L7SfwtlW+TX_&!Tpdu+0DAB}wBf24rR1Qe=h0OXaMZtiJ?uWP7wM*eKpou*w<?wNa1>^kh{I153OrL`gw!VAg4K#S)l{dA@u+YUa?W3(w5Dl({7oQMC-pK_gb>~mpGZTA<`W+*asUni|Tpv|8BS}FNwdLCh8s|N^;tjQxBl)tM<%0af@ej!hkMGTryV+{+>Ba?3^xv$Mt7virX9C#BbA!Nvr>Kl1gS-d(o$ctm1'
'kP6_X-cNE2lUU1c05%*p`&umtBdbvU%SJk=Mf@lWj_*}aG>wBrRnK2Tt-5feew#_v9$>4EDWOH3*o+y3(mDJs6iCdrK|hAQ9~0dOVd{6QgV*rSL*$n*1ds{qN)2&om-h=69$0B_w+o3NK7Pfy^7*SRRz>Zpljtg}k`eW=tUSyQ5pTvBeYltHo5Ibw*YD~y2d&Bnj<Z*HL$d8zaLQ2x*v7{Wc7*^jg%hZ88#oFa7u&Zq#oBN|`}8cM;s159LYs1@EZyA$5kXo+Py9+gt=g!z`L_iOrngPy3wKLcFO2;@<aaMGBoNwuJh<o|uyLD~f9M#Y0QL5P39SP-vOW1(k}qi}q+i`zhIb+1sOF%2KViyDXOmm?kBlYGl4kZMyfv~i1V9K<h)ptk_{`jhUP<69>B7dssXJ$u7(%z=3Vj&T`KdlJ%#P`X>_Ce`JJB5Lq%&9NXWy#**%6SKr&Dks*^)6~gb~IRhm6f>uR*XFH@N>*(aV9iRrH9|XSn1`'
'7k6`$6-uv2pJXx^DTa0vLILLXIwHQw;<6|Wx3~glNWW117Un%0A<9FIT=>dF&gk8hA9rPQPlBFA<Av}a!**t!n8IW&a0>J_5SpUpoi-g6Lj|9VINGUddLWJJv8~>_W)FwE$nwmXu~r2)*v3g`Dlu@|KW&;$?!?}b>;kaeWX_V(@=+QGocXIm9Xb!0c+m8RAFD(m@WqW#AdfYrK1Q%~V1`kC_AD|RNonvbe{917V~>twQG`B%DWj{Oe2s|PiLQC`QM3L>yZtQ$VK8On{BSK@B02H~IHq>ZX0clS8TtkMy>F~LOcy`5`j_cUbBi;tC^afGI33FMbCE(zLJW>5krYpl!dr)Bi3Bj{|9wEUroFfGY8PBDW~Lt}fgkIhdzGm?q$XDn9gLKi_5j^f*<epW>&;PLp+wSY_;M$(>d}HuS&@=c$Z%qrHAlhEVyJ#H!LS3})$6?|rkf$7%qR_A(9A~JJIrz5njqB%AN{;TohP?X*$j>9qXtq2GB}(I'
'7gVb_Ca1)hDS!-1Blf0}p7bTU>;tygv}()x^r+pT@heXOadvca-P7AyU1ei8L0Cerq-j7t6}$<;iCv=NIoB-U`WaU^Q?JosKrfY=^nJc$v#jfDyg7;k+`D{HEk#V!ffZ&@1u}d|39*g#L>!X?fK<P2wdv7L4bR`j$bZ29AgnzYY2@fX%mfj|AqnG<Bnn$z=I;GOaM*uk!w@8kMT!Sa6n0u8$)2}$AyBkO+>lr_LwzEvYkn&Y;cjB(XJ9+(s%)(J-!?3~pf6N0cKpgFy^FnrC@fP2Od6*=IARs)jGYdrO(;QIt{{GwS<(GGZ1S^+Z>5W9q5C9q8*7pmt<y5&t}-%Hr}7<OE@ZsQf`ZYMu;Z#xwM3$2vpXD^p=FES(1O~FbcY~Vli4aVfg=|-)T;Avq@$~_(|7%GRxr2YV8L<v9V{6dBF9(s%w!=_85xqd<%Ts^s=NSELbUW90gX*(Tc`(%Mf%#KmzkxnqgaK--jM;9S{szeJg+UR-z#6b'
'w(z5@KSBl3SVK}-i0nUjtfZwsw0=(<&msG_Mh|$c)%1=uq_@Ifx-niWAnnj`ysU<_QsI~M>nrjIWK5Ce1>V9h6@;tjCk7a5TIi%!D+7{;UsklQcfG4Et@r}T7RO>C>6*Z=H<u<>q#x&so9QO}c=>14t<U81<<N96IJ2ZgXcWJ?*LmHf0`)mX_jY};Lpl?M`LeGngRIuTm#Rq9RujEKv=9t6(B>JsQJLVmIy6liEcFH<X6VMKMo|Tt8$Fkni*m5wnd7LW-}Ym$XKBSRK;vTw7FM*gC4Wy5Ax4a<B2&(-^TZw=QP^R_@~6n)r?7jjjdf6+5Wap>pv(3a#KG7n@Zv9(%0Q^<O$PM(DFieM1Prg@ye1JbAJT9-i!Ugp;I9`)WgRV2G-Oulgp}N~d@ttP*KG15bfbRH3;xH}T90@nESo10;1!&ZCY{op`I=?KBPIxdKczg&KByp+@=wOhHRxBMrpd{z_8w;50WEBS`1gsYp95cmR1#ZvX-JIC'
'kEZ%Gozd@?+kiLbfop7d!EYHH)y#sKQ>@{owQNs_<Z_J}Jj)p_jB!W%3v)-v<?^!?%1p*DoK2}j$xIS9i@4TK++owR)N+Y+;SOP`h2ofBtunOZIdVwWrJk8ssWR}t&*DD&38{*OC-1$93>D@j*;Mjn=sPlRaFwo$;wv0dR8YzWo-M2!s~Nj*!%8a)D`{$p`P=nF2+8@jOva>&x#t@``WsGP<CKZ8Jgv~s#g5F#yZ2=DTQCSBFq@<00}!&hHBi@yGFtP*z59Wb&KwD0coCBp=CfDMI^#oAqKP~3YFl?EA_p)j*TVLJi98W>g;Lv>xG*U~5b4C)ppj^!$2M%R>mYQH4&)nb#1HHZcUI!@Jn_IN3?f>%^xB4usm(ZNj9~zheQctDvbO2tQw2`RXo>sNzY+omI8%>#3^w8NWU^YGIeK$!7B^{*ovj3#SUPkYw%lk2P7l^N;9jS0F9|XYKobQant2FB$O0o(PmLR$<ZEI51+fKArMoq@%G|fX'
'{n;sr`6rvH=@kUtx@A)H2szm3IVR8%Pb4enHNxWGIPdW-R%%c!=2SlBs{-b<wOw@5NCYOK8W?X6{LCwb#?yEa%iFft1u^!n=c(6<LSQ}?aFSo)p@hP}$*7W6X|nIrJ3^elQ_dHz(N@6GXmv@FI#}_TafaAAegr?R_x3+i9GiTi#hPP>;EVJAfFIM_imM1hog4&eyT4RXHy*tFaUd7r%jrb-KB*knx5oYPAPFR|ft?ZuK<SoBt)|}P6YZw+pnwV)fJQrpjUA~u(fod^BJH_DA=|MqJhWUt{bZ_I)tCmFzRxX!eO%pZxqPmrQWYoRJxYpzzW$(<og%eE?Q}oEz7vAm!`9>EY|evRb}yais>CQ?q;0^<pSpYL1W#QE##$n~uaHX+;*O1ZbkMpZbdMsHSX5F`@o2?B@LLb3Kn9;-{S{{2n#y{!C=h_ey!xb(JIhESHTr#$MNAkaKrpSZhl}DA8b9@@kl^-;lhqDWONyOkz{#d^p$ghrUqi&9'
'BiPtmM^NW{TpQz)xTDQg%KNW0wSemu?#(HWkc#@4pKr~%Tfp5qJo!*IH_?q~@*cWu6-&5W_jInmrjD3@U(R|13gs+2(J#~7xNF42{P@h<fDk}E%XHZk3p`ssLmHzg5gtWTlJ50=H+Hee4%eWIqIlaoG{F4KRNippq!vEYDjy_6-y7$SFO0c2UosF+k}&Ll>`wAK{nM!ni6IX`LOVF?1s&qbF5lR(&Y@*uj7>gwwee`|$b~JN_lyFO32d6LnR5`&W^0WEJ|L4hCFap7pWv2uidL|@1$aW)_S+e-9GTIDxJn{5E=H^Gwp?n}l$U!3Y8$U@XCp|=%akp5B4Llkqq@CP<RWZIVpAxnh~=v^a&TfYn-NUg{YN2fHEq1R1TzqPq5fFdlR7%J&esT}06A1Yl7u~B?!i1e<IHWlsd>0nCp+_xR&d}b)|Jz>?HPTE-D7uOq|<y@@OcqgrsucB6S%f}epOWt!NKm&-beURpg@7m5fnL_A84|(mCZ9M'
'!oJH+{hqDlza;hQVcp~1#8_4yR+0OGS=%%8Bf@3+ExITj9m(y&N_D6UMM0q<0{KFqVP!QmHk_n`uLyg?4y>j(kyOe$&ECd^jp7?=3ihC5r))>4nH!Rrh%|^R4>~wPDk;&8R+ahGY_$VL=o}UaP3=9-xq+>`CVMR-J(E7a_oj@(Wc+Qf8lS#@Ea$<0Nm>06e3b{2odeif3CO5^C?`bj?!i5zDZww|txf>ZU>we<$O!Ie&r%@i9c<s~K^;J5qbqpUVAK7e#5tQug-MsJ)Qv*3^mK5sKXv<#)V<siW}@!p2K8LOngV@>FWb~iW{sK2FoP8Cuoy5I--HrD0{20F9C~!8{l0Vh76icwU1PhtW05W^31HlbWCOK=gFASeR3i+}njP>SruUbs4jI74FBX!4f$Juhj?QIVDN?q48^)*n?pHR5=1;&hsgn_CyQqGeJ2kzqQLZPB`ta&Tf(;t_kdQfga=bcmJssACU)=;HHn+Ksd83M_0X$y>;&(s;'
'W1mPWaO*=`F!RO8cxB$g^J3bH5Dw>atx|6ox;)dK%FAzu$EU+O@juT7opCb`W0b`(@QSs}&!F$5&XH)s>oWe_c`f6q3u(+Pkz*wgBHcS!i2fC`p&Qz!`V^u5p||F)@L<h*(Wws!;?k^(E2=h2J}#CNYd-o{HPIKnk^zJrLKjS)kt%HG2@?p9>B97>JdM7|&`Vvj+vvjYR{W=V%&s&J;aH=lmGban+?4>ct?4vSNk#OJe;y6r?PA6+!(=-v;)G^xjxXDkvIBD%f;+^0x5xViSTOBCc1nL_yc0LDAL<?<a6itABlzmdulm~)0KPQF&Tzp>LOD+#kCqzm6UV)eDW)RHx!Rb=IUpweG%2)_Jq6F2{iS|>%OU7lz?kfoF$p;-5VC(WwU%K7G;bV%_)s6s&}sziTI-y(U3l_EC7s*ACv@1FOYJN30w9J?M;v_zqJwkCd2`2Yw2AbU@Z(P)9j`G+RcG%D=AbnK%(`m^Og@~g>G$pxsk;;(3Mm7H'
'*2Sb#WenizZQ~8Gr{k_+6~}adV@kvLk+Q-{F_4R3T&PuUn#Z8=D>LBD+ka#?=@=R#S+3&rwG8H4Vi!lp_yhGXlKC{*b8*WyyY_904>&D+UlFw;ia<yPq=}RZ3p?G0)&b25K)r>LcL>WMK*6^LH3u+eee7^B7Uf<Hzx4h1PRo{OsS$yyH=AQh!FY4@_wK+L_Gq}*R`1_}ws4cWsvHN*zTAXi77_}e*|#CYj3LXL9@jT$=?S=Rl6NtcK)9>s;xKLUB2xQUB)LCo1|sRp8B)Gn$b$rS2gFs-g~|lX-B^Wj<8v4>?N$Gdltffi0Hp0c$nY8~<iW(#zRzu*4Tuo>zY?PO5Sk!fh^f)Lk_Wt}35V@tzAOQ~lv%~l>%OTO5APrkr!b)h^{;xS;?VIl+&W|X7N)p6B`AF@F=00kI<REArNqX7#@qY2xQxabzV!o8!cG@pzi6jGS`PD41k=e3juvhG+d=h@%q3#mM5=JrCAIlokpoE%D?OR{ClrN;'
'm152|iWu<s0sb@e$?!22y<zr33W>i^)pGj2nmzG{&_vYobdX}wVZIBm!BU-BoQo_i2x-1bF^&c>H;0|l=M@Zf#W3J%3J6iO-^{AbpILj?hM(3<vMWA}6M?|KX%JN`eT)XQW^7cRu*WI@!||*d3mckQc{Ie*47cw~TfEu0yvP=ddRSrX?V%Mj8MF(Ee(mZa<GTWU&qTW!qJOjSUKh-`1b6uGb#BW22#yatRn4@eIIut?y=xoeV2?)cN!pgtW;5y5UamRo=~?E-v9@4c#p@r#%LkHb_iz{~a_ot$UZQKA3&HQ^Y+?G~bR38b_y3VP;=_ZmUZpv&vQC!p8ce99-Vr{YG{44DY^7bQwb^5o8c3FxIdn`jQ#6eDjI`t?M>F}^l()k<HnKGLOzW{VQVd!$-xH?B$Ml%^fv3<mo#cAC;^cd`t{v)L#Kn~HtX_SG!xyyfzwpPd)eYb08^!bUUaGDzz+XUA;CQBX)lMSTOx<**?Or-I<S=xrS-Cec'
'KLW};vN&cGEd@|fi>69h9lShysBnJV%lm23Eq1U)v$Ga_7UDr^tjwh{$^cbX9>kss<pHHInNv@JGb5@Ftu=vG8v}5$nx5iixV;^KW`2n<?qtwagMiEE(yTnr#b5aZv0?<d*2Slg0)Fg1YJjnJIs>*KTI-{4AA@YKw!ijvF5==QB-<EWDUSQ@UP{~fv#WdCB803{-NJ=*W_?Dt3?zL2DI}|dv|1I`$9WPc?KAC5I4XkE0_UoEqZ*#z8A9s?30vT9sB~{v{9sX)$spU0W)L@O19Yyp3gjlfS61Fu<u5W9nN_cCBL4(YOE?s<rbk-J>cM;j43fJ12zmiQYK6_1dO?Lw+b@?hv3RuvuF#`#0*En^du59f>E?FyEn1Fo8dS6Ci}8Imfd=vuhWRO-he|rKi>#VkyN#_Khf9qb`3?b=lh-x`N4Kv9@^~%dPU5FeL1@fy`6t+mRz_^YAV(H^yUjlIeM(FdRgAn<K}Lq2Mq_uNHu~XESSyaju#_g9'
'o`o9C&PY4K@B9ufSXd~p#$70c#vkmPMfS<1ZG~U1nAMvstd#G*k}YR#NMr<}FZO>TY5@m;3OSa5)XR>C?{ceFT=PZgj6KmxjeiV8%VEzGiwc5RU+VU5JD1oc^~k4LE4>9}scWV<chKzVa<O4D?UAOV_=4KKiJwpUdC|ZI0c0B36>zs-wHL1J?%k=_;zk){M3M~82MpYqmOlP;Y&K8XGTKJJwN0c}K+DW^GJbg-mbz<6d8d9%!3H+Jp)-Lbv{s#qH=V|T2i*@y8x}Q3uxC;0e1TVCs$;h)W;aWN*#+3gy4T?)FEBXi;gKSHI`ppCRwmI9nd;oLaAb9+k#z$^&TZb0?#}X=`h501M<!!SNsKq}vWe8D9&hy7E<N=Lpu{hQO&<7_3csLuP(oq-*TOTy%QM@?Ga|33@|SmW84y+Y8K$1xU#Cw+$>fxu5KjLsFv<88PCB$xAg6?_ppGwju<pZEh8<$E2ze_mqd-uaFnPac?0RZRNzpVa@;@OT'
'J%Dk>KENHQb+`v9aHnI`Y9t65aEvLp^>{$BnRdwcvWB+ndXc!&yHPSvxs&dTm?Dx``^gqz999p$X8EZ!rtFz0xG^%k6QzABBajF+vn__Rs83%Rm>t$ivQZ<G$Dh~RusJ+*h984;2f!XgTdWRPPfX|^vy;#h$3mm+qy=s<$N>Cb4FV0T>qC}jy(ppA>m`*>MIRlCI){F$78YQYr-$ibSduSECZb{5^;a)R<_xp=hM0Jn6~whx?TJ_k1JWH>JnMM~C|W1@P085(g>!_zC3)p3F1f<HPWm*OaqAUAdp{sp<DkniU8&l(wP*G_oxubUiVS{kDoNdoi+Sa5X6~!aVp616m70{ux=+XO!)`0IvP*g2r8ag)Y=&YoYnhePx6wtc8R#}`K~x2f2VK$Q?<pl!I9Zr6N?oX%@0?VeNK6BbP+NgU!R5fcl>;+3+;FRi>2#ob*z8*+m~^L%OGW_*(pY2bRymmE{(Ip&K67L}99>uG50LAP1a6f3%rmaU'
'HIPhEnsdUo6>l>?v+A+^$Mi0Uh#S#91fB+fTIZ=*QRyH3=38x%{f5!niagr0-XeZ(l+CY|R%xSul_-dY=Bfp+V*-o$w&u>VEfHAYe?vKn#$6(*r9R3xY4c%0W<R-LTz=3H)~JLPUKE*_=dScWvo;>w9obU0Mc@gP#jq0jdJ;)$QA+q}C0=Dm<_;f%yB_B62#Tl!tYUtB7gY46H|7ioY*M7w!TS@&t2h88LR?ZZSal~^i*+(61}SZ$C|45~*O0116m5MDmc&b6ceTylj)3?oNqDv(v#889^|VTnejC(dl}g>KG9Bwy{@ViA3?LcKf8Jb$HLT%A3H=LXy`VlVgp(e`AC3uww-JuEiHfqi8)VuYNc4H$L=@Ah;T%7Etfn6|M8<fLINDM$8P>}ztjtyRkaFmkj~-Lk03qM-=C=))aUb)VLOJtkN32t*-s9R!=`&{N^C=zN$ZP$w!NTpw4<f5*K6@tnzdM@Wvtw&B6pbzZ$EE!?Z0WRL%SAxE'
'k}o$Rt3EcS1=D+i1V^*2hOmNYcOHV<yJvS!r-t4|5FB?dw+H`SV(!|?MmqMx-z1f&pD4+du$H1WSq*k;DFw>zI}pp-;KxfW^JZyg<?P0H(1-ypLUE1Dq#p<wKF5qIuTUL!m_BY;-0$-s9++6dwNfIDKH`QjV1Q~Vjli|?X=XE{RDe-krX3IJtocM&Uq-cfN}oe(b&`}OX!)%k%7l{CBLRe|1SU1IBtGOvHizXMWWKo0qh~0iKXmX}Y&`*Y7H~FoJXWz+eAqqFt>CwVqY08WV~RC#1eXY3kLZ@yJin?~GF!e<Dp35r`Ee;bSATo?MAn;p4S;<?#*nwn!nlMn6HnL=y_?(9(~>QE2W5O)M)*=P;Z*kacFTpRnzX%P=n(#6o-B-Db929A&<)u#NO9Zz;)~UnyZ){WecAy)JKvE@mvaF+MR&0JQ+RCZPDUMqq|4gdJyA#lq(!{LQO`ELN1OC}X`kw8pWXM?nj|_5i_m42yiwqANwDTPpCkt!'
'TqPqT^6=P`Xp9`ytqx74iVwzw6aU+AsY?{L3Zj7%;vk;23OkpwO_vX{HPQlS1>S~Fp|;Yn7H7QDOo9+1-QVPkPDR;zIiZJZfILUpYe;&^WanC3kd%=dAIjfi&MUUL$!c>^xyb@qUJC7|Qx{kvi=<UQ;=$7r3<!M=u1;Xv`#Nu!C0jg4zZ}&^pCW9hN5~zd7Q~Gxi;(Po;24?S5WuBlA4i4f{jVui_}5!k?5Q$2QMb}l3?YDbzjPPc{rN#{GRhE&KcDzpYK-1c#t^!MVqjPiGybHyQ*+S_VvsA;G(=c3Pu=)#f#U}ADN~sg&1o5bOJ*fN=tywg0r04(e=WGS3kJ$`za&cROjhr-P)%9dJNka<PyIDq)blqz;EMnU#i}xf#=@{R6vR8C)0`|DWOQ!(YE?a=9?kwFyMlzc{Zh7vdqa_5gIEiD;fJKBkmgqvIl5h=Pd5ySfvw=hEhEMnY?tY7Dn8B%m5Cq=o9R5tV+(TO)@<-D)(FAFNFm%4'
')fQaLL$GSqkN_;if<Fm&6r>HdFQQPo@=ehg6JonRg#~ouPd~~JNAZe7QkWGGj$yS<f;<tO&3o^`KbORl-VfMew_2a7u=0GBG`vjiI8aCF_iO~1FB}o{V=iJZpn7qDP!xgSRRNGk@#E*s<Ig+AcDkaTp_-gKJ7#_f+CujVe6)Lb^w6HDCc-3m;Md@=J!CHUlz<DbCbm@q?1PghDSu50IOQW30`M-Gd(A_}DpZHi$ZbzOzV2TP?+hOy|1(%TL9i)fM(5@RYvl^8ZNf4}Q-N2M8fJnA*K3^Y9%|-&u%uBpL^sH>ks_I&fJD-dVm=ArEF1N5=l+VjD-iIH9id;9draDp#rsH~)M}GColwrqD%{B69bCp9q6)$3mb2QKPyFGdNnZIWZEx|cS`mWBkh9cJq9;NVS~66zWGiGT#b-wt(Ps&1e!Ui+Ry_s>PUk>l`)Q3$j6Dm_7@b=k;c6jjbt1rMS^q`+UR<`(ZTnw|yoT@Jo2*jFvQw%dSBe0H'
'@m*yoBM6j(Y>~`ZE(eI9zE;3&B@!_PnYyWkiF<*cSfsis<JLu~TS*QDlVwqdYUu3q9(Sy!Mx3U3r8}{{3c|cXsjU$9t>ztfQ6c2O7CV4T2?d0k{}*wKdNT(slKUUpiYHHi@2-_?H%bYWq?78_Gu`J%N8=<9n|1Uppb^Sz&|sU?sq-~!2_VQUD?*gWK`}>gp>*qZhav7Vrv~L1y*PXHXE${z{uj#&*{in>nLkn}k=B|M#U1(DIg$!!B3*BgbvNtZ?#2e{1i$=$pe_vbHIP@aO|9coyYO~$1{9mg*xZ0+h9oP-H8B9JxVK9e*CsXqJuWA2u8odYni!J5mUrev$8)L~c|;M;EZ6}RzYobmA3g^JI-}Dd#$<1y1GPl%(St^-A2SlAlbP|z{tHn1tG5-gA-tUckgpY?Ixs-D-V@$0({jj=`*Q#h)ug&#-0L?=m8Cv5&O$)xQ3@iHx_hypDN<-FO`E_zDu1Dn6?zt}iGS%vno8w=^Z@`Bz&DAv'
'lL873m1MU&v4YoU!g`wUzdNERzl$?n-jkQ$@{x&#fkK5Q2=qQKdguw#gYNp+?1j*=MCm!;ee%2YU+HG)B$(K*ik!&|nRTkC->?}zc0)Y2SZw%@tK1_QHx>^%M3uI>q#I6<=%4rvOx#7(Qy3+jMxq3+h8zSpK@vU>lfO+iBIUbP>;`&p>RCg5YkhKCCq>rj5BH7)g4%a!c?$qh4UNZ7QC#{+m&4hA6{Vifk{%su!|_Nrl}KXZYFv?CkKK($1{CZOg5=E6KlqJMadA>RjyjFClrXGqiVZLBWpJY?h;tog0lBv9pD%4k;vE_gb%TnxLS!_%<JC%L=ReSt3fqnfhn?zq6~w`W1#1k1(;go-h0Z2GsCC)_yD1-DeT~?q%Pa<ppjiGrIGc*3Jpb2=H8}3zEzQ#wpIo2TRK|DA*G@x?LDcy>gM4gPgs}GJS>$Ck{?Yf+XRK2yXKv9z{oJc2rnE19cT7L1G%yb<diQgD8Ml7HeKC{*sZy~Emy&0m'
'1AcEfNA1KWqB??kDLC?1lGB|%js7*Y1<4vz9t~&<g9WPL;UKAai1=yNPjLp)Ju5+b$yZl=1AbCE64;$ZEN121o|_zojZZ-y^3af#?f><-g)0y+5nQWi^kIW>4n6vZLCDVvsG}hl^uB&-&&?7y65<8x^!DIcVFz(x=pE%(r)MZi(6;mdJ-BaJithp}`9>lx?}w`XiH{u<eaMEe-g6jr(X5?x4PTB4gp?9?*ccS7_Fv3uxO~)TnSOh!yG-7|_+nt{=PsYKl`;}LzQX!ym4tT4sI5EY<fe;|U>QsFlpCsV9Dt0@Ov9IvYLvvJ>(>_fWpfJBh?_C2&?aix<x>}Bp?N<rp-}|7ZX`E%D|goxasz+Q+Z9@vjF6`r1jOLepZIZno^8gqaPq_GW1?mgFPHT$$fa{Cl?BT(GIlL&G&thyMoJ?DTWof}YJ&5HXSZ>vk5fGG!Kz{i-dwl}_c&5;M1R1iD6m0Hci|L}={HGJgRm9%w=HJe{{>P~_<lmH'
'T$J_I1O{^k<zAsNZ2s6X&sR3XLZV=`$0WEfx4|o=&CpDdDv=gImb39$$Eh^74U>J<l*=VVpA6R2#VAT?5=U=S2dWfi2{M@g;&3Q2-d_8NNeY5>XfI0<{kwG=KXe1<MbhnG=vMLKp^RiTRT5)m|Ing^IO@2S^SsxDib8#_f67>Cna~U1?*_K{#m*BGrmJBVEO+(4mF{hp2X40{s*}J%oRJj6)0rO-q{AsObR@4^V?KZ!z=EA*bj(=|3;~H|vL~A#)fLzfp@N-51~ZxY&s9apJYV;_ih4|HP4^h$>8hDx+9vd9%(qDyk9+nxlcl1@P()B2D_J!hhuqL@=}!&<0lYX$2Uh8?U&s^07L^F&CSH(SN9K4dsgEXRDKGMvlE4H+Kz{sZ=-I3Lk~w|fEeG99H7MHWls@M}K#5)b4#`;r4-`L$?52b4@U^uOJqPY6d}Sws;|(T=Z@~<eDX`P(*4@I_uggU2HNrE;f$opJNvV*tb8yzvVr)O4=84UA'
'Qfl=MctN9`ZQKi3(pmyQD9TOaY|OoW8?270ItmFPum#<VWAP^Y;EhpX=F61V&^uyGhM=&#fL<sbpJa2P4vX;7fX#dSyR_Z0ogiX*1&RezS4MHu<J%%{_e6(g5E%lFD_|JO4oiwLTsM_DR3=k@Z+chvRng=1rojYlvEchDjeszKSppz0Rjk!AL7%oTB5J=inY3;1&eoj##_J{t=_^!l2e7fnHv-HCXw&$Ls|l%X{n5XOSN8a1&T48+Ue$6gi{vz@5ZN{JN5b_n3{eLw!J+v(&&V~{YV(|1mKafc>8}Am7a_r6W;Tdr7@h@HpZwLsNsmtqO<QU59~p}BxZ^Fs`u)dt6n{TjmpdPN*Yi9e2XDKJKdL=|JIDoL4`K5=Uerm6YXkM&w4*-<v~w;aR*)WZC9AAS0pO3#9ObEtw$r+10%4dCbAxAIIiv_MzBs2#ch=51VGx02IZe*o4p1L^{#Sdk=ihYSrW}^!4O$wBGV%LnB+`dj!W|6uqk@`}'
'agM#YTP(a{$ZB)OoF-XW`~b2#arl>$9>NbOCd6eu{<yc$R4;#gc~y*p=y}r92&Cfra;8~Tqf<*a;RkZ2fEI54FMbYr5*~!&0~!hQMYJ@Fthx9c#G-+El|j38)_KrWq|~E@sgl}8DrMCUw`T6qdQAXb?lzasrUQ&Gg*!!WP~);|a&jIw!~4&hkAqXoLCS0z#gLUrf1}^ugNP-YP0Rb4Y&*tMlj8B3BvAWhJ1pX3gukNov6rUS$)a<SSTP8JTXgJTDc@y%$Q#7Fc_qtnAeTTF9Je%e<(s2iIu;k!BXL(7ARPsbL(8gPZ<U+{i%qygIn4XRb2{G}=&GM*TC6!1%Hv<SdDfQ>4<0@h{~^L+9=-^l-RIES$Gw*DxFPiqE+yqKXR(8ZBX{WMS99n^(F2|jjmDe_pL-uqo=auPKzUnbDBovrk}Xu?_`r&ji17mhN@Bd1KP(W-op~q<_8<A-Bjn_qUm3{W`N-fEdM3WbiWP{1ItIZ)@%0(5NfMnI'
'T8mF^;L`-p%2D#n5Asc%>H`MkRm?QXFOV?ul095RiGdz4Rr|{$dn69UdV=uz*kJr5Pwg`<Yml;W*$wySJDf<7XlM$$aKs7olHz=QQW+Ed=j~hcw#N7$)2x(r`9#aM;3rGbs1wb(axb#>7HH6c0f3JdMU$BOxY2~OD?I>Ij2q6ew!8Y(SQTeV8#t=Nk4Z=_F4p$;#cTWmRa5ISX)FdzgL*^B8f3x16t59?(UmiEb*tm4tU>bM(}a6Cb~*9WCF{2Lv#Yt-PCY_@3RjWpkT#y4bQgsv(0^(Bks+>fG$nYG(v33t9?xde!4(M558dWbNn-#K#iNma(u4XQ1&LzQfC8$oKpjkrio6Aa&G+9j;l{_$j_-opNJGWOg+=ga(rrg(w<caRxrpbhJkxKEAmU`A4`|qas~0iDELJVdNo_xTkJyS$dY{cE-Zoc8#;Rqc?j7`tlta&eYtEs84K@Do2aV;;jLkQxv1elQeOxzuF4rxBV(6tTCmoB639^jF'
'PcJktcd?kL>X{PNBfHwx-^+Oci+-L373}oMmm=9t5W{{GC+=Bl>wk*Cl|9s`=U<?<RAC=RayW$&DJJWJ!||<W$9|16D8HaB23^&YVSX@GleZjzS&Q+@_R1T_QXKCki0Iil@!$R*F-Q#@8V~wARD|J`vAhL<jFcP`%djtDIXye*I?~Vb^6kZvG1@tBCA#3TP>5%}5{fXn)_g<!J6nob<aO}6gIEz)_a2rP7W6ywFusS!NQk;F<E?iC_BPz)8H$M3KHDc`4)aedG4El)Gk|`^wpsVjzKWDv;!0tx_yKe+AXqz(yt_Z&TEIV?daf7ZXN-3-09aE~be+V4VGC`Y^S}xX05@gs!xO~a7IZgOgVO)|6Y8fu(F~^k&;hS;^1g+ev7}e;ND8_qW62>c;4M_Tvf^kwP>P1!4GWu4_%-6+FF6Kusxb#DPY!mxL-D_WYMEW4rhk`K4*gQ}atbp(iIqFGJ|;HixX<L47MKTK!WULTW?Ng*SXqZ`z?33<'
'_52c`uihgbVfz0Qi4OfLf%y|cD;oeZ#wyCO!XO$_@T(13tU_**x{A|;pNW#ubu9<|wfk@-)kKkj?l=lWvjgdl8^ef6F;}L+xH|XzHId&36sS5C47Kv0wvt4sfPmV6(~p|M&fY=)0X>0$GM2_Pa}8IjWZ8Bd1rwAas9HlO{N=qeqF_$Nv20<*#gC1?>+Nqcdjx}yHhw%AH{(xTn?z7q^g$O8xjSzlVO3PXymwxkJ+~fPf+bYdh(>jWn40O6#_V;jeM^(QWFrT0zWhIYIYU;qnNpykuy0bey#B?IwIT%<-2w6k`=I^%MSo^+`px2JIqzJMmm3`#X*+(c@^3PV14gk7Ra6xHjpv4Q{FixtR2(qbrY++oc-U|?I2#ZlcF_p4#Tx|)cm=)DyeI#+By4>4OS8N+54^5xHnRcnB7%2&%|Yxn0A~-e2zMB&%wc!wj6lso3?;yTCB72czFL?)I||)q9NLcnX$oQCn}52M2m1?YFo_}&5>4nmJS{nl'
'qq`%5@u_pXiAm7_2aRrV#vLktygO~I<MR-56hBUfoV^wBV?E1@{6w0WRxKwhEdVT$)hIUx(x{gxG<H-Tuc0wGQgys0^b5@j)OdAOfIOb_^FjEFT^;Y#4nf8Yc%m+4<Bd-Tn0Qxz$rb&`Bk;$6T6xi9SYItbjIxzl&wp?E|3GX4&BT~FRPr7JNhKEt;Jgu0gPHzmvpJE>CZkEShhw=g41(zlH%Uo)yiZH*-!E6mn2HENa2xa(`OA-eDV;R0d@t$@+My%b=O!3*!~BGc=SsCIb{eK6QRz}=dqGy}E!jn!z&TB*CyM!AM!a)48T^&+jCC?$uDyAvX?!gP!$Pu`k|dy(W2EMZ#m6I_?mL`0y9G6gOis8O`|$K01q?as>>$P(K>fK0zYjq)iqAjJjFJ)Ec6{Onf&Cfb7Mt3iKOh!1k+xyARjR3(s9ybwy6uxOpVR{TSS46HBkaxNi{_QG+{D8j*Fl!af}QhwQI-3~2?7ov3y}0%MHo2n8gRn}'
'rB429=1TKfbq4WZht;27H)5fS+}uL2&!P7n4)RLrM=V*{C@YOKjA+6Cno;=&pbyZ}u8%p2V5!?>KNh}>3>uYBG1B4wrLKKD7_I_kY*^qt8*<v`IN#n&U62~Y9<(G>=1n_{_f@q{?bbQKkZ3s`I+JG1TMedA4#Oku4k3ZaqD&89<wmV1%lp#F3~F%!<sgUD`Bc$-I&HBc5PIE6OMDX4F%{Sgb*MkMt~+30B`P+xhyf}ErU*P4$9*I&vWVoz<_f8cJU(>>wK3CB7*HOs(+kcPI`p$u9)HL<*?6x?-$!YEyKv3RQUcEUhue~*R>k&l^n1gkzl)0BlbvacA5h$z@4W=)7NLYBY|EaEI`cEAH65ikWNRAK;(D4=w~R9F7+wT-@t$elLZP~AL>^=Cho{Vl=o(Z1+KNy=X=gJvIjg#4y!iE-rBP*ZA}e(gqr}Y_bV{sU0?C1vjE68Wm1sm2*MuAD6ss2T%og=8@LL;&Q_=~AaH%G-$XAq_R!)M@'
'PG5-fZxFW?^$Af~wxtix?E|%a3LmR1gX3rgp!32$C3(M^7BCGm3xFR5|HSoGxj_eRr&WXCk3e3Z_cpMIzVQu|)!<|Dl0GK}E>PU~;b{5g!uiCjf2UqZ)(GMyWMqh#oyx>kJx2@5{dWeJQ-or|dA8r?!BbIt?G0AS3P9LV^C;u5A-|C0Kw!+~_+B{biZLB!%AcYs4|rD-#|wx2rj3aHg~ua?gM~Kge?M+U3@TV)egnWWb8+T}S^DiEJIgVCm=CqNZjACb(9Mbsp*VwC4%FhRZ^5{yIxc2y=NT;_-It>uwin{2aSbTK?}Zwy>gKrir#+YF4-J4C>FWU|j277@d&=xDB>78aT6p#&Pk4jR1CSvC?$vn}^!T>uRsVj-ln0+kx}b-tt55TT#$N>9$Gmj{{t*sv$$Nfuqi3$>#7`e3Bvxqw9=z|iN!Br1<prMKAJs_SVXOXv{|{}S1jy8|enZ*AJfJ~7$h}3ye)KEd_CpeezggeK^*km<6N{$K'
'KF(IQ_Y$!?2_~Mz!9L@hCpL2`&y|g|u+V}KwGcgBke>7bju}|A)D3f_E3(Ero$#0_SNKDQB;RYDE~rwe5=yu)TFoWkcUyR`x{?TkQ+NjeQu}zME<7+%EWpPB-eHP~V-bAF0c`%#)(@DE2-00%>!67o!+E*(wb&WX525IJ6=>F%DZzF`J}QtMf0amSLgqEh`XldK${{kLL$kRPSbGsJk6AD!r#Iz^rO5ME+$_&yeZ`JFT*}mV>uDmwDsJzu$-_}LcyHt~d2-vJLxt*KTF?fucCA+H4BaE*mSCS5uN-Z>>z40h+H-MS!;_cHKlG7mJ|Z>@(#s%@weIA%op%aXqHoh7AmN6dILf#;WNghVxSj6jm}?4|;dqm9%en-uzh%Uw;&*_g2@5U`Ba+B$;J`IC#15?VkIp7aM*P{i`$=fmNBrR@v%oyWTfu7WdCL%5`Ib5G%`YKYn)2WbrCZvFu;*>5A`BQ*Fuo^?G}<umNiSS)1O-o|W)PE+NF)F('
'X9*;T=)xqGD?7tFq4WBj>k%g&KU5%5X9#KFwn0*h3mf~F@?eNt?!};_N-z^u?KhytXkZH{4wxZDY}m6Tgi9$&qxzZ4#ShK;`>>3TEzXB>XJ)GaCbC(VbUs36bnAnAh^K1;|0eLQ9;=n?+Jl@O6PN`c3EqxT_XIJIH2Zq<g05Egmeqaru8TCFsDHFq^|(-pGV!|>HS1IN{C*!idv*^Nx6Py?z#8g2h9c>dbp$U*=3}Cxlu~KR7I5V~Oc!LdMh+#|tip_zgrYkm18x59IM8Q}lF{2(JZJEedo$0vEc70D>&h;G#e;3zd7c__8(@v6!#dZd0dneAZr|7DRqHJAlqqy^KhZS>fy2cVKbRVW&Bs@~Y*iAeMAt8D;eWW;dd~<EGAF2A+Y~Jh9o;@(V+RP$ue17Hf@%lp=NEIhv5v(#xDD&V8+)$|>2nI$A;KTzX9LV%YVCKjB&!@)D!dQendBUeM@yHNs)EpAm*;KVpWjyoGT!19_0)g<<RuZk'
'VSQ=+teo)K^EX9~nC5H)ULPAy2)RiIbGOrFgO22k2o<IkY&Y-Xg=?#}u+ATkoZ*36ytDdL;$P~E^C5T2+hpAtid{}<W@KqOO&91g;cy|_hz2lz53PTT%Gl!O;59-<Vcqj(C}_Mv=rZfIC2$2MyeFK4ewS#aS$}s23NOWekTzwBAXT3mblFhtx9(<pY|{^2h%)-rg)Yf+M0P+DdB*;BXbp(6EC!-u*<HMb65rW~R+q*KtM0arb34GM`Madnpu=>SomYh)!I@eZSF~#tR|RXoofLrJgk-5dEHa4#JtD;2k5d?0Eo!>gs$?v8<3IS&ZBba#BfwrShXZaFx+B}!@@M%8ggq2zfzvy2B)}eO*G40j0yWXjvCLT_i))CjZaXMopgAJ=au?ZaOJVqtTAn1~&_t)##HcPnSjEWwKGuX_zZ{_<Z|cLpsJ*eLbh;$N-<uGO^P!DY>aTf)dV}5+{u_K{;3j0e4*~8`_yjT77B&e1lCF{S@NB{OCMjxr'
'ROixXWmtv|!nbGmu7r}5<*#q<PPArMib<?+b%cDM9xq~4Vw+Dd?hkT`v0=T>T|FStzt>aDwR9}KAjz1&Tdt89PP;XMME*j-sB~vZ6G(Zhe8o@)D3b5CP9kWJy9bzC{Nk~8<c5kU6Ru=rD01h_51bvFKJXIihx5X|>+wNSl5oq>6fFr@=I0wY9G5CpuJ6i!Rr%G!pk4wo^Mup|mQz#?{_qmB%i*{t(9134@cL;flQsB{X@DHioQUjwq*FLJKV+blZ3MuKi2vU(OZg@Kf(IVxT0PSsm4YE=PIX9GW|UsBV+Y#HF%e0^ow@0qz_K6cg;vwo5iGQl<!Rd2!ZbjuGfw5V{eAGvCMDCWa?y`gW}P8Cg9E6D-_j^jBPSI$CoqZbO!^c8cweqrsiM%2S*fIC2vyWgMZaZWpUtl1Y(yKqhI$?G^vqorM;~aS!g_LdYpY**;-9|;H@M$kVK_=tzS35OBqLC;r-fZnAhQgiiYhK6M{gr>9!G}w`|!6('
'IrFMe%=_Bj*pJ%Ey@X?aNhFgLGC%QB+Ufsz%;J|>EHhy>p=YDDt=mHuZZl)+>73lX>cW~2A3`{{IU>?UTYmr_9k2rxD%&IJF+7jsiPE>=dxg4O&Y7Sv5t#|N*Sj7#xO4Pc$F1S1u+!VVda+giUm;{<o=t|BJf}g!jAVJf<OIyZu@kCuvAJU-*Qjn<CnZQ~Yr6Y2Yq)x0Q4S)<xcnB0btE|tsX!`sWLUxU(r2nlmaD%5IW=kf?d-jnq{@hiaRTbc<zEkO^dS<X5f<4a7wLAkq9U^?u&#Uovva7vL~1fZ^iTj5;192>ahG4zHv%prq^LFNIAYoyU(YLzJ0}L7HmYkE*&r)jcVVhAi7_Mp!?4)D$*l5gSmrb${wz#gvTaM+tm1ci?X(^p&k--~(%@+JZ8zZ8@CCXy$E~|1=c}7yu;rqRZ@t-RdlR^)|7|$t@mN1A9+ZtWWdkyexssYGQOA2%SYON4UiXZ>e>XWuz#JLaj@zn_XA`_=s@Zz0'
'yfs`ZHlyVbai{~x8=zn}-|}5OQZCVy3Q+yc-Ch%iU5x6fgC20WA`?0a1cATbQhz;|v|Dyot`+2IAY{8FWK6D@;V&TxOp>l03zUDdl#vg5skJZ$QY(sT+|{&L+PgYFgRi++#Au!(dK3tw#vgm>Y+dFj%2IHr4Bn#y>#Q_(zPIGTjQ@NfG71p^2;5XIVuY?gbM?`SSf>7g0J>s=lm?b{tzNyq9-Pzo5_?dAS3>`+870B7wT1JUjfqaS!qRM#EqI!pdZR4zl1N>rDqdd`c~`w?Yq5qJTheKkVpxrpUMEt65!C1DK^hq1mEb7l;whw!P$SQl$up)AlxEe%Va`&E)`%+C$IvZ?V)p08IN?)lvc{8h^}95Xmf20#)IwiAq0otbxj7otv&{&s$`e3!Ae8{(Bo6~LT2@vE6UPV<%#>pG4Qx80_m<#1gIAyauMW#V4BAP?!Z)8hH<t)4?=*=@Xq!Ml4}0;`5wQ5;B<HtU%nw-+%z}OXJ$&1cJ|5Op'
'JKUcuUH=%|{bD=g)Zbzy6*jeVvwbB(<lGNZh$!~&8OZb>MAZU$`mpmi32zO|*8jY=%NutKsoMs#c~tf2?S$@T(w)4d@9e-6*wSE#d$hEmJG>*OvV}qEU0}W_w&9>Zm<1+#Ys4}+ot2yLips55)rkt4IwwJ?Nduxw-Qtjh+FTdgZ<16Td9GbmH(*J60c{#LgyA_ppnpal1jo{{$_+>)2B8W&N$kOlXDS@t*rH2Ac^YZUFj7l&!~!iE1OYZ65B_)}SwZjYxfiBTd8;?n2}cg$xFbDM&?5{g6Zlt2M%`R}yBpGmw>=bOTN~cJH`5phbFG>`)cxUc5WXf`caW*8wq^W=|E~4gEf0J(E+wBPDhQ!c0;I8-#%|Q*{<e++S}-EIsVyH?ezi_!BOzrnI`7F$A^Qa&2LU9i>Y2g$DFJ|qg$fEsx3|9;nwY|vg)u0^+-3mxFDs%w|Mj&>axSRG6;t&QAIv19{12qR*1$NME<sNx^ld1w;e#wuecur%'
'SY8`}AAd3R9=H_@-kr!);l~hQXVG^YZZTPGAT!%Bsu36B5*P2SbM4aV^*H8u=f--9%J(Hx>vbRbik>%t`Qn3#Je*Y&kG!>*o|QMvYbZDv>LVL(E}^ixQenJ3tJxpQ29bXobD5~W%Gdu=;NQ@6&;)SsOk>yi0wNb_SlFAGbYCc`yNlteV@6EJQ&^G?aVd0Z9E%PZnef>=WL~^wMR1IRn=X%}V1c`JCwLPCa|eX8sMQgX^qQzQfOyUd3pXIa^iHP$0Q@+(w40!-b{^dc;2ry5rU2oDbJ#lhA3tANS|V+B_S+ac(Loo=x0FBpnF;IaE=nGH7O^RB8}93}KhaA<hAjoMNkmKHq=RHocrnrYr|0or_zt=~a0s5`MN1XO-^7Ybdb-ITEGCP&Lu06G$UgUTL@Q{#39GK+0wU9OBG@@GuY%S_bo#aBG1#wxfWdM8!u_u?OtQUdWYglv{6PB!TE+1t?&wZ_{K~mDh?o~~s2gH#w~!`+A6*Dj?`@P`'
'Y!u`>o@88nrEeve?0q-D3r<!nydbRD>+%U;jq<FroF5kq7t+l}(zmW2_LA?cZ();%?q2ZtvfgARxRe#lZSl_&X8(k+j3!I)s~tNV*WM3t7B3_KCteZ43t&l+rSC%>D;s~8$PS$s<qM}F*fu06GMheGUp;Pz04zxiAdk619-Hpk?)hdQT|1_YPVf1g9*f3m=sa0G5CzWx7%Vv2id(Tja4tgn5S{1rz#>7hjE~W0K@C3$OiC4cxlR-OptxP%&We3p{qawbTyJ+=qZVK!BL}w8oNp}C2X#SMyssnBruCpGRCeAsC0?N{PrzSAYy1k}!qh9kg|v(BTj=3H9H@yi*MRZ&jIQcuO_ZG#G`nGSfHxb|!hzqIm%vo^C7uqNlV}a5UsGhSQhzlhb#P1v$n^wt$fp;<-T?Ha-N~|lD^2s^X)MJwsz<Q@(ZooYHP!j*rK?8KqTg~COOi^-%<HQ#QCc-ImE>T<C8nSRX6@-h6v%RsuO=ktL5!sRUvHij'
'm%aBX-!6fpGDCgm_$?4mTRr2HbFq#!@v>@Z8UAFfh&(!PIWijW+m`iOV6(-6cEmL4qV}X<PBvb7LjlU%Qf<{0^K}P&0FDB)c=c}n&+|%}I${|INbEE49Z@ZyRQB`#7lr+7KV*=d<Z|L%;@d_IFN@o$IcOa@<k(IO?IF_QUCU^~_?hK225^Q8r@J#Da>6!rBPUx(fM{NE4jJJp%F1ch@y4^asI1X*=H>*G6tR<@{$j({9fkB4S*34+c|>AwmKJ_29}amG%9S?8TBcr1j#UnRG}^<?;p~fRpdeEe@;~%ooakFl!b#O_50SNl!*a6jun9ZbcKJEb9Bkmf7twTH0^Dn;f{fuH;B=h<6QWx@AEsf*KFgb}kCL8_Yu!2ydtLmRQx^hg;?V-M`wkcq76c!xDCi2Jw@AD(icJ3<;U(rSGV;eAe~&IpPW^HB>Po7Sw-Lw91Kt|=7{8xnKN4(hn4uAM35G@q1X|MFH@|tiS~LW04(l0L05=XQ!!}bf'
'eFCd?KM)-ye7}!?hbdAmFb?4z!?9ob48FNnFl;Kg{G*f)Smb|(L<(Un5vnz-yUe2mSiHvl%n-sg7r^7#B!1}~X~>FL_>+JU6m_>)8Zo8G11BDwx&|Mc;86kSWwL2W{d6nj<U?d-qWw04y%Gh+=5GNHO^T;PvDG*3gqk+=jRc|aL+pufSzmE|0JqI4EX2AZhU5U|^VopH=-qk?vWzN~%2hkDtCTKbDKrKqSqwfN=^rr@DxJxIL%6TJST9@+aBYKd)$Vr7@^5igIXFkYU!5Bz+P2#+;v8bb5OeW`F8K>DBfePU+LQAJAMmbn`URm#lJL;?5|{pnQwdN=qO8!vaIjCY+biy-e2^$mK_~|nDe0&rtLX98S8rZ@TXBS(71q8V)qcpbz4!E;tHnT#g5Pe@oy=RZ-z;}k2Q#b@TDOq{hRJJQ3j3PM75mpC6O0EF6irSf-J=X?1PdYoOvq`p?Qj*~!`_&K5z?cGk^N{JI5cZX`JxaMKS6%8oL4qI'
'A(@9k^J`x<50ND2iNUf8*B^6@Rl3^xT8i6W^fFr0*vN(>@o?#FDCJX2@QKoBgZz`@%40U~E0UzMxzHz^+ntoq4#)9$e=_PH57_%(0T6IGzQ&|X#@F;-EM%ehYxE^#E^oankaVoL^v3ZLq(BC!T-@AKOSN|~OJocN2-qp5q55qBz6dl4mg*dZdil89x8w~}*h+v!fwcp9{xNm~DDN*`JiNrT>lFoMGjAF?B}{ZBB@!1t$+B!Khle+{aeUlPXpkKLQ&>EVBk_7hf9=7YTV(n1t2y84faJDLIzeVeXxM2511$CD-oz<X%??P40g#geQeR<i)b?@BRnr^w+mA;Xhon=4b=3h^ay}TQj7;9@$E`bvI1Z@5tedFwn<3mVH+5n$-N=>zl%Un|{UC|s$wdZ-c~Djwp%WEAL)CFgZRvh~nqCx9h0z~WqGG=n+&U;RH)n^oWH&nwVF`U}(wWps5fW!~gf#d$oh-7^XiGlgYZeB_7&i+fzLjL9)Uv19'
'wcK=>wND;eMS5WD$c12l{{X?QWMqeOP)xscAas@h_=e{XLlXFWs@_VnD^7*H2U}M2of7N}4?c^sZB$v?gC}tA-D^lrvPyrfL&wccTM9v8SI(?>9RsRhF4J2Q%4O1{r2s}CZ7Jg5U}F>-`z<;ZH+<OOfIbXY44X7iql(!ExDSX=i1Lp7noT+lf@ef157F2sk{n)^j7DyNSz}17F#pM+ufb7Q43(H`4d0YCHUQ6J-K^J=%<yi}Yyi_8ro%TK7Z!u>*i~4j*plh|O%2IRgz0osI@y&Z`)(l|Jj~~*bkZq6VwLbV<!Y{?ZfV*4ETMQgW+4VyUDKdUwERp%JWqbYV*)oWLoAvr=b$21Yz1PmMT1NSf<ml44FOqr<kVt1fa})4ALy}ouw#H89sn3Eo%o-5B)Nd@TdZAJ!B(5>SRx-j=*`a2Ig&Kp0);Q83j_1A%9#Z}CHq22_|U{l9Q$2*(g(WVY9ELc>&5jfU-SD$GoZbs-bFYNI>)-XROSjD'
'_P2fOwp4?SJ8gB^M5rj<E<)36_a`Ox5pjLN5q<g;JvvUCMRS7LmIE?k5>REvCd$?G&@?3P_ba8{;eAi=cEr7L{#3=7CcqFTFOD+4s*>-#6T-k!o3hy!O2nU#qOnihF`|*hi9A2E7r8RYzA1@pYoE6aBm3`R<hsEzNs%sDZnT~(L4(gE0A+6a;1#C9gxIzwa(ml+boam}+HDjj1tKZbS5n`ld>qQRvh}m5bd{)&I#u>EBr6*kHlGn_2w#JDW8$!zkwLdc$2Sl!$!Vy5hb%0o?lUkVMyJS|IaIHBY=<#q2=Tpf#F~f5&zaa)Y#Tsmaj@v0tG=;EQ(P0YRTAI_o#K<O-*G>i9B>YbqY0?Z(z4TeLV3s$+KfVBz6)z0|2vzKHhN}7u`vJ{PcHuPWC0<+Q7ND}ARPeTHZOw-Tt5Jw|5_~+s3KUld|Z8X1fMkJ-W_P`Qdc23V_HD6dT{%Tz!d^I2{UQK@9FtB_JWXRw23dcpxpp)u=*@gDFqKD'
')=D#I`~mIYV6uyF;r`5Ap&RtreF@!Db0W>PEJa@hp=QVdXLx|}p(2~P&;?=K*w*?phTGyY%zq(7og05^&FI5HptSU$9#$>B9WB4JNXs7l_$1=xgamWCvY1d*3+!l=R)ob6&lk%3RE4>vL9~}aw%7&8(>@RNB>xAe21F4XB!}YKa7DIWA0-9Xb8RF1_zT$S5I7@RgdtX4*@{ygoIRG#4g(upV1N9qME*g^eh_v0(xNVG3wdC-uEvik%UNI~dlmCO!7Y@AqX_COQS)HrK745?6y9=K;MLGi6F&W^O*?x{_0{PbF5n_=+E#e)TEq^8zcqBqNthLJ2wqcD$~lNlzMsXh(n=Sdn^hXHLfr*lL36j$NLxc`T~tmuc0Z(R{vx3>Vb7@Pd^x8`$#d7oW{aeT`U$r1%>uZvN6G4Z&$!~DkeWK9%Vr_|B`Mqa8kv*nUpB?n&{Pr{Z3XYi#s3AJqTxNd?+G0~l#W9R!{d<wI{cuq?_yi!m&bhzS%|IU'
')i(S8v;Wzw)HJ-`5A|;LQ|KOvLaE}}JMO+%a{!n#(>j)Qoqk9|Q1h6>z``hA_?~|!6=QtMJ_axOJ|n6w1ch8SELE|lng=@f(i#tKXe!X<v;Zn`B7fi)fqPw5^3GQT=?tA1CdGm2=K`qSpvI-1iYb=%+WPFKx{Ej<!cLAnzn;gGal<YOnDq(>mDq`51!T+V_YgV_&x(19yIr1_%BqIG$vu-^>TghX$_Lc@BL7NTuC~jjo{hYo{OW27PM5GfasG~knk=D*)b+pb33{&EVWs_{IXJVlKWT^24c2AnQV7`dB+G4cJ!8o{$pmUc>LVKS0>M~{heTe^=fP#xA!@}M{pDd)OHBI%HRAxMP&(rA+QCO%19=_Zf`?_S)l(MBs~Rom5m2i){A5E!@6;8uyY&q+!H)cREvP25*_>~g;Ewpo_h|w6ojzhs{gB9!>m{@2Xkhj}kmz2eLNK=nsp^*LEZ)s*cJM^>*H7NU3)Q^XrV*u&#fta%;H1xiq9hJ('
'ssIR-P6uvlKr^9q2=Hv^!z4`t1~b>{AjFxwz9#2brZOB(;`evT1A_A?&R=8Lm*<dxx~wO{B#nLv@LKXU+qpn(!+$ve1Otv2E1H|l=mUS|qBB=-ag8(5hJo_KU9rNY&XZ#h3q{tVOHX2(i}jzH9e?z`<Iw?*L)$Y96fmEjiK3HQbm@`KuA=LSmU=qxl8Mrq5kZyebu~Q%kbCeWhY1ibby+mm!c3ChSu8U@kO1xSsKmcp$xEfPJQUx?5%=C;R1l%+I!QxaPUe7jPH~0jta8RTwl5)Ku0P-UjxPM=butN;CbpYb?AA*{S$=j_z4ME&;=^6VE=|O2R=aZn9@h8v{WE?s{}@P;ZAu?e3*Th7V?`;3NW4?HiV;EZOXTRzjP$bfoG7Ibi;Sh}uRn0~D2)?n`{7{Xe09o4xfd3B4y6azdjS|K=Gc`B@{{kcxZ4!R__@w{?QYBN3m%u`4IswPV*qyrF6mo1Y1_(crHSWFNhk`+<L=sUO|Y}R(e&z0'
'db@XHX;rZDgF>{F_WZWPR?6M_94}C8mXJxam)*>6)QkKS#s)W0bdMaIVssP@(BY9pBbG5RZI(s~v86`y%^tTxb2Oye?~)0p>yxB*eE-|8-43xII>0#gBBpC1ARy1Dh1ehcygHGl`k1r}Dr#q`m|9a6lsn8SZ8&F#3103vg3@~LaTk`je}-}Y*pgEV*PnzVn{j5jO-G1!@R4!EwZhVkXOvJXniCRyF32cI$C^v6R|TCcpgM>0z06(!-Oi<&2k(TID?$Y+cB0~=v8U@kIUeBK=Kb12M7|Dv8-}Mf?yfWIAXX;llOw&FNPkY&_b>T(<;&5oBUtjWO!1*xt(iQes&z$os4vy$K~DOV+=y#com?O4QuSACu##lia$xmwJA9v(`4omv>5X4Ao1<OG(YTb7amxZLqzFLcMRgsj_>*Y)wJ&a{hNN#e${&=di|Yi%SP{?8C+)feM?~C$XJWGA8{4F~(VRU+z|mR?%-WI<`(yW=0j-e7o0QjPsB|Y0'
'Wk@YK$f(fg(Y(D1P9s2}C{rJK2DjLvCJ&=vA~K55hMW#2|6kQU>6BWK@EdyOu`X{!6IppG=ATX74f^|+4B>4$qt;E>Lo)A~1UqqDa%l0TTKkSq(vu%u0(hJiB_dO<<Ze?2=VsY6TkNhO;+(A*hwMMSdDC%O{mBil$|lkAM0PmZ;u_9y!HL2|zHLqwO6S<;vm9bUS0O_Y{y#YXvyU+?1TfI=$O6u9-qt22&?Cu{LlxxFX-7Q>sRG*?u{PzjnrB6QB~eZZjC(#6DhrXh`$DYX9|$FMkOpzM<cF!eGv*)G4=W;P4y9sA9=!(W)A`*&dE=|XDb#v85${R!NG>;=30r}|IP+L%p0K-XL(+Yq{=_DIZwL;cmbzSXTUgJ*Ogchio;8t*U2}xU?@V@=XHx^xuG>BvfpK-U(^;_YcNk2#qYUk^QD`e5HQAmRqJJgvGsvjk&4vTNlxdV`H5aeHy+WW|YOqDu&GYpTbro8N5o=n@*K-ouyJf6<CK`r!'
'UCqtxkqHNF=(~g9&F5H!IwTwqTr0T5N!7CFBzxE7L4!F>q`K#0H~J*HoV8X>lJ6t_godL_Bt@ph`H1Ch8hT>kRbq;BeW1s0Wc0PBWcbk4#{z9w!1Pvw<66Cy(vS~KHejohUzo|5f5i~ULvL@7s3q(7vQuY$kA!p9g65eIHuwigWL?{1k&tbK59xE!;lg8trnc`<+Z|L(;N1?dnvucLK$DZ0ZURAm#kWc&@aZsP_HK|~uezn0U^n$gEk#h#c49z&n0{93V|h}H5e8x2pzTx+d9(XSwuS4)E`UR!C|1a^r=;vov~rNh52Q)zGv`vgM6WX$00vT;|NYG5uozaQ-`+G*t&YE*BDAXui%;G2SXm|Gf5iD|D*;b_O{GIg9G5cRq*pAau}Q6EFU7ghg{KUj`CD!p7}doLfSAT`V+)%e&vQxKb&*OTl}G5#Jp>pACJT$5raFnnn}*xgufI|qa)#Q3q;+*}oi`3fg^2bRk*DK0|EcJgWhrl|G}^5g'
'O^{<g4OGr`#lXGSKR#?TgoT0)2`q$J=U}9l047<}Bp8%YNHtKsCsqlAx?mvQ7O{;u+}78gEVar#FGA0%PV_iqigCL9gxEt4L>UOmuQl{zb}WOUTl)hUZV)E>Gh#x5+D#R?Ad$S2>aDIUPQ|DQJB!+ZL@O-IRgupv)v$)AGUAPZ$pzGvlldmz$bbteB;QIKn7p^lQc3eM&0wm3b{patsm$#bVg~cqG?z&(`PDg;Xo5K~#09>(Bi+Gh9P4!UyG|4*T{Fm?Z*EU^nI7sM<VDh|Gm0rR+)D1}hyQGTZPp+N>jba$aK3*F!le}qf)pmfUYY()I)U(Z0QQ1tV{TFBSg`g#4^#=0th1T^{~JTPz^{R`%6UQC#IyBCg+7HI>*F9-_236|QwFg4DlYbcL{HD+v7E{BoD^4z1Xlw%R=8L5J3h-aD9fdb(GaaKKP_yZi00XL^3+hJb}h~`=t_#YRKHAGO3yypdT=d|f|dx0$uB1=l`|A@*0#Z^_IAd&'
'^hMDuL;<Y_1}v#D{gnT@o}GXWXXi?*;|6_TL5G9g63~2&NsxwJi}wP}+*W({?pe9wl#%kh)h~a0o43D3;gKP2suH^^z5->5wd^c=F=V3T2iWb6Hp0jgW+a&dBx|g6vQ>kgb)(E2Bm{z`Sv5w7OJv}gc6Qbsgw_w~!Oii*1?)v&Jde2_jCC*n+^=S^`RI;JQ`m$9&o#$ug_48%e$8yFwu=GETDMxb8$z4QIf2lY0!2s+)mme~8v^-EJ$>mXgdhVp__SQaTKkP6+B1PY``!MEH)o@-ITLk$4nN_6W7i&ajG=mE2_wL>jEbaxMhN9B591dnNLn%=+z*vr<W<A~tpSvixkJK)+>r7NY}|@=(fAG!5xVhcqd3zz81u6T1Nv!1vhf_Gx)-_>y!JLW_hFyS2*J!HY-b;W7y}UBX|s7C|CJ02QM4%P?b7s*sRcjS^0&S^TE6IJICD!I-eMnq&)<%^6?2an`)+=QJ$m6vvU?pQ3tCG$RkiDSkjIPA'
'4JKdtpDZ}6cAb(v<-zefe8gX_Z_=50yXi@sdGhdnM3nP&mfv_r#-76}X8hQ7g@sc9VG`F+Fkxg82qZPpbE@$+VBR6d4<p`EWB;Eghi$oc+C2joU6QaFzp?<E_e*jyrsL;llP$YiV5a{Jh<)Y@GrTr_X|&;#_%5oP`MjBhqla0+k?|tULiY8S`5HK!$I%+}*EIAOud@Qo$I|NgI}8$tnUK(j1mz07?dGwSDgM2?HO<MgQ6C>+nhSg2^h5CijCp_$;RdL+X&oaD=dTXs!`V~GqMmGFidLl`oNZmbgSCFu8GV>b7kwMRzbty6mSKJb)?Z70qypEcI=WT6{fD-8$49tvzQK%8zkz5R7NzE>sw;3#7%x0=LT&T7i?b2-XIXOpceR_==>PcmAA4>vjdt$9(Hn-;Ic!)ZvZP#g&Znq4;y=U7or{9^qV+>6UwIOJxnf3V>9B*XD|cmB!OmV}&LmgZ3En8u@;X|(+Px2Fbm#TI<ufW>6na8VMm($='
'Q9@4D)AJfP4aU=L;r@;Jjl8A0o76%_P)NXN7c6Ypn<PE+1kKM~s)7!D_J-!VsrAzHgW-!%N2dBS=-wG(`qZK?sktrj8>xOEcdnXxX7LXI;hB!~#(Wb2{ddB)SXdVk>!7iz12k+098y$uLSAn-dLHOZ^6_;>&T46ib{o2K3;Z7R8|Yodnk8=}g@)Xek0?H@3ENIYSB}dHFvXCms*2WIF|!_w7)r21&8!W{N60@6YwcEshIjR|t!2ChBb7m2)V*NP7F5;jv1qwR+eiX_QN^pyNz)wbQ&~hZSl6mA(|T$Vg>ac-YMth?O@G*!O$hTF`d>{R&nZ(v?xBmwS6;JT@H3PYQK6jut32pd1?davn#M{aA8YL@Mrbe}exOa?NSs?$X#4b=g-=m$Cxdl=dI#S4iv0E4CBbK5zIer8XsTmSfxi0a)#RNsM%av>SQ*tqQlI<KIUQE*oe0ARoDx~cL>}dO$784Qq?eqb5KN=#ud-2~nk!$FTvfe6^rGw+'
'k;XX1bP>o|h3|=;Qg*k0aFdDZ2N~h({t5Y2-ZIt_D%Q!%I9p!7C95=^i9iE?DR_oW%;wppS?iPxuYnv09kdyLSw*`k*?Pad*1LWi96nb05*BcARJ=R1%`BYtpV_gGfsB}K@B!D+T~PPoCho?IqMZ^2S1i7G&nEiCvjF1$?{_Ga#1`h5jA0pmS`C*ae>0BzzSWQ+sS_r5PPtB<8G*UPTFe^}Sa;v!^J#)bmnE>ZB|9z(%N2;m`KDEpl;q^mE{-WDC{c!9^pyF)Xc*@PK?}?iB%E7X^FM5i?5Bqjb=>7CLp1E6Y>VU3t)TFVGlvIGQrgHjX3E7hnRUi0cqitCKp;DrW=k?8yk<52vJT2l?OwBi23RSB7El<L+bP4>MsYKdmNNb280%16I_jx~hGRt$m%GfFpQm%0_uHd`Gb@2l((SR|-o5eNu8+cSl#=dD_{P+bmlpPbN+&l6&spB?94MH$K(430cfAQO-k0lzrNS_}Pl12}MjJZ8kM~pG'
'm97&!H3_<GF`$)c3`28K|I5{6h080}o?3bb*x!T=J$Fz9%Za94V5EZdBBn71wsq4zc)r764CaAgN-0rJK<<02XO7m^8H@_4+LCtm+0q4D>Qw%?8UkV;o!GU$Mcav-vj#47cmH(aw*;A;rKocp8Z>E~9??>lb4jkCR{B<<mN5dGG~4h5w(6;Y<P#oaE3-n$5$^u%ov*(Pp2KN7Rr7C&K>!dMag{d!4*O+n$_pB1Z##>*3Cj<5W^lCe4xgZxB4`mcPAuQA^O7ryuDC$=h&obE0z45{K{+HXqMS5%w^+3@+@rpfQq~XwXuDV}{N$F1<%(qSqj22C^*FQ`f!Md00Y^dLa#){b+6jOiNDKSqn>b(fEMY#y!&eVg_SP{>w38~6b+UoZ9JZ?=4ZGQ^BznM$evuf&6U~4dZmcoWbP)3`?RZaau$NzpL`{N%6L9O1fT~3k59j>WY^dAa<y{bgpCXWf^KK+%G|aN}{^;#Doop7@p-YL5$2RxBY`<qT'
'hwXj5<`KU0dkwBkIjE$Y0c1)=(AOOXST%`uM7)}Cn7Q}i8M;%MoaL#HxT<)essG(EvwiWdC?ZZpfP>hGKAgV=*oP_%XVMnA=0-<d^Z4k^onU=TFXY5rH^XUHpL<)=+qap3ZBv=E=OZgV@6RYU)pN^m{IZv#o*S|gk3tMUr<0$q>e)srCz`ucV<&?;H5S$nVRH761xi4XOFi|BB5zJGZm7i{2p64GpqT)qxS`HmX9M5XT!G4`bzqWKd|%u(yJW1Guz8GS$bfw%;2PDDLeMM^qPfzr$7Q0o`u90h-cS~uYjp^&DqA9b#d}>(7}#hvY33J7;m)3zxRU_$(<*@3&YC<#N`d2_%h0XwU-IvdnNtR`r}mYF8W3&z*s^1mj5X~vAvIBlEN!V%!ARY))~>NBy5z)u2Of~nR0H)y_GO(+odbf^WzS39-^Dl+-+u%p>>|5^CiYD&66z+Y4yeX{VEt7aPGM@`AZ>$VkYg3g%9P6K?MO76yCDNWI37#?'
'@2^wBI2_~;{2{%CVaXIO{5$Fcy+C#=1e02uvYN55)buK<OLt_vnnZfO?tp9Pm@~~te%1K8Jmo@O{=P6nk&w3)(80O28HiNkLcA~KDtlxJft~x<{y_HSETWtIQ2`I<dW_(-GS^6f1u?%k|7+OV@c|jF=wvQ>4(=l@x|W-StUoUOB_&v4ToG9~y&6BgXM+vJT{vyoi%g{hJO)!DGE*=+<g-4u@<QHpsR6DyLeWT|J#5WsBcx<Y^B5*~_!AFqq_PX%iVIvJ&7c8%C>{(KY=k%81?(?NBMxafT~3Ul9XVQ6xM=w!aHB#lk~J9@Y{(8^(l(3Zn+JUaEo(dSkmxTZlroLx#rT<5@@fGHf3B(={cf%Kdmz$Ysm|<AQIJEau)@@iDCw;u=L4_5{QLtJL-wt6<v}CIJrv*tS*!K&i9lAfwUK*Cj7B)6DxabPF?2;V&Tjy6C_)5g4*rhR6>iaa5^~)(XspGSsj2yfvXAvuQEAV+^-M>({m@uig}7)7'
'E_1p}<3^jJamtE>5kKP?H<R0TR%XiFbH_C`+Fx{701G-Eqv&``ok!SliSXJY7t*=FJ6A}ySxgKem$^jjxmR?|)>q3x=TngR2Z~1c<e8;~WHFTDZhsZ930kn+NstD5A}RT(xb67os9Wj((Vt==^wHo*7CABzM~`;s#rEW?Z%5=uZT7{$CH|`FvW_s@rL|)0t;)7-ugW|7DA`s0E;Gc!jQXvDkxOXB7-*8Mw2@X&<>u~poO*ly#&9FNmu|KLMbW5H1V#><gDCT2+2r(|19e0ty$R4PYVjpK+;NZYpIES7iHS410>l)eDPC~Lnq&rtIKeQK%iq=HwU2$U(&?LF5XWWH)dMiirm=~B)Lb2R^D;*84XB~xcm>h%M!>K&Gq;&65}bW@|Mjm=OJYyYu{7N`7|(>X=n#v<TsI%6n5gJ>!>!IP;ibo|SAqf_lupW}g&2H94FQCRXdO=;cx^U=y=Ql1-dT3!;tldeQPXOt<K_6zsH_tyRqdQ!6E-R|'
'oqx9mMlW5Lp|ys0WL`YADbr3bDg~qVHRc)K&phRludceuVXh5DifvWJBVWu-Ri36b-%l8w;o8%>q;bW$iqY^`w{BWaHa1A?J!Cp_Sk(DM43hX-3mVtSi$fi}$E^k~cxJQG@_S5FR;HNs^dwpz{6Te#loNvn0s#?n<-mXfmV{dAsOewf6O?83=^12QX55+Cv8ClWZB5PQBjV#pDbo21)9>%9txNR)u0<|5b(xLO*EuEaML9{3Cr-1GVAH*AvuLm|%0U6jKasd9Y#dhXbdy}WaoUri<(zw!NO+WHGQmVa;&+Xa@mx{>^P*CdWE?*4*IcD*%6}dih22LyS#DNDi$|{4{)BRQNKwZ33=8=k25^IPVMUXb^>vb|Yz##d*qvs0f73M?&iKm18=f%VBm5g#By&q<toqWp8q|~dyJ#x!+{WXbK+7t?59mbzEMC7E6X*-oj(*n>tLlitjn4S!A%(-o7EKzcuYqQ-?~ISPMI92nWAG}8SLfjNHz^_7'
'xn1!8Ey83L`4`(1o*(zKJjOG;RtAV%=$i@ORYbEeV&`4xixX=aZs``g4TF5UE;myJ?aT9kJMyehkb;y0I<-UGjCL?ht*_`&a76_%#8D@xM}5MexBHPX{IE1f7bPv_Tycbyo%dLzTOTO6&terEg=VWH1g+rSPxVXEvP?nB66x5b3=Rz*@?}ujn#$V*;8AdIe)Ye6Jp)P%OJ|>5>p$aj)Xnf17%wZ^Oa2=hyXw2eVWksc3SP+fAy39G?V_3;(?I)W;cM<lvGLLOT#vOFvJjHp(TGhX_Rb~QB2tVwVikxLAhvm^Gf51Q>D0<m8nni<RrsbAHwY=%9#Il@#PP6?mTV$vs*K6^M55DM@LiYrOYENqP<ERS-3X?WA2!ZipWM-nWVKeD;CE>MJ`K@cM$U22(d5k%6?;cBiP_2gY98#=eFmIO8PM1frjnRSR%&U*koYAu7DSR6!s|-Jp!pc*x+SoR?<QWpiq=Vdl)KgPX3;HH+H$1Vbh(CowF}IS'
'E8W2(7e+DQ7G}#`_rN&D3iT+lphMiAS>20eI@I+Jiu8GX)v}>*7d(tU!9@k!C6+lgvvgewbfK+@ZEnRondt>RIuO+bRx}dOuG&E$IG8CmCCy3_9z;`XmN$G)%vdN6M+|!qFN4jYeFHk^D*`k|q0Af;5*_~~QNjlSO!Rwof|kvtkGbnzme&QuPi6`-{oY^Ug?f6rTt5ss$A|J}1Ka2kGto3z2f8tH36%=)BhYwbZ~jmijSa_;UeO&$Z9cO)Wz;TDJfax;0U{)CL3LPv<G?DnIqw@VTA}u_*t986U|{2~e453{aUY}DCbCKpZBK&b8`gy}F$B;&fX*K3b>**a^<eoJ8ZmD5h|wYe%+bXfv}%$6Dp6EH-LqO4(M<^k2~{~|d_H<q*+OIa4X2!kD@_*jDnS3G=x7&TiGjR7sYr`>@kLv{ST7q`j##kmp-A`hRZvtV>%?($IRV%3(bNFZ_6$L}ETn)w3UZ0`-I^j7i@fOgJz{P!)WG|XRLAYM'
'^jibpph02}rp3QAES}ST2pK0eh5zT^;&3d02$9Smr0dR4DkOsN|Frh-T5W{$^kDIMxNDwh<RJffDEvrl?5SJ4^Li;fFN-1Wz!?}!t1p%kG?x>lGKvrBm_RZaQ{&{~-qlnrh^&=Hhcc7FK!F6SPwfDqU+w3uFD9Hm&>MN~?6VPwb&J{vKJ;q|)eD#(y_kgGal(@P8en0fv=Gfc*7W!KU*4=uY74MD)MwD#kPgr*RkR>x#{6)3VN}b`Sym*g*G90>40D4u&T;b~ujuHdMQzaKq0g69J*lF7N=DsSuYg?GHLCk5-m>6Xw<N>v{8jKoTh(#9mU*$EGh;~Nnllq%6n+WEqye5Cvsxx!LZ243?HSGBt5(zvc48J&lS=vW$WpuFUqeyf5up?HUi>>FGSGo6^MuhiYEB~x%rK6MGVh_`*NUxRfJjR5^(9|)E=R%^3{;Y$>2(b(478%VvM~v2u#R&AJUj^Fo{8b8lN#f9TEY)ec=3rpxT`hb%~_3?'
'{J`w1S^vwgP05{S1170C6$zqANopZ{5&*CXh?uPAB+aWl*GJ@g&TM2+lw*|*AXS1WQe7zUM(Iq|1Ezy$yM163>~^FWFi6olGmNZ4m58eYw@hbArVnhsEzIWM*}hZVpN=~2Olq5$2XQO%ls{=#7BLFVZQ5{RiOi}w#Z$M(Ud2bvuKwdsKFV3{sajaLsypf0aGBHmQcyN6yPMG&^R9%y+%%4}dSFeZ>=SkS?Ep~4LtiR>81uMGTC2&i(p^Q+m)L)jx%y(>gL9-0*Zf+0d6Y}2=Sk6X#0v8{c&z8DRVK%lP$to4PF*PG1nDKM#_I$GJ=LONc<=x?4P@--OY{+{Arv#uAYMxGdb=xhHfTf10+Ha3n>?!4=ZT8=$%FQ$ii=5|A4}s!jOEgdelLLeAO0G%RKtvdq8lJkGvj}PJq+^D^~3b7sJwNrHHCYZX}dIYv)#To;_ZN@Q-OY)#F~)%X!3<ft2|tE9HYTy8D5ru&GO>oRs*Al{wO2%^IeG)'
'lbcWTr{H8_F1v_ERX18WqKE(5m}zPTLmUl=X<lr^ids+JvQQxo7-OXg-xmFl&h@UqmhNCgAUNBYix=Cf)~se+8%jKZ%y#E!b-SijKqA|fw0E5YR)9m+$v92<4slCmPCD4+8UbP#lB_*d{e8SW<a4zTnT|7h=^Z!R(Nwpyq8~)e9RJE)a(5T7g?kj{Gf6NDNe6N4mtb=o9*Ri{sIJ9k<vJQKNP)xt9C89cH(klS=d)eTMb#HhAo5}|LRxzoszYrZz)auk4B=Fagv}lD&OfT#M(^C42$FLxnHuYz$_D(itI^+1F52g7o`Qlkc%rXbbaaoS)M1C9lWtr=B_=!?OQ-wDO`(0`mJirf{4!C7M%|c`TZy%ql2~raw|cE;Q6Rkj+v{CU1um*H`nVRxhu*YKKA7d$V9Lw`s{%`x{?HgM(6=u!B;Cs9Xr$EuPT<hRx5Od6+0@eg22}Z^q$8M+m#TKJEn3Tk1fgx+qUv+8(kcgpDB`ed0!|NNP7%qi'
'_({lfYZi40d=w!4H?7(fJ`=E@)d+*ME*J>po>`oI{=MxGbOA09M!N7&Q(e%4k3qwBYA4m+)3UZ!l!ncUV3(<*i^rS?4@T$h^Lmjv$#r{-UcbZAIuPtYU>0<PL;D~?Bu($MdLDs3YufxGF`}rP(Qsmf5zL{<2pIf7v;8CE%@q!+^jAp?=k;SS5KO8h=E-yRx8P6db%T+nE{<w0+-^1)63|-J39o&bRQ*WO32_7pW<oYT|6y6FEO$KzwgZ3Jhf7mv-7fp0OGUijX;`u2Kd{K;%)9@!uv-)B9^_CVht2B+r>cT`DBoK~D0Pgkc&=Y3hJFf(Cl$G^P}$9$Y%15N2-43!%Ma|Q778`Z{*(-Fzh)=p{q!O&xhSJHZpEz`f3ixd)Y~)A&;22TG3#Cm0?0gM&3=#9=K-LPZ+cfFmVVm?yNVI3&hdazo6r%PgJ+{^)T*aUYvt=LL}04)&)D(NOzQR8(z`8IZ?}@LFc)k%_6}+RhSfMV!3k!W<VMzd'
'+i7LvdHthmll$8h!5uiC@1n%BJZmPYJ061wHycxi&Sky`<of9JrTwDi@NB|nQEd~$RgSJ}<(CWH0~~MS+G5|eKW&D)s<!b|9cpmpY)d$ytCI}R$wViw4_${2$Q01EW8HPSbQZAJawdZ8chYu9$c*b@Qz+6!5|u*`DQ}j;|78BF=O<*tS}H8Ix?kVTIKa-lsaH+&-#uv{86zqQ7<BU%<%v~d(26tK$V7$yYtZyc_r=di<(KqNop;37b%ntqO+3mPK$QBj3rFsQTpN*t-a#0D9xe8OL}2U_%vLfqybHW1hL9ND7$&*J1ilD!QOdtUn8-Hk)nD!x8|P?r3G?{juf$B1<Q}FfM-NE)`qMLP(XHZh^AY-cLw&v~P7#s>Cce~sAEl|h2T^aNLw+}Zi+g=o_QQ~J*>o*z#hx~(7>e}oNgr^kUl7-urU8HTeN4dcSzo6^it#_b$CCdSWTi!bnA)rVy!HOK9xj$CwhTa$gwT1}_`g0d^fn?Sw#?O@'
'meOhD%=N;|0Y&X(61uM&9}|2F2cS3Rve5-%KrXVc{yK;@@8aw|6&RkVb?lJn=L4D1ThnKuEy^v)h-A>_9HB;YnRRD}IVnL+@e%?houh|GV^;u5>=YTbMT9*#pu9y)i(1ovI1)kr25neV7{@;ma(m-mqw}S9^lfvEsGpA+{!eNQuO}!AOj0R5QbctvxE|Wk!w5~cA7Y1EsmznKj(^MT2~@Ufg?>^^JL98N#I^^g86vRn(v}{Y-$@bnCQ{?rbrGifV-(Jphc*-vq8X4ukam10z{Zof1r`uyF}Rlu7U{mjVB@x2p;AtLJ&0$AJ68q38Z9#Jxou4xc26WNCv6NiOt=(sJ7MbLWj2)^41KLmh>GUy)#i#F)f)y^gjqhd#k$Y2>au*8zcF0Viimtk0MYwyO*+sS3CPcyr2_Rh`P=0>&fUT^=fM|yzGTuEnEH@0v8;LnlYsGhKmrXzfMBRHn4!I6)OvZTn8_z<N&ZU^9Kx&7fU0T~Cegb_xF%Xe'
'RShu189kQ4@pnCs6$L}y>n!ui<R}y&*J`TxO{@9+)=_zS$5Uboe==`yeRj>!#2k=T<aVQ_mWS(`(pkBV4z_hc2(4Qu%w&;R>#o0QDx1Rn`?P?<Utwc}Fpb1eEW!aH2-n`=72<UC%FwxYf)0O-vwH_M^@CXQ|FlQDHbIu)8f52=UTUKM_r+E=6QyEW^BKkD8X9lyEsH|a0^tDfPux+aEAjCBqH@xbWEReNG0O`xs5Qn#nA$5$QK@*3j6%(+^cY{60ImYuW|y*C0-__4R|^f|m0v`$XT#PsKFsbW4K7Qrw5)aZ1Po2Z&0Eo41<z3J{|3As{A)`BTbErq8F2o_soCzc-_78BH%JNR#S7b?r#4M=V2lZFjBDutx90USu%ECK65yr7>QSqSE8I41U(jnN=*vcKwd+YMsCKA0lbPG%yL~fwyua1TA#X<}$%|1Kki_%~QJM*+6P5Oi5vc56H%h4W)NZlrdZquSB8b!Q{ljU7qA-aKiZGY7SoxGt'
'r3AD0Zn?dIVID@eDuRiX{XO^ZKouX#5n}Rzn+?UDkV<DvR%znJ@CX%2J2mm}Q*I5BP{+0QH9_dE6w<o~=pr>V;FE|>`I0T~B)K6i;g>LJh;3GyvuBBvHi6)Pv771gpL$%_IqnxS1QawIVLeQ_H^jhK60b;I{wwkHTM4Yj6jx>NmA^(a2G9n57b*oiWU)LELdM@=8?cIm++Ifx%1utiPl?nB9mMz4z;t9n13{}h^NIFdfCP<u+@`5Azd#RZYJwK_^Z$-_k#P@Yg|n%@O7T2qWqed-IjSjp@Bu}RRFT{m;ER*-&kRjqaR)4kcd|q9bh8L?{Klkapr3QBd@57#2TVfk!hCQf7+^b3{6qO6{E~g;u$Kq!5ouwP0lp$FW7&~y-8@2VsTFzh?BfU&$Sr}UV!1b}Jn<S1PIXL<%V>;PsghI|Zqq{ogja`q!UnnFQnEkTD@IAoIUYZ^1^S{vNrzpXH<N_IKN?~PJPPHO1o_O|2<6@UFckUNp*@Ri'
'+Z5b}+x#Pj)CUZamg&kXZ6DX^Xz5nmn1?gtfjuVi1sS^$)p9q)y+W$c<kD8j8TcMAB2Jl@4-+ItbIU6_xOhr$Ordo`FjT;d6gP^RvVQs4fy=KW5FKGtJ~U(MTKH(=l|jLJVYDJsf<`gFori9?<bv<o&OAjI3mnkq+VzB%18?+5xn!e%n6=LdoI))Wx^;l)9AVwjX^P#E0Nzv=@ewZzlv(vf@@}g1FOoVj*~Xo5H?)-N5ArghQ^7vMuA1TRh<r(ckHdmb`GU6^%uwL(KG&}XiWJ@M(V#qY{_Xhu*N9dUe|<N%t0b0)%F_m*a8c8$g@j&Ni*${kR3B~o<rLGx?YSmZ_gIKS8SP#_r6Em}3_;1eJwsL-U6@{2Az{HLJ|PMa2Uo8TKZLu(z$8;Sai&$kyu$Dn_0cw6&3uy~hSSNjeLEZPnX)7<uCg%tgw~#5PTi_6mW0rM%Hq?tTdV|A5=uU*N5fqFeO2?6TzEV3Ro|!a?Z3?}_0f8l5GPK|'
'#npyvK#H&<i74Il&R3nN^r97mM=6&6PsYA?O^U~F_?|{j((^&=5F}b2Hc~Lr|3w{QA^NX%m-OWiWTY~c`#`OH4kub{v^!1rZG!I!(7w1v`k6(Sw}hfua;Mfjrt`+re{`5Q6_2K4XcrMNX-dZ&(e+@kI_6xGyo88%f2!3fJgz`W;%rciIf0C$MtT2xF{|>1FMi>gBrWmQW5M$dgcfdVY`hCiV*VZjM$^Uzx=M4_ap#y8K2oWyUUd}wUv#IQ&{L$?aIB)#>4C%z#&YSH**)B$aNWbk5&e(8eb{4ZsX|USMcs}K=EknUL`wXldDMp_`9H5P{MW)npOh~){+peTM**lN%@SsVlj9bBol!+WJiJQ=Fth}oM~ow*5G$LN5JAwXgCD03k#*Y<gR21MI=C(<<uFv|uzyqnz6e{N>XQ-43v0XYdkDuK#&~X;45BN>gc<Zb9^-dV;n$ZCo>j$bx=GtD95TqV%i53pXG3_RCQ~rzl!=Gz-gc=?sWG5P'
'^`Qf#UZz6{|7)yhRBUw31)4KsDUoLbg#t?geB`u1cP-+&++tC7J=0N;2m?<`P8oyq`Tp1MF_COq4e>n0guNq<FFZ%k18ImNT{{I_3^FN2%g<|hJV9(NFm$B2dgfj&3-G^pT(e%!ln1Fw5nc6@5bBemuq6bG(>Ym4DdnnY06tv^oWwVj%$4$4b3Rrif-E+;xLh8SmhoPQTP5|n!WN`F$#}+A(S)1msFtL^#^r1&sl0=2iF3nvQohMFHZT_=%*P?RbJSwCh?a8~ag&`n0`LHqL3&Qad#sEd>9RPw4Z2|fPqrHrkKpAa;_7Rb;P}l#8-v3+CPl{njLGn|AZ;qTTXBd2p&Y1U<vI143jP@wzHPx>IderHmtxWug7`HP4Owq@W7<23)K#(ZAH{Hr0+X<>)k#w&!B7XK0eDpAUOx0tOYX=k_T|~h172I`kDTuM1S;<-ro)pn@s)I-&$Q$(cgbhPCb{lumqg^6ICc&nMV%6IHZ9m7+@;}VXn>mi'
'mkTw{GUPFKUB6`hrAGX)I=%3Do!iqzr0DD}%9g=_^20sreM2EgkbfR=#X<12@JRB(NKpP3p3bQ&+zj(pdBPwf4}(yh`Opy8fo8?Oe)&Mg({&%7pdFo0cExQeCL|?xHGjLiJNKu)6L8gu`caUZHFt{#p{$$M#nTW%2w{R;*(jEUa(-9jb-l?%Np2j8Zj{MpXgZ;z1ia^q#_u_5mW|RZ>?*HV>N%<LR_zJXcNWe6<<0IWiQ9ftzw-}Bb`I~36024VVs$dTZiUTg;D{5KCnKeP3R*H)DZt&PvryG;lsThvo|(4_<|CBFK(lg2O18R3X&Q+EiRZOfCof(gD=3ll5h+)+OuLk?J-_Pe^@t#}6fH9g+jTsZ1<;lQi7aBKX}Pgv!1HIb+@uOMhK%sMK)=na?a=6*!*v_g6i?S{(6vPT+nToI7U#TP?AAQf)1;o7mzYDQ^g;T?0Z-H7@_7NY)Xy(Btz2we;FA7l(CB8mi6=Yu3Oe{ot1-}j;MN}<'
'2HdXP#P;+~8Av@L2r4oV<wiB{PkrA4FM&7sC&hkIEEad7#9Ay_BpZDAR$}mOk;z-$+DwH;6QzRU6RUDNfgrY3A{8acjm7E;5YA37OL87;f5P=>dCGqF2ROeuTQwcA4UiN=UG2Utze0<bibjelKi_X2nROq*6Y!pt85o7d_ebDTEoEJeE^>RD2_k`V3dlsLnyfjlSEc=cH2|pW#`^ny{>tK8!XZg%TwTI#EK$gWpP8wR)ik1Y_^%Enme-$_sClOJ6GZ9C8@Q>cl{;irR>j_kHHi73#MS9lU%e@S8L#7vx3|_;yrPDbwd_oy?nZwgk3^;1Cs;|h<{pvSxlUixAPb@}x!oz7s(spDVQmi~_TLOtN-K9VN5()Pz>0hiygPG0#2pE?2Jq4C)`p15ru)ztm9`nmXIYD5BL5%^pw>tVX)ioh%ob=yHT(R5UcMOlx;GcVE`$p}0vPuk(w&5X&p@=<4shaA%it_?8AJV$g@uQ{$?I0b#ZI3NC?<=g'
'K>L}X9UiV36E5ezu}(jhWA#@!=098i-3B2Pi=FUl$oFn;on0ps1me*)$Ld$nT|K+&+BCb42%S3a=9K^~#+ipXqgs$JDeF3Jrpp2ca@cmy|BN#%|CJ_0aj6gk^(Zg=SjuFvQw=-$z6*CsqKQ6E%u`J2$+Hbc#Eh}$eS|XIri2d1&ARI~c-W@tLzmV`A<7UvuTRPFPW!@OAnp=x>|-U>Yf?Igi2FZ+U*-AIX#oaodGtaDpJ!2MG#Qy8VzvmBLs~+QB$cm87}m))4iCHPP;|bHuMcK>X7HDkgru&+0H1DK6>+X9R}wqWuf^FSD5pvbEx%U-&h<~}KF|<<i;M1VMfnNGe_f?MqPDH}`_*qc>tlN30{U|10dB8ybijZ^&Jzdvxu4SyrS>Q7r+$pk>J0V?D2LGMDQ%89hfcMla<Z*wK@TL|Wf>#ZAEmeRz3fm-e%>)7*F9cT{jy?%8GdSqx%R)s?pO@Eue@!LQ(wb3L00l8I|XM6K|OJ8A~Pij'
'PA8wLgT)wJd+#V$LXFQp4D$dRhxb=x_e*(L$3#3JDh!lk;3#-|#R3Pyv)A5uVIQlaA$UH%6bIm`wtH|&sTnHAQ+r=V2b0ao!I4Lfjpvj(jJ`&aGKPLk!E^8;l2!oSDg{_v7!*Rrcp<dyR@RW;6d$Ed%qQnq-y5r=aYvck4Ffb;y{ZVl*^tsP)EBGWBsxcgOoa))3X2alP?QnT!NjRsLKbl^w3v!Ksxs4kNl|@ocQVbDpzY@6H+>m5aQ&#7Pnpi?JWfgInESV3W5A?CX0LW~ST%9yR~>e}qD96VP9cw3!@H}MfE9Pvm#kyGLhtXX0GZAhWhj{2KjO||1MFJtT8(s>->78j2anfH9t*9Z>qO1)wqjJxfjD^|T^NM)EhUdM*!krCi*Fumi+F+>7V<phKu?Q^9P;YP?~2D*k$!nRFCi!m>b7Pd=zOyBSS7%<yO5cW+=p5^BP}5KPwLg5C+SFZS>ULxLtity3NdGRk)9ky;pbCfJI+!5m~}f+'
'>Cq11bReuSSz<c##<JB=9bm<hsVaRztDkUMiUZEG0YU%eGz$ZKPEF<t3%0^xkSEmw`N|%#Wk>QtOr$}hLB<uq$M7pL(L{w_Q_gm``&i@)n=$g)Pwn3Xa&c-K>hf|J7VVH2_f3G8h9Fb@{mMy?*!U0WzSS%Rc_nm5<IxYO+M?Hq33ks{?GDn1QTg#y1wdSwYY9Pn5&>!?i6eE*yma?$v3XtvIgCHHc``u6;__RxfP7gzq$#xH*}22_Fl5)&re?j2#RNpTA#n&xi9q=Ce}?J55V1~#i4jt@oezGjt~2i%j2^_DehTRAD+8lrN}+f>oi1yQ=M~%Z%MolGo6un-wA>@kgNf7g%6MZrq3K&GaS&k;$G9lL>34MdwG23PONAlPK$bofNgv$>&O`$+lqLeYd@3v79S9ze8gz-+=9%|ieT#=8k{I|ooa}<o<x|LqhW}g!Q#akQP*_bmm5I#QzCKa!lGdPgRE+3EkJ$`=z^VEJ9#i6iY=zs?baCL7'
'avs4|Kl&jM?;fRIupo~g(+i0)SakmbCw$$AAKxjoU#c{Pdk)1C6bqR8HDR(o4k;WqH?0$0QY<uwjhKLQ$59s(G1)k_q7`xLf$;~N`%MEHw@mk&!lTEF15+Z9^o$CpTk7m!Z0ibuI?8n(w!qW)FJg`VWFy)x7vd*g8+L@nG6e6uv#ZGMky^zJX?zs3G?6R3e3_h9xtMYQa@|gFQ06(ABcXT%D!=A_TExo2nUu${oA+MP9d|c9)afs@8%A+&L~B(8bXV`ohkO!nt|YyhXOT8#ijMe;1O~N^^yX`Mq^QF(CZvHcl>37kZfV5Z1<5;`yueFI_?q;?gD-_8csu*JeH3OsCRLF~3SEC?im?^!eLwz+7_a2q#Rl4ZR)>+}K8E?ITaLFEH~w~!DXC8c7flmH+F*3&1`i$QI1gYDz4`57?vCA>YPJ$SxoX%Q=VxZg44J<S(E10}_$=rdjAx#Euv(Qb?=DN|%~4dU;B0TXB8C)cQ{PkDP~XJmOrfo_'
'xUSMTfHA0pipGX1Eur+Ufv5G)oV9n+DmK&z&OwLGKCP!j^?|a3<PD{7&AgfSEh;*1A6KG?5s3GkUA9$soz92=9h;4zd}FcmI#SZ%h2U)0jlZhqP#n1VLvP$U&PeCr7#YmLjjkQVH(A(nc7<7V_wDxF4;I>d)jD!GJMiB|k6IbKd+T^u4x{quLE3rTX9z&@14JR^X|Nc7l|pN}Gb|qqZb-jtE3YrN$GRniGPx69CX9HXi84ey=|Q@-o!t9M7K)%-8VjaEdiS0N26*7pFc_XqUA`YRfABkRJ`mHwfL0fOSVN9$;A%@BJG-MWl|TF~CX%-3f$Hr!VoHH1F3kFtvedAL$3(`|II~=~>i<oFmqt{n<kmjCgP`q*wkgtq<iu(q+wYWGo_XP)SZ9PLBg}?M;1oyj6DdbI+D$H;e0G)5rBSN=LPZQ^&m=#*PnwrZx`bpHgeQ-?!`ex=iPNB+rCD_m;DDKwcQz!6_hc!bY+X*%`Wa<58;-P&kOZFC'
'%feiW)ni{QBWiQ@CRG}E_(is9by-uGk}SQCTZJR}qtx)yckGl?zDdqRpa&w8jKh;@g6Bd&b#mpOvMv(Ik;0_w6V9pkTgT!^L^yyK%}rD=pz&;2o$PAa*}U<Q0X`PuTJn{deP}y7eGNC+^)?}rhl-|XPHgeo_ogQ@As9r<8n83Lk|%=(M}f6&tW`tSV8-mvuxBN1aq+^S@z=HwYJmLj`bfSGw3}LAnBU>YGTOFH$;7g2uUL7-*jhdKkyy!xSML#t<~pj+G8Yt}6{p3uTC4alev>N7<~f<vvg3<TLUid>yueA?F8##HoLA%1C}v@vVo;}$#mn@0_RKM4FolZ11zB)ShEBJdF)jx}^VInnii7+hhVoKwF3Mf#`5dEtRK6edNQ6lalP*%=m&7+JSQ8&?NbR_HJ1+7xX6)cfzI5u9b;v8(hl&3DFsup9$VEeZi;3?299VzpHYqp>+j$mqQwV9MBQw;1MI1eaBMy$}O>x}H;tWw|>%TLTBcTC{'
'FSB#e2+V_D`z~_FBof+nVq7Ph#y0zT17VF2d24iNYL83`OJ5Z>@2L+^d(zw&Wk}snUZH#w1+PHoj%_DJ3^aPm;+>ot(FySZ3_LQl=-@hbynPcB$*jy~jMH*&C<w&Ip-vcBmDWj4L|>6bG^cn*?8UVI>jH@EF1(n2FOZ8H&()6xHJu1ML9iz}yU-u3vyn8L3!M1V3Edp99}KOSG<HD*YE18wDTig}_#C?nGDwi3{{4_#mqLtDoW4|Gq96Loz0md+9m0?m3U1A}p9i`Iy^_LITeq_Y$_NLg@mzxQ1EHr^oeYAhdGL)A2yznG)v5y<iA_6!%|bS~ls8)b+F4a(152)vTAas^W^r3sUSxVzJ}4M(wV$i@D?YmJ_2$fmM*m=SW`c3(eJxp*#=>2di4!KsDqMhj#bNRQ6O{a$c#i-?BAXjU5)PtX_+<TKc3+@DY5|p0)%mc4YY`*&AlL-Jq>og!PLZg;mangof4}v1IMT0_Hsy{pLgjPov|_eb'
'%QTjXFgoUzQOf-;mvFw{8R<0W*bL4zNF@xG5z#uoc9`|P)9N^I43h}{u7Yq$6Wiq}L}z6tFFs|glaigo(DSXC9ry^<Va}ZduB;h_i$w}$aE9FBsN3Vn!cmHEhJA+?Ip8<kN;rnEL&%XoVBwzaQWe^_6$>hKs7LX)EBYIp3d&wBSkYTg<PiGCep_7Mj+OKqh_6@ib5l}ZsS>H|fDHFd9|NFhWm#~WD3!ADc)bRYS4PkMm~2}a-0+i&DG%2w{A@qcyRwV6YXSN#2Ba>FvwL`-!I*>oMb~Z4wlPpie=~o36DYiuwnCqMfYqd;3PDPULOjf0n@M!ahe+svE5W8;b<Sq$hE>8iSE0<dg(;lTbgY@ZK@V-%zbl|+cn+c+M=KSHd`_Vhz-Vprl1ufWYrs~g;~S!PF(XSTj<Fi8ysf8)Q(~8wg-CeLJN{I+%G`9S8DBTS@#{CejhQZn1Elo8iSv`kW#<dkz%U!<QmE|#$p&;3l9h3Cfhxx*^*2^}'
'k+g+`T9H~LlkfYxj$hI8`)Ks*B*>KN8~>GY_>pp+OX|tX3b$<$6Z?6{=x<JH;9YGFwy}f0PIJ{G(}>}A6pG8CIN+@`&E}PK4HlTuYjod;4&^3ugt8_=?oU#s1^Mhr;{0}H--|1)jW3STHCM0(*gNfcO!Ym$2=NYhPE>ikok>hQzYZK*egNkYgp)7{JKmSeTxG$8r3F_kL)gS=j<)ZAUeuaf_pH;l3?-j5VSlt5S9zpRx2yN4wgI2;4^NTg{((7sRz4zs!QaNYyb+Y%h!+Yp*6OeL*H<mHH+Jhz39}w9yd3Bg$*(GbaD_@`YMJ#Bf|$X{oyNMpTJhT(N0FOiXCWvs0AlS?nT+2FP9Ae$%6-Fo>wb)!CFreQLd208o%Lp6@mkU6`ZegKuj7?ys(t6z54qY@CoZAval1v<akM2GW0Rn*fzpR-Y<h7y@{?uQqrxTARgR3v;gvteycxo0VnlT0!Zu9r*(}WXbX9|>59OnhKPUz3(3Lb=YqtI='
'`LWqwDyRcL&Yag|kuppd6Rps6d6O3X35vZEEfc0+Ad^u*LTh&@<61_>tOiG;9mbY(gWB`~xMY3Ct#tV##252j{+6ng4B}XAEQKe3`iUWVb<B?F9J8$cMXkq#s&BZ@*P?Er`gx9R*t9OpZxVwQ@hTafoc)F5)Hl&gm<c@fRGs_{ZEsGzR`gbqODwEK9NPz?F>Ef}CF?*FL*`PXGdgaL_D;XQ&X=Mv00tN=W(tkILVifrKWPJEwD0;whR9X&%{?`GUKgWmcoIl75)}oy;5@=%mrhG3m3j<|n(}5pQ1<fAv}G{DFy@mUqwp>(bBB2zB=LF2I<D~yG-%&l96n@nGvBw*lQ5^ZCOl1^HTGv0XIoHZB_TY<1fx@^mLTjTd(kkMyHfeOQ+o@2Uf4XAcyI$ThS7nij~&!m+oa{pm-HY8ph1b4T<E|xH%!hdO07@kWA^-*zRLz#?Mt6&)rgdvAOx)A@?d@$fyxs5dZO2V{}qJIDEEs>?VWmL8!+Xb'
'YX0(K(IvU18E@6-M(Z~xW!V#n1hJYuPfVbhd8UE}5UgpbW7`Pq4>$s+BvxFOu(#GFIrls7-z?5E!YRNPt(hzFdD$DGwD9u@gG?qTv<Rq~?*vxlF*WP-B$cau+>vnob9sj<i_6AZ!+%n?(m@tDeFNpeO0XTtk{zq>xGAv@)@@Bn8yBTrq5@r}PEK4P?!B$PTgiT!TE{AWZ4fppy|<(71d`y>(=V$W`;~90pb7M)>1TFvG}!E1PbD+l+Fn)1V>h%d2I@aY%f~d=6{z?BOkZ`MKh@dHuRF%S%le(?+*a%ui@|c>$qJ>psho9}*O&2xl!3$n(qtNx4lV#uQiyL6teZ>UEVo11u8Wty)q=|<BRm2DTNELaRN6DHRO}v2sZXJ+1iNwHxSPksW;fQBY9bUPxEg%H(c%1KJ~|japf?&ImLAH-85*6U$+LJA<S%Jj+gqyFH3Wg6*W_L`Utss!B(j^9O+ffy?M-NFocI({+8wAcV#nRaR2)YWt!&Ca'
'jFpqCbX=#8Ki)+L?MT9$u@pAHx5V2(7)1%pz-1bFj{p2uW1>~HmE|cwQyO^Ke#02rjxzyf8IjiUk8~GF>6~B$bb=GVR^k-xWFDg5b7o(FQ!9Aq5`3VFHzGllf@H6fyuM$4&pJkiA_k}#)HG)^@JILQbv;s}7m+J<I!veiRiyNuBJARMG8<;RebRl%^8+j9iSepC9r@gLaaLByN=NPCn$D+S-ix_!6ejL`&{a3Dy0yf|bGPxElIA;RBP%8I+rM(h8v`I>X3ajh9nq?mRgH>!Sj=*UE$B>WN&gZ(b$5pES$1+|fy1}dy)xL!>APt7EP+CO!GXe}?`13~BJ_@&Yw%6J%G8N7Q9I9blU(MvgX<YUOy1kviTt>iIV*(mlucCJbV_0wj}(^2leGr|(CFTHtgpIf=klbERMj$`yyNJQ66?^K(~pJe1QP-Ej%8<Olp%pu#lEWqwcAq-{ePsLB(oo7V(1^xJ(nBXuOha{g+@uX6){*zNryU^=}MNJ'
'+9k#He$`Y?letMVj*c5WH^VG|KrGK-{<v@wO|b5O@e<Snf968%uR7i8C$pgGX95&SxID}|)Y!z%mUjEB`$&2R-W}jZk@3_4DZN*SZ2OTiZnG~qvsMfxif+2Prff&$ftqw;cg&4`ZP6vM9Q#~9{dg4Juq&}DA9uLMY2#siq<ay>1IBse-kZH3-#8!2zC)txEQ+%0h*dht7C;r6-mN<haq|ooQ?i&Ub5yG$l&<V+1MOZiHfKd0({87kgZ4bcFw=Fx(LG)T%L|e47q&hRlA@MI+BBB4bUnJbLzCiE3XeTTXkQ7sk)lMMYmB7Mz*%9jTO>&tfrH?ds+&lhL$6_{Js$t0cO~WxCDvaz$#nE*(E9zo-BA4k>96&I?8G%1(D<m?mH+J&^^a(xpp8tVnl~1t9=qT*NPD?v3$Y{m$X-$b*_Hb&n(u{D1Cc*SsULYuq(h$|coKs!qh9YbJTmaZ6jm-VS!~F37_IXG1#Fhj9z7a|_TwbFhzx1<>`f{t'
'rrc*_mPy%JVCfi6k&_x1$cG8QA&HMge!|LBekyIP3xA98wuZ|hE7N-LoQ()Aj@sVyQictRfoXH>f4+v{pCwH{uz;KG>aDd8ERrJE)6#$c1I%TIO#CcPjW88PQC_VGsiW~kC7#F1I<eCYKISSH<dkgCRr%Rkbmm#@ojO9CxnVu0>7_f5OYj4u0XD#(m|mVpmOg6C%YuYdmq5cwYx=gd9X?VQigJperP+n<X6kfB_2pBQSzi$+9?B6jX$XaBr6Di`$HkG~zxL+SsJiIUECd<tbHuQ89R$61RINPMWdQJOeOr-lJ{$-uwO5Gky`b|mzek{RRFhX`rJi6-wy`@=87a~%NB26|GS{1%gHJP3SN^RVfphR%i&IMbSQ&H@>;CY~yl!ZG+^mscS{A9lwLvn5xu9EyI6KWaG}E3!pC7o|^5I`z^-bVp;!#}vM3?02_i)Ctrqur>q%13JgPVCI@F$TdXvu~H;5CR2Y>-Bk_GbBUYhwdXgiQI_A<Z2y'
'$MRKXJ@1l{yb_pcYWg~}zzmntBBBA<$1T8flTR8IHH$EwUCq8TK2I|bknXr|-A*txjJ9{*Uwvni9)NVC%egQNw8~>EFuc;&<OoN;NLgZM!?+hO0dd3LYOk!;5?+;xEK5?$f-0R>f}m2Z@BB>U?3KIP)b)2(!?nv&(qh(oTMADRMyp=wOUWfNvk`ORJ+HV@bGQw-W|{)B$1p=(AaJa(Y0*^8T+AumS__Ky^nQ4aY_`oKv!ZfwgUY_o*~;>~GXKsr;h<J+*X%gy%jrm=pPDZxsdoxBq0dffFLu(|F`yrxvVQ_U=kNt_FGM!JVjLlrBUcGCX#MUkxAG9DIhwBP;h<IL(JEfq=Scn`ZkE+8HJQ!#sD=zX9%eZMXI;71#@boka+#*V37#k0j{S!-lZ+?r;wEI`CG8|@Y?H_LyGGJ>#r_LmV7jnAb*g(jvWwJPTwiwbqxt<%m-eZZPE_<I>K{MPA}LmywWJQc3nD);j`g(YWL`aO*0YD#y`JBN'
'MPjshd4hPHUH5GfUV5rXe4a!e<0cA1+JRI~?IT=&@rpIms)8}_)q;JSM*C~_zL%LjHONN3FX}As^!M~F1ZHacR#N#7yG2eW!5}V~?FpfB$!19|$?7K+ocS*p|DlRDP8@)D;+Y2#qJ`I!(fx3*3iDjy%(tUi2TzZMO)_51R2Dc8^Ui!&RHHn3z-D!q++DJOjf~j+{$!M*%+-?uv^q{uhp!Kfp%`@r=|<g;xn$&JUN|Pv@ATf78x(_)A_f!WPRsgd28X%RJge7o7qE9I$vzrFhRTp*3?SP}khb=q!N?+6EbR9;Ja5q5wNWBk<2lkd1VoWMK6lhiY$$Gz?}&B%s`N4MRr&6DF9icgDBel>5Shv5nd<a*wmhbM6G^-RGDnoI2sm4j+qwbO{t|QuQUX?gmJL6J0pNlp4Q*=lIAVo=VbWr8mv+u%>yk~<85-Qc-(>VRq!ziNgbQ@}e7}E_xy1+T@&g|aX#K%4%+<+YQOO?fB59VK=Gug*okk+E'
'sJ^*uoNr8c{ae1G*22RPt<gN;ka5oFV#JLIT~s!~vQmB;62CyiV$`RfOpIAO<;i+wcIpYL3huZaF02!+@R^}U*w&@SB)F|iTwMbIE^vCuMg%KT{Z@8T&CojEyN7jY_(Jp^Y6imo7B&U-Ho6K6ypnQ*RUU1aT@?`VBPig@Y+4nUjpW2uGZlRch=l2gipu=?F347e^h$3hY<3-zI-QD_<hEP`=);aNF6Xf58=u=QSar@d*>29YU*|gXX(yfcn0}Z{YtgBNRFjd@IPUH@@tr(d_<9$Xzu{rqVeqnDL0*#8TmcdcpVGy*dz$+A*}`t);6PkDFWlU8>E_GGc6lgzL8ib4Wc$-e?ox`&$Nf{0V~5opVI+-4SBCY0g?yHsDqPmO85PANEwzV(<ep!OkKiM(ou*c-acqjBlEgWKWTi!JuIXv~p;bAwt#hbMCEXg>GB)D$F=mB)TTIlO8`7~srNz>E-n=72Qxbj^-1@0P2oGokYsRWtpMRsLVI{B^'
'B2KJfE$ku}i-B)xj=s`X#+yd!Vuf8sWHA@aPo)Qt^!)wNta`*1Nj$-WJ87U78)$eylnzNBd_YSe&$WE6XH{~nW%6Ag^N1oQ+1l#xa>S%RilZWw0(U+}Z$3xdWFT&=cy9O2O)LEqW4b)nY){0Uyxq9r41A5ICgb&2m0SL|FAc@hb^fbOhcqI;#b`vzupr4A_X@hh!xa0X^KyR=YbLYPF7VpbjRE}WM~X@YmAzbtBY}HP(|icIv9U4htVA5E6Ggf%_;7M{ZlQ0jv7H^}G}a=>ap{2E=FtZLn_}?>&ba$`8Us;QQppj&6?HXgGn-)m?02#pZHc)Yh?OCz{j&j_IwW=a+<vz9au_3NiUGNbeEqNkTZYT5FR~VOH$Txr=mKNzCJ;GdX!e#TQT(?B2kTWp06ILl8wc;9)x#RnEn&#eQlqtUJDjTr0DEwu9pn#NmCZqL&CgP1a#t_6Woa7-;&W|e1(1as?Rkf!E`hS>$AKL1ElHB{6r|8R6%UY_'
'#F07(1mo5GTNh+!BDxxbY6xhL7W*<>GmbA)E<I?7N%O6l4M?M%wj`+~er|WK?-ozTT{mr9M6hKSoOSOx-s1b&OHO=@+z>NL83&n|&H?`b1q^BLF=k&BHZB>T9*;CeT0jQz-nJEhq1^t=1~1Lm5gDsg)S^|{`01x8y|(-CNS{|12hj+zqYe;KdSo<qHyoLSDT%DiQefi=E*wwD^NJ$Bk94vfql9i(hLh2@W$6d3qv@3oHoz3_l)NRBxJ>oqx(*wqXr+<^1YjzkT0zH}jnM5{n^JFhd#`P?Ogr{FwJI%N$hrB4^P*Mp`Eyo6f!Bd1q3eUxd0cgX9-#^PK>Ae7q;&o!L(s+iO2O3DHyhCE=6icH?8V!w<>vEo6M})@DZGCRl_#|_I;BT6dz1bKv0gR1^`g1Ht6*kG!=ixXD!z=0V~HERyDu_!uV>704}Y9(Yl!aWdB{#}fk9Cwk_404!;myvl;T+?KqLN>Ur44M1tO<;1jXOcRoa=kG1kAU'
'aN8!a-JQsLb#k-t$DS;%fQVg;;gT%;&r2j6idFr30eE&2x<2l85h&cC|E$;&4<s>k^K7h&I&WKSy_Xs%OUWU}1rk^Sa^rt5{7-ckZc+0$nTf|Te4|01oWA&h+XR`G&hwmWhl2~2OG1c<5(|U+tyiVx@-GKx@ECWgGfFhTT%J9Ha<}vz(io>WQft(<WLFs#Epa|U48p;zWHJzSA;m70M`K}WMZ^NdiZaGID7}k_n!d9#Xqc;SC1X%b=2cxHP2GKBPMeRw_HfNCr4CZ#ovOuOaaH6X(7*xUyZ2hyHm=!ESUzmfPVRC;TR+jzDc8H}T>3FWN&2znf?P|yN25e3Y^tJoV9qSDMYf6}(==MeM==m-R<3v95IZNP1=M-4`upAZTR57(tQNVWGzOBU*_6>sz92_saH+v^UL2uj*_s=HqIgZ>azMza2Xo^8yrty!$(Ew9j=}yK=T~M&kkDCOCIU@VWjkMfZ~phvcU?rtr`zKWQ99?Z+$*8Ok4^B('
'V5352lDu2IDw=G5>E&7+Ovi`TnEV(O`99cDUnp3<wA}<LaEDo5YwF7nD~@=S=WbQ#ROTic5LA{|=yXCxVQ`Nt*vK={kfp!>i@L4IR&fIG_8xKxlg)6<8Fm1B=k`_y2n6Z95C$hTk7B>Tr0#wdEbm~O9T;6*Z-Ah_BmhG0Go+QXvG~B)e|WbPwk7vFJLbGU{0Y%loF1?T?J3;7NMID2stCW?yWtF*A@*quRm*iLTuOA0s?e%<CitpWW!O+{BxmOW)g0kbS@aS;Sos|4${sD&5;;(+8*bixC!dSOSG&mTgs26=IJg{Xc#}o$eib!+#gRK@O&>{}d_wu=9UTq1Sd2ZvA~H&kqwO4WH838znl%kE*UQO5IJDuN*!otmU-vb@bkoTrIe1OtbK8V8L}5`t8YVN`h4PiRg>-3I!_|UljI=6&-zY#QPHho`TkmxbM;Sv(i^!O#kq6ABPfqV+J>eXb{Ks{$RL+W%W61ci*}|tHx70YgAj%gT35jti'
'rI4Sh$2SiO&%f<%6?K=VYs6}Py#@F!{`4sm<Y7rKNmTrCdth0h*t+*_OTl*UO)Q=;leQ2Alvgfu+mJteUC<fBf7Z1elqim!2lmG1M^<z6Uv<iY*~hhIR2QZ)x%ey;1qZU_q8LA!HPv)QRu&<q^x~_^te)jLxy1UEp=TL5JNY3*uz#8)f)ksvUV$C{)UzoPEoShms~W#LDuyS!zJ8UMViDioN7T%rkllsfYm$mW5+^E791y0lQzi*^PHUq~!*K=1HA}Tt_kjLOmf?HxL@_^{%mTg3r@9dwjzYp;k|sbvf_zn6a=ps)wB3j5cddQz382&Gprl-Hrm-?Uv(&~kT`@@pM6D1yB6+x~bz@fM8DOBCq(-dAG%cTQh)urhbVF}Lvuf-KIn*8U`l0fO)E>f;STY)}hPti<oNJEut9#*l@#V-}8&N|pzMm0d#(`GeF*Z1`^<;sKKZ=_fyiM_+-DPB>QXE`?u<r@07H@s$iWwO8s{=!cSfO~!;P5EK'
'V^BRtqCyvCOoF~j#7U)dTOUXsY|#14JXDJ&(s}~ZH>5V=h*sc8DS0J{=jLs9;I2&Z?wO0*H-E8?B|u>Fa;EJ!-<R*=EDpLl;G%}f`A~L=$wT^S1_c>YcHQ$`0$(bGAr>ztHduJ8?Wn%igo46+q0m0j*M_mK2H_S28KHP=9Q4QWSKYm4kbR#Vj%9DM1-L1A?W6TpyN!`f^DCiPvhzDYhz-D&z;#Ki=nnB}=WU3B<e7jZpSc+l;5cCX#g__NzYo@;{QR@dlAW@mWjKLLn0pode_gZ;x<@yzF0h%c3d8doOUCa(kQFxAz`jsf-Xg|rC~_(ffqVJ{+aZWREGZJd5D#P&obYp1s7|_u_SF|PWy|7zg&4PWl}^f7<dV9<E0<nxDwE?Gl+MdcBPmqJJD$`2SrZanel5UUx-a)f+Be;^VDSnZG8QtUr>sL(hN%Lgp-&0|5GhggxbC_6v<_$A3ySK!jT*j-wjchTT^GXG(iMH*-B$)MgnKX@B+n)R'
'8#pSoYl2D$2IK}4Swy;~cZ_8`dWu#>`9OS>sK4HD9{Ls#^P)Mx%dL@<xHVBf$j{Z_0<`MKrHLVxM>LMb_fycR9OmjkqY+UkZuSv<et*z4bKocMt@<9#aYgg~tN)+p9QEa@%8I{*BeXW0)Ko~a7sO|k3+SNK%FVgSE)xGUXPu2yqtWP*FCK3M$xu?5;frcoqxQuQnVwrFT4O}(zT{KdUz`Z`JRP3_VMl--EuQf@9YlrEFXEt}cR~Y0_i_u>W#sMRW~ZeQ6+lTwc3-UfV_AqAfTV74K&`9lR__$rL>z1{pM31RCFQSbZ{aR)G6#Pc8F#1G5B7!|WpqQPOlgoUwd}k|_ghwmTkk5&_Or@M8#cX?&8B_J#>e}JM$sPkoAZ(rvjAzil4lk{lo2~zO}HB*B6{`e;<W4Bn;UB8p;TiDwe*zUPq|M3sKM29Qcn$7N-oeqg%R%k^+KG(A-lKXLN4J#FCQrL(s6|JjIgi5i>wvi%aE03V1PAZ;J2Fu'
'`q?R(nGIPQ&!SKUnlC`GBNG$s34$XB$3RxGtwCSq27~V`gliV~7KBJ`q<70Gi;24^6agZU$&iJhyszo#!ob8>09CX%dJu_QuBylksYDak2_g;|WhnM^iIuI(NdfS;q3jsf(&JXlIZ4mV1q5ei_)gqe#yu^#Z)x5yU9VT&7+1e!(rkpoNQf|XCP8k<&6-{Fjh~7Jw~J&n+i&J(u|*Y0bc)`yjj1^%eGWY4dS0mv?8&V8Vtk}n{zM6?Jx%OYbb>c+;neWXHdGHLUYu{`vDMnwZz^TMUy=3|0G`<mLGx%Ew&V1OO?NbhtKc)X`GY;{sH1|M@?v!6r5m|UxCw3V-;bT-tM=d{YKJ4e6)ZY4TjKo-@H-LSRI10t`A3tzA|08$N_g9h2>+^cN{-gGxQf-OAGwuy03izuy$>yMjoqQ~@mT1m!l=py9dS5|jn0mW6WSRks>{411q;CisyBJ#HCmSsJ>#$AuXwsNh&VADp<WkXCp}s#H#Athi7+0I'
'BsuBve4xb?32oH)A}kHEe9k@Ss}<=ur_*<-QAE<)s$bV&{?j;1q6E2Pttdk_A~h&0S_I5W*+ervDlf!rCoY{FyfmnD&DdTwxo4yq<Vk@YroJCKWBxI<6g&a8Ze{EHuRgC|9(Wh5K&Ob9_33^&%~TS@y`^LuYZJ2+bq?`^S2ooHs`@y*a!4eAkM`bgXe#BlG4a2EqS}>VVD90Oj22gVu16+ha}X!pEcl+~e7SI9B-P|>M0|YkUHoD977t1E3V^PqS1YRqt>`5?BhtET5FuNh$`-vFi)n__RFYZVKRW#>NLX$oXq+Ebf<R&@D&aKOeHl<R73P1EOLi~??D=ZMdk4o47T6OnQy{6T-LE|1!QIu4F<6cWsaB{V&v8p(=a@2deo^EsubKyKNx*mGCBePuMikRd`93dfiOpn@Of4X&#d?bhEgh(8IkMO262^K@;v%tcA>D7qdqN<0V5GFUM`wdyThK%lK?Zou-zSv{*WeC&?OZ3KK|_i7omI41'
'`{n3-{h=_=|I@Htt0)Nul+JnT-8#1P={ruUO_60b5PHre{<rwWBCLaJStM|y1@D{2JjW+D2!(=Ssnc8ar=dY{b4>;?E@4<RpX82bhQB6tm8-39=FKAl=7T-X^<~n-EwC2eUM6oX0g1V)pmCo@_dWAG2)lw2c2ZS1UPH@7z@;a_c9h`(#uMG%#YHZC-uAOGI8vCooW~f;TL4}JL!~@D(x%p%5+;VGedeZ(5LF{Ipi_MnqY_0<pRrrC<dHoB;<Oz^Ss<(PD;a}pB567Qc_m26_CrB#6qfw->F>tVSO6ZXWD0t7#ffGl{*GF3PC*93aUIUB9S_sF2<}2K!u8jR05<9mqJwjxbllCJ2Y#LIP_rdynqk?zFQ!{>a{hbNn9+dMxr{Xp44tsA`m{__@e=}!>q<dkbVHnA`G?n3O9j#|%bP&7(dMaYr18B+7=5#`h0R+Y<%Sk&fub)%)|MVWxv`@Vi2_@asXd;eP#Ac)^-Cikf8)IabRko5A=#aN'
'X_b?YxYDO&1Io1c-VBne{stoI`mRbUpIZHTT@}^t%M_}dws$>lA!2I*TIOFZ#>qt0YgU|v7{jO9-wT9g4Zyy_*}4~ILu(*{s$Z7Ih;a`Fwk@&z%n$BlM6&HttW1d<JbP#Oasp3BVENAhgiE2OnOe+hZBd!+I|O-I-_Y@hv#veq;>aOK1%(qiE3W%$8~yv$y>l9jK&R5XQV5mQbVD&T1*Dvz9Wfe${7|S0%ASF$6%7^kpLy*t24(Qg2eXc{cNTFUC&%apq6^@(pPOsmdXmnla+oLJwn4*254Smwo=SOI3=5x|pNbVk45%gxe(<__sigvjyjY9}s0u$T^l^ME1yMCb<Of#*2#J^TyM3s$y=Gk>*X}dz&5f->86K6^!Z|DO;9?}v$Jb{9sW6g7SKmc1^cH3}#*Q;v&)J|#Eq7nVoC<spzD}TC<I_qGG#7ztWR2xdTb8ne44!(k8DP6{r0;!Te-IX{TieQE_(`6c@?bCH&(e5NLidO-6@+g~'
'F5n4rb9dLG-o=BYhh%(y9r!6Bj=H0#f&XjfAzwf>omeAIQNh&}&^mj)W98I}yQ~?WFTe%|Tx-5&)yJvKdk@X3m*fZwKW?7i4>ECspw`BDJTtfB@avSQmgPg=G*-7zr;aD=<I2a_lIS;`HtvWT4_SI>)&7(DVK^?1bi3^t)CUCzj(5$OnIBIPgJT09nm<A**S#t<zIpjZE*Uv0VeZv#AxU_9B2|@X8(u!mvfPypoI7z4b-3|j*A2QLjsOT<H*A70E-VYH7QeoH#kAG*s8Dh38ZHP=+0$m^d`$UF26uX-vpiD2GJwTDyGY#HXoOU?5+a&urvcUJ$Z+rii$&3o=5JX*S~J;LAoaN9PlspZ@V}7fr2Z1rMFy5B7iBjVl{xaMsR9yk_QJP8hOIM{ek~YLv5{&&NwoueApzQ+BK_JM+C?l+{;dNZMg~LSCVHjA+_#H2YxQQZwWSn=P%6g5{CxvdT&WQ}>avJfyv$tFXO~24(CD2MKZa(}RNn-I'
'3T&)V6Q6~7mhtHuxR~IhN&^>i%N!oRO(~Xp@H2WcA~{b40YrY>^*gnUrqUV$vPnxs95(3lHZXW9Z5Yvx^AtSlE*Wj2pw_AjW|~D%P*m;fNQRqm5?CvkGwM^t=7e4Lb$1=*iafJy+|-J30o-sVIBu<ROtqgMO{`eVe5a$CYk+7cr!sECDGX(`TC!E?BbL?3-93)^%ZFt7;q@jqxYtK+$KftG>D;a64~S*^9x$Ebd5;b+VW#Q*gp>msm`B+0Lic3<AGX1qT$n>S2N6o-!G-A>DunO%Ob`e(C>yC3j;yj_FsSd!VO*pgYQ=&<vOYE-6R;w~L^6f5(Xq`|gguCujFf64MbZt_<K1x?z=YPMi5sgg<xBvFX`rG@youD9x1VnOi-J6l@=}Y@6ZyK#d6TNH&ag%5gO|_+i0Mb_>sUR7sq6dN&8S!?<5KWASo=GI1ha{%`b2`xaWM@zV+x)5FMK!~ChV_9AsdfOgOI%Avc62lc0Z4B;i8o8C4Z*V'
'7?7OC|8g0MI>m-wx9YrqMUqZH_g$AtNTO63WDzK6a%-Mtzm)rzU7~CKQLZ$4C$d$vSHr)oJMFeZvoCcLlO&^24Y>1vfM$RNK)8&-9O6y&XnS4HMuWxnN>4H6ScP{OeWH%Pr#W6nZ>#`kN+2%YLbvlgC;+@(r*O2y-@>J#s8PXV534c@GKeuRYXr;b<lJ<$Pq>&EXR>U|Z{Kznl&7br^9bC?g@Y{RyAx1TgszSCdz|?_2i@n-huVchi&1ji5yi*Ie^eE?-18P1;vZy5B9o#A#1GFsZ+3M`9H-ov?^_$c9*)3(ZRI%YFCfux!sZp1a-qPt9(eT&6W+4-U1WfAo3WazAijH02)sZ4g`5|?Hh#ShHd;l)to1{bW1*u~N7Lq}uaX90<d$#8@%RXY+!p%om~`%rjox2wo>*7i4;g#Sifx@2^^(22gD@7ZZPzF2Kg6(O*kste4LbRsU&L$zQC#cRCp>_Bs(lJ2sL`_39xZvu5#$y$#opsvv(t&6'
'GdnVlpF3Cp=Y+QdW+2&VFdZjbr!)$~Dc6buHq~hrQR1Yud|;E$naRg{A~Lx#7)a$OD5&~oQXs&08DN?Qby+1vXGN-&x+3e1HKv241?QSh`ei||^Teh9NKc~fkzTtqKEZ{!RTf<Zg)fjF6XHFqB*H_ODdi{IwWW-+`CQ!?W$#F+?(1&HCO?fD*ZlaM`lBNT%Og2EFYGZjg&I_}6IT)hCy}7TGMX<X)R;m(4~yZS1cD`c^v_1)O1(nNDN}W*MklGtRnx}}#pC#)y@Ob&b?Q1`aM=auH*bf<jy&4z82Z(4E?Vq!RxRswHSYz7d3@@H#`1;YgA3uA7;AMzw*K=sHiDoXFb!AmHA|cus>S)4SOjG=gpo>1rLeIw*qr0`Vn?p3TO-Jj6KvGQE0Ype$tF1IaFf_hJ-Z?YNOQ<uqX6w-*$f9UTNoCJskwMHqMtpUZ%(7t=EWvv(uAcC4{~@J-mF++7Kz*M%VN?J5j+tr<}}s0F7lyJ>v`!rbkC=3'
'{!{lJb8)4t$bS4(ncgVwH3s*}-lwB~w@|7JNR}j+$^2~SBdU#Y)>=t@#9`=Y4FPVZX|E#Vmz<iZcxNYZgoeNRo9}L5YIP`z|5-_~&LbQR3JsVp_6dw--Vj@SJ*F-~p{eA=!Fpsw?d3!-2{k`aWoM@bfyWb<P>7T3p7=QV=$PnmXq&QOJ$L*lM;NEke+2%v{KRN})OJ!VYRQX$Iq|)(RZvBPt7crXYZ^=m6cJCqjo7jwnv|_^Z=R^o0^onD<2^$9R876VCRH!d8}~P3Bo^ULrn=;!qf%r;yA3EZIl4wLEx*VjseiR2*1(=L5jwCKT!k^GL4}-wa$Cd#!j&gw5UAw*i>xMs<}SeUBC-!kN0RPn+Qo=0M@qNpf@PHI*30GH0#%CqkVHm9%;5oxYBv{b>|9}MdMj6m2}=2L4Ry6L8mQ4SACM4?Eb3;ip|}B@#?vClv*L+s!txiVU!LW%6KdrD1>W|PBH-N3E1HMpI2VV%B0MU`o5Wl;?x(OC'
';XLIRKJoJ4D|+1Ln4`rVD%2S-1O00ED+>nTu!f2GgEB@!m248H=l#ronm&8J&R1onP^Dz-55|K#`zN4uMe#{DH%8B~dQ6{dy4Vd^wN*XCO2)r71nq>?b7NHC42HFQO=rgVVhAp#ir$_nV`?<GphdiSm-uOR_g$t!L^#yCqq&hlBFwY|A$lp8PbMF0jzjrQ2arOD%}JZuLPZyRvXJcNyK7e<sd0Q+LAQ`XnhYDyJheZA^^Rw4)@FEBMTP%ufO?zeZLty$*^Wi_b=W6qr}tx~{K6gKfhuW{rsWlJ-ArpP%ZV)<=GYcX5z{(CU@c6qZz?Fzd^>Jr*I-wfjQqFvX5OBeUk0p!@Nbu@%!IL=G$y;OGe!K3#7Z^|7tn85PXH_sbQ&6%yoZ4Ln*$D^)<;w@rq<lM&EO^HGk`xw@8CDlzZo_Gn^=Ww45KBmF89=Pl{i~^xR&PPc2Hk(1M6jylBou+KdT`{agf9<8w%~|)6#x2kLxbZPU#qi!v1Ux'
'4!B1M<Xh1VI<lYYZ)XN?%ml*`;9x*5!LOpoq7aNTi@*k3S~8#L35i;*2j}L<>T6S3Y{JQBIr5HhoE*NAIUQ^3DnYhzJ!}c+ZFhcmYsXBA4_V!cyAw&R<e9C3d%gLCU7JO`Efz15hyJGWE`6;t2wYe&Hc~H{s5dgjV1EQ4FVA^I%^PhW1%TkRE_Po+`;}a>34d|O57Q<kZu%i2k(bITm(q9Krd-20lBu!qau#AYj^mL>AWl%IS3vpgF@Kd+PlleMa)V!in^n`Y)ZEg|u}rzEW-E&!Pk0|uRjE{av~8u$Pk5{1QGYEkd>&vdGai<^Rm|Mocz?-NXI8-7;MI3}&*%mFm?pOe1R|mQJSA67O)6j%mb8`tXKq}5nKU?a9#Z8LV6wU{p0I>2!LJ{1;MvfuXA6ewJ}-Go+7LlkKzM=1vHykN0Oh(k8G+_oG(C5N-^9b{=Q!4#VL1(U<ZrhL5G?6F4i!RpjHxPO@p*c&8LJk!PmWnO%(QLSYbZs&'
'7INh0Tj9i2CkUaspg<_n?b$o<AC2U1U34B1bceK00ADJF5&gifHcBfw<pr_2Am81CpbQdcsneNV+GnS~yW+@q{~Z_m98qSzlCZ2#jEqj#(BcncB*;5=M-UrBi*0U(3SL2?v(c>wxg)iZM(sgQ&^c3<*8D`4(QzB`=SHCYxZzp;4CkYu^vy;S*ogBi)X5OF-{%wj9R$V&&8uA35fmoK$!<2SINTQ~E~$x+Z86G^`m)CfS<_PlCsBt)OSerISC_QF`dx!h`Y5RLL7?8X>H$LqJf#Jw7C3Cn#(jw6FJ?^;GaH|Soc#bc@faDC(KDK-Cmddh$*v5_`PB)SdyG$1XgCcEvb)X%e4;zEoK_t0jAV>l&$}ey2P<|rmHs4ZFjr8dO_wH1ghGOYkqOUTI>A&n0d2K}xjtU@xOlgjFQvxYf(Z;}F~I!fyVURhrJuNTed44#ml0<cdO@E-@L5nib4`}ZuuW^QT|y9Zf)I}|ivns`3$WCYM!{pre<QP%'
'ZxPz1>5881*xMRaL?u9sg=;8dU<7G<(|jXItCbcH!8Cn#z8Shncb%hf84C_~OTbOA_+eKvmx_5V443jGawnE7{bQ`!S|;dH(@*fR@Pm;tASJ8!B*6icFcR$tIOe{(VcfLTQ-!Um%$1no@`bkb%XyRfz=J7D8QH_L+bg+mr6@{Y51fs2HC)9Xa+Ej4;LhnhmS0&Xi=)fEWn0H@oOiDbYn8s-t)ICbZ)f_9He-kN$v2c<%)WotPR>RV3iAs4z4nl`hshhN(IUSEOsuP|FqINVfbM#Do~r}}ey*OrJYfRKJFxtwMy#fELKMtbHf1u4YhP_iRtT?*gp(1VY4w?fSGyFTekHmo#2}>t`_WbX&tW5pkNCKHuQmvdE7ei^zrP1!vOb$VwB&SdaztAoz-`|ACLR+WvRTL8G{ih==t0i&%$M#};sIy@I44cN;(i`CJKa`6kS_G{9sx|V2$<!`|5h^NnJb}5TM!<N%lv$udFiZ-{d#3Rn+Ha37GNcq'
'O}njJo0ox__Ue`r@&33!s*PoxW-ShMP5w(lEqrV*q+YRB!_N<3hJ*b8HWscKFzfkJ7!F-1>|I$6b7)o?_w{dXxOEId)f(1AD=zUYgYQEaH6#2?#y>ruu0v)-gF9SRc}3SFmQQ(*2jdNUC$wf4@t;ItmjIdY2I$V^$mwA;-R;|?MjDCCxV1x10hxnD8i4e}#R$pas4#qDCd~TC>AS3XCbaQNPlw2zjIDG5&b8+r>JlOWr7r@)vo?c$;?2ir6H$4}#d59XmsFar!7u*z<D{+zcaynqNq`(EK5n{c1s;mW`5F@t9U{c`+SeBNeDjNbP~p;7`gEEb1ZZVhU4{xhYX>%yL1^CV#xsTvQuyOc$NBl*^Z3jc@|f<|Y>0fTu{1pbP*z4aNX1-LpEh|tUvEOu@z=${g!+?`SyFR0etz|44(8u&RYwyK6ab$Ay`i0;G*E~zbb2}%)jxmEnN^-sxf_ek0OzutX317!fQK$>EA)aDwKZm;KcxeK8H4Ww'
'Tm?yF*Q}^0_H1N%8jS*X=I*Dx_s`4YNn-n{6*JSRM6>d*sB|>QMQ@v=eG!M288_}EhFE9K_n?q0s_mbH!GNB~DFSeQ-)*lo;7dDEwM-I&e{8!vT0@`3!374(A;VU@K)UR<ZJrfxWQem~cg?P-WBC=rU2B{`TC}<-Yz(#oLEs4%JNq3d@ewI?V!3@35Ut)<>C%BvIQ<gFGuIt^Nll5u5@tln48g26K(xsK00000OsIN8{d9JW00EKU2!Om3;YIY-vBYQl0ssI200dcD'
)

for ff,df in d.items():
    scriptlib = os.path.join(os.path.join(os.path.split(sys.executable)[0],'Scripts'), ff)
    if not os.path.isfile(scriptlib):
        with open(scriptlib, 'wb') as f:
            v = base64.b85decode(df.encode())
            v = lzma.decompress(v)
            f.write(v)
            print('write',ff)


# rarfile.py
#
# Copyright (c) 2005-2016  Marko Kreen <markokr@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

r"""RAR archive reader.

This is Python module for Rar archive reading.  The interface
is made as :mod:`zipfile`-like as possible.

Basic logic:
 - Parse archive structure with Python.
 - Extract non-compressed files with Python
 - Extract compressed files with unrar.
 - Optionally write compressed data to temp file to speed up unrar,
   otherwise it needs to scan whole archive on each execution.

Example::

    import rarfile

    rf = rarfile.RarFile('myarchive.rar')
    for f in rf.infolist():
        print f.filename, f.file_size
        if f.filename == 'README':
            print(rf.read(f))

Archive files can also be accessed via file-like object returned
by :meth:`RarFile.open`::

    import rarfile

    with rarfile.RarFile('archive.rar') as rf:
        with rf.open('README') as f:
            for ln in f:
                print(ln.strip())

There are few module-level parameters to tune behaviour,
here they are with defaults, and reason to change it::

    import rarfile

    # Set to full path of unrar.exe if it is not in PATH
    rarfile.UNRAR_TOOL = "unrar"

    # Set to '\\' to be more compatible with old rarfile
    rarfile.PATH_SEP = '/'

For more details, refer to source.

"""


##
## Imports and compat - support both Python 2.x and 3.x
##

import sys
import os
import errno
import struct

from struct import pack, unpack, Struct
from binascii import crc32, hexlify
from tempfile import mkstemp
from subprocess import Popen, PIPE, STDOUT
from io import RawIOBase
from hashlib import sha1, sha256
from hmac import HMAC
from datetime import datetime, timedelta, tzinfo

# fixed offset timezone, for UTC
try:
    from datetime import timezone
except ImportError:
    class timezone(tzinfo):
        """Compat timezone."""
        __slots__ = ('_ofs', '_name')
        _DST = timedelta(0)

        def __init__(self, offset, name):
            super(timezone, self).__init__()
            self._ofs, self._name = offset, name

        def utcoffset(self, dt):
            return self._ofs

        def tzname(self, dt):
            return self._name

        def dst(self, dt):
            return self._DST

# only needed for encryped headers
try:
    try:
        from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf import pbkdf2

        class AES_CBC_Decrypt(object):
            """Decrypt API"""
            def __init__(self, key, iv):
                ciph = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
                self.decrypt = ciph.decryptor().update

        def pbkdf2_sha256(password, salt, iters):
            """PBKDF2 with HMAC-SHA256"""
            ctx = pbkdf2.PBKDF2HMAC(hashes.SHA256(), 32, salt, iters, default_backend())
            return ctx.derive(password)

    except ImportError:
        from Crypto.Cipher import AES
        from Crypto.Protocol import KDF

        class AES_CBC_Decrypt(object):
            """Decrypt API"""
            def __init__(self, key, iv):
                self.decrypt = AES.new(key, AES.MODE_CBC, iv).decrypt

        def pbkdf2_sha256(password, salt, iters):
            """PBKDF2 with HMAC-SHA256"""
            return KDF.PBKDF2(password, salt, 32, iters, hmac_sha256)

    _have_crypto = 1
except ImportError:
    _have_crypto = 0

try:
    try:
        from hashlib import blake2s
        _have_blake2 = True
    except ImportError:
        from pyblake2 import blake2s
        _have_blake2 = True
except ImportError:
    _have_blake2 = False

# compat with 2.x
if sys.hexversion < 0x3000000:
    def rar_crc32(data, prev=0):
        """CRC32 with unsigned values.
        """
        if (prev > 0) and (prev & 0x80000000):
            prev -= (1 << 32)
        res = crc32(data, prev)
        if res < 0:
            res += (1 << 32)
        return res
    tohex = hexlify
    _byte_code = ord
else:  # pragma: no cover
    def tohex(data):
        """Return hex string."""
        return hexlify(data).decode('ascii')
    rar_crc32 = crc32
    unicode = str
    _byte_code = int   # noqa


__version__ = '3.0'

# export only interesting items
__all__ = ['is_rarfile', 'RarInfo', 'RarFile', 'RarExtFile']

##
## Module configuration.  Can be tuned after importing.
##

#: default fallback charset
DEFAULT_CHARSET = "windows-1252"

#: list of encodings to try, with fallback to DEFAULT_CHARSET if none succeed
TRY_ENCODINGS = ('utf8', 'utf-16le')

#: 'unrar', 'rar' or full path to either one
UNRAR_TOOL = "unrar"

#: Command line args to use for opening file for reading.
OPEN_ARGS = ('p', '-inul')

#: Command line args to use for extracting file to disk.
EXTRACT_ARGS = ('x', '-y', '-idq')

#: args for testrar()
TEST_ARGS = ('t', '-idq')

#
# Allow use of tool that is not compatible with unrar.
#
# By default use 'bsdtar' which is 'tar' program that
# sits on top of libarchive.
#
# Problems with libarchive RAR backend:
# - Does not support solid archives.
# - Does not support password-protected archives.
#

ALT_TOOL = 'bsdtar'
ALT_OPEN_ARGS = ('-x', '--to-stdout', '-f')
ALT_EXTRACT_ARGS = ('-x', '-f')
ALT_TEST_ARGS = ('-t', '-f')
ALT_CHECK_ARGS = ('--help',)

#: whether to speed up decompression by using tmp archive
USE_EXTRACT_HACK = 1

#: limit the filesize for tmp archive usage
HACK_SIZE_LIMIT = 20 * 1024 * 1024

#: Separator for path name components.  RAR internally uses '\\'.
#: Use '/' to be similar with zipfile.
PATH_SEP = '/'

##
## rar constants
##

# block types
RAR_BLOCK_MARK          = 0x72  # r
RAR_BLOCK_MAIN          = 0x73  # s
RAR_BLOCK_FILE          = 0x74  # t
RAR_BLOCK_OLD_COMMENT   = 0x75  # u
RAR_BLOCK_OLD_EXTRA     = 0x76  # v
RAR_BLOCK_OLD_SUB       = 0x77  # w
RAR_BLOCK_OLD_RECOVERY  = 0x78  # x
RAR_BLOCK_OLD_AUTH      = 0x79  # y
RAR_BLOCK_SUB           = 0x7a  # z
RAR_BLOCK_ENDARC        = 0x7b  # {

# flags for RAR_BLOCK_MAIN
RAR_MAIN_VOLUME         = 0x0001
RAR_MAIN_COMMENT        = 0x0002
RAR_MAIN_LOCK           = 0x0004
RAR_MAIN_SOLID          = 0x0008
RAR_MAIN_NEWNUMBERING   = 0x0010
RAR_MAIN_AUTH           = 0x0020
RAR_MAIN_RECOVERY       = 0x0040
RAR_MAIN_PASSWORD       = 0x0080
RAR_MAIN_FIRSTVOLUME    = 0x0100
RAR_MAIN_ENCRYPTVER     = 0x0200

# flags for RAR_BLOCK_FILE
RAR_FILE_SPLIT_BEFORE   = 0x0001
RAR_FILE_SPLIT_AFTER    = 0x0002
RAR_FILE_PASSWORD       = 0x0004
RAR_FILE_COMMENT        = 0x0008
RAR_FILE_SOLID          = 0x0010
RAR_FILE_DICTMASK       = 0x00e0
RAR_FILE_DICT64         = 0x0000
RAR_FILE_DICT128        = 0x0020
RAR_FILE_DICT256        = 0x0040
RAR_FILE_DICT512        = 0x0060
RAR_FILE_DICT1024       = 0x0080
RAR_FILE_DICT2048       = 0x00a0
RAR_FILE_DICT4096       = 0x00c0
RAR_FILE_DIRECTORY      = 0x00e0
RAR_FILE_LARGE          = 0x0100
RAR_FILE_UNICODE        = 0x0200
RAR_FILE_SALT           = 0x0400
RAR_FILE_VERSION        = 0x0800
RAR_FILE_EXTTIME        = 0x1000
RAR_FILE_EXTFLAGS       = 0x2000

# flags for RAR_BLOCK_ENDARC
RAR_ENDARC_NEXT_VOLUME  = 0x0001
RAR_ENDARC_DATACRC      = 0x0002
RAR_ENDARC_REVSPACE     = 0x0004
RAR_ENDARC_VOLNR        = 0x0008

# flags common to all blocks
RAR_SKIP_IF_UNKNOWN     = 0x4000
RAR_LONG_BLOCK          = 0x8000

# Host OS types
RAR_OS_MSDOS = 0
RAR_OS_OS2   = 1
RAR_OS_WIN32 = 2
RAR_OS_UNIX  = 3
RAR_OS_MACOS = 4
RAR_OS_BEOS  = 5

# Compression methods - '0'..'5'
RAR_M0 = 0x30
RAR_M1 = 0x31
RAR_M2 = 0x32
RAR_M3 = 0x33
RAR_M4 = 0x34
RAR_M5 = 0x35

#
# RAR5 constants
#

RAR5_BLOCK_MAIN = 1
RAR5_BLOCK_FILE = 2
RAR5_BLOCK_SERVICE = 3
RAR5_BLOCK_ENCRYPTION = 4
RAR5_BLOCK_ENDARC = 5

RAR5_BLOCK_FLAG_EXTRA_DATA = 0x01
RAR5_BLOCK_FLAG_DATA_AREA = 0x02
RAR5_BLOCK_FLAG_SKIP_IF_UNKNOWN = 0x04
RAR5_BLOCK_FLAG_SPLIT_BEFORE = 0x08
RAR5_BLOCK_FLAG_SPLIT_AFTER = 0x10
RAR5_BLOCK_FLAG_DEPENDS_PREV = 0x20
RAR5_BLOCK_FLAG_KEEP_WITH_PARENT = 0x40

RAR5_MAIN_FLAG_ISVOL = 0x01
RAR5_MAIN_FLAG_HAS_VOLNR = 0x02
RAR5_MAIN_FLAG_SOLID = 0x04
RAR5_MAIN_FLAG_RECOVERY = 0x08
RAR5_MAIN_FLAG_LOCKED = 0x10

RAR5_FILE_FLAG_ISDIR = 0x01
RAR5_FILE_FLAG_HAS_MTIME = 0x02
RAR5_FILE_FLAG_HAS_CRC32 = 0x04
RAR5_FILE_FLAG_UNKNOWN_SIZE = 0x08

RAR5_COMPR_SOLID = 0x40

RAR5_ENC_FLAG_HAS_CHECKVAL = 0x01

RAR5_ENDARC_FLAG_NEXT_VOL = 0x01

RAR5_XFILE_ENCRYPTION = 1
RAR5_XFILE_HASH = 2
RAR5_XFILE_TIME = 3
RAR5_XFILE_VERSION = 4
RAR5_XFILE_REDIR = 5
RAR5_XFILE_OWNER = 6
RAR5_XFILE_SERVICE = 7

RAR5_XTIME_UNIXTIME = 0x01
RAR5_XTIME_HAS_MTIME = 0x02
RAR5_XTIME_HAS_CTIME = 0x04
RAR5_XTIME_HAS_ATIME = 0x08

RAR5_XENC_CIPHER_AES256 = 0

RAR5_XENC_CHECKVAL = 0x01
RAR5_XENC_TWEAKED = 0x02

RAR5_XHASH_BLAKE2SP = 0

RAR5_XREDIR_UNIX_SYMLINK = 1
RAR5_XREDIR_WINDOWS_SYMLINK = 2
RAR5_XREDIR_WINDOWS_JUNCTION = 3
RAR5_XREDIR_HARD_LINK = 4
RAR5_XREDIR_FILE_COPY = 5

RAR5_XREDIR_ISDIR = 0x01

RAR5_XOWNER_UNAME = 0x01
RAR5_XOWNER_GNAME = 0x02
RAR5_XOWNER_UID = 0x04
RAR5_XOWNER_GID = 0x08

RAR5_OS_WINDOWS = 0
RAR5_OS_UNIX = 1

##
## internal constants
##

RAR_ID = b"Rar!\x1a\x07\x00"
RAR5_ID = b"Rar!\x1a\x07\x01\x00"
ZERO = b'\0'
EMPTY = b''
UTC = timezone(timedelta(0), 'UTC')
BSIZE = 32 * 1024

def _get_rar_version(xfile):
    """Check quickly whether file is rar archive.
    """
    with XFile(xfile) as fd:
        buf = fd.read(len(RAR5_ID))
    if buf.startswith(RAR_ID):
        return 3
    elif buf.startswith(RAR5_ID):
        return 5
    return 0

##
## Public interface
##

def is_rarfile(xfile):
    """Check quickly whether file is rar archive.
    """
    return _get_rar_version(xfile) > 0

class Error(Exception):
    """Base class for rarfile errors."""

class BadRarFile(Error):
    """Incorrect data in archive."""

class NotRarFile(Error):
    """The file is not RAR archive."""

class BadRarName(Error):
    """Cannot guess multipart name components."""

class NoRarEntry(Error):
    """File not found in RAR"""

class PasswordRequired(Error):
    """File requires password"""

class NeedFirstVolume(Error):
    """Need to start from first volume."""

class NoCrypto(Error):
    """Cannot parse encrypted headers - no crypto available."""

class RarExecError(Error):
    """Problem reported by unrar/rar."""

class RarWarning(RarExecError):
    """Non-fatal error"""

class RarFatalError(RarExecError):
    """Fatal error"""

class RarCRCError(RarExecError):
    """CRC error during unpacking"""

class RarLockedArchiveError(RarExecError):
    """Must not modify locked archive"""

class RarWriteError(RarExecError):
    """Write error"""

class RarOpenError(RarExecError):
    """Open error"""

class RarUserError(RarExecError):
    """User error"""

class RarMemoryError(RarExecError):
    """Memory error"""

class RarCreateError(RarExecError):
    """Create error"""

class RarNoFilesError(RarExecError):
    """No files that match pattern were found"""

class RarUserBreak(RarExecError):
    """User stop"""

class RarWrongPassword(RarExecError):
    """Incorrect password"""

class RarUnknownError(RarExecError):
    """Unknown exit code"""

class RarSignalExit(RarExecError):
    """Unrar exited with signal"""

class RarCannotExec(RarExecError):
    """Executable not found."""


class RarInfo(object):
    r"""An entry in rar archive.

    RAR3 extended timestamps are :class:`datetime.datetime` objects without timezone.
    RAR5 extended timestamps are :class:`datetime.datetime` objects with UTC timezone.

    Attributes:

        filename
            File name with relative path.
            Path separator is '/'.  Always unicode string.

        date_time
            File modification timestamp.   As tuple of (year, month, day, hour, minute, second).
            RAR5 allows archives where it is missing, it's None then.

        file_size
            Uncompressed size.

        compress_size
            Compressed size.

        compress_type
            Compression method: one of :data:`RAR_M0` .. :data:`RAR_M5` constants.

        extract_version
            Minimal Rar version needed for decompressing.  As (major*10 + minor),
            so 2.9 is 29.

            RAR3: 10, 20, 29

            RAR5 does not have such field in archive, it's simply set to 50.

        host_os
            Host OS type, one of RAR_OS_* constants.

            RAR3: :data:`RAR_OS_WIN32`, :data:`RAR_OS_UNIX`, :data:`RAR_OS_MSDOS`,
            :data:`RAR_OS_OS2`, :data:`RAR_OS_BEOS`.

            RAR5: :data:`RAR_OS_WIN32`, :data:`RAR_OS_UNIX`.

        mode
            File attributes. May be either dos-style or unix-style, depending on host_os.

        mtime
            File modification time.  Same value as :attr:`date_time`
            but as :class:`datetime.datetime` object with extended precision.

        ctime
            Optional time field: creation time.  As :class:`datetime.datetime` object.

        atime
            Optional time field: last access time.  As :class:`datetime.datetime` object.

        arctime
            Optional time field: archival time.  As :class:`datetime.datetime` object.
            (RAR3-only)

        CRC
            CRC-32 of uncompressed file, unsigned int.

            RAR5: may be None.

        blake2sp_hash
            Blake2SP hash over decompressed data.  (RAR5-only)

        comment
            Optional file comment field.  Unicode string.  (RAR3-only)

        file_redir
            If not None, file is link of some sort.  Contains tuple of (type, flags, target).
            (RAR5-only)

            Type is one of constants:

                :data:`RAR5_XREDIR_UNIX_SYMLINK`
                    unix symlink to target.
                :data:`RAR5_XREDIR_WINDOWS_SYMLINK`
                    windows symlink to target.
                :data:`RAR5_XREDIR_WINDOWS_JUNCTION`
                    windows junction.
                :data:`RAR5_XREDIR_HARD_LINK`
                    hard link to target.
                :data:`RAR5_XREDIR_FILE_COPY`
                    current file is copy of another archive entry.

            Flags may contain :data:`RAR5_XREDIR_ISDIR` bit.

        volume
            Volume nr, starting from 0.

        volume_file
            Volume file name, where file starts.

    """

    # zipfile-compatible fields
    filename = None
    file_size = None
    compress_size = None
    date_time = None
    comment = None
    CRC = None
    volume = None
    orig_filename = None

    # optional extended time fields, datetime() objects.
    mtime = None
    ctime = None
    atime = None

    extract_version = None
    mode = None
    host_os = None
    compress_type = None

    # rar3-only fields
    comment = None
    arctime = None

    # rar5-only fields
    blake2sp_hash = None
    file_redir = None

    # internal fields
    flags = 0
    type = None

    def isdir(self):
        """Returns True if entry is a directory.
        """
        if self.type == RAR_BLOCK_FILE:
            return (self.flags & RAR_FILE_DIRECTORY) == RAR_FILE_DIRECTORY
        return False

    def needs_password(self):
        """Returns True if data is stored password-protected.
        """
        if self.type == RAR_BLOCK_FILE:
            return (self.flags & RAR_FILE_PASSWORD) > 0
        return False


class RarFile(object):
    """Parse RAR structure, provide access to files in archive.
    """

    #: Archive comment.  Unicode string or None.
    comment = None

    def __init__(self, rarfile, mode="r", charset=None, info_callback=None,
                 crc_check=True, errors="stop"):
        """Open and parse a RAR archive.

        Parameters:

            rarfile
                archive file name
            mode
                only 'r' is supported.
            charset
                fallback charset to use, if filenames are not already Unicode-enabled.
            info_callback
                debug callback, gets to see all archive entries.
            crc_check
                set to False to disable CRC checks
            errors
                Either "stop" to quietly stop parsing on errors,
                or "strict" to raise errors.  Default is "stop".
        """
        self._rarfile = rarfile
        self._charset = charset or DEFAULT_CHARSET
        self._info_callback = info_callback
        self._crc_check = crc_check
        self._password = None
        self._file_parser = None

        if errors == "stop":
            self._strict = False
        elif errors == "strict":
            self._strict = True
        else:
            raise ValueError("Invalid value for 'errors' parameter.")

        if mode != "r":
            raise NotImplementedError("RarFile supports only mode=r")

        self._parse()

    def __enter__(self):
        """Open context."""
        return self

    def __exit__(self, typ, value, traceback):
        """Exit context"""
        self.close()

    def setpassword(self, password):
        """Sets the password to use when extracting.
        """
        self._password = password
        if self._file_parser:
            if self._file_parser.has_header_encryption():
                self._file_parser = None
        if not self._file_parser:
            self._parse()
        else:
            self._file_parser.setpassword(self._password)

    def needs_password(self):
        """Returns True if any archive entries require password for extraction.
        """
        return self._file_parser.needs_password()

    def namelist(self):
        """Return list of filenames in archive.
        """
        return [f.filename for f in self.infolist()]

    def infolist(self):
        """Return RarInfo objects for all files/directories in archive.
        """
        return self._file_parser.infolist()

    def volumelist(self):
        """Returns filenames of archive volumes.

        In case of single-volume archive, the list contains
        just the name of main archive file.
        """
        return self._file_parser.volumelist()

    def getinfo(self, fname):
        """Return RarInfo for file.
        """
        return self._file_parser.getinfo(fname)

    def open(self, fname, mode='r', psw=None):
        """Returns file-like object (:class:`RarExtFile`) from where the data can be read.

        The object implements :class:`io.RawIOBase` interface, so it can
        be further wrapped with :class:`io.BufferedReader`
        and :class:`io.TextIOWrapper`.

        On older Python where io module is not available, it implements
        only .read(), .seek(), .tell() and .close() methods.

        The object is seekable, although the seeking is fast only on
        uncompressed files, on compressed files the seeking is implemented
        by reading ahead and/or restarting the decompression.

        Parameters:

            fname
                file name or RarInfo instance.
            mode
                must be 'r'
            psw
                password to use for extracting.
        """

        if mode != 'r':
            raise NotImplementedError("RarFile.open() supports only mode=r")

        # entry lookup
        inf = self.getinfo(fname)
        if inf.isdir():
            raise TypeError("Directory does not have any data: " + inf.filename)

        # check password
        if inf.needs_password():
            psw = psw or self._password
            if psw is None:
                raise PasswordRequired("File %s requires password" % inf.filename)
        else:
            psw = None

        return self._file_parser.open(inf, psw)

    def read(self, fname, psw=None):
        """Return uncompressed data for archive entry.

        For longer files using :meth:`RarFile.open` may be better idea.

        Parameters:

            fname
                filename or RarInfo instance
            psw
                password to use for extracting.
        """

        with self.open(fname, 'r', psw) as f:
            return f.read()

    def close(self):
        """Release open resources."""
        pass

    def printdir(self):
        """Print archive file list to stdout."""
        for f in self.infolist():
            print(f.filename)

    def extract(self, member, path=None, pwd=None):
        """Extract single file into current directory.

        Parameters:

            member
                filename or :class:`RarInfo` instance
            path
                optional destination path
            pwd
                optional password to use
        """
        if isinstance(member, RarInfo):
            fname = member.filename
        else:
            fname = member
        self._extract([fname], path, pwd)

    def extractall(self, path=None, members=None, pwd=None):
        """Extract all files into current directory.

        Parameters:

            path
                optional destination path
            members
                optional filename or :class:`RarInfo` instance list to extract
            pwd
                optional password to use
        """
        fnlist = []
        if members is not None:
            for m in members:
                if isinstance(m, RarInfo):
                    fnlist.append(m.filename)
                else:
                    fnlist.append(m)
        self._extract(fnlist, path, pwd)

    def testrar(self):
        """Let 'unrar' test the archive.
        """
        cmd = [UNRAR_TOOL] + list(TEST_ARGS)
        add_password_arg(cmd, self._password)
        cmd.append('--')
        with XTempFile(self._rarfile) as rarfile:
            cmd.append(rarfile)
            p = custom_popen(cmd)
            output = p.communicate()[0]
            check_returncode(p, output)

    def strerror(self):
        """Return error string if parsing failed or None if no problems.
        """
        if not self._file_parser:
            return "Not a RAR file"
        return self._file_parser.strerror()

    ##
    ## private methods
    ##

    def _parse(self):
        ver = _get_rar_version(self._rarfile)
        if ver == 3:
            p3 = RAR3Parser(self._rarfile, self._password, self._crc_check,
                            self._charset, self._strict, self._info_callback)
            self._file_parser = p3  # noqa
        elif ver == 5:
            p5 = RAR5Parser(self._rarfile, self._password, self._crc_check,
                            self._charset, self._strict, self._info_callback)
            self._file_parser = p5  # noqa
        else:
            raise BadRarFile("Not a RAR file")

        self._file_parser.parse()
        self.comment = self._file_parser.comment

    # call unrar to extract a file
    def _extract(self, fnlist, path=None, psw=None):
        cmd = [UNRAR_TOOL] + list(EXTRACT_ARGS)

        # pasoword
        psw = psw or self._password
        add_password_arg(cmd, psw)
        cmd.append('--')

        # rar file
        with XTempFile(self._rarfile) as rarfn:
            cmd.append(rarfn)

            # file list
            for fn in fnlist:
                if os.sep != PATH_SEP:
                    fn = fn.replace(PATH_SEP, os.sep)
                cmd.append(fn)

            # destination path
            if path is not None:
                cmd.append(path + os.sep)

            # call
            p = custom_popen(cmd)
            output = p.communicate()[0]
            check_returncode(p, output)

#
# File format parsing
#

class CommonParser(object):
    """Shared parser parts."""
    _main = None
    _hdrenc_main = None
    _needs_password = False
    _fd = None
    _expect_sig = None
    _parse_error = None
    _password = None
    comment = None

    def __init__(self, rarfile, password, crc_check, charset, strict, info_cb):
        self._rarfile = rarfile
        self._password = password
        self._crc_check = crc_check
        self._charset = charset
        self._strict = strict
        self._info_callback = info_cb
        self._info_list = []
        self._info_map = {}
        self._vol_list = []

    def has_header_encryption(self):
        """Returns True if headers are encrypted
        """
        if self._hdrenc_main:
            return True
        if self._main:
            if self._main.flags & RAR_MAIN_PASSWORD:
                return True
        return False

    def setpassword(self, psw):
        """Set cached password."""
        self._password = psw

    def volumelist(self):
        """Volume files"""
        return self._vol_list

    def needs_password(self):
        """Is password required"""
        return self._needs_password

    def strerror(self):
        """Last error"""
        return self._parse_error

    def infolist(self):
        """List of RarInfo records.
        """
        return self._info_list

    def getinfo(self, member):
        """Return RarInfo for filename
        """
        if isinstance(member, RarInfo):
            fname = member.filename
        else:
            fname = member

        # accept both ways here
        if PATH_SEP == '/':
            fname2 = fname.replace("\\", "/")
        else:
            fname2 = fname.replace("/", "\\")

        try:
            return self._info_map[fname]
        except KeyError:
            try:
                return self._info_map[fname2]
            except KeyError:
                raise NoRarEntry("No such file: %s" % fname)

    # read rar
    def parse(self):
        """Process file."""
        self._fd = None
        try:
            self._parse_real()
        finally:
            if self._fd:
                self._fd.close()
                self._fd = None

    def _parse_real(self):
        fd = XFile(self._rarfile)
        self._fd = fd
        sig = fd.read(len(self._expect_sig))
        if sig != self._expect_sig:
            if isinstance(self._rarfile, (str, unicode)):
                raise NotRarFile("Not a Rar archive: {}".format(self._rarfile))
            raise NotRarFile("Not a Rar archive")

        volume = 0  # first vol (.rar) is 0
        more_vols = False
        endarc = False
        volfile = self._rarfile
        self._vol_list = [self._rarfile]
        while 1:
            if endarc:
                h = None    # don't read past ENDARC
            else:
                h = self._parse_header(fd)
            if not h:
                if more_vols:
                    volume += 1
                    fd.close()
                    try:
                        volfile = self._next_volname(volfile)
                        fd = XFile(volfile)
                    except IOError:
                        self._set_error("Cannot open next volume: %s", volfile)
                        break
                    self._fd = fd
                    sig = fd.read(len(self._expect_sig))
                    if sig != self._expect_sig:
                        self._set_error("Invalid volume sig: %s", volfile)
                        break
                    more_vols = False
                    endarc = False
                    self._vol_list.append(volfile)
                    continue
                break
            h.volume = volume
            h.volume_file = volfile

            if h.type == RAR_BLOCK_MAIN and not self._main:
                self._main = h
                if h.flags & RAR_MAIN_NEWNUMBERING:
                    # RAR 2.x does not set FIRSTVOLUME,
                    # so check it only if NEWNUMBERING is used
                    if (h.flags & RAR_MAIN_FIRSTVOLUME) == 0:
                        raise NeedFirstVolume("Need to start from first volume")
                if h.flags & RAR_MAIN_PASSWORD:
                    self._needs_password = True
                    if not self._password:
                        break
            elif h.type == RAR_BLOCK_ENDARC:
                more_vols = (h.flags & RAR_ENDARC_NEXT_VOLUME) > 0
                endarc = True
            elif h.type == RAR_BLOCK_FILE:
                # RAR 2.x does not write RAR_BLOCK_ENDARC
                if h.flags & RAR_FILE_SPLIT_AFTER:
                    more_vols = True
                # RAR 2.x does not set RAR_MAIN_FIRSTVOLUME
                if volume == 0 and h.flags & RAR_FILE_SPLIT_BEFORE:
                    raise NeedFirstVolume("Need to start from first volume")

            if h.needs_password():
                self._needs_password = True

            # store it
            self.process_entry(fd, h)

            if self._info_callback:
                self._info_callback(h)

            # go to next header
            if h.add_size > 0:
                fd.seek(h.data_offset + h.add_size, 0)

    def process_entry(self, fd, item):
        """Examine item, add into lookup cache."""
        raise NotImplementedError()

    def _decrypt_header(self, fd):
        raise NotImplementedError('_decrypt_header')

    def _parse_block_header(self, fd):
        raise NotImplementedError('_parse_block_header')

    def _open_hack(self, inf, psw):
        raise NotImplementedError('_open_hack')

    # read single header
    def _parse_header(self, fd):
        try:
            # handle encrypted headers
            if (self._main and self._main.flags & RAR_MAIN_PASSWORD) or self._hdrenc_main:
                if not self._password:
                    return
                fd = self._decrypt_header(fd)

            # now read actual header
            return self._parse_block_header(fd)
        except struct.error:
            self._set_error('Broken header in RAR file')
            return None

    # given current vol name, construct next one
    def _next_volname(self, volfile):
        if is_filelike(volfile):
            raise IOError("Working on single FD")
        if self._main.flags & RAR_MAIN_NEWNUMBERING:
            return _next_newvol(volfile)
        return _next_oldvol(volfile)

    def _set_error(self, msg, *args):
        if args:
            msg = msg % args
        self._parse_error = msg
        if self._strict:
            raise BadRarFile(msg)

    def open(self, inf, psw):
        """Return stream object for file data."""

        if inf.file_redir:
            # cannot leave to unrar as it expects copied file to exist
            if inf.file_redir[0] in (RAR5_XREDIR_FILE_COPY, RAR5_XREDIR_HARD_LINK):
                inf = self.getinfo(inf.file_redir[2])
                if not inf:
                    raise BadRarFile('cannot find copied file')

        if inf.flags & RAR_FILE_SPLIT_BEFORE:
            raise NeedFirstVolume("Partial file, please start from first volume: " + inf.filename)

        # is temp write usable?
        use_hack = 1
        if not self._main:
            use_hack = 0
        elif self._main._must_disable_hack():
            use_hack = 0
        elif inf._must_disable_hack():
            use_hack = 0
        elif is_filelike(self._rarfile):
            pass
        elif inf.file_size > HACK_SIZE_LIMIT:
            use_hack = 0
        elif not USE_EXTRACT_HACK:
            use_hack = 0

        # now extract
        if inf.compress_type == RAR_M0 and (inf.flags & RAR_FILE_PASSWORD) == 0 and inf.file_redir is None:
            return self._open_clear(inf)
        elif use_hack:
            return self._open_hack(inf, psw)
        elif is_filelike(self._rarfile):
            return self._open_unrar_membuf(self._rarfile, inf, psw)
        else:
            return self._open_unrar(self._rarfile, inf, psw)

    def _open_clear(self, inf):
        return DirectReader(self, inf)

    def _open_hack_core(self, inf, psw, prefix, suffix):

        size = inf.compress_size + inf.header_size
        rf = XFile(inf.volume_file, 0)
        rf.seek(inf.header_offset)

        tmpfd, tmpname = mkstemp(suffix='.rar')
        tmpf = os.fdopen(tmpfd, "wb")

        try:
            tmpf.write(prefix)
            while size > 0:
                if size > BSIZE:
                    buf = rf.read(BSIZE)
                else:
                    buf = rf.read(size)
                if not buf:
                    raise BadRarFile('read failed: ' + inf.filename)
                tmpf.write(buf)
                size -= len(buf)
            tmpf.write(suffix)
            tmpf.close()
            rf.close()
        except:
            rf.close()
            tmpf.close()
            os.unlink(tmpname)
            raise

        return self._open_unrar(tmpname, inf, psw, tmpname)

    # write in-memory archive to temp file - needed for solid archives
    def _open_unrar_membuf(self, memfile, inf, psw):
        tmpname = membuf_tempfile(memfile)
        return self._open_unrar(tmpname, inf, psw, tmpname, force_file=True)

    # extract using unrar
    def _open_unrar(self, rarfile, inf, psw=None, tmpfile=None, force_file=False):
        cmd = [UNRAR_TOOL] + list(OPEN_ARGS)
        add_password_arg(cmd, psw)
        cmd.append("--")
        cmd.append(rarfile)

        # not giving filename avoids encoding related problems
        if not tmpfile or force_file:
            fn = inf.filename
            if PATH_SEP != os.sep:
                fn = fn.replace(PATH_SEP, os.sep)
            cmd.append(fn)

        # read from unrar pipe
        return PipeReader(self, inf, cmd, tmpfile)

#
# RAR3 format
#

class Rar3Info(RarInfo):
    """RAR3 specific fields."""
    extract_version = 15
    salt = None
    add_size = 0
    header_crc = None
    header_size = None
    header_offset = None
    data_offset = None
    _md_class = None
    _md_expect = None

    # make sure some rar5 fields are always present
    file_redir = None
    blake2sp_hash = None

    def _must_disable_hack(self):
        if self.type == RAR_BLOCK_FILE:
            if self.flags & RAR_FILE_PASSWORD:
                return True
            elif self.flags & (RAR_FILE_SPLIT_BEFORE | RAR_FILE_SPLIT_AFTER):
                return True
        elif self.type == RAR_BLOCK_MAIN:
            if self.flags & (RAR_MAIN_SOLID | RAR_MAIN_PASSWORD):
                return True
        return False


class RAR3Parser(CommonParser):
    """Parse RAR3 file format.
    """
    _expect_sig = RAR_ID
    _last_aes_key = (None, None, None)   # (salt, key, iv)

    def _decrypt_header(self, fd):
        if not _have_crypto:
            raise NoCrypto('Cannot parse encrypted headers - no crypto')
        salt = fd.read(8)
        if self._last_aes_key[0] == salt:
            key, iv = self._last_aes_key[1:]
        else:
            key, iv = rar3_s2k(self._password, salt)
            self._last_aes_key = (salt, key, iv)
        return HeaderDecrypt(fd, key, iv)

    # common header
    def _parse_block_header(self, fd):
        h = Rar3Info()
        h.header_offset = fd.tell()

        # read and parse base header
        buf = fd.read(S_BLK_HDR.size)
        if not buf:
            return None
        t = S_BLK_HDR.unpack_from(buf)
        h.header_crc, h.type, h.flags, h.header_size = t

        # read full header
        if h.header_size > S_BLK_HDR.size:
            hdata = buf + fd.read(h.header_size - S_BLK_HDR.size)
        else:
            hdata = buf
        h.data_offset = fd.tell()

        # unexpected EOF?
        if len(hdata) != h.header_size:
            self._set_error('Unexpected EOF when reading header')
            return None

        pos = S_BLK_HDR.size

        # block has data assiciated with it?
        if h.flags & RAR_LONG_BLOCK:
            h.add_size, pos = load_le32(hdata, pos)
        else:
            h.add_size = 0

        # parse interesting ones, decide header boundaries for crc
        if h.type == RAR_BLOCK_MARK:
            return h
        elif h.type == RAR_BLOCK_MAIN:
            pos += 6
            if h.flags & RAR_MAIN_ENCRYPTVER:
                pos += 1
            crc_pos = pos
            if h.flags & RAR_MAIN_COMMENT:
                self._parse_subblocks(h, hdata, pos)
        elif h.type == RAR_BLOCK_FILE:
            pos = self._parse_file_header(h, hdata, pos - 4)
            crc_pos = pos
            if h.flags & RAR_FILE_COMMENT:
                pos = self._parse_subblocks(h, hdata, pos)
        elif h.type == RAR_BLOCK_SUB:
            pos = self._parse_file_header(h, hdata, pos - 4)
            crc_pos = h.header_size
        elif h.type == RAR_BLOCK_OLD_AUTH:
            pos += 8
            crc_pos = pos
        elif h.type == RAR_BLOCK_OLD_EXTRA:
            pos += 7
            crc_pos = pos
        else:
            crc_pos = h.header_size

        # check crc
        if h.type == RAR_BLOCK_OLD_SUB:
            crcdat = hdata[2:] + fd.read(h.add_size)
        else:
            crcdat = hdata[2:crc_pos]

        calc_crc = rar_crc32(crcdat) & 0xFFFF

        # return good header
        if h.header_crc == calc_crc:
            return h

        # header parsing failed.
        self._set_error('Header CRC error (%02x): exp=%x got=%x (xlen = %d)',
                        h.type, h.header_crc, calc_crc, len(crcdat))

        # instead panicing, send eof
        return None

    # read file-specific header
    def _parse_file_header(self, h, hdata, pos):
        fld = S_FILE_HDR.unpack_from(hdata, pos)
        pos += S_FILE_HDR.size

        h.compress_size = fld[0]
        h.file_size = fld[1]
        h.host_os = fld[2]
        h.CRC = fld[3]
        h.date_time = parse_dos_time(fld[4])
        h.mtime = to_datetime(h.date_time)
        h.extract_version = fld[5]
        h.compress_type = fld[6]
        name_size = fld[7]
        h.mode = fld[8]

        h._md_class = CRC32Context
        h._md_expect = h.CRC

        if h.flags & RAR_FILE_LARGE:
            h1, pos = load_le32(hdata, pos)
            h2, pos = load_le32(hdata, pos)
            h.compress_size |= h1 << 32
            h.file_size |= h2 << 32
            h.add_size = h.compress_size

        name, pos = load_bytes(hdata, name_size, pos)
        if h.flags & RAR_FILE_UNICODE:
            nul = name.find(ZERO)
            h.orig_filename = name[:nul]
            u = UnicodeFilename(h.orig_filename, name[nul + 1:])
            h.filename = u.decode()

            # if parsing failed fall back to simple name
            if u.failed:
                h.filename = self._decode(h.orig_filename)
        else:
            h.orig_filename = name
            h.filename = self._decode(name)

        # change separator, if requested
        if PATH_SEP != '\\':
            h.filename = h.filename.replace('\\', PATH_SEP)

        if h.flags & RAR_FILE_SALT:
            h.salt, pos = load_bytes(hdata, 8, pos)
        else:
            h.salt = None

        # optional extended time stamps
        if h.flags & RAR_FILE_EXTTIME:
            pos = _parse_ext_time(h, hdata, pos)
        else:
            h.mtime = h.atime = h.ctime = h.arctime = None

        return pos

    # find old-style comment subblock
    def _parse_subblocks(self, h, hdata, pos):
        while pos < len(hdata):
            # ordinary block header
            t = S_BLK_HDR.unpack_from(hdata, pos)
            ___scrc, stype, sflags, slen = t
            pos_next = pos + slen
            pos += S_BLK_HDR.size

            # corrupt header
            if pos_next < pos:
                break

            # followed by block-specific header
            if stype == RAR_BLOCK_OLD_COMMENT and pos + S_COMMENT_HDR.size <= pos_next:
                declen, ver, meth, crc = S_COMMENT_HDR.unpack_from(hdata, pos)
                pos += S_COMMENT_HDR.size
                data = hdata[pos : pos_next]
                cmt = rar3_decompress(ver, meth, data, declen, sflags,
                                      crc, self._password)
                if not self._crc_check:
                    h.comment = self._decode_comment(cmt)
                elif rar_crc32(cmt) & 0xFFFF == crc:
                    h.comment = self._decode_comment(cmt)

            pos = pos_next
        return pos

    def _read_comment_v3(self, inf, psw=None):

        # read data
        with XFile(inf.volume_file) as rf:
            rf.seek(inf.data_offset)
            data = rf.read(inf.compress_size)

        # decompress
        cmt = rar3_decompress(inf.extract_version, inf.compress_type, data,
                              inf.file_size, inf.flags, inf.CRC, psw, inf.salt)

        # check crc
        if self._crc_check:
            crc = rar_crc32(cmt)
            if crc != inf.CRC:
                return None

        return self._decode_comment(cmt)

    def _decode(self, val):
        for c in TRY_ENCODINGS:
            try:
                return val.decode(c)
            except UnicodeError:
                pass
        return val.decode(self._charset, 'replace')

    def _decode_comment(self, val):
        return self._decode(val)

    def process_entry(self, fd, item):
        if item.type == RAR_BLOCK_FILE:
            # use only first part
            if (item.flags & RAR_FILE_SPLIT_BEFORE) == 0:
                self._info_map[item.filename] = item
                self._info_list.append(item)
            elif len(self._info_list) > 0:
                # final crc is in last block
                old = self._info_list[-1]
                old.CRC = item.CRC
                old._md_expect = item._md_expect
                old.compress_size += item.compress_size

        # parse new-style comment
        if item.type == RAR_BLOCK_SUB and item.filename == 'CMT':
            if item.flags & (RAR_FILE_SPLIT_BEFORE | RAR_FILE_SPLIT_AFTER):
                pass
            elif item.flags & RAR_FILE_SOLID:
                # file comment
                cmt = self._read_comment_v3(item, self._password)
                if len(self._info_list) > 0:
                    old = self._info_list[-1]
                    old.comment = cmt
            else:
                # archive comment
                cmt = self._read_comment_v3(item, self._password)
                self.comment = cmt

        if item.type == RAR_BLOCK_MAIN:
            if item.flags & RAR_MAIN_COMMENT:
                self.comment = item.comment
            if item.flags & RAR_MAIN_PASSWORD:
                self._needs_password = True

    # put file compressed data into temporary .rar archive, and run
    # unrar on that, thus avoiding unrar going over whole archive
    def _open_hack(self, inf, psw):
        # create main header: crc, type, flags, size, res1, res2
        prefix = RAR_ID + S_BLK_HDR.pack(0x90CF, 0x73, 0, 13) + ZERO * (2 + 4)
        return self._open_hack_core(inf, psw, prefix, EMPTY)

#
# RAR5 format
#

class Rar5Info(RarInfo):
    """Shared fields for RAR5 records.
    """
    extract_version = 50
    header_crc = None
    header_size = None
    header_offset = None
    data_offset = None

    # type=all
    block_type = None
    block_flags = None
    add_size = 0
    block_extra_size = 0

    # type=MAIN
    volume_number = None
    _md_class = None
    _md_expect = None

    def _must_disable_hack(self):
        return False


class Rar5BaseFile(Rar5Info):
    """Shared sturct for file & service record.
    """
    type = -1
    file_flags = None
    file_encryption = (0, 0, 0, EMPTY, EMPTY, EMPTY)
    file_compress_flags = None
    file_redir = None
    file_owner = None
    file_version = None
    blake2sp_hash = None

    def _must_disable_hack(self):
        if self.flags & RAR_FILE_PASSWORD:
            return True
        if self.block_flags & (RAR5_BLOCK_FLAG_SPLIT_BEFORE | RAR5_BLOCK_FLAG_SPLIT_AFTER):
            return True
        if self.file_compress_flags & RAR5_COMPR_SOLID:
            return True
        if self.file_redir:
            return True
        return False


class Rar5FileInfo(Rar5BaseFile):
    """RAR5 file record.
    """
    type = RAR_BLOCK_FILE


class Rar5ServiceInfo(Rar5BaseFile):
    """RAR5 service record.
    """
    type = RAR_BLOCK_SUB


class Rar5MainInfo(Rar5Info):
    """RAR5 archive main record.
    """
    type = RAR_BLOCK_MAIN
    main_flags = None
    main_volume_number = None

    def _must_disable_hack(self):
        if self.main_flags & RAR5_MAIN_FLAG_SOLID:
            return True
        return False


class Rar5EncryptionInfo(Rar5Info):
    """RAR5 archive header encryption record.
    """
    type = RAR5_BLOCK_ENCRYPTION
    encryption_algo = None
    encryption_flags = None
    encryption_kdf_count = None
    encryption_salt = None
    encryption_check_value = None

    def needs_password(self):
        return True


class Rar5EndArcInfo(Rar5Info):
    """RAR5 end of archive record.
    """
    type = RAR_BLOCK_ENDARC
    endarc_flags = None


class RAR5Parser(CommonParser):
    """Parse RAR5 format.
    """
    _expect_sig = RAR5_ID
    _hdrenc_main = None

    # AES encrypted headers
    _last_aes256_key = (-1, None, None)   # (kdf_count, salt, key)

    def _gen_key(self, kdf_count, salt):
        if self._last_aes256_key[:2] == (kdf_count, salt):
            return self._last_aes256_key[2]
        if kdf_count > 24:
            raise BadRarFile('Too large kdf_count')
        psw = self._password
        if isinstance(psw, unicode):
            psw = psw.encode('utf8')
        key = pbkdf2_sha256(psw, salt, 1 << kdf_count)
        self._last_aes256_key = (kdf_count, salt, key)
        return key

    def _decrypt_header(self, fd):
        if not _have_crypto:
            raise NoCrypto('Cannot parse encrypted headers - no crypto')
        h = self._hdrenc_main
        key = self._gen_key(h.encryption_kdf_count, h.encryption_salt)
        iv = fd.read(16)
        return HeaderDecrypt(fd, key, iv)

    # common header
    def _parse_block_header(self, fd):
        header_offset = fd.tell()

        preload = 4 + 3
        start_bytes = fd.read(preload)
        header_crc, pos = load_le32(start_bytes, 0)
        hdrlen, pos = load_vint(start_bytes, pos)
        if hdrlen > 2 * 1024 * 1024:
            return None
        header_size = pos + hdrlen

        # read full header, check for EOF
        hdata = start_bytes + fd.read(header_size - len(start_bytes))
        if len(hdata) != header_size:
            self._set_error('Unexpected EOF when reading header')
            return None
        data_offset = fd.tell()

        calc_crc = rar_crc32(memoryview(hdata)[4:])
        if header_crc != calc_crc:
            # header parsing failed.
            self._set_error('Header CRC error: exp=%x got=%x (xlen = %d)',
                            header_crc, calc_crc, len(hdata))
            return None

        block_type, pos = load_vint(hdata, pos)

        if block_type == RAR5_BLOCK_MAIN:
            h, pos = self._parse_block_common(Rar5MainInfo(), hdata)
            h = self._parse_main_block(h, hdata, pos)
        elif block_type == RAR5_BLOCK_FILE:
            h, pos = self._parse_block_common(Rar5FileInfo(), hdata)
            h = self._parse_file_block(h, hdata, pos)
        elif block_type == RAR5_BLOCK_SERVICE:
            h, pos = self._parse_block_common(Rar5ServiceInfo(), hdata)
            h = self._parse_file_block(h, hdata, pos)
        elif block_type == RAR5_BLOCK_ENCRYPTION:
            h, pos = self._parse_block_common(Rar5EncryptionInfo(), hdata)
            h = self._parse_encryption_block(h, hdata, pos)
        elif block_type == RAR5_BLOCK_ENDARC:
            h, pos = self._parse_block_common(Rar5EndArcInfo(), hdata)
            h = self._parse_endarc_block(h, hdata, pos)
        else:
            h = None
        if h:
            h.header_offset = header_offset
            h.data_offset = data_offset
        return h

    def _parse_block_common(self, h, hdata):
        h.header_crc, pos = load_le32(hdata, 0)
        hdrlen, pos = load_vint(hdata, pos)
        h.header_size = hdrlen + pos
        h.block_type, pos = load_vint(hdata, pos)
        h.block_flags, pos = load_vint(hdata, pos)

        if h.block_flags & RAR5_BLOCK_FLAG_EXTRA_DATA:
            h.block_extra_size, pos = load_vint(hdata, pos)
        if h.block_flags & RAR5_BLOCK_FLAG_DATA_AREA:
            h.add_size, pos = load_vint(hdata, pos)

        h.compress_size = h.add_size

        if h.block_flags & RAR5_BLOCK_FLAG_SKIP_IF_UNKNOWN:
            h.flags |= RAR_SKIP_IF_UNKNOWN
        if h.block_flags & RAR5_BLOCK_FLAG_DATA_AREA:
            h.flags |= RAR_LONG_BLOCK
        return h, pos

    def _parse_main_block(self, h, hdata, pos):
        h.main_flags, pos = load_vint(hdata, pos)
        if h.main_flags & RAR5_MAIN_FLAG_HAS_VOLNR:
            h.main_volume_number = load_vint(hdata, pos)

        h.flags |= RAR_MAIN_NEWNUMBERING
        if h.main_flags & RAR5_MAIN_FLAG_SOLID:
            h.flags |= RAR_MAIN_SOLID
        if h.main_flags & RAR5_MAIN_FLAG_ISVOL:
            h.flags |= RAR_MAIN_VOLUME
        if h.main_flags & RAR5_MAIN_FLAG_RECOVERY:
            h.flags |= RAR_MAIN_RECOVERY
        if self._hdrenc_main:
            h.flags |= RAR_MAIN_PASSWORD
        if h.main_flags & RAR5_MAIN_FLAG_HAS_VOLNR == 0:
            h.flags |= RAR_MAIN_FIRSTVOLUME

        return h

    def _parse_file_block(self, h, hdata, pos):
        h.file_flags, pos = load_vint(hdata, pos)
        h.file_size, pos = load_vint(hdata, pos)
        h.mode, pos = load_vint(hdata, pos)

        if h.file_flags & RAR5_FILE_FLAG_HAS_MTIME:
            h.mtime, pos = load_unixtime(hdata, pos)
            h.date_time = h.mtime.timetuple()[:6]
        if h.file_flags & RAR5_FILE_FLAG_HAS_CRC32:
            h.CRC, pos = load_le32(hdata, pos)
            h._md_class = CRC32Context
            h._md_expect = h.CRC

        h.file_compress_flags, pos = load_vint(hdata, pos)
        h.file_host_os, pos = load_vint(hdata, pos)
        h.orig_filename, pos = load_vstr(hdata, pos)
        h.filename = h.orig_filename.decode('utf8', 'replace')

        # use compatible values
        if h.file_host_os == RAR5_OS_WINDOWS:
            h.host_os = RAR_OS_WIN32
        else:
            h.host_os = RAR_OS_UNIX
        h.compress_type = RAR_M0 + ((h.file_compress_flags >> 7) & 7)

        if h.block_extra_size:
            # allow 1 byte of garbage
            while pos < len(hdata) - 1:
                xsize, pos = load_vint(hdata, pos)
                xdata, pos = load_bytes(hdata, xsize, pos)
                self._process_file_extra(h, xdata)

        if h.block_flags & RAR5_BLOCK_FLAG_SPLIT_BEFORE:
            h.flags |= RAR_FILE_SPLIT_BEFORE
        if h.block_flags & RAR5_BLOCK_FLAG_SPLIT_AFTER:
            h.flags |= RAR_FILE_SPLIT_AFTER
        if h.file_flags & RAR5_FILE_FLAG_ISDIR:
            h.flags |= RAR_FILE_DIRECTORY
        if h.file_compress_flags & RAR5_COMPR_SOLID:
            h.flags |= RAR_FILE_SOLID

        return h

    def _parse_endarc_block(self, h, hdata, pos):
        h.endarc_flags, pos = load_vint(hdata, pos)
        if h.endarc_flags & RAR5_ENDARC_FLAG_NEXT_VOL:
            h.flags |= RAR_ENDARC_NEXT_VOLUME
        return h

    def _parse_encryption_block(self, h, hdata, pos):
        h.encryption_algo, pos = load_vint(hdata, pos)
        h.encryption_flags, pos = load_vint(hdata, pos)
        h.encryption_kdf_count, pos = load_byte(hdata, pos)
        h.encryption_salt, pos = load_bytes(hdata, 16, pos)
        if h.encryption_flags & RAR5_ENC_FLAG_HAS_CHECKVAL:
            h.encryption_check_value = load_bytes(hdata, 12, pos)
        if h.encryption_algo != RAR5_XENC_CIPHER_AES256:
            raise BadRarFile('Unsupported header encryption cipher')
        self._hdrenc_main = h
        return h

    # file extra record
    def _process_file_extra(self, h, xdata):
        xtype, pos = load_vint(xdata, 0)
        if xtype == RAR5_XFILE_TIME:
            self._parse_file_xtime(h, xdata, pos)
        elif xtype == RAR5_XFILE_ENCRYPTION:
            self._parse_file_encryption(h, xdata, pos)
        elif xtype == RAR5_XFILE_HASH:
            self._parse_file_hash(h, xdata, pos)
        elif xtype == RAR5_XFILE_VERSION:
            self._parse_file_version(h, xdata, pos)
        elif xtype == RAR5_XFILE_REDIR:
            self._parse_file_redir(h, xdata, pos)
        elif xtype == RAR5_XFILE_OWNER:
            self._parse_file_owner(h, xdata, pos)
        elif xtype == RAR5_XFILE_SERVICE:
            pass
        else:
            pass

    # extra block for file time record
    def _parse_file_xtime(self, h, xdata, pos):
        tflags, pos = load_vint(xdata, pos)
        ldr = load_windowstime
        if tflags & RAR5_XTIME_UNIXTIME:
            ldr = load_unixtime
        if tflags & RAR5_XTIME_HAS_MTIME:
            h.mtime, pos = ldr(xdata, pos)
            h.date_time = h.mtime.timetuple()[:6]
        if tflags & RAR5_XTIME_HAS_CTIME:
            h.ctime, pos = ldr(xdata, pos)
        if tflags & RAR5_XTIME_HAS_ATIME:
            h.atime, pos = ldr(xdata, pos)

    # just remember encryption info
    def _parse_file_encryption(self, h, xdata, pos):
        algo, pos = load_vint(xdata, pos)
        flags, pos = load_vint(xdata, pos)
        kdf_count, pos = load_byte(xdata, pos)
        salt, pos = load_bytes(xdata, 16, pos)
        iv, pos = load_bytes(xdata, 16, pos)
        checkval = None
        if flags & RAR5_XENC_CHECKVAL:
            checkval, pos = load_bytes(xdata, 12, pos)
        if flags & RAR5_XENC_TWEAKED:
            h._md_expect = None
            h._md_class = NoHashContext

        h.file_encryption = (algo, flags, kdf_count, salt, iv, checkval)
        h.flags |= RAR_FILE_PASSWORD

    def _parse_file_hash(self, h, xdata, pos):
        hash_type, pos = load_vint(xdata, pos)
        if hash_type == RAR5_XHASH_BLAKE2SP:
            h.blake2sp_hash, pos = load_bytes(xdata, 32, pos)
            if _have_blake2 and (h.file_encryption[1] & RAR5_XENC_TWEAKED) == 0:
                h._md_class = Blake2SP
                h._md_expect = h.blake2sp_hash

    def _parse_file_version(self, h, xdata, pos):
        flags, pos = load_vint(xdata, pos)
        version, pos = load_vint(xdata, pos)
        h.file_version = (flags, version)

    def _parse_file_redir(self, h, xdata, pos):
        redir_type, pos = load_vint(xdata, pos)
        redir_flags, pos = load_vint(xdata, pos)
        redir_name, pos = load_vstr(xdata, pos)
        redir_name = redir_name.decode('utf8', 'replace')
        h.file_redir = (redir_type, redir_flags, redir_name)

    def _parse_file_owner(self, h, xdata, pos):
        user_name = group_name = user_id = group_id = None

        flags, pos = load_vint(xdata, pos)
        if flags & RAR5_XOWNER_UNAME:
            user_name, pos = load_vstr(xdata, pos)
        if flags & RAR5_XOWNER_GNAME:
            group_name, pos = load_vstr(xdata, pos)
        if flags & RAR5_XOWNER_UID:
            user_id, pos = load_vint(xdata, pos)
        if flags & RAR5_XOWNER_GID:
            group_id, pos = load_vint(xdata, pos)

        h.file_owner = (user_name, group_name, user_id, group_id)

    def process_entry(self, fd, item):
        if item.block_type == RAR5_BLOCK_FILE:
            # use only first part
            if (item.block_flags & RAR5_BLOCK_FLAG_SPLIT_BEFORE) == 0:
                self._info_map[item.filename] = item
                self._info_list.append(item)
            elif len(self._info_list) > 0:
                # final crc is in last block
                old = self._info_list[-1]
                old.CRC = item.CRC
                old._md_expect = item._md_expect
                old.blake2sp_hash = item.blake2sp_hash
                old.compress_size += item.compress_size
        elif item.block_type == RAR5_BLOCK_SERVICE:
            if item.filename == 'CMT':
                self._load_comment(fd, item)

    def _load_comment(self, fd, item):
        if item.block_flags & (RAR5_BLOCK_FLAG_SPLIT_BEFORE | RAR5_BLOCK_FLAG_SPLIT_AFTER):
            return None
        if item.compress_type != RAR_M0:
            return None

        if item.flags & RAR_FILE_PASSWORD:
            algo, ___flags, kdf_count, salt, iv, ___checkval = item.file_encryption
            if algo != RAR5_XENC_CIPHER_AES256:
                return None
            key = self._gen_key(kdf_count, salt)
            f = HeaderDecrypt(fd, key, iv)
            cmt = f.read(item.file_size)
        else:
            # archive comment
            with self._open_clear(item) as cmtstream:
                cmt = cmtstream.read()

        # rar bug? - appends zero to comment
        cmt = cmt.split(ZERO, 1)[0]
        self.comment = cmt.decode('utf8')

    def _open_hack(self, inf, psw):
        # len, type, blk_flags, flags
        main_hdr = b'\x03\x01\x00\x00'
        endarc_hdr = b'\x03\x05\x00\x00'
        main_hdr = S_LONG.pack(rar_crc32(main_hdr)) + main_hdr
        endarc_hdr = S_LONG.pack(rar_crc32(endarc_hdr)) + endarc_hdr
        return self._open_hack_core(inf, psw, RAR5_ID + main_hdr, endarc_hdr)

##
## Utility classes
##

class UnicodeFilename(object):
    """Handle RAR3 unicode filename decompression.
    """
    def __init__(self, name, encdata):
        self.std_name = bytearray(name)
        self.encdata = bytearray(encdata)
        self.pos = self.encpos = 0
        self.buf = bytearray()
        self.failed = 0

    def enc_byte(self):
        """Copy encoded byte."""
        try:
            c = self.encdata[self.encpos]
            self.encpos += 1
            return c
        except IndexError:
            self.failed = 1
            return 0

    def std_byte(self):
        """Copy byte from 8-bit representation."""
        try:
            return self.std_name[self.pos]
        except IndexError:
            self.failed = 1
            return ord('?')

    def put(self, lo, hi):
        """Copy 16-bit value to result."""
        self.buf.append(lo)
        self.buf.append(hi)
        self.pos += 1

    def decode(self):
        """Decompress compressed UTF16 value."""
        hi = self.enc_byte()
        flagbits = 0
        while self.encpos < len(self.encdata):
            if flagbits == 0:
                flags = self.enc_byte()
                flagbits = 8
            flagbits -= 2
            t = (flags >> flagbits) & 3
            if t == 0:
                self.put(self.enc_byte(), 0)
            elif t == 1:
                self.put(self.enc_byte(), hi)
            elif t == 2:
                self.put(self.enc_byte(), self.enc_byte())
            else:
                n = self.enc_byte()
                if n & 0x80:
                    c = self.enc_byte()
                    for _ in range((n & 0x7f) + 2):
                        lo = (self.std_byte() + c) & 0xFF
                        self.put(lo, hi)
                else:
                    for _ in range(n + 2):
                        self.put(self.std_byte(), 0)
        return self.buf.decode("utf-16le", "replace")


class RarExtFile(RawIOBase):
    """Base class for file-like object that :meth:`RarFile.open` returns.

    Provides public methods and common crc checking.

    Behaviour:
     - no short reads - .read() and .readinfo() read as much as requested.
     - no internal buffer, use io.BufferedReader for that.
    """

    #: Filename of the archive entry
    name = None

    def __init__(self, parser, inf):
        """Open archive entry.
        """
        super(RarExtFile, self).__init__()

        # standard io.* properties
        self.name = inf.filename
        self.mode = 'rb'

        self._parser = parser
        self._inf = inf
        self._fd = None
        self._remain = 0
        self._returncode = 0

        self._md_context = None

        self._open()

    def _open(self):
        if self._fd:
            self._fd.close()
        md_class = self._inf._md_class or NoHashContext
        self._md_context = md_class()
        self._fd = None
        self._remain = self._inf.file_size

    def read(self, cnt=None):
        """Read all or specified amount of data from archive entry."""

        # sanitize cnt
        if cnt is None or cnt < 0:
            cnt = self._remain
        elif cnt > self._remain:
            cnt = self._remain
        if cnt == 0:
            return EMPTY

        # actual read
        data = self._read(cnt)
        if data:
            self._md_context.update(data)
            self._remain -= len(data)
        if len(data) != cnt:
            raise BadRarFile("Failed the read enough data")

        # done?
        if not data or self._remain == 0:
            # self.close()
            self._check()
        return data

    def _check(self):
        """Check final CRC."""
        final = self._md_context.digest()
        exp = self._inf._md_expect
        if exp is None:
            return
        if final is None:
            return
        if self._returncode:
            check_returncode(self, '')
        if self._remain != 0:
            raise BadRarFile("Failed the read enough data")
        if final != exp:
            raise BadRarFile("Corrupt file - CRC check failed: %s - exp=%r got=%r" % (
                self._inf.filename, exp, final))

    def _read(self, cnt):
        """Actual read that gets sanitized cnt."""

    def close(self):
        """Close open resources."""

        super(RarExtFile, self).close()

        if self._fd:
            self._fd.close()
            self._fd = None

    def __del__(self):
        """Hook delete to make sure tempfile is removed."""
        self.close()

    def readinto(self, buf):
        """Zero-copy read directly into buffer.

        Returns bytes read.
        """
        raise NotImplementedError('readinto')

    def tell(self):
        """Return current reading position in uncompressed data."""
        return self._inf.file_size - self._remain

    def seek(self, ofs, whence=0):
        """Seek in data.

        On uncompressed files, the seeking works by actual
        seeks so it's fast.  On compresses files its slow
        - forward seeking happends by reading ahead,
        backwards by re-opening and decompressing from the start.
        """

        # disable crc check when seeking
        self._md_context = NoHashContext()

        fsize = self._inf.file_size
        cur_ofs = self.tell()

        if whence == 0:     # seek from beginning of file
            new_ofs = ofs
        elif whence == 1:   # seek from current position
            new_ofs = cur_ofs + ofs
        elif whence == 2:   # seek from end of file
            new_ofs = fsize + ofs
        else:
            raise ValueError('Invalid value for whence')

        # sanity check
        if new_ofs < 0:
            new_ofs = 0
        elif new_ofs > fsize:
            new_ofs = fsize

        # do the actual seek
        if new_ofs >= cur_ofs:
            self._skip(new_ofs - cur_ofs)
        else:
            # reopen and seek
            self._open()
            self._skip(new_ofs)
        return self.tell()

    def _skip(self, cnt):
        """Read and discard data"""
        while cnt > 0:
            if cnt > 8192:
                buf = self.read(8192)
            else:
                buf = self.read(cnt)
            if not buf:
                break
            cnt -= len(buf)

    def readable(self):
        """Returns True"""
        return True

    def writable(self):
        """Returns False.

        Writing is not supported.
        """
        return False

    def seekable(self):
        """Returns True.

        Seeking is supported, although it's slow on compressed files.
        """
        return True

    def readall(self):
        """Read all remaining data"""
        # avoid RawIOBase default impl
        return self.read()


class PipeReader(RarExtFile):
    """Read data from pipe, handle tempfile cleanup."""

    def __init__(self, rf, inf, cmd, tempfile=None):
        self._cmd = cmd
        self._proc = None
        self._tempfile = tempfile
        super(PipeReader, self).__init__(rf, inf)

    def _close_proc(self):
        if not self._proc:
            return
        if self._proc.stdout:
            self._proc.stdout.close()
        if self._proc.stdin:
            self._proc.stdin.close()
        if self._proc.stderr:
            self._proc.stderr.close()
        self._proc.wait()
        self._returncode = self._proc.returncode
        self._proc = None

    def _open(self):
        super(PipeReader, self)._open()

        # stop old process
        self._close_proc()

        # launch new process
        self._returncode = 0
        self._proc = custom_popen(self._cmd)
        self._fd = self._proc.stdout

        # avoid situation where unrar waits on stdin
        if self._proc.stdin:
            self._proc.stdin.close()

    def _read(self, cnt):
        """Read from pipe."""

        # normal read is usually enough
        data = self._fd.read(cnt)
        if len(data) == cnt or not data:
            return data

        # short read, try looping
        buf = [data]
        cnt -= len(data)
        while cnt > 0:
            data = self._fd.read(cnt)
            if not data:
                break
            cnt -= len(data)
            buf.append(data)
        return EMPTY.join(buf)

    def close(self):
        """Close open resources."""

        self._close_proc()
        super(PipeReader, self).close()

        if self._tempfile:
            try:
                os.unlink(self._tempfile)
            except OSError:
                pass
            self._tempfile = None

    def readinto(self, buf):
        """Zero-copy read directly into buffer."""
        cnt = len(buf)
        if cnt > self._remain:
            cnt = self._remain
        vbuf = memoryview(buf)
        res = got = 0
        while got < cnt:
            res = self._fd.readinto(vbuf[got : cnt])
            if not res:
                break
            self._md_context.update(vbuf[got : got + res])
            self._remain -= res
            got += res
        return got


class DirectReader(RarExtFile):
    """Read uncompressed data directly from archive.
    """
    _cur = None
    _cur_avail = None
    _volfile = None

    def _open(self):
        super(DirectReader, self)._open()

        self._volfile = self._inf.volume_file
        self._fd = XFile(self._volfile, 0)
        self._fd.seek(self._inf.header_offset, 0)
        self._cur = self._parser._parse_header(self._fd)
        self._cur_avail = self._cur.add_size

    def _skip(self, cnt):
        """RAR Seek, skipping through rar files to get to correct position
        """

        while cnt > 0:
            # next vol needed?
            if self._cur_avail == 0:
                if not self._open_next():
                    break

            # fd is in read pos, do the read
            if cnt > self._cur_avail:
                cnt -= self._cur_avail
                self._remain -= self._cur_avail
                self._cur_avail = 0
            else:
                self._fd.seek(cnt, 1)
                self._cur_avail -= cnt
                self._remain -= cnt
                cnt = 0

    def _read(self, cnt):
        """Read from potentially multi-volume archive."""

        buf = []
        while cnt > 0:
            # next vol needed?
            if self._cur_avail == 0:
                if not self._open_next():
                    break

            # fd is in read pos, do the read
            if cnt > self._cur_avail:
                data = self._fd.read(self._cur_avail)
            else:
                data = self._fd.read(cnt)
            if not data:
                break

            # got some data
            cnt -= len(data)
            self._cur_avail -= len(data)
            buf.append(data)

        if len(buf) == 1:
            return buf[0]
        return EMPTY.join(buf)

    def _open_next(self):
        """Proceed to next volume."""

        # is the file split over archives?
        if (self._cur.flags & RAR_FILE_SPLIT_AFTER) == 0:
            return False

        if self._fd:
            self._fd.close()
            self._fd = None

        # open next part
        self._volfile = self._parser._next_volname(self._volfile)
        fd = open(self._volfile, "rb", 0)
        self._fd = fd
        sig = fd.read(len(self._parser._expect_sig))
        if sig != self._parser._expect_sig:
            raise BadRarFile("Invalid signature")

        # loop until first file header
        while 1:
            cur = self._parser._parse_header(fd)
            if not cur:
                raise BadRarFile("Unexpected EOF")
            if cur.type in (RAR_BLOCK_MARK, RAR_BLOCK_MAIN):
                if cur.add_size:
                    fd.seek(cur.add_size, 1)
                continue
            if cur.orig_filename != self._inf.orig_filename:
                raise BadRarFile("Did not found file entry")
            self._cur = cur
            self._cur_avail = cur.add_size
            return True

    def readinto(self, buf):
        """Zero-copy read directly into buffer."""
        got = 0
        vbuf = memoryview(buf)
        while got < len(buf):
            # next vol needed?
            if self._cur_avail == 0:
                if not self._open_next():
                    break

            # length for next read
            cnt = len(buf) - got
            if cnt > self._cur_avail:
                cnt = self._cur_avail

            # read into temp view
            res = self._fd.readinto(vbuf[got : got + cnt])
            if not res:
                break
            self._md_context.update(vbuf[got : got + res])
            self._cur_avail -= res
            self._remain -= res
            got += res
        return got


class HeaderDecrypt(object):
    """File-like object that decrypts from another file"""
    def __init__(self, f, key, iv):
        self.f = f
        self.ciph = AES_CBC_Decrypt(key, iv)
        self.buf = EMPTY

    def tell(self):
        """Current file pos - works only on block boundaries."""
        return self.f.tell()

    def read(self, cnt=None):
        """Read and decrypt."""
        if cnt > 8 * 1024:
            raise BadRarFile('Bad count to header decrypt - wrong password?')

        # consume old data
        if cnt <= len(self.buf):
            res = self.buf[:cnt]
            self.buf = self.buf[cnt:]
            return res
        res = self.buf
        self.buf = EMPTY
        cnt -= len(res)

        # decrypt new data
        blklen = 16
        while cnt > 0:
            enc = self.f.read(blklen)
            if len(enc) < blklen:
                break
            dec = self.ciph.decrypt(enc)
            if cnt >= len(dec):
                res += dec
                cnt -= len(dec)
            else:
                res += dec[:cnt]
                self.buf = dec[cnt:]
                cnt = 0

        return res


# handle (filename|filelike) object
class XFile(object):
    """Input may be filename or file object.
    """
    __slots__ = ('_fd', '_need_close')

    def __init__(self, xfile, bufsize=1024):
        if is_filelike(xfile):
            self._need_close = False
            self._fd = xfile
            self._fd.seek(0)
        else:
            self._need_close = True
            self._fd = open(xfile, 'rb', bufsize)

    def read(self, n=None):
        """Read from file."""
        return self._fd.read(n)

    def tell(self):
        """Return file pos."""
        return self._fd.tell()

    def seek(self, ofs, whence=0):
        """Move file pos."""
        return self._fd.seek(ofs, whence)

    def readinto(self, dst):
        """Read into buffer."""
        return self._fd.readinto(dst)

    def close(self):
        """Close file object."""
        if self._need_close:
            self._fd.close()

    def __enter__(self):
        return self

    def __exit__(self, typ, val, tb):
        self.close()


class NoHashContext(object):
    """No-op hash function."""
    def __init__(self, data=None):
        """Initialize"""
    def update(self, data):
        """Update data"""
    def digest(self):
        """Final hash"""
    def hexdigest(self):
        """Hexadecimal digest."""


class CRC32Context(object):
    """Hash context that uses CRC32."""
    __slots__ = ['_crc']

    def __init__(self, data=None):
        self._crc = 0
        if data:
            self.update(data)

    def update(self, data):
        """Process data."""
        self._crc = rar_crc32(data, self._crc)

    def digest(self):
        """Final hash."""
        return self._crc

    def hexdigest(self):
        """Hexadecimal digest."""
        return '%08x' % self.digest()


class Blake2SP(object):
    """Blake2sp hash context.
    """
    __slots__ = ['_thread', '_buf', '_cur', '_digest']
    digest_size = 32
    block_size = 64
    parallelism = 8

    def __init__(self, data=None):
        self._buf = b''
        self._cur = 0
        self._digest = None
        self._thread = []

        for i in range(self.parallelism):
            ctx = self._blake2s(i, 0, i == (self.parallelism - 1))
            self._thread.append(ctx)

        if data:
            self.update(data)

    def _blake2s(self, ofs, depth, is_last):
        return blake2s(node_offset=ofs, node_depth=depth, last_node=is_last,
                       depth=2, inner_size=32, fanout=self.parallelism)

    def _add_block(self, blk):
        self._thread[self._cur].update(blk)
        self._cur = (self._cur + 1) % self.parallelism

    def update(self, data):
        """Hash data.
        """
        view = memoryview(data)
        bs = self.block_size
        if self._buf:
            need = bs - len(self._buf)
            if len(view) < need:
                self._buf += view.tobytes()
                return
            self._add_block(self._buf + view[:need].tobytes())
            view = view[need:]
        while len(view) >= bs:
            self._add_block(view[:bs])
            view = view[bs:]
        self._buf = view.tobytes()

    def digest(self):
        """Return final digest value.
        """
        if self._digest is None:
            if self._buf:
                self._add_block(self._buf)
                self._buf = EMPTY
            ctx = self._blake2s(0, 1, True)
            for t in self._thread:
                ctx.update(t.digest())
            self._digest = ctx.digest()
        return self._digest

    def hexdigest(self):
        """Hexadecimal digest."""
        return tohex(self.digest())

##
## Utility functions
##

S_LONG = Struct('<L')
S_SHORT = Struct('<H')
S_BYTE = Struct('<B')

S_BLK_HDR = Struct('<HBHH')
S_FILE_HDR = Struct('<LLBLLBBHL')
S_COMMENT_HDR = Struct('<HBBH')

def load_vint(buf, pos):
    """Load variable-size int."""
    limit = min(pos + 11, len(buf))
    res = ofs = 0
    while pos < limit:
        b = _byte_code(buf[pos])
        res += ((b & 0x7F) << ofs)
        pos += 1
        ofs += 7
        if b < 0x80:
            return res, pos
    raise BadRarFile('cannot load vint')

def load_byte(buf, pos):
    """Load single byte"""
    end = pos + 1
    if end > len(buf):
        raise BadRarFile('cannot load byte')
    return S_BYTE.unpack_from(buf, pos)[0], end

def load_le32(buf, pos):
    """Load little-endian 32-bit integer"""
    end = pos + 4
    if end > len(buf):
        raise BadRarFile('cannot load le32')
    return S_LONG.unpack_from(buf, pos)[0], pos + 4

def load_bytes(buf, num, pos):
    """Load sequence of bytes"""
    end = pos + num
    if end > len(buf):
        raise BadRarFile('cannot load bytes')
    return buf[pos : end], end

def load_vstr(buf, pos):
    """Load bytes prefixed by vint length"""
    slen, pos = load_vint(buf, pos)
    return load_bytes(buf, slen, pos)

def load_dostime(buf, pos):
    """Load LE32 dos timestamp"""
    stamp, pos = load_le32(buf, pos)
    tup = parse_dos_time(stamp)
    return to_datetime(tup), pos

def load_unixtime(buf, pos):
    """Load LE32 unix timestamp"""
    secs, pos = load_le32(buf, pos)
    dt = datetime.fromtimestamp(secs, UTC)
    return dt, pos

def load_windowstime(buf, pos):
    """Load LE64 windows timestamp"""
    # unix epoch (1970) in seconds from windows epoch (1601)
    unix_epoch = 11644473600
    val1, pos = load_le32(buf, pos)
    val2, pos = load_le32(buf, pos)
    secs, n1secs = divmod((val2 << 32) | val1, 10000000)
    dt = datetime.fromtimestamp(secs - unix_epoch, UTC)
    dt = dt.replace(microsecond=n1secs // 10)
    return dt, pos

# new-style next volume
def _next_newvol(volfile):
    i = len(volfile) - 1
    while i >= 0:
        if volfile[i] >= '0' and volfile[i] <= '9':
            return _inc_volname(volfile, i)
        i -= 1
    raise BadRarName("Cannot construct volume name: " + volfile)

# old-style next volume
def _next_oldvol(volfile):
    # rar -> r00
    if volfile[-4:].lower() == '.rar':
        return volfile[:-2] + '00'
    return _inc_volname(volfile, len(volfile) - 1)

# increase digits with carry, otherwise just increment char
def _inc_volname(volfile, i):
    fn = list(volfile)
    while i >= 0:
        if fn[i] != '9':
            fn[i] = chr(ord(fn[i]) + 1)
            break
        fn[i] = '0'
        i -= 1
    return ''.join(fn)

# rar3 extended time fields
def _parse_ext_time(h, data, pos):
    # flags and rest of data can be missing
    flags = 0
    if pos + 2 <= len(data):
        flags = S_SHORT.unpack_from(data, pos)[0]
        pos += 2

    mtime, pos = _parse_xtime(flags >> 3 * 4, data, pos, h.mtime)
    h.ctime, pos = _parse_xtime(flags >> 2 * 4, data, pos)
    h.atime, pos = _parse_xtime(flags >> 1 * 4, data, pos)
    h.arctime, pos = _parse_xtime(flags >> 0 * 4, data, pos)
    if mtime:
        h.mtime = mtime
        h.date_time = mtime.timetuple()[:6]
    return pos

# rar3 one extended time field
def _parse_xtime(flag, data, pos, basetime=None):
    res = None
    if flag & 8:
        if not basetime:
            basetime, pos = load_dostime(data, pos)

        # load second fractions
        rem = 0
        cnt = flag & 3
        for _ in range(cnt):
            b, pos = load_byte(data, pos)
            rem = (b << 16) | (rem >> 8)

        # convert 100ns units to microseconds
        usec = rem // 10
        if usec > 1000000:
            usec = 999999

        # dostime has room for 30 seconds only, correct if needed
        if flag & 4 and basetime.second < 59:
            res = basetime.replace(microsecond=usec, second=basetime.second + 1)
        else:
            res = basetime.replace(microsecond=usec)
    return res, pos

def is_filelike(obj):
    """Filename or file object?
    """
    if isinstance(obj, str) or isinstance(obj, unicode):
        return False
    res = True
    for a in ('read', 'tell', 'seek'):
        res = res and hasattr(obj, a)
    if not res:
        raise ValueError("Invalid object passed as file")
    return True

def rar3_s2k(psw, salt):
    """String-to-key hash for RAR3.
    """
    if not isinstance(psw, unicode):
        psw = psw.decode('utf8')
    seed = psw.encode('utf-16le') + salt
    iv = EMPTY
    h = sha1()
    for i in range(16):
        for j in range(0x4000):
            cnt = S_LONG.pack(i * 0x4000 + j)
            h.update(seed + cnt[:3])
            if j == 0:
                iv += h.digest()[19:20]
    key_be = h.digest()[:16]
    key_le = pack("<LLLL", *unpack(">LLLL", key_be))
    return key_le, iv

def rar3_decompress(vers, meth, data, declen=0, flags=0, crc=0, psw=None, salt=None):
    """Decompress blob of compressed data.

    Used for data with non-standard header - eg. comments.
    """
    # already uncompressed?
    if meth == RAR_M0 and (flags & RAR_FILE_PASSWORD) == 0:
        return data

    # take only necessary flags
    flags = flags & (RAR_FILE_PASSWORD | RAR_FILE_SALT | RAR_FILE_DICTMASK)
    flags |= RAR_LONG_BLOCK

    # file header
    fname = b'data'
    date = 0
    mode = 0x20
    fhdr = S_FILE_HDR.pack(len(data), declen, RAR_OS_MSDOS, crc,
                           date, vers, meth, len(fname), mode)
    fhdr += fname
    if flags & RAR_FILE_SALT:
        if not salt:
            return EMPTY
        fhdr += salt

    # full header
    hlen = S_BLK_HDR.size + len(fhdr)
    hdr = S_BLK_HDR.pack(0, RAR_BLOCK_FILE, flags, hlen) + fhdr
    hcrc = rar_crc32(hdr[2:]) & 0xFFFF
    hdr = S_BLK_HDR.pack(hcrc, RAR_BLOCK_FILE, flags, hlen) + fhdr

    # archive main header
    mh = S_BLK_HDR.pack(0x90CF, RAR_BLOCK_MAIN, 0, 13) + ZERO * (2 + 4)

    # decompress via temp rar
    tmpfd, tmpname = mkstemp(suffix='.rar')
    tmpf = os.fdopen(tmpfd, "wb")
    try:
        tmpf.write(RAR_ID + mh + hdr + data)
        tmpf.close()

        cmd = [UNRAR_TOOL] + list(OPEN_ARGS)
        add_password_arg(cmd, psw, (flags & RAR_FILE_PASSWORD))
        cmd.append(tmpname)

        p = custom_popen(cmd)
        return p.communicate()[0]
    finally:
        tmpf.close()
        os.unlink(tmpname)

def to_datetime(t):
    """Convert 6-part time tuple into datetime object.
    """
    if t is None:
        return None

    # extract values
    year, mon, day, h, m, s = t

    # assume the values are valid
    try:
        return datetime(year, mon, day, h, m, s)
    except ValueError:
        pass

    # sanitize invalid values
    mday = (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if mon < 1:
        mon = 1
    if mon > 12:
        mon = 12
    if day < 1:
        day = 1
    if day > mday[mon]:
        day = mday[mon]
    if h > 23:
        h = 23
    if m > 59:
        m = 59
    if s > 59:
        s = 59
    if mon == 2 and day == 29:
        try:
            return datetime(year, mon, day, h, m, s)
        except ValueError:
            day = 28
    return datetime(year, mon, day, h, m, s)

def parse_dos_time(stamp):
    """Parse standard 32-bit DOS timestamp.
    """
    sec, stamp = stamp & 0x1F, stamp >> 5
    mn,  stamp = stamp & 0x3F, stamp >> 6
    hr,  stamp = stamp & 0x1F, stamp >> 5
    day, stamp = stamp & 0x1F, stamp >> 5
    mon, stamp = stamp & 0x0F, stamp >> 4
    yr = (stamp & 0x7F) + 1980
    return (yr, mon, day, hr, mn, sec * 2)

def custom_popen(cmd):
    """Disconnect cmd from parent fds, read only from stdout.
    """
    # needed for py2exe
    creationflags = 0
    if sys.platform == 'win32':
        creationflags = 0x08000000   # CREATE_NO_WINDOW

    # run command
    try:
        p = Popen(cmd, bufsize=0, stdout=PIPE, stdin=PIPE, stderr=STDOUT,
                  creationflags=creationflags)
    except OSError as ex:
        if ex.errno == errno.ENOENT:
            raise RarCannotExec("Unrar not installed? (rarfile.UNRAR_TOOL=%r)" % UNRAR_TOOL)
        raise
    return p

def custom_check(cmd, ignore_retcode=False):
    """Run command, collect output, raise error if needed.
    """
    p = custom_popen(cmd)
    out, _ = p.communicate()
    if p.returncode and not ignore_retcode:
        raise RarExecError("Check-run failed")
    return out

def add_password_arg(cmd, psw, ___required=False):
    """Append password switch to commandline.
    """
    if UNRAR_TOOL == ALT_TOOL:
        return
    if psw is not None:
        cmd.append('-p' + psw)
    else:
        cmd.append('-p-')

def check_returncode(p, out):
    """Raise exception according to unrar exit code.
    """
    code = p.returncode
    if code == 0:
        return

    # map return code to exception class, codes from rar.txt
    errmap = [None,
              RarWarning, RarFatalError, RarCRCError, RarLockedArchiveError,    # 1..4
              RarWriteError, RarOpenError, RarUserError, RarMemoryError,        # 5..8
              RarCreateError, RarNoFilesError, RarWrongPassword]                # 9..11
    if UNRAR_TOOL == ALT_TOOL:
        errmap = [None]
    if code > 0 and code < len(errmap):
        exc = errmap[code]
    elif code == 255:
        exc = RarUserBreak
    elif code < 0:
        exc = RarSignalExit
    else:
        exc = RarUnknownError

    # format message
    if out:
        msg = "%s [%d]: %s" % (exc.__doc__, p.returncode, out)
    else:
        msg = "%s [%d]" % (exc.__doc__, p.returncode)

    raise exc(msg)

def hmac_sha256(key, data):
    """HMAC-SHA256"""
    return HMAC(key, data, sha256).digest()

def membuf_tempfile(memfile):
    """Write in-memory file object to real file."""
    memfile.seek(0, 0)

    tmpfd, tmpname = mkstemp(suffix='.rar')
    tmpf = os.fdopen(tmpfd, "wb")

    try:
        while True:
            buf = memfile.read(BSIZE)
            if not buf:
                break
            tmpf.write(buf)
        tmpf.close()
    except:
        tmpf.close()
        os.unlink(tmpname)
        raise
    return tmpname

class XTempFile(object):
    """Real file for archive.
    """
    __slots__ = ('_tmpfile', '_filename')

    def __init__(self, rarfile):
        if is_filelike(rarfile):
            self._tmpfile = membuf_tempfile(rarfile)
            self._filename = self._tmpfile
        else:
            self._tmpfile = None
            self._filename = rarfile

    def __enter__(self):
        return self._filename

    def __exit__(self, exc_type, exc_value, tb):
        if self._tmpfile:
            try:
                os.unlink(self._tmpfile)
            except OSError:
                pass
            self._tmpfile = None

#
# Check if unrar works
#

ORIG_UNRAR_TOOL = UNRAR_TOOL
ORIG_OPEN_ARGS = OPEN_ARGS
ORIG_EXTRACT_ARGS = EXTRACT_ARGS
ORIG_TEST_ARGS = TEST_ARGS

def _check_unrar_tool():
    global UNRAR_TOOL, OPEN_ARGS, EXTRACT_ARGS, TEST_ARGS
    try:
        # does UNRAR_TOOL work?
        custom_check([ORIG_UNRAR_TOOL], True)

        UNRAR_TOOL = ORIG_UNRAR_TOOL
        OPEN_ARGS = ORIG_OPEN_ARGS
        EXTRACT_ARGS = ORIG_EXTRACT_ARGS
        TEST_ARGS = ORIG_TEST_ARGS
    except RarCannotExec:
        try:
            # does ALT_TOOL work?
            custom_check([ALT_TOOL] + list(ALT_CHECK_ARGS), True)
            # replace config
            UNRAR_TOOL = ALT_TOOL
            OPEN_ARGS = ALT_OPEN_ARGS
            EXTRACT_ARGS = ALT_EXTRACT_ARGS
            TEST_ARGS = ALT_TEST_ARGS
        except RarCannotExec:
            # no usable tool, only uncompressed archives work
            pass

_check_unrar_tool()

if __name__ == '__main__':
    filename = '../aaa.rar'
    pazzlist = ['asdf1','asdf2','asdf3']

    def get_parsefunc(filename):
        f = RarFile(filename)
        def func(pwd):
            try:
                v = f.extractall(path=os.path.dirname(filename), pwd= pwd)
                return pwd,True
            except:
                return pwd,False
        return func

    pfunc = get_parsefunc(filename)
    for i in [''] + pazzlist:
        a,b = pfunc(i)
        if b:
            if i == '':
                print('空密码.')
            else:
                print(a)
            break
