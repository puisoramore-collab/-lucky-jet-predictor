import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

results = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 LUCKY JET ANALYZER\n\n"
        "/add 1.50 - Adauga un rezultat\n"
        "/stats - Analiza statistică\n"
        "/history - Ultimele rezultate"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        x = float(context.args[0])

        if x < 1:
            raise ValueError()

        results.append(x)

        await update.message.reply_text(
            f"✅ Rezultat adăugat: {x}x"
        )
    except (ValueError, IndexError):
        await update.message.reply_text(
            "Folosește: /add 1.50"
        )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not results:
        await update.message.reply_text(
            "Nu există rezultate încă."
        )
        return

    average = sum(results) / len(results)
    low = sum(x < 2 for x in results)
    high = sum(x >= 2 for x in results)

    await update.message.reply_text(
        f"📊 ANALIZA LUCKY JET\n\n"
        f"Runde analizate: {len(results)}\n"
        f"Media: {average:.2f}x\n"
        f"Sub 2x: {low}\n"
        f"Peste sau egal cu 2x: {high}\n\n"
        "⚠️ Statisticile nu prezic următoarea rundă."
    )

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 Ultimele rezultate:\n" +
        str(results[-20:])
        
            )


def main():
    token = os.environ["BOT_TOKEN"]
    webhook_url = os.environ["WEBHOOK_URL"].rstrip("/")
    secret = os.environ["WEBHOOK_SECRET"]

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("history", history))
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        url_path="telegram",
        webhook_url=f"{webhook_url}/telegram",
        secret_token=secret
    )


if __name__ == "__main__":
    main()

