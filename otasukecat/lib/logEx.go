package lib

import (
	"log"
	"os"
)

func LogInit(prefix string) LogEx {
	const LOG_FLAG = log.LstdFlags | log.Ldate | log.Ltime | log.Lmicroseconds
	return LogEx{
		succ: log.New(os.Stdout, prefix, LOG_FLAG),
		warn: log.New(os.Stdout, prefix, LOG_FLAG),
		err:  log.New(os.Stdout, prefix, LOG_FLAG),
		info: log.New(os.Stdout, prefix, LOG_FLAG),
	}
}

type LogEx struct {
	succ *log.Logger
	warn *log.Logger
	err  *log.Logger
	info *log.Logger
}

func (l LogEx) Success(s ...any) {
	l.succ.Println(append([]any{"[+]"}, s...)...)
}

func (l LogEx) Warning(s ...any) {
	l.warn.Println(append([]any{"[!]"}, s...)...)
}

func (l LogEx) Error(s ...any) {
	l.err.Println(append([]any{"[-]"}, s...)...)
}

func (l LogEx) Info(s ...any) {
	l.info.Println(append([]any{"[*]"}, s...)...)
}
