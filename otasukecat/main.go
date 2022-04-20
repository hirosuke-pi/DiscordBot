package main

import (
	"flag"
	"os"
	"os/signal"
	"syscall"

	"otasukecat/lib"
	"otasukecat/mod"

	"github.com/bwmarrin/discordgo"
	"github.com/joho/godotenv"
)

// コマンド内容
var (
	// コマンドとその説明
	Commands = []*discordgo.ApplicationCommand{
		{
			Name:        "ping",
			Description: "接続状況をみるよ！",
		},
		{
			Name:        "cmd",
			Description: "Command",
		},
	}

	// 実行されるコマンド
	CommandHandlers = map[string]func(s *discordgo.Session, i *discordgo.InteractionCreate){
		"ping": mod.Ping,
	}
)

// 固定値
var (
	GuildID        = flag.String("guild", "", "Test guild ID. If not passed - bot registers commands globally")
	RemoveCommands = flag.Bool("rmcmd", true, "Remove all commands after shutdowning or not")
)

var (
	BotToken string
	BotName  string
)

var (
	Log        = lib.LogInit("")
	BotSession *discordgo.Session
)

/*
	グローバル変数初期化
*/
func init() {
	loadEnv()
	BotToken = "Bot " + os.Getenv("BOT_TOKEN")
	BotName = "<@" + os.Getenv("CLIENT_ID") + ">"

	Log.Info("Bot token:", BotToken)
	Log.Info("Client ID:", BotName)
}

/*
	Discordに接続
*/
func init() {
	// Discrod認証
	session, err := discordgo.New(BotToken)
	if err != nil {
		Log.Error("ログインに失敗しました:", err)
		panic(1)
	}

	// イベントハンドラ追加
	session.AddHandler(func(s *discordgo.Session, r *discordgo.Ready) {
		Log.Success("ログインしました:", s.State.User.Username+"#"+s.State.User.Discriminator)
	})
	session.AddHandler(func(s *discordgo.Session, i *discordgo.InteractionCreate) {
		if h, ok := CommandHandlers[i.ApplicationCommandData().Name]; ok {
			h(s, i)
		}
	})

	// セッション確立
	err = session.Open()
	if err != nil {
		Log.Error("コネクション確立に失敗しました:", err)
		panic(0)
	}

	BotSession = session
}

/*
	コマンド追加、削除処理
*/
func main() {
	defer BotSession.Close()

	// コマンド追加処理
	registeredCommands := make([]*discordgo.ApplicationCommand, len(Commands))
	for i, v := range Commands {
		cmd, err := BotSession.ApplicationCommandCreate(BotSession.State.User.ID, *GuildID, v)
		if err != nil {
			Log.Error("コマンド '"+v.Name+"' の作成に失敗しました:", err)
		}
		registeredCommands[i] = cmd
	}

	// サーバーと同期
	stopBot := make(chan os.Signal, 1)
	signal.Notify(stopBot, syscall.SIGINT, syscall.SIGTERM, os.Interrupt, os.Kill)
	<-stopBot

	// 登録されているコマンド削除
	if *RemoveCommands {
		Log.Info("コマンド削除中...")
		for _, v := range registeredCommands {
			err := BotSession.ApplicationCommandDelete(BotSession.State.User.ID, *GuildID, v.ID)
			if err != nil {
				Log.Error("コマンド '"+v.Name+"' の削除に失敗しました:", err)
			}
		}
	}
}

/*
	.envファイル読み込み
*/
func loadEnv() {
	err := godotenv.Load(".env")

	if err != nil {
		Log.Error(".env読み込みエラー: ", err)
		panic(1)
	}
	Log.Success(".envを読み込みました。")
}
