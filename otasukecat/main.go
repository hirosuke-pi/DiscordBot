package main

import (
	"flag"
	"log"
	"os"
	"os/signal"
	"syscall"

	. "otasukecat/mod"

	"github.com/bwmarrin/discordgo"
	"github.com/joho/godotenv"
)

var Log LogEx
var Commands = []*discordgo.ApplicationCommand{
	{
		Name:        "test",
		Description: "Test Command",
	},
	{
		Name:        "cmd",
		Description: "Command",
	},
}

var (
	GuildID        = flag.String("guild", "", "Test guild ID. If not passed - bot registers commands globally")
	RemoveCommands = flag.Bool("rmcmd", true, "Remove all commands after shutdowning or not")
)

func init() {
	Log = LogInit("")
}

func main() {
	loadEnv()

	token := "Bot " + os.Getenv("BOT_TOKEN")
	botName := "<@" + os.Getenv("CLIENT_ID") + ">"
	commandHandlers := map[string]func(s *discordgo.Session, i *discordgo.InteractionCreate){
		"test": func(s *discordgo.Session, i *discordgo.InteractionCreate) {
			s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
				Type: discordgo.InteractionResponseChannelMessageWithSource,
				Data: &discordgo.InteractionResponseData{
					Content: "test",
				},
			})
		},
		"cmd": func(s *discordgo.Session, i *discordgo.InteractionCreate) {
			s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
				Type: discordgo.InteractionResponseChannelMessageWithSource,
				Data: &discordgo.InteractionResponseData{
					Content: "cmd",
				},
			})
		},
	}

	Log.Info("Bot token:", token)
	Log.Info("Client ID:", botName)

	// Discrod接続
	discord, err := discordgo.New(token)
	if err != nil {
		Log.Error("ログインに失敗しました:", err)
		return
	}

	// イベントハンドラ追加
	discord.AddHandler(func(s *discordgo.Session, r *discordgo.Ready) {
		Log.Success("ログインしました:", s.State.User.Username+"#"+s.State.User.Discriminator)
	})
	discord.AddHandler(func(s *discordgo.Session, i *discordgo.InteractionCreate) {
		if h, ok := commandHandlers[i.ApplicationCommandData().Name]; ok {
			h(s, i)
		}
	})

	err = discord.Open()
	if err != nil {
		Log.Error("コネクション確立に失敗しました:", err)
	}

	defer discord.Close()

	// コマンド追加処理
	registeredCommands := make([]*discordgo.ApplicationCommand, len(Commands))
	for i, v := range Commands {
		cmd, err := discord.ApplicationCommandCreate(discord.State.User.ID, *GuildID, v)
		if err != nil {
			Log.Error("Cannot create '%v' command: %v", v.Name, err)
		}
		registeredCommands[i] = cmd
	}

	stopBot := make(chan os.Signal, 1)
	signal.Notify(stopBot, syscall.SIGINT, syscall.SIGTERM, os.Interrupt, os.Kill)
	<-stopBot

	if *RemoveCommands {
		Log.Info("コマンド削除中...")
		for _, v := range registeredCommands {
			err := discord.ApplicationCommandDelete(discord.State.User.ID, *GuildID, v.ID)
			if err != nil {
				log.Panicf("Cannot delete '%v' command: %v", v.Name, err)
			}
		}
	}
}

func loadEnv() {
	err := godotenv.Load(".env")

	if err != nil {
		Log.Error(".env読み込みエラー: ", err)
		return
	}
	Log.Success(".envを読み込みました。")
}
