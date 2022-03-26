package main

import (
	"os"

	. "otasukecat/mod"

	"github.com/joho/godotenv"
)

var Log LogEx

func init() {
	Log = LogInit("")
}

func main() {
	loadEnv()

	token := os.Getenv("BOT_TOKEN")
	botName := "<@" + os.Getenv("CLIENT_ID") + ">"

	Log.Info("Bot token: ", token)
	Log.Info("Client ID: ", botName)
}

func loadEnv() {
	err := godotenv.Load(".env")

	if err != nil {
		Log.Error(".env読み込みエラー: ", err)
		return
	}
	Log.Success(".envを読み込みました。")
}
