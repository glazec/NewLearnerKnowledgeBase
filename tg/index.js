const TelegramBot = require("node-telegram-bot-api");
const axios = require("axios");

async function search(message) {
  try {
    const response = await axios.get(
      "https://newlearnersearch.inevitable.tech/api/query",
      {
        params: {
          query: message,
        },
      }
    );

    if (response.data && Object.keys(response.data).length > 0) {
      console.log(response.data);
      return response.data;
    } else {
      return "Sorry, I don't understand";
    }
  } catch (error) {
    console.error(`Error: ${error}`);
    return "Sorry, an error occurred";
  }
}

async function main() {
  // Replace 'YOUR_TELEGRAM_BOT_TOKEN' with the token you obtained from BotFather.
  const token = process.env.newlearner_knowledge_bot;
  // Create a new Telegram bot instance
  const bot = new TelegramBot(token, { polling: true });

  // Listen for incoming messages
  bot.on("message", async (msg) => {
    const chatId = msg.chat.id;
    const message = msg.text;
    if (message) {
      // send typing event
      bot.sendChatAction(chatId, "typing");
      try {
        const response = await search(message);
        for (let i = 0; i < response.matches.length; i++) {
          await bot.sendMessage(
            chatId,
            `=========结果 ${i + 1} 相关性 ${
              response.matches[i].score
            }=========\n` + response.matches[i].text,
            {
              parse_mode: "Markdown",
              // reply_to_message_id: msg.message_id,
              reply_markup: {
                inline_keyboard: [
                  [
                    {
                      text: "点赞",
                      callback_data: "like",
                    },
                    {
                      text: "差评",
                      callback_data: "dislike",
                    },
                  ],
                ],
              },
            }
          );
          // wait for 1 second
          await new Promise((resolve) => setTimeout(resolve, 1000));
          // add action button to the message
        }
      } catch (error) {
        console.error(`Error: ${error}`);
        bot.sendMessage(chatId, "反馈开发者 @glazecl \nchatid: " + chatId);
      }
    }
  });

  bot.on("callback_query", async (msg) => {
    const chatId = msg.message.chat.id;
    const messageId = msg.message.message_id;
    const data = msg.data;
    if (data === "like") {
      bot.sendMessage(chatId, "感谢您的反馈");
    } else if (data === "dislike") {
      bot.sendMessage(chatId, "感谢您的反馈");
      bot.deleteMessage(chatId, messageId);
    }
  });
}
main();
