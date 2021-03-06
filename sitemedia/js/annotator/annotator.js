/*
** Annotator v2.0.0-alpha.3-6a22d86
** https://github.com/okfn/annotator/
**
** Copyright 2015, the Annotator project contributors.
** Dual licensed under the MIT and GPLv3 licenses.
** https://github.com/okfn/annotator/blob/master/LICENSE
**
** Built at: 2015-07-03 04:09:04Z
*/
(function(f) {
  if (typeof exports === "object" && typeof module !== "undefined") {
    module.exports = f()
  } else if (typeof define === "function" && define.amd) {
    define([], f)
  } else {
    var g;
    if (typeof window !== "undefined") {
      g = window
    } else if (typeof global !== "undefined") {
      g = global
    } else if (typeof self !== "undefined") {
      g = self
    } else {
      g = this
    }
    g.annotator = f()
  }
})(function() {
  var define,
    module,
    exports;
  return function e(t, n, r) {
    function s(o, u) {
      if (!n[o]) {
        if (!t[o]) {
          var a = typeof require == "function" && require;
          if (!u && a)
            return a(o, !0);
          if (i)
            return i(o, !0);
          var f = new Error("Cannot find module '" + o + "'");
          throw f.code = "MODULE_NOT_FOUND",
          f
        }
        var l = n[o] = {
          exports: {}
        };
        t[o][0].call(l.exports, function(e) {
          var n = t[o][1][e];
          return s(n
            ? n
            : e)
        }, l, l.exports, e, t, n, r)
      }
      return n[o].exports
    }
    var i = typeof require == "function" && require;
    for (var o = 0; o < r.length; o++)
      s(r[o]);
    return s
  }({
    1: [
      function(require, module, exports) {
        (function(global) {
          "use strict";
          var insertCss = require("insert-css");
          var css = require("./css/annotator.css");
          insertCss(css);
          var app = require("./src/app");
          var util = require("./src/util");
          exports.App = app.App;
          exports.authz = require("./src/authz");
          exports.identity = require("./src/identity");
          exports.notification = require("./src/notification");
          exports.storage = require("./src/storage");
          exports.ui = require("./src/ui");
          exports.util = util;
          exports.ext = {};
          var wgxpath = global.wgxpath;
          if (typeof wgxpath !== "undefined" && wgxpath !== null && typeof wgxpath.install === "function") {
            wgxpath.install()
          }
          var _annotator = global.annotator;
          exports.noConflict = function noConflict() {
            global.annotator = _annotator;
            return this
          }
        }).call(this, typeof global !== "undefined"
          ? global
          : typeof self !== "undefined"
            ? self
            : typeof window !== "undefined"
              ? window
              : {})
      }, {
        "./css/annotator.css": 2,
        "./src/app": 22,
        "./src/authz": 23,
        "./src/identity": 24,
        "./src/notification": 25,
        "./src/storage": 27,
        "./src/ui": 28,
        "./src/util": 39,
        "insert-css": 16
      }
    ],
    2: [
      function(require, module, exports) {
        module.exports = '.annotator-filter *,.annotator-notice,.annotator-widget *{font-family:"Helvetica Neue",Arial,Helvetica,sans-serif;font-weight:400;text-align:left;margin:0;padding:0;background:0 0;-webkit-transition:none;-moz-transition:none;-o-transition:none;transition:none;-moz-box-shadow:none;-webkit-box-shadow:none;-o-box-shadow:none;box-shadow:none;color:#909090}.annotator-adder{background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJAAAAAwCAYAAAD+WvNWAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA2ZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDowMzgwMTE3NDA3MjA2ODExODRCQUU5RDY0RTkyQTJDNiIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDowOUY5RUFERDYwOEIxMUUxOTQ1RDkyQzU2OTNEMDZENCIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDowOUY5RUFEQzYwOEIxMUUxOTQ1RDkyQzU2OTNEMDZENCIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ1M1IE1hY2ludG9zaCI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjA1ODAxMTc0MDcyMDY4MTE5MTA5OUIyNDhFRUQ1QkM4IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjAzODAxMTc0MDcyMDY4MTE4NEJBRTlENjRFOTJBMkM2Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+CtAI3wAAGEBJREFUeNrMnAd8FMe9x3+7d6cuEIgqhCQQ3cI0QQyIblPiENcQ20KiPPzBuLzkYSeOA6Q5zufl896L7cQxOMYRVWAgxjE2YDq2qAIZJJkiUYR6Be5O0p3ubnfezF7R6rS7VxBlkvEdd3s735n57b/M7IojhIDjOKgU9xfchnXrFtPjltE6Gne/CJQrj9bVmQsXrqf/JuzDTRs2EO8D52dmap3Hwz/9+X9K/PTtPeGnyBL/oS2LPfwzXljXjv9g9kK/+H8WNXsxB8aPe8SPPAKy+v3GvR7+n0fNacfPaQiIfch98vHHY/R6/bL+ycmLhg0bhq6xsXednjHdbGhAYWEhbpSUrHU4HKv/48UXz7GvNq5f36YTGQsWaA0+N3XeR2N4Xr8sKTF5Ub9+QxEZ1ZWe/673AM2NN3Hl6vcoKy9ZK4qO1Ue2LZX4Zzyf1ab1g1sWafK/GjVzjA78sjE/GLto8oxpiI/vA4h3EZ22KhIRFRUVOPT1AeTnnVsrQFz9QeM+id9bRHoteFaZeCakpS1KSkqCzWaDyWTCvSjhERFIm5SGuLi4JSeOH2cfveQWjLeItPg5TrcsdczERTFdk2G2AMY61+V0V+eAg8EQi8HDJqNnj95Lcs+28jPBTH/un37z6zh+2U8XpC8aO3QUSIMV4qVbd78DPNAnNAaZz83HqeFDl2zfsMXD/17jHvw8ulVEvBb8P9eulSwPU31jY6MkIFEU70llbZnNjeibkIDExMQljMXNRUUkWU6ibEo4mfVZlpiQvCiyUzLqjYC1hdpmevWKd7myNlhbDbeByM4DEd8ncQljcXMd2kq9kaQCbf7XomctG00tT2rScJByM9BsZ+YBkgm9m1UgUlukzIxx/Udg+KgRSxiLm+s98x5OS0DuTvC0LB0ydAgsFus9E453tVgsSHl4OINZKufVEJCHn+P4pX2TUmBsdgmH3NvqoG2aaNv9B4wEYwmUn7qupdPSJkNssECkkyqK97iyNustmDnjMTAWJb3o1a6AH86ZE0YnLSUsLAxWdjndxxISYmC+KGXkyJGGc+fOsVEXifroS/wJQ2aH8RyfwuliYLfffauvViSrFNaJubWUbnEjDPWV5yV++OBPDekfpjPoUnqEdAFpbrl/HaAiiuWjqZr5lP76HoZrjlonP+ck4tWi/oS+fSN0Oh0dfBsEQbjP1QEai+GRceOi3YwLFy/mFObAwx8VEx9BOw2b/d64LS135hB46PQ69EgY6+E/vO1FjrSPhj383XWdIgwGA4iFuhJ6EiLep0rb5h0EIaEhGGyI8/C/Z3K6MVULZLFaeTZBbldyPwtrn7EwJlmMQLRiIIfdIvELrknUSPnQaCxDk7kqYK4e8WNhs95GSFgMc1GqxzkEp8tiTP7y2+Dg2TspLBGJRr5HUG6uRVVjfcD8qb2GwtjSiM6hUdTf85pWiLFITDJ+9l/VLMxht3NuATEroFbs1D+sWfMRNm3aFHAHvv32Wxw7loNHHnkE4eHhGgLiXRNg52RXqWYMIQr0WJqOSvGIhoCs5nI8MyMUT82cGDD/whWlGJpowaUbTdCH91EVkTT/jEVoy88+U+WHyHkuHo0OlFvqEPHjAZg699mA+Ytf2gnb4EiYixsQZ+iiKiLO1b6LifNK2JSvALsgcCK7gn24l3/84x9BiefGjRJs3LgRK1asxOrVa6RgWasdxsKYZFeA9JkaPxGd/CwYFDTqE9OYePoEzL/490Y8Ng54Y8kgPEnPYWmsoJZGUGxDCkhZ0Cy25deyQAKI8xiRaNbIHw5AwtyRAfPXvrYP+mnxGPafjyLy8WRUWm7ScRZV23GuLpI2/FoWCILD4UmVtVzY7t17pNedOz/DuHHj/IvL6EAfPXpUEhB7/+mnn0qB8qJFi+hriOLCouSOKJP35+pWi/GLPl3Y9PHdpdd3PmlBcTnve4lQFKglNCIxrjOendMXOp7DE4/GweaowFfHacqli2rfX5GxihJTW351MHa1Ow2XtgXqOWWQ9Gr6v1zgutmPmFiEyd6Mzgnd0O3JUeBonNj38REotYtoPlCFSBKmmAmQVgskc5/tBcTJV6iJy31pubCWFmeGFh0djStXrvjsALM0Z86cxejRo/CHP/web7/9R2lx8rPPdkquLCUlRVFwRPQkLq2MYrvggGt9lYIHnwIKMThFc6OaaMdK7gl31GFIvAVXK5uwcXc8np+lR2Q4jx9N642L5QKKy6AoIKe7asuvENxwbV453y6MD3FOob3CBJ2onaoxK9hAzLAODEfj9Urot11GxDODwEcYED87BY1XHBCvGZVdGKfASHug17ASflkguZBY1qZVrFYrvvzyK8nlTZkyBa+/vhy/+tWbePfd95CZmYGHH34YDodD3QI5XZh/FsjFL/oKomWT7PM4Wx2mjgGef3wAvsmtxebd5eD5BDwzHdh/muBqhfI5RNHJKgbA73FhgjMT8mkZaaDr67gGwQw+rTeGPTsG1ceKUbK9EP2oBQ2bmwzb0TII143KHXB95mbyZyvD2WFpArQtkDxT8nXcnj17sGvXLixYkIkPP1xNU3Mdli9fjuTkZAwYMAC3b99WHFTGICosvImam1rE6TZ8BNHyeFbrOIu5ErPH6yRL8+XRevxkVk8a89Rg2yEzymujcfmGugVzLh6L7VaetVxY674U0czCWseIJkUax1U1NSB8eiL6zh6Oqq8voM+TI0AcIhq+uIqYqibYi2+5on0FDEK8QudWPrUgGm4X5lyVVF8plgtIq2ZnZ2P//gOSeE6ePCVZmiNHjiI3Nxfx8fG4efOmM1hW/D2Ru7BWRuUZ59yTI0/j1ao8U1U7pslUhSemGvBYWg98cZi6sKQQ6HUcpozrjv4JUSi4SlBbcU6zHacVFdsxauzAA7IYSK16RKlxTDVN8aNooBw3Yygq9hQifGA3KfbpNWkQovt1h+1iPfJriny0o8zIq1+/8Fz1WtXbzSjV7du34/jxE3j66aewb99+nD59GrGxsTRoXojhw4dL+2zp6fM1zyGxKPh0TQskiU97oU82/u0XAanIm6l45k7SYcrYbjhwvAGpw8IxalgMjI0C9p6gqXBJC+rLT2Hz/4zQbKfNZPtjgVy5DnNNoiCq1lb+9t/ZHHZpfSh8Vj/0nDAQ1UcuI3pkHGIf7guHyQrrgRtoLq5DbvUFjP94gWobxLUO1M4KcRoCgmfyxKAtkNlspsHxZzTj+gZPPfWkZHFOnTqFLl26UMGkY968eaiqqsKsWbOllWa1NtzWxPs+DK0YQmKH6HO/Su5m2uxjOWzgHJX40eQQzJjQHfuP12Hk4DCkpsTA1CTi65PAvw6LiIrkcHhjmuI55JUo7F74dGF+WSDl42yUv1q8jaiZyeg9dQgqD19EVEpPdBuVCMHcAuvhUjR/eQVcpAFzvnrdZ1tqRTsGoj9soYGvpbnZZ0dZgCyf4Pr6euz8/HNqXZowZ/ZsfL7zc1y8dAnstpDXXnuNZlw/QGVFRZugWa0dGip5VqO94y5Nfnr11Jpo8GjSWsl1lhp6TKOVuAbSjq5htUif2wU9YsPw9bEGTBnTGQ8NiEJZjQPrdhPsO0Ngp+gtQqsLrDIqt2Ojsad0JXsLyEdwxgRWe+EaBKNV9Ziu4mPSa92F60Cj3bnyTQSYYoGkF9MQ2SMGJbvOoMe0oYhN6QtL6U3UrT0N417qsuwUvmcE4thYOgTUFChn0brOYcpi11oHct9swG4207hjsa3FdR1369YtfPXVbjQ3NUuZ1cFDhyTxJCQk4KWXlmLUyBGoq61t5/DV2mGfK938QHy4MCkyVr1rQrnDRHSgU0gd5s+JQq9uYSgsNmHiyChJPBV1AtbvEbAvl6bN7iUdoqBGxXO3d2Hww4VxAtsW8OMeJHaMw7XO04Wgb+Z4RPXsgvqCUnSnsQ4Tj7X8Nmo/zoVp92WqatE59kIro1o7jCFgF+bLdKkVFs/s+vJLlNy4IYnn22+/ke4s7NOnjySeQYMG4ZZKtuWPKffXAkliCOLWwwjDbaTPMmBY/3DkF93EhBERGDE4GtUNIjbsJTh9kW2rcAGf1+mCA7kAPHsamtX7uKYIET0XpCImJR4150rQLW0AdVtJaKkyoeHjM7AeKwXv0D6HVjv+uzB3Bzn4Z4FcluokjXHYWk9cXG/s2LEDVdXVGDhwIN5++w/oS7Mto9Eo7Z+5B09+btV2OHdM4/8EEFcaH5gBIpg+miD98ThU1bXg6RndEdc9FNcrBfx5sw3fFet8nkN9LEUQBB4D+ZrA1lTbue3RaeZADF4wGU0Vt5A0bywi+3SF5WoDKn53AC1nKtunUV4CUmNQmxefMZBLQX70gJOyory87ySBlJdXSGk5i3lWrPg1uyEMdfX1bY5v8+r93os00BgIUuAtBGQlOGLDlNERMOg59OkRCh1N1ctqBLy7TURZnR53clOOxOIlGE0+uQvzoxvsGAc9f4/pg8EbdIiK7wpOz8N64xZq3zkC8bpJ+Tyil6sK0IXpfWVhfsdA9Bi2lsPclfvfDz30EJYv/y/JfTFRsaq17KEZAwWahYH4dYXLS2xUE0YN6e7hKioTseZzEXlFzoD5TkqwFogXtUMl+XH2biHolprkGVbrhVrUvXsc1hMVUsDMqyygus0kL6qfO+gsTEl4ahdMYUEhevXqheeeew5paRMl12W1WNDU1OQUo49VM07j3IFbIBJQDCTYTJgwPgb1Rg67jjtw5hLB5VKaEJi19sjYBi/bwIz0MwYKfCWaJ/4JqEmwonfacIg1zbi54wKaj5XB9n0thAYLtSCi4tgyQVscLZ4xVhUQgepKtM8YyJcFiomJkdZ7mOtiT1E8/czTUlvSExw03nGn6UrnYC7ufP556X337t19WqCAYiDXSrqvYmwiiIoAUgfcwjfHS3Ekh8DcJMBqE6jV0RYgc3EjU3rQd73QYPQjCQgkjWdxHxOQQPsuqI+/eIum+NFhcIzvgfzDuSAHTsFuskCw2CHatX0fc3GJ41Kdc1HXLLWlKCDGoGBJiIqASBsL5ENAmZmZeOedd/Dff/7zHZn4n86bpykgLwtENCwQke+F+So7jnD42U+A/31jyB3x//sYD60Htrz2woiGBSJtLBC7g0JUH/+mdQUI/c0k/OCjzDvit26+AJ1KOxIDp8DoTwwEHwJ64okfIzw8DCtXrgoYmu3es62M+fPTkTZxIhoaGjouBnKtRPsq2fsFKb5543ldwPxMvxdvEHz+rYAvckSt/CLolWieXeYah5k/yqPmXkDXP04NXDUCQUtBDRo3FaJpy/eqazq8xrKFqoAKCgsbJ0+Zwp6NkTIotcmqr6vDzMcek24GC2ZthN0fxITDnkRVEqr0Gf2/xWq1HTh40OjvXtjt2kuNvRIfgY46dl7KENU5th8WpHo3Cs+sCC/QGKvZVn09x+jvQmKRtapxnDAAOnbbjchpJoDNa/OleidFB/UlFFZaHDbbCXOR0VcM5MYkNTU1gt1mO2M0GVNDQyNosKg+wEwAatbD7xRaxcqxpxnY2pHDbv/Om1EhhvB8Z22qpyFWyxnOXpaq1ydIT2fcj6KnI8y1lFFrpcBP1Pkb7GbBQYQz1Tpzam9dGIhNuC/8XIgOFbwZAsR2/NqbqfQAk9mclZd3nrqoUPDU3XDUEt3LysQTFhaKgoILMJpMWd4LMdq78TRzbWnMaijZg+hwZkXv/eDraJus7VtlB2Gzmtvx+3BhpFlsyfrG+j30ESHQcbwUo9zTSttkbZ+0XUYTZWm3EKYiIPfiLXn//fe3FhUVbygs/B6RkWEwGPSSO3MH1nersjZYW0y4hYUFuHDh4oa//vWv2+VsGjGQ55hLp7O23qou2GCv34Ou0RxCDezc7pju7lQnP4ewEA5dogjsdV+hoTJvw+XcdQr8oiZ/VtWRrRcbSzccNRRB3ykMOjb+7H90cu9qZWKlbek6heKw/jIKzNc3rKs60p5fIwYirpRCzMnJ+RO7FbO8rCxjzJjR6BzTBexpVfcEOhyilKqLYnCrtGyw2Z2JrLrdGHuU2nj7JnLPnMX1ayXrjxw9+o6bp00qI4rwxV9XdvZP9ECuU31RRvd+M4GweBBdJ9c9RtS322gGYvPvtlc1KxMWAoSGOOMdqQ+CEZytAnUX98JYf3l9bekpRX6NPxPi4T9jvvYnGsNy10NrMqbEPoQ4eydECqHO37IO2GhwbnU4bwcIqgP05KFUBqG81AGOVhPfgmqDCUeshSg2V64/aSxS5tdI491VOHHiRD2tby7IzDxcUlKaodfrh1ML0c198JChgzFhwgTYaJARqIiYeEJDDcg9nYv8/EL5AmENFeWF2trajes3bNjLlpXg3DcOyAKx39RX5NXT+ma/4U8dNtVfzuB43XCOa+WP7TMWnfu+AGMTH7CImHg6RVIRVm5HWWmO3DXVEFG4YG1u2Hi9YKcGv+iTP890rZ7WN5/t9cjhq7aqDD3lpz7Awz8quj+e0o8CZ3Y4H8YPVDyRIdgVWYBTlstOQkF67rrGYREu0Dhs447qk6r8akE054Z3vWcrgbxrIg9KAbuzMvfHv/rqqyx/f2EiTcMDEZFbPKdOncaxYye2/u1vf/u9TOWCq115FWSdwFtvvUUUYiBVftdEtuMfOMa8qhchL3ROSA9IRG7xWCu3oap479ais5sC4h82fqlaEK3I75rIdvwL46etQiT3wjNigCJyieffEfk42JS/NavsUED8rybNIWouzG0+OVknIDt5mw588MEHv6WnY4/ppk+aNMkvETHxsOfATp48ycSzhZ7jNzJwUQbr3QE3m8bfVgiMv/jspt+yxzd6gqR3Tpjvl4g84qn4FFVX9m4pOrs5YH6NFD4g/nXlh3/LJXCEi+TSf+KviFzi2RlNxdNcsIWKJ3B+V7jhKwaC68dEdmJe1gGpM1QAq1555RV2zPzJkydrisgtHuoWmXiy6W9XymAFlY4I3j7Yxz5XQPxFeZtXsYioJxHnd07M1BRRq3i2orJ4b3ZxXnaQ/GKH8WeVHlqFRI4gGvN/SkaDM2mIiIknKgSfdTqPg5b87KzSg0Hxu2WtZoG4Nmpr3wFe1gF2DvHvf/87BXmFWYaMqVOmKIqIBWihVDzHqXhyco5n09+soB/bvVQuqlSP7/3lL3/pywIFzF+ct2WlcwsfGZ2TlEXkEU/5Fqd4vtsSFP/QcYsJOpg/6wYVQhIVUScu4zlxNHglEVHxgIrnX53PY39LQTb9TVD8ryQ/7qHXskDenZGbVvdfadDJG6WCWEXIy2xsMqZNYyJqzc5YdsJinmPHjkni+fDDD3/tgpd3QAm4DfwvfvEL4scue1D8VBDMEqEXCBXRgjYicovHUp5NxbMn+8p3nwbFP2TcQuLHFktQ/FklB1ZREYGLQcbzxEtETDzRIdjRJd8pnpIDQfG/kvwjv/5GohK8fFPf3Yl26qTCWEkI+2tohIpoGux2h3SxMfHk5OTIxWPz6oCgkCq2uaHwjTfeIAHcohEUPxXGShaf9IJIRbRIEhErTvFsRmURFc+5bUHxDxmbSeD/PUpB8WeV7F9J+nEgXbiMdLclYmNGLc+2rvnYZyvIXleyPyj+lwfMbTf6ej+vBO9/K5lYT2OrV69e6XwkCBmPPjpDsj7s0Z6cnGOb6Xdu5du84NunibS8/vrrxJ/N047kv3Juu8Tfi/J3TV4srdk33tjELM9m+l1A/INTM+45/7rr+1aiPz0olsuYz4+RNkM/7XoO++35m+l3AfG/PHCuJrQ+yM4QtL3JsV1H16xZs4IKh32eyf7ihks8b8lUr2Q6iVwwHVwC4r96fgfll1brMnX6MCqe3VQ8//LJPzg13etc4n3hX3dt3woumY5/F2SGwoB9joLNWdf2+eR/edCPAxp/fQd0SJ4ttFkMY4KxWCx5Op0u4pNPPlkvi/YV4ZcvX04IuWd/DNAnPxOMYG/J4zg+4lrhFz75B495geAB4s+6+vVbln72PB3l33ztgE/+ZYOfCJie8/GX6v06h8wnyzMDveu9/CqRp4vtxBNM43/5y1/ueMO5I/gl8QRRLp/NfiD4mXiC2oq6U3rXxBOFVUzmY1tcr/Lq6CjxdERxTfwd8Qcrno4orom/I/5gxdMhAlIQkXwF064CLzwI4lERUUD891M8KiIKiP9OxNNhAvISEVFZDpevaJIHRTwKIvKb/0EQj4KI/Oa/U/F0qIA03JnS+wdKPD7cmSL/gyQeH+5Mkb8jxHOnWZiWiOTBLVH6/kEtbmHIglui9P2DWtzCWH3534r8HSUcd/l/AQYA7PGYKl3+RK0AAAAASUVORK5CYII=);background-repeat:no-repeat}.annotator-editor a:after,.annotator-filter .annotator-filter-navigation button:after,.annotator-filter .annotator-filter-property .annotator-filter-clear,.annotator-resize,.annotator-viewer .annotator-controls a,.annotator-viewer .annotator-controls button,.annotator-widget:after{background-image:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAEiCAYAAAD0w4JOAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyJpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBNYWNpbnRvc2giIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6RDY0MTMzNTM2QUQzMTFFMUE2REJERDgwQTM3Njg5NTUiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6RDY0MTMzNTQ2QUQzMTFFMUE2REJERDgwQTM3Njg5NTUiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDo2ODkwQjlFQzZBRDExMUUxQTZEQkREODBBMzc2ODk1NSIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDpENjQxMzM1MjZBRDMxMUUxQTZEQkREODBBMzc2ODk1NSIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PkijPpwAABBRSURBVHja7JsJVBRXFoarq5tNQZZWo6BxTRQXNOooxhWQBLcYlwRkMirmOKMnmVFHUcYdDUp0Yo5OopM4cQM1TlyjUSFGwIUWFQUjatxNQEFEFtnX+W/7Sovqqt7w5EwMdc6ltldf3/fevffderxSZWVlZbi5uTXh6rAVFBTkqbVubl07eno2d3BwaGgtZNPGjYf5wsLCDRu/+ir20aNH2dZCcnNzN6uPHTv2S2xsbHZaWpqLJZqJIR9FRMTxdHFJeHiiJZrl5+fniiF0jRdumgsjyOZNm44AshHPxAnXeXEhUzAJJEF8j5cWVoIZg9CmqqiokK3CksWLX3d0dJwy+f3331Cr1RoliEajMQ4Sw2xsbHglTZ6CampquOex8dxz2l5gkEY4qKyslOu1Qa6urpPRs9VkW2RjFmskQCaFhASQLZEZkDlYBBJDnJ2dXSnwmYLxpiDCdVMw3hyIObCnlr1g/nwfQCYpQcQbOTM5tbgDeDEkZPLkoaYgSpqpKysqnkIaNWrkYq7dUEim0EwhmkI1bw1ETjNVTk7OA2sg0jarDyO/ZhiJjtpS4923L1dWVs5VV1vW8Dyv4uzsbLnkc+c4dceOnn1LS0vat23bhnvSgypOpTItajXP2dvbcefOneVSL146ys+dOzvgyuWrMadOJeKGrb6AeRBb7syZM1xqyo9HwfDncZ0L+0dowGXATpw4qVfVGEyAJCUBkvrjUTzrTwzUkirDcfOewk5w9oBp8AD9iljoGt07rTvNpaRcPDqPIOx5+mlOkPnz5wakpV2JiU84ztlRNTVqTsXzeuHValyz4xJ1Ou4CICjrL37WoPsXLAgD7HJMXFw8Z2ur4dT8E23s7Wy4UydPchcupB5FGX8ZOxKUeyYLF84LSLt0OebYsXi9ZvYOdtwJBsE9f7lnVAUFuYp2smxpxJFOnTu9aWtry6VcSDm6cNF8f6WyRkEMFg7rclq0aP7fjZWrDyNmeL9c8iDedu7YMRK7xoHjx28y2tjGcsivt29PaOTsPNAGeSIGidNBwcF9La6aAPH18+UG+QzmtFqtN67pLALt2LYtAUOUHoLMWO/1BMM45o17OgUQ2dEz2R4drYf4AMLzakTNahY5n8FQRid9rpZG26KiE5ypOkP89JqIjZWOVSqeG+zrw7lp3bxRVidbteitUQnOLtQmhhApzMfXFzCtN57R1QJFbdkKiMtAP0Ao7lB16CE5oXtUTYJRB+BZPUzd6uWXE1xcXQcO8R+iqIms3aADWrdpw2VmZrbQJeoCeBdoYinkWTVVHNVC21jrrSopKakh67Y2ChCMXmw0xizbXM2I8dyc9gUObBpTBTw8WqixGw45n5GRnl4XjaZD9kP+DaibVSA8OAu7SHZKWm3GtTYWgfDATOxWQGxElynsepkNAoSq808JhII7DZKHzWpsQGYwiPhHyPzD0NifmtVGrE1WUlSQaDIXkNVm2REgc1jDiqtTBQk1pkmtqgEyCLu/SqpKkFmArDHLsgGxw57euaiXIkSQOeZCBI1egtCs324IxVGy3s9NtYkcqCtkGBtXHkLeAyTBGl8rZPZxCfIAkNIXLB6h9/4A6a/gMv0hvUyCUKgLdlsoXODYXwJ5E7sDzPM7G7OjPtjvgnjSizNkqwDDPoD9AL08E2QXaa7Ua40gLUTXmkHW44Gd2I9ndiZsLVh52ar9AAlmNiRs7eg9ByIOYtkMHGe0+6HBW9ithbSSKXcH8iFs7DuTvYZC31KKpFAuyhhE2v3kJkEK5YJZwytbtru7B8GGQjZCmhopmwkJgcRCu2o5jXwh2yWQWyxS3pH05teQwUpVK4Jkia49YA07l/ast8T3ihR7DfXvhuP/Mq2CATksarsRrBPuQQJx76Kp7vfGzh4F42V8zQe7YtxL+u2EkVoDZJ8+fej8VQi9vPRmg8BpCKXAN5OSkqpNVg0QR7VaPR3n05FLN6k9mcJnYLcK178ErEQRBIgTMtMNyG4Djaqv0XyJMtMBM4jrPCC8vb19KEHatWtXMHbs2LtOTk7lQoHGjRuXjBs37q6Hh0cRyvwZr+5/kW1s3GhXVVWlfxXv27fvhTlz5iybNm1aCuBVeEsqnzFjRmJoaOjS7t27X2fVXIgfdzfQtnnz5sPv3r2r/3/Rvn37WkdHR/8I1UNdXV1X4kdK+vfvPxsPNm3YsKE++JWWlmpbtNBH0C21QDY2NgOEk8LCwlY4340HhwM2DZfKcaxFJ+wsKip6OlfZoEGDwVIQD/Vrzc1Ciyb+/v4UGS9A0nx8fDxRHSdxGbzTaQ2q1qpVq3vnz58XGrYUbZIM0FVo0gOXyqBZ8p49ey6tW7fO8/Hjx7ZUrm3btgbZLe/p6Xnczs6ODI8bMWJEGiDTAfGAFjGo5nc4rh4zZswMaKYPKdSjXl5e8XLdfzQgIEBf6ODBg2qcv47qRcH4GuNlpRWOd+Bap8TERH0CNnz48Gv9+vVLkDNINXrtg8jIyEWootaYQaIHs2AKc5s1a7aVZS8GLuJ0//798M2bN4+NiYlxxztcLR90dHSsGDlyZHpwcHBU06ZNKWUuNRZGnGAjwTdu3BifkpLS7PLly05oJ65r164FMMZ0WH0UXIRG5GJz4pGajaad2RBOnXCZSYa0OrVAMueOEFc23tODuUyKxSBpQBS3hcbd3b396NGj+/v6+np16NDhVfRcNar40/fff5+ya9euk/n5+XeYlsoRomfPnv3j4+O3oJ0e1Ug2uMeDQ4cOfdmlS5deQlSVzgfoqzNkyJDXrl+/Hl9jYrt48eIh/GBHWRCq4HTq1KmtVLC4uDgZu48QVrKFhxGD7mC3DCZxjc5jY2M/o9HGAAQfGlBeXv6YCqEtKLd2weFYNM9jALNwTJ7e5OzZs1Hsx7JXrlzZ3QCk0+nmCb+el5d3Jzw8/ANKpnDqC6FBQLt27dp5CDGZQrnjx49/aACCe2yRNOx9wPsJvQBN3iorK8sXl7l58+bnUpDGwcGh1lQEQqyNt7d3GYUdeqXo1atXKQraissgWlbIDAyaZOzfZ/8+TMd5iEqluhMWFvZHmEIpjncDNAHttR6RUsuC31kDA4LanihUxOq+ivLGNWvWzAYjF4Hs3qJFi6bgWuvU1NStrBepR1satBH+0ERLJBXKyMi4AMP7Ag2bJbRHbm7unQMHDqzPzs7+ic5RNgw7lZxB0oErfumgKYOE5tHYNVSybAHmBlkB+8mXAnDtISALcdhI7LRiUUnmgowmEWj4akXvF1+g4Zs6hYmGRUIyhXLKRIzlUuJshEYOyvZDUBUHaTaCax/jcINcAiHORlpi6NmJHulrIhtZi06ZDViF3HAE43aINAahZAIWD0bl3wD7E55RGYBcXFy84f3vKkFo9IWVJ82aNSsVY34lNF8Ky25pAELW8Ta6VnZCSqvV0hB+ys/Pb/qZM2d2oRxlI+4Y194wAKFLe9IBDduBgYG3e/TooX/dwg+UzZw5U4chnNKatgjDoXAnDc07oikGGrQf1G1AB+3bt8/FABgJ1duvWrXqvUGDBl0HZBYgbSgtRBu6irIRZwONkDTRywqH0UL7zjvvvILBMQLD9+qhQ4cS5GVAvkIju4pMoQY/+osBCDFbh8arIkdEo89euHDhAgC+ZZpsFEP0bzbNmhUhG/nBADRgwIADqEbG0ymaqqrZqN5+xJ5NgBhMzmHcO4cU57gBqGXLlmkTJ07c0K1bt0dPp68qKjoCaLAOibJbZL00o5Oj5CKu6enpS5CIvo3hpjnito2kOsVBQUE/jxo16hP0zUY2q6OYRDijjQJv3boViDzJHdGyCaUz6Lnszp07X0GnbGRv5JXmZCPk/ZRD08wE2UoBez2/xhIJztxshGfZiBsbRSgePWKQEuk8tlI2Yo8M1xOJZz9kI52QWL2CqpYg6F9FHE/duXMnrX24K9c+4s0B7jEKxngQXV6ikI18gQy4h7FsRD116tQ3MzMzL5kK/uiEfTDgNrIgdKv7lStXYk2MHlmIkAV0jKHpYyRkDQxAyOqDULDMCITSGh/kRpMoa8GWsXr16l5SEA8H7AdHtJVrOGjxC+5NQui4mpyc3Ap7Ncb95sgHDGe+7t279x0biovhGovx8H6mSQZpQoYdFRW1VEgJcb/q9u3b6wyq9vDhwz1suD6PzL4nUhZnnG6AUBRshiQ+HJA80WBZmZWV9YkBKCcnZxErUI3R4Ru4Ak1wksO6b9q0abEYwjQtR0IWaABCKvc6bhYLBRGbd+NV9D1UJ4IyEmnjI9ymYecul43YoTfWiwtTBoJrRXK9iLYMUkwicPASChwxIxtZRm9TprKRxpDlaKocmWzkKnYTITbmZiNqNuNH89tjWSSk6aBk2FCWMe9/kf+7vnz5ilp1k55b8q+/moiI5TWiHpCemyVKD1sM44w8bDXI6mrJgercRnWGGbPsGpkB1CqDVP3GXeR3CLI4CsgZFzPGOvmaVRADkLWQWiApxKp4pACxDPQ8IIL3S728xlKHFexIVRevr3faFwZkdQIhE0ZeoJFWLh5ZBTOlidkwc6plFkwpibA4tPAW/FOh3tfqQRaBrHrRMZWNmDvyPheIrPdbmwO8wBmbNB5ZldLI2ZGq3td+RRBNz0NWWr2ShRaguLi4LFOr1R9UVVXdx6U5FoP8/Pym2dvbr8jLy3O2em1NUFDQ4cLCwoA6t9G2bdscpk6des3BwaGyTiC0yachISHX9+zZk4Qq3qtrxuYEmQWJO3v2bEzv3r2/qWui1R6y5Hl4f72vWTgjY0n78UoDZp2rplKpHCCd6gIiB+44evTod1NSUhZb21Yvd+jQYZROp9tZWVlZVlxcnKU03aFo2di8du/evVa88MQqEP58IZ0Itxakhkyj1R51AkkWDui1QzXvWw0SAWmVyjeWguq9vx70XCIkxjD6T3E4ZGlSUlK+1Rrt3buXFpPSmtFbyEimQdRWgRo0aPA2O6b/X6+DXAQs4Hm0EYXZw4CF1Qnk5uZWGhgY+CnaK9KqjM3W1rZ62LBhVydMmDDdw8PjqMWNlJubewL5UWZiYmIo/WPTmgRCiJBLIc2tBdTHo/+3tMaS1IZnRknLX23qpNLBgwddk5OT93p5edG/nFtLtTTbIOPi4uif4TXl5eUFBw4cWOfo6EgfWTS1GiRa7vnzmjVrKD9qXyeQaAuzBCS37OxnyAykf3utCiPck9U8tEIzEpASa15qaHkHLfloY860UL3314Pk4pG7u4ex+7QYhT60bA6Jh2yAlGZkpBu1bOlGn6HtF52P4Z587duVk6xpM1a1cSLIEchJkYazzG0jWuxOCTstfKMv6OhLMlquF8vuDzcH1I5BaKO1o/tEk3jC0sUcUyD69RvckwWDHIuStIDSHjKE3actwlgYoRXj/2HH9GYkfGlInyreEZ3/jXuyoFlWIy8RRBgAxJ+WCRD6cPdfxgzyI3ZMHwPu4Z6sgKaPLO+z6ze5J0usPzMVIYWPKZ0YuJr1lPB91ihImjmhlj5bfI118SlIHkRIRqeYAxFchNZiX+EMP6ScImq7WpuSi5SwTHYyc4u7rFEvWuS09TH79wz6nwADANCoQA3w0fcjAAAAAElFTkSuQmCC);background-repeat:no-repeat}.annotator-hl{background:#FFFF0A;background:rgba(255,255,10,.3);-ms-filter:"progid:DXImageTransform.Microsoft.gradient(startColorstr=#4DFFFF0A, endColorstr=#4DFFFF0A)"}.annotator-hl-temporary{background:#007CFF;background:rgba(0,124,255,.3);-ms-filter:"progid:DXImageTransform.Microsoft.gradient(startColorstr=#4D007CFF, endColorstr=#4D007CFF)"}.annotator-wrapper{position:relative}.annotator-adder,.annotator-notice,.annotator-outer{z-index:1020}.annotator-adder,.annotator-notice,.annotator-outer,.annotator-widget{position:absolute;font-size:10px;line-height:1}.annotator-hide{display:none;visibility:hidden}.annotator-adder{margin-top:-48px;margin-left:-24px;width:48px;height:48px;background-position:left top}.annotator-adder:hover{background-position:center top}.annotator-adder:active{background-position:center right}.annotator-adder button{display:block;width:36px;height:41px;margin:0 auto;border:none;background:0 0;text-indent:-999em;cursor:pointer}.annotator-outer{width:0;height:0}.annotator-widget{margin:0;padding:0;bottom:15px;left:-18px;min-width:265px;background-color:#FBFBFB;background-color:rgba(251,251,251,.98);border:1px solid #7A7A7A;border:1px solid rgba(122,122,122,.6);-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;-webkit-box-shadow:0 5px 15px rgba(0,0,0,.2);-moz-box-shadow:0 5px 15px rgba(0,0,0,.2);-o-box-shadow:0 5px 15px rgba(0,0,0,.2);box-shadow:0 5px 15px rgba(0,0,0,.2)}.annotator-invert-x .annotator-widget{left:auto;right:-18px}.annotator-invert-y .annotator-widget{bottom:auto;top:8px}.annotator-widget strong{font-weight:700}.annotator-widget .annotator-item,.annotator-widget .annotator-listing{padding:0;margin:0;list-style:none}.annotator-widget:after{content:"";display:block;width:18px;height:10px;background-position:0 0;position:absolute;bottom:-10px;left:8px}.annotator-invert-x .annotator-widget:after{left:auto;right:8px}.annotator-invert-y .annotator-widget:after{background-position:0 -15px;bottom:auto;top:-9px}.annotator-editor .annotator-item input,.annotator-editor .annotator-item textarea,.annotator-widget .annotator-item{position:relative;font-size:12px}.annotator-viewer .annotator-item{border-top:2px solid #7A7A7A;border-top:2px solid rgba(122,122,122,.2)}.annotator-widget .annotator-item:first-child{border-top:none}.annotator-editor .annotator-item,.annotator-viewer div{border-top:1px solid #858585;border-top:1px solid rgba(133,133,133,.11)}.annotator-viewer div{padding:6px}.annotator-viewer .annotator-item ol,.annotator-viewer .annotator-item ul{padding:4px 16px}.annotator-editor .annotator-item:first-child textarea,.annotator-viewer div:first-of-type{padding-top:12px;padding-bottom:12px;color:#3c3c3c;font-size:13px;font-style:italic;line-height:1.3;border-top:none}.annotator-viewer .annotator-controls{position:relative;top:5px;right:5px;padding-left:5px;opacity:0;-webkit-transition:opacity .2s ease-in;-moz-transition:opacity .2s ease-in;-o-transition:opacity .2s ease-in;transition:opacity .2s ease-in;float:right}.annotator-viewer li .annotator-controls.annotator-visible,.annotator-viewer li:hover .annotator-controls{opacity:1}.annotator-viewer .annotator-controls a,.annotator-viewer .annotator-controls button{cursor:pointer;display:inline-block;width:13px;height:13px;margin-left:2px;border:none;opacity:.2;text-indent:-900em;background-color:transparent;outline:0}.annotator-viewer .annotator-controls a:focus,.annotator-viewer .annotator-controls a:hover,.annotator-viewer .annotator-controls button:focus,.annotator-viewer .annotator-controls button:hover{opacity:.9}.annotator-viewer .annotator-controls a:active,.annotator-viewer .annotator-controls button:active{opacity:1}.annotator-viewer .annotator-controls button[disabled]{display:none}.annotator-viewer .annotator-controls .annotator-edit{background-position:0 -60px}.annotator-viewer .annotator-controls .annotator-delete{background-position:0 -75px}.annotator-viewer .annotator-controls .annotator-link{background-position:0 -270px}.annotator-editor .annotator-item{position:relative}.annotator-editor .annotator-item label{top:0;display:inline;cursor:pointer;font-size:12px}.annotator-editor .annotator-item input,.annotator-editor .annotator-item textarea{display:block;min-width:100%;padding:10px 8px;border:none;margin:0;color:#3c3c3c;background:0 0;-webkit-box-sizing:border-box;-moz-box-sizing:border-box;-o-box-sizing:border-box;box-sizing:border-box;resize:none}.annotator-editor .annotator-item textarea::-webkit-scrollbar{height:8px;width:8px}.annotator-editor .annotator-item textarea::-webkit-scrollbar-track-piece{margin:13px 0 3px;background-color:#e5e5e5;-webkit-border-radius:4px}.annotator-editor .annotator-item textarea::-webkit-scrollbar-thumb:vertical{height:25px;background-color:#ccc;-webkit-border-radius:4px;-webkit-box-shadow:0 1px 1px rgba(0,0,0,.1)}.annotator-editor .annotator-item textarea::-webkit-scrollbar-thumb:horizontal{width:25px;background-color:#ccc;-webkit-border-radius:4px}.annotator-editor .annotator-item:first-child textarea{min-height:5.5em;-webkit-border-radius:5px 5px 0 0;-moz-border-radius:5px 5px 0 0;-o-border-radius:5px 5px 0 0;border-radius:5px 5px 0 0}.annotator-editor .annotator-item input:focus,.annotator-editor .annotator-item textarea:focus{background-color:#f3f3f3;outline:0}.annotator-editor .annotator-item input[type=checkbox],.annotator-editor .annotator-item input[type=radio]{width:auto;min-width:0;padding:0;display:inline;margin:0 4px 0 0;cursor:pointer}.annotator-editor .annotator-checkbox{padding:8px 6px}.annotator-editor .annotator-controls,.annotator-filter,.annotator-filter .annotator-filter-navigation button{text-align:right;padding:3px;border-top:1px solid #d4d4d4;background-color:#d4d4d4;background-image:-webkit-gradient(linear,left top,left bottom,from(#f5f5f5),color-stop(.6,#dcdcdc),to(#d2d2d2));background-image:-moz-linear-gradient(to bottom,#f5f5f5,#dcdcdc 60%,#d2d2d2);background-image:-webkit-linear-gradient(to bottom,#f5f5f5,#dcdcdc 60%,#d2d2d2);background-image:linear-gradient(to bottom,#f5f5f5,#dcdcdc 60%,#d2d2d2);-webkit-box-shadow:inset 1px 0 0 rgba(255,255,255,.7),inset -1px 0 0 rgba(255,255,255,.7),inset 0 1px 0 rgba(255,255,255,.7);-moz-box-shadow:inset 1px 0 0 rgba(255,255,255,.7),inset -1px 0 0 rgba(255,255,255,.7),inset 0 1px 0 rgba(255,255,255,.7);-o-box-shadow:inset 1px 0 0 rgba(255,255,255,.7),inset -1px 0 0 rgba(255,255,255,.7),inset 0 1px 0 rgba(255,255,255,.7);box-shadow:inset 1px 0 0 rgba(255,255,255,.7),inset -1px 0 0 rgba(255,255,255,.7),inset 0 1px 0 rgba(255,255,255,.7);-webkit-border-radius:0 0 5px 5px;-moz-border-radius:0 0 5px 5px;-o-border-radius:0 0 5px 5px;border-radius:0 0 5px 5px}.annotator-editor.annotator-invert-y .annotator-controls{border-top:none;border-bottom:1px solid #b4b4b4;-webkit-border-radius:5px 5px 0 0;-moz-border-radius:5px 5px 0 0;-o-border-radius:5px 5px 0 0;border-radius:5px 5px 0 0}.annotator-editor a,.annotator-filter .annotator-filter-property label{position:relative;display:inline-block;padding:0 6px 0 22px;color:#363636;text-shadow:0 1px 0 rgba(255,255,255,.75);text-decoration:none;line-height:24px;font-size:12px;font-weight:700;border:1px solid #a2a2a2;background-color:#d4d4d4;background-image:-webkit-gradient(linear,left top,left bottom,from(#f5f5f5),color-stop(.5,#d2d2d2),color-stop(.5,#bebebe),to(#d2d2d2));background-image:-moz-linear-gradient(to bottom,#f5f5f5,#d2d2d2 50%,#bebebe 50%,#d2d2d2);background-image:-webkit-linear-gradient(to bottom,#f5f5f5,#d2d2d2 50%,#bebebe 50%,#d2d2d2);background-image:linear-gradient(to bottom,#f5f5f5,#d2d2d2 50%,#bebebe 50%,#d2d2d2);-webkit-box-shadow:inset 0 0 5px rgba(255,255,255,.2),inset 0 0 1px rgba(255,255,255,.8);-moz-box-shadow:inset 0 0 5px rgba(255,255,255,.2),inset 0 0 1px rgba(255,255,255,.8);-o-box-shadow:inset 0 0 5px rgba(255,255,255,.2),inset 0 0 1px rgba(255,255,255,.8);box-shadow:inset 0 0 5px rgba(255,255,255,.2),inset 0 0 1px rgba(255,255,255,.8);-webkit-border-radius:5px;-moz-border-radius:5px;-o-border-radius:5px;border-radius:5px}.annotator-editor a:after{position:absolute;top:50%;left:5px;display:block;content:"";width:15px;height:15px;margin-top:-7px;background-position:0 -90px}.annotator-editor a.annotator-focus,.annotator-editor a:focus,.annotator-editor a:hover,.annotator-filter .annotator-filter-active label,.annotator-filter .annotator-filter-navigation button:hover{outline:0;border-color:#435aa0;background-color:#3865f9;background-image:-webkit-gradient(linear,left top,left bottom,from(#7691fb),color-stop(.5,#5075fb),color-stop(.5,#3865f9),to(#3665fa));background-image:-moz-linear-gradient(to bottom,#7691fb,#5075fb 50%,#3865f9 50%,#3665fa);background-image:-webkit-linear-gradient(to bottom,#7691fb,#5075fb 50%,#3865f9 50%,#3665fa);background-image:linear-gradient(to bottom,#7691fb,#5075fb 50%,#3865f9 50%,#3665fa);color:#fff;text-shadow:0 -1px 0 rgba(0,0,0,.42)}.annotator-editor a:focus:after,.annotator-editor a:hover:after{margin-top:-8px;background-position:0 -105px}.annotator-editor a:active,.annotator-filter .annotator-filter-navigation button:active{border-color:#700c49;background-color:#d12e8e;background-image:-webkit-gradient(linear,left top,left bottom,from(#fc7cca),color-stop(.5,#e85db2),color-stop(.5,#d12e8e),to(#ff009c));background-image:-moz-linear-gradient(to bottom,#fc7cca,#e85db2 50%,#d12e8e 50%,#ff009c);background-image:-webkit-linear-gradient(to bottom,#fc7cca,#e85db2 50%,#d12e8e 50%,#ff009c);background-image:linear-gradient(to bottom,#fc7cca,#e85db2 50%,#d12e8e 50%,#ff009c)}.annotator-editor a.annotator-save:after{background-position:0 -120px}.annotator-editor a.annotator-save.annotator-focus:after,.annotator-editor a.annotator-save:focus:after,.annotator-editor a.annotator-save:hover:after{margin-top:-8px;background-position:0 -135px}.annotator-editor .annotator-widget:after{background-position:0 -30px}.annotator-editor.annotator-invert-y .annotator-widget .annotator-controls{background-color:#f2f2f2}.annotator-editor.annotator-invert-y .annotator-widget:after{background-position:0 -45px;height:11px}.annotator-resize{position:absolute;top:0;right:0;width:12px;height:12px;background-position:2px -150px}.annotator-invert-x .annotator-resize{right:auto;left:0;background-position:0 -195px}.annotator-invert-y .annotator-resize{top:auto;bottom:0;background-position:2px -165px}.annotator-invert-y.annotator-invert-x .annotator-resize{background-position:0 -180px}.annotator-notice{color:#fff;position:fixed;top:-54px;left:0;width:100%;font-size:14px;line-height:50px;text-align:center;background:#000;background:rgba(0,0,0,.9);border-bottom:4px solid #d4d4d4;-webkit-transition:top .4s ease-out;-moz-transition:top .4s ease-out;-o-transition:top .4s ease-out;transition:top .4s ease-out}.annotator-notice-success{border-color:#3665f9}.annotator-notice-error{border-color:#ff7e00}.annotator-notice p{margin:0}.annotator-notice a{color:#fff}.annotator-notice-show{top:0}.annotator-tags{margin-bottom:-2px}.annotator-tags .annotator-tag{display:inline-block;padding:0 8px;margin-bottom:2px;line-height:1.6;font-weight:700;background-color:#e6e6e6;-webkit-border-radius:8px;-moz-border-radius:8px;-o-border-radius:8px;border-radius:8px}.annotator-filter{z-index:1010;position:fixed;top:0;right:0;left:0;text-align:left;line-height:0;border:none;border-bottom:1px solid #878787;padding-left:10px;padding-right:10px;-webkit-border-radius:0;-moz-border-radius:0;-o-border-radius:0;border-radius:0;-webkit-box-shadow:inset 0 -1px 0 rgba(255,255,255,.3);-moz-box-shadow:inset 0 -1px 0 rgba(255,255,255,.3);-o-box-shadow:inset 0 -1px 0 rgba(255,255,255,.3);box-shadow:inset 0 -1px 0 rgba(255,255,255,.3)}.annotator-filter strong{font-size:12px;font-weight:700;color:#3c3c3c;text-shadow:0 1px 0 rgba(255,255,255,.7);position:relative;top:-9px}.annotator-filter .annotator-filter-navigation,.annotator-filter .annotator-filter-property{position:relative;display:inline-block;overflow:hidden;line-height:10px;padding:2px 0;margin-right:8px}.annotator-filter .annotator-filter-navigation button,.annotator-filter .annotator-filter-property label{text-align:left;display:block;float:left;line-height:20px;-webkit-border-radius:10px 0 0 10px;-moz-border-radius:10px 0 0 10px;-o-border-radius:10px 0 0 10px;border-radius:10px 0 0 10px}.annotator-filter .annotator-filter-navigation .annotator-filter-next,.annotator-filter .annotator-filter-property input{-webkit-border-radius:0 10px 10px 0;border-radius:0 10px 10px 0;-moz-border-radius:0 10px 10px 0;-o-border-radius:0 10px 10px 0}.annotator-filter .annotator-filter-property label{padding-left:8px}.annotator-filter .annotator-filter-property input{display:block;float:right;-webkit-appearance:none;border:1px solid #878787;border-left:none;padding:2px 4px;line-height:16px;min-height:16px;font-size:12px;width:150px;color:#333;background-color:#f8f8f8;-webkit-box-shadow:inset 0 1px 1px rgba(0,0,0,.2);-moz-box-shadow:inset 0 1px 1px rgba(0,0,0,.2);-o-box-shadow:inset 0 1px 1px rgba(0,0,0,.2);box-shadow:inset 0 1px 1px rgba(0,0,0,.2)}.annotator-filter .annotator-filter-property input:focus{outline:0;background-color:#fff}.annotator-filter .annotator-filter-clear{position:absolute;right:3px;top:6px;border:none;text-indent:-900em;width:15px;height:15px;background-position:0 -90px;opacity:.4}.annotator-filter .annotator-filter-clear:focus,.annotator-filter .annotator-filter-clear:hover{opacity:.8}.annotator-filter .annotator-filter-clear:active{opacity:1}.annotator-filter .annotator-filter-navigation button{border:1px solid #a2a2a2;padding:0;text-indent:-900px;width:20px;min-height:22px;-webkit-box-shadow:inset 0 0 5px rgba(255,255,255,.2),inset 0 0 1px rgba(255,255,255,.8);-moz-box-shadow:inset 0 0 5px rgba(255,255,255,.2),inset 0 0 1px rgba(255,255,255,.8);-o-box-shadow:inset 0 0 5px rgba(255,255,255,.2),inset 0 0 1px rgba(255,255,255,.8);box-shadow:inset 0 0 5px rgba(255,255,255,.2),inset 0 0 1px rgba(255,255,255,.8)}.annotator-filter .annotator-filter-navigation button,.annotator-filter .annotator-filter-navigation button:focus,.annotator-filter .annotator-filter-navigation button:hover{color:transparent}.annotator-filter .annotator-filter-navigation button:after{position:absolute;top:8px;left:8px;content:"";display:block;width:9px;height:9px;background-position:0 -210px}.annotator-filter .annotator-filter-navigation button:hover:after{background-position:0 -225px}.annotator-filter .annotator-filter-navigation .annotator-filter-next{border-left:none}.annotator-filter .annotator-filter-navigation .annotator-filter-next:after{left:auto;right:7px;background-position:0 -240px}.annotator-filter .annotator-filter-navigation .annotator-filter-next:hover:after{background-position:0 -255px}.annotator-hl-active{background:#FFFF0A;background:rgba(255,255,10,.8);-ms-filter:"progid:DXImageTransform.Microsoft.gradient(startColorstr=#CCFFFF0A, endColorstr=#CCFFFF0A)"}.annotator-hl-filtered{background-color:transparent}';
      }, {}
    ],
    3: [
      function(require, module, exports) {
        (function(definition) {
          if (typeof exports === "object") {
            module.exports = definition()
          } else if (typeof define === "function" && define.amd) {
            define(definition)
          } else {
            window.BackboneExtend = definition()
          }
        })(function() {
          "use strict";
          var _ = {
            has: function(obj, key) {
              return Object.prototype.hasOwnProperty.call(obj, key)
            },
            extend: function(obj) {
              for (var i = 1; i < arguments.length; ++i) {
                var source = arguments[i];
                if (source) {
                  for (var prop in source) {
                    obj[prop] = source[prop]
                  }
                }
              }
              return obj
            }
          };
          var extend = function(protoProps, staticProps) {
            var parent = this;
            var child;
            if (protoProps && _.has(protoProps, "constructor")) {
              child = protoProps.constructor
            } else {
              child = function() {
                return parent.apply(this, arguments)
              }
            }
            _.extend(child, parent, staticProps);
            var Surrogate = function() {
              this.constructor = child
            };
            Surrogate.prototype = parent.prototype;
            child.prototype = new Surrogate;
            if (protoProps)
              _.extend(child.prototype, protoProps);
            child.__super__ = parent.prototype;
            return child
          };
          return extend
        })
      }, {}
    ],
    4: [
      function(require, module, exports) {
        var process = module.exports = {};
        var queue = [];
        var draining = false;
        function drainQueue() {
          if (draining) {
            return
          }
          draining = true;
          var currentQueue;
          var len = queue.length;
          while (len) {
            currentQueue = queue;
            queue = [];
            var i = -1;
            while (++i < len) {
              currentQueue[i]()
            }
            len = queue.length
          }
          draining = false
        }
        process.nextTick = function(fun) {
          queue.push(fun);
          if (!draining) {
            setTimeout(drainQueue, 0)
          }
        };
        process.title = "browser";
        process.browser = true;
        process.env = {};
        process.argv = [];
        process.version = "";
        process.versions = {};
        function noop() {}
        process.on = noop;
        process.addListener = noop;
        process.once = noop;
        process.off = noop;
        process.removeListener = noop;
        process.removeAllListeners = noop;
        process.emit = noop;
        process.binding = function(name) {
          throw new Error("process.binding is not supported")
        };
        process.cwd = function() {
          return "/"
        };
        process.chdir = function(dir) {
          throw new Error("process.chdir is not supported")
        };
        process.umask = function() {
          return 0
        }
      }, {}
    ],
    5: [
      function(require, module, exports) {
        "use strict";
        var Promise = require("./promise/promise").Promise;
        var polyfill = require("./promise/polyfill").polyfill;
        exports.Promise = Promise;
        exports.polyfill = polyfill
      }, {
        "./promise/polyfill": 10,
        "./promise/promise": 11
      }
    ],
    6: [
      function(require, module, exports) {
        "use strict";
        var isArray = require("./utils").isArray;
        var isFunction = require("./utils").isFunction;
        function all(promises) {
          var Promise = this;
          if (!isArray(promises)) {
            throw new TypeError("You must pass an array to all.")
          }
          return new Promise(function(resolve, reject) {
            var results = [],
              remaining = promises.length,
              promise;
            if (remaining === 0) {
              resolve([])
            }
            function resolver(index) {
              return function(value) {
                resolveAll(index, value)
              }
            }
            function resolveAll(index, value) {
              results[index] = value;
              if (--remaining === 0) {
                resolve(results)
              }
            }
            for (var i = 0; i < promises.length; i++) {
              promise = promises[i];
              if (promise && isFunction(promise.then)) {
                promise.then(resolver(i), reject)
              } else {
                resolveAll(i, promise)
              }
            }
          })
        }
        exports.all = all
      }, {
        "./utils": 15
      }
    ],
    7: [
      function(require, module, exports) {
        (function(process, global) {
          "use strict";
          var browserGlobal = typeof window !== "undefined"
            ? window
            : {};
          var BrowserMutationObserver = browserGlobal.MutationObserver || browserGlobal.WebKitMutationObserver;
          var local = typeof global !== "undefined"
            ? global
            : this === undefined
              ? window
              : this;
          function useNextTick() {
            return function() {
              process.nextTick(flush)
            }
          }
          function useMutationObserver() {
            var iterations = 0;
            var observer = new BrowserMutationObserver(flush);
            var node = document.createTextNode("");
            observer.observe(node, {characterData: true});
            return function() {
              node.data = iterations = ++iterations % 2
            }
          }
          function useSetTimeout() {
            return function() {
              local.setTimeout(flush, 1)
            }
          }
          var queue = [];
          function flush() {
            for (var i = 0; i < queue.length; i++) {
              var tuple = queue[i];
              var callback = tuple[0],
                arg = tuple[1];
              callback(arg)
            }
            queue = []
          }
          var scheduleFlush;
          if (typeof process !== "undefined" && {}.toString.call(process) === "[object process]") {
            scheduleFlush = useNextTick()
          } else if (BrowserMutationObserver) {
            scheduleFlush = useMutationObserver()
          } else {
            scheduleFlush = useSetTimeout()
          }
          function asap(callback, arg) {
            var length = queue.push([callback, arg]);
            if (length === 1) {
              scheduleFlush()
            }
          }
          exports.asap = asap
        }).call(this, require("_process"), typeof global !== "undefined"
          ? global
          : typeof self !== "undefined"
            ? self
            : typeof window !== "undefined"
              ? window
              : {})
      }, {
        _process: 4
      }
    ],
    8: [
      function(require, module, exports) {
        "use strict";
        function cast(object) {
          if (object && typeof object === "object" && object.constructor === this) {
            return object
          }
          var Promise = this;
          return new Promise(function(resolve) {
            resolve(object)
          })
        }
        exports.cast = cast
      }, {}
    ],
    9: [
      function(require, module, exports) {
        "use strict";
        var config = {
          instrument: false
        };
        function configure(name, value) {
          if (arguments.length === 2) {
            config[name] = value
          } else {
            return config[name]
          }
        }
        exports.config = config;
        exports.configure = configure
      }, {}
    ],
    10: [
      function(require, module, exports) {
        (function(global) {
          "use strict";
          var RSVPPromise = require("./promise").Promise;
          var isFunction = require("./utils").isFunction;
          function polyfill() {
            var local;
            if (typeof global !== "undefined") {
              local = global
            } else if (typeof window !== "undefined" && window.document) {
              local = window
            } else {
              local = self
            }
            var es6PromiseSupport = "Promise" in local && "cast" in local.Promise && "resolve" in local.Promise && "reject" in local.Promise && "all" in local.Promise && "race" in local.Promise && function() {
              var resolve;
              new local.Promise(function(r) {
                resolve = r
              });
              return isFunction(resolve)
            }();
            if (!es6PromiseSupport) {
              local.Promise = RSVPPromise
            }
          }
          exports.polyfill = polyfill
        }).call(this, typeof global !== "undefined"
          ? global
          : typeof self !== "undefined"
            ? self
            : typeof window !== "undefined"
              ? window
              : {})
      }, {
        "./promise": 11,
        "./utils": 15
      }
    ],
    11: [
      function(require, module, exports) {
        "use strict";
        var config = require("./config").config;
        var configure = require("./config").configure;
        var objectOrFunction = require("./utils").objectOrFunction;
        var isFunction = require("./utils").isFunction;
        var now = require("./utils").now;
        var cast = require("./cast").cast;
        var all = require("./all").all;
        var race = require("./race").race;
        var staticResolve = require("./resolve").resolve;
        var staticReject = require("./reject").reject;
        var asap = require("./asap").asap;
        var counter = 0;
        config.async = asap;
        function Promise(resolver) {
          if (!isFunction(resolver)) {
            throw new TypeError("You must pass a resolver function as the first argument to the promise constructor")
          }
          if (!(this instanceof Promise)) {
            throw new TypeError("Failed to construct 'Promise': Please use the 'new' operator, this object constructor cannot be called as a function.")
          }
          this._subscribers = [];
          invokeResolver(resolver, this)
        }
        function invokeResolver(resolver, promise) {
          function resolvePromise(value) {
            resolve(promise, value)
          }
          function rejectPromise(reason) {
            reject(promise, reason)
          }
          try {
            resolver(resolvePromise, rejectPromise)
          } catch (e) {
            rejectPromise(e)
          }
        }
        function invokeCallback(settled, promise, callback, detail) {
          var hasCallback = isFunction(callback),
            value,
            error,
            succeeded,
            failed;
          if (hasCallback) {
            try {
              value = callback(detail);
              succeeded = true
            } catch (e) {
              failed = true;
              error = e
            }
          } else {
            value = detail;
            succeeded = true
          }
          if (handleThenable(promise, value)) {
            return
          } else if (hasCallback && succeeded) {
            resolve(promise, value)
          } else if (failed) {
            reject(promise, error)
          } else if (settled === FULFILLED) {
            resolve(promise, value)
          } else if (settled === REJECTED) {
            reject(promise, value)
          }
        }
        var PENDING = void 0;
        var SEALED = 0;
        var FULFILLED = 1;
        var REJECTED = 2;
        function subscribe(parent, child, onFulfillment, onRejection) {
          var subscribers = parent._subscribers;
          var length = subscribers.length;
          subscribers[length] = child;
          subscribers[length + FULFILLED] = onFulfillment;
          subscribers[length + REJECTED] = onRejection
        }
        function publish(promise, settled) {
          var child,
            callback,
            subscribers = promise._subscribers,
            detail = promise._detail;
          for (var i = 0; i < subscribers.length; i += 3) {
            child = subscribers[i];
            callback = subscribers[i + settled];
            invokeCallback(settled, child, callback, detail)
          }
          promise._subscribers = null
        }
        Promise.prototype = {
          constructor: Promise,
          _state: undefined,
          _detail: undefined,
          _subscribers: undefined,
          then: function(onFulfillment, onRejection) {
            var promise = this;
            var thenPromise = new this.constructor(function() {});
            if (this._state) {
              var callbacks = arguments;
              config.async(function invokePromiseCallback() {
                invokeCallback(promise._state, thenPromise, callbacks[promise._state - 1], promise._detail)
              })
            } else {
              subscribe(this, thenPromise, onFulfillment, onRejection)
            }
            return thenPromise
          },
          "catch": function(onRejection) {
            return this.then(null, onRejection)
          }
        };
        Promise.all = all;
        Promise.cast = cast;
        Promise.race = race;
        Promise.resolve = staticResolve;
        Promise.reject = staticReject;
        function handleThenable(promise, value) {
          var then = null,
            resolved;
          try {
            if (promise === value) {
              throw new TypeError("A promises callback cannot return that same promise.")
            }
            if (objectOrFunction(value)) {
              then = value.then;
              if (isFunction(then)) {
                then.call(value, function(val) {
                  if (resolved) {
                    return true
                  }
                  resolved = true;
                  if (value !== val) {
                    resolve(promise, val)
                  } else {
                    fulfill(promise, val)
                  }
                }, function(val) {
                  if (resolved) {
                    return true
                  }
                  resolved = true;
                  reject(promise, val)
                });
                return true
              }
            }
          } catch (error) {
            if (resolved) {
              return true
            }
            reject(promise, error);
            return true
          }
          return false
        }
        function resolve(promise, value) {
          if (promise === value) {
            fulfill(promise, value)
          } else if (!handleThenable(promise, value)) {
            fulfill(promise, value)
          }
        }
        function fulfill(promise, value) {
          if (promise._state !== PENDING) {
            return
          }
          promise._state = SEALED;
          promise._detail = value;
          config.async(publishFulfillment, promise)
        }
        function reject(promise, reason) {
          if (promise._state !== PENDING) {
            return
          }
          promise._state = SEALED;
          promise._detail = reason;
          config.async(publishRejection, promise)
        }
        function publishFulfillment(promise) {
          publish(promise, promise._state = FULFILLED)
        }
        function publishRejection(promise) {
          publish(promise, promise._state = REJECTED)
        }
        exports.Promise = Promise
      }, {
        "./all": 6,
        "./asap": 7,
        "./cast": 8,
        "./config": 9,
        "./race": 12,
        "./reject": 13,
        "./resolve": 14,
        "./utils": 15
      }
    ],
    12: [
      function(require, module, exports) {
        "use strict";
        var isArray = require("./utils").isArray;
        function race(promises) {
          var Promise = this;
          if (!isArray(promises)) {
            throw new TypeError("You must pass an array to race.")
          }
          return new Promise(function(resolve, reject) {
            var results = [],
              promise;
            for (var i = 0; i < promises.length; i++) {
              promise = promises[i];
              if (promise && typeof promise.then === "function") {
                promise.then(resolve, reject)
              } else {
                resolve(promise)
              }
            }
          })
        }
        exports.race = race
      }, {
        "./utils": 15
      }
    ],
    13: [
      function(require, module, exports) {
        "use strict";
        function reject(reason) {
          var Promise = this;
          return new Promise(function(resolve, reject) {
            reject(reason)
          })
        }
        exports.reject = reject
      }, {}
    ],
    14: [
      function(require, module, exports) {
        "use strict";
        function resolve(value) {
          var Promise = this;
          return new Promise(function(resolve, reject) {
            resolve(value)
          })
        }
        exports.resolve = resolve
      }, {}
    ],
    15: [
      function(require, module, exports) {
        "use strict";
        function objectOrFunction(x) {
          return isFunction(x) || typeof x === "object" && x !== null
        }
        function isFunction(x) {
          return typeof x === "function"
        }
        function isArray(x) {
          return Object.prototype.toString.call(x) === "[object Array]"
        }
        var now = Date.now || function() {
          return (new Date).getTime()
        };
        exports.objectOrFunction = objectOrFunction;
        exports.isFunction = isFunction;
        exports.isArray = isArray;
        exports.now = now
      }, {}
    ],
    16: [
      function(require, module, exports) {
        var inserted = {};
        module.exports = function(css, options) {
          if (inserted[css])
            return;
          inserted[css] = true;
          var elem = document.createElement("style");
          elem.setAttribute("type", "text/css");
          if ("textContent" in elem) {
            elem.textContent = css
          } else {
            elem.styleSheet.cssText = css
          }
          var head = document.getElementsByTagName("head")[0];
          if (options && options.prepend) {
            head.insertBefore(elem, head.childNodes[0])
          } else {
            head.appendChild(elem)
          }
        }
      }, {}
    ],
    17: [
      function(require, module, exports) {
        (function(global, factory) {
          if (typeof module === "object" && typeof module.exports === "object") {
            module.exports = global.document
              ? factory(global, true)
              : function(w) {
                if (!w.document) {
                  throw new Error("jQuery requires a window with a document")
                }
                return factory(w)
              }
          } else {
            factory(global)
          }
        })(typeof window !== "undefined"
          ? window
          : this, function(window, noGlobal) {
          var deletedIds = [];
          var slice = deletedIds.slice;
          var concat = deletedIds.concat;
          var push = deletedIds.push;
          var indexOf = deletedIds.indexOf;
          var class2type = {};
          var toString = class2type.toString;
          var hasOwn = class2type.hasOwnProperty;
          var support = {};
          var version = "1.11.2",
            jQuery = function(selector, context) {
              return new jQuery.fn.init(selector, context)
            },
            rtrim = /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,
            rmsPrefix = /^-ms-/,
            rdashAlpha = /-([\da-z])/gi,
            fcamelCase = function(all, letter) {
              return letter.toUpperCase()
            };
          jQuery.fn = jQuery.prototype = {
            jquery: version,
            constructor: jQuery,
            selector: "",
            length: 0,
            toArray: function() {
              return slice.call(this)
            },
            get: function(num) {
              return num != null
                ? num < 0
                  ? this[num + this.length]
                  : this[num]
                : slice.call(this)
            },
            pushStack: function(elems) {
              var ret = jQuery.merge(this.constructor(), elems);
              ret.prevObject = this;
              ret.context = this.context;
              return ret
            },
            each: function(callback, args) {
              return jQuery.each(this, callback, args)
            },
            map: function(callback) {
              return this.pushStack(jQuery.map(this, function(elem, i) {
                return callback.call(elem, i, elem)
              }))
            },
            slice: function() {
              return this.pushStack(slice.apply(this, arguments))
            },
            first: function() {
              return this.eq(0)
            },
            last: function() {
              return this.eq(-1)
            },
            eq: function(i) {
              var len = this.length,
                j =+ i + (i < 0
                  ? len
                  : 0);
              return this.pushStack(j >= 0 && j < len
                ? [this[j]]
                : [])
            },
            end: function() {
              return this.prevObject || this.constructor(null)
            },
            push: push,
            sort: deletedIds.sort,
            splice: deletedIds.splice
          };
          jQuery.extend = jQuery.fn.extend = function() {
            var src,
              copyIsArray,
              copy,
              name,
              options,
              clone,
              target = arguments[0] || {},
              i = 1,
              length = arguments.length,
              deep = false;
            if (typeof target === "boolean") {
              deep = target;
              target = arguments[i] || {};
              i++
            }
            if (typeof target !== "object" && !jQuery.isFunction(target)) {
              target = {}
            }
            if (i === length) {
              target = this;
              i--
            }
            for (; i < length; i++) {
              if ((options = arguments[i]) != null) {
                for (name in options) {
                  src = target[name];
                  copy = options[name];
                  if (target === copy) {
                    continue
                  }
                  if (deep && copy && (jQuery.isPlainObject(copy) || (copyIsArray = jQuery.isArray(copy)))) {
                    if (copyIsArray) {
                      copyIsArray = false;
                      clone = src && jQuery.isArray(src)
                        ? src
                        : []
                    } else {
                      clone = src && jQuery.isPlainObject(src)
                        ? src
                        : {}
                    }
                    target[name] = jQuery.extend(deep, clone, copy)
                  } else if (copy !== undefined) {
                    target[name] = copy
                  }
                }
              }
            }
            return target
          };
          jQuery.extend({
            expando: "jQuery" + (version + Math.random()).replace(/\D/g, ""),
            isReady: true,
            error: function(msg) {
              throw new Error(msg)
            },
            noop: function() {},
            isFunction: function(obj) {
              return jQuery.type(obj) === "function"
            },
            isArray: Array.isArray || function(obj) {
              return jQuery.type(obj) === "array"
            },
            isWindow: function(obj) {
              return obj != null && obj == obj.window
            },
            isNumeric: function(obj) {
              return !jQuery.isArray(obj) && obj - parseFloat(obj) + 1 >= 0
            },
            isEmptyObject: function(obj) {
              var name;
              for (name in obj) {
                return false
              }
              return true
            },
            isPlainObject: function(obj) {
              var key;
              if (!obj || jQuery.type(obj) !== "object" || obj.nodeType || jQuery.isWindow(obj)) {
                return false
              }
              try {
                if (obj.constructor && !hasOwn.call(obj, "constructor") && !hasOwn.call(obj.constructor.prototype, "isPrototypeOf")) {
                  return false
                }
              } catch (e) {
                return false
              }
              if (support.ownLast) {
                for (key in obj) {
                  return hasOwn.call(obj, key)
                }
              }
              for (key in obj) {}
              return key === undefined || hasOwn.call(obj, key)
            },
            type: function(obj) {
              if (obj == null) {
                return obj + ""
              }
              return typeof obj === "object" || typeof obj === "function"
                ? class2type[toString.call(obj)] || "object"
                : typeof obj
            },
            globalEval: function(data) {
              if (data && jQuery.trim(data)) {
                (window.execScript || function(data) {
                  window["eval"].call(window, data)
                })(data)
              }
            },
            camelCase: function(string) {
              return string.replace(rmsPrefix, "ms-").replace(rdashAlpha, fcamelCase)
            },
            nodeName: function(elem, name) {
              return elem.nodeName && elem.nodeName.toLowerCase() === name.toLowerCase()
            },
            each: function(obj, callback, args) {
              var value,
                i = 0,
                length = obj.length,
                isArray = isArraylike(obj);
              if (args) {
                if (isArray) {
                  for (; i < length; i++) {
                    value = callback.apply(obj[i], args);
                    if (value === false) {
                      break
                    }
                  }
                } else {
                  for (i in obj) {
                    value = callback.apply(obj[i], args);
                    if (value === false) {
                      break
                    }
                  }
                }
              } else {
                if (isArray) {
                  for (; i < length; i++) {
                    value = callback.call(obj[i], i, obj[i]);
                    if (value === false) {
                      break
                    }
                  }
                } else {
                  for (i in obj) {
                    value = callback.call(obj[i], i, obj[i]);
                    if (value === false) {
                      break
                    }
                  }
                }
              }
              return obj
            },
            trim: function(text) {
              return text == null
                ? ""
                : (text + "").replace(rtrim, "")
            },
            makeArray: function(arr, results) {
              var ret = results || [];
              if (arr != null) {
                if (isArraylike(Object(arr))) {
                  jQuery.merge(ret, typeof arr === "string"
                    ? [arr]
                    : arr)
                } else {
                  push.call(ret, arr)
                }
              }
              return ret
            },
            inArray: function(elem, arr, i) {
              var len;
              if (arr) {
                if (indexOf) {
                  return indexOf.call(arr, elem, i)
                }
                len = arr.length;
                i = i
                  ? i < 0
                    ? Math.max(0, len + i)
                    : i
                  : 0;
                for (; i < len; i++) {
                  if (i in arr && arr[i] === elem) {
                    return i
                  }
                }
              }
              return -1
            },
            merge: function(first, second) {
              var len =+ second.length,
                j = 0,
                i = first.length;
              while (j < len) {
                first[i++] = second[j++]
              }
              if (len !== len) {
                while (second[j] !== undefined) {
                  first[i++] = second[j++]
                }
              }
              first.length = i;
              return first
            },
            grep: function(elems, callback, invert) {
              var callbackInverse,
                matches = [],
                i = 0,
                length = elems.length,
                callbackExpect = !invert;
              for (; i < length; i++) {
                callbackInverse = !callback(elems[i], i);
                if (callbackInverse !== callbackExpect) {
                  matches.push(elems[i])
                }
              }
              return matches
            },
            map: function(elems, callback, arg) {
              var value,
                i = 0,
                length = elems.length,
                isArray = isArraylike(elems),
                ret = [];
              if (isArray) {
                for (; i < length; i++) {
                  value = callback(elems[i], i, arg);
                  if (value != null) {
                    ret.push(value)
                  }
                }
              } else {
                for (i in elems) {
                  value = callback(elems[i], i, arg);
                  if (value != null) {
                    ret.push(value)
                  }
                }
              }
              return concat.apply([], ret)
            },
            guid: 1,
            proxy: function(fn, context) {
              var args,
                proxy,
                tmp;
              if (typeof context === "string") {
                tmp = fn[context];
                context = fn;
                fn = tmp
              }
              if (!jQuery.isFunction(fn)) {
                return undefined
              }
              args = slice.call(arguments, 2);
              proxy = function() {
                return fn.apply(context || this, args.concat(slice.call(arguments)))
              };
              proxy.guid = fn.guid = fn.guid || jQuery.guid++;
              return proxy
            },
            now: function() {
              return + new Date
            },
            support: support
          });
          jQuery.each("Boolean Number String Function Array Date RegExp Object Error".split(" "), function(i, name) {
            class2type["[object " + name + "]"] = name.toLowerCase()
          });
          function isArraylike(obj) {
            var length = obj.length,
              type = jQuery.type(obj);
            if (type === "function" || jQuery.isWindow(obj)) {
              return false
            }
            if (obj.nodeType === 1 && length) {
              return true
            }
            return type === "array" || length === 0 || typeof length === "number" && length > 0 && length - 1 in obj
          }
          var Sizzle = function(window) {
            var i,
              support,
              Expr,
              getText,
              isXML,
              tokenize,
              compile,
              select,
              outermostContext,
              sortInput,
              hasDuplicate,
              setDocument,
              document,
              docElem,
              documentIsHTML,
              rbuggyQSA,
              rbuggyMatches,
              matches,
              contains,
              expando = "sizzle" + 1 * new Date,
              preferredDoc = window.document,
              dirruns = 0,
              done = 0,
              classCache = createCache(),
              tokenCache = createCache(),
              compilerCache = createCache(),
              sortOrder = function(a, b) {
                if (a === b) {
                  hasDuplicate = true
                }
                return 0
              },
              MAX_NEGATIVE = 1 << 31,
              hasOwn = {}.hasOwnProperty,
              arr = [],
              pop = arr.pop,
              push_native = arr.push,
              push = arr.push,
              slice = arr.slice,
              indexOf = function(list, elem) {
                var i = 0,
                  len = list.length;
                for (; i < len; i++) {
                  if (list[i] === elem) {
                    return i
                  }
                }
                return -1
              },
              booleans = "checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|ismap|loop|multiple|open|readonly|required|scoped",
              whitespace = "[\\x20\\t\\r\\n\\f]",
              characterEncoding = "(?:\\\\.|[\\w-]|[^\\x00-\\xa0])+",
              identifier = characterEncoding.replace("w", "w#"),
              attributes = "\\[" + whitespace + "*(" + characterEncoding + ")(?:" + whitespace + "*([*^$|!~]?=)" + whitespace + "*(?:'((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\"|(" + identifier + "))|)" + whitespace + "*\\]",
              pseudos = ":(" + characterEncoding + ")(?:\\((" + "('((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\")|" + "((?:\\\\.|[^\\\\()[\\]]|" + attributes + ")*)|" + ".*" + ")\\)|)",
              rwhitespace = new RegExp(whitespace + "+", "g"),
              rtrim = new RegExp("^" + whitespace + "+|((?:^|[^\\\\])(?:\\\\.)*)" + whitespace + "+$", "g"),
              rcomma = new RegExp("^" + whitespace + "*," + whitespace + "*"),
              rcombinators = new RegExp("^" + whitespace + "*([>+~]|" + whitespace + ")" + whitespace + "*"),
              rattributeQuotes = new RegExp("=" + whitespace + "*([^\\]'\"]*?)" + whitespace + "*\\]", "g"),
              rpseudo = new RegExp(pseudos),
              ridentifier = new RegExp("^" + identifier + "$"),
              matchExpr = {
                ID: new RegExp("^#(" + characterEncoding + ")"),
                CLASS: new RegExp("^\\.(" + characterEncoding + ")"),
                TAG: new RegExp("^(" + characterEncoding.replace("w", "w*") + ")"),
                ATTR: new RegExp("^" + attributes),
                PSEUDO: new RegExp("^" + pseudos),
                CHILD: new RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\(" + whitespace + "*(even|odd|(([+-]|)(\\d*)n|)" + whitespace + "*(?:([+-]|)" + whitespace + "*(\\d+)|))" + whitespace + "*\\)|)", "i"),
                bool: new RegExp("^(?:" + booleans + ")$", "i"),
                needsContext: new RegExp("^" + whitespace + "*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\(" + whitespace + "*((?:-\\d)?\\d*)" + whitespace + "*\\)|)(?=[^-]|$)", "i")
              },
              rinputs = /^(?:input|select|textarea|button)$/i,
              rheader = /^h\d$/i,
              rnative = /^[^{]+\{\s*\[native \w/,
              rquickExpr = /^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,
              rsibling = /[+~]/,
              rescape = /'|\\/g,
              runescape = new RegExp("\\\\([\\da-f]{1,6}" + whitespace + "?|(" + whitespace + ")|.)", "ig"),
              funescape = function(_, escaped, escapedWhitespace) {
                var high = "0x" + escaped - 65536;
                return high !== high || escapedWhitespace
                  ? escaped
                  : high < 0
                    ? String.fromCharCode(high + 65536)
                    : String.fromCharCode(high >> 10 | 55296, high & 1023 | 56320)
              },
              unloadHandler = function() {
                setDocument()
              };
            try {
              push.apply(arr = slice.call(preferredDoc.childNodes), preferredDoc.childNodes);
              arr[preferredDoc.childNodes.length].nodeType
            } catch (e) {
              push = {
                apply: arr.length
                  ? function(target, els) {
                    push_native.apply(target, slice.call(els))
                  }
                  : function(target, els) {
                    var j = target.length,
                      i = 0;
                    while (target[j++] = els[i++]) {}
                    target.length = j - 1
                  }
              }
            }
            function Sizzle(selector, context, results, seed) {
              var match,
                elem,
                m,
                nodeType,
                i,
                groups,
                old,
                nid,
                newContext,
                newSelector;
              if ((context
                ? context.ownerDocument || context
                : preferredDoc) !== document) {
                setDocument(context)
              }
              context = context || document;
              results = results || [];
              nodeType = context.nodeType;
              if (typeof selector !== "string" || !selector || nodeType !== 1 && nodeType !== 9 && nodeType !== 11) {
                return results
              }
              if (!seed && documentIsHTML) {
                if (nodeType !== 11 && (match = rquickExpr.exec(selector))) {
                  if (m = match[1]) {
                    if (nodeType === 9) {
                      elem = context.getElementById(m);
                      if (elem && elem.parentNode) {
                        if (elem.id === m) {
                          results.push(elem);
                          return results
                        }
                      } else {
                        return results
                      }
                    } else {
                      if (context.ownerDocument && (elem = context.ownerDocument.getElementById(m)) && contains(context, elem) && elem.id === m) {
                        results.push(elem);
                        return results
                      }
                    }
                  } else if (match[2]) {
                    push.apply(results, context.getElementsByTagName(selector));
                    return results
                  } else if ((m = match[3]) && support.getElementsByClassName) {
                    push.apply(results, context.getElementsByClassName(m));
                    return results
                  }
                }
                if (support.qsa && (!rbuggyQSA || !rbuggyQSA.test(selector))) {
                  nid = old = expando;
                  newContext = context;
                  newSelector = nodeType !== 1 && selector;
                  if (nodeType === 1 && context.nodeName.toLowerCase() !== "object") {
                    groups = tokenize(selector);
                    if (old = context.getAttribute("id")) {
                      nid = old.replace(rescape, "\\$&")
                    } else {
                      context.setAttribute("id", nid)
                    }
                    nid = "[id='" + nid + "'] ";
                    i = groups.length;
                    while (i--) {
                      groups[i] = nid + toSelector(groups[i])
                    }
                    newContext = rsibling.test(selector) && testContext(context.parentNode) || context;
                    newSelector = groups.join(",")
                  }
                  if (newSelector) {
                    try {
                      push.apply(results, newContext.querySelectorAll(newSelector));
                      return results
                    } catch (qsaError) {} finally {
                      if (!old) {
                        context.removeAttribute("id")
                      }
                    }
                  }
                }
              }
              return select(selector.replace(rtrim, "$1"), context, results, seed)
            }
            function createCache() {
              var keys = [];
              function cache(key, value) {
                if (keys.push(key + " ") > Expr.cacheLength) {
                  delete cache[keys.shift()]
                }
                return cache[key + " "] = value
              }
              return cache
            }
            function markFunction(fn) {
              fn[expando] = true;
              return fn
            }
            function assert(fn) {
              var div = document.createElement("div");
              try {
                return !!fn(div)
              } catch (e) {
                return false
              } finally {
                if (div.parentNode) {
                  div.parentNode.removeChild(div)
                }
                div = null
              }
            }
            function addHandle(attrs, handler) {
              var arr = attrs.split("|"),
                i = attrs.length;
              while (i--) {
                Expr.attrHandle[arr[i]] = handler
              }
            }
            function siblingCheck(a, b) {
              var cur = b && a,
                diff = cur && a.nodeType === 1 && b.nodeType === 1 && (~ b.sourceIndex || MAX_NEGATIVE) - (~ a.sourceIndex || MAX_NEGATIVE);
              if (diff) {
                return diff
              }
              if (cur) {
                while (cur = cur.nextSibling) {
                  if (cur === b) {
                    return -1
                  }
                }
              }
              return a
                ? 1
                : -1
            }
            function createInputPseudo(type) {
              return function(elem) {
                var name = elem.nodeName.toLowerCase();
                return name === "input" && elem.type === type
              }
            }
            function createButtonPseudo(type) {
              return function(elem) {
                var name = elem.nodeName.toLowerCase();
                return (name === "input" || name === "button") && elem.type === type
              }
            }
            function createPositionalPseudo(fn) {
              return markFunction(function(argument) {
                argument =+ argument;
                return markFunction(function(seed, matches) {
                  var j,
                    matchIndexes = fn([], seed.length, argument),
                    i = matchIndexes.length;
                  while (i--) {
                    if (seed[j = matchIndexes[i]]) {
                      seed[j] = !(matches[j] = seed[j])
                    }
                  }
                })
              })
            }
            function testContext(context) {
              return context && typeof context.getElementsByTagName !== "undefined" && context
            }
            support = Sizzle.support = {};
            isXML = Sizzle.isXML = function(elem) {
              var documentElement = elem && (elem.ownerDocument || elem).documentElement;
              return documentElement
                ? documentElement.nodeName !== "HTML"
                : false
            };
            setDocument = Sizzle.setDocument = function(node) {
              var hasCompare,
                parent,
                doc = node
                  ? node.ownerDocument || node
                  : preferredDoc;
              if (doc === document || doc.nodeType !== 9 || !doc.documentElement) {
                return document
              }
              document = doc;
              docElem = doc.documentElement;
              parent = doc.defaultView;
              if (parent && parent !== parent.top) {
                if (parent.addEventListener) {
                  parent.addEventListener("unload", unloadHandler, false)
                } else if (parent.attachEvent) {
                  parent.attachEvent("onunload", unloadHandler)
                }
              }
              documentIsHTML = !isXML(doc);
              support.attributes = assert(function(div) {
                div.className = "i";
                return !div.getAttribute("className")
              });
              support.getElementsByTagName = assert(function(div) {
                div.appendChild(doc.createComment(""));
                return !div.getElementsByTagName("*").length
              });
              support.getElementsByClassName = rnative.test(doc.getElementsByClassName);
              support.getById = assert(function(div) {
                docElem.appendChild(div).id = expando;
                return !doc.getElementsByName || !doc.getElementsByName(expando).length
              });
              if (support.getById) {
                Expr.find["ID"] = function(id, context) {
                  if (typeof context.getElementById !== "undefined" && documentIsHTML) {
                    var m = context.getElementById(id);
                    return m && m.parentNode
                      ? [m]
                      : []
                  }
                };
                Expr.filter["ID"] = function(id) {
                  var attrId = id.replace(runescape, funescape);
                  return function(elem) {
                    return elem.getAttribute("id") === attrId
                  }
                }
              } else {
                delete Expr.find["ID"];
                Expr.filter["ID"] = function(id) {
                  var attrId = id.replace(runescape, funescape);
                  return function(elem) {
                    var node = typeof elem.getAttributeNode !== "undefined" && elem.getAttributeNode("id");
                    return node && node.value === attrId
                  }
                }
              }
              Expr.find["TAG"] = support.getElementsByTagName
                ? function(tag, context) {
                  if (typeof context.getElementsByTagName !== "undefined") {
                    return context.getElementsByTagName(tag)
                  } else if (support.qsa) {
                    return context.querySelectorAll(tag)
                  }
                }
                : function(tag, context) {
                  var elem,
                    tmp = [],
                    i = 0,
                    results = context.getElementsByTagName(tag);
                  if (tag === "*") {
                    while (elem = results[i++]) {
                      if (elem.nodeType === 1) {
                        tmp.push(elem)
                      }
                    }
                    return tmp
                  }
                  return results
                };
              Expr.find["CLASS"] = support.getElementsByClassName && function(className, context) {
                if (documentIsHTML) {
                  return context.getElementsByClassName(className)
                }
              };
              rbuggyMatches = [];
              rbuggyQSA = [];
              if (support.qsa = rnative.test(doc.querySelectorAll)) {
                assert(function(div) {
                  docElem.appendChild(div).innerHTML = "<a id='" + expando + "'></a>" + "<select id='" + expando + "-\f]' msallowcapture=''>" + "<option selected=''></option></select>";
                  if (div.querySelectorAll("[msallowcapture^='']").length) {
                    rbuggyQSA.push("[*^$]=" + whitespace + "*(?:''|\"\")")
                  }
                  if (!div.querySelectorAll("[selected]").length) {
                    rbuggyQSA.push("\\[" + whitespace + "*(?:value|" + booleans + ")")
                  }
                  if (!div.querySelectorAll("[id~=" + expando + "-]").length) {
                    rbuggyQSA.push("~=")
                  }
                  if (!div.querySelectorAll(":checked").length) {
                    rbuggyQSA.push(":checked")
                  }
                  if (!div.querySelectorAll("a#" + expando + "+*").length) {
                    rbuggyQSA.push(".#.+[+~]")
                  }
                });
                assert(function(div) {
                  var input = doc.createElement("input");
                  input.setAttribute("type", "hidden");
                  div.appendChild(input).setAttribute("name", "D");
                  if (div.querySelectorAll("[name=d]").length) {
                    rbuggyQSA.push("name" + whitespace + "*[*^$|!~]?=")
                  }
                  if (!div.querySelectorAll(":enabled").length) {
                    rbuggyQSA.push(":enabled", ":disabled")
                  }
                  div.querySelectorAll("*,:x");
                  rbuggyQSA.push(",.*:")
                })
              }
              if (support.matchesSelector = rnative.test(matches = docElem.matches || docElem.webkitMatchesSelector || docElem.mozMatchesSelector || docElem.oMatchesSelector || docElem.msMatchesSelector)) {
                assert(function(div) {
                  support.disconnectedMatch = matches.call(div, "div");
                  matches.call(div, "[s!='']:x");
                  rbuggyMatches.push("!=", pseudos)
                })
              }
              rbuggyQSA = rbuggyQSA.length && new RegExp(rbuggyQSA.join("|"));
              rbuggyMatches = rbuggyMatches.length && new RegExp(rbuggyMatches.join("|"));
              hasCompare = rnative.test(docElem.compareDocumentPosition);
              contains = hasCompare || rnative.test(docElem.contains)
                ? function(a, b) {
                  var adown = a.nodeType === 9
                      ? a.documentElement
                      : a,
                    bup = b && b.parentNode;
                  return a === bup || !!(bup && bup.nodeType === 1 && (adown.contains
                    ? adown.contains(bup)
                    : a.compareDocumentPosition && a.compareDocumentPosition(bup) & 16))
                }
                : function(a, b) {
                  if (b) {
                    while (b = b.parentNode) {
                      if (b === a) {
                        return true
                      }
                    }
                  }
                  return false
                };
              sortOrder = hasCompare
                ? function(a, b) {
                  if (a === b) {
                    hasDuplicate = true;
                    return 0
                  }
                  var compare = !a.compareDocumentPosition - !b.compareDocumentPosition;
                  if (compare) {
                    return compare
                  }
                  compare = (a.ownerDocument || a) === (b.ownerDocument || b)
                    ? a.compareDocumentPosition(b)
                    : 1;
                  if (compare & 1 || !support.sortDetached && b.compareDocumentPosition(a) === compare) {
                    if (a === doc || a.ownerDocument === preferredDoc && contains(preferredDoc, a)) {
                      return -1
                    }
                    if (b === doc || b.ownerDocument === preferredDoc && contains(preferredDoc, b)) {
                      return 1
                    }
                    return sortInput
                      ? indexOf(sortInput, a) - indexOf(sortInput, b)
                      : 0
                  }
                  return compare & 4
                    ? -1
                    : 1
                }
                : function(a, b) {
                  if (a === b) {
                    hasDuplicate = true;
                    return 0
                  }
                  var cur,
                    i = 0,
                    aup = a.parentNode,
                    bup = b.parentNode,
                    ap = [a],
                    bp = [b];
                  if (!aup || !bup) {
                    return a === doc
                      ? -1
                      : b === doc
                        ? 1
                        : aup
                          ? -1
                          : bup
                            ? 1
                            : sortInput
                              ? indexOf(sortInput, a) - indexOf(sortInput, b)
                              : 0
                  } else if (aup === bup) {
                    return siblingCheck(a, b)
                  }
                  cur = a;
                  while (cur = cur.parentNode) {
                    ap.unshift(cur)
                  }
                  cur = b;
                  while (cur = cur.parentNode) {
                    bp.unshift(cur)
                  }
                  while (ap[i] === bp[i]) {
                    i++
                  }
                  return i
                    ? siblingCheck(ap[i], bp[i])
                    : ap[i] === preferredDoc
                      ? -1
                      : bp[i] === preferredDoc
                        ? 1
                        : 0
                };
              return doc
            };
            Sizzle.matches = function(expr, elements) {
              return Sizzle(expr, null, null, elements)
            };
            Sizzle.matchesSelector = function(elem, expr) {
              if ((elem.ownerDocument || elem) !== document) {
                setDocument(elem)
              }
              expr = expr.replace(rattributeQuotes, "='$1']");
              if (support.matchesSelector && documentIsHTML && (!rbuggyMatches || !rbuggyMatches.test(expr)) && (!rbuggyQSA || !rbuggyQSA.test(expr))) {
                try {
                  var ret = matches.call(elem, expr);
                  if (ret || support.disconnectedMatch || elem.document && elem.document.nodeType !== 11) {
                    return ret
                  }
                } catch (e) {}
              }
              return Sizzle(expr, document, null, [elem]).length > 0
            };
            Sizzle.contains = function(context, elem) {
              if ((context.ownerDocument || context) !== document) {
                setDocument(context)
              }
              return contains(context, elem)
            };
            Sizzle.attr = function(elem, name) {
              if ((elem.ownerDocument || elem) !== document) {
                setDocument(elem)
              }
              var fn = Expr.attrHandle[name.toLowerCase()],
                val = fn && hasOwn.call(Expr.attrHandle, name.toLowerCase())
                  ? fn(elem, name, !documentIsHTML)
                  : undefined;
              return val !== undefined
                ? val
                : support.attributes || !documentIsHTML
                  ? elem.getAttribute(name)
                  : (val = elem.getAttributeNode(name)) && val.specified
                    ? val.value
                    : null
            };
            Sizzle.error = function(msg) {
              throw new Error("Syntax error, unrecognized expression: " + msg)
            };
            Sizzle.uniqueSort = function(results) {
              var elem,
                duplicates = [],
                j = 0,
                i = 0;
              hasDuplicate = !support.detectDuplicates;
              sortInput = !support.sortStable && results.slice(0);
              results.sort(sortOrder);
              if (hasDuplicate) {
                while (elem = results[i++]) {
                  if (elem === results[i]) {
                    j = duplicates.push(i)
                  }
                }
                while (j--) {
                  results.splice(duplicates[j], 1)
                }
              }
              sortInput = null;
              return results
            };
            getText = Sizzle.getText = function(elem) {
              var node,
                ret = "",
                i = 0,
                nodeType = elem.nodeType;
              if (!nodeType) {
                while (node = elem[i++]) {
                  ret += getText(node)
                }
              } else if (nodeType === 1 || nodeType === 9 || nodeType === 11) {
                if (typeof elem.textContent === "string") {
                  return elem.textContent
                } else {
                  for (elem = elem.firstChild; elem; elem = elem.nextSibling) {
                    ret += getText(elem)
                  }
                }
              } else if (nodeType === 3 || nodeType === 4) {
                return elem.nodeValue
              }
              return ret
            };
            Expr = Sizzle.selectors = {
              cacheLength: 50,
              createPseudo: markFunction,
              match: matchExpr,
              attrHandle: {},
              find: {},
              relative: {
                ">": {
                  dir: "parentNode",
                  first: true
                },
                " ": {
                  dir: "parentNode"
                },
                "+": {
                  dir: "previousSibling",
                  first: true
                },
                "~": {
                  dir: "previousSibling"
                }
              },
              preFilter: {
                ATTR: function(match) {
                  match[1] = match[1].replace(runescape, funescape);
                  match[3] = (match[3] || match[4] || match[5] || "").replace(runescape, funescape);
                  if (match[2] === "~=") {
                    match[3] = " " + match[3] + " "
                  }
                  return match.slice(0, 4)
                },
                CHILD: function(match) {
                  match[1] = match[1].toLowerCase();
                  if (match[1].slice(0, 3) === "nth") {
                    if (!match[3]) {
                      Sizzle.error(match[0])
                    }
                    match[4] =+ (match[4]
                      ? match[5] + (match[6] || 1)
                      : 2 * (match[3] === "even" || match[3] === "odd"));
                    match[5] =+ (match[7] + match[8] || match[3] === "odd")
                  } else if (match[3]) {
                    Sizzle.error(match[0])
                  }
                  return match
                },
                PSEUDO: function(match) {
                  var excess,
                    unquoted = !match[6] && match[2];
                  if (matchExpr["CHILD"].test(match[0])) {
                    return null
                  }
                  if (match[3]) {
                    match[2] = match[4] || match[5] || ""
                  } else if (unquoted && rpseudo.test(unquoted) && (excess = tokenize(unquoted, true)) && (excess = unquoted.indexOf(")", unquoted.length - excess) - unquoted.length)) {
                    match[0] = match[0].slice(0, excess);
                    match[2] = unquoted.slice(0, excess)
                  }
                  return match.slice(0, 3)
                }
              },
              filter: {
                TAG: function(nodeNameSelector) {
                  var nodeName = nodeNameSelector.replace(runescape, funescape).toLowerCase();
                  return nodeNameSelector === "*"
                    ? function() {
                      return true
                    }
                    : function(elem) {
                      return elem.nodeName && elem.nodeName.toLowerCase() === nodeName
                    }
                },
                CLASS: function(className) {
                  var pattern = classCache[className + " "];
                  return pattern || (pattern = new RegExp("(^|" + whitespace + ")" + className + "(" + whitespace + "|$)")) && classCache(className, function(elem) {
                    return pattern.test(typeof elem.className === "string" && elem.className || typeof elem.getAttribute !== "undefined" && elem.getAttribute("class") || "")
                  })
                },
                ATTR: function(name, operator, check) {
                  return function(elem) {
                    var result = Sizzle.attr(elem, name);
                    if (result == null) {
                      return operator === "!="
                    }
                    if (!operator) {
                      return true
                    }
                    result += "";
                    return operator === "="
                      ? result === check
                      : operator === "!="
                        ? result !== check
                        : operator === "^="
                          ? check && result.indexOf(check) === 0
                          : operator === "*="
                            ? check && result.indexOf(check) > -1
                            : operator === "$="
                              ? check && result.slice(-check.length) === check
                              : operator === "~="
                                ? (" " + result.replace(rwhitespace, " ") + " ").indexOf(check) > -1
                                : operator === "|="
                                  ? result === check || result.slice(0, check.length + 1) === check + "-"
                                  : false
                  }
                },
                CHILD: function(type, what, argument, first, last) {
                  var simple = type.slice(0, 3) !== "nth",
                    forward = type.slice(-4) !== "last",
                    ofType = what === "of-type";
                  return first === 1 && last === 0
                    ? function(elem) {
                      return !!elem.parentNode
                    }
                    : function(elem, context, xml) {
                      var cache,
                        outerCache,
                        node,
                        diff,
                        nodeIndex,
                        start,
                        dir = simple !== forward
                          ? "nextSibling"
                          : "previousSibling",
                        parent = elem.parentNode,
                        name = ofType && elem.nodeName.toLowerCase(),
                        useCache = !xml && !ofType;
                      if (parent) {
                        if (simple) {
                          while (dir) {
                            node = elem;
                            while (node = node[dir]) {
                              if (ofType
                                ? node.nodeName.toLowerCase() === name
                                : node.nodeType === 1) {
                                return false
                              }
                            }
                            start = dir = type === "only" && !start && "nextSibling"
                          }
                          return true
                        }
                        start = [forward
                            ? parent.firstChild
                            : parent.lastChild];
                        if (forward && useCache) {
                          outerCache = parent[expando] || (parent[expando] = {});
                          cache = outerCache[type] || [];
                          nodeIndex = cache[0] === dirruns && cache[1];
                          diff = cache[0] === dirruns && cache[2];
                          node = nodeIndex && parent.childNodes[nodeIndex];
                          while (node = ++nodeIndex && node && node[dir] || (diff = nodeIndex = 0) || start.pop()) {
                            if (node.nodeType === 1 && ++diff && node === elem) {
                              outerCache[type] = [dirruns, nodeIndex, diff];
                              break
                            }
                          }
                        } else if (useCache && (cache = (elem[expando] || (elem[expando] = {}))[type]) && cache[0] === dirruns) {
                          diff = cache[1]
                        } else {
                          while (node = ++nodeIndex && node && node[dir] || (diff = nodeIndex = 0) || start.pop()) {
                            if ((ofType
                              ? node.nodeName.toLowerCase() === name
                              : node.nodeType === 1) && ++diff) {
                              if (useCache) {
                                (node[expando] || (node[expando] = {}))[type] = [dirruns, diff]
                              }
                              if (node === elem) {
                                break
                              }
                            }
                          }
                        }
                        diff -= last;
                        return diff === first || diff % first === 0 && diff / first >= 0
                      }
                    }
                },
                PSEUDO: function(pseudo, argument) {
                  var args,
                    fn = Expr.pseudos[pseudo] || Expr.setFilters[pseudo.toLowerCase()] || Sizzle.error("unsupported pseudo: " + pseudo);
                  if (fn[expando]) {
                    return fn(argument)
                  }
                  if (fn.length > 1) {
                    args = [pseudo, pseudo, "", argument];
                    return Expr.setFilters.hasOwnProperty(pseudo.toLowerCase())
                      ? markFunction(function(seed, matches) {
                        var idx,
                          matched = fn(seed, argument),
                          i = matched.length;
                        while (i--) {
                          idx = indexOf(seed, matched[i]);
                          seed[idx] = !(matches[idx] = matched[i])
                        }
                      })
                      : function(elem) {
                        return fn(elem, 0, args)
                      }
                  }
                  return fn
                }
              },
              pseudos: {
                not: markFunction(function(selector) {
                  var input = [],
                    results = [],
                    matcher = compile(selector.replace(rtrim, "$1"));
                  return matcher[expando]
                    ? markFunction(function(seed, matches, context, xml) {
                      var elem,
                        unmatched = matcher(seed, null, xml, []),
                        i = seed.length;
                      while (i--) {
                        if (elem = unmatched[i]) {
                          seed[i] = !(matches[i] = elem)
                        }
                      }
                    })
                    : function(elem, context, xml) {
                      input[0] = elem;
                      matcher(input, null, xml, results);
                      input[0] = null;
                      return !results.pop()
                    }
                }),
                has: markFunction(function(selector) {
                  return function(elem) {
                    return Sizzle(selector, elem).length > 0
                  }
                }),
                contains: markFunction(function(text) {
                  text = text.replace(runescape, funescape);
                  return function(elem) {
                    return (elem.textContent || elem.innerText || getText(elem)).indexOf(text) > -1
                  }
                }),
                lang: markFunction(function(lang) {
                  if (!ridentifier.test(lang || "")) {
                    Sizzle.error("unsupported lang: " + lang)
                  }
                  lang = lang.replace(runescape, funescape).toLowerCase();
                  return function(elem) {
                    var elemLang;
                    do
                      {
                        if(elemLang = documentIsHTML
                          ? elem.lang
                          : elem.getAttribute("xml:lang") || elem.getAttribute("lang")) {
                          elemLang = elemLang.toLowerCase();
                          return elemLang === lang || elemLang.indexOf(lang + "-") === 0
                        }
                      } while ((elem = elem.parentNode) && elem.nodeType === 1);
                    return false
                  }
                }),
                target: function(elem) {
                  var hash = window.location && window.location.hash;
                  return hash && hash.slice(1) === elem.id
                },
                root: function(elem) {
                  return elem === docElem
                },
                focus: function(elem) {
                  return elem === document.activeElement && (!document.hasFocus || document.hasFocus()) && !!(elem.type || elem.href ||~ elem.tabIndex)
                },
                enabled: function(elem) {
                  return elem.disabled === false
                },
                disabled: function(elem) {
                  return elem.disabled === true
                },
                checked: function(elem) {
                  var nodeName = elem.nodeName.toLowerCase();
                  return nodeName === "input" && !!elem.checked || nodeName === "option" && !!elem.selected
                },
                selected: function(elem) {
                  if (elem.parentNode) {
                    elem.parentNode.selectedIndex
                  }
                  return elem.selected === true
                },
                empty: function(elem) {
                  for (elem = elem.firstChild; elem; elem = elem.nextSibling) {
                    if (elem.nodeType < 6) {
                      return false
                    }
                  }
                  return true
                },
                parent: function(elem) {
                  return !Expr.pseudos["empty"](elem)
                },
                header: function(elem) {
                  return rheader.test(elem.nodeName)
                },
                input: function(elem) {
                  return rinputs.test(elem.nodeName)
                },
                button: function(elem) {
                  var name = elem.nodeName.toLowerCase();
                  return name === "input" && elem.type === "button" || name === "button"
                },
                text: function(elem) {
                  var attr;
                  return elem.nodeName.toLowerCase() === "input" && elem.type === "text" && ((attr = elem.getAttribute("type")) == null || attr.toLowerCase() === "text")
                },
                first: createPositionalPseudo(function() {
                  return [0]
                }),
                last: createPositionalPseudo(function(matchIndexes, length) {
                  return [length - 1]
                }),
                eq: createPositionalPseudo(function(matchIndexes, length, argument) {
                  return [argument < 0
                      ? argument + length
                      : argument]
                }),
                even: createPositionalPseudo(function(matchIndexes, length) {
                  var i = 0;
                  for (; i < length; i += 2) {
                    matchIndexes.push(i)
                  }
                  return matchIndexes
                }),
                odd: createPositionalPseudo(function(matchIndexes, length) {
                  var i = 1;
                  for (; i < length; i += 2) {
                    matchIndexes.push(i)
                  }
                  return matchIndexes
                }),
                lt: createPositionalPseudo(function(matchIndexes, length, argument) {
                  var i = argument < 0
                    ? argument + length
                    : argument;
                  for (; --i >= 0;) {
                    matchIndexes.push(i)
                  }
                  return matchIndexes
                }),
                gt: createPositionalPseudo(function(matchIndexes, length, argument) {
                  var i = argument < 0
                    ? argument + length
                    : argument;
                  for (; ++i < length;) {
                    matchIndexes.push(i)
                  }
                  return matchIndexes
                })
              }
            };
            Expr.pseudos["nth"] = Expr.pseudos["eq"];
            for (i in {radio: true, checkbox: true, file: true, password: true, image: true}) {
              Expr.pseudos[i] = createInputPseudo(i)
            }
            for (i in {submit: true, reset: true}) {
              Expr.pseudos[i] = createButtonPseudo(i)
            }
            function setFilters() {}
            setFilters.prototype = Expr.filters = Expr.pseudos;
            Expr.setFilters = new setFilters;
            tokenize = Sizzle.tokenize = function(selector, parseOnly) {
              var matched,
                match,
                tokens,
                type,
                soFar,
                groups,
                preFilters,
                cached = tokenCache[selector + " "];
              if (cached) {
                return parseOnly
                  ? 0
                  : cached.slice(0)
              }
              soFar = selector;
              groups = [];
              preFilters = Expr.preFilter;
              while (soFar) {
                if (!matched || (match = rcomma.exec(soFar))) {
                  if (match) {
                    soFar = soFar.slice(match[0].length) || soFar
                  }
                  groups.push(tokens = [])
                }
                matched = false;
                if (match = rcombinators.exec(soFar)) {
                  matched = match.shift();
                  tokens.push({
                    value: matched,
                    type: match[0].replace(rtrim, " ")
                  });
                  soFar = soFar.slice(matched.length)
                }
                for (type in Expr.filter) {
                  if ((match = matchExpr[type].exec(soFar)) && (!preFilters[type] || (match = preFilters[type](match)))) {
                    matched = match.shift();
                    tokens.push({value: matched, type: type, matches: match});
                    soFar = soFar.slice(matched.length)
                  }
                }
                if (!matched) {
                  break
                }
              }
              return parseOnly
                ? soFar.length
                : soFar
                  ? Sizzle.error(selector)
                  : tokenCache(selector, groups).slice(0)
            };
            function toSelector(tokens) {
              var i = 0,
                len = tokens.length,
                selector = "";
              for (; i < len; i++) {
                selector += tokens[i].value
              }
              return selector
            }
            function addCombinator(matcher, combinator, base) {
              var dir = combinator.dir,
                checkNonElements = base && dir === "parentNode",
                doneName = done++;
              return combinator.first
                ? function(elem, context, xml) {
                  while (elem = elem[dir]) {
                    if (elem.nodeType === 1 || checkNonElements) {
                      return matcher(elem, context, xml)
                    }
                  }
                }
                : function(elem, context, xml) {
                  var oldCache,
                    outerCache,
                    newCache = [dirruns, doneName];
                  if (xml) {
                    while (elem = elem[dir]) {
                      if (elem.nodeType === 1 || checkNonElements) {
                        if (matcher(elem, context, xml)) {
                          return true
                        }
                      }
                    }
                  } else {
                    while (elem = elem[dir]) {
                      if (elem.nodeType === 1 || checkNonElements) {
                        outerCache = elem[expando] || (elem[expando] = {});
                        if ((oldCache = outerCache[dir]) && oldCache[0] === dirruns && oldCache[1] === doneName) {
                          return newCache[2] = oldCache[2]
                        } else {
                          outerCache[dir] = newCache;
                          if (newCache[2] = matcher(elem, context, xml)) {
                            return true
                          }
                        }
                      }
                    }
                  }
                }
            }
            function elementMatcher(matchers) {
              return matchers.length > 1
                ? function(elem, context, xml) {
                  var i = matchers.length;
                  while (i--) {
                    if (!matchers[i](elem, context, xml)) {
                      return false
                    }
                  }
                  return true
                }
                : matchers[0]
            }
            function multipleContexts(selector, contexts, results) {
              var i = 0,
                len = contexts.length;
              for (; i < len; i++) {
                Sizzle(selector, contexts[i], results)
              }
              return results
            }
            function condense(unmatched, map, filter, context, xml) {
              var elem,
                newUnmatched = [],
                i = 0,
                len = unmatched.length,
                mapped = map != null;
              for (; i < len; i++) {
                if (elem = unmatched[i]) {
                  if (!filter || filter(elem, context, xml)) {
                    newUnmatched.push(elem);
                    if (mapped) {
                      map.push(i)
                    }
                  }
                }
              }
              return newUnmatched
            }
            function setMatcher(preFilter, selector, matcher, postFilter, postFinder, postSelector) {
              if (postFilter && !postFilter[expando]) {
                postFilter = setMatcher(postFilter)
              }
              if (postFinder && !postFinder[expando]) {
                postFinder = setMatcher(postFinder, postSelector)
              }
              return markFunction(function(seed, results, context, xml) {
                var temp,
                  i,
                  elem,
                  preMap = [],
                  postMap = [],
                  preexisting = results.length,
                  elems = seed || multipleContexts(selector || "*", context.nodeType
                    ? [context]
                    : context, []),
                  matcherIn = preFilter && (seed || !selector)
                    ? condense(elems, preMap, preFilter, context, xml)
                    : elems,
                  matcherOut = matcher
                    ? postFinder || (seed
                      ? preFilter
                      : preexisting || postFilter)
                      ? []
                      : results
                    : matcherIn;
                if (matcher) {
                  matcher(matcherIn, matcherOut, context, xml)
                }
                if (postFilter) {
                  temp = condense(matcherOut, postMap);
                  postFilter(temp, [], context, xml);
                  i = temp.length;
                  while (i--) {
                    if (elem = temp[i]) {
                      matcherOut[postMap[i]] = !(matcherIn[postMap[i]] = elem)
                    }
                  }
                }
                if (seed) {
                  if (postFinder || preFilter) {
                    if (postFinder) {
                      temp = [];
                      i = matcherOut.length;
                      while (i--) {
                        if (elem = matcherOut[i]) {
                          temp.push(matcherIn[i] = elem)
                        }
                      }
                      postFinder(null, matcherOut = [], temp, xml)
                    }
                    i = matcherOut.length;
                    while (i--) {
                      if ((elem = matcherOut[i]) && (temp = postFinder
                        ? indexOf(seed, elem)
                        : preMap[i]) > -1) {
                        seed[temp] = !(results[temp] = elem)
                      }
                    }
                  }
                } else {
                  matcherOut = condense(matcherOut === results
                    ? matcherOut.splice(preexisting, matcherOut.length)
                    : matcherOut);
                  if (postFinder) {
                    postFinder(null, results, matcherOut, xml)
                  } else {
                    push.apply(results, matcherOut)
                  }
                }
              })
            }
            function matcherFromTokens(tokens) {
              var checkContext,
                matcher,
                j,
                len = tokens.length,
                leadingRelative = Expr.relative[tokens[0].type],
                implicitRelative = leadingRelative || Expr.relative[" "],
                i = leadingRelative
                  ? 1
                  : 0,
                matchContext = addCombinator(function(elem) {
                  return elem === checkContext
                }, implicitRelative, true),
                matchAnyContext = addCombinator(function(elem) {
                  return indexOf(checkContext, elem) > -1
                }, implicitRelative, true),
                matchers = [function(elem, context, xml) {
                    var ret = !leadingRelative && (xml || context !== outermostContext) || ((checkContext = context).nodeType
                      ? matchContext(elem, context, xml)
                      : matchAnyContext(elem, context, xml));
                    checkContext = null;
                    return ret
                  }
                ];
              for (; i < len; i++) {
                if (matcher = Expr.relative[tokens[i].type]) {
                  matchers = [addCombinator(elementMatcher(matchers), matcher)]
                } else {
                  matcher = Expr.filter[tokens[i].type].apply(null, tokens[i].matches);
                  if (matcher[expando]) {
                    j = ++i;
                    for (; j < len; j++) {
                      if (Expr.relative[tokens[j].type]) {
                        break
                      }
                    }
                    return setMatcher(i > 1 && elementMatcher(matchers), i > 1 && toSelector(tokens.slice(0, i - 1).concat({
                      value: tokens[i - 2].type === " "
                        ? "*"
                        : ""
                    })).replace(rtrim, "$1"), matcher, i < j && matcherFromTokens(tokens.slice(i, j)), j < len && matcherFromTokens(tokens = tokens.slice(j)), j < len && toSelector(tokens))
                  }
                  matchers.push(matcher)
                }
              }
              return elementMatcher(matchers)
            }
            function matcherFromGroupMatchers(elementMatchers, setMatchers) {
              var bySet = setMatchers.length > 0,
                byElement = elementMatchers.length > 0,
                superMatcher = function(seed, context, xml, results, outermost) {
                  var elem,
                    j,
                    matcher,
                    matchedCount = 0,
                    i = "0",
                    unmatched = seed && [],
                    setMatched = [],
                    contextBackup = outermostContext,
                    elems = seed || byElement && Expr.find["TAG"]("*", outermost),
                    dirrunsUnique = dirruns += contextBackup == null
                      ? 1
                      : Math.random() || .1,
                    len = elems.length;
                  if (outermost) {
                    outermostContext = context !== document && context
                  }
                  for (; i !== len && (elem = elems[i]) != null; i++) {
                    if (byElement && elem) {
                      j = 0;
                      while (matcher = elementMatchers[j++]) {
                        if (matcher(elem, context, xml)) {
                          results.push(elem);
                          break
                        }
                      }
                      if (outermost) {
                        dirruns = dirrunsUnique
                      }
                    }
                    if (bySet) {
                      if (elem = !matcher && elem) {
                        matchedCount--
                      }
                      if (seed) {
                        unmatched.push(elem)
                      }
                    }
                  }
                  matchedCount += i;
                  if (bySet && i !== matchedCount) {
                    j = 0;
                    while (matcher = setMatchers[j++]) {
                      matcher(unmatched, setMatched, context, xml)
                    }
                    if (seed) {
                      if (matchedCount > 0) {
                        while (i--) {
                          if (!(unmatched[i] || setMatched[i])) {
                            setMatched[i] = pop.call(results)
                          }
                        }
                      }
                      setMatched = condense(setMatched)
                    }
                    push.apply(results, setMatched);
                    if (outermost && !seed && setMatched.length > 0 && matchedCount + setMatchers.length > 1) {
                      Sizzle.uniqueSort(results)
                    }
                  }
                  if (outermost) {
                    dirruns = dirrunsUnique;
                    outermostContext = contextBackup
                  }
                  return unmatched
                };
              return bySet
                ? markFunction(superMatcher)
                : superMatcher
            }
            compile = Sizzle.compile = function(selector, match) {
              var i,
                setMatchers = [],
                elementMatchers = [],
                cached = compilerCache[selector + " "];
              if (!cached) {
                if (!match) {
                  match = tokenize(selector)
                }
                i = match.length;
                while (i--) {
                  cached = matcherFromTokens(match[i]);
                  if (cached[expando]) {
                    setMatchers.push(cached)
                  } else {
                    elementMatchers.push(cached)
                  }
                }
                cached = compilerCache(selector, matcherFromGroupMatchers(elementMatchers, setMatchers));
                cached.selector = selector
              }
              return cached
            };
            select = Sizzle.select = function(selector, context, results, seed) {
              var i,
                tokens,
                token,
                type,
                find,
                compiled = typeof selector === "function" && selector,
                match = !seed && tokenize(selector = compiled.selector || selector);
              results = results || [];
              if (match.length === 1) {
                tokens = match[0] = match[0].slice(0);
                if (tokens.length > 2 && (token = tokens[0]).type === "ID" && support.getById && context.nodeType === 9 && documentIsHTML && Expr.relative[tokens[1].type]) {
                  context = (Expr.find["ID"](token.matches[0].replace(runescape, funescape), context) || [])[0];
                  if (!context) {
                    return results
                  } else if (compiled) {
                    context = context.parentNode
                  }
                  selector = selector.slice(tokens.shift().value.length)
                }
                i = matchExpr["needsContext"].test(selector)
                  ? 0
                  : tokens.length;
                while (i--) {
                  token = tokens[i];
                  if (Expr.relative[type = token.type]) {
                    break
                  }
                  if (find = Expr.find[type]) {
                    if (seed = find(token.matches[0].replace(runescape, funescape), rsibling.test(tokens[0].type) && testContext(context.parentNode) || context)) {
                      tokens.splice(i, 1);
                      selector = seed.length && toSelector(tokens);
                      if (!selector) {
                        push.apply(results, seed);
                        return results
                      }
                      break
                    }
                  }
                }
              }
              (compiled || compile(selector, match))(seed, context, !documentIsHTML, results, rsibling.test(selector) && testContext(context.parentNode) || context);
              return results
            };
            support.sortStable = expando.split("").sort(sortOrder).join("") === expando;
            support.detectDuplicates = !!hasDuplicate;
            setDocument();
            support.sortDetached = assert(function(div1) {
              return div1.compareDocumentPosition(document.createElement("div")) & 1
            });
            if (!assert(function(div) {
              div.innerHTML = "<a href='#'></a>";
              return div.firstChild.getAttribute("href") === "#"
            })) {
              addHandle("type|href|height|width", function(elem, name, isXML) {
                if (!isXML) {
                  return elem.getAttribute(name, name.toLowerCase() === "type"
                    ? 1
                    : 2)
                }
              })
            }
            if (!support.attributes || !assert(function(div) {
              div.innerHTML = "<input/>";
              div.firstChild.setAttribute("value", "");
              return div.firstChild.getAttribute("value") === ""
            })) {
              addHandle("value", function(elem, name, isXML) {
                if (!isXML && elem.nodeName.toLowerCase() === "input") {
                  return elem.defaultValue
                }
              })
            }
            if (!assert(function(div) {
              return div.getAttribute("disabled") == null
            })) {
              addHandle(booleans, function(elem, name, isXML) {
                var val;
                if (!isXML) {
                  return elem[name] === true
                    ? name.toLowerCase()
                    : (val = elem.getAttributeNode(name)) && val.specified
                      ? val.value
                      : null
                }
              })
            }
            return Sizzle
          }(window);
          jQuery.find = Sizzle;
          jQuery.expr = Sizzle.selectors;
          jQuery.expr[":"] = jQuery.expr.pseudos;
          jQuery.unique = Sizzle.uniqueSort;
          jQuery.text = Sizzle.getText;
          jQuery.isXMLDoc = Sizzle.isXML;
          jQuery.contains = Sizzle.contains;
          var rneedsContext = jQuery.expr.match.needsContext;
          var rsingleTag = /^<(\w+)\s*\/?>(?:<\/\1>|)$/;
          var risSimple = /^.[^:#\[\.,]*$/;
          function winnow(elements, qualifier, not) {
            if (jQuery.isFunction(qualifier)) {
              return jQuery.grep(elements, function(elem, i) {
                return !!qualifier.call(elem, i, elem) !== not
              })
            }
            if (qualifier.nodeType) {
              return jQuery.grep(elements, function(elem) {
                return elem === qualifier !== not
              })
            }
            if (typeof qualifier === "string") {
              if (risSimple.test(qualifier)) {
                return jQuery.filter(qualifier, elements, not)
              }
              qualifier = jQuery.filter(qualifier, elements)
            }
            return jQuery.grep(elements, function(elem) {
              return jQuery.inArray(elem, qualifier) >= 0 !== not
            })
          }
          jQuery.filter = function(expr, elems, not) {
            var elem = elems[0];
            if (not) {
              expr = ":not(" + expr + ")"
            }
            return elems.length === 1 && elem.nodeType === 1
              ? jQuery.find.matchesSelector(elem, expr)
                ? [elem]
                : []
              : jQuery.find.matches(expr, jQuery.grep(elems, function(elem) {
                return elem.nodeType === 1
              }))
          };
          jQuery.fn.extend({
            find: function(selector) {
              var i,
                ret = [],
                self = this,
                len = self.length;
              if (typeof selector !== "string") {
                return this.pushStack(jQuery(selector).filter(function() {
                  for (i = 0; i < len; i++) {
                    if (jQuery.contains(self[i], this)) {
                      return true
                    }
                  }
                }))
              }
              for (i = 0; i < len; i++) {
                jQuery.find(selector, self[i], ret)
              }
              ret = this.pushStack(len > 1
                ? jQuery.unique(ret)
                : ret);
              ret.selector = this.selector
                ? this.selector + " " + selector
                : selector;
              return ret
            },
            filter: function(selector) {
              return this.pushStack(winnow(this, selector || [], false))
            },
            not: function(selector) {
              return this.pushStack(winnow(this, selector || [], true))
            },
            is: function(selector) {
              return !!winnow(this, typeof selector === "string" && rneedsContext.test(selector)
                ? jQuery(selector)
                : selector || [], false).length
            }
          });
          var rootjQuery,
            document = window.document,
            rquickExpr = /^(?:\s*(<[\w\W]+>)[^>]*|#([\w-]*))$/,
            init = jQuery.fn.init = function(selector, context) {
              var match,
                elem;
              if (!selector) {
                return this
              }
              if (typeof selector === "string") {
                if (selector.charAt(0) === "<" && selector.charAt(selector.length - 1) === ">" && selector.length >= 3) {
                  match = [null, selector, null]
                } else {
                  match = rquickExpr.exec(selector)
                }
                if (match && (match[1] || !context)) {
                  if (match[1]) {
                    context = context instanceof jQuery
                      ? context[0]
                      : context;
                    jQuery.merge(this, jQuery.parseHTML(match[1], context && context.nodeType
                      ? context.ownerDocument || context
                      : document, true));
                    if (rsingleTag.test(match[1]) && jQuery.isPlainObject(context)) {
                      for (match in context) {
                        if (jQuery.isFunction(this[match])) {
                          this[match](context[match])
                        } else {
                          this.attr(match, context[match])
                        }
                      }
                    }
                    return this
                  } else {
                    elem = document.getElementById(match[2]);
                    if (elem && elem.parentNode) {
                      if (elem.id !== match[2]) {
                        return rootjQuery.find(selector)
                      }
                      this.length = 1;
                      this[0] = elem
                    }
                    this.context = document;
                    this.selector = selector;
                    return this
                  }
                } else if (!context || context.jquery) {
                  return (context || rootjQuery).find(selector)
                } else {
                  return this.constructor(context).find(selector)
                }
              } else if (selector.nodeType) {
                this.context = this[0] = selector;
                this.length = 1;
                return this
              } else if (jQuery.isFunction(selector)) {
                return typeof rootjQuery.ready !== "undefined"
                  ? rootjQuery.ready(selector)
                  : selector(jQuery)
              }
              if (selector.selector !== undefined) {
                this.selector = selector.selector;
                this.context = selector.context
              }
              return jQuery.makeArray(selector, this)
            };
          init.prototype = jQuery.fn;
          rootjQuery = jQuery(document);
          var rparentsprev = /^(?:parents|prev(?:Until|All))/,
            guaranteedUnique = {
              children: true,
              contents: true,
              next: true,
              prev: true
            };
          jQuery.extend({
            dir: function(elem, dir, until) {
              var matched = [],
                cur = elem[dir];
              while (cur && cur.nodeType !== 9 && (until === undefined || cur.nodeType !== 1 || !jQuery(cur).is(until))) {
                if (cur.nodeType === 1) {
                  matched.push(cur)
                }
                cur = cur[dir]
              }
              return matched
            },
            sibling: function(n, elem) {
              var r = [];
              for (; n; n = n.nextSibling) {
                if (n.nodeType === 1 && n !== elem) {
                  r.push(n)
                }
              }
              return r
            }
          });
          jQuery.fn.extend({
            has: function(target) {
              var i,
                targets = jQuery(target, this),
                len = targets.length;
              return this.filter(function() {
                for (i = 0; i < len; i++) {
                  if (jQuery.contains(this, targets[i])) {
                    return true
                  }
                }
              })
            },
            closest: function(selectors, context) {
              var cur,
                i = 0,
                l = this.length,
                matched = [],
                pos = rneedsContext.test(selectors) || typeof selectors !== "string"
                  ? jQuery(selectors, context || this.context)
                  : 0;
              for (; i < l; i++) {
                for (cur = this[i]; cur && cur !== context; cur = cur.parentNode) {
                  if (cur.nodeType < 11 && (pos
                    ? pos.index(cur) > -1
                    : cur.nodeType === 1 && jQuery.find.matchesSelector(cur, selectors))) {
                    matched.push(cur);
                    break
                  }
                }
              }
              return this.pushStack(matched.length > 1
                ? jQuery.unique(matched)
                : matched)
            },
            index: function(elem) {
              if (!elem) {
                return this[0] && this[0].parentNode
                  ? this.first().prevAll().length
                  : -1
              }
              if (typeof elem === "string") {
                return jQuery.inArray(this[0], jQuery(elem))
              }
              return jQuery.inArray(elem.jquery
                ? elem[0]
                : elem, this)
            },
            add: function(selector, context) {
              return this.pushStack(jQuery.unique(jQuery.merge(this.get(), jQuery(selector, context))))
            },
            addBack: function(selector) {
              return this.add(selector == null
                ? this.prevObject
                : this.prevObject.filter(selector))
            }
          });
          function sibling(cur, dir) {
            do
              {
                cur = cur[dir]
              }
            while (cur && cur.nodeType !== 1);
            return cur
          }
          jQuery.each({
            parent: function(elem) {
              var parent = elem.parentNode;
              return parent && parent.nodeType !== 11
                ? parent
                : null
            },
            parents: function(elem) {
              return jQuery.dir(elem, "parentNode")
            },
            parentsUntil: function(elem, i, until) {
              return jQuery.dir(elem, "parentNode", until)
            },
            next: function(elem) {
              return sibling(elem, "nextSibling")
            },
            prev: function(elem) {
              return sibling(elem, "previousSibling")
            },
            nextAll: function(elem) {
              return jQuery.dir(elem, "nextSibling")
            },
            prevAll: function(elem) {
              return jQuery.dir(elem, "previousSibling")
            },
            nextUntil: function(elem, i, until) {
              return jQuery.dir(elem, "nextSibling", until)
            },
            prevUntil: function(elem, i, until) {
              return jQuery.dir(elem, "previousSibling", until)
            },
            siblings: function(elem) {
              return jQuery.sibling((elem.parentNode || {}).firstChild, elem)
            },
            children: function(elem) {
              return jQuery.sibling(elem.firstChild)
            },
            contents: function(elem) {
              return jQuery.nodeName(elem, "iframe")
                ? elem.contentDocument || elem.contentWindow.document
                : jQuery.merge([], elem.childNodes)
            }
          }, function(name, fn) {
            jQuery.fn[name] = function(until, selector) {
              var ret = jQuery.map(this, fn, until);
              if (name.slice(-5) !== "Until") {
                selector = until
              }
              if (selector && typeof selector === "string") {
                ret = jQuery.filter(selector, ret)
              }
              if (this.length > 1) {
                if (!guaranteedUnique[name]) {
                  ret = jQuery.unique(ret)
                }
                if (rparentsprev.test(name)) {
                  ret = ret.reverse()
                }
              }
              return this.pushStack(ret)
            }
          });
          var rnotwhite = /\S+/g;
          var optionsCache = {};
          function createOptions(options) {
            var object = optionsCache[options] = {};
            jQuery.each(options.match(rnotwhite) || [], function(_, flag) {
              object[flag] = true
            });
            return object
          }
          jQuery.Callbacks = function(options) {
            options = typeof options === "string"
              ? optionsCache[options] || createOptions(options)
              : jQuery.extend({}, options);
            var firing,
              memory,
              fired,
              firingLength,
              firingIndex,
              firingStart,
              list = [],
              stack = !options.once && [],
              fire = function(data) {
                memory = options.memory && data;
                fired = true;
                firingIndex = firingStart || 0;
                firingStart = 0;
                firingLength = list.length;
                firing = true;
                for (; list && firingIndex < firingLength; firingIndex++) {
                  if (list[firingIndex].apply(data[0], data[1]) === false && options.stopOnFalse) {
                    memory = false;
                    break
                  }
                }
                firing = false;
                if (list) {
                  if (stack) {
                    if (stack.length) {
                      fire(stack.shift())
                    }
                  } else if (memory) {
                    list = []
                  } else {
                    self.disable()
                  }
                }
              },
              self = {
                add: function() {
                  if (list) {
                    var start = list.length;
                    (function add(args) {
                      jQuery.each(args, function(_, arg) {
                        var type = jQuery.type(arg);
                        if (type === "function") {
                          if (!options.unique || !self.has(arg)) {
                            list.push(arg)
                          }
                        } else if (arg && arg.length && type !== "string") {
                          add(arg)
                        }
                      })
                    })(arguments);
                    if (firing) {
                      firingLength = list.length
                    } else if (memory) {
                      firingStart = start;
                      fire(memory)
                    }
                  }
                  return this
                },
                remove: function() {
                  if (list) {
                    jQuery.each(arguments, function(_, arg) {
                      var index;
                      while ((index = jQuery.inArray(arg, list, index)) > -1) {
                        list.splice(index, 1);
                        if (firing) {
                          if (index <= firingLength) {
                            firingLength--
                          }
                          if (index <= firingIndex) {
                            firingIndex--
                          }
                        }
                      }
                    })
                  }
                  return this
                },
                has: function(fn) {
                  return fn
                    ? jQuery.inArray(fn, list) > -1
                    : !!(list && list.length)
                },
                empty: function() {
                  list = [];
                  firingLength = 0;
                  return this
                },
                disable: function() {
                  list = stack = memory = undefined;
                  return this
                },
                disabled: function() {
                  return !list
                },
                lock: function() {
                  stack = undefined;
                  if (!memory) {
                    self.disable()
                  }
                  return this
                },
                locked: function() {
                  return !stack
                },
                fireWith: function(context, args) {
                  if (list && (!fired || stack)) {
                    args = args || [];
                    args = [
                      context, args.slice
                        ? args.slice()
                        : args
                    ];
                    if (firing) {
                      stack.push(args)
                    } else {
                      fire(args)
                    }
                  }
                  return this
                },
                fire: function() {
                  self.fireWith(this, arguments);
                  return this
                },
                fired: function() {
                  return !!fired
                }
              };
            return self
          };
          jQuery.extend({
            Deferred: function(func) {
              var tuples = [
                  [
                    "resolve", "done", jQuery.Callbacks("once memory"), "resolved"
                  ],
                  [
                    "reject", "fail", jQuery.Callbacks("once memory"), "rejected"
                  ],
                  ["notify", "progress", jQuery.Callbacks("memory")]
                ],
                state = "pending",
                promise = {
                  state: function() {
                    return state
                  },
                  always: function() {
                    deferred.done(arguments).fail(arguments);
                    return this
                  },
                  then: function() {
                    var fns = arguments;
                    return jQuery.Deferred(function(newDefer) {
                      jQuery.each(tuples, function(i, tuple) {
                        var fn = jQuery.isFunction(fns[i]) && fns[i];
                        deferred[tuple[1]](function() {
                          var returned = fn && fn.apply(this, arguments);
                          if (returned && jQuery.isFunction(returned.promise)) {
                            returned.promise().done(newDefer.resolve).fail(newDefer.reject).progress(newDefer.notify)
                          } else {
                            newDefer[tuple[0] + "With"](this === promise
                              ? newDefer.promise()
                              : this, fn
                              ? [returned]
                              : arguments)
                          }
                        })
                      });
                      fns = null
                    }).promise()
                  },
                  promise: function(obj) {
                    return obj != null
                      ? jQuery.extend(obj, promise)
                      : promise
                  }
                },
                deferred = {};
              promise.pipe = promise.then;
              jQuery.each(tuples, function(i, tuple) {
                var list = tuple[2],
                  stateString = tuple[3];
                promise[tuple[1]] = list.add;
                if (stateString) {
                  list.add(function() {
                    state = stateString
                  }, tuples[i ^ 1][2].disable, tuples[2][2].lock)
                }
                deferred[tuple[0]] = function() {
                  deferred[tuple[0] + "With"](this === deferred
                    ? promise
                    : this, arguments);
                  return this
                };
                deferred[tuple[0] + "With"] = list.fireWith
              });
              promise.promise(deferred);
              if (func) {
                func.call(deferred, deferred)
              }
              return deferred
            },
            when: function(subordinate) {
              var i = 0,
                resolveValues = slice.call(arguments),
                length = resolveValues.length,
                remaining = length !== 1 || subordinate && jQuery.isFunction(subordinate.promise)
                  ? length
                  : 0,
                deferred = remaining === 1
                  ? subordinate
                  : jQuery.Deferred(),
                updateFunc = function(i, contexts, values) {
                  return function(value) {
                    contexts[i] = this;
                    values[i] = arguments.length > 1
                      ? slice.call(arguments)
                      : value;
                    if (values === progressValues) {
                      deferred.notifyWith(contexts, values)
                    } else if (!--remaining) {
                      deferred.resolveWith(contexts, values)
                    }
                  }
                },
                progressValues,
                progressContexts,
                resolveContexts;
              if (length > 1) {
                progressValues = new Array(length);
                progressContexts = new Array(length);
                resolveContexts = new Array(length);
                for (; i < length; i++) {
                  if (resolveValues[i] && jQuery.isFunction(resolveValues[i].promise)) {
                    resolveValues[i].promise().done(updateFunc(i, resolveContexts, resolveValues)).fail(deferred.reject).progress(updateFunc(i, progressContexts, progressValues))
                  } else {
                    --remaining
                  }
                }
              }
              if (!remaining) {
                deferred.resolveWith(resolveContexts, resolveValues)
              }
              return deferred.promise()
            }
          });
          var readyList;
          jQuery.fn.ready = function(fn) {
            jQuery.ready.promise().done(fn);
            return this
          };
          jQuery.extend({
            isReady: false,
            readyWait: 1,
            holdReady: function(hold) {
              if (hold) {
                jQuery.readyWait++
              } else {
                jQuery.ready(true)
              }
            },
            ready: function(wait) {
              if (wait === true
                ? --jQuery.readyWait
                : jQuery.isReady) {
                return
              }
              if (!document.body) {
                return setTimeout(jQuery.ready)
              }
              jQuery.isReady = true;
              if (wait !== true && --jQuery.readyWait > 0) {
                return
              }
              readyList.resolveWith(document, [jQuery]);
              if (jQuery.fn.triggerHandler) {
                jQuery(document).triggerHandler("ready");
                jQuery(document).off("ready")
              }
            }
          });
          function detach() {
            if (document.addEventListener) {
              document.removeEventListener("DOMContentLoaded", completed, false);
              window.removeEventListener("load", completed, false)
            } else {
              document.detachEvent("onreadystatechange", completed);
              window.detachEvent("onload", completed)
            }
          }
          function completed() {
            if (document.addEventListener || event.type === "load" || document.readyState === "complete") {
              detach();
              jQuery.ready()
            }
          }
          jQuery.ready.promise = function(obj) {
            if (!readyList) {
              readyList = jQuery.Deferred();
              if (document.readyState === "complete") {
                setTimeout(jQuery.ready)
              } else if (document.addEventListener) {
                document.addEventListener("DOMContentLoaded", completed, false);
                window.addEventListener("load", completed, false)
              } else {
                document.attachEvent("onreadystatechange", completed);
                window.attachEvent("onload", completed);
                var top = false;
                try {
                  top = window.frameElement == null && document.documentElement
                } catch (e) {}
                if (top && top.doScroll) {
                  (function doScrollCheck() {
                    if (!jQuery.isReady) {
                      try {
                        top.doScroll("left")
                      } catch (e) {
                        return setTimeout(doScrollCheck, 50)
                      }
                      detach();
                      jQuery.ready()
                    }
                  })()
                }
              }
            }
            return readyList.promise(obj)
          };
          var strundefined = typeof undefined;
          var i;
          for (i in jQuery(support)) {
            break
          }
          support.ownLast = i !== "0";
          support.inlineBlockNeedsLayout = false;
          jQuery(function() {
            var val,
              div,
              body,
              container;
            body = document.getElementsByTagName("body")[0];
            if (!body || !body.style) {
              return
            }
            div = document.createElement("div");
            container = document.createElement("div");
            container.style.cssText = "position:absolute;border:0;width:0;height:0;top:0;left:-9999px";
            body.appendChild(container).appendChild(div);
            if (typeof div.style.zoom !== strundefined) {
              div.style.cssText = "display:inline;margin:0;border:0;padding:1px;width:1px;zoom:1";
              support.inlineBlockNeedsLayout = val = div.offsetWidth === 3;
              if (val) {
                body.style.zoom = 1
              }
            }
            body.removeChild(container)
          });
          (function() {
            var div = document.createElement("div");
            if (support.deleteExpando == null) {
              support.deleteExpando = true;
              try {
                delete div.test
              } catch (e) {
                support.deleteExpando = false
              }
            }
            div = null
          })();
          jQuery.acceptData = function(elem) {
            var noData = jQuery.noData[(elem.nodeName + " ").toLowerCase()],
              nodeType =+ elem.nodeType || 1;
            return nodeType !== 1 && nodeType !== 9
              ? false
              : !noData || noData !== true && elem.getAttribute("classid") === noData
          };
          var rbrace = /^(?:\{[\w\W]*\}|\[[\w\W]*\])$/,
            rmultiDash = /([A-Z])/g;
          function dataAttr(elem, key, data) {
            if (data === undefined && elem.nodeType === 1) {
              var name = "data-" + key.replace(rmultiDash, "-$1").toLowerCase();
              data = elem.getAttribute(name);
              if (typeof data === "string") {
                try {
                  data = data === "true"
                    ? true
                    : data === "false"
                      ? false
                      : data === "null"
                        ? null :+ data + "" === data ?+ data
                        : rbrace.test(data)
                          ? jQuery.parseJSON(data)
                          : data
                } catch (e) {}
                jQuery.data(elem, key, data)
              } else {
                data = undefined
              }
            }
            return data
          }
          function isEmptyDataObject(obj) {
            var name;
            for (name in obj) {
              if (name === "data" && jQuery.isEmptyObject(obj[name])) {
                continue
              }
              if (name !== "toJSON") {
                return false
              }
            }
            return true
          }
          function internalData(elem, name, data, pvt) {
            if (!jQuery.acceptData(elem)) {
              return
            }
            var ret,
              thisCache,
              internalKey = jQuery.expando,
              isNode = elem.nodeType,
              cache = isNode
                ? jQuery.cache
                : elem,
              id = isNode
                ? elem[internalKey]
                : elem[internalKey] && internalKey;
            if ((!id || !cache[id] || !pvt && !cache[id].data) && data === undefined && typeof name === "string") {
              return
            }
            if (!id) {
              if (isNode) {
                id = elem[internalKey] = deletedIds.pop() || jQuery.guid++
              } else {
                id = internalKey
              }
            }
            if (!cache[id]) {
              cache[id] = isNode
                ? {}
                : {
                  toJSON: jQuery.noop
                }
            }
            if (typeof name === "object" || typeof name === "function") {
              if (pvt) {
                cache[id] = jQuery.extend(cache[id], name)
              } else {
                cache[id].data = jQuery.extend(cache[id].data, name)
              }
            }
            thisCache = cache[id];
            if (!pvt) {
              if (!thisCache.data) {
                thisCache.data = {}
              }
              thisCache = thisCache.data
            }
            if (data !== undefined) {
              thisCache[jQuery.camelCase(name)] = data
            }
            if (typeof name === "string") {
              ret = thisCache[name];
              if (ret == null) {
                ret = thisCache[jQuery.camelCase(name)]
              }
            } else {
              ret = thisCache
            }
            return ret
          }
          function internalRemoveData(elem, name, pvt) {
            if (!jQuery.acceptData(elem)) {
              return
            }
            var thisCache,
              i,
              isNode = elem.nodeType,
              cache = isNode
                ? jQuery.cache
                : elem,
              id = isNode
                ? elem[jQuery.expando]
                : jQuery.expando;
            if (!cache[id]) {
              return
            }
            if (name) {
              thisCache = pvt
                ? cache[id]
                : cache[id].data;
              if (thisCache) {
                if (!jQuery.isArray(name)) {
                  if (name in thisCache) {
                    name = [name]
                  } else {
                    name = jQuery.camelCase(name);
                    if (name in thisCache) {
                      name = [name]
                    } else {
                      name = name.split(" ")
                    }
                  }
                } else {
                  name = name.concat(jQuery.map(name, jQuery.camelCase))
                }
                i = name.length;
                while (i--) {
                  delete thisCache[name[i]]
                }
                if (pvt
                  ? !isEmptyDataObject(thisCache)
                  : !jQuery.isEmptyObject(thisCache)) {
                  return
                }
              }
            }
            if (!pvt) {
              delete cache[id].data;
              if (!isEmptyDataObject(cache[id])) {
                return
              }
            }
            if (isNode) {
              jQuery.cleanData([elem], true)
            } else if (support.deleteExpando || cache != cache.window) {
              delete cache[id]
            } else {
              cache[id] = null
            }
          }
          jQuery.extend({
            cache: {},
            noData: {
              "applet ": true,
              "embed ": true,
              "object ": "clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"
            },
            hasData: function(elem) {
              elem = elem.nodeType
                ? jQuery.cache[elem[jQuery.expando]]
                : elem[jQuery.expando];
              return !!elem && !isEmptyDataObject(elem)
            },
            data: function(elem, name, data) {
              return internalData(elem, name, data)
            },
            removeData: function(elem, name) {
              return internalRemoveData(elem, name)
            },
            _data: function(elem, name, data) {
              return internalData(elem, name, data, true)
            },
            _removeData: function(elem, name) {
              return internalRemoveData(elem, name, true)
            }
          });
          jQuery.fn.extend({
            data: function(key, value) {
              var i,
                name,
                data,
                elem = this[0],
                attrs = elem && elem.attributes;
              if (key === undefined) {
                if (this.length) {
                  data = jQuery.data(elem);
                  if (elem.nodeType === 1 && !jQuery._data(elem, "parsedAttrs")) {
                    i = attrs.length;
                    while (i--) {
                      if (attrs[i]) {
                        name = attrs[i].name;
                        if (name.indexOf("data-") === 0) {
                          name = jQuery.camelCase(name.slice(5));
                          dataAttr(elem, name, data[name])
                        }
                      }
                    }
                    jQuery._data(elem, "parsedAttrs", true)
                  }
                }
                return data
              }
              if (typeof key === "object") {
                return this.each(function() {
                  jQuery.data(this, key)
                })
              }
              return arguments.length > 1
                ? this.each(function() {
                  jQuery.data(this, key, value)
                })
                : elem
                  ? dataAttr(elem, key, jQuery.data(elem, key))
                  : undefined
            },
            removeData: function(key) {
              return this.each(function() {
                jQuery.removeData(this, key)
              })
            }
          });
          jQuery.extend({
            queue: function(elem, type, data) {
              var queue;
              if (elem) {
                type = (type || "fx") + "queue";
                queue = jQuery._data(elem, type);
                if (data) {
                  if (!queue || jQuery.isArray(data)) {
                    queue = jQuery._data(elem, type, jQuery.makeArray(data))
                  } else {
                    queue.push(data)
                  }
                }
                return queue || []
              }
            },
            dequeue: function(elem, type) {
              type = type || "fx";
              var queue = jQuery.queue(elem, type),
                startLength = queue.length,
                fn = queue.shift(),
                hooks = jQuery._queueHooks(elem, type),
                next = function() {
                  jQuery.dequeue(elem, type)
                };
              if (fn === "inprogress") {
                fn = queue.shift();
                startLength--
              }
              if (fn) {
                if (type === "fx") {
                  queue.unshift("inprogress")
                }
                delete hooks.stop;
                fn.call(elem, next, hooks)
              }
              if (!startLength && hooks) {
                hooks.empty.fire()
              }
            },
            _queueHooks: function(elem, type) {
              var key = type + "queueHooks";
              return jQuery._data(elem, key) || jQuery._data(elem, key, {
                empty: jQuery.Callbacks("once memory").add(function() {
                  jQuery._removeData(elem, type + "queue");
                  jQuery._removeData(elem, key)
                })
              })
            }
          });
          jQuery.fn.extend({
            queue: function(type, data) {
              var setter = 2;
              if (typeof type !== "string") {
                data = type;
                type = "fx";
                setter--
              }
              if (arguments.length < setter) {
                return jQuery.queue(this[0], type)
              }
              return data === undefined
                ? this
                : this.each(function() {
                  var queue = jQuery.queue(this, type, data);
                  jQuery._queueHooks(this, type);
                  if (type === "fx" && queue[0] !== "inprogress") {
                    jQuery.dequeue(this, type)
                  }
                })
            },
            dequeue: function(type) {
              return this.each(function() {
                jQuery.dequeue(this, type)
              })
            },
            clearQueue: function(type) {
              return this.queue(type || "fx", [])
            },
            promise: function(type, obj) {
              var tmp,
                count = 1,
                defer = jQuery.Deferred(),
                elements = this,
                i = this.length,
                resolve = function() {
                  if (!--count) {
                    defer.resolveWith(elements, [elements])
                  }
                };
              if (typeof type !== "string") {
                obj = type;
                type = undefined
              }
              type = type || "fx";
              while (i--) {
                tmp = jQuery._data(elements[i], type + "queueHooks");
                if (tmp && tmp.empty) {
                  count++;
                  tmp.empty.add(resolve)
                }
              }
              resolve();
              return defer.promise(obj)
            }
          });
          var pnum = /[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/.source;
          var cssExpand = ["Top", "Right", "Bottom", "Left"];
          var isHidden = function(elem, el) {
            elem = el || elem;
            return jQuery.css(elem, "display") === "none" || !jQuery.contains(elem.ownerDocument, elem)
          };
          var access = jQuery.access = function(elems, fn, key, value, chainable, emptyGet, raw) {
            var i = 0,
              length = elems.length,
              bulk = key == null;
            if (jQuery.type(key) === "object") {
              chainable = true;
              for (i in key) {
                jQuery.access(elems, fn, i, key[i], true, emptyGet, raw)
              }
            } else if (value !== undefined) {
              chainable = true;
              if (!jQuery.isFunction(value)) {
                raw = true
              }
              if (bulk) {
                if (raw) {
                  fn.call(elems, value);
                  fn = null
                } else {
                  bulk = fn;
                  fn = function(elem, key, value) {
                    return bulk.call(jQuery(elem), value)
                  }
                }
              }
              if (fn) {
                for (; i < length; i++) {
                  fn(elems[i], key, raw
                    ? value
                    : value.call(elems[i], i, fn(elems[i], key)))
                }
              }
            }
            return chainable
              ? elems
              : bulk
                ? fn.call(elems)
                : length
                  ? fn(elems[0], key)
                  : emptyGet
          };
          var rcheckableType = /^(?:checkbox|radio)$/i;
          (function() {
            var input = document.createElement("input"),
              div = document.createElement("div"),
              fragment = document.createDocumentFragment();
            div.innerHTML = "  <link/><table></table><a href='/a'>a</a><input type='checkbox'/>";
            support.leadingWhitespace = div.firstChild.nodeType === 3;
            support.tbody = !div.getElementsByTagName("tbody").length;
            support.htmlSerialize = !!div.getElementsByTagName("link").length;
            support.html5Clone = document.createElement("nav").cloneNode(true).outerHTML !== "<:nav></:nav>";
            input.type = "checkbox";
            input.checked = true;
            fragment.appendChild(input);
            support.appendChecked = input.checked;
            div.innerHTML = "<textarea>x</textarea>";
            support.noCloneChecked = !!div.cloneNode(true).lastChild.defaultValue;
            fragment.appendChild(div);
            div.innerHTML = "<input type='radio' checked='checked' name='t'/>";
            support.checkClone = div.cloneNode(true).cloneNode(true).lastChild.checked;
            support.noCloneEvent = true;
            if (div.attachEvent) {
              div.attachEvent("onclick", function() {
                support.noCloneEvent = false
              });
              div.cloneNode(true).click()
            }
            if (support.deleteExpando == null) {
              support.deleteExpando = true;
              try {
                delete div.test
              } catch (e) {
                support.deleteExpando = false
              }
            }
          })();
          (function() {
            var i,
              eventName,
              div = document.createElement("div");
            for (i in {submit: true, change: true, focusin: true}) {
              eventName = "on" + i;
              if (!(support[i + "Bubbles"] = eventName in window)) {
                div.setAttribute(eventName, "t");
                support[i + "Bubbles"] = div.attributes[eventName].expando === false
              }
            }
            div = null
          })();
          var rformElems = /^(?:input|select|textarea)$/i,
            rkeyEvent = /^key/,
            rmouseEvent = /^(?:mouse|pointer|contextmenu)|click/,
            rfocusMorph = /^(?:focusinfocus|focusoutblur)$/,
            rtypenamespace = /^([^.]*)(?:\.(.+)|)$/;
          function returnTrue() {
            return true
          }
          function returnFalse() {
            return false
          }
          function safeActiveElement() {
            try {
              return document.activeElement
            } catch (err) {}
          }
          jQuery.event = {
            global: {},
            add: function(elem, types, handler, data, selector) {
              var tmp,
                events,
                t,
                handleObjIn,
                special,
                eventHandle,
                handleObj,
                handlers,
                type,
                namespaces,
                origType,
                elemData = jQuery._data(elem);
              if (!elemData) {
                return
              }
              if (handler.handler) {
                handleObjIn = handler;
                handler = handleObjIn.handler;
                selector = handleObjIn.selector
              }
              if (!handler.guid) {
                handler.guid = jQuery.guid++
              }
              if (!(events = elemData.events)) {
                events = elemData.events = {}
              }
              if (!(eventHandle = elemData.handle)) {
                eventHandle = elemData.handle = function(e) {
                  return typeof jQuery !== strundefined && (!e || jQuery.event.triggered !== e.type)
                    ? jQuery.event.dispatch.apply(eventHandle.elem, arguments)
                    : undefined
                };
                eventHandle.elem = elem
              }
              types = (types || "").match(rnotwhite) || [""];
              t = types.length;
              while (t--) {
                tmp = rtypenamespace.exec(types[t]) || [];
                type = origType = tmp[1];
                namespaces = (tmp[2] || "").split(".").sort();
                if (!type) {
                  continue
                }
                special = jQuery.event.special[type] || {};
                type = (selector
                  ? special.delegateType
                  : special.bindType) || type;
                special = jQuery.event.special[type] || {};
                handleObj = jQuery.extend({
                  type: type,
                  origType: origType,
                  data: data,
                  handler: handler,
                  guid: handler.guid,
                  selector: selector,
                  needsContext: selector && jQuery.expr.match.needsContext.test(selector),
                  namespace: namespaces.join(".")
                }, handleObjIn);
                if (!(handlers = events[type])) {
                  handlers = events[type] = [];
                  handlers.delegateCount = 0;
                  if (!special.setup || special.setup.call(elem, data, namespaces, eventHandle) === false) {
                    if (elem.addEventListener) {
                      elem.addEventListener(type, eventHandle, false)
                    } else if (elem.attachEvent) {
                      elem.attachEvent("on" + type, eventHandle)
                    }
                  }
                }
                if (special.add) {
                  special.add.call(elem, handleObj);
                  if (!handleObj.handler.guid) {
                    handleObj.handler.guid = handler.guid
                  }
                }
                if (selector) {
                  handlers.splice(handlers.delegateCount++, 0, handleObj)
                } else {
                  handlers.push(handleObj)
                }
                jQuery.event.global[type] = true
              }
              elem = null
            },
            remove: function(elem, types, handler, selector, mappedTypes) {
              var j,
                handleObj,
                tmp,
                origCount,
                t,
                events,
                special,
                handlers,
                type,
                namespaces,
                origType,
                elemData = jQuery.hasData(elem) && jQuery._data(elem);
              if (!elemData || !(events = elemData.events)) {
                return
              }
              types = (types || "").match(rnotwhite) || [""];
              t = types.length;
              while (t--) {
                tmp = rtypenamespace.exec(types[t]) || [];
                type = origType = tmp[1];
                namespaces = (tmp[2] || "").split(".").sort();
                if (!type) {
                  for (type in events) {
                    jQuery.event.remove(elem, type + types[t], handler, selector, true)
                  }
                  continue
                }
                special = jQuery.event.special[type] || {};
                type = (selector
                  ? special.delegateType
                  : special.bindType) || type;
                handlers = events[type] || [];
                tmp = tmp[2] && new RegExp("(^|\\.)" + namespaces.join("\\.(?:.*\\.|)") + "(\\.|$)");
                origCount = j = handlers.length;
                while (j--) {
                  handleObj = handlers[j];
                  if ((mappedTypes || origType === handleObj.origType) && (!handler || handler.guid === handleObj.guid) && (!tmp || tmp.test(handleObj.namespace)) && (!selector || selector === handleObj.selector || selector === "**" && handleObj.selector)) {
                    handlers.splice(j, 1);
                    if (handleObj.selector) {
                      handlers.delegateCount--
                    }
                    if (special.remove) {
                      special.remove.call(elem, handleObj)
                    }
                  }
                }
                if (origCount && !handlers.length) {
                  if (!special.teardown || special.teardown.call(elem, namespaces, elemData.handle) === false) {
                    jQuery.removeEvent(elem, type, elemData.handle)
                  }
                  delete events[type]
                }
              }
              if (jQuery.isEmptyObject(events)) {
                delete elemData.handle;
                jQuery._removeData(elem, "events")
              }
            },
            trigger: function(event, data, elem, onlyHandlers) {
              var handle,
                ontype,
                cur,
                bubbleType,
                special,
                tmp,
                i,
                eventPath = [elem || document],
                type = hasOwn.call(event, "type")
                  ? event.type
                  : event,
                namespaces = hasOwn.call(event, "namespace")
                  ? event.namespace.split(".")
                  : [];
              cur = tmp = elem = elem || document;
              if (elem.nodeType === 3 || elem.nodeType === 8) {
                return
              }
              if (rfocusMorph.test(type + jQuery.event.triggered)) {
                return
              }
              if (type.indexOf(".") >= 0) {
                namespaces = type.split(".");
                type = namespaces.shift();
                namespaces.sort()
              }
              ontype = type.indexOf(":") < 0 && "on" + type;
              event = event[jQuery.expando]
                ? event
                : new jQuery.Event(type, typeof event === "object" && event);
              event.isTrigger = onlyHandlers
                ? 2
                : 3;
              event.namespace = namespaces.join(".");
              event.namespace_re = event.namespace
                ? new RegExp("(^|\\.)" + namespaces.join("\\.(?:.*\\.|)") + "(\\.|$)")
                : null;
              event.result = undefined;
              if (!event.target) {
                event.target = elem
              }
              data = data == null
                ? [event]
                : jQuery.makeArray(data, [event]);
              special = jQuery.event.special[type] || {};
              if (!onlyHandlers && special.trigger && special.trigger.apply(elem, data) === false) {
                return
              }
              if (!onlyHandlers && !special.noBubble && !jQuery.isWindow(elem)) {
                bubbleType = special.delegateType || type;
                if (!rfocusMorph.test(bubbleType + type)) {
                  cur = cur.parentNode
                }
                for (; cur; cur = cur.parentNode) {
                  eventPath.push(cur);
                  tmp = cur
                }
                if (tmp === (elem.ownerDocument || document)) {
                  eventPath.push(tmp.defaultView || tmp.parentWindow || window)
                }
              }
              i = 0;
              while ((cur = eventPath[i++]) && !event.isPropagationStopped()) {
                event.type = i > 1
                  ? bubbleType
                  : special.bindType || type;
                handle = (jQuery._data(cur, "events") || {})[event.type] && jQuery._data(cur, "handle");
                if (handle) {
                  handle.apply(cur, data)
                }
                handle = ontype && cur[ontype];
                if (handle && handle.apply && jQuery.acceptData(cur)) {
                  event.result = handle.apply(cur, data);
                  if (event.result === false) {
                    event.preventDefault()
                  }
                }
              }
              event.type = type;
              if (!onlyHandlers && !event.isDefaultPrevented()) {
                if ((!special._default || special._default.apply(eventPath.pop(), data) === false) && jQuery.acceptData(elem)) {
                  if (ontype && elem[type] && !jQuery.isWindow(elem)) {
                    tmp = elem[ontype];
                    if (tmp) {
                      elem[ontype] = null
                    }
                    jQuery.event.triggered = type;
                    try {
                      elem[type]()
                    } catch (e) {}
                    jQuery.event.triggered = undefined;
                    if (tmp) {
                      elem[ontype] = tmp
                    }
                  }
                }
              }
              return event.result
            },
            dispatch: function(event) {
              event = jQuery.event.fix(event);
              var i,
                ret,
                handleObj,
                matched,
                j,
                handlerQueue = [],
                args = slice.call(arguments),
                handlers = (jQuery._data(this, "events") || {})[event.type] || [],
                special = jQuery.event.special[event.type] || {};
              args[0] = event;
              event.delegateTarget = this;
              if (special.preDispatch && special.preDispatch.call(this, event) === false) {
                return
              }
              handlerQueue = jQuery.event.handlers.call(this, event, handlers);
              i = 0;
              while ((matched = handlerQueue[i++]) && !event.isPropagationStopped()) {
                event.currentTarget = matched.elem;
                j = 0;
                while ((handleObj = matched.handlers[j++]) && !event.isImmediatePropagationStopped()) {
                  if (!event.namespace_re || event.namespace_re.test(handleObj.namespace)) {
                    event.handleObj = handleObj;
                    event.data = handleObj.data;
                    ret = ((jQuery.event.special[handleObj.origType] || {}).handle || handleObj.handler).apply(matched.elem, args);
                    if (ret !== undefined) {
                      if ((event.result = ret) === false) {
                        event.preventDefault();
                        event.stopPropagation()
                      }
                    }
                  }
                }
              }
              if (special.postDispatch) {
                special.postDispatch.call(this, event)
              }
              return event.result
            },
            handlers: function(event, handlers) {
              var sel,
                handleObj,
                matches,
                i,
                handlerQueue = [],
                delegateCount = handlers.delegateCount,
                cur = event.target;
              if (delegateCount && cur.nodeType && (!event.button || event.type !== "click")) {
                for (; cur != this; cur = cur.parentNode || this) {
                  if (cur.nodeType === 1 && (cur.disabled !== true || event.type !== "click")) {
                    matches = [];
                    for (i = 0; i < delegateCount; i++) {
                      handleObj = handlers[i];
                      sel = handleObj.selector + " ";
                      if (matches[sel] === undefined) {
                        matches[sel] = handleObj.needsContext
                          ? jQuery(sel, this).index(cur) >= 0
                          : jQuery.find(sel, this, null, [cur]).length
                      }
                      if (matches[sel]) {
                        matches.push(handleObj)
                      }
                    }
                    if (matches.length) {
                      handlerQueue.push({elem: cur, handlers: matches})
                    }
                  }
                }
              }
              if (delegateCount < handlers.length) {
                handlerQueue.push({elem: this, handlers: handlers.slice(delegateCount)})
              }
              return handlerQueue
            },
            fix: function(event) {
              if (event[jQuery.expando]) {
                return event
              }
              var i,
                prop,
                copy,
                type = event.type,
                originalEvent = event,
                fixHook = this.fixHooks[type];
              if (!fixHook) {
                this.fixHooks[type] = fixHook = rmouseEvent.test(type)
                  ? this.mouseHooks
                  : rkeyEvent.test(type)
                    ? this.keyHooks
                    : {}
              }
              copy = fixHook.props
                ? this.props.concat(fixHook.props)
                : this.props;
              event = new jQuery.Event(originalEvent);
              i = copy.length;
              while (i--) {
                prop = copy[i];
                event[prop] = originalEvent[prop]
              }
              if (!event.target) {
                event.target = originalEvent.srcElement || document
              }
              if (event.target.nodeType === 3) {
                event.target = event.target.parentNode
              }
              event.metaKey = !!event.metaKey;
              return fixHook.filter
                ? fixHook.filter(event, originalEvent)
                : event
            },
            props: "altKey bubbles cancelable ctrlKey currentTarget eventPhase metaKey relatedTarget shiftKey target timeStamp view which".split(" "),
            fixHooks: {},
            keyHooks: {
              props: "char charCode key keyCode".split(" "),
              filter: function(event, original) {
                if (event.which == null) {
                  event.which = original.charCode != null
                    ? original.charCode
                    : original.keyCode
                }
                return event
              }
            },
            mouseHooks: {
              props: "button buttons clientX clientY fromElement offsetX offsetY pageX pageY screenX screenY toElement".split(" "),
              filter: function(event, original) {
                var body,
                  eventDoc,
                  doc,
                  button = original.button,
                  fromElement = original.fromElement;
                if (event.pageX == null && original.clientX != null) {
                  eventDoc = event.target.ownerDocument || document;
                  doc = eventDoc.documentElement;
                  body = eventDoc.body;
                  event.pageX = original.clientX + (doc && doc.scrollLeft || body && body.scrollLeft || 0) - (doc && doc.clientLeft || body && body.clientLeft || 0);
                  event.pageY = original.clientY + (doc && doc.scrollTop || body && body.scrollTop || 0) - (doc && doc.clientTop || body && body.clientTop || 0)
                }
                if (!event.relatedTarget && fromElement) {
                  event.relatedTarget = fromElement === event.target
                    ? original.toElement
                    : fromElement
                }
                if (!event.which && button !== undefined) {
                  event.which = button & 1
                    ? 1
                    : button & 2
                      ? 3
                      : button & 4
                        ? 2
                        : 0
                }
                return event
              }
            },
            special: {
              load: {
                noBubble: true
              },
              focus: {
                trigger: function() {
                  if (this !== safeActiveElement() && this.focus) {
                    try {
                      this.focus();
                      return false
                    } catch (e) {}
                  }
                },
                delegateType: "focusin"
              },
              blur: {
                trigger: function() {
                  if (this === safeActiveElement() && this.blur) {
                    this.blur();
                    return false
                  }
                },
                delegateType: "focusout"
              },
              click: {
                trigger: function() {
                  if (jQuery.nodeName(this, "input") && this.type === "checkbox" && this.click) {
                    this.click();
                    return false
                  }
                },
                _default: function(event) {
                  return jQuery.nodeName(event.target, "a")
                }
              },
              beforeunload: {
                postDispatch: function(event) {
                  if (event.result !== undefined && event.originalEvent) {
                    event.originalEvent.returnValue = event.result
                  }
                }
              }
            },
            simulate: function(type, elem, event, bubble) {
              var e = jQuery.extend(new jQuery.Event, event, {
                type: type,
                isSimulated: true,
                originalEvent: {}
              });
              if (bubble) {
                jQuery.event.trigger(e, null, elem)
              } else {
                jQuery.event.dispatch.call(elem, e)
              }
              if (e.isDefaultPrevented()) {
                event.preventDefault()
              }
            }
          };
          jQuery.removeEvent = document.removeEventListener
            ? function(elem, type, handle) {
              if (elem.removeEventListener) {
                elem.removeEventListener(type, handle, false)
              }
            }
            : function(elem, type, handle) {
              var name = "on" + type;
              if (elem.detachEvent) {
                if (typeof elem[name] === strundefined) {
                  elem[name] = null
                }
                elem.detachEvent(name, handle)
              }
            };
          jQuery.Event = function(src, props) {
            if (!(this instanceof jQuery.Event)) {
              return new jQuery.Event(src, props)
            }
            if (src && src.type) {
              this.originalEvent = src;
              this.type = src.type;
              this.isDefaultPrevented = src.defaultPrevented || src.defaultPrevented === undefined && src.returnValue === false
                ? returnTrue
                : returnFalse
            } else {
              this.type = src
            }
            if (props) {
              jQuery.extend(this, props)
            }
            this.timeStamp = src && src.timeStamp || jQuery.now();
            this[jQuery.expando] = true
          };
          jQuery.Event.prototype = {
            isDefaultPrevented: returnFalse,
            isPropagationStopped: returnFalse,
            isImmediatePropagationStopped: returnFalse,
            preventDefault: function() {
              var e = this.originalEvent;
              this.isDefaultPrevented = returnTrue;
              if (!e) {
                return
              }
              if (e.preventDefault) {
                e.preventDefault()
              } else {
                e.returnValue = false
              }
            },
            stopPropagation: function() {
              var e = this.originalEvent;
              this.isPropagationStopped = returnTrue;
              if (!e) {
                return
              }
              if (e.stopPropagation) {
                e.stopPropagation()
              }
              e.cancelBubble = true
            },
            stopImmediatePropagation: function() {
              var e = this.originalEvent;
              this.isImmediatePropagationStopped = returnTrue;
              if (e && e.stopImmediatePropagation) {
                e.stopImmediatePropagation()
              }
              this.stopPropagation()
            }
          };
          jQuery.each({
            mouseenter: "mouseover",
            mouseleave: "mouseout",
            pointerenter: "pointerover",
            pointerleave: "pointerout"
          }, function(orig, fix) {
            jQuery.event.special[orig] = {
              delegateType: fix,
              bindType: fix,
              handle: function(event) {
                var ret,
                  target = this,
                  related = event.relatedTarget,
                  handleObj = event.handleObj;
                if (!related || related !== target && !jQuery.contains(target, related)) {
                  event.type = handleObj.origType;
                  ret = handleObj.handler.apply(this, arguments);
                  event.type = fix
                }
                return ret
              }
            }
          });
          if (!support.submitBubbles) {
            jQuery.event.special.submit = {
              setup: function() {
                if (jQuery.nodeName(this, "form")) {
                  return false
                }
                jQuery.event.add(this, "click._submit keypress._submit", function(e) {
                  var elem = e.target,
                    form = jQuery.nodeName(elem, "input") || jQuery.nodeName(elem, "button")
                      ? elem.form
                      : undefined;
                  if (form && !jQuery._data(form, "submitBubbles")) {
                    jQuery.event.add(form, "submit._submit", function(event) {
                      event._submit_bubble = true
                    });
                    jQuery._data(form, "submitBubbles", true)
                  }
                })
              },
              postDispatch: function(event) {
                if (event._submit_bubble) {
                  delete event._submit_bubble;
                  if (this.parentNode && !event.isTrigger) {
                    jQuery.event.simulate("submit", this.parentNode, event, true)
                  }
                }
              },
              teardown: function() {
                if (jQuery.nodeName(this, "form")) {
                  return false
                }
                jQuery.event.remove(this, "._submit")
              }
            }
          }
          if (!support.changeBubbles) {
            jQuery.event.special.change = {
              setup: function() {
                if (rformElems.test(this.nodeName)) {
                  if (this.type === "checkbox" || this.type === "radio") {
                    jQuery.event.add(this, "propertychange._change", function(event) {
                      if (event.originalEvent.propertyName === "checked") {
                        this._just_changed = true
                      }
                    });
                    jQuery.event.add(this, "click._change", function(event) {
                      if (this._just_changed && !event.isTrigger) {
                        this._just_changed = false
                      }
                      jQuery.event.simulate("change", this, event, true)
                    })
                  }
                  return false
                }
                jQuery.event.add(this, "beforeactivate._change", function(e) {
                  var elem = e.target;
                  if (rformElems.test(elem.nodeName) && !jQuery._data(elem, "changeBubbles")) {
                    jQuery.event.add(elem, "change._change", function(event) {
                      if (this.parentNode && !event.isSimulated && !event.isTrigger) {
                        jQuery.event.simulate("change", this.parentNode, event, true)
                      }
                    });
                    jQuery._data(elem, "changeBubbles", true)
                  }
                })
              },
              handle: function(event) {
                var elem = event.target;
                if (this !== elem || event.isSimulated || event.isTrigger || elem.type !== "radio" && elem.type !== "checkbox") {
                  return event.handleObj.handler.apply(this, arguments)
                }
              },
              teardown: function() {
                jQuery.event.remove(this, "._change");
                return !rformElems.test(this.nodeName)
              }
            }
          }
          if (!support.focusinBubbles) {
            jQuery.each({
              focus: "focusin",
              blur: "focusout"
            }, function(orig, fix) {
              var handler = function(event) {
                jQuery.event.simulate(fix, event.target, jQuery.event.fix(event), true)
              };
              jQuery.event.special[fix] = {
                setup: function() {
                  var doc = this.ownerDocument || this,
                    attaches = jQuery._data(doc, fix);
                  if (!attaches) {
                    doc.addEventListener(orig, handler, true)
                  }
                  jQuery._data(doc, fix, (attaches || 0) + 1)
                },
                teardown: function() {
                  var doc = this.ownerDocument || this,
                    attaches = jQuery._data(doc, fix) - 1;
                  if (!attaches) {
                    doc.removeEventListener(orig, handler, true);
                    jQuery._removeData(doc, fix)
                  } else {
                    jQuery._data(doc, fix, attaches)
                  }
                }
              }
            })
          }
          jQuery.fn.extend({
            on: function(types, selector, data, fn, one) {
              var type,
                origFn;
              if (typeof types === "object") {
                if (typeof selector !== "string") {
                  data = data || selector;
                  selector = undefined
                }
                for (type in types) {
                  this.on(type, selector, data, types[type], one)
                }
                return this
              }
              if (data == null && fn == null) {
                fn = selector;
                data = selector = undefined
              } else if (fn == null) {
                if (typeof selector === "string") {
                  fn = data;
                  data = undefined
                } else {
                  fn = data;
                  data = selector;
                  selector = undefined
                }
              }
              if (fn === false) {
                fn = returnFalse
              } else if (!fn) {
                return this
              }
              if (one === 1) {
                origFn = fn;
                fn = function(event) {
                  jQuery().off(event);
                  return origFn.apply(this, arguments)
                };
                fn.guid = origFn.guid || (origFn.guid = jQuery.guid++)
              }
              return this.each(function() {
                jQuery.event.add(this, types, fn, data, selector)
              })
            },
            one: function(types, selector, data, fn) {
              return this.on(types, selector, data, fn, 1)
            },
            off: function(types, selector, fn) {
              var handleObj,
                type;
              if (types && types.preventDefault && types.handleObj) {
                handleObj = types.handleObj;
                jQuery(types.delegateTarget).off(handleObj.namespace
                  ? handleObj.origType + "." + handleObj.namespace
                  : handleObj.origType, handleObj.selector, handleObj.handler);
                return this
              }
              if (typeof types === "object") {
                for (type in types) {
                  this.off(type, selector, types[type])
                }
                return this
              }
              if (selector === false || typeof selector === "function") {
                fn = selector;
                selector = undefined
              }
              if (fn === false) {
                fn = returnFalse
              }
              return this.each(function() {
                jQuery.event.remove(this, types, fn, selector)
              })
            },
            trigger: function(type, data) {
              return this.each(function() {
                jQuery.event.trigger(type, data, this)
              })
            },
            triggerHandler: function(type, data) {
              var elem = this[0];
              if (elem) {
                return jQuery.event.trigger(type, data, elem, true)
              }
            }
          });
          function createSafeFragment(document) {
            var list = nodeNames.split("|"),
              safeFrag = document.createDocumentFragment();
            if (safeFrag.createElement) {
              while (list.length) {
                safeFrag.createElement(list.pop())
              }
            }
            return safeFrag
          }
          var nodeNames = "abbr|article|aside|audio|bdi|canvas|data|datalist|details|figcaption|figure|footer|" +
            "header|hgroup|mark|meter|nav|output|progress|section|summary|time|video",
            rinlinejQuery = / jQuery\d+="(?:null|\d+)"/g,
            rnoshimcache = new RegExp("<(?:" + nodeNames + ")[\\s/>]", "i"),
            rleadingWhitespace = /^\s+/,
            rxhtmlTag = /<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:]+)[^>]*)\/>/gi,
            rtagName = /<([\w:]+)/,
            rtbody = /<tbody/i,
            rhtml = /<|&#?\w+;/,
            rnoInnerhtml = /<(?:script|style|link)/i,
            rchecked = /checked\s*(?:[^=]|=\s*.checked.)/i,
            rscriptType = /^$|\/(?:java|ecma)script/i,
            rscriptTypeMasked = /^true\/(.*)/,
            rcleanScript = /^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g,
            wrapMap = {
              option: [
                1, "<select multiple='multiple'>", "</select>"
              ],
              legend: [
                1, "<fieldset>", "</fieldset>"
              ],
              area: [
                1, "<map>", "</map>"
              ],
              param: [
                1, "<object>", "</object>"
              ],
              thead: [
                1, "<table>", "</table>"
              ],
              tr: [
                2, "<table><tbody>", "</tbody></table>"
              ],
              col: [
                2, "<table><tbody></tbody><colgroup>", "</colgroup></table>"
              ],
              td: [
                3, "<table><tbody><tr>", "</tr></tbody></table>"
              ],
              _default: support.htmlSerialize
                ? [0, "", ""]
                : [1, "X<div>", "</div>"]
            },
            safeFragment = createSafeFragment(document),
            fragmentDiv = safeFragment.appendChild(document.createElement("div"));
          wrapMap.optgroup = wrapMap.option;
          wrapMap.tbody = wrapMap.tfoot = wrapMap.colgroup = wrapMap.caption = wrapMap.thead;
          wrapMap.th = wrapMap.td;
          function getAll(context, tag) {
            var elems,
              elem,
              i = 0,
              found = typeof context.getElementsByTagName !== strundefined
                ? context.getElementsByTagName(tag || "*")
                : typeof context.querySelectorAll !== strundefined
                  ? context.querySelectorAll(tag || "*")
                  : undefined;
            if (!found) {
              for (found = [], elems = context.childNodes || context; (elem = elems[i]) != null; i++) {
                if (!tag || jQuery.nodeName(elem, tag)) {
                  found.push(elem)
                } else {
                  jQuery.merge(found, getAll(elem, tag))
                }
              }
            }
            return tag === undefined || tag && jQuery.nodeName(context, tag)
              ? jQuery.merge([context], found)
              : found
          }
          function fixDefaultChecked(elem) {
            if (rcheckableType.test(elem.type)) {
              elem.defaultChecked = elem.checked
            }
          }
          function manipulationTarget(elem, content) {
            return jQuery.nodeName(elem, "table") && jQuery.nodeName(content.nodeType !== 11
              ? content
              : content.firstChild, "tr")
              ? elem.getElementsByTagName("tbody")[0] || elem.appendChild(elem.ownerDocument.createElement("tbody"))
              : elem
          }
          function disableScript(elem) {
            elem.type = (jQuery.find.attr(elem, "type") !== null) + "/" + elem.type;
            return elem
          }
          function restoreScript(elem) {
            var match = rscriptTypeMasked.exec(elem.type);
            if (match) {
              elem.type = match[1]
            } else {
              elem.removeAttribute("type")
            }
            return elem
          }
          function setGlobalEval(elems, refElements) {
            var elem,
              i = 0;
            for (; (elem = elems[i]) != null; i++) {
              jQuery._data(elem, "globalEval", !refElements || jQuery._data(refElements[i], "globalEval"))
            }
          }
          function cloneCopyEvent(src, dest) {
            if (dest.nodeType !== 1 || !jQuery.hasData(src)) {
              return
            }
            var type,
              i,
              l,
              oldData = jQuery._data(src),
              curData = jQuery._data(dest, oldData),
              events = oldData.events;
            if (events) {
              delete curData.handle;
              curData.events = {};
              for (type in events) {
                for (i = 0, l = events[type].length; i < l; i++) {
                  jQuery.event.add(dest, type, events[type][i])
                }
              }
            }
            if (curData.data) {
              curData.data = jQuery.extend({}, curData.data)
            }
          }
          function fixCloneNodeIssues(src, dest) {
            var nodeName,
              e,
              data;
            if (dest.nodeType !== 1) {
              return
            }
            nodeName = dest.nodeName.toLowerCase();
            if (!support.noCloneEvent && dest[jQuery.expando]) {
              data = jQuery._data(dest);
              for (e in data.events) {
                jQuery.removeEvent(dest, e, data.handle)
              }
              dest.removeAttribute(jQuery.expando)
            }
            if (nodeName === "script" && dest.text !== src.text) {
              disableScript(dest).text = src.text;
              restoreScript(dest)
            } else if (nodeName === "object") {
              if (dest.parentNode) {
                dest.outerHTML = src.outerHTML
              }
              if (support.html5Clone && (src.innerHTML && !jQuery.trim(dest.innerHTML))) {
                dest.innerHTML = src.innerHTML
              }
            } else if (nodeName === "input" && rcheckableType.test(src.type)) {
              dest.defaultChecked = dest.checked = src.checked;
              if (dest.value !== src.value) {
                dest.value = src.value
              }
            } else if (nodeName === "option") {
              dest.defaultSelected = dest.selected = src.defaultSelected
            } else if (nodeName === "input" || nodeName === "textarea") {
              dest.defaultValue = src.defaultValue
            }
          }
          jQuery.extend({
            clone: function(elem, dataAndEvents, deepDataAndEvents) {
              var destElements,
                node,
                clone,
                i,
                srcElements,
                inPage = jQuery.contains(elem.ownerDocument, elem);
              if (support.html5Clone || jQuery.isXMLDoc(elem) || !rnoshimcache.test("<" + elem.nodeName + ">")) {
                clone = elem.cloneNode(true)
              } else {
                fragmentDiv.innerHTML = elem.outerHTML;
                fragmentDiv.removeChild(clone = fragmentDiv.firstChild)
              }
              if ((!support.noCloneEvent || !support.noCloneChecked) && (elem.nodeType === 1 || elem.nodeType === 11) && !jQuery.isXMLDoc(elem)) {
                destElements = getAll(clone);
                srcElements = getAll(elem);
                for (i = 0; (node = srcElements[i]) != null; ++i) {
                  if (destElements[i]) {
                    fixCloneNodeIssues(node, destElements[i])
                  }
                }
              }
              if (dataAndEvents) {
                if (deepDataAndEvents) {
                  srcElements = srcElements || getAll(elem);
                  destElements = destElements || getAll(clone);
                  for (i = 0; (node = srcElements[i]) != null; i++) {
                    cloneCopyEvent(node, destElements[i])
                  }
                } else {
                  cloneCopyEvent(elem, clone)
                }
              }
              destElements = getAll(clone, "script");
              if (destElements.length > 0) {
                setGlobalEval(destElements, !inPage && getAll(elem, "script"))
              }
              destElements = srcElements = node = null;
              return clone
            },
            buildFragment: function(elems, context, scripts, selection) {
              var j,
                elem,
                contains,
                tmp,
                tag,
                tbody,
                wrap,
                l = elems.length,
                safe = createSafeFragment(context),
                nodes = [],
                i = 0;
              for (; i < l; i++) {
                elem = elems[i];
                if (elem || elem === 0) {
                  if (jQuery.type(elem) === "object") {
                    jQuery.merge(nodes, elem.nodeType
                      ? [elem]
                      : elem)
                  } else if (!rhtml.test(elem)) {
                    nodes.push(context.createTextNode(elem))
                  } else {
                    tmp = tmp || safe.appendChild(context.createElement("div"));
                    tag = (rtagName.exec(elem) || ["", ""])[1].toLowerCase();
                    wrap = wrapMap[tag] || wrapMap._default;
                    tmp.innerHTML = wrap[1] + elem.replace(rxhtmlTag, "<$1></$2>") + wrap[2];
                    j = wrap[0];
                    while (j--) {
                      tmp = tmp.lastChild
                    }
                    if (!support.leadingWhitespace && rleadingWhitespace.test(elem)) {
                      nodes.push(context.createTextNode(rleadingWhitespace.exec(elem)[0]))
                    }
                    if (!support.tbody) {
                      elem = tag === "table" && !rtbody.test(elem)
                        ? tmp.firstChild
                        : wrap[1] === "<table>" && !rtbody.test(elem)
                          ? tmp
                          : 0;
                      j = elem && elem.childNodes.length;
                      while (j--) {
                        if (jQuery.nodeName(tbody = elem.childNodes[j], "tbody") && !tbody.childNodes.length) {
                          elem.removeChild(tbody)
                        }
                      }
                    }
                    jQuery.merge(nodes, tmp.childNodes);
                    tmp.textContent = "";
                    while (tmp.firstChild) {
                      tmp.removeChild(tmp.firstChild)
                    }
                    tmp = safe.lastChild
                  }
                }
              }
              if (tmp) {
                safe.removeChild(tmp)
              }
              if (!support.appendChecked) {
                jQuery.grep(getAll(nodes, "input"), fixDefaultChecked)
              }
              i = 0;
              while (elem = nodes[i++]) {
                if (selection && jQuery.inArray(elem, selection) !== -1) {
                  continue
                }
                contains = jQuery.contains(elem.ownerDocument, elem);
                tmp = getAll(safe.appendChild(elem), "script");
                if (contains) {
                  setGlobalEval(tmp)
                }
                if (scripts) {
                  j = 0;
                  while (elem = tmp[j++]) {
                    if (rscriptType.test(elem.type || "")) {
                      scripts.push(elem)
                    }
                  }
                }
              }
              tmp = null;
              return safe
            },
            cleanData: function(elems, acceptData) {
              var elem,
                type,
                id,
                data,
                i = 0,
                internalKey = jQuery.expando,
                cache = jQuery.cache,
                deleteExpando = support.deleteExpando,
                special = jQuery.event.special;
              for (; (elem = elems[i]) != null; i++) {
                if (acceptData || jQuery.acceptData(elem)) {
                  id = elem[internalKey];
                  data = id && cache[id];
                  if (data) {
                    if (data.events) {
                      for (type in data.events) {
                        if (special[type]) {
                          jQuery.event.remove(elem, type)
                        } else {
                          jQuery.removeEvent(elem, type, data.handle)
                        }
                      }
                    }
                    if (cache[id]) {
                      delete cache[id];
                      if (deleteExpando) {
                        delete elem[internalKey]
                      } else if (typeof elem.removeAttribute !== strundefined) {
                        elem.removeAttribute(internalKey)
                      } else {
                        elem[internalKey] = null
                      }
                      deletedIds.push(id)
                    }
                  }
                }
              }
            }
          });
          jQuery.fn.extend({
            text: function(value) {
              return access(this, function(value) {
                return value === undefined
                  ? jQuery.text(this)
                  : this.empty().append((this[0] && this[0].ownerDocument || document).createTextNode(value))
              }, null, value, arguments.length)
            },
            append: function() {
              return this.domManip(arguments, function(elem) {
                if (this.nodeType === 1 || this.nodeType === 11 || this.nodeType === 9) {
                  var target = manipulationTarget(this, elem);
                  target.appendChild(elem)
                }
              })
            },
            prepend: function() {
              return this.domManip(arguments, function(elem) {
                if (this.nodeType === 1 || this.nodeType === 11 || this.nodeType === 9) {
                  var target = manipulationTarget(this, elem);
                  target.insertBefore(elem, target.firstChild)
                }
              })
            },
            before: function() {
              return this.domManip(arguments, function(elem) {
                if (this.parentNode) {
                  this.parentNode.insertBefore(elem, this)
                }
              })
            },
            after: function() {
              return this.domManip(arguments, function(elem) {
                if (this.parentNode) {
                  this.parentNode.insertBefore(elem, this.nextSibling)
                }
              })
            },
            remove: function(selector, keepData) {
              var elem,
                elems = selector
                  ? jQuery.filter(selector, this)
                  : this,
                i = 0;
              for (; (elem = elems[i]) != null; i++) {
                if (!keepData && elem.nodeType === 1) {
                  jQuery.cleanData(getAll(elem))
                }
                if (elem.parentNode) {
                  if (keepData && jQuery.contains(elem.ownerDocument, elem)) {
                    setGlobalEval(getAll(elem, "script"))
                  }
                  elem.parentNode.removeChild(elem)
                }
              }
              return this
            },
            empty: function() {
              var elem,
                i = 0;
              for (; (elem = this[i]) != null; i++) {
                if (elem.nodeType === 1) {
                  jQuery.cleanData(getAll(elem, false))
                }
                while (elem.firstChild) {
                  elem.removeChild(elem.firstChild)
                }
                if (elem.options && jQuery.nodeName(elem, "select")) {
                  elem.options.length = 0
                }
              }
              return this
            },
            clone: function(dataAndEvents, deepDataAndEvents) {
              dataAndEvents = dataAndEvents == null
                ? false
                : dataAndEvents;
              deepDataAndEvents = deepDataAndEvents == null
                ? dataAndEvents
                : deepDataAndEvents;
              return this.map(function() {
                return jQuery.clone(this, dataAndEvents, deepDataAndEvents)
              })
            },
            html: function(value) {
              return access(this, function(value) {
                var elem = this[0] || {},
                  i = 0,
                  l = this.length;
                if (value === undefined) {
                  return elem.nodeType === 1
                    ? elem.innerHTML.replace(rinlinejQuery, "")
                    : undefined
                }
                if (typeof value === "string" && !rnoInnerhtml.test(value) && (support.htmlSerialize || !rnoshimcache.test(value)) && (support.leadingWhitespace || !rleadingWhitespace.test(value)) && !wrapMap[(rtagName.exec(value) || ["", ""])[1].toLowerCase()]) {
                  value = value.replace(rxhtmlTag, "<$1></$2>");
                  try {
                    for (; i < l; i++) {
                      elem = this[i] || {};
                      if (elem.nodeType === 1) {
                        jQuery.cleanData(getAll(elem, false));
                        elem.innerHTML = value
                      }
                    }
                    elem = 0
                  } catch (e) {}
                }
                if (elem) {
                  this.empty().append(value)
                }
              }, null, value, arguments.length)
            },
            replaceWith: function() {
              var arg = arguments[0];
              this.domManip(arguments, function(elem) {
                arg = this.parentNode;
                jQuery.cleanData(getAll(this));
                if (arg) {
                  arg.replaceChild(elem, this)
                }
              });
              return arg && (arg.length || arg.nodeType)
                ? this
                : this.remove()
            },
            detach: function(selector) {
              return this.remove(selector, true)
            },
            domManip: function(args, callback) {
              args = concat.apply([], args);
              var first,
                node,
                hasScripts,
                scripts,
                doc,
                fragment,
                i = 0,
                l = this.length,
                set = this,
                iNoClone = l - 1,
                value = args[0],
                isFunction = jQuery.isFunction(value);
              if (isFunction || l > 1 && typeof value === "string" && !support.checkClone && rchecked.test(value)) {
                return this.each(function(index) {
                  var self = set.eq(index);
                  if (isFunction) {
                    args[0] = value.call(this, index, self.html())
                  }
                  self.domManip(args, callback)
                })
              }
              if (l) {
                fragment = jQuery.buildFragment(args, this[0].ownerDocument, false, this);
                first = fragment.firstChild;
                if (fragment.childNodes.length === 1) {
                  fragment = first
                }
                if (first) {
                  scripts = jQuery.map(getAll(fragment, "script"), disableScript);
                  hasScripts = scripts.length;
                  for (; i < l; i++) {
                    node = fragment;
                    if (i !== iNoClone) {
                      node = jQuery.clone(node, true, true);
                      if (hasScripts) {
                        jQuery.merge(scripts, getAll(node, "script"))
                      }
                    }
                    callback.call(this[i], node, i)
                  }
                  if (hasScripts) {
                    doc = scripts[scripts.length - 1].ownerDocument;
                    jQuery.map(scripts, restoreScript);
                    for (i = 0; i < hasScripts; i++) {
                      node = scripts[i];
                      if (rscriptType.test(node.type || "") && !jQuery._data(node, "globalEval") && jQuery.contains(doc, node)) {
                        if (node.src) {
                          if (jQuery._evalUrl) {
                            jQuery._evalUrl(node.src)
                          }
                        } else {
                          jQuery.globalEval((node.text || node.textContent || node.innerHTML || "").replace(rcleanScript, ""))
                        }
                      }
                    }
                  }
                  fragment = first = null
                }
              }
              return this
            }
          });
          jQuery.each({
            appendTo: "append",
            prependTo: "prepend",
            insertBefore: "before",
            insertAfter: "after",
            replaceAll: "replaceWith"
          }, function(name, original) {
            jQuery.fn[name] = function(selector) {
              var elems,
                i = 0,
                ret = [],
                insert = jQuery(selector),
                last = insert.length - 1;
              for (; i <= last; i++) {
                elems = i === last
                  ? this
                  : this.clone(true);
                jQuery(insert[i])[original](elems);
                push.apply(ret, elems.get())
              }
              return this.pushStack(ret)
            }
          });
          var iframe,
            elemdisplay = {};
          function actualDisplay(name, doc) {
            var style,
              elem = jQuery(doc.createElement(name)).appendTo(doc.body),
              display = window.getDefaultComputedStyle && (style = window.getDefaultComputedStyle(elem[0]))
                ? style.display
                : jQuery.css(elem[0], "display");
            elem.detach();
            return display
          }
          function defaultDisplay(nodeName) {
            var doc = document,
              display = elemdisplay[nodeName];
            if (!display) {
              display = actualDisplay(nodeName, doc);
              if (display === "none" || !display) {
                iframe = (iframe || jQuery("<iframe frameborder='0' width='0' height='0'/>")).appendTo(doc.documentElement);
                doc = (iframe[0].contentWindow || iframe[0].contentDocument).document;
                doc.write();
                doc.close();
                display = actualDisplay(nodeName, doc);
                iframe.detach()
              }
              elemdisplay[nodeName] = display
            }
            return display
          }(function() {
            var shrinkWrapBlocksVal;
            support.shrinkWrapBlocks = function() {
              if (shrinkWrapBlocksVal != null) {
                return shrinkWrapBlocksVal
              }
              shrinkWrapBlocksVal = false;
              var div,
                body,
                container;
              body = document.getElementsByTagName("body")[0];
              if (!body || !body.style) {
                return
              }
              div = document.createElement("div");
              container = document.createElement("div");
              container.style.cssText = "position:absolute;border:0;width:0;height:0;top:0;left:-9999px";
              body.appendChild(container).appendChild(div);
              if (typeof div.style.zoom !== strundefined) {
                div.style.cssText = "-webkit-box-sizing:content-box;-moz-box-sizing:content-box;" +
                  "box-sizing:content-box;display:block;margin:0;border:0;" +
                  "padding:1px;width:1px;zoom:1";
                div.appendChild(document.createElement("div")).style.width = "5px";
                shrinkWrapBlocksVal = div.offsetWidth !== 3
              }
              body.removeChild(container);
              return shrinkWrapBlocksVal
            }
          })();
          var rmargin = /^margin/;
          var rnumnonpx = new RegExp("^(" + pnum + ")(?!px)[a-z%]+$", "i");
          var getStyles,
            curCSS,
            rposition = /^(top|right|bottom|left)$/;
          if (window.getComputedStyle) {
            getStyles = function(elem) {
              if (elem.ownerDocument.defaultView.opener) {
                return elem.ownerDocument.defaultView.getComputedStyle(elem, null)
              }
              return window.getComputedStyle(elem, null)
            };
            curCSS = function(elem, name, computed) {
              var width,
                minWidth,
                maxWidth,
                ret,
                style = elem.style;
              computed = computed || getStyles(elem);
              ret = computed
                ? computed.getPropertyValue(name) || computed[name]
                : undefined;
              if (computed) {
                if (ret === "" && !jQuery.contains(elem.ownerDocument, elem)) {
                  ret = jQuery.style(elem, name)
                }
                if (rnumnonpx.test(ret) && rmargin.test(name)) {
                  width = style.width;
                  minWidth = style.minWidth;
                  maxWidth = style.maxWidth;
                  style.minWidth = style.maxWidth = style.width = ret;
                  ret = computed.width;
                  style.width = width;
                  style.minWidth = minWidth;
                  style.maxWidth = maxWidth
                }
              }
              return ret === undefined
                ? ret
                : ret + ""
            }
          } else if (document.documentElement.currentStyle) {
            getStyles = function(elem) {
              return elem.currentStyle
            };
            curCSS = function(elem, name, computed) {
              var left,
                rs,
                rsLeft,
                ret,
                style = elem.style;
              computed = computed || getStyles(elem);
              ret = computed
                ? computed[name]
                : undefined;
              if (ret == null && style && style[name]) {
                ret = style[name]
              }
              if (rnumnonpx.test(ret) && !rposition.test(name)) {
                left = style.left;
                rs = elem.runtimeStyle;
                rsLeft = rs && rs.left;
                if (rsLeft) {
                  rs.left = elem.currentStyle.left
                }
                style.left = name === "fontSize"
                  ? "1em"
                  : ret;
                ret = style.pixelLeft + "px";
                style.left = left;
                if (rsLeft) {
                  rs.left = rsLeft
                }
              }
              return ret === undefined
                ? ret
                : ret + "" || "auto"
            }
          }
          function addGetHookIf(conditionFn, hookFn) {
            return {
              get: function() {
                var condition = conditionFn();
                if (condition == null) {
                  return
                }
                if (condition) {
                  delete this.get;
                  return
                }
                return (this.get = hookFn).apply(this, arguments)
              }
            }
          }(function() {
            var div,
              style,
              a,
              pixelPositionVal,
              boxSizingReliableVal,
              reliableHiddenOffsetsVal,
              reliableMarginRightVal;
            div = document.createElement("div");
            div.innerHTML = "  <link/><table></table><a href='/a'>a</a><input type='checkbox'/>";
            a = div.getElementsByTagName("a")[0];
            style = a && a.style;
            if (!style) {
              return
            }
            style.cssText = "float:left;opacity:.5";
            support.opacity = style.opacity === "0.5";
            support.cssFloat = !!style.cssFloat;
            div.style.backgroundClip = "content-box";
            div.cloneNode(true).style.backgroundClip = "";
            support.clearCloneStyle = div.style.backgroundClip === "content-box";
            support.boxSizing = style.boxSizing === "" || style.MozBoxSizing === "" || style.WebkitBoxSizing === "";
            jQuery.extend(support, {
              reliableHiddenOffsets: function() {
                if (reliableHiddenOffsetsVal == null) {
                  computeStyleTests()
                }
                return reliableHiddenOffsetsVal
              },
              boxSizingReliable: function() {
                if (boxSizingReliableVal == null) {
                  computeStyleTests()
                }
                return boxSizingReliableVal
              },
              pixelPosition: function() {
                if (pixelPositionVal == null) {
                  computeStyleTests()
                }
                return pixelPositionVal
              },
              reliableMarginRight: function() {
                if (reliableMarginRightVal == null) {
                  computeStyleTests()
                }
                return reliableMarginRightVal
              }
            });
            function computeStyleTests() {
              var div,
                body,
                container,
                contents;
              body = document.getElementsByTagName("body")[0];
              if (!body || !body.style) {
                return
              }
              div = document.createElement("div");
              container = document.createElement("div");
              container.style.cssText = "position:absolute;border:0;width:0;height:0;top:0;left:-9999px";
              body.appendChild(container).appendChild(div);
              div.style.cssText = "-webkit-box-sizing:border-box;-moz-box-sizing:border-box;" +
                "box-sizing:border-box;display:block;margin-top:1%;top:1%;" +
                "border:1px;padding:1px;width:4px;position:absolute";
              pixelPositionVal = boxSizingReliableVal = false;
              reliableMarginRightVal = true;
              if (window.getComputedStyle) {
                pixelPositionVal = (window.getComputedStyle(div, null) || {}).top !== "1%";
                boxSizingReliableVal = (window.getComputedStyle(div, null) || {
                  width: "4px"
                }).width === "4px";
                contents = div.appendChild(document.createElement("div"));
                contents.style.cssText = div.style.cssText = "-webkit-box-sizing:content-box;-moz-box-sizing:content-box;" +
                  "box-sizing:content-box;display:block;margin:0;border:0;padding:0";
                contents.style.marginRight = contents.style.width = "0";
                div.style.width = "1px";
                reliableMarginRightVal = !parseFloat((window.getComputedStyle(contents, null) || {}).marginRight);
                div.removeChild(contents)
              }
              div.innerHTML = "<table><tr><td></td><td>t</td></tr></table>";
              contents = div.getElementsByTagName("td");
              contents[0].style.cssText = "margin:0;border:0;padding:0;display:none";
              reliableHiddenOffsetsVal = contents[0].offsetHeight === 0;
              if (reliableHiddenOffsetsVal) {
                contents[0].style.display = "";
                contents[1].style.display = "none";
                reliableHiddenOffsetsVal = contents[0].offsetHeight === 0
              }
              body.removeChild(container)
            }
          })();
          jQuery.swap = function(elem, options, callback, args) {
            var ret,
              name,
              old = {};
            for (name in options) {
              old[name] = elem.style[name];
              elem.style[name] = options[name]
            }
            ret = callback.apply(elem, args || []);
            for (name in options) {
              elem.style[name] = old[name]
            }
            return ret
          };
          var ralpha = /alpha\([^)]*\)/i,
            ropacity = /opacity\s*=\s*([^)]*)/,
            rdisplayswap = /^(none|table(?!-c[ea]).+)/,
            rnumsplit = new RegExp("^(" + pnum + ")(.*)$", "i"),
            rrelNum = new RegExp("^([+-])=(" + pnum + ")", "i"),
            cssShow = {
              position: "absolute",
              visibility: "hidden",
              display: "block"
            },
            cssNormalTransform = {
              letterSpacing: "0",
              fontWeight: "400"
            },
            cssPrefixes = ["Webkit", "O", "Moz", "ms"];
          function vendorPropName(style, name) {
            if (name in style) {
              return name
            }
            var capName = name.charAt(0).toUpperCase() + name.slice(1),
              origName = name,
              i = cssPrefixes.length;
            while (i--) {
              name = cssPrefixes[i] + capName;
              if (name in style) {
                return name
              }
            }
            return origName
          }
          function showHide(elements, show) {
            if (elements.hasClass('annotator-checkbox')) {
              return elements;
            }
            var display,
              elem,
              hidden,
              values = [],
              index = 0,
              length = elements.length;
            for (; index < length; index++) {
              elem = elements[index];
              if (!elem.style) {
                continue
              }
              values[index] = jQuery._data(elem, "olddisplay");
              display = elem.style.display;
              if (show) {
                if (!values[index] && display === "none") {
                  elem.style.display = ""
                }
                if (elem.style.display === "" && isHidden(elem)) {
                  values[index] = jQuery._data(elem, "olddisplay", defaultDisplay(elem.nodeName))
                }
              } else {
                hidden = isHidden(elem);
                if (display && display !== "none" || !hidden) {
                  jQuery._data(elem, "olddisplay", hidden
                    ? display
                    : jQuery.css(elem, "display"))
                }
              }
            }
            for (index = 0; index < length; index++) {
              elem = elements[index];
              if (!elem.style) {
                continue
              }
              if (!show || elem.style.display === "none" || elem.style.display === "") {
                elem.style.display = show
                  ? values[index] || ""
                  : "none"
              }
            }
            return elements
          }
          function setPositiveNumber(elem, value, subtract) {
            var matches = rnumsplit.exec(value);
            return matches
              ? Math.max(0, matches[1] - (subtract || 0)) + (matches[2] || "px")
              : value
          }
          function augmentWidthOrHeight(elem, name, extra, isBorderBox, styles) {
            var i = extra === (isBorderBox
                ? "border"
                : "content")
                ? 4
                : name === "width"
                  ? 1
                  : 0,
              val = 0;
            for (; i < 4; i += 2) {
              if (extra === "margin") {
                val += jQuery.css(elem, extra + cssExpand[i], true, styles)
              }
              if (isBorderBox) {
                if (extra === "content") {
                  val -= jQuery.css(elem, "padding" + cssExpand[i], true, styles)
                }
                if (extra !== "margin") {
                  val -= jQuery.css(elem, "border" + cssExpand[i] + "Width", true, styles)
                }
              } else {
                val += jQuery.css(elem, "padding" + cssExpand[i], true, styles);
                if (extra !== "padding") {
                  val += jQuery.css(elem, "border" + cssExpand[i] + "Width", true, styles)
                }
              }
            }
            return val
          }
          function getWidthOrHeight(elem, name, extra) {
            var valueIsBorderBox = true,
              val = name === "width"
                ? elem.offsetWidth
                : elem.offsetHeight,
              styles = getStyles(elem),
              isBorderBox = support.boxSizing && jQuery.css(elem, "boxSizing", false, styles) === "border-box";
            if (val <= 0 || val == null) {
              val = curCSS(elem, name, styles);
              if (val < 0 || val == null) {
                val = elem.style[name]
              }
              if (rnumnonpx.test(val)) {
                return val
              }
              valueIsBorderBox = isBorderBox && (support.boxSizingReliable() || val === elem.style[name]);
              val = parseFloat(val) || 0
            }
            return val + augmentWidthOrHeight(elem, name, extra || (isBorderBox
              ? "border"
              : "content"), valueIsBorderBox, styles) + "px"
          }
          jQuery.extend({
            cssHooks: {
              opacity: {
                get: function(elem, computed) {
                  if (computed) {
                    var ret = curCSS(elem, "opacity");
                    return ret === ""
                      ? "1"
                      : ret
                  }
                }
              }
            },
            cssNumber: {
              columnCount: true,
              fillOpacity: true,
              flexGrow: true,
              flexShrink: true,
              fontWeight: true,
              lineHeight: true,
              opacity: true,
              order: true,
              orphans: true,
              widows: true,
              zIndex: true,
              zoom: true
            },
            cssProps: {
              "float": support.cssFloat
                ? "cssFloat"
                : "styleFloat"
            },
            style: function(elem, name, value, extra) {
              if (!elem || elem.nodeType === 3 || elem.nodeType === 8 || !elem.style) {
                return
              }
              var ret,
                type,
                hooks,
                origName = jQuery.camelCase(name),
                style = elem.style;
              name = jQuery.cssProps[origName] || (jQuery.cssProps[origName] = vendorPropName(style, origName));
              hooks = jQuery.cssHooks[name] || jQuery.cssHooks[origName];
              if (value !== undefined) {
                type = typeof value;
                if (type === "string" && (ret = rrelNum.exec(value))) {
                  value = (ret[1] + 1) * ret[2] + parseFloat(jQuery.css(elem, name));
                  type = "number"
                }
                if (value == null || value !== value) {
                  return
                }
                if (type === "number" && !jQuery.cssNumber[origName]) {
                  value += "px"
                }
                if (!support.clearCloneStyle && value === "" && name.indexOf("background") === 0) {
                  style[name] = "inherit"
                }
                if (!hooks || !("set" in hooks) || (value = hooks.set(elem, value, extra)) !== undefined) {
                  try {
                    style[name] = value
                  } catch (e) {}
                }
              } else {
                if (hooks && "get" in hooks && (ret = hooks.get(elem, false, extra)) !== undefined) {
                  return ret
                }
                return style[name]
              }
            },
            css: function(elem, name, extra, styles) {
              var num,
                val,
                hooks,
                origName = jQuery.camelCase(name);
              name = jQuery.cssProps[origName] || (jQuery.cssProps[origName] = vendorPropName(elem.style, origName));
              hooks = jQuery.cssHooks[name] || jQuery.cssHooks[origName];
              if (hooks && "get" in hooks) {
                val = hooks.get(elem, true, extra)
              }
              if (val === undefined) {
                val = curCSS(elem, name, styles)
              }
              if (val === "normal" && name in cssNormalTransform) {
                val = cssNormalTransform[name]
              }
              if (extra === "" || extra) {
                num = parseFloat(val);
                return extra === true || jQuery.isNumeric(num)
                  ? num || 0
                  : val
              }
              return val
            }
          });
          jQuery.each([
            "height", "width"
          ], function(i, name) {
            jQuery.cssHooks[name] = {
              get: function(elem, computed, extra) {
                if (computed) {
                  return rdisplayswap.test(jQuery.css(elem, "display")) && elem.offsetWidth === 0
                    ? jQuery.swap(elem, cssShow, function() {
                      return getWidthOrHeight(elem, name, extra)
                    })
                    : getWidthOrHeight(elem, name, extra)
                }
              },
              set: function(elem, value, extra) {
                var styles = extra && getStyles(elem);
                return setPositiveNumber(elem, value, extra
                  ? augmentWidthOrHeight(elem, name, extra, support.boxSizing && jQuery.css(elem, "boxSizing", false, styles) === "border-box", styles)
                  : 0)
              }
            }
          });
          if (!support.opacity) {
            jQuery.cssHooks.opacity = {
              get: function(elem, computed) {
                return ropacity.test((computed && elem.currentStyle
                  ? elem.currentStyle.filter
                  : elem.style.filter) || "")
                  ? .01 * parseFloat(RegExp.$1) + ""
                  : computed
                    ? "1"
                    : ""
              },
              set: function(elem, value) {
                var style = elem.style,
                  currentStyle = elem.currentStyle,
                  opacity = jQuery.isNumeric(value)
                    ? "alpha(opacity=" + value * 100 + ")"
                    : "",
                  filter = currentStyle && currentStyle.filter || style.filter || "";
                style.zoom = 1;
                if ((value >= 1 || value === "") && jQuery.trim(filter.replace(ralpha, "")) === "" && style.removeAttribute) {
                  style.removeAttribute("filter");
                  if (value === "" || currentStyle && !currentStyle.filter) {
                    return
                  }
                }
                style.filter = ralpha.test(filter)
                  ? filter.replace(ralpha, opacity)
                  : filter + " " + opacity
              }
            }
          }
          jQuery.cssHooks.marginRight = addGetHookIf(support.reliableMarginRight, function(elem, computed) {
            if (computed) {
              return jQuery.swap(elem, {
                display: "inline-block"
              }, curCSS, [elem, "marginRight"])
            }
          });
          jQuery.each({
            margin: "",
            padding: "",
            border: "Width"
          }, function(prefix, suffix) {
            jQuery.cssHooks[prefix + suffix] = {
              expand: function(value) {
                var i = 0,
                  expanded = {},
                  parts = typeof value === "string"
                    ? value.split(" ")
                    : [value];
                for (; i < 4; i++) {
                  expanded[prefix + cssExpand[i] + suffix] = parts[i] || parts[i - 2] || parts[0]
                }
                return expanded
              }
            };
            if (!rmargin.test(prefix)) {
              jQuery.cssHooks[prefix + suffix].set = setPositiveNumber
            }
          });
          jQuery.fn.extend({
            css: function(name, value) {
              return access(this, function(elem, name, value) {
                var styles,
                  len,
                  map = {},
                  i = 0;
                if (jQuery.isArray(name)) {
                  styles = getStyles(elem);
                  len = name.length;
                  for (; i < len; i++) {
                    map[name[i]] = jQuery.css(elem, name[i], false, styles)
                  }
                  return map
                }
                return value !== undefined
                  ? jQuery.style(elem, name, value)
                  : jQuery.css(elem, name)
              }, name, value, arguments.length > 1)
            },
            show: function() {
              return showHide(this, true)
            },
            hide: function() {
              return showHide(this)
            },
            toggle: function(state) {
              if (typeof state === "boolean") {
                return state
                  ? this.show()
                  : this.hide()
              }
              return this.each(function() {
                if (isHidden(this)) {
                  jQuery(this).show()
                } else {
                  jQuery(this).hide()
                }
              })
            }
          });
          function Tween(elem, options, prop, end, easing) {
            return new Tween.prototype.init(elem, options, prop, end, easing)
          }
          jQuery.Tween = Tween;
          Tween.prototype = {
            constructor: Tween,
            init: function(elem, options, prop, end, easing, unit) {
              this.elem = elem;
              this.prop = prop;
              this.easing = easing || "swing";
              this.options = options;
              this.start = this.now = this.cur();
              this.end = end;
              this.unit = unit || (jQuery.cssNumber[prop]
                ? ""
                : "px")
            },
            cur: function() {
              var hooks = Tween.propHooks[this.prop];
              return hooks && hooks.get
                ? hooks.get(this)
                : Tween.propHooks._default.get(this)
            },
            run: function(percent) {
              var eased,
                hooks = Tween.propHooks[this.prop];
              if (this.options.duration) {
                this.pos = eased = jQuery.easing[this.easing](percent, this.options.duration * percent, 0, 1, this.options.duration)
              } else {
                this.pos = eased = percent
              }
              this.now = (this.end - this.start) * eased + this.start;
              if (this.options.step) {
                this.options.step.call(this.elem, this.now, this)
              }
              if (hooks && hooks.set) {
                hooks.set(this)
              } else {
                Tween.propHooks._default.set(this)
              }
              return this
            }
          };
          Tween.prototype.init.prototype = Tween.prototype;
          Tween.propHooks = {
            _default: {
              get: function(tween) {
                var result;
                if (tween.elem[tween.prop] != null && (!tween.elem.style || tween.elem.style[tween.prop] == null)) {
                  return tween.elem[tween.prop]
                }
                result = jQuery.css(tween.elem, tween.prop, "");
                return !result || result === "auto"
                  ? 0
                  : result
              },
              set: function(tween) {
                if (jQuery.fx.step[tween.prop]) {
                  jQuery.fx.step[tween.prop](tween)
                } else if (tween.elem.style && (tween.elem.style[jQuery.cssProps[tween.prop]] != null || jQuery.cssHooks[tween.prop])) {
                  jQuery.style(tween.elem, tween.prop, tween.now + tween.unit)
                } else {
                  tween.elem[tween.prop] = tween.now
                }
              }
            }
          };
          Tween.propHooks.scrollTop = Tween.propHooks.scrollLeft = {
            set: function(tween) {
              if (tween.elem.nodeType && tween.elem.parentNode) {
                tween.elem[tween.prop] = tween.now
              }
            }
          };
          jQuery.easing = {
            linear: function(p) {
              return p
            },
            swing: function(p) {
              return.5 - Math.cos(p * Math.PI) / 2
            }
          };
          jQuery.fx = Tween.prototype.init;
          jQuery.fx.step = {};
          var fxNow,
            timerId,
            rfxtypes = /^(?:toggle|show|hide)$/,
            rfxnum = new RegExp("^(?:([+-])=|)(" + pnum + ")([a-z%]*)$", "i"),
            rrun = /queueHooks$/,
            animationPrefilters = [defaultPrefilter],
            tweeners = {
              "*": [function(prop, value) {
                  var tween = this.createTween(prop, value),
                    target = tween.cur(),
                    parts = rfxnum.exec(value),
                    unit = parts && parts[3] || (jQuery.cssNumber[prop]
                      ? ""
                      : "px"),
                    start = (jQuery.cssNumber[prop] || unit !== "px" &&+ target) && rfxnum.exec(jQuery.css(tween.elem, prop)),
                    scale = 1,
                    maxIterations = 20;
                  if (start && start[3] !== unit) {
                    unit = unit || start[3];
                    parts = parts || [];
                    start =+ target || 1;
                    do
                      {
                        scale = scale || ".5";
                      start = start / scale;
                      jQuery.style(tween.elem, prop, start + unit)
                    } while (scale !== (scale = tween.cur() / target) && scale !== 1 && --maxIterations)
                  }
                  if (parts) {
                    start = tween.start =+ start ||+ target || 0;
                    tween.unit = unit;
                    tween.end = parts[1]
                      ? start + (parts[1] + 1) * parts[2] :+ parts[2]
                  }
                  return tween
                }
              ]
            };
          function createFxNow() {
            setTimeout(function() {
              fxNow = undefined
            });
            return fxNow = jQuery.now()
          }
          function genFx(type, includeWidth) {
            var which,
              attrs = {
                height: type
              },
              i = 0;
            includeWidth = includeWidth
              ? 1
              : 0;
            for (; i < 4; i += 2 - includeWidth) {
              which = cssExpand[i];
              attrs["margin" + which] = attrs["padding" + which] = type
            }
            if (includeWidth) {
              attrs.opacity = attrs.width = type
            }
            return attrs
          }
          function createTween(value, prop, animation) {
            var tween,
              collection = (tweeners[prop] || []).concat(tweeners["*"]),
              index = 0,
              length = collection.length;
            for (; index < length; index++) {
              if (tween = collection[index].call(animation, prop, value)) {
                return tween
              }
            }
          }
          function defaultPrefilter(elem, props, opts) {
            var prop,
              value,
              toggle,
              tween,
              hooks,
              oldfire,
              display,
              checkDisplay,
              anim = this,
              orig = {},
              style = elem.style,
              hidden = elem.nodeType && isHidden(elem),
              dataShow = jQuery._data(elem, "fxshow");
            if (!opts.queue) {
              hooks = jQuery._queueHooks(elem, "fx");
              if (hooks.unqueued == null) {
                hooks.unqueued = 0;
                oldfire = hooks.empty.fire;
                hooks.empty.fire = function() {
                  if (!hooks.unqueued) {
                    oldfire()
                  }
                }
              }
              hooks.unqueued++;
              anim.always(function() {
                anim.always(function() {
                  hooks.unqueued--;
                  if (!jQuery.queue(elem, "fx").length) {
                    hooks.empty.fire()
                  }
                })
              })
            }
            if (elem.nodeType === 1 && ("height" in props || "width" in props)) {
              opts.overflow = [style.overflow, style.overflowX, style.overflowY];
              display = jQuery.css(elem, "display");
              checkDisplay = display === "none"
                ? jQuery._data(elem, "olddisplay") || defaultDisplay(elem.nodeName)
                : display;
              if (checkDisplay === "inline" && jQuery.css(elem, "float") === "none") {
                if (!support.inlineBlockNeedsLayout || defaultDisplay(elem.nodeName) === "inline") {
                  style.display = "inline-block"
                } else {
                  style.zoom = 1
                }
              }
            }
            if (opts.overflow) {
              style.overflow = "hidden";
              if (!support.shrinkWrapBlocks()) {
                anim.always(function() {
                  style.overflow = opts.overflow[0];
                  style.overflowX = opts.overflow[1];
                  style.overflowY = opts.overflow[2]
                })
              }
            }
            for (prop in props) {
              value = props[prop];
              if (rfxtypes.exec(value)) {
                delete props[prop];
                toggle = toggle || value === "toggle";
                if (value === (hidden
                  ? "hide"
                  : "show")) {
                  if (value === "show" && dataShow && dataShow[prop] !== undefined) {
                    hidden = true
                  } else {
                    continue
                  }
                }
                orig[prop] = dataShow && dataShow[prop] || jQuery.style(elem, prop)
              } else {
                display = undefined
              }
            }
            if (!jQuery.isEmptyObject(orig)) {
              if (dataShow) {
                if ("hidden" in dataShow) {
                  hidden = dataShow.hidden
                }
              } else {
                dataShow = jQuery._data(elem, "fxshow", {})
              }
              if (toggle) {
                dataShow.hidden = !hidden
              }
              if (hidden) {
                jQuery(elem).show()
              } else {
                anim.done(function() {
                  jQuery(elem).hide()
                })
              }
              anim.done(function() {
                var prop;
                jQuery._removeData(elem, "fxshow");
                for (prop in orig) {
                  jQuery.style(elem, prop, orig[prop])
                }
              });
              for (prop in orig) {
                tween = createTween(hidden
                  ? dataShow[prop]
                  : 0, prop, anim);
                if (!(prop in dataShow)) {
                  dataShow[prop] = tween.start;
                  if (hidden) {
                    tween.end = tween.start;
                    tween.start = prop === "width" || prop === "height"
                      ? 1
                      : 0
                  }
                }
              }
            } else if ((display === "none"
              ? defaultDisplay(elem.nodeName)
              : display) === "inline") {
              style.display = display
            }
          }
          function propFilter(props, specialEasing) {
            var index,
              name,
              easing,
              value,
              hooks;
            for (index in props) {
              name = jQuery.camelCase(index);
              easing = specialEasing[name];
              value = props[index];
              if (jQuery.isArray(value)) {
                easing = value[1];
                value = props[index] = value[0]
              }
              if (index !== name) {
                props[name] = value;
                delete props[index]
              }
              hooks = jQuery.cssHooks[name];
              if (hooks && "expand" in hooks) {
                value = hooks.expand(value);
                delete props[name];
                for (index in value) {
                  if (!(index in props)) {
                    props[index] = value[index];
                    specialEasing[index] = easing
                  }
                }
              } else {
                specialEasing[name] = easing
              }
            }
          }
          function Animation(elem, properties, options) {
            var result,
              stopped,
              index = 0,
              length = animationPrefilters.length,
              deferred = jQuery.Deferred().always(function() {
                delete tick.elem
              }),
              tick = function() {
                if (stopped) {
                  return false
                }
                var currentTime = fxNow || createFxNow(),
                  remaining = Math.max(0, animation.startTime + animation.duration - currentTime),
                  temp = remaining / animation.duration || 0,
                  percent = 1 - temp,
                  index = 0,
                  length = animation.tweens.length;
                for (; index < length; index++) {
                  animation.tweens[index].run(percent)
                }
                deferred.notifyWith(elem, [animation, percent, remaining]);
                if (percent < 1 && length) {
                  return remaining
                } else {
                  deferred.resolveWith(elem, [animation]);
                  return false
                }
              },
              animation = deferred.promise({
                elem: elem,
                props: jQuery.extend({}, properties),
                opts: jQuery.extend(true, {
                  specialEasing: {}
                }, options),
                originalProperties: properties,
                originalOptions: options,
                startTime: fxNow || createFxNow(),
                duration: options.duration,
                tweens: [],
                createTween: function(prop, end) {
                  var tween = jQuery.Tween(elem, animation.opts, prop, end, animation.opts.specialEasing[prop] || animation.opts.easing);
                  animation.tweens.push(tween);
                  return tween
                },
                stop: function(gotoEnd) {
                  var index = 0,
                    length = gotoEnd
                      ? animation.tweens.length
                      : 0;
                  if (stopped) {
                    return this
                  }
                  stopped = true;
                  for (; index < length; index++) {
                    animation.tweens[index].run(1)
                  }
                  if (gotoEnd) {
                    deferred.resolveWith(elem, [animation, gotoEnd])
                  } else {
                    deferred.rejectWith(elem, [animation, gotoEnd])
                  }
                  return this
                }
              }),
              props = animation.props;
            propFilter(props, animation.opts.specialEasing);
            for (; index < length; index++) {
              result = animationPrefilters[index].call(animation, elem, props, animation.opts);
              if (result) {
                return result
              }
            }
            jQuery.map(props, createTween, animation);
            if (jQuery.isFunction(animation.opts.start)) {
              animation.opts.start.call(elem, animation)
            }
            jQuery.fx.timer(jQuery.extend(tick, {
              elem: elem,
              anim: animation,
              queue: animation.opts.queue
            }));
            return animation.progress(animation.opts.progress).done(animation.opts.done, animation.opts.complete).fail(animation.opts.fail).always(animation.opts.always)
          }
          jQuery.Animation = jQuery.extend(Animation, {
            tweener: function(props, callback) {
              if (jQuery.isFunction(props)) {
                callback = props;
                props = ["*"]
              } else {
                props = props.split(" ")
              }
              var prop,
                index = 0,
                length = props.length;
              for (; index < length; index++) {
                prop = props[index];
                tweeners[prop] = tweeners[prop] || [];
                tweeners[prop].unshift(callback)
              }
            },
            prefilter: function(callback, prepend) {
              if (prepend) {
                animationPrefilters.unshift(callback)
              } else {
                animationPrefilters.push(callback)
              }
            }
          });
          jQuery.speed = function(speed, easing, fn) {
            var opt = speed && typeof speed === "object"
              ? jQuery.extend({}, speed)
              : {
                complete: fn || !fn && easing || jQuery.isFunction(speed) && speed,
                duration: speed,
                easing: fn && easing || easing && !jQuery.isFunction(easing) && easing
              };
            opt.duration = jQuery.fx.off
              ? 0
              : typeof opt.duration === "number"
                ? opt.duration
                : opt.duration in jQuery.fx.speeds
                  ? jQuery.fx.speeds[opt.duration]
                  : jQuery.fx.speeds._default;
            if (opt.queue == null || opt.queue === true) {
              opt.queue = "fx"
            }
            opt.old = opt.complete;
            opt.complete = function() {
              if (jQuery.isFunction(opt.old)) {
                opt.old.call(this)
              }
              if (opt.queue) {
                jQuery.dequeue(this, opt.queue)
              }
            };
            return opt
          };
          jQuery.fn.extend({
            fadeTo: function(speed, to, easing, callback) {
              return this.filter(isHidden).css("opacity", 0).show().end().animate({
                opacity: to
              }, speed, easing, callback)
            },
            animate: function(prop, speed, easing, callback) {
              var empty = jQuery.isEmptyObject(prop),
                optall = jQuery.speed(speed, easing, callback),
                doAnimation = function() {
                  var anim = Animation(this, jQuery.extend({}, prop), optall);
                  if (empty || jQuery._data(this, "finish")) {
                    anim.stop(true)
                  }
                };
              doAnimation.finish = doAnimation;
              return empty || optall.queue === false
                ? this.each(doAnimation)
                : this.queue(optall.queue, doAnimation)
            },
            stop: function(type, clearQueue, gotoEnd) {
              var stopQueue = function(hooks) {
                var stop = hooks.stop;
                delete hooks.stop;
                stop(gotoEnd)
              };
              if (typeof type !== "string") {
                gotoEnd = clearQueue;
                clearQueue = type;
                type = undefined
              }
              if (clearQueue && type !== false) {
                this.queue(type || "fx", [])
              }
              return this.each(function() {
                var dequeue = true,
                  index = type != null && type + "queueHooks",
                  timers = jQuery.timers,
                  data = jQuery._data(this);
                if (index) {
                  if (data[index] && data[index].stop) {
                    stopQueue(data[index])
                  }
                } else {
                  for (index in data) {
                    if (data[index] && data[index].stop && rrun.test(index)) {
                      stopQueue(data[index])
                    }
                  }
                }
                for (index = timers.length; index--;) {
                  if (timers[index].elem === this && (type == null || timers[index].queue === type)) {
                    timers[index].anim.stop(gotoEnd);
                    dequeue = false;
                    timers.splice(index, 1)
                  }
                }
                if (dequeue || !gotoEnd) {
                  jQuery.dequeue(this, type)
                }
              })
            },
            finish: function(type) {
              if (type !== false) {
                type = type || "fx"
              }
              return this.each(function() {
                var index,
                  data = jQuery._data(this),
                  queue = data[type + "queue"],
                  hooks = data[type + "queueHooks"],
                  timers = jQuery.timers,
                  length = queue
                    ? queue.length
                    : 0;
                data.finish = true;
                jQuery.queue(this, type, []);
                if (hooks && hooks.stop) {
                  hooks.stop.call(this, true)
                }
                for (index = timers.length; index--;) {
                  if (timers[index].elem === this && timers[index].queue === type) {
                    timers[index].anim.stop(true);
                    timers.splice(index, 1)
                  }
                }
                for (index = 0; index < length; index++) {
                  if (queue[index] && queue[index].finish) {
                    queue[index].finish.call(this)
                  }
                }
                delete data.finish
              })
            }
          });
          jQuery.each([
            "toggle", "show", "hide"
          ], function(i, name) {
            var cssFn = jQuery.fn[name];
            jQuery.fn[name] = function(speed, easing, callback) {
              return speed == null || typeof speed === "boolean"
                ? cssFn.apply(this, arguments)
                : this.animate(genFx(name, true), speed, easing, callback)
            }
          });
          jQuery.each({
            slideDown: genFx("show"),
            slideUp: genFx("hide"),
            slideToggle: genFx("toggle"),
            fadeIn: {
              opacity: "show"
            },
            fadeOut: {
              opacity: "hide"
            },
            fadeToggle: {
              opacity: "toggle"
            }
          }, function(name, props) {
            jQuery.fn[name] = function(speed, easing, callback) {
              return this.animate(props, speed, easing, callback)
            }
          });
          jQuery.timers = [];
          jQuery.fx.tick = function() {
            var timer,
              timers = jQuery.timers,
              i = 0;
            fxNow = jQuery.now();
            for (; i < timers.length; i++) {
              timer = timers[i];
              if (!timer() && timers[i] === timer) {
                timers.splice(i--, 1)
              }
            }
            if (!timers.length) {
              jQuery.fx.stop()
            }
            fxNow = undefined
          };
          jQuery.fx.timer = function(timer) {
            jQuery.timers.push(timer);
            if (timer()) {
              jQuery.fx.start()
            } else {
              jQuery.timers.pop()
            }
          };
          jQuery.fx.interval = 13;
          jQuery.fx.start = function() {
            if (!timerId) {
              timerId = setInterval(jQuery.fx.tick, jQuery.fx.interval)
            }
          };
          jQuery.fx.stop = function() {
            clearInterval(timerId);
            timerId = null
          };
          jQuery.fx.speeds = {
            slow: 600,
            fast: 200,
            _default: 400
          };
          jQuery.fn.delay = function(time, type) {
            time = jQuery.fx
              ? jQuery.fx.speeds[time] || time
              : time;
            type = type || "fx";
            return this.queue(type, function(next, hooks) {
              var timeout = setTimeout(next, time);
              hooks.stop = function() {
                clearTimeout(timeout)
              }
            })
          };
          (function() {
            var input,
              div,
              select,
              a,
              opt;
            div = document.createElement("div");
            div.setAttribute("className", "t");
            div.innerHTML = "  <link/><table></table><a href='/a'>a</a><input type='checkbox'/>";
            a = div.getElementsByTagName("a")[0];
            select = document.createElement("select");
            opt = select.appendChild(document.createElement("option"));
            input = div.getElementsByTagName("input")[0];
            a.style.cssText = "top:1px";
            support.getSetAttribute = div.className !== "t";
            support.style = /top/.test(a.getAttribute("style"));
            support.hrefNormalized = a.getAttribute("href") === "/a";
            support.checkOn = !!input.value;
            support.optSelected = opt.selected;
            support.enctype = !!document.createElement("form").enctype;
            select.disabled = true;
            support.optDisabled = !opt.disabled;
            input = document.createElement("input");
            input.setAttribute("value", "");
            support.input = input.getAttribute("value") === "";
            input.value = "t";
            input.setAttribute("type", "radio");
            support.radioValue = input.value === "t"
          })();
          var rreturn = /\r/g;
          jQuery.fn.extend({
            val: function(value) {
              var hooks,
                ret,
                isFunction,
                elem = this[0];
              if (!arguments.length) {
                if (elem) {
                  hooks = jQuery.valHooks[elem.type] || jQuery.valHooks[elem.nodeName.toLowerCase()];
                  if (hooks && "get" in hooks && (ret = hooks.get(elem, "value")) !== undefined) {
                    return ret
                  }
                  ret = elem.value;
                  return typeof ret === "string"
                    ? ret.replace(rreturn, "")
                    : ret == null
                      ? ""
                      : ret
                }
                return
              }
              isFunction = jQuery.isFunction(value);
              return this.each(function(i) {
                var val;
                if (this.nodeType !== 1) {
                  return
                }
                if (isFunction) {
                  val = value.call(this, i, jQuery(this).val())
                } else {
                  val = value
                }
                if (val == null) {
                  val = ""
                } else if (typeof val === "number") {
                  val += ""
                } else if (jQuery.isArray(val)) {
                  val = jQuery.map(val, function(value) {
                    return value == null
                      ? ""
                      : value + ""
                  })
                }
                hooks = jQuery.valHooks[this.type] || jQuery.valHooks[this.nodeName.toLowerCase()];
                if (!hooks || !("set" in hooks) || hooks.set(this, val, "value") === undefined) {
                  this.value = val
                }
              })
            }
          });
          jQuery.extend({
            valHooks: {
              option: {
                get: function(elem) {
                  var val = jQuery.find.attr(elem, "value");
                  return val != null
                    ? val
                    : jQuery.trim(jQuery.text(elem))
                }
              },
              select: {
                get: function(elem) {
                  var value,
                    option,
                    options = elem.options,
                    index = elem.selectedIndex,
                    one = elem.type === "select-one" || index < 0,
                    values = one
                      ? null
                      : [],
                    max = one
                      ? index + 1
                      : options.length,
                    i = index < 0
                      ? max
                      : one
                        ? index
                        : 0;
                  for (; i < max; i++) {
                    option = options[i];
                    if ((option.selected || i === index) && (support.optDisabled
                      ? !option.disabled
                      : option.getAttribute("disabled") === null) && (!option.parentNode.disabled || !jQuery.nodeName(option.parentNode, "optgroup"))) {
                      value = jQuery(option).val();
                      if (one) {
                        return value
                      }
                      values.push(value)
                    }
                  }
                  return values
                },
                set: function(elem, value) {
                  var optionSet,
                    option,
                    options = elem.options,
                    values = jQuery.makeArray(value),
                    i = options.length;
                  while (i--) {
                    option = options[i];
                    if (jQuery.inArray(jQuery.valHooks.option.get(option), values) >= 0) {
                      try {
                        option.selected = optionSet = true
                      } catch (_) {
                        option.scrollHeight
                      }
                    } else {
                      option.selected = false
                    }
                  }
                  if (!optionSet) {
                    elem.selectedIndex = -1
                  }
                  return options
                }
              }
            }
          });
          jQuery.each([
            "radio", "checkbox"
          ], function() {
            jQuery.valHooks[this] = {
              set: function(elem, value) {
                if (jQuery.isArray(value)) {
                  return elem.checked = jQuery.inArray(jQuery(elem).val(), value) >= 0
                }
              }
            };
            if (!support.checkOn) {
              jQuery.valHooks[this].get = function(elem) {
                return elem.getAttribute("value") === null
                  ? "on"
                  : elem.value
              }
            }
          });
          var nodeHook,
            boolHook,
            attrHandle = jQuery.expr.attrHandle,
            ruseDefault = /^(?:checked|selected)$/i,
            getSetAttribute = support.getSetAttribute,
            getSetInput = support.input;
          jQuery.fn.extend({
            attr: function(name, value) {
              return access(this, jQuery.attr, name, value, arguments.length > 1)
            },
            removeAttr: function(name) {
              return this.each(function() {
                jQuery.removeAttr(this, name)
              })
            }
          });
          jQuery.extend({
            attr: function(elem, name, value) {
              var hooks,
                ret,
                nType = elem.nodeType;
              if (!elem || nType === 3 || nType === 8 || nType === 2) {
                return
              }
              if (typeof elem.getAttribute === strundefined) {
                return jQuery.prop(elem, name, value)
              }
              if (nType !== 1 || !jQuery.isXMLDoc(elem)) {
                name = name.toLowerCase();
                hooks = jQuery.attrHooks[name] || (jQuery.expr.match.bool.test(name)
                  ? boolHook
                  : nodeHook)
              }
              if (value !== undefined) {
                if (value === null) {
                  jQuery.removeAttr(elem, name)
                } else if (hooks && "set" in hooks && (ret = hooks.set(elem, value, name)) !== undefined) {
                  return ret
                } else {
                  elem.setAttribute(name, value + "");
                  return value
                }
              } else if (hooks && "get" in hooks && (ret = hooks.get(elem, name)) !== null) {
                return ret
              } else {
                ret = jQuery.find.attr(elem, name);
                return ret == null
                  ? undefined
                  : ret
              }
            },
            removeAttr: function(elem, value) {
              var name,
                propName,
                i = 0,
                attrNames = value && value.match(rnotwhite);
              if (attrNames && elem.nodeType === 1) {
                while (name = attrNames[i++]) {
                  propName = jQuery.propFix[name] || name;
                  if (jQuery.expr.match.bool.test(name)) {
                    if (getSetInput && getSetAttribute || !ruseDefault.test(name)) {
                      elem[propName] = false
                    } else {
                      elem[jQuery.camelCase("default-" + name)] = elem[propName] = false
                    }
                  } else {
                    jQuery.attr(elem, name, "")
                  }
                  elem.removeAttribute(getSetAttribute
                    ? name
                    : propName)
                }
              }
            },
            attrHooks: {
              type: {
                set: function(elem, value) {
                  if (!support.radioValue && value === "radio" && jQuery.nodeName(elem, "input")) {
                    var val = elem.value;
                    elem.setAttribute("type", value);
                    if (val) {
                      elem.value = val
                    }
                    return value
                  }
                }
              }
            }
          });
          boolHook = {
            set: function(elem, value, name) {
              if (value === false) {
                jQuery.removeAttr(elem, name)
              } else if (getSetInput && getSetAttribute || !ruseDefault.test(name)) {
                elem.setAttribute(!getSetAttribute && jQuery.propFix[name] || name, name)
              } else {
                elem[jQuery.camelCase("default-" + name)] = elem[name] = true
              }
              return name
            }
          };
          jQuery.each(jQuery.expr.match.bool.source.match(/\w+/g), function(i, name) {
            var getter = attrHandle[name] || jQuery.find.attr;
            attrHandle[name] = getSetInput && getSetAttribute || !ruseDefault.test(name)
              ? function(elem, name, isXML) {
                var ret,
                  handle;
                if (!isXML) {
                  handle = attrHandle[name];
                  attrHandle[name] = ret;
                  ret = getter(elem, name, isXML) != null
                    ? name.toLowerCase()
                    : null;
                  attrHandle[name] = handle
                }
                return ret
              }
              : function(elem, name, isXML) {
                if (!isXML) {
                  return elem[jQuery.camelCase("default-" + name)]
                    ? name.toLowerCase()
                    : null
                }
              }
          });
          if (!getSetInput || !getSetAttribute) {
            jQuery.attrHooks.value = {
              set: function(elem, value, name) {
                if (jQuery.nodeName(elem, "input")) {
                  elem.defaultValue = value
                } else {
                  return nodeHook && nodeHook.set(elem, value, name)
                }
              }
            }
          }
          if (!getSetAttribute) {
            nodeHook = {
              set: function(elem, value, name) {
                var ret = elem.getAttributeNode(name);
                if (!ret) {
                  elem.setAttributeNode(ret = elem.ownerDocument.createAttribute(name));
                }
                ret.value = value += "";
                if (name === "value" || value === elem.getAttribute(name)) {
                  return value
                }
              }
            };
            attrHandle.id = attrHandle.name = attrHandle.coords = function(elem, name, isXML) {
              var ret;
              if (!isXML) {
                return (ret = elem.getAttributeNode(name)) && ret.value !== ""
                  ? ret.value
                  : null
              }
            };
            jQuery.valHooks.button = {
              get: function(elem, name) {
                var ret = elem.getAttributeNode(name);
                if (ret && ret.specified) {
                  return ret.value
                }
              },
              set: nodeHook.set
            };
            jQuery.attrHooks.contenteditable = {
              set: function(elem, value, name) {
                nodeHook.set(elem, value === ""
                  ? false
                  : value, name)
              }
            };
            jQuery.each([
              "width", "height"
            ], function(i, name) {
              jQuery.attrHooks[name] = {
                set: function(elem, value) {
                  if (value === "") {
                    elem.setAttribute(name, "auto");
                    return value
                  }
                }
              }
            })
          }
          if (!support.style) {
            jQuery.attrHooks.style = {
              get: function(elem) {
                return elem.style.cssText || undefined
              },
              set: function(elem, value) {
                return elem.style.cssText = value + ""
              }
            }
          }
          var rfocusable = /^(?:input|select|textarea|button|object)$/i,
            rclickable = /^(?:a|area)$/i;
          jQuery.fn.extend({
            prop: function(name, value) {
              return access(this, jQuery.prop, name, value, arguments.length > 1)
            },
            removeProp: function(name) {
              name = jQuery.propFix[name] || name;
              return this.each(function() {
                try {
                  this[name] = undefined;
                  delete this[name]
                } catch (e) {}
              })
            }
          });
          jQuery.extend({
            propFix: {
              "for": "htmlFor",
              "class": "className"
            },
            prop: function(elem, name, value) {
              var ret,
                hooks,
                notxml,
                nType = elem.nodeType;
              if (!elem || nType === 3 || nType === 8 || nType === 2) {
                return
              }
              notxml = nType !== 1 || !jQuery.isXMLDoc(elem);
              if (notxml) {
                name = jQuery.propFix[name] || name;
                hooks = jQuery.propHooks[name]
              }
              if (value !== undefined) {
                return hooks && "set" in hooks && (ret = hooks.set(elem, value, name)) !== undefined
                  ? ret
                  : elem[name] = value
              } else {
                return hooks && "get" in hooks && (ret = hooks.get(elem, name)) !== null
                  ? ret
                  : elem[name]
              }
            },
            propHooks: {
              tabIndex: {
                get: function(elem) {
                  var tabindex = jQuery.find.attr(elem, "tabindex");
                  return tabindex
                    ? parseInt(tabindex, 10)
                    : rfocusable.test(elem.nodeName) || rclickable.test(elem.nodeName) && elem.href
                      ? 0
                      : -1
                }
              }
            }
          });
          if (!support.hrefNormalized) {
            jQuery.each([
              "href", "src"
            ], function(i, name) {
              jQuery.propHooks[name] = {
                get: function(elem) {
                  return elem.getAttribute(name, 4)
                }
              }
            })
          }
          if (!support.optSelected) {
            jQuery.propHooks.selected = {
              get: function(elem) {
                var parent = elem.parentNode;
                if (parent) {
                  parent.selectedIndex;
                  if (parent.parentNode) {
                    parent.parentNode.selectedIndex
                  }
                }
                return null
              }
            }
          }
          jQuery.each([
            "tabIndex",
            "readOnly",
            "maxLength",
            "cellSpacing",
            "cellPadding",
            "rowSpan",
            "colSpan",
            "useMap",
            "frameBorder",
            "contentEditable"
          ], function() {
            jQuery.propFix[this.toLowerCase()] = this
          });
          if (!support.enctype) {
            jQuery.propFix.enctype = "encoding"
          }
          var rclass = /[\t\r\n\f]/g;
          jQuery.fn.extend({
            addClass: function(value) {
              var classes,
                elem,
                cur,
                clazz,
                j,
                finalValue,
                i = 0,
                len = this.length,
                proceed = typeof value === "string" && value;
              if (jQuery.isFunction(value)) {
                return this.each(function(j) {
                  jQuery(this).addClass(value.call(this, j, this.className))
                })
              }
              if (proceed) {
                classes = (value || "").match(rnotwhite) || [];
                for (; i < len; i++) {
                  elem = this[i];
                  cur = elem.nodeType === 1 && (elem.className
                    ? (" " + elem.className + " ").replace(rclass, " ")
                    : " ");
                  if (cur) {
                    j = 0;
                    while (clazz = classes[j++]) {
                      if (cur.indexOf(" " + clazz + " ") < 0) {
                        cur += clazz + " "
                      }
                    }
                    finalValue = jQuery.trim(cur);
                    if (elem.className !== finalValue) {
                      elem.className = finalValue
                    }
                  }
                }
              }
              return this
            },
            removeClass: function(value) {
              var classes,
                elem,
                cur,
                clazz,
                j,
                finalValue,
                i = 0,
                len = this.length,
                proceed = arguments.length === 0 || typeof value === "string" && value;
              if (jQuery.isFunction(value)) {
                return this.each(function(j) {
                  jQuery(this).removeClass(value.call(this, j, this.className))
                })
              }
              if (proceed) {
                classes = (value || "").match(rnotwhite) || [];
                for (; i < len; i++) {
                  elem = this[i];
                  cur = elem.nodeType === 1 && (elem.className
                    ? (" " + elem.className + " ").replace(rclass, " ")
                    : "");
                  if (cur) {
                    j = 0;
                    while (clazz = classes[j++]) {
                      while (cur.indexOf(" " + clazz + " ") >= 0) {
                        cur = cur.replace(" " + clazz + " ", " ")
                      }
                    }
                    finalValue = value
                      ? jQuery.trim(cur)
                      : "";
                    if (elem.className !== finalValue) {
                      elem.className = finalValue
                    }
                  }
                }
              }
              return this
            },
            toggleClass: function(value, stateVal) {
              var type = typeof value;
              if (typeof stateVal === "boolean" && type === "string") {
                return stateVal
                  ? this.addClass(value)
                  : this.removeClass(value)
              }
              if (jQuery.isFunction(value)) {
                return this.each(function(i) {
                  jQuery(this).toggleClass(value.call(this, i, this.className, stateVal), stateVal)
                })
              }
              return this.each(function() {
                if (type === "string") {
                  var className,
                    i = 0,
                    self = jQuery(this),
                    classNames = value.match(rnotwhite) || [];
                  while (className = classNames[i++]) {
                    if (self.hasClass(className)) {
                      self.removeClass(className)
                    } else {
                      self.addClass(className)
                    }
                  }
                } else if (type === strundefined || type === "boolean") {
                  if (this.className) {
                    jQuery._data(this, "__className__", this.className)
                  }
                  this.className = this.className || value === false
                    ? ""
                    : jQuery._data(this, "__className__") || ""
                }
              })
            },
            hasClass: function(selector) {
              var className = " " + selector + " ",
                i = 0,
                l = this.length;
              for (; i < l; i++) {
                if (this[i].nodeType === 1 && (" " + this[i].className + " ").replace(rclass, " ").indexOf(className) >= 0) {
                  return true
                }
              }
              return false
            }
          });
          jQuery.each(("blur focus focusin focusout load resize scroll unload click dblclick " +
            "mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave " +
            "change select submit keydown keypress keyup error contextmenu").split(" "), function(i, name) {
            jQuery.fn[name] = function(data, fn) {
              return arguments.length > 0
                ? this.on(name, null, data, fn)
                : this.trigger(name)
            }
          });
          jQuery.fn.extend({
            hover: function(fnOver, fnOut) {
              return this.mouseenter(fnOver).mouseleave(fnOut || fnOver)
            },
            bind: function(types, data, fn) {
              return this.on(types, null, data, fn)
            },
            unbind: function(types, fn) {
              return this.off(types, null, fn)
            },
            delegate: function(selector, types, data, fn) {
              return this.on(types, selector, data, fn)
            },
            undelegate: function(selector, types, fn) {
              return arguments.length === 1
                ? this.off(selector, "**")
                : this.off(types, selector || "**", fn)
            }
          });
          var nonce = jQuery.now();
          var rquery = /\?/;
          var rvalidtokens = /(,)|(\[|{)|(}|])|"(?:[^"\\\r\n]|\\["\\\/bfnrt]|\\u[\da-fA-F]{4})*"\s*:?|true|false|null|-?(?!0\d)\d+(?:\.\d+|)(?:[eE][+-]?\d+|)/g;
          jQuery.parseJSON = function(data) {
            if (window.JSON && window.JSON.parse) {
              return window.JSON.parse(data + "")
            }
            var requireNonComma,
              depth = null,
              str = jQuery.trim(data + "");
            return str && !jQuery.trim(str.replace(rvalidtokens, function(token, comma, open, close) {
              if (requireNonComma && comma) {
                depth = 0
              }
              if (depth === 0) {
                return token
              }
              requireNonComma = open || comma;
              depth += !close - !open;
              return ""
            }))
              ? Function("return " + str)()
              : jQuery.error("Invalid JSON: " + data)
          };
          jQuery.parseXML = function(data) {
            var xml,
              tmp;
            if (!data || typeof data !== "string") {
              return null
            }
            try {
              if (window.DOMParser) {
                tmp = new DOMParser;
                xml = tmp.parseFromString(data, "text/xml")
              } else {
                xml = new ActiveXObject("Microsoft.XMLDOM");
                xml.async = "false";
                xml.loadXML(data)
              }
            } catch (e) {
              xml = undefined
            }
            if (!xml || !xml.documentElement || xml.getElementsByTagName("parsererror").length) {
              jQuery.error("Invalid XML: " + data)
            }
            return xml
          };
          var ajaxLocParts,
            ajaxLocation,
            rhash = /#.*$/,
            rts = /([?&])_=[^&]*/,
            rheaders = /^(.*?):[ \t]*([^\r\n]*)\r?$/gm,
            rlocalProtocol = /^(?:about|app|app-storage|.+-extension|file|res|widget):$/,
            rnoContent = /^(?:GET|HEAD)$/,
            rprotocol = /^\/\//,
            rurl = /^([\w.+-]+:)(?:\/\/(?:[^\/?#]*@|)([^\/?#:]*)(?::(\d+)|)|)/,
            prefilters = {},
            transports = {},
            allTypes = "*/".concat("*");
          try {
            ajaxLocation = location.href
          } catch (e) {
            ajaxLocation = document.createElement("a");
            ajaxLocation.href = "";
            ajaxLocation = ajaxLocation.href
          }
          ajaxLocParts = rurl.exec(ajaxLocation.toLowerCase()) || [];
          function addToPrefiltersOrTransports(structure) {
            return function(dataTypeExpression, func) {
              if (typeof dataTypeExpression !== "string") {
                func = dataTypeExpression;
                dataTypeExpression = "*"
              }
              var dataType,
                i = 0,
                dataTypes = dataTypeExpression.toLowerCase().match(rnotwhite) || [];
              if (jQuery.isFunction(func)) {
                while (dataType = dataTypes[i++]) {
                  if (dataType.charAt(0) === "+") {
                    dataType = dataType.slice(1) || "*";
                    (structure[dataType] = structure[dataType] || []).unshift(func)
                  } else {
                    (structure[dataType] = structure[dataType] || []).push(func)
                  }
                }
              }
            }
          }
          function inspectPrefiltersOrTransports(structure, options, originalOptions, jqXHR) {
            var inspected = {},
              seekingTransport = structure === transports;
            function inspect(dataType) {
              var selected;
              inspected[dataType] = true;
              jQuery.each(structure[dataType] || [], function(_, prefilterOrFactory) {
                var dataTypeOrTransport = prefilterOrFactory(options, originalOptions, jqXHR);
                if (typeof dataTypeOrTransport === "string" && !seekingTransport && !inspected[dataTypeOrTransport]) {
                  options.dataTypes.unshift(dataTypeOrTransport);
                  inspect(dataTypeOrTransport);
                  return false
                } else if (seekingTransport) {
                  return !(selected = dataTypeOrTransport)
                }
              });
              return selected
            }
            return inspect(options.dataTypes[0]) || !inspected["*"] && inspect("*")
          }
          function ajaxExtend(target, src) {
            var deep,
              key,
              flatOptions = jQuery.ajaxSettings.flatOptions || {};
            for (key in src) {
              if (src[key] !== undefined) {
                (flatOptions[key]
                  ? target
                  : deep || (deep = {}))[key] = src[key]
              }
            }
            if (deep) {
              jQuery.extend(true, target, deep)
            }
            return target
          }
          function ajaxHandleResponses(s, jqXHR, responses) {
            var firstDataType,
              ct,
              finalDataType,
              type,
              contents = s.contents,
              dataTypes = s.dataTypes;
            while (dataTypes[0] === "*") {
              dataTypes.shift();
              if (ct === undefined) {
                ct = s.mimeType || jqXHR.getResponseHeader("Content-Type")
              }
            }
            if (ct) {
              for (type in contents) {
                if (contents[type] && contents[type].test(ct)) {
                  dataTypes.unshift(type);
                  break
                }
              }
            }
            if (dataTypes[0] in responses) {
              finalDataType = dataTypes[0]
            } else {
              for (type in responses) {
                if (!dataTypes[0] || s.converters[type + " " + dataTypes[0]]) {
                  finalDataType = type;
                  break
                }
                if (!firstDataType) {
                  firstDataType = type
                }
              }
              finalDataType = finalDataType || firstDataType
            }
            if (finalDataType) {
              if (finalDataType !== dataTypes[0]) {
                dataTypes.unshift(finalDataType)
              }
              return responses[finalDataType]
            }
          }
          function ajaxConvert(s, response, jqXHR, isSuccess) {
            var conv2,
              current,
              conv,
              tmp,
              prev,
              converters = {},
              dataTypes = s.dataTypes.slice();
            if (dataTypes[1]) {
              for (conv in s.converters) {
                converters[conv.toLowerCase()] = s.converters[conv]
              }
            }
            current = dataTypes.shift();
            while (current) {
              if (s.responseFields[current]) {
                jqXHR[s.responseFields[current]] = response
              }
              if (!prev && isSuccess && s.dataFilter) {
                response = s.dataFilter(response, s.dataType)
              }
              prev = current;
              current = dataTypes.shift();
              if (current) {
                if (current === "*") {
                  current = prev
                } else if (prev !== "*" && prev !== current) {
                  conv = converters[prev + " " + current] || converters["* " + current];
                  if (!conv) {
                    for (conv2 in converters) {
                      tmp = conv2.split(" ");
                      if (tmp[1] === current) {
                        conv = converters[prev + " " + tmp[0]] || converters["* " + tmp[0]];
                        if (conv) {
                          if (conv === true) {
                            conv = converters[conv2]
                          } else if (converters[conv2] !== true) {
                            current = tmp[0];
                            dataTypes.unshift(tmp[1])
                          }
                          break
                        }
                      }
                    }
                  }
                  if (conv !== true) {
                    if (conv && s["throws"]) {
                      response = conv(response)
                    } else {
                      try {
                        response = conv(response)
                      } catch (e) {
                        return {
                          state: "parsererror",
                          error: conv
                            ? e
                            : "No conversion from " + prev + " to " + current
                        }
                      }
                    }
                  }
                }
              }
            }
            return {state: "success", data: response}
          }
          jQuery.extend({
            active: 0,
            lastModified: {},
            etag: {},
            ajaxSettings: {
              url: ajaxLocation,
              type: "GET",
              isLocal: rlocalProtocol.test(ajaxLocParts[1]),
              global: true,
              processData: true,
              async: true,
              contentType: "application/x-www-form-urlencoded; charset=UTF-8",
              accepts: {
                "*": allTypes,
                text: "text/plain",
                html: "text/html",
                xml: "application/xml, text/xml",
                json: "application/json, text/javascript"
              },
              contents: {
                xml: /xml/,
                html: /html/,
                json: /json/
              },
              responseFields: {
                xml: "responseXML",
                text: "responseText",
                json: "responseJSON"
              },
              converters: {
                "* text": String,
                "text html": true,
                "text json": jQuery.parseJSON,
                "text xml": jQuery.parseXML
              },
              flatOptions: {
                url: true,
                context: true
              }
            },
            ajaxSetup: function(target, settings) {
              return settings
                ? ajaxExtend(ajaxExtend(target, jQuery.ajaxSettings), settings)
                : ajaxExtend(jQuery.ajaxSettings, target)
            },
            ajaxPrefilter: addToPrefiltersOrTransports(prefilters),
            ajaxTransport: addToPrefiltersOrTransports(transports),
            ajax: function(url, options) {
              if (typeof url === "object") {
                options = url;
                url = undefined
              }
              options = options || {};
              var parts,
                i,
                cacheURL,
                responseHeadersString,
                timeoutTimer,
                fireGlobals,
                transport,
                responseHeaders,
                s = jQuery.ajaxSetup({}, options),
                callbackContext = s.context || s,
                globalEventContext = s.context && (callbackContext.nodeType || callbackContext.jquery)
                  ? jQuery(callbackContext)
                  : jQuery.event,
                deferred = jQuery.Deferred(),
                completeDeferred = jQuery.Callbacks("once memory"),
                statusCode = s.statusCode || {},
                requestHeaders = {},
                requestHeadersNames = {},
                state = 0,
                strAbort = "canceled",
                jqXHR = {
                  readyState: 0,
                  getResponseHeader: function(key) {
                    var match;
                    if (state === 2) {
                      if (!responseHeaders) {
                        responseHeaders = {};
                        while (match = rheaders.exec(responseHeadersString)) {
                          responseHeaders[match[1].toLowerCase()] = match[2]
                        }
                      }
                      match = responseHeaders[key.toLowerCase()]
                    }
                    return match == null
                      ? null
                      : match
                  },
                  getAllResponseHeaders: function() {
                    return state === 2
                      ? responseHeadersString
                      : null
                  },
                  setRequestHeader: function(name, value) {
                    var lname = name.toLowerCase();
                    if (!state) {
                      name = requestHeadersNames[lname] = requestHeadersNames[lname] || name;
                      requestHeaders[name] = value
                    }
                    return this
                  },
                  overrideMimeType: function(type) {
                    if (!state) {
                      s.mimeType = type
                    }
                    return this
                  },
                  statusCode: function(map) {
                    var code;
                    if (map) {
                      if (state < 2) {
                        for (code in map) {
                          statusCode[code] = [statusCode[code], map[code]]
                        }
                      } else {
                        jqXHR.always(map[jqXHR.status])
                      }
                    }
                    return this
                  },
                  abort: function(statusText) {
                    var finalText = statusText || strAbort;
                    if (transport) {
                      transport.abort(finalText)
                    }
                    done(0, finalText);
                    return this
                  }
                };
              deferred.promise(jqXHR).complete = completeDeferred.add;
              jqXHR.success = jqXHR.done;
              jqXHR.error = jqXHR.fail;
              s.url = ((url || s.url || ajaxLocation) + "").replace(rhash, "").replace(rprotocol, ajaxLocParts[1] + "//");
              s.type = options.method || options.type || s.method || s.type;
              s.dataTypes = jQuery.trim(s.dataType || "*").toLowerCase().match(rnotwhite) || [""];
              if (s.crossDomain == null) {
                parts = rurl.exec(s.url.toLowerCase());
                s.crossDomain = !!(parts && (parts[1] !== ajaxLocParts[1] || parts[2] !== ajaxLocParts[2] || (parts[3] || (parts[1] === "http:"
                  ? "80"
                  : "443")) !== (ajaxLocParts[3] || (ajaxLocParts[1] === "http:"
                  ? "80"
                  : "443"))))
              }
              if (s.data && s.processData && typeof s.data !== "string") {
                s.data = jQuery.param(s.data, s.traditional)
              }
              inspectPrefiltersOrTransports(prefilters, s, options, jqXHR);
              if (state === 2) {
                return jqXHR
              }
              fireGlobals = jQuery.event && s.global;
              if (fireGlobals && jQuery.active ++=== 0) {
                jQuery.event.trigger("ajaxStart")
              }
              s.type = s.type.toUpperCase();
              s.hasContent = !rnoContent.test(s.type);
              cacheURL = s.url;
              if (!s.hasContent) {
                if (s.data) {
                  cacheURL = s.url += (rquery.test(cacheURL)
                    ? "&"
                    : "?") + s.data;
                  delete s.data
                }
                if (s.cache === false) {
                  s.url = rts.test(cacheURL)
                    ? cacheURL.replace(rts, "$1_=" + nonce++)
                    : cacheURL + (rquery.test(cacheURL)
                      ? "&"
                      : "?") + "_=" + nonce++
                }
              }
              if (s.ifModified) {
                if (jQuery.lastModified[cacheURL]) {
                  jqXHR.setRequestHeader("If-Modified-Since", jQuery.lastModified[cacheURL])
                }
                if (jQuery.etag[cacheURL]) {
                  jqXHR.setRequestHeader("If-None-Match", jQuery.etag[cacheURL])
                }
              }
              if (s.data && s.hasContent && s.contentType !== false || options.contentType) {
                jqXHR.setRequestHeader("Content-Type", s.contentType)
              }
              jqXHR.setRequestHeader("Accept", s.dataTypes[0] && s.accepts[s.dataTypes[0]]
                ? s.accepts[s.dataTypes[0]] + (s.dataTypes[0] !== "*"
                  ? ", " + allTypes + "; q=0.01"
                  : "")
                : s.accepts["*"]);
              for (i in s.headers) {
                jqXHR.setRequestHeader(i, s.headers[i])
              }
              if (s.beforeSend && (s.beforeSend.call(callbackContext, jqXHR, s) === false || state === 2)) {
                return jqXHR.abort()
              }
              strAbort = "abort";
              for (i in {success: 1, error: 1, complete: 1}) {
                jqXHR[i](s[i])
              }
              transport = inspectPrefiltersOrTransports(transports, s, options, jqXHR);
              if (!transport) {
                done(-1, "No Transport")
              } else {
                jqXHR.readyState = 1;
                if (fireGlobals) {
                  globalEventContext.trigger("ajaxSend", [jqXHR, s])
                }
                if (s.async && s.timeout > 0) {
                  timeoutTimer = setTimeout(function() {
                    jqXHR.abort("timeout")
                  }, s.timeout)
                }
                try {
                  state = 1;
                  transport.send(requestHeaders, done)
                } catch (e) {
                  if (state < 2) {
                    done(-1, e)
                  } else {
                    throw e
                  }
                }
              }
              function done(status, nativeStatusText, responses, headers) {
                var isSuccess,
                  success,
                  error,
                  response,
                  modified,
                  statusText = nativeStatusText;
                if (state === 2) {
                  return
                }
                state = 2;
                if (timeoutTimer) {
                  clearTimeout(timeoutTimer)
                }
                transport = undefined;
                responseHeadersString = headers || "";
                jqXHR.readyState = status > 0
                  ? 4
                  : 0;
                isSuccess = status >= 200 && status < 300 || status === 304;
                if (responses) {
                  response = ajaxHandleResponses(s, jqXHR, responses)
                }
                response = ajaxConvert(s, response, jqXHR, isSuccess);
                if (isSuccess) {
                  if (s.ifModified) {
                    modified = jqXHR.getResponseHeader("Last-Modified");
                    if (modified) {
                      jQuery.lastModified[cacheURL] = modified
                    }
                    modified = jqXHR.getResponseHeader("etag");
                    if (modified) {
                      jQuery.etag[cacheURL] = modified
                    }
                  }
                  if (status === 204 || s.type === "HEAD") {
                    statusText = "nocontent"
                  } else if (status === 304) {
                    statusText = "notmodified"
                  } else {
                    statusText = response.state;
                    success = response.data;
                    error = response.error;
                    isSuccess = !error
                  }
                } else {
                  error = statusText;
                  if (status || !statusText) {
                    statusText = "error";
                    if (status < 0) {
                      status = 0
                    }
                  }
                }
                jqXHR.status = status;
                jqXHR.statusText = (nativeStatusText || statusText) + "";
                if (isSuccess) {
                  deferred.resolveWith(callbackContext, [success, statusText, jqXHR])
                } else {
                  deferred.rejectWith(callbackContext, [jqXHR, statusText, error])
                }
                jqXHR.statusCode(statusCode);
                statusCode = undefined;
                if (fireGlobals) {
                  globalEventContext.trigger(isSuccess
                    ? "ajaxSuccess"
                    : "ajaxError", [
                    jqXHR, s, isSuccess
                      ? success
                      : error
                  ])
                }
                completeDeferred.fireWith(callbackContext, [jqXHR, statusText]);
                if (fireGlobals) {
                  globalEventContext.trigger("ajaxComplete", [jqXHR, s]);
                  if (!--jQuery.active) {
                    jQuery.event.trigger("ajaxStop")
                  }
                }
              }
              return jqXHR
            },
            getJSON: function(url, data, callback) {
              return jQuery.get(url, data, callback, "json")
            },
            getScript: function(url, callback) {
              return jQuery.get(url, undefined, callback, "script")
            }
          });
          jQuery.each([
            "get", "post"
          ], function(i, method) {
            jQuery[method] = function(url, data, callback, type) {
              if (jQuery.isFunction(data)) {
                type = type || callback;
                callback = data;
                data = undefined
              }
              return jQuery.ajax({url: url, type: method, dataType: type, data: data, success: callback})
            }
          });
          jQuery._evalUrl = function(url) {
            return jQuery.ajax({
              url: url,
              type: "GET",
              dataType: "script",
              async: false,
              global: false,
              "throws": true
            })
          };
          jQuery.fn.extend({
            wrapAll: function(html) {
              if (jQuery.isFunction(html)) {
                return this.each(function(i) {
                  jQuery(this).wrapAll(html.call(this, i))
                })
              }
              if (this[0]) {
                var wrap = jQuery(html, this[0].ownerDocument).eq(0).clone(true);
                if (this[0].parentNode) {
                  wrap.insertBefore(this[0])
                }
                wrap.map(function() {
                  var elem = this;
                  while (elem.firstChild && elem.firstChild.nodeType === 1) {
                    elem = elem.firstChild
                  }
                  return elem
                }).append(this)
              }
              return this
            },
            wrapInner: function(html) {
              if (jQuery.isFunction(html)) {
                return this.each(function(i) {
                  jQuery(this).wrapInner(html.call(this, i))
                })
              }
              return this.each(function() {
                var self = jQuery(this),
                  contents = self.contents();
                if (contents.length) {
                  contents.wrapAll(html)
                } else {
                  self.append(html)
                }
              })
            },
            wrap: function(html) {
              var isFunction = jQuery.isFunction(html);
              return this.each(function(i) {
                jQuery(this).wrapAll(isFunction
                  ? html.call(this, i)
                  : html)
              })
            },
            unwrap: function() {
              return this.parent().each(function() {
                if (!jQuery.nodeName(this, "body")) {
                  jQuery(this).replaceWith(this.childNodes)
                }
              }).end()
            }
          });
          jQuery.expr.filters.hidden = function(elem) {
            return elem.offsetWidth <= 0 && elem.offsetHeight <= 0 || !support.reliableHiddenOffsets() && (elem.style && elem.style.display || jQuery.css(elem, "display")) === "none"
          };
          jQuery.expr.filters.visible = function(elem) {
            return !jQuery.expr.filters.hidden(elem)
          };
          var r20 = /%20/g,
            rbracket = /\[\]$/,
            rCRLF = /\r?\n/g,
            rsubmitterTypes = /^(?:submit|button|image|reset|file)$/i,
            rsubmittable = /^(?:input|select|textarea|keygen)/i;
          function buildParams(prefix, obj, traditional, add) {
            var name;
            if (jQuery.isArray(obj)) {
              jQuery.each(obj, function(i, v) {
                if (traditional || rbracket.test(prefix)) {
                  add(prefix, v)
                } else {
                  buildParams(prefix + "[" + (typeof v === "object"
                    ? i
                    : "") + "]", v, traditional, add)
                }
              })
            } else if (!traditional && jQuery.type(obj) === "object") {
              for (name in obj) {
                buildParams(prefix + "[" + name + "]", obj[name], traditional, add)
              }
            } else {
              add(prefix, obj)
            }
          }
          jQuery.param = function(a, traditional) {
            var prefix,
              s = [],
              add = function(key, value) {
                value = jQuery.isFunction(value)
                  ? value()
                  : value == null
                    ? ""
                    : value;
                s[s.length] = encodeURIComponent(key) + "=" + encodeURIComponent(value)
              };
            if (traditional === undefined) {
              traditional = jQuery.ajaxSettings && jQuery.ajaxSettings.traditional
            }
            if (jQuery.isArray(a) || a.jquery && !jQuery.isPlainObject(a)) {
              jQuery.each(a, function() {
                add(this.name, this.value)
              })
            } else {
              for (prefix in a) {
                buildParams(prefix, a[prefix], traditional, add)
              }
            }
            return s.join("&").replace(r20, "+")
          };
          jQuery.fn.extend({
            serialize: function() {
              return jQuery.param(this.serializeArray())
            },
            serializeArray: function() {
              return this.map(function() {
                var elements = jQuery.prop(this, "elements");
                return elements
                  ? jQuery.makeArray(elements)
                  : this
              }).filter(function() {
                var type = this.type;
                return this.name && !jQuery(this).is(":disabled") && rsubmittable.test(this.nodeName) && !rsubmitterTypes.test(type) && (this.checked || !rcheckableType.test(type))
              }).map(function(i, elem) {
                var val = jQuery(this).val();
                return val == null
                  ? null
                  : jQuery.isArray(val)
                    ? jQuery.map(val, function(val) {
                      return {
                        name: elem.name,
                        value: val.replace(rCRLF, "\r\n")
                      }
                    })
                    : {
                      name: elem.name,
                      value: val.replace(rCRLF, "\r\n")
                    }
              }).get()
            }
          });
          jQuery.ajaxSettings.xhr = window.ActiveXObject !== undefined
            ? function() {
              return !this.isLocal && /^(get|post|head|put|delete|options)$/i.test(this.type) && createStandardXHR() || createActiveXHR()
            }
            : createStandardXHR;
          var xhrId = 0,
            xhrCallbacks = {},
            xhrSupported = jQuery.ajaxSettings.xhr();
          if (window.attachEvent) {
            window.attachEvent("onunload", function() {
              for (var key in xhrCallbacks) {
                xhrCallbacks[key](undefined, true)
              }
            })
          }
          support.cors = !!xhrSupported && "withCredentials" in xhrSupported;
          xhrSupported = support.ajax = !!xhrSupported;
          if (xhrSupported) {
            jQuery.ajaxTransport(function(options) {
              if (!options.crossDomain || support.cors) {
                var callback;
                return {
                  send: function(headers, complete) {
                    var i,
                      xhr = options.xhr(),
                      id = ++xhrId;
                    xhr.open(options.type, options.url, options.async, options.username, options.password);
                    if (options.xhrFields) {
                      for (i in options.xhrFields) {
                        xhr[i] = options.xhrFields[i]
                      }
                    }
                    if (options.mimeType && xhr.overrideMimeType) {
                      xhr.overrideMimeType(options.mimeType)
                    }
                    if (!options.crossDomain && !headers["X-Requested-With"]) {
                      headers["X-Requested-With"] = "XMLHttpRequest"
                    }
                    for (i in headers) {
                      if (headers[i] !== undefined) {
                        xhr.setRequestHeader(i, headers[i] + "")
                      }
                    }
                    xhr.send(options.hasContent && options.data || null);
                    callback = function(_, isAbort) {
                      var status,
                        statusText,
                        responses;
                      if (callback && (isAbort || xhr.readyState === 4)) {
                        delete xhrCallbacks[id];
                        callback = undefined;
                        xhr.onreadystatechange = jQuery.noop;
                        if (isAbort) {
                          if (xhr.readyState !== 4) {
                            xhr.abort()
                          }
                        } else {
                          responses = {};
                          status = xhr.status;
                          if (typeof xhr.responseText === "string") {
                            responses.text = xhr.responseText
                          }
                          try {
                            statusText = xhr.statusText
                          } catch (e) {
                            statusText = ""
                          }
                          if (!status && options.isLocal && !options.crossDomain) {
                            status = responses.text
                              ? 200
                              : 404
                          } else if (status === 1223) {
                            status = 204
                          }
                        }
                      }
                      if (responses) {
                        complete(status, statusText, responses, xhr.getAllResponseHeaders())
                      }
                    };
                    if (!options.async) {
                      callback()
                    } else if (xhr.readyState === 4) {
                      setTimeout(callback)
                    } else {
                      xhr.onreadystatechange = xhrCallbacks[id] = callback
                    }
                  },
                  abort: function() {
                    if (callback) {
                      callback(undefined, true)
                    }
                  }
                }
              }
            })
          }
          function createStandardXHR() {
            try {
              return new window.XMLHttpRequest
            } catch (e) {}
          }
          function createActiveXHR() {
            try {
              return new window.ActiveXObject("Microsoft.XMLHTTP")
            } catch (e) {}
          }
          jQuery.ajaxSetup({
            accepts: {
              script: "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"
            },
            contents: {
              script: /(?:java|ecma)script/
            },
            converters: {
              "text script": function(text) {
                jQuery.globalEval(text);
                return text
              }
            }
          });
          jQuery.ajaxPrefilter("script", function(s) {
            if (s.cache === undefined) {
              s.cache = false
            }
            if (s.crossDomain) {
              s.type = "GET";
              s.global = false
            }
          });
          jQuery.ajaxTransport("script", function(s) {
            if (s.crossDomain) {
              var script,
                head = document.head || jQuery("head")[0] || document.documentElement;
              return {
                send: function(_, callback) {
                  script = document.createElement("script");
                  script.async = true;
                  if (s.scriptCharset) {
                    script.charset = s.scriptCharset
                  }
                  script.src = s.url;
                  script.onload = script.onreadystatechange = function(_, isAbort) {
                    if (isAbort || !script.readyState || /loaded|complete/.test(script.readyState)) {
                      script.onload = script.onreadystatechange = null;
                      if (script.parentNode) {
                        script.parentNode.removeChild(script)
                      }
                      script = null;
                      if (!isAbort) {
                        callback(200, "success")
                      }
                    }
                  };
                  head.insertBefore(script, head.firstChild)
                },
                abort: function() {
                  if (script) {
                    script.onload(undefined, true)
                  }
                }
              }
            }
          });
          var oldCallbacks = [],
            rjsonp = /(=)\?(?=&|$)|\?\?/;
          jQuery.ajaxSetup({
            jsonp: "callback",
            jsonpCallback: function() {
              var callback = oldCallbacks.pop() || jQuery.expando + "_" + nonce++;
              this[callback] = true;
              return callback
            }
          });
          jQuery.ajaxPrefilter("json jsonp", function(s, originalSettings, jqXHR) {
            var callbackName,
              overwritten,
              responseContainer,
              jsonProp = s.jsonp !== false && (rjsonp.test(s.url)
                ? "url"
                : typeof s.data === "string" && !(s.contentType || "").indexOf("application/x-www-form-urlencoded") && rjsonp.test(s.data) && "data");
            if (jsonProp || s.dataTypes[0] === "jsonp") {
              callbackName = s.jsonpCallback = jQuery.isFunction(s.jsonpCallback)
                ? s.jsonpCallback()
                : s.jsonpCallback;
              if (jsonProp) {
                s[jsonProp] = s[jsonProp].replace(rjsonp, "$1" + callbackName)
              } else if (s.jsonp !== false) {
                s.url += (rquery.test(s.url)
                  ? "&"
                  : "?") + s.jsonp + "=" + callbackName
              }
              s.converters["script json"] = function() {
                if (!responseContainer) {
                  jQuery.error(callbackName + " was not called")
                }
                return responseContainer[0]
              };
              s.dataTypes[0] = "json";
              overwritten = window[callbackName];
              window[callbackName] = function() {
                responseContainer = arguments
              };
              jqXHR.always(function() {
                window[callbackName] = overwritten;
                if (s[callbackName]) {
                  s.jsonpCallback = originalSettings.jsonpCallback;
                  oldCallbacks.push(callbackName)
                }
                if (responseContainer && jQuery.isFunction(overwritten)) {
                  overwritten(responseContainer[0])
                }
                responseContainer = overwritten = undefined
              });
              return "script"
            }
          });
          jQuery.parseHTML = function(data, context, keepScripts) {
            if (!data || typeof data !== "string") {
              return null
            }
            if (typeof context === "boolean") {
              keepScripts = context;
              context = false
            }
            context = context || document;
            var parsed = rsingleTag.exec(data),
              scripts = !keepScripts && [];
            if (parsed) {
              return [context.createElement(parsed[1])]
            }
            parsed = jQuery.buildFragment([data], context, scripts);
            if (scripts && scripts.length) {
              jQuery(scripts).remove()
            }
            return jQuery.merge([], parsed.childNodes)
          };
          var _load = jQuery.fn.load;
          jQuery.fn.load = function(url, params, callback) {
            if (typeof url !== "string" && _load) {
              return _load.apply(this, arguments)
            }
            var selector,
              response,
              type,
              self = this,
              off = url.indexOf(" ");
            if (off >= 0) {
              selector = jQuery.trim(url.slice(off, url.length));
              url = url.slice(0, off)
            }
            if (jQuery.isFunction(params)) {
              callback = params;
              params = undefined
            } else if (params && typeof params === "object") {
              type = "POST"
            }
            if (self.length > 0) {
              jQuery.ajax({url: url, type: type, dataType: "html", data: params}).done(function(responseText) {
                response = arguments;
                self.html(selector
                  ? jQuery("<div>").append(jQuery.parseHTML(responseText)).find(selector)
                  : responseText)
              }).complete(callback && function(jqXHR, status) {
                self.each(callback, response || [jqXHR.responseText, status, jqXHR])
              })
            }
            return this
          };
          jQuery.each([
            "ajaxStart",
            "ajaxStop",
            "ajaxComplete",
            "ajaxError",
            "ajaxSuccess",
            "ajaxSend"
          ], function(i, type) {
            jQuery.fn[type] = function(fn) {
              return this.on(type, fn)
            }
          });
          jQuery.expr.filters.animated = function(elem) {
            return jQuery.grep(jQuery.timers, function(fn) {
              return elem === fn.elem
            }).length
          };
          var docElem = window.document.documentElement;
          function getWindow(elem) {
            return jQuery.isWindow(elem)
              ? elem
              : elem.nodeType === 9
                ? elem.defaultView || elem.parentWindow
                : false
          }
          jQuery.offset = {
            setOffset: function(elem, options, i) {
              var curPosition,
                curLeft,
                curCSSTop,
                curTop,
                curOffset,
                curCSSLeft,
                calculatePosition,
                position = jQuery.css(elem, "position"),
                curElem = jQuery(elem),
                props = {};
              if (position === "static") {
                elem.style.position = "relative"
              }
              curOffset = curElem.offset();
              curCSSTop = jQuery.css(elem, "top");
              curCSSLeft = jQuery.css(elem, "left");
              calculatePosition = (position === "absolute" || position === "fixed") && jQuery.inArray("auto", [curCSSTop, curCSSLeft]) > -1;
              if (calculatePosition) {
                curPosition = curElem.position();
                curTop = curPosition.top;
                curLeft = curPosition.left
              } else {
                curTop = parseFloat(curCSSTop) || 0;
                curLeft = parseFloat(curCSSLeft) || 0
              }
              if (jQuery.isFunction(options)) {
                options = options.call(elem, i, curOffset)
              }
              if (options.top != null) {
                props.top = options.top - curOffset.top + curTop
              }
              if (options.left != null) {
                props.left = options.left - curOffset.left + curLeft
              }
              if ("using" in options) {
                options.using.call(elem, props)
              } else {
                curElem.css(props)
              }
            }
          };
          jQuery.fn.extend({
            offset: function(options) {
              if (arguments.length) {
                return options === undefined
                  ? this
                  : this.each(function(i) {
                    jQuery.offset.setOffset(this, options, i)
                  })
              }
              var docElem,
                win,
                box = {
                  top: 0,
                  left: 0
                },
                elem = this[0],
                doc = elem && elem.ownerDocument;
              if (!doc) {
                return
              }
              docElem = doc.documentElement;
              if (!jQuery.contains(docElem, elem)) {
                return box
              }
              if (typeof elem.getBoundingClientRect !== strundefined) {
                box = elem.getBoundingClientRect()
              }
              win = getWindow(doc);
              return {
                top: box.top + (win.pageYOffset || docElem.scrollTop) - (docElem.clientTop || 0),
                left: box.left + (win.pageXOffset || docElem.scrollLeft) - (docElem.clientLeft || 0)
              }
            },
            position: function() {
              if (!this[0]) {
                return
              }
              var offsetParent,
                offset,
                parentOffset = {
                  top: 0,
                  left: 0
                },
                elem = this[0];
              if (jQuery.css(elem, "position") === "fixed") {
                offset = elem.getBoundingClientRect()
              } else {
                offsetParent = this.offsetParent();
                offset = this.offset();
                if (!jQuery.nodeName(offsetParent[0], "html")) {
                  parentOffset = offsetParent.offset()
                }
                parentOffset.top += jQuery.css(offsetParent[0], "borderTopWidth", true);
                parentOffset.left += jQuery.css(offsetParent[0], "borderLeftWidth", true)
              }
              return {
                top: offset.top - parentOffset.top - jQuery.css(elem, "marginTop", true),
                left: offset.left - parentOffset.left - jQuery.css(elem, "marginLeft", true)
              }
            },
            offsetParent: function() {
              return this.map(function() {
                var offsetParent = this.offsetParent || docElem;
                while (offsetParent && (!jQuery.nodeName(offsetParent, "html") && jQuery.css(offsetParent, "position") === "static")) {
                  offsetParent = offsetParent.offsetParent
                }
                return offsetParent || docElem
              })
            }
          });
          jQuery.each({
            scrollLeft: "pageXOffset",
            scrollTop: "pageYOffset"
          }, function(method, prop) {
            var top = /Y/.test(prop);
            jQuery.fn[method] = function(val) {
              return access(this, function(elem, method, val) {
                var win = getWindow(elem);
                if (val === undefined) {
                  return win
                    ? prop in win
                      ? win[prop]
                      : win.document.documentElement[method]
                    : elem[method]
                }
                if (win) {
                  win.scrollTo(!top
                    ? val
                    : jQuery(win).scrollLeft(), top
                    ? val
                    : jQuery(win).scrollTop())
                } else {
                  elem[method] = val
                }
              }, method, val, arguments.length, null)
            }
          });
          jQuery.each([
            "top", "left"
          ], function(i, prop) {
            jQuery.cssHooks[prop] = addGetHookIf(support.pixelPosition, function(elem, computed) {
              if (computed) {
                computed = curCSS(elem, prop);
                return rnumnonpx.test(computed)
                  ? jQuery(elem).position()[prop] + "px"
                  : computed
              }
            })
          });
          jQuery.each({
            Height: "height",
            Width: "width"
          }, function(name, type) {
            jQuery.each({
              padding: "inner" + name,
              content: type,
              "": "outer" + name
            }, function(defaultExtra, funcName) {
              jQuery.fn[funcName] = function(margin, value) {
                var chainable = arguments.length && (defaultExtra || typeof margin !== "boolean"),
                  extra = defaultExtra || (margin === true || value === true
                    ? "margin"
                    : "border");
                return access(this, function(elem, type, value) {
                  var doc;
                  if (jQuery.isWindow(elem)) {
                    return elem.document.documentElement["client" + name]
                  }
                  if (elem.nodeType === 9) {
                    doc = elem.documentElement;
                    return Math.max(elem.body["scroll" + name], doc["scroll" + name], elem.body["offset" + name], doc["offset" + name], doc["client" + name])
                  }
                  return value === undefined
                    ? jQuery.css(elem, type, extra)
                    : jQuery.style(elem, type, value, extra)
                }, type, chainable
                  ? margin
                  : undefined, chainable, null)
              }
            })
          });
          jQuery.fn.size = function() {
            return this.length
          };
          jQuery.fn.andSelf = jQuery.fn.addBack;
          if (typeof define === "function" && define.amd) {
            define("jquery", [], function() {
              return jQuery
            })
          }
          var _jQuery = window.jQuery,
            _$ = window.$;
          jQuery.noConflict = function(deep) {
            if (window.$ === jQuery) {
              window.$ = _$
            }
            if (deep && window.jQuery === jQuery) {
              window.jQuery = _jQuery
            }
            return jQuery
          };
          if (typeof noGlobal === strundefined) {
            window.jQuery = window.$ = jQuery
          }
          return jQuery
        })
      }, {}
    ],
    18: [
      function(require, module, exports) {
        (function() {
          module.exports = {
            xpath: require("./xpath"),
            Range: require("./range")
          }
        }).call(this)
      }, {
        "./range": 19,
        "./xpath": 21
      }
    ],
    19: [
      function(require, module, exports) {
        (function() {
          var $,
            Range,
            Util,
            xpath,
            __hasProp = {}.hasOwnProperty,
            __extends = function(child, parent) {
              for (var key in parent) {
                if (__hasProp.call(parent, key))
                  child[key] = parent[key]
              }
              function ctor() {
                this.constructor = child
              }
              ctor.prototype = parent.prototype;
              child.prototype = new ctor;
              child.__super__ = parent.prototype;
              return child
            };
          xpath = require("./xpath");
          Util = require("./util");
          $ = require("jquery");
          Range = {};
          Range.sniff = function(r) {
            if (r.commonAncestorContainer != null) {
              return new Range.BrowserRange(r)
            } else if (typeof r.start === "string") {
              return new Range.SerializedRange(r)
            } else if (r.start && typeof r.start === "object") {
              return new Range.NormalizedRange(r)
            } else {
              console.error("Could not sniff range type");
              return false
            }
          };
          Range.RangeError = function(_super) {
            __extends(RangeError, _super);
            function RangeError(type, message, parent) {
              this.type = type;
              this.message = message;
              this.parent = parent != null
                ? parent
                : null;
              RangeError.__super__.constructor.call(this, this.message)
            }
            return RangeError
          }(Error);
          Range.BrowserRange = function() {
            function BrowserRange(obj) {
              this.commonAncestorContainer = obj.commonAncestorContainer;
              this.startContainer = obj.startContainer;
              this.startOffset = obj.startOffset;
              this.endContainer = obj.endContainer;
              this.endOffset = obj.endOffset
            }
            BrowserRange.prototype.normalize = function(root) {
              var nr,
                r;
              if (this.tainted) {
                console.error("You may only call normalize() once on a BrowserRange!");
                return false
              } else {
                this.tainted = true
              }
              r = {};
              this._normalizeStart(r);
              this._normalizeEnd(r);
              nr = {};
              if (r.startOffset > 0) {
                if (r.start.nodeValue.length > r.startOffset) {
                  nr.start = r.start.splitText(r.startOffset)
                } else {
                  nr.start = r.start.nextSibling
                }
              } else {
                nr.start = r.start
              }
              if (r.start === r.end) {
                if (nr.start.nodeValue.length > r.endOffset - r.startOffset) {
                  nr.start.splitText(r.endOffset - r.startOffset)
                }
                nr.end = nr.start
              } else {
                if (r.end.nodeValue.length > r.endOffset) {
                  r.end.splitText(r.endOffset)
                }
                nr.end = r.end
              }
              nr.commonAncestor = this.commonAncestorContainer;
              while (nr.commonAncestor.nodeType !== Util.NodeTypes.ELEMENT_NODE) {
                nr.commonAncestor = nr.commonAncestor.parentNode
              }
              return new Range.NormalizedRange(nr)
            };
            BrowserRange.prototype._normalizeStart = function(r) {
              if (this.startContainer.nodeType === Util.NodeTypes.ELEMENT_NODE) {
                r.start = Util.getFirstTextNodeNotBefore(this.startContainer.childNodes[this.startOffset]);
                return r.startOffset = 0
              } else {
                r.start = this.startContainer;
                return r.startOffset = this.startOffset
              }
            };
            BrowserRange.prototype._normalizeEnd = function(r) {
              var n,
                node;
              if (this.endContainer.nodeType === Util.NodeTypes.ELEMENT_NODE) {
                node = this.endContainer.childNodes[this.endOffset];
                if (node != null) {
                  n = node;
                  while (n != null && n.nodeType !== Util.NodeTypes.TEXT_NODE) {
                    n = n.firstChild
                  }
                  if (n != null) {
                    r.end = n;
                    r.endOffset = 0
                  }
                }
                if (r.end == null) {
                  if (this.endOffset) {
                    node = this.endContainer.childNodes[this.endOffset - 1]
                  } else {
                    node = this.endContainer.previousSibling
                  }
                  r.end = Util.getLastTextNodeUpTo(node);
                  return r.endOffset = r.end.nodeValue.length
                }
              } else {
                r.end = this.endContainer;
                return r.endOffset = this.endOffset
              }
            };
            BrowserRange.prototype.serialize = function(root, ignoreSelector) {
              return this.normalize(root).serialize(root, ignoreSelector)
            };
            return BrowserRange
          }();
          Range.NormalizedRange = function() {
            function NormalizedRange(obj) {
              this.commonAncestor = obj.commonAncestor;
              this.start = obj.start;
              this.end = obj.end
            }
            NormalizedRange.prototype.normalize = function(root) {
              return this
            };
            NormalizedRange.prototype.limit = function(bounds) {
              var nodes,
                parent,
                startParents,
                _i,
                _len,
                _ref;
              nodes = $.grep(this.textNodes(), function(node) {
                return node.parentNode === bounds || $.contains(bounds, node.parentNode)
              });
              if (!nodes.length) {
                return null
              }
              this.start = nodes[0];
              this.end = nodes[nodes.length - 1];
              startParents = $(this.start).parents();
              _ref = $(this.end).parents();
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                parent = _ref[_i];
                if (startParents.index(parent) !== -1) {
                  this.commonAncestor = parent;
                  break
                }
              }
              return this
            };
            NormalizedRange.prototype.serialize = function(root, ignoreSelector) {
              var end,
                serialization,
                start;
              serialization = function(node, isEnd) {
                var n,
                  nodes,
                  offset,
                  origParent,
                  path,
                  textNodes,
                  _i,
                  _len;
                if (ignoreSelector) {
                  origParent = $(node).parents(":not(" + ignoreSelector + ")").eq(0)
                } else {
                  origParent = $(node).parent()
                }
                path = xpath.fromNode(origParent, root)[0];
                textNodes = Util.getTextNodes(origParent);
                nodes = textNodes.slice(0, textNodes.index(node));
                offset = 0;
                for (_i = 0, _len = nodes.length; _i < _len; _i++) {
                  n = nodes[_i];
                  offset += n.nodeValue.length
                }
                if (isEnd) {
                  return [
                    path, offset + node.nodeValue.length
                  ]
                } else {
                  return [path, offset]
                }
              };
              start = serialization(this.start);
              end = serialization(this.end, true);
              return new Range.SerializedRange({start: start[0], end: end[0], startOffset: start[1], endOffset: end[1]})
            };
            NormalizedRange.prototype.text = function() {
              var node;
              return function() {
                var _i,
                  _len,
                  _ref,
                  _results;
                _ref = this.textNodes();
                _results = [];
                for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                  node = _ref[_i];
                  _results.push(node.nodeValue)
                }
                return _results
              }.call(this).join("")
            };
            NormalizedRange.prototype.textNodes = function() {
              var end,
                start,
                textNodes,
                _ref;
              textNodes = Util.getTextNodes($(this.commonAncestor));
              _ref = [
                textNodes.index(this.start),
                textNodes.index(this.end)
              ],
              start = _ref[0],
              end = _ref[1];
              return $.makeArray(textNodes.slice(start, + end + 1 || 9e9))
            };
            return NormalizedRange
          }();
          Range.SerializedRange = function() {
            function SerializedRange(obj) {
              this.start = obj.start;
              this.startOffset = obj.startOffset;
              this.end = obj.end;
              this.endOffset = obj.endOffset
            }
            SerializedRange.prototype.normalize = function(root) {
              var contains,
                e,
                length,
                node,
                p,
                range,
                targetOffset,
                tn,
                _i,
                _j,
                _len,
                _len1,
                _ref,
                _ref1;
              range = {};
              _ref = ["start", "end"];
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                p = _ref[_i];
                try {
                  node = xpath.toNode(this[p], root)
                } catch (_error) {
                  e = _error;
                  throw new Range.RangeError(p, "Error while finding " + p + " node: " + this[p] + ": " + e, e)
                }
                if (!node) {
                  throw new Range.RangeError(p, "Couldn't find " + p + " node: " + this[p])
                }
                length = 0;
                targetOffset = this[p + "Offset"];
                if (p === "end") {
                  targetOffset -= 1
                }
                _ref1 = Util.getTextNodes($(node));
                for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
                  tn = _ref1[_j];
                  if (length + tn.nodeValue.length > targetOffset) {
                    range[p + "Container"] = tn;
                    range[p + "Offset"] = this[p + "Offset"] - length;
                    break
                  } else {
                    length += tn.nodeValue.length
                  }
                }
                if (range[p + "Offset"] == null) {
                  throw new Range.RangeError("" + p + "offset", "Couldn't find offset " + this[p + "Offset"] + " in element " + this[p])
                }
              }
              contains = document.compareDocumentPosition != null
                ? function(a, b) {
                  return a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_CONTAINED_BY
                }
                : function(a, b) {
                  return a.contains(b)
                };
              $(range.startContainer).parents().each(function() {
                var endContainer;
                if (range.endContainer.nodeType === Util.NodeTypes.TEXT_NODE) {
                  endContainer = range.endContainer.parentNode
                } else {
                  endContainer = range.endContainer
                }
                if (contains(this, endContainer)) {
                  range.commonAncestorContainer = this;
                  return false
                }
              });
              return new Range.BrowserRange(range).normalize(root)
            };
            SerializedRange.prototype.serialize = function(root, ignoreSelector) {
              return this.normalize(root).serialize(root, ignoreSelector)
            };
            SerializedRange.prototype.toObject = function() {
              return {start: this.start, startOffset: this.startOffset, end: this.end, endOffset: this.endOffset}
            };
            return SerializedRange
          }();
          module.exports = Range
        }).call(this)
      }, {
        "./util": 20,
        "./xpath": 21,
        jquery: 17
      }
    ],
    20: [
      function(require, module, exports) {
        (function() {
          var $,
            Util;
          $ = require("jquery");
          Util = {};
          Util.NodeTypes = {
            ELEMENT_NODE: 1,
            ATTRIBUTE_NODE: 2,
            TEXT_NODE: 3,
            CDATA_SECTION_NODE: 4,
            ENTITY_REFERENCE_NODE: 5,
            ENTITY_NODE: 6,
            PROCESSING_INSTRUCTION_NODE: 7,
            COMMENT_NODE: 8,
            DOCUMENT_NODE: 9,
            DOCUMENT_TYPE_NODE: 10,
            DOCUMENT_FRAGMENT_NODE: 11,
            NOTATION_NODE: 12
          };
          Util.getFirstTextNodeNotBefore = function(n) {
            var result;
            switch (n.nodeType) {
              case Util.NodeTypes.TEXT_NODE:
                return n;
              case Util.NodeTypes.ELEMENT_NODE:
                if (n.firstChild != null) {
                  result = Util.getFirstTextNodeNotBefore(n.firstChild);
                  if (result != null) {
                    return result
                  }
                }
                break
            }
            n = n.nextSibling;
            if (n != null) {
              return Util.getFirstTextNodeNotBefore(n)
            } else {
              return null
            }
          };
          Util.getLastTextNodeUpTo = function(n) {
            var result;
            switch (n.nodeType) {
              case Util.NodeTypes.TEXT_NODE:
                return n;
              case Util.NodeTypes.ELEMENT_NODE:
                if (n.lastChild != null) {
                  result = Util.getLastTextNodeUpTo(n.lastChild);
                  if (result != null) {
                    return result
                  }
                }
                break
            }
            n = n.previousSibling;
            if (n != null) {
              return Util.getLastTextNodeUpTo(n)
            } else {
              return null
            }
          };
          Util.getTextNodes = function(jq) {
            var getTextNodes;
            getTextNodes = function(node) {
              var nodes;
              if (node && node.nodeType !== Util.NodeTypes.TEXT_NODE) {
                nodes = [];
                if (node.nodeType !== Util.NodeTypes.COMMENT_NODE) {
                  node = node.lastChild;
                  while (node) {
                    nodes.push(getTextNodes(node));
                    node = node.previousSibling
                  }
                }
                return nodes.reverse()
              } else {
                return node
              }
            };
            return jq.map(function() {
              return Util.flatten(getTextNodes(this))
            })
          };
          Util.getGlobal = function() {
            return function() {
              return this
            }()
          };
          Util.contains = function(parent, child) {
            var node;
            node = child;
            while (node != null) {
              if (node === parent) {
                return true
              }
              node = node.parentNode
            }
            return false
          };
          Util.flatten = function(array) {
            var flatten;
            flatten = function(ary) {
              var el,
                flat,
                _i,
                _len;
              flat = [];
              for (_i = 0, _len = ary.length; _i < _len; _i++) {
                el = ary[_i];
                flat = flat.concat(el && $.isArray(el)
                  ? flatten(el)
                  : el)
              }
              return flat
            };
            return flatten(array)
          };
          module.exports = Util
        }).call(this)
      }, {
        jquery: 17
      }
    ],
    21: [
      function(require, module, exports) {
        (function() {
          var $,
            Util,
            evaluateXPath,
            findChild,
            fromNode,
            getNodeName,
            getNodePosition,
            simpleXPathJQuery,
            simpleXPathPure,
            toNode;
          $ = require("jquery");
          Util = require("./util");
          evaluateXPath = function(xp, root, nsResolver) {
            var exception,
              idx,
              name,
              node,
              step,
              steps,
              _i,
              _len,
              _ref;
            if (root == null) {
              root = document
            }
            if (nsResolver == null) {
              nsResolver = null
            }
            try {
              return document.evaluate("." + xp, root, nsResolver, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
            } catch (_error) {
              exception = _error;
              console.log("XPath evaluation failed.");
              console.log("Trying fallback...");
              steps = xp.substring(1).split("/");
              node = root;
              for (_i = 0, _len = steps.length; _i < _len; _i++) {
                step = steps[_i];
                _ref = step.split("["),
                name = _ref[0],
                idx = _ref[1];
                idx = idx != null
                  ? parseInt((idx != null
                    ? idx.split("]")
                    : void 0)[0])
                  : 1;
                node = findChild(node, name.toLowerCase(), idx)
              }
              return node
            }
          };
          simpleXPathJQuery = function($el, relativeRoot) {
            var jq;
            jq = $el.map(function() {
              var elem,
                idx,
                path,
                tagName;
              path = "";
              elem = this;
              while ((elem != null
                ? elem.nodeType
                : void 0) === Util.NodeTypes.ELEMENT_NODE && elem !== relativeRoot) {
                tagName = elem.tagName.replace(":", "\\:");
                idx = $(elem.parentNode).children(tagName).index(elem) + 1;
                idx = "[" + idx + "]";
                path = "/" + elem.tagName.toLowerCase() + idx + path;
                elem = elem.parentNode
              }
              return path
            });
            return jq.get()
          };
          simpleXPathPure = function($el, relativeRoot) {
            var getPathSegment,
              getPathTo,
              jq,
              rootNode;
            getPathSegment = function(node) {
              var name,
                pos;
              name = getNodeName(node);
              pos = getNodePosition(node);
              return "" + name + "[" + pos + "]"
            };
            rootNode = relativeRoot;
            getPathTo = function(node) {
              var xpath;
              xpath = "";
              while (node !== rootNode) {
                if (node == null) {
                  throw new Error("Called getPathTo on a node which was not a descendant of @rootNode. " + rootNode)
                }
                xpath = getPathSegment(node) + "/" + xpath;
                node = node.parentNode
              }
              xpath = "/" + xpath;
              xpath = xpath.replace(/\/$/, "");
              return xpath
            };
            jq = $el.map(function() {
              var path;
              path = getPathTo(this);
              return path
            });
            return jq.get()
          };
          findChild = function(node, type, index) {
            var child,
              children,
              found,
              name,
              _i,
              _len;
            if (!node.hasChildNodes()) {
              throw new Error("XPath error: node has no children!")
            }
            children = node.childNodes;
            found = 0;
            for (_i = 0, _len = children.length; _i < _len; _i++) {
              child = children[_i];
              name = getNodeName(child);
              if (name === type) {
                found += 1;
                if (found === index) {
                  return child
                }
              }
            }
            throw new Error("XPath error: wanted child not found.")
          };
          getNodeName = function(node) {
            var nodeName;
            nodeName = node.nodeName.toLowerCase();
            switch (nodeName) {
              case "#text":
                return "text()";
              case "#comment":
                return "comment()";
              case "#cdata-section":
                return "cdata-section()";
              default:
                return nodeName
            }
          };
          getNodePosition = function(node) {
            var pos,
              tmp;
            pos = 0;
            tmp = node;
            while (tmp) {
              if (tmp.nodeName === node.nodeName) {
                pos += 1
              }
              tmp = tmp.previousSibling
            }
            return pos
          };
          fromNode = function($el, relativeRoot) {
            var exception,
              result;
            try {
              result = simpleXPathJQuery($el, relativeRoot)
            } catch (_error) {
              exception = _error;
              console.log("jQuery-based XPath construction failed! Falling back to manual.");
              result = simpleXPathPure($el, relativeRoot)
            }
            return result
          };
          toNode = function(path, root) {
            var customResolver,
              namespace,
              node,
              segment;
            if (root == null) {
              root = document
            }
            if (!$.isXMLDoc(document.documentElement)) {
              return evaluateXPath(path, root)
            } else {
              customResolver = document.createNSResolver(document.ownerDocument === null
                ? document.documentElement
                : document.ownerDocument.documentElement);
              node = evaluateXPath(path, root, customResolver);
              if (!node) {
                path = function() {
                  var _i,
                    _len,
                    _ref,
                    _results;
                  _ref = path.split("/");
                  _results = [];
                  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                    segment = _ref[_i];
                    if (segment && segment.indexOf(":") === -1) {
                      _results.push(segment.replace(/^([a-z]+)/, "xhtml:$1"))
                    } else {
                      _results.push(segment)
                    }
                  }
                  return _results
                }().join("/");
                namespace = document.lookupNamespaceURI(null);
                customResolver = function(ns) {
                  if (ns === "xhtml") {
                    return namespace
                  } else {
                    return document.documentElement.getAttribute("xmlns:" + ns)
                  }
                };
                node = evaluateXPath(path, root, customResolver)
              }
              return node
            }
          };
          module.exports = {
            fromNode: fromNode,
            toNode: toNode
          }
        }).call(this)
      }, {
        "./util": 20,
        jquery: 17
      }
    ],
    22: [
      function(require, module, exports) {
        "use strict";
        var extend = require("backbone-extend-standalone");
        var Promise = require("es6-promise").Promise;
        var authz = require("./authz");
        var identity = require("./identity");
        var notification = require("./notification");
        var registry = require("./registry");
        var storage = require("./storage");
        function App() {
          this.modules = [];
          this.registry = new registry.Registry;
          this._started = false;
          this.registry.registerUtility(notification.defaultNotifier, "notifier");
          this.include(authz.acl);
          this.include(identity.simple);
          this.include(storage.noop)
        }
        App.prototype.include = function(module, options) {
          var mod = module(options);
          if (typeof mod.configure === "function") {
            mod.configure(this.registry)
          }
          this.modules.push(mod);
          return this
        };
        App.prototype.start = function() {
          if (this._started) {
            return
          }
          this._started = true;
          var self = this;
          var reg = this.registry;
          this.authz = reg.getUtility("authorizationPolicy");
          this.ident = reg.getUtility("identityPolicy");
          this.notify = reg.getUtility("notifier");
          this.annotations = new storage.StorageAdapter(reg.getUtility("storage"), function() {
            return self.runHook.apply(self, arguments)
          });
          return this.runHook("start", [this])
        };
        App.prototype.destroy = function() {
          return this.runHook("destroy")
        };
        App.prototype.runHook = function(name, args) {
          var results = [];
          for (var i = 0, len = this.modules.length; i < len; i++) {
            var mod = this.modules[i];
            if (typeof mod[name] === "function") {
              results.push(mod[name].apply(mod, args))
            }
          }
          return Promise.all(results)
        };
        App.extend = extend;
        exports.App = App
      }, {
        "./authz": 23,
        "./identity": 24,
        "./notification": 25,
        "./registry": 26,
        "./storage": 27,
        "backbone-extend-standalone": 3,
        "es6-promise": 5
      }
    ],
    23: [
      function(require, module, exports) {
        "use strict";
        var AclAuthzPolicy;
        exports.acl = function acl() {
          var authorization = new AclAuthzPolicy;
          return {
            configure: function(registry) {
              registry.registerUtility(authorization, "authorizationPolicy")
            }
          }
        };
        AclAuthzPolicy = exports.AclAuthzPolicy = function AclAuthzPolicy() {};
        AclAuthzPolicy.prototype.permits = function(action, context, identity) {
          var userid = this.authorizedUserId(identity);
          var permissions = context.permissions;
          if (permissions) {
            var tokens = permissions[action];
            if (typeof tokens === "undefined" || tokens === null) {
              return true
            }
            for (var i = 0, len = tokens.length; i < len; i++) {
              if (userid === tokens[i]) {
                return true
              }
            }
            return false
          } else if (context.user) {
            return userid === context.user
          }
          return true
        };
        AclAuthzPolicy.prototype.authorizedUserId = function(identity) {
          return identity
        }
      }, {}
    ],
    24: [
      function(require, module, exports) {
        "use strict";
        var SimpleIdentityPolicy;
        exports.simple = function simple() {
          var identity = new SimpleIdentityPolicy;
          return {
            configure: function(registry) {
              registry.registerUtility(identity, "identityPolicy")
            }
          }
        };
        SimpleIdentityPolicy = function SimpleIdentityPolicy() {
          this.identity = null
        };
        exports.SimpleIdentityPolicy = SimpleIdentityPolicy;
        SimpleIdentityPolicy.prototype.who = function() {
          return this.identity
        }
      }, {}
    ],
    25: [
      function(require, module, exports) {
        (function(global) {
          "use strict";
          var util = require("./util");
          var $ = util.$;
          var INFO = "info",
            SUCCESS = "success",
            ERROR = "error";
          var bannerTemplate = "<div class='annotator-notice'></div>";
          var bannerClasses = {
            show: "annotator-notice-show",
            info: "annotator-notice-info",
            success: "annotator-notice-success",
            error: "annotator-notice-error"
          };
          function banner(message, severity) {
            if (typeof severity === "undefined" || severity === null) {
              severity = INFO
            }
            var element = $(bannerTemplate)[0];
            var closed = false;
            var close = function() {
              if (closed) {
                return
              }
              closed = true;
              $(element).removeClass(bannerClasses.show).removeClass(bannerClasses[severity]);
              setTimeout(function() {
                $(element).remove()
              }, 500)
            };
            $(element).addClass(bannerClasses.show).addClass(bannerClasses[severity]).html(util.escapeHtml(message || "")).appendTo(global.document.body);
            $(element).on("click", close);
            setTimeout(close, 5e3);
            return {close: close}
          }
          exports.banner = banner;
          exports.defaultNotifier = banner;
          exports.INFO = INFO;
          exports.SUCCESS = SUCCESS;
          exports.ERROR = ERROR
        }).call(this, typeof global !== "undefined"
          ? global
          : typeof self !== "undefined"
            ? self
            : typeof window !== "undefined"
              ? window
              : {})
      }, {
        "./util": 39
      }
    ],
    26: [
      function(require, module, exports) {
        "use strict";
        function Registry() {
          this.utilities = {}
        }
        Registry.prototype.registerUtility = function(component, iface) {
          this.utilities[iface] = component
        };
        Registry.prototype.getUtility = function(iface) {
          var component = this.queryUtility(iface);
          if (component === null) {
            throw new LookupError(iface)
          }
          return component
        };
        Registry.prototype.queryUtility = function(iface) {
          var component = this.utilities[iface];
          if (typeof component === "undefined" || component === null) {
            return null
          }
          return component
        };
        function LookupError(iface) {
          this.name = "LookupError";
          this.message = 'No utility registered for interface "' + iface + '".'
        }
        LookupError.prototype = Object.create(Error.prototype);
        LookupError.prototype.constructor = LookupError;
        exports.LookupError = LookupError;
        exports.Registry = Registry
      }, {}
    ],
    27: [
      function(require, module, exports) {
        "use strict";
        var util = require("./util");
        var $ = util.$;
        var _t = util.gettext;
        var Promise = util.Promise;
        var id = function() {
          var counter;
          counter = -1;
          return function() {
            return counter += 1
          }
        }();
        exports.debug = function() {
          function trace(action, annotation) {
            var copyAnno = JSON.parse(JSON.stringify(annotation));
            console.debug("annotator.storage.debug: " + action, copyAnno)
          }
          return {
            create: function(annotation) {
              annotation.id = id();
              trace("create", annotation);
              return annotation
            },
            update: function(annotation) {
              trace("update", annotation);
              return annotation
            },
            "delete": function(annotation) {
              trace("destroy", annotation);
              return annotation
            },
            query: function(queryObj) {
              trace("query", queryObj);
              return {
                results: [],
                meta: {
                  total: 0
                }
              }
            },
            configure: function(registry) {
              registry.registerUtility(this, "storage")
            }
          }
        };
        exports.noop = function() {
          return {
            create: function(annotation) {
              if (typeof annotation.id === "undefined" || annotation.id === null) {
                annotation.id = id()
              }
              return annotation
            },
            update: function(annotation) {
              return annotation
            },
            "delete": function(annotation) {
              return annotation
            },
            query: function() {
              return {results: []}
            },
            configure: function(registry) {
              registry.registerUtility(this, "storage")
            }
          }
        };
        var HttpStorage;
        exports.http = function http(options) {
          var notify = function() {};
          if (typeof options === "undefined" || options === null) {
            options = {}
          }
          options.onError = options.onError || function(msg, xhr) {
            console.error(msg, xhr);
            notify(msg, "error")
          };
          var storage = new HttpStorage(options);
          return {
            configure: function(registry) {
              registry.registerUtility(storage, "storage")
            },
            start: function(app) {
              notify = app.notify
            }
          }
        };
        HttpStorage = exports.HttpStorage = function HttpStorage(options) {
          this.options = $.extend(true, {}, HttpStorage.options, options);
          this.onError = this.options.onError
        };
        HttpStorage.prototype.create = function(annotation) {
          return this._apiRequest("create", annotation)
        };
        HttpStorage.prototype.update = function(annotation) {
          return this._apiRequest("update", annotation)
        };
        HttpStorage.prototype["delete"] = function(annotation) {
          return this._apiRequest("destroy", annotation)
        };
        HttpStorage.prototype.query = function(queryObj) {
          return this._apiRequest("search", queryObj).then(function(obj) {
            var rows = obj.rows;
            delete obj.rows;
            return {results: rows, meta: obj}
          })
        };
        HttpStorage.prototype.setHeader = function(key, value) {
          this.options.headers[key] = value
        };
        HttpStorage.prototype._apiRequest = function(action, obj) {
          var id = obj && obj.id;
          var url = this._urlFor(action, id);
          var options = this._apiRequestOptions(action, obj);
          var request = $.ajax(url, options);
          request._id = id;
          request._action = action;
          return request
        };
        HttpStorage.prototype._apiRequestOptions = function(action, obj) {
          var method = this._methodFor(action);
          var self = this;
          var opts = {
            type: method,
            dataType: "json",
            error: function() {
              self._onError.apply(self, arguments)
            },
            headers: this.options.headers
          };
          if (this.options.emulateHTTP && (method === "PUT" || method === "DELETE")) {
            opts.headers = $.extend(opts.headers, {"X-HTTP-Method-Override": method});
            opts.type = "POST"
          }
          if (action === "search") {
            opts = $.extend(opts, {data: obj});
            return opts
          }
          var data = obj && JSON.stringify(obj);
          if (this.options.emulateJSON) {
            opts.data = {
              json: data
            };
            if (this.options.emulateHTTP) {
              opts.data._method = method
            }
            return opts
          }
          opts = $.extend(opts, {
            data: data,
            contentType: "application/json; charset=utf-8"
          });
          return opts
        };
        HttpStorage.prototype._urlFor = function(action, id) {
          if (typeof id === "undefined" || id === null) {
            id = ""
          }
          var url = "";
          if (typeof this.options.prefix !== "undefined" && this.options.prefix !== null) {
            url = this.options.prefix
          }
          url += this.options.urls[action];
          url = url.replace(/\{id\}/, id);
          return url
        };
        HttpStorage.prototype._methodFor = function(action) {
          var table = {
            create: "POST",
            update: "PUT",
            destroy: "DELETE",
            search: "GET"
          };
          return table[action]
        };
        HttpStorage.prototype._onError = function(xhr) {
          if (typeof this.onError !== "function") {
            return
          }
          var message;
          if (xhr.status === 400) {
            message = _t("The annotation store did not understand the request! " +
              "(Error 400)")
          } else if (xhr.status === 401) {
            message = _t("You must be logged in to perform this operation! " +
              "(Error 401)")
          } else if (xhr.status === 403) {
            message = _t("You don't have permission to perform this operation! " +
              "(Error 403)")
          } else if (xhr.status === 404) {
            message = _t("Could not connect to the annotation store! " +
              "(Error 404)")
          } else if (xhr.status === 500) {
            message = _t("Internal error in annotation store! " +
              "(Error 500)")
          } else {
            message = _t("Unknown error while speaking to annotation store!")
          }
          this.onError(message, xhr)
        };
        HttpStorage.options = {
          emulateHTTP: false,
          emulateJSON: false,
          headers: {},
          onError: function(message) {
            console.error("API request failed: " + message)
          },
          prefix: "/store",
          urls: {
            create: "/annotations",
            update: "/annotations/{id}",
            destroy: "/annotations/{id}",
            search: "/search"
          }
        };
        function StorageAdapter(store, runHook) {
          this.store = store;
          this.runHook = runHook
        }
        StorageAdapter.prototype.create = function(obj) {
          if (typeof obj === "undefined" || obj === null) {
            obj = {}
          }
          return this._cycle(obj, "create", "beforeAnnotationCreated", "annotationCreated")
        };
        StorageAdapter.prototype.update = function(obj) {
          if (typeof obj.id === "undefined" || obj.id === null) {
            throw new TypeError("annotation must have an id for update()")
          }
          return this._cycle(obj, "update", "beforeAnnotationUpdated", "annotationUpdated")
        };
        StorageAdapter.prototype["delete"] = function(obj) {
          if (typeof obj.id === "undefined" || obj.id === null) {
            throw new TypeError("annotation must have an id for delete()")
          }
          return this._cycle(obj, "delete", "beforeAnnotationDeleted", "annotationDeleted")
        };
        StorageAdapter.prototype.query = function(query) {
          return Promise.resolve(this.store.query(query))
        };
        StorageAdapter.prototype.load = function(query) {
          var self = this;
          return this.query(query).then(function(data) {
            self.runHook("annotationsLoaded", [data.results])
          })
        };
        StorageAdapter.prototype._cycle = function(obj, storeFunc, beforeEvent, afterEvent) {
          var self = this;
          return this.runHook(beforeEvent, [obj]).then(function() {
            var safeCopy = $.extend(true, {}, obj);
            delete safeCopy._local;
            var result = self.store[storeFunc](safeCopy);
            return Promise.resolve(result)
          }).then(function(ret) {
            for (var k in obj) {
              if (obj.hasOwnProperty(k)) {
                if (k !== "_local") {
                  delete obj[k]
                }
              }
            }
            $.extend(obj, ret);
            self.runHook(afterEvent, [obj]);
            return obj
          })
        };
        exports.StorageAdapter = StorageAdapter
      }, {
        "./util": 39
      }
    ],
    28: [
      function(require, module, exports) {
        exports.main = require("./ui/main").main;
        exports.adder = require("./ui/adder");
        exports.editor = require("./ui/editor");
        exports.filter = require("./ui/filter");
        exports.highlighter = require("./ui/highlighter");
        exports.markdown = require("./ui/markdown");
        exports.tags = require("./ui/tags");
        exports.textselector = require("./ui/textselector");
        exports.viewer = require("./ui/viewer");
        exports.widget = require("./ui/widget")
      }, {
        "./ui/adder": 29,
        "./ui/editor": 30,
        "./ui/filter": 31,
        "./ui/highlighter": 32,
        "./ui/main": 33,
        "./ui/markdown": 34,
        "./ui/tags": 35,
        "./ui/textselector": 36,
        "./ui/viewer": 37,
        "./ui/widget": 38
      }
    ],
    29: [
      function(require, module, exports) {
        "use strict";
        var Widget = require("./widget").Widget,
          util = require("../util");
        var $ = util.$;
        var _t = util.gettext;
        var NS = "annotator-adder";
        var Adder = Widget.extend({
          constructor: function(options) {
            Widget.call(this, options);
            this.ignoreMouseup = false;
            this.annotation = null;
            this.onCreate = this.options.onCreate;
            var self = this;
            this.element.on("click." + NS, "button", function(e) {
              self._onClick(e)
            }).on("mousedown." + NS, "button", function(e) {
              self._onMousedown(e)
            });
            this.document = this.element[0].ownerDocument;
            $(this.document.body).on("mouseup." + NS, function(e) {
              self._onMouseup(e)
            })
          },
          destroy: function() {
            this.element.off("." + NS);
            $(this.document.body).off("." + NS);
            Widget.prototype.destroy.call(this)
          },
          load: function(annotation, position) {
            this.annotation = annotation;
            this.show(position)
          },
          show: function(position) {
            if (typeof position !== "undefined" && position !== null) {
              this.element.css({top: position.top, left: position.left})
            }
            Widget.prototype.show.call(this)
          },
          _onMousedown: function(event) {
            if (event.which > 1) {
              return
            }
            event.preventDefault();
            this.ignoreMouseup = true
          },
          _onMouseup: function(event) {
            if (event.which > 1) {
              return
            }
            if (this.ignoreMouseup) {
              event.stopImmediatePropagation()
            }
          },
          _onClick: function(event) {
            if (event.which > 1) {
              return
            }
            event.preventDefault();
            this.hide();
            this.ignoreMouseup = false;
            if (this.annotation !== null && typeof this.onCreate === "function") {
              this.onCreate(this.annotation, event)
            }
          }
        });
        Adder.template = [
          '<div class="annotator-adder annotator-hide">', '  <button type="button">' + _t("Annotate") + "</button>",
          "</div>"
        ].join("\n");
        Adder.options = {
          onCreate: null
        };
        exports.Adder = Adder
      }, {
        "../util": 39,
        "./widget": 38
      }
    ],
    30: [
      function(require, module, exports) {
        "use strict";
        var Widget = require("./widget").Widget,
          util = require("../util");
        var $ = util.$;
        var _t = util.gettext;
        var Promise = util.Promise;
        var NS = "annotator-editor";
        var id = function() {
          var counter;
          counter = -1;
          return function() {
            return counter += 1
          }
        }();
        function preventEventDefault(event) {
          if (typeof event !== "undefined" && event !== null && typeof event.preventDefault === "function") {
            event.preventDefault()
          }
        }
        var dragTracker = exports.dragTracker = function dragTracker(handle, callback) {
          var lastPos = null,
            throttled = false;
          function mouseMove(e) {
            if (throttled || lastPos === null) {
              return
            }
            var delta = {
              y: e.pageY - lastPos.top,
              x: e.pageX - lastPos.left
            };
            var trackLastMove = true;
            if (typeof callback === "function") {
              trackLastMove = callback(delta)
            }
            if (trackLastMove !== false) {
              lastPos = {
                top: e.pageY,
                left: e.pageX
              }
            }
            throttled = true;
            setTimeout(function() {
              throttled = false
            }, 1e3 / 60)
          }
          function mouseUp() {
            lastPos = null;
            $(handle.ownerDocument).off("mouseup", mouseUp).off("mousemove", mouseMove)
          }
          function mouseDown(e) {
            if (e.target !== handle) {
              return
            }
            lastPos = {
              top: e.pageY,
              left: e.pageX
            };
            $(handle.ownerDocument).on("mouseup", mouseUp).on("mousemove", mouseMove);
            e.preventDefault()
          }
          function destroy() {
            $(handle).off("mousedown", mouseDown)
          }
          $(handle).on("mousedown", mouseDown);
          return {destroy: destroy}
        };
        var resizer = exports.resizer = function resizer(element, handle, options) {
          var $el = $(element);
          if (typeof options === "undefined" || options === null) {
            options = {}
          }
          function translate(delta) {
            var directionX = 1,
              directionY = -1;
            if (typeof options.invertedX === "function" && options.invertedX()) {
              directionX = -1
            }
            if (typeof options.invertedY === "function" && options.invertedY()) {
              directionY = 1
            }
            return {x: delta.directionX, y: delta.directionY}
          }
          function resize(delta) {
            var height = $el.height(),
              width = $el.width(),
              translated = translate(delta);
            if (Math.abs(translated.x) > 0) {
              $el.width(width + translated.x)
            }
            if (Math.abs(translated.y) > 0) {
              $el.height(height + translated.y)
            }
            var didChange = $el.height() !== height || $el.width() !== width;
            return didChange
          }
          return dragTracker(handle, resize)
        };
        var mover = exports.mover = function mover(element, handle) {
          function move(delta) {
            $(element).css({
              top: parseInt($(element).css("top"), 10) + delta.y,
              left: parseInt($(element).css("left"), 10) + delta.x
            })
          }
          return dragTracker(handle, move)
        };
        var Editor = exports.Editor = Widget.extend({
          constructor: function(options) {
            Widget.call(this, options);
            this.fields = [];
            this.annotation = {};
            if (this.options.defaultFields) {
              this.addField({
                type: "textarea",
                label: _t("Comments") + "…",
                load: function(field, annotation) {
                  $(field).find("textarea").val(annotation.text || "")
                },
                submit: function(field, annotation) {
                  annotation.text = $(field).find("textarea").val()
                }
              })
            }
            var self = this;
            this.element.on("submit." + NS, "form", function(e) {
              self._onFormSubmit(e)
            }).on("click." + NS, ".annotator-save", function(e) {
              self._onSaveClick(e)
            }).on("click." + NS, ".annotator-cancel", function(e) {
              self._onCancelClick(e)
            }).on("mouseover." + NS, ".annotator-cancel", function(e) {
              self._onCancelMouseover(e)
            }).on("keydown." + NS, "textarea", function(e) {
              self._onTextareaKeydown(e)
            })
          },
          destroy: function() {
            this.element.off("." + NS);
            Widget.prototype.destroy.call(this)
          },
          show: function(position) {
            if (typeof position !== "undefined" && position !== null) {
              this.element.css({top: position.top, left: position.left})
            }
            this.element.find(".annotator-save").addClass(this.classes.focus);
            Widget.prototype.show.call(this);
            this.element.find(":input:first").focus();
            this._setupDraggables()
          },
          load: function(annotation, position) {
            this.annotation = annotation;
            for (var i = 0, len = this.fields.length; i < len; i++) {
              var field = this.fields[i];
              field.load(field.element, this.annotation)
            }
            var self = this;
            return new Promise(function(resolve, reject) {
              self.dfd = {
                resolve: resolve,
                reject: reject
              };
              self.show(position)
            })
          },
          submit: function() {
            for (var i = 0, len = this.fields.length; i < len; i++) {
              var field = this.fields[i];
              field.submit(field.element, this.annotation)
            }
            if (typeof this.dfd !== "undefined" && this.dfd !== null) {
              this.dfd.resolve()
            }
            this.hide()
          },
          cancel: function() {
            if (typeof this.dfd !== "undefined" && this.dfd !== null) {
              this.dfd.reject("editing cancelled")
            }
            this.hide()
          },
          addField: function(options) {
            var field = $.extend({
              id: "annotator-field-" + id(),
              type: "input",
              label: "",
              load: function() {},
              submit: function() {}
            }, options);
            var input = null,
              element = $('<li class="annotator-item" />');
            field.element = element[0];
            if (field.type === "textarea") {
              input = $("<textarea />")
            } else if (field.type === "checkbox") {
              input = $('<input type="checkbox" />')
            } else if (field.type === "input") {
              input = $("<input />")
            } else if (field.type === "select") {
              input = $("<select />")
            }
            element.append(input);
            input.attr({id: field.id, placeholder: field.label});
            if (field.type === "checkbox") {
              element.addClass("annotator-checkbox");
              element.append($("<label />", {
                "for": field.id,
                html: field.label
              }))
            }
            this.element.find("ul:first").append(element);
            this.fields.push(field);
            return field.element
          },
          checkOrientation: function() {
            Widget.prototype.checkOrientation.call(this);
            var list = this.element.find("ul").first(),
              controls = this.element.find(".annotator-controls");
            if (this.element.hasClass(this.classes.invert.y)) {
              controls.insertBefore(list)
            } else if (controls.is(":first-child")) {
              controls.insertAfter(list)
            }
            return this
          },
          _onFormSubmit: function(event) {
            preventEventDefault(event);
            this.submit()
          },
          _onSaveClick: function(event) {
            preventEventDefault(event);
            this.submit()
          },
          _onCancelClick: function(event) {
            preventEventDefault(event);
            this.cancel()
          },
          _onCancelMouseover: function() {
            this.element.find("." + this.classes.focus).removeClass(this.classes.focus)
          },
          _onTextareaKeydown: function(event) {
            if (event.which === 27) {
              this.cancel()
            } else if (event.which === 13 && !event.shiftKey) {
              this.submit()
            }
          },
          _setupDraggables: function() {
            if (typeof this._resizer !== "undefined" && this._resizer !== null) {
              this._resizer.destroy()
            }
            if (typeof this._mover !== "undefined" && this._mover !== null) {
              this._mover.destroy()
            }
            this.element.find(".annotator-resize").remove();
            var cornerItem;
            if (this.element.hasClass(this.classes.invert.y)) {
              cornerItem = this.element.find(".annotator-item:last")
            } else {
              cornerItem = this.element.find(".annotator-item:first")
            }
            if (cornerItem) {
              $('<span class="annotator-resize"></span>').appendTo(cornerItem)
            }
            var controls = this.element.find(".annotator-controls")[0],
              textarea = this.element.find("textarea:first")[0],
              resizeHandle = this.element.find(".annotator-resize")[0],
              self = this;
            this._resizer = resizer(textarea, resizeHandle, {
              invertedX: function() {
                return self.element.hasClass(self.classes.invert.x)
              },
              invertedY: function() {
                return self.element.hasClass(self.classes.invert.y)
              }
            });
            this._mover = mover(this.element[0], controls)
          }
        });
        Editor.classes = {
          hide: "annotator-hide",
          focus: "annotator-focus"
        };
        Editor.template = [
          '<div class="annotator-outer annotator-editor annotator-hide">', '  <form class="annotator-widget">', '    <ul class="annotator-listing"></ul>', '    <div class="annotator-controls">', '     <a href="#cancel" class="annotator-cancel">' + _t("Cancel") + "</a>",
          '      <a href="#save"',
          '         class="annotator-save annotator-focus">' + _t("Save") + "</a>",
          "    </div>",
          "  </form>",
          "</div>"
        ].join("\n");
        Editor.options = {
          defaultFields: true
        };
        exports.standalone = function standalone(options) {
          var widget = new exports.Editor(options);
          return {
            destroy: function() {
              widget.destroy()
            },
            beforeAnnotationCreated: function(annotation) {
              return widget.load(annotation)
            },
            beforeAnnotationUpdated: function(annotation) {
              return widget.load(annotation)
            }
          }
        }
      }, {
        "../util": 39,
        "./widget": 38
      }
    ],
    31: [
      function(require, module, exports) {
        "use strict";
        var util = require("../util");
        var $ = util.$;
        var _t = util.gettext;
        var NS = "annotator-filter";
        var Filter = exports.Filter = function Filter(options) {
          this.options = $.extend(true, {}, Filter.options, options);
          this.classes = $.extend(true, {}, Filter.classes);
          this.element = $(Filter.html.element).appendTo(this.options.appendTo);
          this.filter = $(Filter.html.filter);
          this.filters = [];
          this.current = 0;
          for (var i = 0, len = this.options.filters.length; i < len; i++) {
            var filter = this.options.filters[i];
            this.addFilter(filter)
          }
          this.updateHighlights();
          var filterInput = ".annotator-filter-property input",
            self = this;
          this.element.on("focus." + NS, filterInput, function(e) {
            self._onFilterFocus(e)
          }).on("blur." + NS, filterInput, function(e) {
            self._onFilterBlur(e)
          }).on("keyup." + NS, filterInput, function(e) {
            self._onFilterKeyup(e)
          }).on("click." + NS, ".annotator-filter-previous", function(e) {
            self._onPreviousClick(e)
          }).on("click." + NS, ".annotator-filter-next", function(e) {
            self._onNextClick(e)
          }).on("click." + NS, ".annotator-filter-clear", function(e) {
            self._onClearClick(e)
          });
          this._insertSpacer();
          if (this.options.addAnnotationFilter) {
            this.addFilter({label: _t("Annotation"), property: "text"})
          }
        };
        Filter.prototype.destroy = function() {
          var html = $("html"),
            currentMargin = parseInt(html.css("padding-top"), 10) || 0;
          html.css("padding-top", currentMargin - this.element.outerHeight());
          this.element.off("." + NS);
          this.element.remove()
        };
        Filter.prototype._insertSpacer = function() {
          var html = $("html"),
            currentMargin = parseInt(html.css("padding-top"), 10) || 0;
          html.css("padding-top", currentMargin + this.element.outerHeight());
          return this
        };
        Filter.prototype.addFilter = function(options) {
          var filter = $.extend({
            label: "",
            property: "",
            isFiltered: this.options.isFiltered
          }, options);
          var hasFilterForProp = false;
          for (var i = 0, len = this.filters.length; i < len; i++) {
            var f = this.filters[i];
            if (f.property === filter.property) {
              hasFilterForProp = true;
              break
            }
          }
          if (!hasFilterForProp) {
            filter.id = "annotator-filter-" + filter.property;
            filter.annotations = [];
            filter.element = this.filter.clone().appendTo(this.element);
            filter.element.find("label").html(filter.label).attr("for", filter.id);
            filter.element.find("input").attr({
              id: filter.id,
              placeholder: _t("Filter by ") + filter.label + "…"
            });
            filter.element.find("button").hide();
            filter.element.data("filter", filter);
            this.filters.push(filter)
          }
          return this
        };
        Filter.prototype.updateFilter = function(filter) {
          filter.annotations = [];
          this.updateHighlights();
          this.resetHighlights();
          var input = $.trim(filter.element.find("input").val());
          if (!input) {
            return
          }
          var annotations = this.highlights.map(function() {
            return $(this).data("annotation")
          });
          annotations = $.makeArray(annotations);
          for (var i = 0, len = annotations.length; i < len; i++) {
            var annotation = annotations[i],
              property = annotation[filter.property];
            if (filter.isFiltered(input, property)) {
              filter.annotations.push(annotation)
            }
          }
          this.filterHighlights()
        };
        Filter.prototype.updateHighlights = function() {
          this.highlights = $(this.options.filterElement).find(".annotator-hl:visible");
          this.filtered = this.highlights.not(this.classes.hl.hide)
        };
        Filter.prototype.filterHighlights = function() {
          var activeFilters = $.grep(this.filters, function(filter) {
            return Boolean(filter.annotations.length)
          });
          var filtered = [];
          if (activeFilters.length > 0) {
            filtered = activeFilters[0].annotations
          }
          if (activeFilters.length > 1) {
            var annotations = [];
            $.each(activeFilters, function() {
              $.merge(annotations, this.annotations)
            });
            var uniques = [];
            filtered = [];
            $.each(annotations, function() {
              if ($.inArray(this, uniques) === -1) {
                uniques.push(this)
              } else {
                filtered.push(this)
              }
            })
          }
          var highlights = this.highlights;
          for (var i = 0, len = filtered.length; i < len; i++) {
            highlights = highlights.not(filtered[i]._local.highlights)
          }
          highlights.addClass(this.classes.hl.hide);
          this.filtered = this.highlights.not(this.classes.hl.hide);
          return this
        };
        Filter.prototype.resetHighlights = function() {
          this.highlights.removeClass(this.classes.hl.hide);
          this.filtered = this.highlights;
          return this
        };
        Filter.prototype._onFilterFocus = function(event) {
          var input = $(event.target);
          input.parent().addClass(this.classes.active);
          input.next("button").show()
        };
        Filter.prototype._onFilterBlur = function(event) {
          if (!event.target.value) {
            var input = $(event.target);
            input.parent().removeClass(this.classes.active);
            input.next("button").hide()
          }
        };
        Filter.prototype._onFilterKeyup = function(event) {
          var filter = $(event.target).parent().data("filter");
          if (filter) {
            this.updateFilter(filter)
          }
        };
        Filter.prototype._findNextHighlight = function(previous) {
          if (this.highlights.length === 0) {
            return this
          }
          var offset = -1,
            resetOffset = 0,
            operator = "gt";
          if (previous) {
            offset = 0;
            resetOffset = -1;
            operator = "lt"
          }
          var active = this.highlights.not("." + this.classes.hl.hide),
            current = active.filter("." + this.classes.hl.active);
          if (current.length === 0) {
            current = active.eq(offset)
          }
          var annotation = current.data("annotation");
          var index = active.index(current[0]),
            next = active.filter(":" + operator + "(" + index + ")").not(annotation._local.highlights).eq(resetOffset);
          if (next.length === 0) {
            next = active.eq(resetOffset)
          }
          this._scrollToHighlight(next.data("annotation")._local.highlights)
        };
        Filter.prototype._onNextClick = function() {
          this._findNextHighlight()
        };
        Filter.prototype._onPreviousClick = function() {
          this._findNextHighlight(true)
        };
        Filter.prototype._scrollToHighlight = function(highlight) {
          highlight = $(highlight);
          this.highlights.removeClass(this.classes.hl.active);
          highlight.addClass(this.classes.hl.active);
          $("html, body").animate({
            scrollTop: highlight.offset().top - (this.element.height() + 20)
          }, 150)
        };
        Filter.prototype._onClearClick = function(event) {
          $(event.target).prev("input").val("").keyup().blur()
        };
        Filter.classes = {
          active: "annotator-filter-active",
          hl: {
            hide: "annotator-hl-filtered",
            active: "annotator-hl-active"
          }
        };
        Filter.html = {
          element: [
            '<div class="annotator-filter">', "  <strong>" + _t("Navigate:") + "</strong>",
            '  <span class="annotator-filter-navigation">',
            '    <button type="button"',
            '            class="annotator-filter-previous">' + _t("Previous") + "</button>",
            '    <button type="button"',
            '            class="annotator-filter-next">' + _t("Next") + "</button>",
            "  </span>",
            "  <strong>" + _t("Filter by:") + "</strong>",
            "</div>"
          ].join("\n"),
          filter: [
            '<span class="annotator-filter-property">', "  <label></label>", "  <input/>", '  <button type="button"', '          class="annotator-filter-clear">' + _t("Clear") + "</button>",
            "</span>"
          ].join("\n")
        };
        Filter.options = {
          appendTo: "body",
          filterElement: "body",
          filters: [],
          addAnnotationFilter: true,
          isFiltered: function(input, property) {
            if (!(input && property)) {
              return false
            }
            var keywords = input.split(/\s+/);
            for (var i = 0, len = keywords.length; i < len; i++) {
              if (property.indexOf(keywords[i]) === -1) {
                return false
              }
            }
            return true
          }
        };
        exports.standalone = function(options) {
          var widget = new exports.Filter(options);
          return {
            destroy: function() {
              widget.destroy()
            },
            annotationsLoaded: function() {
              widget.updateHighlights()
            },
            annotationCreated: function() {
              widget.updateHighlights()
            },
            annotationUpdated: function() {
              widget.updateHighlights()
            },
            annotationDeleted: function() {
              widget.updateHighlights()
            }
          }
        }
      }, {
        "../util": 39
      }
    ],
    32: [
      function(require, module, exports) {
        (function(global) {
          "use strict";
          var Range = require("xpath-range").Range;
          var util = require("../util");
          var $ = util.$;
          var Promise = util.Promise;
          function highlightRange(normedRange, cssClass) {
            if (typeof cssClass === "undefined" || cssClass === null) {
              cssClass = "annotator-hl"
            }
            var white = /^\s*$/;
            var nodes = normedRange.textNodes(),
              results = [];
            for (var i = 0, len = nodes.length; i < len; i++) {
              var node = nodes[i];
              if (!white.test(node.nodeValue)) {
                var hl = global.document.createElement("span");
                hl.className = cssClass;
                node.parentNode.replaceChild(hl, node);
                hl.appendChild(node);
                results.push(hl)
              }
            }
            return results
          }
          function reanchorRange(range, rootElement) {
            try {
              return Range.sniff(range).normalize(rootElement)
            } catch (e) {
              if (!(e instanceof Range.RangeError)) {
                throw e
              }
            }
            return null
          }
          var Highlighter = exports.Highlighter = function Highlighter(element, options) {
            this.element = element;
            this.options = $.extend(true, {}, Highlighter.options, options)
          };
          Highlighter.prototype.destroy = function() {
            $(this.element).find("." + this.options.highlightClass).each(function(_, el) {
              $(el).contents().insertBefore(el);
              $(el).remove()
            })
          };
          Highlighter.prototype.drawAll = function(annotations) {
            var self = this;
            var p = new Promise(function(resolve) {
              var highlights = [];
              function loader(annList) {
                if (typeof annList === "undefined" || annList === null) {
                  annList = []
                }
                var now = annList.splice(0, self.options.chunkSize);
                for (var i = 0, len = now.length; i < len; i++) {
                  highlights = highlights.concat(self.draw(now[i]))
                }
                if (annList.length > 0) {
                  setTimeout(function() {
                    loader(annList)
                  }, self.options.chunkDelay)
                } else {
                  resolve(highlights)
                }
              }
              var clone = annotations.slice();
              loader(clone)
            });
            return p
          };
          Highlighter.prototype.draw = function(annotation) {
            var normedRanges = [];
            for (var i = 0, ilen = annotation.ranges.length; i < ilen; i++) {
              var r = reanchorRange(annotation.ranges[i], this.element);
              if (r !== null) {
                normedRanges.push(r)
              }
            }
            var hasLocal = typeof annotation._local !== "undefined" && annotation._local !== null;
            if (!hasLocal) {
              annotation._local = {}
            }
            var hasHighlights = typeof annotation._local.highlights !== "undefined" && annotation._local.highlights === null;
            if (!hasHighlights) {
              annotation._local.highlights = []
            }
            for (var j = 0, jlen = normedRanges.length; j < jlen; j++) {
              var normed = normedRanges[j];
              $.merge(annotation._local.highlights, highlightRange(normed, this.options.highlightClass))
            }
            $(annotation._local.highlights).data("annotation", annotation);
            if (typeof annotation.id !== "undefined" && annotation.id !== null) {
              $(annotation._local.highlights).attr("data-annotation-id", annotation.id)
            }
            return annotation._local.highlights
          };
          Highlighter.prototype.undraw = function(annotation) {
            var hasHighlights = typeof annotation._local !== "undefined" && annotation._local !== null && typeof annotation._local.highlights !== "undefined" && annotation._local.highlights !== null;
            if (!hasHighlights) {
              return
            }
            for (var i = 0, len = annotation._local.highlights.length; i < len; i++) {
              var h = annotation._local.highlights[i];
              if (h.parentNode !== null) {
                $(h).replaceWith(h.childNodes)
              }
            }
            delete annotation._local.highlights
          };
          Highlighter.prototype.redraw = function(annotation) {
            this.undraw(annotation);
            return this.draw(annotation)
          };
          Highlighter.options = {
            highlightClass: "annotator-hl",
            chunkSize: 10,
            chunkDelay: 10
          };
          exports.standalone = function standalone(element, options) {
            var widget = exports.Highlighter(element, options);
            return {
              destroy: function() {
                widget.destroy()
              },
              annotationsLoaded: function(anns) {
                widget.drawAll(anns)
              },
              annotationCreated: function(ann) {
                widget.draw(ann)
              },
              annotationDeleted: function(ann) {
                widget.undraw(ann)
              },
              annotationUpdated: function(ann) {
                widget.redraw(ann)
              }
            }
          }
        }).call(this, typeof global !== "undefined"
          ? global
          : typeof self !== "undefined"
            ? self
            : typeof window !== "undefined"
              ? window
              : {})
      }, {
        "../util": 39,
        "xpath-range": 18
      }
    ],
    33: [
      function(require, module, exports) {
        (function(global) {
          "use strict";
          var util = require("../util");
          var adder = require("./adder");
          var editor = require("./editor");
          var highlighter = require("./highlighter");
          var textselector = require("./textselector");
          var viewer = require("./viewer");
          var _t = util.gettext;
          function trim(s) {
            if (typeof String.prototype.trim === "function") {
              return String.prototype.trim.call(s)
            } else {
              return s.replace(/^[\s\xA0]+|[\s\xA0]+$/g, "")
            }
          }
          function annotationFactory(contextEl, ignoreSelector) {
            return function(ranges) {
              var text = [],
                serializedRanges = [];
              for (var i = 0, len = ranges.length; i < len; i++) {
                var r = ranges[i];
                text.push(trim(r.text()));
                serializedRanges.push(r.serialize(contextEl, ignoreSelector))
              }
              return {quote: text.join(" / "), ranges: serializedRanges}
            }
          }
          function maxZIndex(elements) {
            var max = -1;
            for (var i = 0, len = elements.length; i < len; i++) {
              var $el = util.$(elements[i]);
              if ($el.css("position") !== "static") {
                var zIndex = parseFloat($el.css("z-index"));
                if (zIndex > max) {
                  max = zIndex
                }
              }
            }
            return max
          }
          function injectDynamicStyle() {
            util.$("#annotator-dynamic-style").remove();
            var sel = "*" +
            ":not(annotator-adder)" +
            ":not(annotator-outer)" +
            ":not(annotator-notice)" +
            ":not(annotator-filter)";
            var max = maxZIndex(util.$(global.document.body).find(sel).get());
            max = Math.max(max, 1e3);
            var rules = [
              ".annotator-adder, .annotator-outer, .annotator-notice {", "  z-index: " + (max + 20) + ";",
              "}",
              ".annotator-filter {",
              "  z-index: " + (max + 10) + ";",
              "}"
            ].join("\n");
            util.$("<style>" + rules + "</style>").attr("id", "annotator-dynamic-style").attr("type", "text/css").appendTo("head")
          }
          function removeDynamicStyle() {
            util.$("#annotator-dynamic-style").remove()
          }
          function addPermissionsCheckboxes(editor, ident, authz) {
            function createLoadCallback(action) {
              return function loadCallback(field, annotation) {
                field = util.$(field).show();
                var u = ident.who();
                var input = field.find("input");
                if (typeof u === "undefined" || u === null) {
                  field.hide()
                }
                if (!authz.permits("admin", annotation, u)) {
                  field.hide()
                }
                if (authz.permits(action, annotation, null)) {
                  input.attr("checked", "checked")
                } else {
                  input.removeAttr("checked")
                }
              }
            }
            function createSubmitCallback(action) {
              return function submitCallback(field, annotation) {
                var u = ident.who();
                if (typeof u === "undefined" || u === null) {
                  return
                }
                if (!annotation.permissions) {
                  annotation.permissions = {}
                }
                if (util.$(field).find("input").is(":checked")) {
                  delete annotation.permissions[action]
                } else {
                  annotation.permissions[action] = [authz.authorizedUserId(u)]
                }
              }
            }
            editor.addField({type: "checkbox", label: _t("Allow anyone to <strong>view</strong> this annotation"), load: createLoadCallback("read"), submit: createSubmitCallback("read")});
            editor.addField({type: "checkbox", label: _t("Allow anyone to <strong>edit</strong> this annotation"), load: createLoadCallback("update"), submit: createSubmitCallback("update")})
          }
          function main(options) {
            if (typeof options === "undefined" || options === null) {
              options = {}
            }
            options.element = options.element || global.document.body;
            options.editorExtensions = options.editorExtensions || [];
            options.viewerExtensions = options.viewerExtensions || [];
            var makeAnnotation = annotationFactory(options.element, ".annotator-hl");
            var s = {
              interactionPoint: null
            };
            function start(app) {
              var ident = app.registry.getUtility("identityPolicy");
              var authz = app.registry.getUtility("authorizationPolicy");
              s.adder = new adder.Adder({
                onCreate: function(ann) {
                  app.annotations.create(ann)
                }
              });
              s.adder.attach();
              s.editor = new editor.Editor({extensions: options.editorExtensions});
              s.editor.attach();
              addPermissionsCheckboxes(s.editor, ident, authz);
              s.highlighter = new highlighter.Highlighter(options.element);
              s.textselector = new textselector.TextSelector(options.element, {
                onSelection: function(ranges, event) {
                  if (ranges.length > 0) {
                    var annotation = makeAnnotation(ranges);
                    s.interactionPoint = util.mousePosition(event);
                    s.adder.load(annotation, s.interactionPoint)
                  } else {
                    s.adder.hide()
                  }
                }
              });
              s.viewer = new viewer.Viewer({
                onEdit: function(ann) {
                  s.interactionPoint = util.$(s.viewer.element).css(["top", "left"]);
                  app.annotations.update(ann)
                },
                onDelete: function(ann) {
                  app.annotations["delete"](ann)
                },
                permitEdit: function(ann) {
                  return authz.permits("update", ann, ident.who())
                },
                permitDelete: function(ann) {
                  return authz.permits("delete", ann, ident.who())
                },
                autoViewHighlights: options.element,
                extensions: options.viewerExtensions
              });
              s.viewer.attach();
              injectDynamicStyle()
            }
            return {
              start: start,
              destroy: function() {
                s.adder.destroy();
                s.editor.destroy();
                s.highlighter.destroy();
                s.textselector.destroy();
                s.viewer.destroy();
                removeDynamicStyle()
              },
              annotationsLoaded: function(anns) {
                s.highlighter.drawAll(anns)
              },
              annotationCreated: function(ann) {
                s.highlighter.draw(ann)
              },
              annotationDeleted: function(ann) {
                s.highlighter.undraw(ann)
              },
              annotationUpdated: function(ann) {
                s.highlighter.redraw(ann)
              },
              beforeAnnotationCreated: function(annotation) {
                return s.editor.load(annotation, s.interactionPoint)
              },
              beforeAnnotationUpdated: function(annotation) {
                return s.editor.load(annotation, s.interactionPoint)
              }
            }
          }
          exports.main = main
        }).call(this, typeof global !== "undefined"
          ? global
          : typeof self !== "undefined"
            ? self
            : typeof window !== "undefined"
              ? window
              : {})
      }, {
        "../util": 39,
        "./adder": 29,
        "./editor": 30,
        "./highlighter": 32,
        "./textselector": 36,
        "./viewer": 37
      }
    ],
    34: [
      function(require, module, exports) {
        (function(global) {
          "use strict";
          var util = require("../util");
          var _t = util.gettext;
          var render = exports.render = function render(annotation) {
            var convert = util.escapeHtml;
            if (global.showdown && typeof global.showdown.Converter === "function") {
              convert = (new global.showdown.Converter).makeHtml
            }
            if (annotation.text) {
              return convert(annotation.text)
            } else {
              return "<i>" + _t("No comment") + "</i>"
            }
          };
          exports.viewerExtension = function viewerExtension(viewer) {
            if (!global.showdown || typeof global.showdown.Converter !== "function") {
              console.warn(_t("To use the Markdown plugin, you must " +
                "include Showdown into the page first."))
            }
            viewer.setRenderer(render)
          }
        }).call(this, typeof global !== "undefined"
          ? global
          : typeof self !== "undefined"
            ? self
            : typeof window !== "undefined"
              ? window
              : {})
      }, {
        "../util": 39
      }
    ],
    35: [
      function(require, module, exports) {
        "use strict";
        var util = require("../util");
        var $ = util.$;
        var _t = util.gettext;
        function stringifyTags(array) {
          return array.join(" ")
        }
        function parseTags(string) {
          string = $.trim(string);
          var tags = [];
          if (string) {
            tags = string.split(/\s+/)
          }
          return tags
        }
        exports.viewerExtension = function viewerExtension(v) {
          function updateViewer(field, annotation) {
            field = $(field);
            if (annotation.tags && $.isArray(annotation.tags) && annotation.tags.length) {
              field.addClass("annotator-tags").html(function() {
                return $.map(annotation.tags, function(tag) {
                  return '<span class="annotator-tag">' + util.escapeHtml(tag) + "</span>"
                }).join(" ")
              })
            } else {
              field.remove()
            }
          }
          v.addField({load: updateViewer})
        };
        exports.editorExtension = function editorExtension(e) {
          var field = null;
          var input = null;
          function updateField(field, annotation) {
            var value = "";
            if (annotation.tags) {
              value = stringifyTags(annotation.tags)
            }
            input.val(value)
          }
          function setAnnotationTags(field, annotation) {
            annotation.tags = parseTags(input.val())
          }
          field = e.addField({
            label: _t("Add some tags here") + "…",
            load: updateField,
            submit: setAnnotationTags
          });
          input = $(field).find(":input")
        }
      }, {
        "../util": 39
      }
    ],
    36: [
      function(require, module, exports) {
        (function(global) {
          "use strict";
          var Range = require("xpath-range").Range;
          var util = require("../util");
          var $ = util.$;
          var TEXTSELECTOR_NS = "annotator-textselector";
          function isAnnotator(element) {
            var elAndParents = $(element).parents().addBack();
            return elAndParents.filter("[class^=annotator-]").length !== 0
          }
          function TextSelector(element, options) {
            this.element = element;
            this.options = $.extend(true, {}, TextSelector.options, options);
            this.onSelection = this.options.onSelection;
            if (typeof this.element.ownerDocument !== "undefined" && this.element.ownerDocument !== null) {
              var self = this;
              this.document = this.element.ownerDocument;
              $(this.document.body).on("mouseup." + TEXTSELECTOR_NS, function(e) {
                self._checkForEndSelection(e)
              })
            } else {
              console.warn("You created an instance of the TextSelector on an " +
                "element that doesn't have an ownerDocument. This won't " +
                "work! Please ensure the element is added to the DOM " +
                "before the plugin is configured:",
              this.element)
            }
          }
          TextSelector.prototype.destroy = function() {
            if (this.document) {
              $(this.document.body).off("." + TEXTSELECTOR_NS)
            }
          };
          TextSelector.prototype.captureDocumentSelection = function() {
            var i,
              len,
              ranges = [],
              rangesToIgnore = [],
              selection = global.getSelection();
            if (selection.isCollapsed) {
              return []
            }
            for (i = 0; i < selection.rangeCount; i++) {
              var r = selection.getRangeAt(i),
                browserRange = new Range.BrowserRange(r),
                normedRange = browserRange.normalize().limit(this.element);
              if (normedRange === null) {
                rangesToIgnore.push(r)
              } else {
                ranges.push(normedRange)
              }
            }
            selection.removeAllRanges();
            for (i = 0, len = rangesToIgnore.length; i < len; i++) {
              selection.addRange(rangesToIgnore[i])
            }
            for (i = 0, len = ranges.length; i < len; i++) {
              var range = ranges[i],
                drange = this.document.createRange();
              drange.setStartBefore(range.start);
              drange.setEndAfter(range.end);
              selection.addRange(drange)
            }
            return ranges
          };
          TextSelector.prototype._checkForEndSelection = function(event) {
            var self = this;
            var _nullSelection = function() {
              if (typeof self.onSelection === "function") {
                self.onSelection([], event)
              }
            };
            var selectedRanges = this.captureDocumentSelection();
            if (selectedRanges.length === 0) {
              _nullSelection();
              return
            }
            for (var i = 0, len = selectedRanges.length; i < len; i++) {
              var container = selectedRanges[i].commonAncestor;
              if ($(container).hasClass("annotator-hl")) {
                container = $(container).parents("[class!=annotator-hl]")[0]
              }
              if (isAnnotator(container)) {
                _nullSelection();
                return
              }
            }
            if (typeof this.onSelection === "function") {
              this.onSelection(selectedRanges, event)
            }
          };
          TextSelector.options = {
            onSelection: null
          };
          exports.TextSelector = TextSelector
        }).call(this, typeof global !== "undefined"
          ? global
          : typeof self !== "undefined"
            ? self
            : typeof window !== "undefined"
              ? window
              : {})
      }, {
        "../util": 39,
        "xpath-range": 18
      }
    ],
    37: [
      function(require, module, exports) {
        "use strict";
        var Widget = require("./widget").Widget,
          util = require("../util");
        var $ = util.$,
          _t = util.gettext;
        var NS = "annotator-viewer";
        function parseLinks(data, rel, cond) {
          cond = $.extend({}, cond, {rel: rel});
          var results = [];
          for (var i = 0, len = data.length; i < len; i++) {
            var d = data[i],
              match = true;
            for (var k in cond) {
              if (cond.hasOwnProperty(k) && d[k] !== cond[k]) {
                match = false;
                break
              }
            }
            if (match) {
              results.push(d)
            }
          }
          return results
        }
        var Viewer = exports.Viewer = Widget.extend({
          constructor: function(options) {
            Widget.call(this, options);
            this.itemTemplate = Viewer.itemTemplate;
            this.fields = [];
            this.annotations = [];
            this.hideTimer = null;
            this.hideTimerDfd = null;
            this.hideTimerActivity = null;
            this.mouseDown = false;
            this.render = function(annotation) {
              if (annotation.text) {
                return util.escapeHtml(annotation.text)
              } else {
                return "<i>" + _t("No comment") + "</i>"
              }
            };
            var self = this;
            if (this.options.defaultFields) {
              this.addField({
                load: function(field, annotation) {
                  $(field).html(self.render(annotation))
                }
              })
            }
            if (typeof this.options.onEdit !== "function") {
              throw new TypeError("onEdit callback must be a function")
            }
            if (typeof this.options.onDelete !== "function") {
              throw new TypeError("onDelete callback must be a function")
            }
            if (typeof this.options.permitEdit !== "function") {
              throw new TypeError("permitEdit callback must be a function")
            }
            if (typeof this.options.permitDelete !== "function") {
              throw new TypeError("permitDelete callback must be a function")
            }
            if (this.options.autoViewHighlights) {
              this.document = this.options.autoViewHighlights.ownerDocument;
              $(this.options.autoViewHighlights).on("mouseover." + NS, ".annotator-hl", function(event) {
                if (event.target === this) {
                  self._onHighlightMouseover(event)
                }
              }).on("mouseleave." + NS, ".annotator-hl", function() {
                self._startHideTimer()
              });
              $(this.document.body).on("mousedown." + NS, function(e) {
                if (e.which === 1) {
                  self.mouseDown = true
                }
              }).on("mouseup." + NS, function(e) {
                if (e.which === 1) {
                  self.mouseDown = false
                }
              })
            }
            this.element.on("click." + NS, ".annotator-edit", function(e) {
              self._onEditClick(e)
            }).on("click." + NS, ".annotator-delete", function(e) {
              self._onDeleteClick(e)
            }).on("mouseenter." + NS, function() {
              self._clearHideTimer()
            }).on("mouseleave." + NS, function() {
              self._startHideTimer()
            })
          },
          destroy: function() {
            if (this.options.autoViewHighlights) {
              $(this.options.autoViewHighlights).off("." + NS);
              $(this.document.body).off("." + NS)
            }
            this.element.off("." + NS);
            Widget.prototype.destroy.call(this)
          },
          show: function(position) {
            if (typeof position !== "undefined" && position !== null) {
              this.element.css({top: position.top, left: position.left})
            }
            var controls = this.element.find(".annotator-controls").addClass(this.classes.showControls);
            var self = this;
            setTimeout(function() {
              controls.removeClass(self.classes.showControls)
            }, 500);
            Widget.prototype.show.call(this)
          },
          load: function(annotations, position) {
            this.annotations = annotations || [];
            var list = this.element.find("ul:first").empty();
            for (var i = 0, len = this.annotations.length; i < len; i++) {
              var annotation = this.annotations[i];
              this._annotationItem(annotation).appendTo(list).data("annotation", annotation)
            }
            this.show(position)
          },
          setRenderer: function(renderer) {
            this.render = renderer
          },
          _annotationItem: function(annotation) {
            var item = $(this.itemTemplate).clone();
            var controls = item.find(".annotator-controls"),
              link = controls.find(".annotator-link"),
              edit = controls.find(".annotator-edit"),
              del = controls.find(".annotator-delete");
            var links = parseLinks(annotation.links || [], "alternate", {type: "text/html"});
            var hasValidLink = links.length > 0 && typeof links[0].href !== "undefined" && links[0].href !== null;
            if (hasValidLink) {
              link.attr("href", links[0].href)
            } else {
              link.remove()
            }
            var controller = {};
            if (this.options.permitEdit(annotation)) {
              controller.showEdit = function() {
                edit.removeAttr("disabled")
              };
              controller.hideEdit = function() {
                edit.attr("disabled", "disabled")
              }
            } else {
              edit.remove()
            }
            if (this.options.permitDelete(annotation)) {
              controller.showDelete = function() {
                del.removeAttr("disabled")
              };
              controller.hideDelete = function() {
                del.attr("disabled", "disabled")
              }
            } else {
              del.remove()
            }
            for (var i = 0, len = this.fields.length; i < len; i++) {
              var field = this.fields[i];
              var element = $(field.element).clone().appendTo(item)[0];
              field.load(element, annotation, controller)
            }
            return item
          },
          addField: function(options) {
            var field = $.extend({
              load: function() {}
            }, options);
            field.element = $("<div />")[0];
            this.fields.push(field);
            return this
          },
          _onEditClick: function(event) {
            var item = $(event.target).parents(".annotator-annotation").data("annotation");
            this.hide();
            this.options.onEdit(item)
          },
          _onDeleteClick: function(event) {
            var item = $(event.target).parents(".annotator-annotation").data("annotation");
            this.hide();
            this.options.onDelete(item)
          },
          _onHighlightMouseover: function(event) {
            if (this.mouseDown) {
              return
            }
            var self = this;
            this._startHideTimer(true).done(function() {
              var annotations = $(event.target).parents(".annotator-hl").addBack().map(function(_, elem) {
                return $(elem).data("annotation")
              }).toArray();
              self.load(annotations, util.mousePosition(event))
            })
          },
          _startHideTimer: function(activity) {
            if (typeof activity === "undefined" || activity === null) {
              activity = false
            }
            if (this.hideTimer) {
              if (activity === false || this.hideTimerActivity === activity) {
                return this.hideTimerDfd
              } else {
                this._clearHideTimer()
              }
            }
            var timeout;
            if (activity) {
              timeout = this.options.activityDelay
            } else {
              timeout = this.options.inactivityDelay
            }
            this.hideTimerDfd = $.Deferred();
            if (!this.isShown()) {
              this.hideTimer = null;
              this.hideTimerDfd.resolve();
              this.hideTimerActivity = null
            } else {
              var self = this;
              this.hideTimer = setTimeout(function() {
                self.hide();
                self.hideTimerDfd.resolve();
                self.hideTimer = null
              }, timeout);
              this.hideTimerActivity = Boolean(activity)
            }
            return this.hideTimerDfd.promise()
          },
          _clearHideTimer: function() {
            clearTimeout(this.hideTimer);
            this.hideTimer = null;
            this.hideTimerDfd.reject();
            this.hideTimerActivity = null
          }
        });
        Viewer.classes = {
          showControls: "annotator-visible"
        };
        Viewer.template = ['<div class="annotator-outer annotator-viewer annotator-hide">', '  <ul class="annotator-widget annotator-listing"></ul>', "</div>"].join("\n");
        Viewer.itemTemplate = [
          '<li class="annotator-annotation annotator-item">', '  <span class="annotator-controls">', '    <a href="#"', '       title="' + _t("View as webpage") + '"',
          '       class="annotator-link">' + _t("View as webpage") + "</a>",
          '    <button type="button"',
          '            title="' + _t("Edit") + '"',
          '            class="annotator-edit">' + _t("Edit") + "</button>",
          '    <button type="button"',
          '            title="' + _t("Delete") + '"',
          '            class="annotator-delete">' + _t("Delete") + "</button>",
          "  </span>",
          "</li>"
        ].join("\n");
        Viewer.options = {
          defaultFields: true,
          inactivityDelay: 500,
          activityDelay: 100,
          permitEdit: function() {
            return false
          },
          permitDelete: function() {
            return false
          },
          autoViewHighlights: null,
          onEdit: function() {},
          onDelete: function() {}
        };
        exports.standalone = function standalone(options) {
          var widget;
          if (typeof options === "undefined" || options === null) {
            options = {}
          }
          return {
            start: function(app) {
              var ident = app.registry.getUtility("identityPolicy");
              var authz = app.registry.getUtility("authorizationPolicy");
              if (typeof options.onEdit === "undefined") {
                options.onEdit = function(annotation) {
                  app.annotations.update(annotation)
                }
              }
              if (typeof options.onDelete === "undefined") {
                options.onDelete = function(annotation) {
                  app.annotations["delete"](annotation)
                }
              }
              if (typeof options.permitEdit === "undefined") {
                options.permitEdit = function(annotation) {
                  return authz.permits("update", annotation, ident.who())
                }
              }
              if (typeof options.permitDelete === "undefined") {
                options.permitDelete = function(annotation) {
                  return authz.permits("delete", annotation, ident.who())
                }
              }
              widget = new exports.Viewer(options)
            },
            destroy: function() {
              widget.destroy()
            }
          }
        }
      }, {
        "../util": 39,
        "./widget": 38
      }
    ],
    38: [
      function(require, module, exports) {
        (function(global) {
          "use strict";
          var extend = require("backbone-extend-standalone");
          var util = require("../util");
          var $ = util.$;
          function Widget(options) {
            this.element = $(this.constructor.template);
            this.classes = $.extend({}, Widget.classes, this.constructor.classes);
            this.options = $.extend({}, Widget.options, this.constructor.options, options);
            this.extensionsInstalled = false
          }
          Widget.prototype.destroy = function() {
            this.element.remove()
          };
          Widget.prototype.installExtensions = function() {
            if (this.options.extensions) {
              for (var i = 0, len = this.options.extensions.length; i < len; i++) {
                var extension = this.options.extensions[i];
                extension(this)
              }
            }
          };
          Widget.prototype._maybeInstallExtensions = function() {
            if (!this.extensionsInstalled) {
              this.extensionsInstalled = true;
              this.installExtensions()
            }
          };
          Widget.prototype.attach = function() {
            this.element.appendTo(this.options.appendTo);
            this._maybeInstallExtensions()
          };
          Widget.prototype.show = function() {
            this.element.removeClass(this.classes.hide);
            this.checkOrientation()
          };
          Widget.prototype.hide = function() {
            $(this.element).addClass(this.classes.hide)
          };
          Widget.prototype.isShown = function() {
            return !$(this.element).hasClass(this.classes.hide)
          };
          Widget.prototype.checkOrientation = function() {
            this.resetOrientation();
            var $win = $(global),
              $widget = this.element.children(":first"),
              offset = $widget.offset(),
              viewport = {
                top: $win.scrollTop(),
                right: $win.width() + $win.scrollLeft()
              },
              current = {
                top: offset.top,
                right: offset.left + $widget.width()
              };
            if (current.top - viewport.top < 0) {
              this.invertY()
            }
            if (current.right - viewport.right > 0) {
              this.invertX()
            }
            return this
          };
          Widget.prototype.resetOrientation = function() {
            this.element.removeClass(this.classes.invert.x).removeClass(this.classes.invert.y);
            return this
          };
          Widget.prototype.invertX = function() {
            this.element.addClass(this.classes.invert.x);
            return this
          };
          Widget.prototype.invertY = function() {
            this.element.addClass(this.classes.invert.y);
            return this
          };
          Widget.prototype.isInvertedY = function() {
            return this.element.hasClass(this.classes.invert.y)
          };
          Widget.prototype.isInvertedX = function() {
            return this.element.hasClass(this.classes.invert.x)
          };
          Widget.classes = {
            hide: "annotator-hide",
            invert: {
              x: "annotator-invert-x",
              y: "annotator-invert-y"
            }
          };
          Widget.template = "<div></div>";
          Widget.options = {
            appendTo: "body"
          };
          Widget.extend = extend;
          exports.Widget = Widget
        }).call(this, typeof global !== "undefined"
          ? global
          : typeof self !== "undefined"
            ? self
            : typeof window !== "undefined"
              ? window
              : {})
      }, {
        "../util": 39,
        "backbone-extend-standalone": 3
      }
    ],
    39: [
      function(require, module, exports) {
        (function(global) {
          "use strict";
          var $ = require("jquery");
          var Promise = require("es6-promise").Promise;
          var ESCAPE_MAP = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;",
            "/": "&#47;"
          };
          function escapeHtml(string) {
            return String(string).replace(/[&<>"'\/]/g, function(c) {
              return ESCAPE_MAP[c]
            })
          }
          var gettext = function() {
            if (typeof global.Gettext === "function") {
              var _gettext = new global.Gettext({domain: "annotator"});
              return function(msgid) {
                return _gettext.gettext(msgid)
              }
            }
            return function(msgid) {
              return msgid
            }
          }();
          function mousePosition(event) {
            var body = global.document.body || $("body");
            var offset = {
              top: 0,
              left: 0
            };
            if ($(body).css("position") !== "static") {
              offset = $(body).offset()
            }
            return {
              top: event.pageY - offset.top,
              left: event.pageX - offset.left
            }
          }
          exports.$ = $;
          exports.Promise = Promise;
          exports.gettext = gettext;
          exports.escapeHtml = escapeHtml;
          exports.mousePosition = mousePosition
        }).call(this, typeof global !== "undefined"
          ? global
          : typeof self !== "undefined"
            ? self
            : typeof window !== "undefined"
              ? window
              : {})
      }, {
        "es6-promise": 5,
        jquery: 17
      }
    ]
  }, {}, [1])(1)
});
