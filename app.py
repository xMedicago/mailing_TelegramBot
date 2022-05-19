if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    import logging
    logging.basicConfig(level=logging.INFO)

    executor.start_polling(dp, skip_updates=True)
