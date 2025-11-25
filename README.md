# SMG -> S(Crappy) Meta Glasses
Have you ever been lost in a conversation? Trying to keep up with all the lingo and jargon? Shitty Meta Glasses is here to help. Packaged with John Blockchain himself, you'll find a convenient package that listens to your conversation and tells you what to say in response. Provide bullcrap answers with confidence, for you will become a 10X networker immediately.

# IRL
<img src="images/irl.jpg" alt="SMG IRL" width="400"/>

# Infrastructure
<img src="images/infra.png" alt="SMG Infra" width="400"/>

Okay so basically we needed to communicate between our phone and the esp32, as we didnt have a mic on hand and needed to use the phone mic. We ended up using a Flask server. This worked fine on localhost, but when connecting via phone, we needed https to allow the speech recognition to work. We couldn't really set up our own certificate, so we used ngrok to tunnel our local connection and make https available for our phone.

Tbh this was more software than hardware. Still fun though.

# CAD
<img src="images/image.png" alt="SMG CAD" width="400"/>
<img src="images/image1.png" alt="SMG CAD" width="400"/>

# Wiring Schematic
<img src="images/wiring diagram.png" alt="SMG Wiring Schematic" width="400"/>

# Bill of Materials
| Part                        | Quantity | Price | Total | Link |
|-----------------------------|----------|-------|-------|------|
| Safety Glasses              | 1        | $1.60 | $1.60 | https://www.aliexpress.us/item/3256805686684104.html?spm=a2g0o.productlist.main.19.3f523f71i1sVge&algo_pvid=0cc368ec-2b2d-4236-aa37-d75b5ead5cf2&algo_exp_id=0cc368ec-2b2d-4236-aa37-d75b5ead5cf2-16&pdp_ext_f=%7B%22order%22%3A%22836%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21USD%213.26%211.60%21%21%2123.25%2111.39%21%402101d9ee17525022372377236eaf63%2112000034654960924%21sea%21US%214343322020%21X&curPageLogUid=ml0dLczIzTQq&utparam-url=scene%3Asearch%7Cquery_from%3A |
| Hot Glue Gun                | 1        | N/A | N/A | N/A | 
| Lolin Esp32 MCU             | 1        | $2.61 | $2.61 | https://www.aliexpress.us/item/3256807691590176.html?spm=a2g0o.productlist.main.14.5db42c05WGsWsj&utparam-url=scene%3Asearch%7Cquery_from%3Apc_back_same_best&algo_pvid=845404b0-32d4-41ab-9d2e-372eacefe656&algo_exp_id=845404b0-32d4-41ab-9d2e-372eacefe656&pdp_ext_f=%7B%22order%22%3A%225010%22%7D&pdp_npi=4%40dis%21USD%212.78%212.61%21%21%212.78%212.61%21%4021030ea417525024021968404e352b%2112000042669746256%21sea%21US%214343322020%21X&gatewayAdapt=4itemAdapt |
| 128x32 0.91" OLED Display   | 1        | $1.53 | $1.53 | https://www.aliexpress.us/item/3256806780992114.html?spm=a2g0o.productlist.main.3.4c3241b5zWYqh3&algo_pvid=43267f9c-f85d-4d9c-b01f-7917a0e6950c&algo_exp_id=43267f9c-f85d-4d9c-b01f-7917a0e6950c-2&pdp_ext_f=%7B%22order%22%3A%2215498%22%2C%22eval%22%3A%221%22%2C%22orig_sl_item_id%22%3A%221005006967306866%22%2C%22orig_item_id%22%3A%221005007799591290%22%7D&pdp_npi=4%40dis%21USD%213.40%211.53%21%21%2124.28%2110.93%21%402101c5b117525021308841080e8543%2112000038886103097%21sea%21US%214343322020%21X&curPageLogUid=KDqyXYDu7H9H&utparam-url=scene%3Asearch%7Cquery_from%3A |
| Large Push Button           | 1        | $1.63 | $1.63 | https://www.aliexpress.us/item/3256807605034530.html?spm=a2g0o.productlist.main.2.36c13cad5fp3jU&algo_pvid=f88770b4-209e-4a2e-b7e1-45b2cf2e4d7e&algo_exp_id=f88770b4-209e-4a2e-b7e1-45b2cf2e4d7e-1&pdp_ext_f=%7B%22order%22%3A%221402%22%2C%22eval%22%3A%221%22%2C%22orig_sl_item_id%22%3A%221005007791349282%22%2C%22orig_item_id%22%3A%221005007385778531%22%7D&pdp_npi=4%40dis%21USD%213.63%211.63%21%21%2125.90%2111.65%21%402101c5a417525025926126411e5fea%2112000042214650600%21sea%21US%214343322020%21X&curPageLogUid=IJUuQu1tVwfp&utparam-url=scene%3Asearch%7Cquery_from%3A |
| Dupont jumpers Pack          | 15       | $1.14 | $1.14 | https://www.aliexpress.us/item/3256806885766712.html?spm=a2g0o.productlist.main.14.eb799502JGFRUz&utparam-url=scene%3Asearch%7Cquery_from%3Apc_back_same_best&algo_pvid=a0d64b4a-875a-49b3-ace8-46a5ef8a482e&algo_exp_id=a0d64b4a-875a-49b3-ace8-46a5ef8a482e&pdp_ext_f=%7B%22order%22%3A%2212434%22%7D&pdp_npi=4%40dis%21USD%213.79%211.14%21%21%2127.00%218.10%21%402103273e17525024532606806e6c74%2112000039311521756%21sea%21US%214343322020%21X&gatewayAdapt=4itemAdapt |
| USB-C Cable                 | 1        | $1.67 | 1.67 | https://www.aliexpress.us/item/3256807238622106.html?spm=a2g0o.productlist.main.14.6ae3192eljYvJg&utparam-url=scene%3Asearch%7Cquery_from%3Apc_back_same_best&algo_pvid=f319f592-0b36-4681-95c4-d08a18297192&algo_exp_id=f319f592-0b36-4681-95c4-d08a18297192&pdp_ext_f=%7B%22order%22%3A%225051%22%7D&pdp_npi=4%40dis%21USD%211.70%211.67%21%21%211.70%211.67%21%402103273e17525025252698782e6c74%2112000040709456625%21sea%21US%214343322020%21X&gatewayAdapt=4itemAdapt |
