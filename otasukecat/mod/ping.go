package mod

import (
	. "otasukecat/lib"

	"github.com/bwmarrin/discordgo"
)

var Log = LogInit("")

/*
	Ping値の送信
*/
func Ping(s *discordgo.Session, i *discordgo.InteractionCreate) {
	Log.Info("Pong! (" + s.HeartbeatLatency().String() + ")")

	s.InteractionRespond(i.Interaction, &discordgo.InteractionResponse{
		Type: discordgo.InteractionResponseChannelMessageWithSource,
		Data: &discordgo.InteractionResponseData{
			Content: "Pong! (" + s.HeartbeatLatency().String() + ")",
		},
	})
}
