
def get_classname(n):
    S = [
        'header.navbar.navbar-default.yq-header',
        'ul.nav.navbar-toolbar.navbar-right.navbar-toolbar-right.yq-navbar-toolbar',
        'li.yq-dropdown-menu-media-apps',
        'a.yq-navbar-menuIcon-24.yq-head-apps',
        'div.dropdown-menu.yq-moreapp-container',
        'ul.list-group.yq-list-group-moreapp.clearfix',
        'li.hide.yq-dropdown-menu-media-msg',
        'a.yq-head-msg.yq-navbar-menuIcon-24',
        'div.yq-msg-nomsg.vertical-align.panel.text-center.hide',
        'div.yq-msg-network-err.vertical-align.panel.text-center.hide',
        'div.dropdown-menu.dropdown-menu-media.yq-dropdown-menu-media-user',
        'div.dropdown-menu-footer.yq-user-footer.clearfix',
        'li#jcHeaderInput.margin-horizontal-10.yq-input-container',
        'ul.dropdown-menu.dropdown-menu-media.yq-track-dropdown',
        'div.yq-more-track-container.clearfix',
        'div.yq-tools-small',
        'img.navbar-brand-logo.hidden-xs.yq-default-logo',
        'img.navbar-brand-logo.visible-xs.yq-default-logo',
        'div.tab-content.yq-panel-tracklist.scrollable.is-enabled.scrollable-vertical',
        'div.yq-panel-gad',
        'div.modal-dialog.yq-modal-dialog',
    ]
    return ' '.join(S[n].split('.')[1:])
def I(p, S):
    def limit(R):
        v = R % 4294967296
        R = -(4294967296 - v) if v >= 2147483648 else v
        return R
    def unlimit(R):
        return 2147483648 + R if R < 0 else R
    R = 1293373362 + 22050549 ^ (S << 16)
    for i in list(range(len(p)))[::-1]:
        A = p[i] if isinstance(p[i], int) else ord(p[i])
        R ^= limit((limit(R << 5) + A) + (R >> 2))
    R = unlimit(R)
    return R

