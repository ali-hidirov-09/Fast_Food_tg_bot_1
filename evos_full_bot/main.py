from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import methods
from database import Database
from register import check
from messages import message_handler
from inlines import inline_handler
import globals
from config import ADMIN_IDS, token

Token=token

db = Database("fast_food.db")


def start_handler(update, context):
    check(update, context)


def contact_handler(update, context):
    message = update.message.contact.phone_number
    user = update.message.from_user
    db.update_user_data(user.id, "phone_number",message)
    check(update,context)



import html
import telegram
def location_handler(update, context):
    db_user = db.get_user_by_chat_id(update.message.from_user.id)
    location = update.message.location

    carts = context.user_data.get("carts", {})
    payment_type = context.user_data.get("payment_type", None)

    # 1) agar savatcha bo'sh bo'lsa — xabar berib menu qaytarish
    if not carts:
        update.message.reply_text(globals.BUYURTMA_EMPTY[db_user['lang_id']] if hasattr(globals, 'BUYURTMA_EMPTY') else "Sizning savatchangiz bo'sh.")
        methods.send_main_menu(context, update.message.from_user.id, db_user['lang_id'])
        return

    # 2) DB ga buyurtma yozish
    # Misol: db.create_order(user_id, carts, payment_type, latitude, longitude)
    lat = getattr(location, "latitude", None)
    lon = getattr(location, "longitude", None)
    # Agar create_order location obyektni qabul qilsa
    try:
        # agar DB lat,long kutsa:
        db.create_order(db_user['id'], carts, payment_type, lat, lon)
    except TypeError:
        # fallback: agar u location obyektini qabul qilsa
        db.create_order(db_user['id'], carts, payment_type, location)

    # 3) Buyurtma matnini tayyorlash
    lang_code = globals.LANGUAGE_CODE[db_user['lang_id']]
    total_price = 0
    text_lines = []
    for cart, val in carts.items():
        product = db.get_product_for_cart(int(cart))
        name = f"{product.get(f'cat_name_{lang_code}','')} {product.get(f'name_{lang_code}','')}"
        text_lines.append(f"{val} x {name}")
        total_price += product.get('price', 0) * val

    payment_text = ("Naqd pul" if payment_type == 1 else "Kaspi KZ" if payment_type == 2 else "Noma'lum")
    order_text = "\n".join(text_lines)
    order_text += f"\n{globals.ALL[db_user['lang_id']]}: {total_price} {globals.SUM[db_user['lang_id']]}"

    # 4) Foydalanuvchiga tasdiq
    update.message.reply_text(globals.BUYURTMA[db_user['lang_id']])

    # 5) Adminlarga yuborish — HTML ga moslab escape qilish
    safe_first = html.escape(str(db_user.get('first_name','')))
    safe_last = html.escape(str(db_user.get('last_name','')))
    safe_phone = html.escape(str(db_user.get('phone_number','')))
    safe_lang = html.escape(str(globals.LANGUAGE_CODE[db_user['lang_id']]))
    safe_order_text = html.escape(order_text).replace("\n", "\n")

    admin_msg = (
        f"<b>Янги буюртма:</b>\n\n"
        f"👤 <b>Исм-фамилия:</b> {safe_first} {safe_last}\n"
        f"📞 <b>Телефон рақам:</b> {safe_phone}\n"
        f"🌐 <b>Тили:</b> {safe_lang}\n"
        f"💳 <b>Тўлов тури:</b> {html.escape(payment_text)}\n\n"
        f"📥 <b>Буюртма:</b>\n{safe_order_text}"
    )

    for admin in ADMIN_IDS:
        try:
            context.bot.send_message(chat_id=admin, text=admin_msg, parse_mode='HTML')
        except telegram.error.TelegramError:
            # log qiling yoki pass
            pass

    # 6) Adminlarga lokatsiyani yuborish (agar kerak bo'lsa)
    if lat is not None and lon is not None:
        for admin in ADMIN_IDS:
            try:
                context.bot.send_location(chat_id=admin, latitude=float(lat), longitude=float(lon))
            except Exception:
                pass

    # 7) Tozalash va menyuga qaytarish
    context.user_data.pop("carts", None)
    methods.send_main_menu(context, update.message.from_user.id, db_user['lang_id'])





# # lesson-4 #############
# def location_handler(update, context):
#     db_user = db.get_user_by_chat_id(update.message.from_user.id)
#     location = update.message.location
#     payment_type = context.user_data.get("payment_type", None)
#     db.create_order(db_user['id'], context.user_data.get("carts", {}), payment_type, location)
#
#     if context.user_data.get("carts", {}):
#         carts = context.user_data.get("carts")
#         text = "\n"
#         lang_code = globals.LANGUAGE_CODE[db_user['lang_id']]
#         total_price = 0
#         for cart, val in carts.items():
#             product = db.get_product_for_cart(int(cart))
#             text += f"{val} x {product[f'cat_name_{lang_code}']} {product[f'name_{lang_code}']}\n"
#             total_price += product['price'] * val
#
#         payment_type = context.user_data.get("payment_type")
#         if payment_type == 1:
#             payment_text = "Naqd pul"
#         elif payment_type == 2:
#             payment_text = "Kaspi KZ"
#         else:
#             payment_text = "Noma'lum"
#
#         text += f"\n{globals.ALL[db_user['lang_id']]}: {total_price} {globals.SUM[db_user['lang_id']]}"
#     update.message.reply_text(f"{globals.BUYURTMA[db_user['lang_id']]}")
#     for admin in ADMIN_IDS:
#         context.bot.send_message(
#             chat_id=admin,
#             text=f"<b>Янги буюртма:</b>\n\n"
#                  f"👤 <b>Исм-фамилия:</b> {db_user['first_name']} {db_user['last_name']}\n"
#                  f"📞 <b>Телефон рақам:</b> {db_user['phone_number']} \n"
#                  f"   <b>Тили:</b> {globals.LANGUAGE_CODE[db_user['lang_id']]}\n"
#                  f"💳 <b>Тўлов тури:</b> {payment_text}\n\n"
#                  f"📥 <b>Буюртма:</b> \n"
#                  f"{text}",
#             parse_mode='HTML'
#         )
#         context.user_data.pop("carts", None)
#
#     for admin in ADMIN_IDS:
#         context.bot.send_location(
#             chat_id=admin,
#             latitude=float(location.latitude),
#             longitude=float(location.longitude)
#         )
#     methods.send_main_menu(context, update.message.from_user.id, db_user['lang_id'])
# ########################
#


def main():
    updater = Updater(Token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))
    dispatcher.add_handler(MessageHandler(Filters.location, location_handler))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
