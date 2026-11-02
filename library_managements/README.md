# Library Borrowing — ORM Practice

သင်ပြီးသား ORM တွေနဲ့ ပြန်ရေးထားတဲ့ လေ့ကျင့်ရန် module ဖြစ်သည်။
Book record တစ်ခု = ငှားလို့ရတဲ့ တကယ့်စာအုပ်တစ်အုပ်။

## ဖတ်ရမယ့်အစဉ်

1. `models/library_book.py` — One2many၊ filtered()၊ computed field၊ @api.depends၊ @api.ondelete။
2. `models/library_member.py` — One2many၊ filtered()၊ len() နဲ့ ငှားထားတဲ့အရေအတွက်တွက်ခြင်း။
3. `models/library_loan.py` ရဲ့ fields — Many2one နဲ့ Selection။
4. အောက်ဆုံးက `action_borrow()`၊ `action_return()`၊ `action_cancel()` — ensure_one() နဲ့ write()။
5. `write()` override — for / if / search() / mapped() / len() နဲ့ စည်းကမ်းစစ်ပြီး super().write(vals) ကို ခေါ်ခြင်း။
6. `create()` override — @api.model_create_multi၊ vals_list နဲ့ super().create()။
7. `_check_dates()` နဲ့ `_unlink_except_draft()` — @api.constrains နဲ့ @api.ondelete။

ဥပမာ Borrow နှိပ်တဲ့ flow:

```text
Borrow button
  -> action_borrow()
  -> self.ensure_one()
  -> self.write({'state': 'borrowed'})
  -> ကိုယ်ရေးထားတဲ့ write() override ထဲဝင်
  -> Draft လား၊ member active လား၊ due date မှန်လား စစ်
  -> search() နဲ့ စာအုပ်ကို ငှားထားပြီးပြီလား စစ်
  -> Borrow Date ဖြည့်
  -> super().write(vals) က database မှာ သိမ်း
  -> Book availability နဲ့ Member count ပြန်တွက်
```

`dict(vals)` က ဝင်လာတဲ့ dictionary ကို copy ယူခြင်းဖြစ်သည်။
`vals.get('state', 'draft')` က state ရှိရင် အဲဒီတန်ဖိုးကိုယူပြီး မရှိရင် draft ကို ယူခြင်းဖြစ်သည်။
`fields.Date.context_today(self)` က အသုံးပြုသူရဲ့ timezone အရ ဒီနေ့ရက်ကို ယူခြင်းဖြစ်သည်။
`return True` က button method အောင်မြင်စွာပြီးဆုံးကြောင်း ပြန်ပေးခြင်းဖြစ်သည်။

## အသုံးပြုရန်

1. `library_management` folder ကို custom addons path ထဲ ထည့်ပါ။ အရင် module ရှိရင် backup အရင်ယူပါ။
2. Odoo restart လုပ်ပြီး Apps မှာ Library Borrowing ကို install / upgrade လုပ်ပါ။
3. Library → Members မှာ member နှစ်ယောက် ဖန်တီးပါ။
4. Library → Books မှာ စာအုပ်တစ်အုပ် ဖန်တီးပါ။
5. Library → Loans မှာ Loan Number၊ Member၊ Book နဲ့ Due Date ဖြည့်ပြီး save လုပ်ပါ။
6. Borrow → Return ကို စမ်းပါ။ Draft မှာ Cancel လည်း စမ်းပါ။

## စစ်ရမယ့်ရလဒ်

- Draft → Borrowed → Returned သို့မဟုတ် Draft → Cancelled ဖြစ်ရမည်။
- Borrow လုပ်ရင် Book Available = False၊ Member Books Borrowed = 1 ဖြစ်ရမည်။
- ငှားထားပြီးတဲ့စာအုပ်ကို နောက် loan တစ်ခုက ငှားရင် error ပြရမည်။
- Return လုပ်ရင် Available = True၊ count = 0 ပြန်ဖြစ်ရမည်။ အခြား member က ငှားလို့ရပြီ။
- Inactive member နဲ့ အတိတ် Due Date ကို Borrow မလုပ်ရ။
- Draft loan ကိုပဲ ပြင် / ဖျက်နိုင်ရမည်။
- Loan history ရှိတဲ့ Book / Member ကို ဖျက်မရ။

## လေ့ကျင့်ရေးအတိုင်းအတာ

ဒီ version မှာ သင်ပြီးသား search() နဲ့ ငှားထားပြီးလားစစ်ထားသည်။
အသုံးပြုသူနှစ်ယောက်က တစ်ချိန်တည်း Borrow လုပ်ခြင်းကို database level မှာ တားတဲ့ unique index မပါပါ။
လက်တွေ့ multi-user စနစ်အဖြစ် သုံးမယ်ဆို အဲဒီအပိုင်းကို ဆက်ထည့်ဖို့လိုသည်။
အရင်ပေးထားတဲ့ advanced version ကို upgrade လုပ်ပြီးသားဆို database ထဲက unique index ကို ဒီ version က အလိုအလျောက်မဖျက်ပါ။