import time
import random
def make_cookieid(data):
    t = [None]*6
    rd = random.randint(0,20)
    t[1] = hex(rd)[2:]
    t[2] = len(hex(rd)[2:])
    t[3] = 2
    RR = I(data, len(data))
    t[5] = '{:>08s}'.format(hex(RR)[2:])
    fingerprint = (
        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAACWCAYAAABkW7XSAAAd0UlEQVR4Xu2ceVxVdfrHPxdkF0QFUUoQBRfEJRIxzZTFNLMUdXKp0dQErNeozZQ2VtNvXNrNdKZkcZksTUvRFixzLzUJMw3UAhUXNrmoLAKX9f5e33PvuRyumEvi9J3X5/'
        '6Th3PP+T7n/Tzfz3me5/u96cAPCZAACUhCQCeJnTTzNhIwRsN4G28nza10CWC8S+Otxg2lAyV34K2YT8G6FWq85o9AgIL1R/DCHbaBgnWHgXO420aAgnXbUMpzIwqWPL6ipQ0J1AvWU4lesKnbA6NuNhKjt10FynQ+CTrj04iPPQrr49tN9s9rXOBoSIRN3RvKeNbH1x'
        'ovJq4XjLoN0BnHodz5JBwNnwBYpjyT9py4581+ouNnwqgbCoPjY/hwUtnNXt7k35+esBzAFhgc9ynPrTMOB/ALYJMCo7ECidEzhA1/ZME6irsxDtHYgAT0QvZvIrsAN4xGLN7HOuW717v2qh7W9IShAEYpXIRvgaXmAZfDqPP9w/pZS+V681b7XdMcqp8PN3Ot+l2gq3'
        'JLoy5Ojacmj2vNAH9cwRLiUmczFwbH6Yo4WB/fCCVrB/0vC5YIKJ1xFYy6qbCtbQuj7n3U2YzGiukXrFH9kQXrRtyqfsdasK53bSOC1VDg1Rfb9W4k63nr+XCjz1EvVsuRELPMnDyIF+I25fgOfq4SrDYeZw/36Ll9YlZWME5nBf+COpvBij0i+wK6urkWYujQ9/d+f3'
        'CsX3Z2oI84Hj586fb0Y+En0tPC7ZXv6oyxZhUeZsnWTGKxA4CH+flmWR62sczF9MbDtFkxH9lW4JUDB8YjPT3slDiu0Lf+1969kx/OyenSwpRB4HMYdUHKG9G53F9kWAMf+Phdt+YFLx/+abj3pcveGDbsvf01VQ5bkrfOeqpjx8PZfn6HI44fH4S83M5bLW9Sazus30'
        'Amm8aF9PnM29HpSocfUkehsqJ5/TNaO+633kpq8JiyoIZvLBOr92HUJUJnXG05b1MXp2Fo8o0qSGq2AGwJ7bfxa32BH3LyuijPbaurubum2r7aq23m7tzcbh3dtg6IKIYTtiJIufVSbMBM7FL+XQYHPIZoy7mF+Awfop8l47E+Pxzp+AQJcEGlkuG8gWHKfT5GCGLxLb'
        'ohDyfQTvlbHB5Q/vs1lmEojin/noHHcTcu411EKMciW3oZI7Gk3b9wOrAInx0fi0F5xXgJI5XzXZGPPVis/Hsw/oZf0BYiBucGv4V7MuzwbN5flGtzA/U4dHwI4vLGWq77pc67rYWXKvB1NnM7d9v/dcuWOXelpIxBaN+kE76+P6PS4Ny6jde57eUGF4ekpJd8KspdRf'
        'zPMfuiPmbEH0Rmq8Y88CaARxtUKg2zt0LojJGWKkW8ZHTGdOXeRt1WGHULYFO3+Crfm7NjcyZ4lzKGwFGrmwBb4ysBfilvhEeuevDgwbGtj6YNOWI5b4qtYdqs28GxTIkLJ/srq9d/Mv859dojPw81pKSMnmIO43o7RWzpjO+KeJsRM92lDlhYVt6yY2lJK7/WnufWre'
        'pX/ax16DfV8VWC1bpldv7oqFf1VTUun33wwdsTAZxTUj9zCdg7aNurof2TxhYU+m/ZnPT8HPV4/4HxJenpYWJCm4RIFSij7gkYdUcalJvXS0U15V9MTGyLmmq78R+vX9SmvNxtQVTU2x0uFrZdfTTtwTeL3/jH65pxftAKlrYk9PTKWh0V9VpkzvnAk8lbZ83190/dHx'
        'G+oryg0H/D5qTnXwdgenPcmGAtjQhP3NIp4NCFr7Y/s+786Z6bIJ7RuoyuFyTTW0h7XOG00pyam9jWv/lMx/XsNjY4BgoVkap0uGIu+erfcOZycEZ0dGZJhfsbW7+c1XFw+Nr5bTxOjtqcNM++QN+hRFv6qKKxDd3xBKZiB5YoZZUQkHNopYiQ+Ajx+gEdlPP+0CvHQm'
        'xUgRPfF5/lWKsIViSexctItpxfhnDMwjiLKKrf+QirlPuI6/egsyJCXihpUNa1RYkiSh1R2MAeH1xSxlMzrNdd1+B0cD7aZHgqgiXKyb3oDPFsqpgqdhjH1wuNphycetBuycHvH3tAf9HnNREnR48MtU85OMZLE087YNSZfGGdbZjEaIbl5aGKlxAJERPWMaWZ/Ao4Ux'
        'tmj6W8qve9KZ7Fx1TGmWLDNN7LDURP28oxjT/Wcl5rnzlu1PlQctkrVQiWIq7iYxYlRdS1dppfijNS0VGIFXQ4FJ8QX+PsXDxi4uMvnrPVVR+P74N3mkqktPe9SrBUtTUC2cXFbYcbKlw823ie2XvqVN+3fzr64PJHHllywcmppLamxs7hp58e6hQUtOdXcVxU1NYvLS'
        '2isl/opk+b2RlaiUEKC30V4PZ2hgUqmJgZ0RXGWszS6WDKxoDd6sPGHMJfjTp0PpjypyU//zTkHVHexMROf7yszN31o4/e7CuOH3lk8fwCve/AlL2Ph8Q8O+leca/CQt97Kw0udl7tTq6prHL237Tp5d739fvkNf+Oh4bt3feEX++e2wpatsyvM1S6uKWlRXZt0SL/75'
        '0DUiKNgL5Q76u8uj3anP16wyfzzxRfajtw6pSZ3zVzMHRQ7DgSuaXBG+jgGC9x3s7e0EVcp9f7hon/enqcfS4+BBstcBt5K0EHV9M1PoakzS8GiSCf9uz0alsDXq00uHS7WOgT3Ny1cNP6DQuWiCwxLGzVm50DUgZWVjgduVzkPc/RqUzfokX+Vp0tvrxU6L2sttbO3d'
        'Pj7IGC851e3fzV3Hmi3xfzVGxAcanniCNHhvUb0H/9uWbNqiv1et8eBQUdcwIDd+/PyekWbNwaGfFMj+Uoda1Bqa09tjl3QHfkoVduNd5Om6lkOf6O2dgSAmQ6u+IntMfIghzktgIOH4/Ah3nJgGOlcv6CczMcgi/6lecjNLUFJhtilQynxE+voEh19UBukQ+eKP8ZFc'
        '41yt+2u4sEAYjOyEFilknwIkPXwrkK+NnDCT/AD1F5uSj2KsOHx/+MOVe+Q2lwJtqUADvbeECP5uhffQ6DUp0xAxMxIuQjONqVowSO2JoxEvMMu7An0AaZxwcotn4dWol8dyDNF1/CiFIb4KXlifEjxLgzpsd8WQ27eTu/mRrU775NFW5uhVdELF+67O3q43v8PwaDY6'
        'AaT8IXRuB8od53kri2lUfujnVrF/mUl7kvFuIUnYo3K6tcQvUFHfrZO5RtbOWe53Tg4GOBv/w6YJzIqER8AwgT/rC1rS6qqXN+RbwwRXyFPbiqH4woqKx0GXTufM+edg7l//BrfzQYQEpZWcsni4q8urdqdW7Nmg+X/Cr6qEqM2huca6ocggr0fkPqjLYftL/rWCslw/'
        'r5wdPR0dGl0MFgqHDrc+nSXQNbe5w7DKNtwqcbX5o84uF3qsV8UObwkYd6lV72mNsn9PPJPx5+JCDjl/73ijkn7BTPaDSiSmeLpfHB+DYmFSJdHZ2Zcd+7u/Y++YEQupjoaFejDSJrHTFvZXdcamrRurZg2aBETODqSsdwoaJVBrvKNR8u6f2bGVZauH1MTHSm+WF3Cx'
        'Xu4HtkQkREQkH6sciLJ44/MCUkZAsK9b7fHP3LxqEWxQaSrprswKhps6NfFOXg0SMPnU9JieokjgtOBySdODGoaEjYir9q1V4dx1DlWqUVrO07otuXVbgv1mRYTwkhCPBPeRjAqYSEBNc2nmfcoqJe1Z081cdp585o++sIVuW1nrGZbe2Hlucwv1kHD1sX07nDnpd0Rm'
        'QIYZ52DK0Kz3b6PD/Xv5VTy8oHxTnUoSQhPnGxU/Piz0ePXniutsaubP36hf1UO2tq7c6tWvle59DQzbt79frqPh1QmZz8bObl0rbtH584t+rSxbuubPz0FW/R74ueOemVnJzAguSts6KiRr/1pjbDEkGsFaws7xoEZjjh6awX8LzfCuj9C7EzfZQyyfeFlsBgD/inem'
        'MaJiM6ZBnOOzpjbfpkiBK7b8gWFBd54ee0SHjgCuaH/p8Sq0tTnlcE62yQHv75wPG0cKUkHNNjLX71Brrkmv62p507woO24NjJAUCWjyJYRS5A59S2mF76tKUkVAXrckgmHKuBgtSB2IWuGBuyCroqW8SnzIZ1hqWWk+LaCo9SeLlnY0HqWfRblqsTolFrtAtct26Ru8'
        'jYhcBX19oNEHzVzEPNsEQcVNY43qvGk3XMjBix2CktPeKe1B8fHRUzPTYCRvRRJ/PoqEXprm4X2+zfN+Gek6dCXHv22IEW7hegtBEMLggNTVrdvdse96QtL/b0bHlmoSjnRJKQsCJurWgHCN95tj45CTbQi0xen9dx5ZgxC44UXWrXMjn52UolRu0MIfqL/mtU0bOUhK'
        'pgAZ0yT4Ym7949dc7YsfO/bOmW75O0eZ6njV3Ne2I+qBmWEMzBYR8M3//9+E4GQ/NgP7/DOJfVY0rm31f9RxUpReRDcNqSYZqzQjXJ+K8LFoSIJMZ7q2putLHptn79/K5dOh6Yf82S0CxYIktSHmBpvCgHh06d9kxGM9vqalsgrqjUY2VKypjBp7PEy8NcPlrLsqa8qb'
        'XBnC2b5rkW6DusEeVOrr7Tmu/3jTsbFfXqZouya8aprHK5+0YES2RYsEFc/PKECcrb3jyZLcFw7QxLEaxrPWNCiLnPYRasyZOfW+foUPKwxeHKYKbVxgbn4hPLxCpsWNiqle3bnxi7a9eU7gEBB/8p7LxS1uo/az96fZY6oRTxS4ivgVHXTdiSnd1tePLW2Z+r/b7MzN'
        'Cju3dPnXY9wbrsXoMBqa54yPAcFrl+hKyQHOzMGoJ3CnciJfgK+mcA5XmmVbtX/Zbie38bnEofiOcdv8Dpu6sxKhVwMZicV+gKfBjsgg0Z4/AKvlB6SA8cB77KqxesC+5QrllpCFfKtT+Hvo896AJdyj2KYImPf4ppPK3oiAxLCNY9WcC+LNO1IkPMdbfBmtRYLLL7pE'
        'FJqPawxPiZHs2wzr0rNqZOFUJh6vuJRQnzgk7MrEkx1VWO9qtWLxt4PcGyjplJk2bXnTkTPDIrp9fEh4a8N1FXhx3x8YnfiTIvtO+WlV26fDfs4ME/dXN2KI4WcwY2WC0yFTXcJ33n/F76scixIsMRYqPMuRVxmapgtfE4OU6J0fi4YpFxPzx86Qonx9Lxu3c/WTpy5F'
        'vbGqsCGmRYAMwCqGTrouLQvsC1gqWOL2zLywt4bc/eJ/1LSj3q+1jiRH0rRylhr5lwNGGadc0M6xYFy9+s/K2UiWsSHmgneLMKPCkyMJF251/o6LT369ieDbYIaFa7YmKmD6wwOIetWfNuB6U8jJk+UF/oMy4p6SXnRsbxsX4jWjvI3MNSMqzfIVhKSSjK3ms9o5Iam0'
        'vCJx6fu965eVG7Bm+gxs4ti2svgrJ30La/BfXaFb1n7+Te1xQsMTFML5NuU6fMPHvmbK9Ju/ZMmSD6fcY6jPlqxzObzp/u+drNClZeyBkkZw3HXwwHUNBZj4cPAz+Wmnpca9q9jh8Dq/Dl8TGY67EOud5mpdIE55U6J2xOn3CVYKkCI0rCMSmmRrv4iKxro3sAdKm9Ed'
        'nr0yYRrJZXgM9CgGK7Zthh06X00kWf+Sk/jKoSg6kCX1bWKln7QrhWhmUdM1OnPWM4dSrk0dxzXReED1k1SBEkk7jsCPBLeX7goLWP7jswsW9L9/x3lcy4vg2iPKu2JLMSLEs7wMaIBcsTEgJEfylq9Fsv2OoqXz50aER1eNjqz5pCsGqcsUu0KIy1tj4FFzrcm1/gn5'
        'wybdtUS18VWCB6sqpYKVmh+pJuQqFSb317BSs9bOYjDy9JaOf9S7Gq7KL5/cTEF0bl5HWZnZ4ePl2/8LWNoskcGLzt2x49djq4u+dnaftY2u0LlvImeXawWu6UFHv9KvphEeGJv3TqdCjTPI5oiv7wewWrsNDHL2nzi4PHjp3/QavWOc2VntZlr9cC/FKmiIBSV1Esz5'
        'iQsBM640eiwSlKAkvWJQTL3EiPiEioEg16RbDeTVikgDc4Picaqfff/7F7YNDutIwzgxfu+XpivGiszoiOfqu03H3JjQrWE0/MyT+fHThp7+4p/c29B8Qnxu3UvKUtTXfrktA6wxJZzKGsgbhg8MTDnT/DkMO2mFEaozTdhWCdC7yIbcdHwcvjDO53P6xkS/sM3TEbjy'
        'lN83y4WbIjbYYlmu7/7vEK2jrnWzIo0RjX98huMsHS9rDECuYXjl2xpH+Loo4dDqfqCzr4nTg2cFH40FWnhcBnnB38luB/sxmWynP/gQkdoka+esjeyfC+krHrjLHamMnJ6Rrx4JC4H+0cKt+Nfz/xV8sClHkxSu2RajKsHeaFocsF5zot3vzV3DfEFoKY2JgjF/Xt32'
        'kKwdL2sJSme0xcrwH3bdjlH/BDuq1tTek338T2yM4OXPzfFCsxdW5YsISar133hr0taqZEDklM8WxzZo5wjpubPlYcZ2T0S0lPD+vT2JK/aEaaxcC0xiw+5o1nogbOL+g0evs3MeXlF9tGwalimjgtmqGiHNz6xbMXsnO7XlSPbevw5vIVca7+HQ991847wzX10KOZhg'
        'rXzTDq3EQAlVW4+2mapJH7D4zXZ57sOzM8bNVxG13darGt4VoZlhhX9LR69tweK/oNR9OGLiq57HlPQMeDn1oE6+AYx9DQTb3tHSq6abc1iGcU/SFRUlq2STyV6NW564Ef29+dfldq6iiUlHjWr1KZRbtdu4xg8zllI17MYTxQUe72wm+WhJoM65ER79hUVDbv69v9UI'
        'To9+lssMn8llf6IL/Vw2pMsAKz7PB64QSUBJ/Erxn98UzecWWLw0K/f+FX/woEp7vgOccRsPc7DWG3d2nNVSt82pJMlIQb0AcePVJx2b1W6eF8ZliprBBuCgW2I/CWS0Jh/77UP2GdXW/MCP43BmXUWLY1qOK6OU/sDRV7aa6gUOfSO/yBDxycnIs3u7pe/EcL9wtiWw'
        'zil66JFy+QWxEscf3a9W94BPdOnpKT3U1sBRLbGu4Xpb3oeemAjzdvnhel2Spk2mYgVhDNJVYjgrXBauuNKTZSMfbixfYv3GpJKDJE7Xxo4ap/R7utwbwlQpSm6hwdNm12dKrouWadCh4g+pXt2mUiKGgnLuT7i/5lw601dzTDMg/WWF2qbazZl8O9ToeX1Xpc+b4OLy'
        'vbGtLClZLQzt4wAEZ8IBrQYgKiDrGiFrepRbbSKDc32UUDWqSfakNa+7ziOvH2q3XCP0WJZX1svcTq758aHh62olY0KUU206wSQeq4NQ5IV8YRE93KJrWnIARHEawQzBGBYQQmWFZHzKs7lmeyPrb6vvY5GntGdaxaZ7wu7FKa7iGYo35XPdayE3Za7mV+DjGO4hsj2o'
        'r+oBB4RdBFc1ScM7GfopQVITitjhufiOd39ADUnpLoQ4kelCidRJ8oOAuKmKhN9+cxFpNC4lDjWIWIdMD7MpQVQscqKCWe+Bz2A37yA0amApebA98GwtLDUktC0eS/L8N0/8x29d8JyDONJz7q/bTn1bJOtU18T2t/hR2QHAxlW8PCvClY0u49pAWWKeOf9ah/zubLoN'
        'M2kWuBWB3wg7pQYs1XG/faeGo0ZkRM1Dfdl4wf/1JmCzd96wYxY0QftZepnWc2wGHLvDD1sJSS0NLk18SGOlesm93W81Ybz5pYUOahOh/MPaypykLafUmiTk8yx+5o1c5G56/Y1nCHtjFYa+BVvyW8nmAJ8RAwdDp0U0s5cSy2QJw508ume+DeNeqSv2WTqFm8FHBiaV'
        'SHyRYRN+KEWgM3CBBTrwvaLQ/KcXzCMXW/SMzT07tUVznMKbjgN8jVtfCQq1vhdzDCUREdjVAqS7JmkTEacUJsC1DFrLHgE+NonhFGHb4H4GMRPCESgC90cNAZYVqj1z6jeXuG2rfSiKuyrcGoQ456TiNoyn2EfRYeVs/wW4IlJp4R6KvtJ9ysYG0IscOGrNF4MSsd9z'
        'seU0TpO2fT44ltDQVuUPpaHqX1AmewM3lSrOAJsRLntGIjMixVsPStTNsarjiarlHFS/z79wiWEFxxfZq7K/bn9seiwn0WwVLFtcjZtK1BXaYXL09rgb9ZwRL7t0QPa+/eyUtFqaTOA7EVqLXn+VV2zaraahvt2pjSxkyDOacRLHXrjQ7oeFVsXCvGzMnAbwmWOh8MlS'
        '4jT2b2DSoraTlJFSwh3teyU51D1iJi2SpiflFedf42/uH2/fjZvPKlbglo0mXOhjuLLSm2mm3cySbgbfTFHbvVb/00R4jLMCg/MlA+Yre62KQpROhA53rBulFjxYZNVbBECaddWbzRe9zI90QjX+ykF7v2H2q3q1Fbm+T/h2X9Cw6xW93g+NiMmZO8tJXIjTyD8h3zz8'
        'catC00K4s3fJ/rfVHdfW/UxYm+6S3Zer0xmuD87RMss3F3al+G9f6Q/8YSaxP4447c8nq/JbQuDxvLgG7WUOsS9Gavv5nva8tTkfGpnyYRLLHa2Ehr4/fOA+sK4Wae/2a/eyfHulnbrL8vrWCJB7lW6vp7ofyvX389wRLPLyb9953rSbQtqu8v3QqfOyVYojQUu9rFBt'
        'XItIaWNpVgKYmR6LlqfsGhLftvhdedEhFtq0SGyuS2C9atOIfX3FkCNyJYd9aiOzNaUwrWnXkCjkLBYgyQAAlIQ4CCJY2raCgJkAAFizFAAiQgDQEKljSuoqEkQAIULMYACZCANAQoWNK4ioaSAAlQsBgDJEAC0hCgYEnjKhpKAiRAwWIMkAAJSEOAgiWNq2goCZAABY'
        'sxQAIkIA0BCpY0rqKhJEACFCzGAAmQgDQEKFjSuIqGkgAJULAYAyRAAtIQoGBJ4yoaSgIkQMFiDJAACUhDgIIljatoKAmQAAWLMUACJCANAQqWNK6ioSRAAhQsxgAJkIA0BChY0riKhpIACVCwGAMkQALSEKBgSeMqGkoCJEDBYgyQAAlIQ4CCJY2raCgJkAAFizFAAi'
        'QgDQEKljSuoqEkQAIULMYACZCANAQoWNK4ioaSAAlQsBgDJEAC0hCgYEnjKhpKAiRAwWIMkAAJSEOAgiWNq2goCZAABYsxQAIkIA0BCpY0rqKhJEACFCzGAAmQgDQEKFjSuIqGkgAJULAYAyRAAtIQoGBJ4yoaSgIkQMFiDJAACUhDgIIljatoKAmQAAWLMUACJCANAQ'
        'qWNK6ioSRAAhQsxgAJkIA0BChY0riKhpIACVCwGAMkQALSEKBgSeMqGkoCJEDBYgyQAAlIQ4CCJY2raCgJkAAFizFAAiQgDQEKljSuoqEkQAIULMYACZCANAQoWNK4ioaSAAlQsBgDJEAC0hCgYEnjKhpKAiRAwWIMkAAJSEOAgiWNq2goCZAABYsxQAIkIA0BCpY0rq'
        'KhJEACFCzGAAmQgDQEKFjSuIqGkgAJULAYAyRAAtIQoGBJ4yoaSgIkQMFiDJAACUhDgIIljatoKAmQAAWLMUACJCANAQqWNK6ioSRAAhQsxgAJkIA0BChY0riKhpIACVCwGAMkQALSEKBgSeMqGkoCJEDBYgyQAAlIQ4CCJY2raCgJkAAFizFAAiQgDQEKljSuoqEkQA'
        'IULMYACZCANAQoWNK4ioaSAAlQsBgDJEAC0hCgYEnjKhpKAiRAwWIMkAAJSEOAgiWNq2goCZAABYsxQAIkIA0BCpY0rqKhJEACFCzGAAmQgDQEKFjSuIqGkgAJULAYAyRAAtIQoGBJ4yoaSgIkQMFiDJAACUhDgIIljatoKAmQAAWLMUACJCANAQqWNK6ioSRAAhQsxg'
        'AJkIA0BChY0riKhpIACVCwGAMkQALSEKBgSeMqGkoCJEDBYgyQAAlIQ4CCJY2raCgJkAAFizFAAiQgDQEKljSuoqEkQAIULMYACZCANAQoWNK4ioaSAAlQsBgDJEAC0hCgYEnjKhpKAiRAwWIMkAAJSEOAgiWNq2goCZAABYsxQAIkIA0BCpY0rqKhJEACFCzGAAmQgD'
        'QEKFjSuIqGkgAJULAYAyRAAtIQoGBJ4yoaSgIkQMFiDJAACUhDgIIljatoKAmQAAWLMUACJCANAQqWNK6ioSRAAhQsxgAJkIA0BChY0riKhpIACVCwGAMkQALSEKBgSeMqGkoCJEDBYgyQAAlIQ4CCJY2raCgJkAAFizFAAiQgDQEKljSuoqEkQAIULMYACZCANAQoWN'
        'K4ioaSAAlQsBgDJEAC0hCgYEnjKhpKAiRAwWIMkAAJSEPg/wHR406Wc3N8mAAAAABJRU5ErkJggg=='
    )
    RR = I(fingerprint, rd)
    R = '{}:{}:{}'.format(get_classname(rd), 'undefined', RR)
    window_time  = hex(int(time.time()*1000))[2:]
    window_width = hex(969)[2:]
    R = '{}/{}/{}/{}'.format(R, window_time, window_width, 'true')
    RR = I(R, rd)
    t[4] = '{:>08s}'.format(hex(RR)[2:])
    t[0] = ''.join([hex(ord(i))[2:] for i in R[::-1]])
    return ''.join(map(str, t))









