package main

import (
	"flag"
	"fmt"
	"log"
	"os/user"
	"path/filepath"

	"github.com/kkdai/youtube"
)

func main() {
	flag.Parse()
	log.Println(flag.Args())
	usr, _ := user.Current()
	currentDir := fmt.Sprintf("%v/Desktop", usr.HomeDir)
	log.Println("download to dir=", currentDir)
	y := youtube.NewYoutube(true)
	arg := flag.Arg(0)
	if err := y.DecodeURL(arg); err != nil {
		fmt.Println("err:", err)
	}
	if err := y.StartDownload(filepath.Join(currentDir, "dl.mp4")); err != nil {
		fmt.Println("err:", err)
	}
}
