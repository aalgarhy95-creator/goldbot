import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# التوكين الخاص بك جاهز هنا
TOKEN = "754246823:AAHuXl79bWVNXcVY16-Z8IrvYWhvOxxobkg"

# أمر الترحيب /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "أهلاً بك يا أستاذ أحمد في مساعد التداول الذكي! 📈\n\n"
        "الأوامر المتاحة حالياً:\n"
        "📍 /gold - لجلب سعر الذهب اللحظي (XAU/USD)\n"
        "📍 /forex - لجلب أسعار العملات الرئيسية مقابل الدولار\n"
        "📍 /help - للمساعدة والدعم"
    )
    await update.message.reply_text(welcome_msg)

# أمر جلب سعر الذهب /gold
async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ جاري جلب سعر الذهب المباشر...")
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/XAU")
        data = response.json()
        usd_price = round(1 / data['rates']['USD'], 2)
        
        msg = f"🏆 **سعر الذهب الحالي (XAU/USD):**\n\n💰 **${usd_price}** للأونصة.\n\n💡 *ملاحظة:* يفضل متابعة فترة تداخل جلسة لندن ونيويورك للحصول على أفضل السيولة."
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ أثناء جلب البيانات، يرجى المحاولة لاحقاً.")

# أمر جلب أسعار العملات /forex
async def forex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ جاري جلب أسعار العملات الرئيسية...")
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        eur = round(1 / data['rates']['EUR'], 4)
        gbp = round(1 / data['rates']['GBP'], 4)
        
        msg = (
            "💱 **أسعار العملات مقابل الدولار (USD):**\n\n"
            f"🇪🇺 EUR/USD: **{eur}**\n"
            f"🇬🇧 GBP/USD: **{gbp}**\n"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ أثناء جلب البيانات.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gold", gold))
    app.add_handler(CommandHandler("forex", forex))
    
    print("البوت يعمل الآن بنجاح...")
    app.run_polling()