import re, json
from urllib import request
def mk_url_headers_body(checkid):
    url = (
        'https://t.17track.net/restapi/track'
    )
    body = {"data":[{"num":str(checkid),"fc":0,"sc":0}],"guid":"","timeZoneOffset":-480}
    body = json.dumps(body, separators=(',', ':')).encode()
    leid = make_cookieid(body)
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, ", # auto delete br encoding. cos requests and scrapy can not decode it.
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": (
            "Last-Event-ID={}".format(leid)
        ),
        "origin": "https://t.17track.net",
        "pragma": "no-cache",
        "referer": "https://t.17track.net/zh-cn",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    return url,headers,body

def mypost(url, headers, body):
    r = request.Request(url, method='POST')
    for k, v in list(headers.items()):
        if k.lower() == 'accept-encoding': 
            headers.pop(k); continue # urllib并不自动解压缩编码，所以忽略该headers字段
        r.add_header(k, v)
    proxies = None # {'http':'http://127.0.0.1:8888', 'https':'http://127.0.0.1:8888'}
    opener = request.build_opener(request.ProxyHandler(proxies))
    return opener.open(r, data=body)

if __name__ == '__main__':
    checkid = '123123'
    url, headers, body = mk_url_headers_body(checkid)
    content = mypost(url, headers, body).read()

    import pprint
    pprint.pprint(json.loads(content))
